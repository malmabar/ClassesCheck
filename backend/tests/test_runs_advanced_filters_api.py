from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from fastapi.testclient import TestClient
import pytest
from sqlalchemy.dialects import postgresql

from app.db.session import get_db
from app.main import app


class _FakeResult:
    def __init__(self, rows: list[object]):
        self._rows = rows

    def scalars(self) -> "_FakeResult":
        return self

    def all(self) -> list[object]:
        return self._rows


@dataclass
class _RecordedStmt:
    kind: str
    statement: object


@dataclass
class _FakeRun:
    id: str = "run-1"
    status: str = "SUCCEEDED"
    semester: str = "144620"
    period: str = "صباحي"
    rule_version: str = "rule-v1"
    idempotency_key: str | None = None
    input_checksum: str = "checksum"
    reference_version: str = "beta6"
    started_at: str | None = None
    finished_at: str | None = None
    created_by: str = "tester"
    created_at: str | None = None
    updated_at: str | None = None


class _FakeDB:
    def __init__(self) -> None:
        self.calls: list[_RecordedStmt] = []

    def scalar(self, statement: object, *_args, **_kwargs) -> int:
        self.calls.append(_RecordedStmt(kind="scalar", statement=statement))
        return 1

    def execute(self, statement: object, *_args, **_kwargs) -> _FakeResult:
        self.calls.append(_RecordedStmt(kind="execute", statement=statement))
        return _FakeResult([])

    def rollback(self) -> None:
        return None

    def get(self, _model, key, *_args, **_kwargs) -> _FakeRun:
        return _FakeRun(id=str(key))

    def last_execute_statement(self) -> object:
        execute_calls = [call.statement for call in self.calls if call.kind == "execute"]
        return execute_calls[-1]


@pytest.fixture
def client_bundle() -> Iterator[tuple[TestClient, _FakeDB]]:
    fake_db = _FakeDB()

    def _override_get_db() -> Iterator[_FakeDB]:
        yield fake_db

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as client:
        yield client, fake_db
    app.dependency_overrides.clear()


def _sql(statement: object) -> str:
    return str(
        statement.compile(
            dialect=postgresql.dialect(),
            compile_kwargs={"literal_binds": True},
        )
    )


