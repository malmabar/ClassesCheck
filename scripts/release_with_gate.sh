#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
PYTHON_EXEC_DEFAULT="${ROOT_DIR}/.venv/bin/python"

PERIOD="all"
SOURCE_CSV=""
SEMESTER=""
CREATED_BY="release-readiness-gate"
OUTPUT_FILE="${ROOT_DIR}/artifacts/acceptance/latest.json"
PROOF_FILE="${ROOT_DIR}/artifacts/acceptance/release_ready.json"
PYTHON_EXEC="${PYTHON_EXEC_DEFAULT}"
SKIP_HEALTH_CHECK="false"
TAG_NAME=""
CLEAN_ACCEPTANCE_CACHE="false"

usage() {
  cat <<'USAGE'
Usage:
  scripts/release_with_gate.sh [options]

Options:
  --period {all|صباحي|مسائي}   Period scope (default: all)
  --source-csv <path>          Optional SS01 CSV file path
  --semester <value>           Optional semester override
  --created-by <value>         Operator value (default: release-readiness-gate)
  --output-file <path>         Acceptance report path
  --proof-file <path>          Release proof path
  --python-exec <path>         Python executable (default: .venv/bin/python)
  --skip-health-check          Skip health check
  --clean-acceptance-cache     Remove generated acceptance cache files before running gate
  --tag <tag-name>             Create annotated git tag after gate success
  -h, --help                   Show this help

Examples:
  scripts/release_with_gate.sh --period all
  scripts/release_with_gate.sh --period all --clean-acceptance-cache
  scripts/release_with_gate.sh --period all --tag v1.29.0
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --period)
      PERIOD="$2"
      shift 2
      ;;
    --source-csv)
      SOURCE_CSV="$2"
      shift 2
      ;;
    --semester)
      SEMESTER="$2"
      shift 2
      ;;
    --created-by)
      CREATED_BY="$2"
      shift 2
      ;;
    --output-file)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --proof-file)
      PROOF_FILE="$2"
      shift 2
      ;;
    --python-exec)
      PYTHON_EXEC="$2"
      shift 2
      ;;
    --skip-health-check)
      SKIP_HEALTH_CHECK="true"
      shift
      ;;
    --clean-acceptance-cache)
      CLEAN_ACCEPTANCE_CACHE="true"
      shift
      ;;
    --tag)
      TAG_NAME="$2"
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

if [[ "${PERIOD}" != "all" && "${PERIOD}" != "صباحي" && "${PERIOD}" != "مسائي" ]]; then
  echo "Invalid --period value: ${PERIOD}" >&2
  exit 1
fi

if [[ ! -f "${PYTHON_EXEC}" ]]; then
  echo "Python executable not found: ${PYTHON_EXEC}" >&2
  exit 1
fi

if [[ -n "${SOURCE_CSV}" && ! -f "${SOURCE_CSV}" ]]; then
  echo "source-csv file not found: ${SOURCE_CSV}" >&2
  exit 1
fi

mkdir -p "$(dirname "${OUTPUT_FILE}")"
mkdir -p "$(dirname "${PROOF_FILE}")"

if [[ "${CLEAN_ACCEPTANCE_CACHE}" == "true" ]]; then
  ACCEPTANCE_DIR="${ROOT_DIR}/artifacts/acceptance"
  ACCEPTANCE_TMP_DIR="${ACCEPTANCE_DIR}/tmp"
  mkdir -p "${ACCEPTANCE_TMP_DIR}"
  removed_count=0
  shopt -s nullglob
  for path in "${ACCEPTANCE_TMP_DIR}"/ss01_from_workbook_*.csv "${ACCEPTANCE_DIR}"/acceptance_*.json; do
    if [[ -f "${path}" ]]; then
      rm -f "${path}"
      removed_count=$((removed_count + 1))
    fi
  done
  shopt -u nullglob
  echo "Acceptance cache cleanup removed ${removed_count} file(s)."
fi

OUTPUT_REL="${OUTPUT_FILE#${ROOT_DIR}/}"
PROOF_REL="${PROOF_FILE#${ROOT_DIR}/}"

GATE_CMD=(
  "${PYTHON_EXEC}"
  -m app.tools.release_readiness_gate
  --period "${PERIOD}"
  --created-by "${CREATED_BY}"
  --output-file "${OUTPUT_FILE}"
  --proof-file "${PROOF_FILE}"
)

if [[ -n "${SOURCE_CSV}" ]]; then
  GATE_CMD+=(--source-csv "${SOURCE_CSV}")
fi
if [[ -n "${SEMESTER}" ]]; then
  GATE_CMD+=(--semester "${SEMESTER}")
fi
if [[ "${SKIP_HEALTH_CHECK}" == "true" ]]; then
  GATE_CMD+=(--skip-health-check)
fi

echo "Running mandatory release gate..."
(
  cd "${BACKEND_DIR}"
  "${GATE_CMD[@]}"
)

"${PYTHON_EXEC}" - "${PROOF_FILE}" <<'PY'
import json
import pathlib
import sys

proof_path = pathlib.Path(sys.argv[1]).expanduser().resolve()
if not proof_path.exists():
    raise SystemExit(f"Release proof file missing: {proof_path}")

payload = json.loads(proof_path.read_text(encoding="utf-8"))
if not payload.get("release_ready"):
    raise SystemExit(f"release_ready is not true in {proof_path}")
if payload.get("acceptance_overall_status") != "PASSED":
    raise SystemExit(
        f"acceptance_overall_status is not PASSED in {proof_path}: "
        f"{payload.get('acceptance_overall_status')}"
    )
print(f"Release proof validated: {proof_path}")
PY

if [[ -n "${TAG_NAME}" ]]; then
  if ! git -C "${ROOT_DIR}" diff --quiet -- . ":(exclude)${OUTPUT_REL}" ":(exclude)${PROOF_REL}"; then
    echo "Working tree has unstaged changes (excluding gate output files). Refusing to tag." >&2
    exit 1
  fi
  if ! git -C "${ROOT_DIR}" diff --cached --quiet -- . ":(exclude)${OUTPUT_REL}" ":(exclude)${PROOF_REL}"; then
    echo "Working tree has staged but uncommitted changes (excluding gate output files). Refusing to tag." >&2
    exit 1
  fi
  if git -C "${ROOT_DIR}" rev-parse -q --verify "refs/tags/${TAG_NAME}" >/dev/null; then
    echo "Tag already exists: ${TAG_NAME}" >&2
    exit 1
  fi
  git -C "${ROOT_DIR}" tag -a "${TAG_NAME}" -m "Release ${TAG_NAME} (gate passed)"
  echo "Tag created: ${TAG_NAME}"
fi

echo "Release gate PASSED. You can proceed with release."
