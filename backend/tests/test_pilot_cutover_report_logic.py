from __future__ import annotations

from app.tools.pilot_cutover_report import (
    _evaluate_period,
    _filter_runs_by_status,
    _filter_runs_by_checksum,
    _parse_created_at,
    _split_statuses,
)


def test_parse_created_at_supports_z_suffix() -> None:
    parsed = _parse_created_at("2026-02-25T01:22:33Z")
    assert parsed is not None
    assert parsed.isoformat().startswith("2026-02-25T01:22:33")


def test_split_statuses_normalizes_and_defaults() -> None:
    assert _split_statuses("published, succeeded") == ("PUBLISHED", "SUCCEEDED")
    assert _split_statuses("   ") == ("PUBLISHED",)


def test_filter_runs_by_status_accepts_only_requested_items() -> None:
    rows = [
        {"id": "a", "status": "PUBLISHED"},
        {"id": "b", "status": "SUCCEEDED"},
        {"id": "c", "status": "FAILED"},
    ]
    filtered = _filter_runs_by_status(rows, ("PUBLISHED", "SUCCEEDED"))
    assert [item["id"] for item in filtered] == ["a", "b"]


def test_filter_runs_by_checksum_respects_requirement_flag() -> None:
    rows = [
        {"id": "a", "input_checksum": "abc"},
        {"id": "b", "input_checksum": "def"},
        {"id": "c", "input_checksum": None},
    ]
    scoped = _filter_runs_by_checksum(
        rows,
        expected_checksum="abc",
        require_match=True,
    )
    assert [item["id"] for item in scoped] == ["a"]

    unscoped = _filter_runs_by_checksum(
        rows,
        expected_checksum="abc",
        require_match=False,
    )
    assert [item["id"] for item in unscoped] == ["a", "b", "c"]


def test_evaluate_period_passes_when_days_and_parity_are_ok() -> None:
    run_reports = [
        {"run_id": "r1", "created_at": "2026-02-20T01:00:00Z", "all_match": True},
        {"run_id": "r2", "created_at": "2026-02-21T01:00:00Z", "all_match": True},
    ]
    result = _evaluate_period("صباحي", run_reports, min_distinct_days=2)
    assert result["status"] == "PASSED"
    assert result["failures"] == []


def test_evaluate_period_fails_on_mismatch() -> None:
    run_reports = [
        {"run_id": "r1", "created_at": "2026-02-20T01:00:00Z", "all_match": True},
        {"run_id": "r2", "created_at": "2026-02-21T01:00:00Z", "all_match": False},
    ]
    result = _evaluate_period("صباحي", run_reports, min_distinct_days=2)
    assert result["status"] == "FAILED"
    assert "parity_mismatch_runs=1" in result["failures"]
    assert result["mismatch_run_ids"] == ["r2"]


def test_evaluate_period_fails_when_days_coverage_is_short() -> None:
    run_reports = [
        {"run_id": "r1", "created_at": "2026-02-20T01:00:00Z", "all_match": True},
        {"run_id": "r2", "created_at": "2026-02-20T02:00:00Z", "all_match": True},
    ]
    result = _evaluate_period("مسائي", run_reports, min_distinct_days=2)
    assert result["status"] == "FAILED"
    assert "insufficient_distinct_days=1/2" in result["failures"]
