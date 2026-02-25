from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_PERIOD = "صباحي"
DEFAULT_TIMEOUT_MS = 120_000
DEFAULT_WAIT_AFTER_ACTION_MS = 1200


@dataclass(frozen=True)
class ViewportProfile:
    key: str
    width: int
    height: int


VIEWPORT_PROFILES: tuple[ViewportProfile, ...] = (
    ViewportProfile("mobile_390x844", 390, 844),
    ViewportProfile("laptop13_1366x768", 1366, 768),
    ViewportProfile("desktop24_1920x1080", 1920, 1080),
    ViewportProfile("desktop27_2560x1440", 2560, 1440),
)


@dataclass
class ResponsiveGateOptions:
    base_url: str
    output_dir: Path
    period: str
    headless: bool
    timeout_ms: int
    wait_after_action_ms: int
    profiles: tuple[ViewportProfile, ...]


def _available_profiles() -> dict[str, ViewportProfile]:
    return {profile.key: profile for profile in VIEWPORT_PROFILES}


def _parse_profiles(value: str) -> tuple[ViewportProfile, ...]:
    selected = []
    lookup = _available_profiles()
    raw_items = [item.strip() for item in (value or "").split(",") if item.strip()]
    if not raw_items or "all" in raw_items:
        return VIEWPORT_PROFILES
    unknown = [item for item in raw_items if item not in lookup]
    if unknown:
        allowed = ", ".join(["all", *lookup.keys()])
        raise ValueError(f"Unknown profile(s): {', '.join(unknown)}. Allowed: {allowed}")
    for item in raw_items:
        selected.append(lookup[item])
    deduped = []
    seen = set()
    for profile in selected:
        if profile.key in seen:
            continue
        seen.add(profile.key)
        deduped.append(profile)
    return tuple(deduped)


def parse_args() -> ResponsiveGateOptions:
    parser = argparse.ArgumentParser(
        description="Responsive UI gate for Morning Classes Check dashboard.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("MC_UI_BASE_URL", DEFAULT_BASE_URL),
        help=f"Dashboard URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Output directory for responsive artifacts. Default: artifacts/responsive/<timestamp>",
    )
    parser.add_argument(
        "--period",
        choices=("صباحي", "مسائي"),
        default=DEFAULT_PERIOD,
        help=f"Period filter before evaluation (default: {DEFAULT_PERIOD})",
    )
    parser.add_argument(
        "--profiles",
        default="all",
        help=(
            "Comma-separated profile keys. Use 'all' for all profiles. "
            f"Available: all, {', '.join(_available_profiles().keys())}"
        ),
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Run browser headless (default: true).",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=DEFAULT_TIMEOUT_MS,
        help=f"Action timeout in milliseconds (default: {DEFAULT_TIMEOUT_MS})",
    )
    parser.add_argument(
        "--wait-after-action-ms",
        type=int,
        default=DEFAULT_WAIT_AFTER_ACTION_MS,
        help=f"Wait after key actions in milliseconds (default: {DEFAULT_WAIT_AFTER_ACTION_MS})",
    )
    args = parser.parse_args()

    try:
        profiles = _parse_profiles(args.profiles)
    except ValueError as exc:
        parser.error(str(exc))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = (
        Path(args.output_dir).expanduser()
        if args.output_dir
        else PROJECT_ROOT / "artifacts" / "responsive" / timestamp
    )
    return ResponsiveGateOptions(
        base_url=args.base_url.rstrip("/"),
        output_dir=output_dir,
        period=args.period,
        headless=bool(args.headless),
        timeout_ms=max(20_000, int(args.timeout_ms)),
        wait_after_action_ms=max(300, int(args.wait_after_action_ms)),
        profiles=profiles,
    )


