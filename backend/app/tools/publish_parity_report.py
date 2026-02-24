from __future__ import annotations

import argparse
import csv
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from app.core.config import PROJECT_ROOT
from app.services.time_slots import resolve_period_and_slots


VALID_PERIODS = ("صباحي", "مسائي")

DAY_ORDER_MAP: Dict[str, int] = {
    "الاحد": 1,
    "الأحد": 1,
    "الاحد ": 1,
    "الاثنين": 2,
    "الإثنين": 2,
    "الثلاثاء": 3,
    "الاربعاء": 4,
    "الأربعاء": 4,
    "الخميس": 5,
}


def _decode_csv(file_bytes: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1256"):
        try:
            return file_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode CSV. Supported encodings: UTF-8, Windows-1256.")


def _detect_delimiter(text: str) -> str:
    sample = "\n".join(text.splitlines()[:20])
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;").delimiter
    except csv.Error:
        return ","


def _build_expected_from_csv(csv_file: Path) -> dict:
    raw = csv_file.read_bytes()
    decoded_text, encoding = _decode_csv(raw)
    delimiter = _detect_delimiter(decoded_text)
    reader = csv.DictReader(decoded_text.splitlines(), delimiter=delimiter)

    expected = {
        "صباحي": {
            "source_rows": 0,
            "unknown_day_rows": 0,
            "no_slot_rows": 0,
            "halls_keys": set(),
            "crns_keys": set(),
            "trainers_keys": set(),
            "rooms": set(),
            "distribution_rows": 40,
        },
        "مسائي": {
            "source_rows": 0,
            "unknown_day_rows": 0,
            "no_slot_rows": 0,
            "halls_keys": set(),
            "crns_keys": set(),
            "trainers_keys": set(),
            "rooms": set(),
            "distribution_rows": 40,
        },
    }
    unknown_period_rows = 0

    for row in reader:
        day_name = str(row.get("اليوم") or "").strip()
        day_order = DAY_ORDER_MAP.get(day_name)
        section_type = str(row.get("نوع الشعبة") or "").strip()
        time_value = str(row.get("الوقت") or "").strip()

        slot_resolution = resolve_period_and_slots(
            time_value=time_value,
            time_hhmm=None,
            section_type=section_type,
            period_hint=None,
        )
        period = slot_resolution.period
        if period not in VALID_PERIODS:
            unknown_period_rows += 1
            continue

        item = expected[period]
        item["source_rows"] += 1
        if day_order is None:
            item["unknown_day_rows"] += 1
            continue

        slots = [slot for slot in slot_resolution.slot_indices if 1 <= slot <= 8]
        if not slots:
            item["no_slot_rows"] += 1
            continue

        room_code = str(row.get("قاعة") or "").strip()
        crn = str(row.get("الرقم المرجعي") or "").strip()
        trainer_job_id = str(row.get("رقم المدرب") or "").strip()

        if room_code:
            item["rooms"].add(room_code)
        for slot_index in sorted(set(slots)):
            if room_code:
                item["halls_keys"].add((room_code, day_order, slot_index))
            if crn:
                item["crns_keys"].add((crn, day_order, slot_index))
            if trainer_job_id:
                item["trainers_keys"].add((trainer_job_id, day_order, slot_index))

    return {
        "encoding": encoding,
        "delimiter": delimiter,
        "unknown_period_rows": unknown_period_rows,
        "periods": {
            period: {
                "source_rows": data["source_rows"],
                "unknown_day_rows": data["unknown_day_rows"],
                "no_slot_rows": data["no_slot_rows"],
                "total_rooms": len(data["rooms"]),
                "halls_rows": len(data["halls_keys"]),
                "crns_rows": len(data["crns_keys"]),
                "trainers_rows": len(data["trainers_keys"]),
                "distribution_rows": data["distribution_rows"],
            }
            for period, data in expected.items()
        },
    }


def _fetch_json(url: str, timeout_sec: int) -> dict:
    request = urllib.request.Request(url=url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout_sec) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Failed to call {url}: {exc}") from exc
    try:
        return json.loads(payload) if payload else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON from {url}") from exc


def _fetch_published_totals(base_url: str, run_id: str, timeout_sec: int) -> dict:
    base = base_url.rstrip("/")
    run_payload = _fetch_json(f"{base}/api/v1/mc/runs/{run_id}", timeout_sec=timeout_sec)
    run_info = run_payload.get("run") or {}
    totals = {}
    for key in ("halls", "crns", "trainers", "distribution", "artifacts"):
        endpoint = f"{base}/api/v1/mc/runs/{run_id}/{key}?page=1&size=1"
        payload = _fetch_json(endpoint, timeout_sec=timeout_sec)
        totals[f"{key}_rows"] = int(payload.get("total") or 0)
    return {
        "run_id": run_id,
        "status": run_info.get("status"),
        "semester": run_info.get("semester"),
        "period": run_info.get("period"),
        "totals": totals,
    }


def _build_comparison(expected_for_period: dict, actual: dict) -> dict:
    mapping = {
        "halls_rows": "halls_rows",
        "crns_rows": "crns_rows",
        "trainers_rows": "trainers_rows",
        "distribution_rows": "distribution_rows",
    }
    rows = []
    for key, actual_key in mapping.items():
        expected_value = int(expected_for_period.get(key) or 0)
        actual_value = int(actual["totals"].get(actual_key) or 0)
        rows.append(
            {
                "metric": key,
                "expected": expected_value,
                "actual": actual_value,
                "delta": actual_value - expected_value,
                "match": expected_value == actual_value,
            }
        )
    all_match = all(row["match"] for row in rows)
    return {
        "all_match": all_match,
        "rows": rows,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate publish parity baseline from SS01 and optionally compare with published run.",
    )
    parser.add_argument("--csv-file", required=True, help="Absolute path to SS01 CSV file.")
    parser.add_argument(
        "--period",
        default="all",
        choices=["all", "صباحي", "مسائي"],
        help="Period to print in console. default: all",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="Optional run_id to compare against /api/v1/mc/runs/{run_id}/[halls|crns|trainers|distribution].",
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="API base URL. default: http://127.0.0.1:8000",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=20,
        help="HTTP timeout in seconds for API comparison. default: 20",
    )
    parser.add_argument(
        "--output-file",
        default=None,
        help="Optional JSON output path. default: artifacts/parity/parity_<timestamp>.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_file = Path(args.csv_file).expanduser().resolve()
    if not csv_file.exists():
        raise SystemExit(f"CSV file not found: {csv_file}")

    expected = _build_expected_from_csv(csv_file)
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "csv_file": str(csv_file),
        "expected": expected,
    }

    periods_to_print = VALID_PERIODS if args.period == "all" else (args.period,)
    print("publish_parity_expected")
    for period in periods_to_print:
        p = expected["periods"][period]
        print(
            f"[{period}] source={p['source_rows']} rooms={p['total_rooms']} "
            f"halls={p['halls_rows']} crns={p['crns_rows']} trainers={p['trainers_rows']} "
            f"distribution={p['distribution_rows']} unknown_day={p['unknown_day_rows']} no_slot={p['no_slot_rows']}"
        )

    if args.run_id:
        try:
            actual = _fetch_published_totals(
                base_url=args.base_url,
                run_id=args.run_id,
                timeout_sec=args.timeout_sec,
            )
            period = actual.get("period")
            if period not in VALID_PERIODS:
                raise RuntimeError(f"Run period is invalid or missing: {period}")
            comparison = _build_comparison(expected["periods"][period], actual)
            report["actual"] = actual
            report["comparison"] = comparison
            print(
                f"[comparison run_id={args.run_id}] period={period} status={actual.get('status')} "
                f"all_match={comparison['all_match']}"
            )
            for row in comparison["rows"]:
                print(
                    f" - {row['metric']}: expected={row['expected']} actual={row['actual']} "
                    f"delta={row['delta']} match={row['match']}"
                )
        except RuntimeError as exc:
            report["comparison_error"] = str(exc)
            print(f"[comparison_error] {exc}")

    output_file = Path(args.output_file) if args.output_file else (
        PROJECT_ROOT
        / "artifacts"
        / "parity"
        / f"publish_parity_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"report_saved={output_file.resolve()}")


if __name__ == "__main__":
    main()
