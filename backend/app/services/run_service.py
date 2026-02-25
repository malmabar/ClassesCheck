from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

from sqlalchemy import delete, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.codes import MCCode
from app.models.run import MCRun, MCRunLog, RunStatus
from app.models.source import MCSourceSS01Row
from app.services.run_lifecycle import (
    RunLockBusyError,
    acquire_run_lock,
    release_run_lock,
    run_with_single_retry,
)
from app.services.time_slots import resolve_period_and_slots


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

SLOT_MAP: Dict[int, int] = {
    800: 1,
    900: 2,
    1000: 3,
    1100: 4,
    1230: 5,
    1321: 6,
    1415: 7,
    1506: 8,
    1800: 1,
    1900: 2,
    2000: 3,
    2100: 4,
    2200: 5,
}


def _normalize_day_name(day_name: Optional[str]) -> Tuple[Optional[str], Optional[int]]:
    if not day_name:
        return None, None
    normalized = day_name.strip()
    order = DAY_ORDER_MAP.get(normalized)
    if order is None:
        compact = normalized.replace(" ", "")
        order = DAY_ORDER_MAP.get(compact)
    return normalized, order


def _count_codes(db: Session, run_id: str) -> dict:
    total_codes = db.scalar(select(func.count()).select_from(MCCode).where(MCCode.run_id == run_id)) or 0
    morning_count = (
        db.scalar(
            select(func.count()).select_from(MCCode).where(MCCode.run_id == run_id, MCCode.is_morning.is_(True))
        )
        or 0
    )
    evening_count = (
        db.scalar(
            select(func.count()).select_from(MCCode).where(MCCode.run_id == run_id, MCCode.is_evening.is_(True))
        )
        or 0
    )
    return {
        "codes_rows": total_codes,
        "morning_rows": morning_count,
        "evening_rows": evening_count,
    }


def _build_codes_once(
    db: Session,
    *,
    run: MCRun,
    run_id: str,
    triggered_by: str,
    attempt: int,
) -> dict:
    source_rows = db.execute(
        select(MCSourceSS01Row)
        .where(MCSourceSS01Row.run_id == run_id)
        .order_by(MCSourceSS01Row.row_number.asc())
    ).scalars().all()
    if not source_rows:
        raise ValueError("Run has no source SS01 rows.")

    run.status = RunStatus.VALIDATING.value
    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="CODES_BUILD_VALIDATE",
            message="Validating source rows before mc_codes derivation.",
            details_json=json.dumps({"attempt": attempt, "triggered_by": triggered_by}, ensure_ascii=False),
        )
    )

    run.status = RunStatus.RUNNING.value
    run.started_at = datetime.now(timezone.utc)
    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="CODES_BUILD_START",
            message="Starting mc_codes derivation.",
            details_json=json.dumps({"attempt": attempt, "triggered_by": triggered_by}, ensure_ascii=False),
        )
    )

    db.execute(delete(MCCode).where(MCCode.run_id == run_id))

    generated = 0
    morning_count = 0
    evening_count = 0
    skipped_other_period = 0

    for row in source_rows:
        day_name, day_order = _normalize_day_name(row.day_name)
        slot_resolution = resolve_period_and_slots(
            time_value=row.time_value,
            time_hhmm=None,
            section_type=row.section_type,
            period_hint=run.period,
        )
        hhmm = slot_resolution.time_range.start_hhmm
        slot_index = slot_resolution.slot_indices[0] if slot_resolution.slot_indices else None
        is_morning = slot_resolution.period == "صباحي"
        is_evening = slot_resolution.period == "مسائي"

        if run.period in ("صباحي", "مسائي") and slot_resolution.period != run.period:
            skipped_other_period += 1
            continue

        # Backward-compatible fallback for legacy fixed-time single-point rows.
        if slot_index is None and hhmm is not None:
            slot_index = SLOT_MAP.get(hhmm)

        if is_morning:
            morning_count += 1
        if is_evening:
            evening_count += 1

        db.add(
            MCCode(
                run_id=run_id,
                source_row_id=row.id,
                semester=run.semester,
                period=run.period,
                department=row.department,
                course_code=row.course_code,
                course_name=row.course_name,
                crn=row.crn,
                section_type=row.section_type,
                day_name=day_name,
                day_order=day_order,
                time_value=row.time_value,
                time_hhmm=hhmm,
                slot_index=slot_index,
                building_code=row.building_code,
                room_code=row.room_code,
                room_capacity=row.room_capacity,
                registered_count=row.registered_count,
                trainer_job_id=row.trainer_job_id,
                trainer_name=row.trainer_name,
                is_morning=is_morning,
                is_evening=is_evening,
            )
        )
        generated += 1

    run.status = RunStatus.SUCCEEDED.value
    run.finished_at = datetime.now(timezone.utc)

    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="CODES_BUILD_FINISHED",
            message="mc_codes derivation completed.",
            details_json=json.dumps(
                {
                    "attempt": attempt,
                    "generated_rows": generated,
                    "morning_rows": morning_count,
                    "evening_rows": evening_count,
                    "skipped_other_period_rows": skipped_other_period,
                },
                ensure_ascii=False,
            ),
        )
    )

    db.commit()

    total_codes = db.scalar(select(func.count()).select_from(MCCode).where(MCCode.run_id == run_id)) or 0
    return {
        "run_id": run_id,
        "status": run.status,
        "generated_rows": generated,
        "codes_rows": total_codes,
        "morning_rows": morning_count,
        "evening_rows": evening_count,
        "skipped_other_period_rows": skipped_other_period,
        "retry_attempts": attempt - 1,
        "idempotent_hit": False,
    }