def _safe_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _eval_rules(
    metrics: dict[str, Any],
    viewport_width: int,
    hidden_metrics: Optional[dict[str, Any]] = None,
) -> list[str]:
    failures: list[str] = []
    doc = metrics.get("doc") or {}
    layout_overflow = metrics.get("layoutOverflow") or {}
    selected = metrics.get("selectedRect") or {}
    controls = metrics.get("controlsRect") or {}
    screens = metrics.get("screensRect") or {}
    heat_wrap = metrics.get("heatWrapRect") or {}
    heat_table = metrics.get("heatTableRect") or {}

    overflow_right = _to_float(layout_overflow.get("maxRightOverflow"))
    if overflow_right is None:
        doc_scroll_width = _to_float(doc.get("scrollWidth")) or 0.0
        doc_client_width = _to_float(doc.get("clientWidth")) or 0.0
        overflow_right = max(0.0, doc_scroll_width - doc_client_width)
    if overflow_right > 2.0:
        failures.append(f"page_horizontal_overflow_right={overflow_right:.2f}px")

    selected_width = _to_float(selected.get("width"))
    controls_width = _to_float(controls.get("width"))
    selected_top = _to_float(selected.get("top"))
    controls_top = _to_float(controls.get("top"))
    controls_visible = bool(metrics.get("controlsVisible"))

    if selected_width is None or selected_width <= 0:
        failures.append("selected_run_panel_missing")

    if viewport_width >= 1060:
        if not controls_visible:
            failures.append("controls_panel_hidden_unexpected_desktop")
        if controls_width is None:
            failures.append("controls_panel_rect_missing_desktop")
        else:
            if controls_width < 300 or controls_width > 520:
                failures.append(f"controls_width_out_of_range_desktop={controls_width:.2f}")
        if selected_width is not None and controls_width is not None:
            if selected_width <= controls_width + 80:
                failures.append("selected_panel_not_wider_than_controls_desktop")
        if selected_top is not None and controls_top is not None:
            if abs(selected_top - controls_top) > 100:
                failures.append("desktop_panels_not_aligned_in_same_row")
    else:
        if selected_top is not None and controls_top is not None:
            if controls_top <= selected_top + 40:
                failures.append("mobile_controls_not_stacked_below_selected")
        if selected_width is not None and controls_width is not None:
            if abs(selected_width - controls_width) > 140:
                failures.append("mobile_column_width_mismatch")

    screens_width = _to_float(screens.get("width"))
    heat_wrap_width = _to_float(heat_wrap.get("width"))
    heat_wrap_height = _to_float(heat_wrap.get("height"))
    if heat_wrap_width is None or heat_wrap_width <= 0:
        failures.append("heatmap_wrap_missing")
    else:
        if heat_wrap_width < 280:
            failures.append(f"heatmap_wrap_too_narrow={heat_wrap_width:.2f}")
        if screens_width and heat_wrap_width < (screens_width * 0.55):
            failures.append("heatmap_wrap_too_small_vs_screens_card")
        if viewport_width >= 1200 and heat_wrap_width < 560:
            failures.append("heatmap_wrap_too_small_desktop")
        if viewport_width >= 1800 and heat_wrap_width < 760:
            failures.append("heatmap_wrap_too_small_large_desktop")
    if heat_wrap_height is not None and heat_wrap_height < 180:
        failures.append(f"heatmap_wrap_too_short={heat_wrap_height:.2f}")

    heat_table_width = _to_float(heat_table.get("width"))
    if heat_wrap_width and heat_table_width:
        if heat_table_width < heat_wrap_width * 0.7:
            failures.append("heatmap_table_too_narrow_vs_wrap")

    if hidden_metrics is not None and viewport_width >= 1060:
        hidden_selected = hidden_metrics.get("selectedRect") or {}
        hidden_doc = hidden_metrics.get("doc") or {}
        hidden_layout_overflow = hidden_metrics.get("layoutOverflow") or {}
        hidden_bento_class = str(hidden_metrics.get("bentoClass") or "")
        hidden_selected_width = _to_float(hidden_selected.get("width"))
        if "controls-hidden" not in hidden_bento_class:
            failures.append("controls_hidden_class_missing_after_toggle")
        if bool(hidden_metrics.get("controlsVisible")):
            failures.append("controls_still_visible_after_toggle")
        if selected_width is not None and hidden_selected_width is not None:
            if hidden_selected_width <= selected_width + 120:
                failures.append("selected_panel_did_not_expand_after_toggle")
        hidden_overflow_right = _to_float(hidden_layout_overflow.get("maxRightOverflow"))
        if hidden_overflow_right is None:
            hidden_overflow_right = (_to_float(hidden_doc.get("scrollWidth")) or 0.0) - (
                _to_float(hidden_doc.get("clientWidth")) or 0.0
            )
        if hidden_overflow_right > 2.0:
            failures.append(
                f"page_horizontal_overflow_after_toggle_right={hidden_overflow_right:.2f}px"
            )

    return failures


def _collect_metrics(page: Any) -> dict[str, Any]:
    return page.evaluate(
        """
        () => {
          const rect = (el) => {
            if (!el) return null;
            const r = el.getBoundingClientRect();
            return {
              x: r.x,
              y: r.y,
              top: r.top,
              left: r.left,
              width: r.width,
              height: r.height,
              right: r.right,
              bottom: r.bottom
            };
          };
          const root = document.documentElement;
          let maxRightOverflow = 0;
          let minLeft = 0;
          for (const el of document.body.querySelectorAll("*")) {
            const style = window.getComputedStyle(el);
            if (style.display === "none" || style.visibility === "hidden") continue;
            const r = el.getBoundingClientRect();
            if (r.width <= 0 || r.height <= 0) continue;
            maxRightOverflow = Math.max(maxRightOverflow, r.right - root.clientWidth);
            minLeft = Math.min(minLeft, r.left);
          }
          const bento = document.querySelector(".bento-grid");
          const selected = document.querySelector(".selected-run");
          const controls = document.querySelector(".controls-panel");
          const screens = document.querySelector(".screens-card");
          const activePanel = document.querySelector(".screen-panel:not([hidden])");
          const heatWrap = activePanel ? activePanel.querySelector(".heatmap-wrap") : null;
          const heatTable = heatWrap ? heatWrap.querySelector(".heatmap-table, .distribution-table") : null;
          const controlsStyle = controls ? window.getComputedStyle(controls) : null;
          const controlsVisible = !!(
            controls &&
            controlsStyle &&
            controlsStyle.display !== "none" &&
            controlsStyle.visibility !== "hidden" &&
            controlsStyle.opacity !== "0"
          );
          return {
            viewport: { width: window.innerWidth, height: window.innerHeight },
            doc: {
              clientWidth: root.clientWidth,
              scrollWidth: root.scrollWidth,
              clientHeight: root.clientHeight,
              scrollHeight: root.scrollHeight
            },
            layoutOverflow: {
              maxRightOverflow: maxRightOverflow,
              minLeft: minLeft
            },
            bentoClass: bento ? bento.className : "",
            activeScreen: activePanel ? activePanel.getAttribute("data-screen-panel") : null,
            controlsVisible,
            selectedRect: rect(selected),
            controlsRect: rect(controls),
            screensRect: rect(screens),
            heatWrapRect: rect(heatWrap),
            heatTableRect: rect(heatTable)
          };
        }
        """
    )


