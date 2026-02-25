from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Optional

import pytest
from fastapi.testclient import TestClient

import app.api.routes.imports as imports_routes
import app.api.routes.runs as runs_routes
from app.db.session import get_db
from app.main import app


@dataclass
class _FakeRun:
    id: str = "run-1"
    status: str = "SUCCEEDED"
    semester: str = "144620"
    period: str = "صباحي"
    rule_version: str = "rule-v1"
    idempotency_key: Optional[str] = None
    input_checksum: str = "checksum"
    reference_version: str = "beta6"
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    created_by: str = "tester"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class _FakeResult:
    def __init__(self, rows: list[_FakeRun]):
        self._rows = rows

    def scalars(self) -> "_FakeResult":
        return self

    def all(self) -> list[_FakeRun]:
        return self._rows


class _FakeDB:
    def __init__(self) -> None:
        self.rows = [_FakeRun()]

    def scalar(self, *_args, **_kwargs):
        return 1

    def execute(self, *_args, **_kwargs) -> _FakeResult:
        return _FakeResult(self.rows)

    def get(self, *_args, **_kwargs) -> _FakeRun:
        return self.rows[0]

    def rollback(self) -> None:
        return None


@pytest.fixture
def client_bundle() -> Iterator[tuple[TestClient, _FakeDB]]:
    fake_db = _FakeDB()

    def _override_get_db() -> Iterator[_FakeDB]:
        yield fake_db

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client, fake_db
    app.dependency_overrides.clear()


def test_viewer_can_read_runs(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get("/api/v1/mc/runs", headers={"X-MC-Role": "viewer"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["id"] == "run-1"


def test_invalid_role_is_rejected(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get("/api/v1/mc/runs", headers={"X-MC-Role": "not-a-role"})

    assert response.status_code == 403
    payload = response.json()
    assert payload["code"] == "FORBIDDEN"
    assert payload["trace_id"]
    assert "Allowed roles" in payload["detail"]
    assert payload["message"] == payload["detail"]


@pytest.mark.parametrize(
    ("method", "url", "request_kind"),
    [
        ("POST", "/api/v1/mc/import/ss01", "multipart"),
        ("POST", "/api/v1/mc/run", "json"),
        ("POST", "/api/v1/mc/checks/run", "json"),
        ("POST", "/api/v1/mc/runs/run-1/publish", "empty"),
        ("GET", "/api/v1/mc/runs/run-1/export.xlsx", "empty"),
        ("GET", "/api/v1/mc/runs/run-1/export.pdf", "empty"),
    ],
)
def test_viewer_cannot_call_mutation_endpoints(
    client_bundle: tuple[TestClient, _FakeDB],
    method: str,
    url: str,
    request_kind: str,
) -> None:
    client, _ = client_bundle
    headers = {"X-MC-Role": "viewer"}

    if request_kind == "multipart":
        response = client.request(
            method,
            url,
            headers=headers,
            data={"semester": "144620", "period": "صباحي"},
            files={"file": ("SS01.csv", b"col1,col2\n1,2\n", "text/csv")},
        )
    elif request_kind == "json":
        response = client.request(method, url, headers=headers, json={"run_id": "run-1"})
    else:
        response = client.request(method, url, headers=headers)

    assert response.status_code == 403


def test_operator_can_import(client_bundle: tuple[TestClient, _FakeDB], monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = client_bundle

    def _fake_import_ss01_csv(**_kwargs):
        return {"run_id": "run-operator", "status": "SUCCEEDED"}

    monkeypatch.setattr(imports_routes, "import_ss01_csv", _fake_import_ss01_csv)

    response = client.post(
        "/api/v1/mc/import/ss01",
        headers={"X-MC-Role": "operator"},
        data={"semester": "144620", "period": "صباحي"},
        files={"file": ("SS01.csv", b"col1,col2\n1,2\n", "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["result"]["run_id"] == "run-operator"


def test_missing_role_header_uses_default_operator(
    client_bundle: tuple[TestClient, _FakeDB], monkeypatch: pytest.MonkeyPatch
) -> None:
    client, _ = client_bundle

    def _fake_import_ss01_csv(**_kwargs):
        return {"run_id": "run-default-role", "status": "SUCCEEDED"}

    monkeypatch.setattr(imports_routes, "import_ss01_csv", _fake_import_ss01_csv)

    response = client.post(
        "/api/v1/mc/import/ss01",
        data={"semester": "144620", "period": "صباحي"},
        files={"file": ("SS01.csv", b"col1,col2\n1,2\n", "text/csv")},
    )

    assert response.status_code == 200
    assert response.json()["result"]["run_id"] == "run-default-role"


def test_operator_can_publish(client_bundle: tuple[TestClient, _FakeDB], monkeypatch: pytest.MonkeyPatch) -> None:
    client, _ = client_bundle

    def _fake_publish_run_outputs(**_kwargs):
        return {"run_id": "run-1", "status": "PUBLISHED"}

    monkeypatch.setattr(runs_routes, "publish_run_outputs", _fake_publish_run_outputs)

    response = client.post("/api/v1/mc/runs/run-1/publish", headers={"X-MC-Role": "operator"})

    assert response.status_code == 200
    assert response.json()["result"]["status"] == "PUBLISHED"


def test_operator_can_export_xlsx(
    client_bundle: tuple[TestClient, _FakeDB],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    client, _ = client_bundle
    xlsx_path = tmp_path / "report.xlsx"
    xlsx_path.write_bytes(b"PK\x03\x04")

    def _fake_export_run_xlsx(**_kwargs):
        return {
            "absolute_path": str(xlsx_path),
            "file_name": "report.xlsx",
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }

    monkeypatch.setattr(runs_routes, "export_run_xlsx", _fake_export_run_xlsx)

    response = client.get("/api/v1/mc/runs/run-1/export.xlsx", headers={"X-MC-Role": "operator"})

    assert response.status_code == 200
    assert "report.xlsx" in response.headers["content-disposition"]


def test_operator_can_export_pdf(
    client_bundle: tuple[TestClient, _FakeDB],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    client, _ = client_bundle
    pdf_path = tmp_path / "report.pdf"
    pdf_path.write_bytes(b"%PDF-1.4")

    def _fake_export_run_pdf(**_kwargs):
        return {
            "absolute_path": str(pdf_path),
            "file_name": "report.pdf",
            "content_type": "application/pdf",
        }

    monkeypatch.setattr(runs_routes, "export_run_pdf", _fake_export_run_pdf)

    response = client.get("/api/v1/mc/runs/run-1/export.pdf", headers={"X-MC-Role": "operator"})

    assert response.status_code == 200
    assert "report.pdf" in response.headers["content-disposition"]