def build_codes_for_run(
    db: Session,
    run_id: str,
    triggered_by: str = "api-user",
) -> dict:
    run = db.get(MCRun, run_id)
    if not run:
        raise ValueError("Run not found.")
    lock_token: Optional[str] = None
    try:
        lock_token = acquire_run_lock(
            db=db,
            semester=run.semester,
            period=run.period,
            locked_by=triggered_by,
        )
    except RunLockBusyError:
        raise

    retry_triggered = {"value": False}

    try:
        existing_counts = _count_codes(db=db, run_id=run_id)
        if run.status in (RunStatus.SUCCEEDED.value, RunStatus.PUBLISHED.value) and existing_counts["codes_rows"] > 0:
            db.add(
                MCRunLog(
                    run_id=run_id,
                    level="INFO",
                    code="CODES_BUILD_IDEMPOTENT_HIT",
                    message="Skipped duplicate pipeline run because derived rows already exist.",
                    details_json=json.dumps(
                        {
                            "triggered_by": triggered_by,
                            "idempotency_key": run.idempotency_key,
                        },
                        ensure_ascii=False,
                    ),
                )
            )
            db.commit()
            return {
                "run_id": run_id,
                "status": run.status,
                "generated_rows": existing_counts["codes_rows"],
                "codes_rows": existing_counts["codes_rows"],
                "morning_rows": existing_counts["morning_rows"],
                "evening_rows": existing_counts["evening_rows"],
                "skipped_other_period_rows": 0,
                "retry_attempts": 0,
                "idempotent_hit": True,
            }

        def _operation(attempt: int) -> dict:
            operation_run = db.get(MCRun, run_id)
            if operation_run is None:
                raise ValueError("Run not found.")
            return _build_codes_once(
                db=db,
                run=operation_run,
                run_id=run_id,
                triggered_by=triggered_by,
                attempt=attempt,
            )

        def _on_retry(exc: BaseException, attempt: int) -> None:
            retry_triggered["value"] = True
            db.rollback()
            retry_run = db.get(MCRun, run_id)
            if retry_run is None:
                return
            retry_run.status = RunStatus.RUNNING.value
            db.add(
                MCRunLog(
                    run_id=run_id,
                    level="WARNING",
                    code="CODES_BUILD_RETRY",
                    message="Transient error detected; retrying pipeline run once.",
                    details_json=json.dumps(
                        {
                            "attempt_failed": attempt,
                            "next_attempt": attempt + 1,
                            "error_type": exc.__class__.__name__,
                            "error": str(exc),
                        },
                        ensure_ascii=False,
                    ),
                )
            )
            db.commit()

        result = run_with_single_retry(operation=_operation, on_retry=_on_retry)
        result["retry_triggered"] = retry_triggered["value"]
        return result
    except RunLockBusyError:
        raise
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        failed_run = db.get(MCRun, run_id)
        if failed_run is not None:
            failed_run.status = RunStatus.FAILED.value
            failed_run.finished_at = datetime.now(timezone.utc)
            db.add(
                MCRunLog(
                    run_id=run_id,
                    level="ERROR",
                    code="CODES_BUILD_FAILED",
                    message="Pipeline run failed.",
                    details_json=json.dumps(
                        {
                            "error_type": exc.__class__.__name__,
                            "error": str(exc),
                            "retry_triggered": retry_triggered["value"],
                        },
                        ensure_ascii=False,
                    ),
                )
            )
            db.commit()
        if isinstance(exc, ValueError):
            raise
        raise ValueError(f"Pipeline run failed: {exc}") from exc
    finally:
        if lock_token:
            try:
                release_run_lock(db=db, lock_token=lock_token)
            except SQLAlchemyError:
                db.rollback()
