from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple
from urllib import error as url_error
from urllib import parse as url_parse
from urllib import request as url_request

from app.core.config import PROJECT_ROOT
from app.tools.publish_parity_report import (
    VALID_PERIODS,
    _build_comparison,
    _build_expected_from_csv,
    _fetch_published_totals,
)


def _fetch_json(url: str, timeout_sec: int) -> dict:
    req = url_request.Request(url=url, method="GET")
    try:
        with url_request.urlopen(req, timeout=timeout_sec) as response:
            payload = response.read().decode("utf-8")
    except url_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {detail}") from exc
    except url_error.URLError as exc:
        raise RuntimeError(f"Failed to call {url}: {exc}") from exc
    try:
        return json.loads(payload) if payload else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from {url}") from exc


def _parse_created_at(value: Any) -> Optional[datetime]:
    text = str(value or "").strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _split_statuses(value: str) -> Tuple[str, ...]:
    parts = [item.strip().upper() for item in str(value or "").split(",")]
    normalized = tuple(item for item in parts if item)
    return normalized or ("PUBLISHED",)


def _csv_sha256(csv_file: Path) -> str:
    return hashlib.sha256(csv_file.read_bytes()).hexdigest()


def _fetch_runs_for_period(
    *,
    base_url: str,
    period: str,
    timeout_sec: int,
    page_size: int,
    max_pages: int,
) -> List[dict]:
    base = base_url.rstrip("/")
    all_items: List[dict] = []
    for page in range(1, max_pages + 1):
        query = url_parse.urlencode({"period": period, "page": page, "size": page_size})
        payload = _fetch_json(f"{base}/api/v1/mc/runs?{query}", timeout_sec=timeout_sec)
        page_items = payload.get("items") or []
        if not isinstance(page_items, list):
            raise RuntimeError(f"Invalid runs payload for period={period}, page={page}")
        all_items.extend(page_items)
        if not payload.get("has_next"):
            break
    return all_items


def _filter_runs_by_status(runs: Sequence[dict], statuses: Sequence[str]) -> List[dict]:
    allowed = {item.upper() for item in statuses}
    return [item for item in runs if str(item.get("status") or "").upper() in allowed]


def _filter_runs_by_checksum(
    runs: Sequence[dict],
    *,
    expected_checksum: Optional[str],
    require_match: bool,
) -> List[dict]:
    if not require_match or not expected_checksum:
        return list(runs)
    expected = str(expected_checksum).strip().lower()
    return [
        item
        for item in runs
        if str(item.get("input_checksum") or "").strip().lower() == expected
    ]


def _build_run_report(
    *,
    base_url: str,
    run_item: dict,
    expected_period_counts: dict,
    timeout_sec: int,
) -> dict:
    run_id = str(run_item.get("id") or "")
    created_at_raw = run_item.get("created_at")
    created_at = _parse_created_at(created_at_raw)
    base_report = {
        "run_id": run_id,
        "status": run_item.get("status"),
        "semester": run_item.get("semester"),
        "period": run_item.get("period"),
        "created_at": created_at_raw,
        "created_at_utc": created_at.isoformat() if created_at else None,
        "all_match": False,
        "comparison": None,
        "error": None,
    }
    if not run_id:
        base_report["error"] = "run_id_missing"
        return base_report

    try:
        actual = _fetch_published_totals(base_url=base_url, run_id=run_id, timeout_sec=timeout_sec)
        comparison = _build_comparison(expected_period_counts, actual)
        base_report["all_match"] = bool(comparison.get("all_match"))
        base_report["comparison"] = comparison
    except RuntimeError as exc:
        base_report["error"] = str(exc)
    return base_report


def _evaluate_period(period: str, run_reports: Sequence[dict], min_distinct_days: int) -> dict:
    distinct_days = sorted(
        {
            dt.date().isoformat()
            for dt in (
                _parse_created_at(item.get("created_at_utc") or item.get("created_at"))
                for item in run_reports
            )
            if dt is not None
        }
    )
    mismatch_runs = [item for item in run_reports if not bool(item.get("all_match"))]
    failures: List[str] = []
    if not run_reports:
        failures.append("no_runs_in_scope")
    if len(distinct_days) < min_distinct_days:
        failures.append(
            f"insufficient_distinct_days={len(distinct_days)}/{min_distinct_days}"
        )
    if mismatch_runs:
        failures.append(f"parity_mismatch_runs={len(mismatch_runs)}")

    return {
        "period": period,
        "status": "PASSED" if not failures else "FAILED",
        "total_runs": len(run_reports),
        "distinct_days_count": len(distinct_days),
        "distinct_days": distinct_days,
        "mismatch_run_ids": [str(item.get("run_id") or "") for item in mismatch_runs],
        "failures": failures,
    }