def test_get_run_includes_checks_ready_flag(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get("/api/v1/mc/runs/run-1", headers={"X-MC-Role": "viewer"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["metrics"]["checks_ready"] is True
    assert payload["metrics"]["checks_finished_count"] >= 1


def test_source_ss01_advanced_filters_are_applied(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/source-ss01",
        headers={"X-MC-Role": "viewer"},
        params={
            "department": "  علوم  ",
            "building_code": " B1 ",
            "crn": " 283 ",
            "trainer": " أحمد ",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {
        "department": "علوم",
        "building_code": "B1",
        "crn": "283",
        "trainer": "أحمد",
    }

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_source_ss01_rows.department ILIKE" in sql
    assert "mc_source_ss01_rows.building_code ILIKE" in sql
    assert "mc_source_ss01_rows.crn ILIKE" in sql
    assert "mc_source_ss01_rows.trainer_job_id ILIKE" in sql
    assert "mc_source_ss01_rows.trainer_name ILIKE" in sql
    assert "علوم" in sql
    assert "B1" in sql
    assert "283" in sql
    assert "أحمد" in sql


def test_codes_advanced_filters_are_applied(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/codes",
        headers={"X-MC-Role": "viewer"},
        params={
            "department": "CS",
            "building_code": "B2",
            "room_code": "A10",
            "crn": "283",
            "trainer": "101",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {
        "department": "CS",
        "building_code": "B2",
        "room_code": "A10",
        "crn": "283",
        "trainer": "101",
    }

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_codes.department ILIKE" in sql
    assert "mc_codes.building_code ILIKE" in sql
    assert "mc_codes.room_code ILIKE" in sql
    assert "mc_codes.crn ILIKE" in sql
    assert "mc_codes.trainer_job_id ILIKE" in sql
    assert "mc_codes.trainer_name ILIKE" in sql


def test_codes_blank_filter_value_is_normalized_to_none(
    client_bundle: tuple[TestClient, _FakeDB],
) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/codes",
        headers={"X-MC-Role": "viewer"},
        params={"department": "   "},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"]["department"] is None

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_codes.department ILIKE" not in sql


def test_halls_filters_include_partial_and_day_slot(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/halls",
        headers={"X-MC-Role": "viewer"},
        params={
            "room_code": "A10",
            "building_code": "B1",
            "crn": "283",
            "day_order": 2,
            "slot_index": 4,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {
        "room_code": "A10",
        "building_code": "B1",
        "crn": "283",
        "day_order": 2,
        "slot_index": 4,
    }

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_publish_halls_copy.room_code ILIKE" in sql
    assert "mc_publish_halls_copy.building_code ILIKE" in sql
    assert "mc_publish_halls_copy.crn_list ILIKE" in sql
    assert "mc_publish_halls_copy.day_order = 2" in sql
    assert "mc_publish_halls_copy.slot_index = 4" in sql


def test_crns_filters_include_trainer_or_and_day_slot(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/crns",
        headers={"X-MC-Role": "viewer"},
        params={
            "crn": "283",
            "course_code": "MTH",
            "room_code": "A1",
            "trainer": "101",
            "day_order": 1,
            "slot_index": 8,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {
        "crn": "283",
        "course_code": "MTH",
        "room_code": "A1",
        "trainer": "101",
        "day_order": 1,
        "slot_index": 8,
    }

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_publish_crns_copy.crn ILIKE" in sql
    assert "mc_publish_crns_copy.course_code ILIKE" in sql
    assert "mc_publish_crns_copy.room_code ILIKE" in sql
    assert "mc_publish_crns_copy.trainer_job_id ILIKE" in sql
    assert "mc_publish_crns_copy.trainer_name ILIKE" in sql
    assert "mc_publish_crns_copy.day_order = 1" in sql
    assert "mc_publish_crns_copy.slot_index = 8" in sql


def test_trainers_filters_include_day_slot(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/trainers",
        headers={"X-MC-Role": "viewer"},
        params={
            "trainer_job_id": "101",
            "trainer_name": "أحمد",
            "crn": "283",
            "day_order": 3,
            "slot_index": 2,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {
        "trainer_job_id": "101",
        "trainer_name": "أحمد",
        "crn": "283",
        "day_order": 3,
        "slot_index": 2,
    }

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_publish_trainers_sc.trainer_job_id ILIKE" in sql
    assert "mc_publish_trainers_sc.trainer_name ILIKE" in sql
    assert "mc_publish_trainers_sc.crn_list ILIKE" in sql
    assert "mc_publish_trainers_sc.day_order = 3" in sql
    assert "mc_publish_trainers_sc.slot_index = 2" in sql


def test_distribution_filters_include_day_slot(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/distribution",
        headers={"X-MC-Role": "viewer"},
        params={"day_order": 5, "slot_index": 7},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"] == {"day_order": 5, "slot_index": 7}

    sql = _sql(fake_db.last_execute_statement())
    assert "mc_publish_distribution.day_order = 5" in sql
    assert "mc_publish_distribution.slot_index = 7" in sql


def test_warnings_endpoint_filters_by_warning_group_and_rule_code(
    client_bundle: tuple[TestClient, _FakeDB],
) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/warnings",
        headers={"X-MC-Role": "viewer"},
        params={"rule_code": "ROOM", "sort": "created_at:desc"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"]["severity_group"] == "warnings"
    assert payload["filters"]["rule_code"] == "ROOM"
    assert payload["filters"]["sort"] == "created_at:desc"

    sql = _sql(fake_db.last_execute_statement())
    assert "upper(" in sql
    assert "mc_issues.severity" in sql
    assert "WARNING" in sql and "WARN" in sql and "MEDIUM" in sql
    assert "mc_issues.rule_code ILIKE" in sql
    assert "created_at DESC" in sql


def test_errors_endpoint_filters_by_error_group_and_rule_code(
    client_bundle: tuple[TestClient, _FakeDB],
) -> None:
    client, fake_db = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/errors",
        headers={"X-MC-Role": "viewer"},
        params={"rule_code": "CAPACITY", "sort": "id:asc"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filters"]["severity_group"] == "errors"
    assert payload["filters"]["rule_code"] == "CAPACITY"
    assert payload["filters"]["sort"] == "id:asc"

    sql = _sql(fake_db.last_execute_statement())
    assert "upper(" in sql
    assert "mc_issues.severity" in sql
    assert "ERROR" in sql and "CRITICAL" in sql and "HIGH" in sql
    assert "mc_issues.rule_code ILIKE" in sql
    assert "ORDER BY mc_core.mc_issues.id ASC" in sql


def test_issue_group_endpoint_rejects_invalid_sort(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get(
        "/api/v1/mc/runs/run-1/errors",
        headers={"X-MC-Role": "viewer"},
        params={"sort": "unknown_field:desc"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["code"] == "BAD_REQUEST"
    assert "Invalid sort field" in payload["message"]


def test_compare_runs_returns_left_right_and_delta(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get(
        "/api/v1/mc/runs/compare",
        headers={"X-MC-Role": "viewer"},
        params={"left_run_id": "run-left", "right_run_id": "run-right"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["left_run_id"] == "run-left"
    assert payload["right_run_id"] == "run-right"
    assert payload["left"]["run"]["id"] == "run-left"
    assert payload["right"]["run"]["id"] == "run-right"
    assert "metrics" in payload["left"]
    assert "metrics" in payload["right"]
    assert "published" in payload["delta"]


def test_compare_runs_rejects_same_run_id(client_bundle: tuple[TestClient, _FakeDB]) -> None:
    client, _ = client_bundle
    response = client.get(
        "/api/v1/mc/runs/compare",
        headers={"X-MC-Role": "viewer"},
        params={"left_run_id": "run-1", "right_run_id": "run-1"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["code"] == "BAD_REQUEST"
    assert "must be different" in payload["message"]
