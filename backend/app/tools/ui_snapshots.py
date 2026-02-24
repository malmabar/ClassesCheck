from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_PERIOD = "صباحي"
DEFAULT_VIEWPORT_WIDTH = 1728
DEFAULT_VIEWPORT_HEIGHT = 980
DEFAULT_TIMEOUT_MS = 120_000
DEFAULT_WAIT_AFTER_ACTION_MS = 1200
SCREEN_TABS: tuple[tuple[str, str], ...] = (
    ("rooms", "القاعات"),
    ("crns", "الشعب"),
    ("trainers", "المدربين"),
    ("distribution", "التوزيع-النسبي"),
)


@dataclass
class SnapshotOptions:
    base_url: str
    output_dir: Path
    period: str
    import_file: Optional[Path]
    semester: Optional[str]
    created_by: str
    headless: bool
    viewport_width: int
    viewport_height: int
    timeout_ms: int
    wait_after_action_ms: int


def parse_args() -> SnapshotOptions:
    parser = argparse.ArgumentParser(
        description="UI visual snapshot automation for Morning Classes Check dashboard.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("MC_UI_BASE_URL", DEFAULT_BASE_URL),
        help=f"Dashboard URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--output-dir",
        default="",
        help="Output directory for screenshots. Default: artifacts/screenshots/<timestamp>",
    )
    parser.add_argument(
        "--period",
        choices=("صباحي", "مسائي"),
        default=DEFAULT_PERIOD,
        help="Period filter to apply before capturing screenshots.",
    )
    parser.add_argument(
        "--import-file",
        default="",
        help="Optional SS01 CSV file path. If passed, script uploads/imports before capture.",
    )
    parser.add_argument(
        "--semester",
        default="",
        help="Semester value for import flow (required with --import-file).",
    )
    parser.add_argument(
        "--created-by",
        default="ui-snapshot-bot",
        help="Value to inject into the operator field before actions.",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Run browser headless (default: true).",
    )
    parser.add_argument(
        "--viewport-width",
        type=int,
        default=DEFAULT_VIEWPORT_WIDTH,
        help=f"Viewport width (default: {DEFAULT_VIEWPORT_WIDTH})",
    )
    parser.add_argument(
        "--viewport-height",
        type=int,
        default=DEFAULT_VIEWPORT_HEIGHT,
        help=f"Viewport height (default: {DEFAULT_VIEWPORT_HEIGHT})",
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

    if args.import_file and not args.semester:
        parser.error("--semester is required when --import-file is provided.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else PROJECT_ROOT / "artifacts" / "screenshots" / timestamp
    import_file = Path(args.import_file).expanduser() if args.import_file else None

    if import_file and not import_file.exists():
        parser.error(f"Import file does not exist: {import_file}")

    return SnapshotOptions(
        base_url=args.base_url,
        output_dir=output_dir,
        period=args.period,
        import_file=import_file,
        semester=args.semester or None,
        created_by=args.created_by,
        headless=bool(args.headless),
        viewport_width=args.viewport_width,
        viewport_height=args.viewport_height,
        timeout_ms=args.timeout_ms,
        wait_after_action_ms=args.wait_after_action_ms,
    )


def _safe_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _wait_for_result_message(page: Any, timeout_ms: int) -> str:
    deadline = time.monotonic() + (timeout_ms / 1000)
    last_text = ""
    success_markers = (
        "تم استيراد SS01",
        "تم استيراد SS01 وتشغيل المعالجة تلقائيًا",
    )
    error_markers = (
        "فشل استيراد SS01",
        "فشلت المعالجة التلقائية",
    )

    while time.monotonic() < deadline:
        last_text = page.locator("#result").inner_text().strip()
        if any(marker in last_text for marker in success_markers):
            return last_text
        if any(marker in last_text for marker in error_markers):
            return last_text
        page.wait_for_timeout(400)
    return last_text


def _capture_panel(page: Any, key: str, suffix: str, output_dir: Path) -> dict[str, Any]:
    tab = page.locator(f'.screen-tab[data-screen="{key}"]')
    tab.click()
    panel = page.locator(f'[data-screen-panel="{key}"]')
    panel.wait_for(state="visible")
    page.wait_for_timeout(350)

    panel_path = output_dir / f"{suffix}_{key}_panel.png"
    panel.screenshot(path=str(panel_path))

    row_count = panel.locator("tbody tr").count()
    table_locator = panel.locator(".heatmap-table, .distribution-table")
    table_count = table_locator.count()

    table_path = None
    if table_count:
        table_path = output_dir / f"{suffix}_{key}_table.png"
        table_locator.first.screenshot(path=str(table_path))

    hover_path = None
    if row_count:
        first_row = panel.locator("tbody tr").first
        first_row.hover()
        page.wait_for_timeout(200)
        hover_path = output_dir / f"{suffix}_{key}_hover_row.png"
        panel.screenshot(path=str(hover_path))

    return {
        "screen": key,
        "rows": row_count,
        "panel_path": str(panel_path),
        "table_path": str(table_path) if table_path else None,
        "hover_path": str(hover_path) if hover_path else None,
    }


def run_snapshots(opts: SnapshotOptions) -> int:
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
    run_meta: dict[str, Any] = {
        "base_url": opts.base_url,
        "period": opts.period,
        "import_file": str(opts.import_file) if opts.import_file else None,
        "semester": opts.semester,
        "created_by": opts.created_by,
        "headless": opts.headless,
        "viewport": {"width": opts.viewport_width, "height": opts.viewport_height},
        "captured_at": datetime.now().isoformat(timespec="seconds"),
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=opts.headless)
            context = browser.new_context(
                viewport={"width": opts.viewport_width, "height": opts.viewport_height},
                locale="ar-SA",
                timezone_id="Asia/Riyadh",
            )
            page = context.new_page()
            page.set_default_timeout(opts.timeout_ms)

            page.goto(opts.base_url, wait_until="domcontentloaded")
            page.wait_for_selector("#globalPeriod", state="visible")
            page.wait_for_selector("#runList", state="visible")
            page.wait_for_timeout(opts.wait_after_action_ms)

            page.select_option("#globalPeriod", opts.period)
            page.wait_for_timeout(opts.wait_after_action_ms)
            page.select_option("#heatmapPeriodFilter", opts.period)
            page.wait_for_timeout(600)

            page.fill("#createdBy", opts.created_by)

            if opts.import_file:
                page.fill("#importSemester", opts.semester or "")
                page.select_option("#importPeriod", opts.period)
                page.set_input_files("#importFile", str(opts.import_file))
                page.click("#importSs01")
                result_text = _wait_for_result_message(page, opts.timeout_ms)
                _safe_write_text(opts.output_dir / "import_result.txt", result_text)
                page.wait_for_timeout(opts.wait_after_action_ms)
                run_meta["import_result"] = result_text

            if page.locator(".run-item").count() > 0:
                page.locator(".run-item").first.click()
                page.wait_for_timeout(opts.wait_after_action_ms)

            page.wait_for_selector(".screens-card", state="visible")

            full_page = opts.output_dir / "00_full_page.png"
            page.screenshot(path=str(full_page), full_page=True)

            screens_card = opts.output_dir / "01_screens_card.png"
            page.locator(".screens-card").screenshot(path=str(screens_card))

            panel_results = []
            for key, _label in SCREEN_TABS:
                panel_results.append(_capture_panel(page, key, "02", opts.output_dir))
            run_meta["panels"] = panel_results

            selected_run = page.locator("#selectedRunText").inner_text().strip()
            result_text = page.locator("#result").inner_text().strip()
            run_meta["selected_run_text"] = selected_run
            run_meta["result_text"] = result_text
            run_meta["run_cards_count"] = page.locator(".run-item").count()

            _safe_write_text(
                opts.output_dir / "meta.json",
                json.dumps(run_meta, ensure_ascii=False, indent=2),
            )

            browser.close()

    except PlaywrightTimeoutError as exc:
        _safe_write_text(opts.output_dir / "error.txt", f"Timeout: {exc}")
        print(f"Snapshot run failed with timeout: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:  # pragma: no cover - operational fallback
        _safe_write_text(opts.output_dir / "error.txt", f"Unhandled error: {exc}")
        print(f"Snapshot run failed: {exc}", file=sys.stderr)
        return 4

    print(f"Snapshots saved to: {opts.output_dir}")
    return 0


def main() -> int:
    options = parse_args()
    return run_snapshots(options)


if __name__ == "__main__":
    raise SystemExit(main())