def _resolve_periods(period_value: str) -> Tuple[str, ...]:
    if period_value == "all":
        return VALID_PERIODS
    return (period_value,)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Pilot/Cutover evidence report (2-4 weeks) using SS01 parity against published runs.",
    )
    parser.add_argument(
        "--csv-file",
        required=True,
        help="Absolute path to SS01 CSV used as baseline.",
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="API base URL (default: http://127.0.0.1:8000).",
    )
    parser.add_argument(
        "--period",
        default="all",
        choices=["all", *VALID_PERIODS],
        help="Period scope for pilot report (default: all).",
    )
    parser.add_argument(
        "--accepted-statuses",
        default="PUBLISHED",
        help="Comma-separated run statuses included in pilot scope (default: PUBLISHED).",
    )
    parser.add_argument(
        "--require-input-checksum-match",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Limit runs to those whose input_checksum matches the provided csv-file checksum "
            "(default: true)."
        ),
    )
    parser.add_argument(
        "--min-distinct-days",
        type=int,
        default=14,
        help="Minimum distinct operation days per period for cutover readiness (default: 14).",
    )
    parser.add_argument(
        "--max-runs-per-period",
        type=int,
        default=120,
        help="Max recent runs evaluated per period after status filtering (default: 120).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Runs page size for API pagination (default: 100).",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=20,
        help="Safety cap for paginated /runs fetch (default: 20).",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=20,
        help="HTTP timeout in seconds (default: 20).",
    )
    parser.add_argument(
        "--output-file",
        default=str(PROJECT_ROOT / "artifacts" / "pilot" / "latest.json"),
        help="Output report file (default: artifacts/pilot/latest.json).",
    )
    parser.add_argument(
        "--save-timestamped",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Also writes artifacts/pilot/pilot_cutover_<timestamp>.json (default: true).",
    )
    args = parser.parse_args()

    csv_file = Path(args.csv_file).expanduser().resolve()
    if not csv_file.exists():
        parser.error(f"CSV file not found: {csv_file}")
    if int(args.min_distinct_days) < 1:
        parser.error("--min-distinct-days must be >= 1")
    if int(args.max_runs_per_period) < 1:
        parser.error("--max-runs-per-period must be >= 1")
    if int(args.page_size) < 1:
        parser.error("--page-size must be >= 1")
    if int(args.max_pages) < 1:
        parser.error("--max-pages must be >= 1")

    args.csv_file = str(csv_file)
    args.accepted_statuses = _split_statuses(args.accepted_statuses)
    args.output_file = str(Path(args.output_file).expanduser().resolve())
    return args


def main() -> int:
    args = parse_args()
    csv_file = Path(args.csv_file)
    output_file = Path(args.output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    expected = _build_expected_from_csv(csv_file)
    expected_checksum = _csv_sha256(csv_file)
    expected_periods = expected.get("periods") or {}
    periods = _resolve_periods(args.period)

    period_reports: List[dict] = []
    failures: List[str] = []

    for period in periods:
        expected_period_counts = expected_periods.get(period) or {}
        all_runs = _fetch_runs_for_period(
            base_url=args.base_url,
            period=period,
            timeout_sec=int(args.timeout_sec),
            page_size=int(args.page_size),
            max_pages=int(args.max_pages),
        )
        in_scope = _filter_runs_by_status(all_runs, args.accepted_statuses)
        checksum_scoped = _filter_runs_by_checksum(
            in_scope,
            expected_checksum=expected_checksum,
            require_match=bool(args.require_input_checksum_match),
        )
        selected_runs = checksum_scoped[: int(args.max_runs_per_period)]

        run_reports = [
            _build_run_report(
                base_url=args.base_url,
                run_item=item,
                expected_period_counts=expected_period_counts,
                timeout_sec=int(args.timeout_sec),
            )
            for item in selected_runs
        ]
        period_summary = _evaluate_period(
            period=period,
            run_reports=run_reports,
            min_distinct_days=int(args.min_distinct_days),
        )
        period_summary["source_totals"] = expected_period_counts
        period_summary["in_scope_statuses"] = list(args.accepted_statuses)
        period_summary["total_runs_fetched"] = len(all_runs)
        period_summary["total_runs_in_scope"] = len(in_scope)
        period_summary["total_runs_checksum_scoped"] = len(checksum_scoped)
        period_summary["checksum_filter_enabled"] = bool(args.require_input_checksum_match)
        period_summary["expected_input_checksum"] = expected_checksum
        period_summary["runs"] = run_reports
        period_reports.append(period_summary)
        if period_summary["status"] != "PASSED":
            failures.extend([f"{period}:{item}" for item in period_summary["failures"]])

    overall_status = "PASSED" if not failures else "FAILED"
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cutover_ready": overall_status == "PASSED",
        "overall_status": overall_status,
        "failures": failures,
        "config": {
            "csv_file": str(csv_file),
            "base_url": args.base_url.rstrip("/"),
            "period": args.period,
            "accepted_statuses": list(args.accepted_statuses),
            "require_input_checksum_match": bool(args.require_input_checksum_match),
            "expected_input_checksum": expected_checksum,
            "min_distinct_days": int(args.min_distinct_days),
            "max_runs_per_period": int(args.max_runs_per_period),
            "page_size": int(args.page_size),
            "max_pages": int(args.max_pages),
            "timeout_sec": int(args.timeout_sec),
        },
        "period_reports": period_reports,
    }

    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"pilot_cutover_report_saved={output_file}")
    print(
        f"cutover_ready={payload['cutover_ready']} "
        f"overall_status={payload['overall_status']} failures={len(payload['failures'])}"
    )
    for period_report in period_reports:
        print(
            f"[{period_report['period']}] status={period_report['status']} "
            f"runs={period_report['total_runs']} "
            f"days={period_report['distinct_days_count']} "
            f"mismatches={len(period_report['mismatch_run_ids'])}"
        )

    if bool(args.save_timestamped):
        timestamp_path = (
            output_file.parent
            / f"pilot_cutover_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        )
        timestamp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"pilot_cutover_report_saved_timestamped={timestamp_path}")

    return 0 if payload["cutover_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
