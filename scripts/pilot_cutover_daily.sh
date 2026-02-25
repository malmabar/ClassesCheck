#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
PYTHON_EXEC_DEFAULT="${ROOT_DIR}/.venv/bin/python"

CSV_FILE=""
BASE_URL="http://127.0.0.1:8000"
PERIOD="all"
ACCEPTED_STATUSES="PUBLISHED"
MIN_DISTINCT_DAYS="14"
OUTPUT_FILE="${ROOT_DIR}/artifacts/pilot/latest.json"
PYTHON_EXEC="${PYTHON_EXEC_DEFAULT}"
REQUIRE_CHECKSUM_MATCH="true"
DAILY_LATEST_ONLY="true"
ALLOW_NOT_READY="false"
APPEND_HISTORY_LOG="true"
HISTORY_LOG_FILE="${ROOT_DIR}/artifacts/pilot/history.log"

usage() {
  cat <<'USAGE'
Usage:
  scripts/pilot_cutover_daily.sh [options]

Options:
  --csv-file <path>                    Required SS01 CSV file path
  --base-url <url>                     API base URL (default: http://127.0.0.1:8000)
  --period {all|صباحي|مسائي}          Period scope (default: all)
  --accepted-statuses <csv>            Run statuses in scope (default: PUBLISHED)
  --min-distinct-days <int>            Pilot day threshold (default: 14)
  --output-file <path>                 Report output path
  --python-exec <path>                 Python executable (default: .venv/bin/python)
  --no-require-input-checksum-match    Disable checksum scoping
  --no-daily-latest-only               Include all runs in each day (not only latest)
  --allow-not-ready                    Always exit 0 even when cutover is not ready
  --no-append-history-log              Do not append daily summary line
  --history-log-file <path>            History log path (default: artifacts/pilot/history.log)
  -h, --help                           Show help

Examples:
  scripts/pilot_cutover_daily.sh --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv
  scripts/pilot_cutover_daily.sh --csv-file /path/SS01.csv --min-distinct-days 7 --allow-not-ready
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --csv-file)
      CSV_FILE="$2"
      shift 2
      ;;
    --base-url)
      BASE_URL="$2"
      shift 2
      ;;
    --period)
      PERIOD="$2"
      shift 2
      ;;
    --accepted-statuses)
      ACCEPTED_STATUSES="$2"
      shift 2
      ;;
    --min-distinct-days)
      MIN_DISTINCT_DAYS="$2"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --python-exec)
      PYTHON_EXEC="$2"
      shift 2
      ;;
    --no-require-input-checksum-match)
      REQUIRE_CHECKSUM_MATCH="false"
      shift
      ;;
    --no-daily-latest-only)
      DAILY_LATEST_ONLY="false"
      shift
      ;;
    --allow-not-ready)
      ALLOW_NOT_READY="true"
      shift
      ;;
    --no-append-history-log)
      APPEND_HISTORY_LOG="false"
      shift
      ;;
    --history-log-file)
      HISTORY_LOG_FILE="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${CSV_FILE}" ]]; then
  echo "--csv-file is required." >&2
  usage
  exit 1
fi
if [[ "${PERIOD}" != "all" && "${PERIOD}" != "صباحي" && "${PERIOD}" != "مسائي" ]]; then
  echo "Invalid --period value: ${PERIOD}" >&2
  exit 1
fi
if [[ ! -f "${CSV_FILE}" ]]; then
  echo "CSV file not found: ${CSV_FILE}" >&2
  exit 1
fi
if [[ ! -f "${PYTHON_EXEC}" ]]; then
  echo "Python executable not found: ${PYTHON_EXEC}" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUTPUT_FILE}")"
mkdir -p "$(dirname "${HISTORY_LOG_FILE}")"

CMD=(
  "${PYTHON_EXEC}"
  -m app.tools.pilot_cutover_report
  --csv-file "${CSV_FILE}"
  --base-url "${BASE_URL}"
  --period "${PERIOD}"
  --accepted-statuses "${ACCEPTED_STATUSES}"
  --min-distinct-days "${MIN_DISTINCT_DAYS}"
  --output-file "${OUTPUT_FILE}"
)

if [[ "${REQUIRE_CHECKSUM_MATCH}" == "true" ]]; then
  CMD+=(--require-input-checksum-match)
else
  CMD+=(--no-require-input-checksum-match)
fi
if [[ "${DAILY_LATEST_ONLY}" == "true" ]]; then
  CMD+=(--daily-latest-only)
else
  CMD+=(--no-daily-latest-only)
fi

set +e
(
  cd "${BACKEND_DIR}"
  "${CMD[@]}"
)
REPORT_EXIT_CODE=$?
set -e

SUMMARY_JSON="$("${PYTHON_EXEC}" - "${OUTPUT_FILE}" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1]).expanduser().resolve()
if not path.exists():
    raise SystemExit(f"Pilot report file missing: {path}")

payload = json.loads(path.read_text(encoding="utf-8"))
rows = []
for period in payload.get("period_reports") or []:
    rows.append(
        {
            "period": period.get("period"),
            "status": period.get("status"),
            "runs": period.get("total_runs"),
            "days": period.get("distinct_days_count"),
            "mismatches": len(period.get("mismatch_run_ids") or []),
        }
    )

print(
    json.dumps(
        {
            "generated_at_utc": payload.get("generated_at_utc"),
            "cutover_ready": payload.get("cutover_ready"),
            "overall_status": payload.get("overall_status"),
            "periods": rows,
        },
        ensure_ascii=False,
    )
)
PY
)"

echo "pilot_daily_summary=${SUMMARY_JSON}"

if [[ "${APPEND_HISTORY_LOG}" == "true" ]]; then
  "${PYTHON_EXEC}" - "${OUTPUT_FILE}" "${HISTORY_LOG_FILE}" <<'PY'
import json
import pathlib
import sys

report = pathlib.Path(sys.argv[1]).expanduser().resolve()
history = pathlib.Path(sys.argv[2]).expanduser().resolve()
payload = json.loads(report.read_text(encoding="utf-8"))

rows = []
for item in payload.get("period_reports") or []:
    rows.append(
        f"{item.get('period')}:status={item.get('status')},days={item.get('distinct_days_count')},mismatches={len(item.get('mismatch_run_ids') or [])}"
    )

line = (
    f"{payload.get('generated_at_utc')} | cutover_ready={payload.get('cutover_ready')} "
    f"| overall={payload.get('overall_status')} | " + " ; ".join(rows)
)
history.parent.mkdir(parents=True, exist_ok=True)
with history.open("a", encoding="utf-8") as fh:
    fh.write(line + "\n")
PY
  echo "pilot_history_appended=${HISTORY_LOG_FILE}"
fi

if [[ "${REPORT_EXIT_CODE}" -ne 0 && "${ALLOW_NOT_READY}" == "true" ]]; then
  echo "pilot_report_not_ready_but_allowed=true"
  exit 0
fi

exit "${REPORT_EXIT_CODE}"
