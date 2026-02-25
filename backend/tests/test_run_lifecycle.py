from __future__ import annotations

import pytest

from app.services.run_lifecycle import build_run_idempotency_key, run_with_single_retry


def test_build_run_idempotency_key_is_stable() -> None:
    key_a = build_run_idempotency_key(
        input_checksum="abc",
        reference_version="beta6",
        semester="144620",
        period="صباحي",
        rule_version="v1.1",
        settings_payload={"source": "SS01"},
    )
    key_b = build_run_idempotency_key(
        input_checksum="abc",
        reference_version="beta6",
        semester="144620",
        period="صباحي",
        rule_version="v1.1",
        settings_payload={"source": "SS01"},
    )

    assert key_a == key_b
    assert len(key_a) == 64


def test_build_run_idempotency_key_changes_with_settings() -> None:
    key_a = build_run_idempotency_key(
        input_checksum="abc",
        reference_version="beta6",
        semester="144620",
        period="صباحي",
        rule_version="v1.1",
        settings_payload={"source": "SS01"},
    )
    key_b = build_run_idempotency_key(
        input_checksum="abc",
        reference_version="beta6",
        semester="144620",
        period="صباحي",
        rule_version="v1.1",
        settings_payload={"source": "SS01", "variant": "v2"},
    )

    assert key_a != key_b


def test_run_with_single_retry_retries_once_on_transient_error() -> None:
    state = {"calls": 0, "retry_events": 0}

    def _operation(_attempt: int) -> str:
        state["calls"] += 1
        if state["calls"] == 1:
            raise TimeoutError("temporary timeout")
        return "ok"

    def _on_retry(_exc: BaseException, _attempt: int) -> None:
        state["retry_events"] += 1

    result = run_with_single_retry(operation=_operation, on_retry=_on_retry, retry_count=1)

    assert result == "ok"
    assert state["calls"] == 2
    assert state["retry_events"] == 1


def test_run_with_single_retry_raises_after_retry_exhausted() -> None:
    state = {"calls": 0}

    def _operation(_attempt: int) -> str:
        state["calls"] += 1
        raise TimeoutError("still failing")

    with pytest.raises(TimeoutError):
        run_with_single_retry(operation=_operation, retry_count=1)

    assert state["calls"] == 2


def test_run_with_single_retry_does_not_retry_non_transient_error() -> None:
    state = {"calls": 0}

    def _operation(_attempt: int) -> str:
        state["calls"] += 1
        raise ValueError("not transient")

    with pytest.raises(ValueError):
        run_with_single_retry(operation=_operation, retry_count=1)

    assert state["calls"] == 1
