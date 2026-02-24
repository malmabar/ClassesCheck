from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error as url_error
from urllib import request as url_request

from app.core.config import PROJECT_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mandatory release readiness gate (health + acceptance_gate).",
    )
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="API base URL (default: http://127.0.0.1:8000).",
    )
    parser.add_argument(
        "--python-exec",
        default=str(PROJECT_ROOT / ".venv" / "bin" / "python"),
        help="Python executable used to run acceptance_gate.",
    )
    parser.add_argument(
        "--workbook-file",
        default=str(PROJECT_ROOT / "MorningClassesCheck - Beta6.xlsm"),
        help="Workbook used by acceptance_gate when source-csv is not provided.",
    )
    parser.add_argument(
        "--source-csv",
        default="",
        help="Optional SS01 CSV path passed to acceptance_gate.",
    )
    parser.add_argument(
        "--semester",
        default="",
        help="Optional semester override passed to acceptance_gate.",
    )
    parser.add_argument(
        "--period",
        choices=("all", "صباحي", "مسائي"),
        default="all",
        help="Period for acceptance_gate (default: all).",
    )
    parser.add_argument(
        "--created-by",
        default="release-readiness-gate",
        help="Operator value passed to acceptance_gate.",
    )
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=120,
        help="HTTP timeout in seconds passed to acceptance_gate.",
    )
    parser.add_argument(
        "--skip-health-check",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Skip GET /health check before running gate.",
    )
    parser.add_argument(
        "--output-file",
        default=str(PROJECT_ROOT / "artifacts" / "acceptance" / "latest.json"),
        help="Acceptance report output file.",
    )
    parser.add_argument(
        "--proof-file",
        default=str(PROJECT_ROOT / "artifacts" / "acceptance" / "release_ready.json"),
        help="Release readiness proof file.",
    )
    return parser.parse_args()


def _http_health_ok(base_url: str, timeout_sec: int) -> Dict[str, Any]:
    url = f"{base_url.rstrip('/')}/health"
    req = url_request.Request(url=url, method="GET")
    try:
        with url_request.urlopen(req, timeout=max(5, timeout_sec)) as response:
            payload = json.loads(response.read().decode("utf-8", errors="replace"))
            status_value = str(payload.get("status") or "").strip().lower()
            if status_value != "ok":
                raise RuntimeError(f"Health check returned unexpected status: {payload}")
            return payload
    except url_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Health check failed with HTTP {exc.code}: {detail}") from exc
    except url_error.URLError as exc:
        raise RuntimeError(f"Health check failed: {exc}") from exc


def _resolve_python_exec(path_value: str) -> str:
    candidate = Path(path_value).expanduser()
    if candidate.exists():
        if candidate.is_absolute():
            return str(candidate)
        return str(candidate.resolve())
    return sys.executable


def _run_acceptance_gate(args: argparse.Namespace) -> Dict[str, Any]:
    backend_dir = PROJECT_ROOT / "backend"
    output_file = Path(args.output_file).expanduser().resolve()
    output_file.parent.mkdir(parents=True, exist_ok=True)

    command = [
        _resolve_python_exec(args.python_exec),
        "-m",
        "app.tools.acceptance_gate",
        "--base-url",
        args.base_url,
        "--workbook-file",
        str(Path(args.workbook_file).expanduser().resolve()),
        "--period",
        args.period,
        "--created-by",
        args.created_by,
        "--timeout-sec",
        str(max(10, int(args.timeout_sec))),
        "--output-file",
        str(output_file),
    ]
    if args.source_csv:
        command.extend(["--source-csv", str(Path(args.source_csv).expanduser().resolve())])
    if str(args.semester or "").strip():
        command.extend(["--semester", str(args.semester).strip()])

    completed = subprocess.run(
        command,
        cwd=str(backend_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "acceptance_gate failed.\n"
            f"command={' '.join(command)}\n"
            f"stdout={completed.stdout[-3000:]}\n"
            f"stderr={completed.stderr[-3000:]}"
        )

    if not output_file.exists():
        raise RuntimeError(f"acceptance_gate did not produce output file: {output_file}")
    report = json.loads(output_file.read_text(encoding="utf-8"))
    if str(report.get("overall_status")) != "PASSED":
        raise RuntimeError(f"acceptance_gate overall_status is not PASSED: {report.get('overall_status')}")
    return report


def _write_release_proof(
    proof_file: Path,
    acceptance_report: Dict[str, Any],
    health_payload: Optional[Dict[str, Any]],
) -> Path:
    proof_file.parent.mkdir(parents=True, exist_ok=True)
    period_statuses = [
        {"period": item.get("period"), "status": item.get("status"), "run_id": item.get("run_id")}
        for item in (acceptance_report.get("period_reports") or [])
    ]
    proof_payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "release_ready": True,
        "gate": "acceptance_gate",
        "acceptance_report_file": acceptance_report.get("output_file"),
        "acceptance_overall_status": acceptance_report.get("overall_status"),
        "period_statuses": period_statuses,
        "health_payload": health_payload,
    }
    proof_file.write_text(json.dumps(proof_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return proof_file


def main() -> int:
    args = parse_args()
    output_file = Path(args.output_file).expanduser().resolve()
    proof_file = Path(args.proof_file).expanduser().resolve()

    health_payload: Optional[Dict[str, Any]] = None
    if not bool(args.skip_health_check):
        health_payload = _http_health_ok(args.base_url, int(args.timeout_sec))

    acceptance_report = _run_acceptance_gate(args)
    proof_path = _write_release_proof(
        proof_file=proof_file,
        acceptance_report=acceptance_report,
        health_payload=health_payload,
    )

    print(
        json.dumps(
            {
                "status": "PASSED",
                "acceptance_report_file": str(output_file),
                "proof_file": str(proof_path),
                "periods": [
                    {"period": item.get("period"), "status": item.get("status")}
                    for item in (acceptance_report.get("period_reports") or [])
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