def _run_single_profile(
    context: Any,
    opts: ResponsiveGateOptions,
    profile: ViewportProfile,
) -> dict[str, Any]:
    page = context.new_page()
    page.set_default_timeout(opts.timeout_ms)
    page.goto(opts.base_url, wait_until="domcontentloaded")
    page.wait_for_selector(".bento-grid", state="visible")
    page.wait_for_selector("#globalPeriod", state="visible")
    page.wait_for_selector("#heatmapPeriodFilter", state="visible")
    page.wait_for_timeout(opts.wait_after_action_ms)

    page.select_option("#globalPeriod", opts.period)
    page.wait_for_timeout(450)
    page.select_option("#heatmapPeriodFilter", opts.period)
    page.wait_for_timeout(650)

    run_count = page.locator(".run-item").count()
    page.evaluate("window.scrollTo({ top: 0, behavior: 'auto' });")
    page.wait_for_timeout(200)

    before = _collect_metrics(page)
    hidden = None

    toggle_button = page.locator("#toggleControlsPanel")
    if profile.width >= 1060 and toggle_button.count() > 0:
        toggle_button.click()
        page.wait_for_timeout(450)
        hidden = _collect_metrics(page)
        toggle_button.click()
        page.wait_for_timeout(350)

    full_page = opts.output_dir / f"{profile.key}_full.png"
    screens_shot = opts.output_dir / f"{profile.key}_screens_card.png"
    page.screenshot(path=str(full_page), full_page=True)
    page.locator(".screens-card").screenshot(path=str(screens_shot))

    failures = _eval_rules(before, profile.width, hidden_metrics=hidden)
    return {
        "profile": asdict(profile),
        "run_items_count": run_count,
        "metrics": before,
        "metrics_controls_hidden": hidden,
        "failures": failures,
        "screenshots": {
            "full_page": str(full_page),
            "screens_card": str(screens_shot),
        },
    }


def run_gate(opts: ResponsiveGateOptions) -> int:
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright is not installed in this environment.\n"
            "Install steps:\n"
            "1) source /Users/malmabar/Documents/MornningClassesCheck/.venv/bin/activate\n"
            "2) pip install playwright\n"
            "3) python -m playwright install chromium",
            file=sys.stderr,
        )
        return 2

    opts.output_dir.mkdir(parents=True, exist_ok=True)
    report: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "base_url": opts.base_url,
        "period": opts.period,
        "headless": opts.headless,
        "timeout_ms": opts.timeout_ms,
        "wait_after_action_ms": opts.wait_after_action_ms,
        "profiles": [profile.key for profile in opts.profiles],
        "results": [],
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=opts.headless)
            try:
                for profile in opts.profiles:
                    context = browser.new_context(
                        viewport={"width": profile.width, "height": profile.height},
                        locale="ar-SA",
                        timezone_id="Asia/Riyadh",
                    )
                    try:
                        result = _run_single_profile(context, opts, profile)
                    finally:
                        context.close()
                    report["results"].append(result)
            finally:
                browser.close()
    except PlaywrightTimeoutError as exc:
        report["status"] = "FAILED"
        report["error"] = f"playwright_timeout: {exc}"
        _safe_write_json(opts.output_dir / "responsive_report.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1
    except Exception as exc:
        report["status"] = "FAILED"
        report["error"] = f"unexpected_error: {exc}"
        _safe_write_json(opts.output_dir / "responsive_report.json", report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    all_failures = []
    for result in report["results"]:
        if result.get("failures"):
            all_failures.append(
                {
                    "profile": result["profile"]["key"],
                    "failures": result["failures"],
                }
            )
    report["status"] = "PASSED" if not all_failures else "FAILED"
    report["gate_failures"] = all_failures
    _safe_write_json(opts.output_dir / "responsive_report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASSED" else 1


def main() -> int:
    opts = parse_args()
    return run_gate(opts)


if __name__ == "__main__":
    raise SystemExit(main())
