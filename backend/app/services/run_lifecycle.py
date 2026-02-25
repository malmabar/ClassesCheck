from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional, TypeVar
from uuid import uuid4

from sqlalchemy import delete, select
from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.run import MCRun, MCRunLock, RunStatus


T = TypeVar("T")

IDEMPOTENT_ACTIVE_STATUSES = {
    RunStatus.CREATED.value,
    RunStatus.VALIDATING.value,
    RunStatus.RUNNING.value,
    RunStatus.SUCCEEDED.value,
    RunStatus.PUBLISHED.value,
}


class RunLifecycleError(ValueError):
    """Base lifecycle error for run orchestration."""


class RunLockBusyError(RunLifecycleError):
    """Raised when context lock is already held by another active process."""


def build_run_idempotency_key(
    *,
    input_checksum: Optional[str],
    reference_version: Optional[str],
    semester: str,
    period: str,
    rule_version: str,
    settings_payload: Optional[dict] = None,
) -> str:
    payload = {
        "input_checksum": (input_checksum or "").strip(),
        "reference_version": (reference_version or "").strip(),
        "semester": (semester or "").strip(),
        "period": (period or "").strip(),
        "rule_version": (rule_version or "").strip(),
        "settings": settings_payload or {},
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def find_latest_idempotent_run(db: Session, idempotency_key: Optional[str]) -> Optional[MCRun]:
    if not idempotency_key:
        return None
    return (
        db.execute(
            select(MCRun)
            .where(
                MCRun.idempotency_key == idempotency_key,
                MCRun.status.in_(IDEMPOTENT_ACTIVE_STATUSES),
            )
            .order_by(MCRun.created_at.desc())
            .limit(1)
        )
        .scalars()
        .first()
    )


def is_transient_error(exc: BaseException) -> bool:
    if isinstance(exc, (TimeoutError, ConnectionError, OperationalError)):
        return True
    if isinstance(exc, DBAPIError):
        return bool(exc.connection_invalidated)
    return False


def run_with_single_retry(
    operation: Callable[[int], T],
    on_retry: Optional[Callable[[BaseException, int], None]] = None,
    retry_count: Optional[int] = None,
) -> T:
    max_retry = settings.mc_transient_retry_count if retry_count is None else max(0, int(retry_count))
    attempt = 1
    while True:
        try:
            return operation(attempt)
        except Exception as exc:  # noqa: BLE001
            if attempt > max_retry or not is_transient_error(exc):
                raise
            if on_retry:
                on_retry(exc, attempt)
            attempt += 1


def acquire_run_lock(
    db: Session,
    *,
    semester: str,
    period: str,
    locked_by: Optional[str] = None,
) -> str:
    now = datetime.now(timezone.utc)
    ttl_seconds = max(1, int(settings.mc_run_lock_ttl_seconds))
    expires_at = now + timedelta(seconds=ttl_seconds)

    existing = (
        db.execute(
            select(MCRunLock)
            .where(MCRunLock.semester == semester, MCRunLock.period == period)
            .limit(1)
        )
        .scalars()
        .first()
    )
    if existing is not None:
        if existing.expires_at is not None and existing.expires_at <= now:
            db.delete(existing)
            db.commit()
        else:
            raise RunLockBusyError(
                f"Run lock is active for semester={semester}, period={period}. Try again later."
            )

    lock_token = uuid4().hex
    db.add(
        MCRunLock(
            semester=semester,
            period=period,
            lock_token=lock_token,
            locked_by=locked_by,
            expires_at=expires_at,
        )
    )
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise RunLockBusyError(
            f"Run lock is active for semester={semester}, period={period}. Try again later."
        ) from exc

    return lock_token


def release_run_lock(db: Session, *, lock_token: str) -> None:
    db.execute(delete(MCRunLock).where(MCRunLock.lock_token == lock_token))
    db.commit()
