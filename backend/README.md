# Morning Classes Check Backend

FastAPI + SQLAlchemy + Alembic scaffold for Morning Classes Check modernization.

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -e /Users/malmabar/Documents/MornningClassesCheck/backend
```
3. Ensure `/Users/malmabar/Documents/MornningClassesCheck/.env.mc` exists and contains the project DB settings.
4. Run migrations:
```bash
alembic -c /Users/malmabar/Documents/MornningClassesCheck/backend/alembic.ini upgrade head
```
5. Start API:
```bash
uvicorn app.main:app --reload --app-dir /Users/malmabar/Documents/MornningClassesCheck/backend
```

Note:
- Publish/export endpoints include a schema guard that auto-creates publish tables if missing.
- Recommended still to run migrations (`alembic upgrade head`) before normal operation.

## Initial Endpoints

- `GET /health`
- `POST /api/v1/mc/import/ss01`
- `POST /api/v1/mc/run`
- `POST /api/v1/mc/checks/run`
- `GET /api/v1/mc/runs?period=صباحي|مسائي`
- `GET /api/v1/mc/runs/{run_id}/source-ss01`
- `GET /api/v1/mc/runs/{run_id}/codes`
- `GET /api/v1/mc/runs/{run_id}/issues`

## Web UI

- `GET /` : Arabic RTL dashboard for runs/codes/issues with global period filter.
- Static UI assets are served from `GET /ui/...`:
  - `/ui/styles/tokens.css`
  - `/ui/styles/components.css`
  - `/ui/scripts/dashboard.js`

## UI Visual Snapshots (Automation)

Generate repeatable screenshots for visual regression checks.

1. Install dev dependencies and browser (once):
```bash
source /Users/malmabar/Documents/MornningClassesCheck/.venv/bin/activate
pip install -e /Users/malmabar/Documents/MornningClassesCheck/backend[dev]
python -m playwright install chromium
```

2. Start API:
```bash
uvicorn app.main:app --reload --app-dir /Users/malmabar/Documents/MornningClassesCheck/backend
```

3. Capture snapshots (without import):
```bash
python -m app.tools.ui_snapshots --period صباحي
```

4. Capture snapshots after importing a specific SS01 file:
```bash
python -m app.tools.ui_snapshots \
  --period صباحي \
  --semester 144620 \
  --import-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv
```

Outputs are saved under:
- `/Users/malmabar/Documents/MornningClassesCheck/artifacts/screenshots/<timestamp>/`

## Publish Parity Report (SS01 vs Published Run)

Generate expected publish totals from a raw `SS01.csv` and optionally compare them with a specific `run_id`.

1. Expected totals from CSV only:
```bash
python -m app.tools.publish_parity_report \
  --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv \
  --period all
```

2. Compare with a published run:
```bash
python -m app.tools.publish_parity_report \
  --csv-file /Users/malmabar/Desktop/TraineeConflicts/SS01.csv \
  --run-id <RUN_ID> \
  --base-url http://127.0.0.1:8000
```

Outputs are saved under:
- `/Users/malmabar/Documents/MornningClassesCheck/artifacts/parity/`

## Mandatory Release Readiness Gate

Before any release/tag/deployment, run the mandatory gate below.  
Release is blocked if this command exits non-zero.

```bash
cd /Users/malmabar/Documents/MornningClassesCheck/backend
../.venv/bin/python -m app.tools.release_readiness_gate \
  --period all \
  --output-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json \
  --proof-file /Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json
```

After editable install (`pip install -e ...`), you can also run:

```bash
mc-release-gate --period all
```

Artifacts:
- Acceptance report: `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/latest.json`
- Release proof: `/Users/malmabar/Documents/MornningClassesCheck/artifacts/acceptance/release_ready.json`

### Unified Release Script (Gate + Optional Tag)

Use this script as the single release entrypoint:

```bash
cd /Users/malmabar/Documents/MornningClassesCheck
scripts/release_with_gate.sh --period all
```

Optional tag creation after gate success:

```bash
cd /Users/malmabar/Documents/MornningClassesCheck
scripts/release_with_gate.sh --period all --tag v1.29.0
```

Behavior:
- Blocks release on any gate failure.
- Validates `release_ready.json` content.
- Refuses tagging if git working tree is not clean.

## CI Enforcement (GitHub Actions)

The workflow below enforces the same gate automatically in CI:

- `/Users/malmabar/Documents/MornningClassesCheck/.github/workflows/release-gate.yml`

It runs on:
- Pull Requests
- Push to `main`
- Tags `v*`

CI flow:
1. Start PostgreSQL service.
2. Run Alembic migrations.
3. Start API (`uvicorn`).
4. Execute:
   - `./scripts/release_with_gate.sh --period all --python-exec "$(which python)"`
5. Upload acceptance artifacts and server log.
