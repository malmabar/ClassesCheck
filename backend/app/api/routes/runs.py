from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import desc, func, or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.api.deps.rbac import require_mutation_access, require_read_access
from app.db.session import get_db
from app.models.codes import MCCode
from app.models.issues import MCIssue
from app.models.publish import (
    MCPublishCRNsCopy,
    MCPublishDistribution,
    MCPublishHallsCopy,
    MCPublishTrainersSC,
)
from app.models.run import MCRun, MCRunLog, MCRunOutputArtifact
from app.models.source import MCImportReject, MCSourceSS01Row
from app.services.export_service import export_run_pdf, export_run_xlsx
from app.services.publish_service import publish_run_outputs


router = APIRouter(
    prefix="/api/v1/mc/runs",
    tags=["mc-runs"],
    dependencies=[Depends(require_read_access)],
)

_WARNING_SEVERITIES = ("WARNING", "WARN", "MEDIUM")
_ERROR_SEVERITIES = ("ERROR", "CRITICAL", "HIGH")


def _ensure_run_exists(db: Session, run_id: str) -> None:
    run_exists = db.scalar(select(func.count()).select_from(MCRun).where(MCRun.id == run_id)) or 0
    if run_exists == 0:
        raise HTTPException(status_code=404, detail="Run not found.")


def _normalized_query(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned or None


def _issue_order_clause(sort: Optional[str]):
    sort_value = _normalized_query(sort) or "id:asc"
    field_name, _, direction = sort_value.partition(":")
    direction = (direction or "asc").strip().lower()
    allowed = {
        "id": MCIssue.id,
        "created_at": MCIssue.created_at,
        "severity": MCIssue.severity,
        "rule_code": MCIssue.rule_code,
    }
    field = allowed.get(field_name.strip())
    if field is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field. Allowed: id, created_at, severity, rule_code.",
        )
    if direction not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="Invalid sort direction. Allowed: asc, desc.")
    return desc(field) if direction == "desc" else field.asc()


def _count_rows_for_run(db: Session, model, run_id: str) -> int:
    return db.scalar(select(func.count()).select_from(model).where(model.run_id == run_id)) or 0


def _count_issues_for_run_by_severity(db: Session, run_id: str, severities: tuple[str, ...]) -> int:
    return (
        db.scalar(
            select(func.count())
            .select_from(MCIssue)
            .where(
                MCIssue.run_id == run_id,
                func.upper(MCIssue.severity).in_(severities),
            )
        )
        or 0
    )


def _build_run_compare_snapshot(db: Session, run_id: str) -> dict:
    run = db.get(MCRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")

    checks_finished_count = (
        db.scalar(
            select(func.count())
            .select_from(MCRunLog)
            .where(
                MCRunLog.run_id == run_id,
                MCRunLog.code == "CHECKS_FINISHED",
            )
        )
        or 0
    )

    metrics = {
        "source_rows": _count_rows_for_run(db, MCSourceSS01Row, run_id),
        "rejected_rows": _count_rows_for_run(db, MCImportReject, run_id),
        "codes_rows": _count_rows_for_run(db, MCCode, run_id),
        "issues_total": _count_rows_for_run(db, MCIssue, run_id),
        "issues_warning": _count_issues_for_run_by_severity(db, run_id, _WARNING_SEVERITIES),
        "issues_error": _count_issues_for_run_by_severity(db, run_id, _ERROR_SEVERITIES),
        "checks_finished_count": checks_finished_count,
        "checks_ready": checks_finished_count > 0,
        "published": {
            "halls_rows": _count_rows_for_run(db, MCPublishHallsCopy, run_id),
            "crns_rows": _count_rows_for_run(db, MCPublishCRNsCopy, run_id),
            "trainers_rows": _count_rows_for_run(db, MCPublishTrainersSC, run_id),
            "distribution_rows": _count_rows_for_run(db, MCPublishDistribution, run_id),
        },
        "artifacts_rows": _count_rows_for_run(db, MCRunOutputArtifact, run_id),
    }

    return {
        "run": {
            "id": run.id,
            "status": run.status,
            "semester": run.semester,
            "period": run.period,
            "created_by": run.created_by,
            "created_at": run.created_at,
            "updated_at": run.updated_at,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
        },
        "metrics": metrics,
    }


@router.get("")
def list_runs(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=500),
    period: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    filters = []
    if period:
        filters.append(MCRun.period == period)

    total = db.scalar(select(func.count()).select_from(MCRun).where(*filters)) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCRun).where(*filters).order_by(MCRun.created_at.desc()).offset(offset).limit(size)
    ).scalars().all()

    items = [
        {
            "id": r.id,
            "status": r.status,
            "semester": r.semester,
            "period": r.period,
            "rule_version": r.rule_version,
            "idempotency_key": r.idempotency_key,
            "input_checksum": r.input_checksum,
            "reference_version": r.reference_version,
            "started_at": r.started_at,
            "finished_at": r.finished_at,
            "created_by": r.created_by,
            "created_at": r.created_at,
            "updated_at": r.updated_at,
        }
        for r in rows
    ]

    return {
        "total": total,
        "page": page,
        "size": size,
        "period_filter": period,
        "has_next": offset + size < total,
        "items": items,
    }


@router.get("/compare")
def compare_runs(
    left_run_id: str = Query(..., min_length=1),
    right_run_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    if left_run_id == right_run_id:
        raise HTTPException(status_code=400, detail="left_run_id and right_run_id must be different.")

    left = _build_run_compare_snapshot(db, left_run_id)
    right = _build_run_compare_snapshot(db, right_run_id)

    left_metrics = left["metrics"]
    right_metrics = right["metrics"]

    delta = {
        "source_rows": right_metrics["source_rows"] - left_metrics["source_rows"],
        "rejected_rows": right_metrics["rejected_rows"] - left_metrics["rejected_rows"],
        "codes_rows": right_metrics["codes_rows"] - left_metrics["codes_rows"],
        "issues_total": right_metrics["issues_total"] - left_metrics["issues_total"],
        "issues_warning": right_metrics["issues_warning"] - left_metrics["issues_warning"],
        "issues_error": right_metrics["issues_error"] - left_metrics["issues_error"],
        "artifacts_rows": right_metrics["artifacts_rows"] - left_metrics["artifacts_rows"],
        "published": {
            "halls_rows": right_metrics["published"]["halls_rows"] - left_metrics["published"]["halls_rows"],
            "crns_rows": right_metrics["published"]["crns_rows"] - left_metrics["published"]["crns_rows"],
            "trainers_rows": right_metrics["published"]["trainers_rows"]
            - left_metrics["published"]["trainers_rows"],
            "distribution_rows": right_metrics["published"]["distribution_rows"]
            - left_metrics["published"]["distribution_rows"],
        },
    }

    return {
        "left_run_id": left_run_id,
        "right_run_id": right_run_id,
        "left": left,
        "right": right,
        "delta": delta,
    }


@router.get("/{run_id}")
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(MCRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found.")

    source_count = db.scalar(
        select(func.count()).select_from(MCSourceSS01Row).where(MCSourceSS01Row.run_id == run_id)
    ) or 0
    rejected_count = db.scalar(
        select(func.count()).select_from(MCImportReject).where(MCImportReject.run_id == run_id)
    ) or 0
    checks_finished_count = db.scalar(
        select(func.count())
        .select_from(MCRunLog)
        .where(
            MCRunLog.run_id == run_id,
            MCRunLog.code == "CHECKS_FINISHED",
        )
    ) or 0

    logs = db.execute(
        select(MCRunLog)
        .where(MCRunLog.run_id == run_id)
        .order_by(MCRunLog.created_at.asc())
        .limit(200)
    ).scalars().all()

    return {
        "run": {
            "id": run.id,
            "status": run.status,
            "semester": run.semester,
            "period": run.period,
            "rule_version": run.rule_version,
            "idempotency_key": run.idempotency_key,
            "input_checksum": run.input_checksum,
            "reference_version": run.reference_version,
            "started_at": run.started_at,
            "finished_at": run.finished_at,
            "created_by": run.created_by,
            "created_at": run.created_at,
            "updated_at": run.updated_at,
        },
        "metrics": {
            "source_rows": source_count,
            "rejected_rows": rejected_count,
            "checks_finished_count": checks_finished_count,
            "checks_ready": checks_finished_count > 0,
        },
        "logs": [
            {
                "id": log.id,
                "level": log.level,
                "code": log.code,
                "message": log.message,
                "details_json": log.details_json,
                "created_at": log.created_at,
            }
            for log in logs
        ],
    }


@router.get("/{run_id}/source-ss01")
def list_run_source_ss01(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    department: Optional[str] = Query(default=None),
    building_code: Optional[str] = Query(default=None),
    crn: Optional[str] = Query(default=None),
    trainer: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)

    filters = [MCSourceSS01Row.run_id == run_id]

    department = _normalized_query(department)
    building_code = _normalized_query(building_code)
    crn = _normalized_query(crn)
    trainer = _normalized_query(trainer)

    if department:
        filters.append(MCSourceSS01Row.department.ilike(f"%{department}%"))
    if building_code:
        filters.append(MCSourceSS01Row.building_code.ilike(f"%{building_code}%"))
    if crn:
        filters.append(MCSourceSS01Row.crn.ilike(f"%{crn}%"))
    if trainer:
        filters.append(
            or_(
                MCSourceSS01Row.trainer_job_id.ilike(f"%{trainer}%"),
                MCSourceSS01Row.trainer_name.ilike(f"%{trainer}%"),
            )
        )

    total = db.scalar(select(func.count()).select_from(MCSourceSS01Row).where(*filters)) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCSourceSS01Row)
        .where(*filters)
        .order_by(MCSourceSS01Row.row_number.asc())
        .offset(offset)
        .limit(size)
    ).scalars().all()

    items = [
        {
            "id": row.id,
            "run_id": row.run_id,
            "row_number": row.row_number,
            "training_term": row.training_term,
            "department": row.department,
            "course_code": row.course_code,
            "course_name": row.course_name,
            "crn": row.crn,
            "section_type": row.section_type,
            "day_name": row.day_name,
            "time_value": row.time_value,
            "building_code": row.building_code,
            "room_code": row.room_code,
            "room_capacity": row.room_capacity,
            "registered_count": row.registered_count,
            "trainer_job_id": row.trainer_job_id,
            "trainer_name": row.trainer_name,
            "created_at": row.created_at,
        }
        for row in rows
    ]

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "department": department,
            "building_code": building_code,
            "crn": crn,
            "trainer": trainer,
        },
        "has_next": offset + size < total,
        "items": items,
    }


@router.get("/{run_id}/warnings")
def list_run_warnings(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    rule_code: Optional[str] = Query(default=None),
    sort: Optional[str] = Query(default="created_at:desc"),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    rule_code = _normalized_query(rule_code)
    order_clause = _issue_order_clause(sort)

    filters = [
        MCIssue.run_id == run_id,
        func.upper(MCIssue.severity).in_(_WARNING_SEVERITIES),
    ]
    if rule_code:
        filters.append(MCIssue.rule_code.ilike(f"%{rule_code}%"))

    total = db.scalar(select(func.count()).select_from(MCIssue).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCIssue)
        .where(*filters)
        .order_by(order_clause)
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "severity_group": "warnings",
            "rule_code": rule_code,
            "sort": sort,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "code_id": row.code_id,
                "related_code_id": row.related_code_id,
                "issue_type": row.issue_type,
                "severity": row.severity,
                "rule_code": row.rule_code,
                "message": row.message,
                "conflict_key": row.conflict_key,
                "details_json": row.details_json,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/errors")
def list_run_errors(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    rule_code: Optional[str] = Query(default=None),
    sort: Optional[str] = Query(default="created_at:desc"),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    rule_code = _normalized_query(rule_code)
    order_clause = _issue_order_clause(sort)

    filters = [
        MCIssue.run_id == run_id,
        func.upper(MCIssue.severity).in_(_ERROR_SEVERITIES),
    ]
    if rule_code:
        filters.append(MCIssue.rule_code.ilike(f"%{rule_code}%"))

    total = db.scalar(select(func.count()).select_from(MCIssue).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCIssue)
        .where(*filters)
        .order_by(order_clause)
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "severity_group": "errors",
            "rule_code": rule_code,
            "sort": sort,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "code_id": row.code_id,
                "related_code_id": row.related_code_id,
                "issue_type": row.issue_type,
                "severity": row.severity,
                "rule_code": row.rule_code,
                "message": row.message,
                "conflict_key": row.conflict_key,
                "details_json": row.details_json,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/codes")
def list_run_codes(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    department: Optional[str] = Query(default=None),
    building_code: Optional[str] = Query(default=None),
    room_code: Optional[str] = Query(default=None),
    crn: Optional[str] = Query(default=None),
    trainer: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)

    filters = [MCCode.run_id == run_id]

    department = _normalized_query(department)
    building_code = _normalized_query(building_code)
    room_code = _normalized_query(room_code)
    crn = _normalized_query(crn)
    trainer = _normalized_query(trainer)

    if department:
        filters.append(MCCode.department.ilike(f"%{department}%"))
    if building_code:
        filters.append(MCCode.building_code.ilike(f"%{building_code}%"))
    if room_code:
        filters.append(MCCode.room_code.ilike(f"%{room_code}%"))
    if crn:
        filters.append(MCCode.crn.ilike(f"%{crn}%"))
    if trainer:
        filters.append(
            or_(
                MCCode.trainer_job_id.ilike(f"%{trainer}%"),
                MCCode.trainer_name.ilike(f"%{trainer}%"),
            )
        )

    total = db.scalar(select(func.count()).select_from(MCCode).where(*filters)) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCCode)
        .where(*filters)
        .order_by(MCCode.id.asc())
        .offset(offset)
        .limit(size)
    ).scalars().all()

    items = [
        {
            "id": row.id,
            "run_id": row.run_id,
            "source_row_id": row.source_row_id,
            "semester": row.semester,
            "period": row.period,
            "department": row.department,
            "course_code": row.course_code,
            "course_name": row.course_name,
            "crn": row.crn,
            "section_type": row.section_type,
            "day_name": row.day_name,
            "day_order": row.day_order,
            "time_value": row.time_value,
            "time_hhmm": row.time_hhmm,
            "slot_index": row.slot_index,
            "building_code": row.building_code,
            "room_code": row.room_code,
            "room_capacity": row.room_capacity,
            "registered_count": row.registered_count,
            "trainer_job_id": row.trainer_job_id,
            "trainer_name": row.trainer_name,
            "is_morning": row.is_morning,
            "is_evening": row.is_evening,
            "created_at": row.created_at,
        }
        for row in rows
    ]

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "department": department,
            "building_code": building_code,
            "room_code": room_code,
            "crn": crn,
            "trainer": trainer,
        },
        "has_next": offset + size < total,
        "items": items,
    }


@router.get("/{run_id}/issues")
def list_run_issues(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    rule_code: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)

    filters = [MCIssue.run_id == run_id]
    if rule_code:
        filters.append(MCIssue.rule_code == rule_code)
    if severity:
        filters.append(MCIssue.severity == severity)

    total = db.scalar(select(func.count()).select_from(MCIssue).where(*filters)) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCIssue)
        .where(*filters)
        .order_by(MCIssue.id.asc())
        .offset(offset)
        .limit(size)
    ).scalars().all()

    items = [
        {
            "id": row.id,
            "run_id": row.run_id,
            "code_id": row.code_id,
            "related_code_id": row.related_code_id,
            "issue_type": row.issue_type,
            "severity": row.severity,
            "rule_code": row.rule_code,
            "message": row.message,
            "conflict_key": row.conflict_key,
            "details_json": row.details_json,
            "created_at": row.created_at,
        }
        for row in rows
    ]

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "has_next": offset + size < total,
        "items": items,
    }


@router.post("/{run_id}/publish", dependencies=[Depends(require_mutation_access)])
def publish_run(
    run_id: str,
    created_by: str = Query(default="api-user"),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    try:
        result = publish_run_outputs(db=db, run_id=run_id, triggered_by=created_by)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Publish failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
            ),
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Publish failed بسبب خطأ غير متوقع "
                f"({exc.__class__.__name__}): {exc}"
            ),
        ) from exc
    return {
        "message": "Run outputs published successfully.",
        "result": result,
    }


@router.get("/{run_id}/halls")
def list_run_halls(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    room_code: Optional[str] = Query(default=None),
    building_code: Optional[str] = Query(default=None),
    crn: Optional[str] = Query(default=None),
    day_order: Optional[int] = Query(default=None, ge=1, le=5),
    slot_index: Optional[int] = Query(default=None, ge=1, le=8),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishHallsCopy.run_id == run_id]

    room_code = _normalized_query(room_code)
    building_code = _normalized_query(building_code)
    crn = _normalized_query(crn)

    if room_code:
        filters.append(MCPublishHallsCopy.room_code.ilike(f"%{room_code}%"))
    if building_code:
        filters.append(MCPublishHallsCopy.building_code.ilike(f"%{building_code}%"))
    if crn:
        filters.append(MCPublishHallsCopy.crn_list.ilike(f"%{crn}%"))
    if day_order is not None:
        filters.append(MCPublishHallsCopy.day_order == day_order)
    if slot_index is not None:
        filters.append(MCPublishHallsCopy.slot_index == slot_index)

    total = db.scalar(select(func.count()).select_from(MCPublishHallsCopy).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCPublishHallsCopy)
        .where(*filters)
        .order_by(
            MCPublishHallsCopy.room_code.asc(),
            MCPublishHallsCopy.day_order.asc(),
            MCPublishHallsCopy.slot_index.asc(),
        )
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "room_code": room_code,
            "building_code": building_code,
            "crn": crn,
            "day_order": day_order,
            "slot_index": slot_index,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "semester": row.semester,
                "period": row.period,
                "room_code": row.room_code,
                "building_code": row.building_code,
                "day_name": row.day_name,
                "day_order": row.day_order,
                "slot_index": row.slot_index,
                "occupancy_count": row.occupancy_count,
                "crn_count": row.crn_count,
                "crn_list": row.crn_list,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/crns")
def list_run_crns(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    crn: Optional[str] = Query(default=None),
    course_code: Optional[str] = Query(default=None),
    room_code: Optional[str] = Query(default=None),
    trainer: Optional[str] = Query(default=None),
    day_order: Optional[int] = Query(default=None, ge=1, le=5),
    slot_index: Optional[int] = Query(default=None, ge=1, le=8),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishCRNsCopy.run_id == run_id]

    crn = _normalized_query(crn)
    course_code = _normalized_query(course_code)
    room_code = _normalized_query(room_code)
    trainer = _normalized_query(trainer)

    if crn:
        filters.append(MCPublishCRNsCopy.crn.ilike(f"%{crn}%"))
    if course_code:
        filters.append(MCPublishCRNsCopy.course_code.ilike(f"%{course_code}%"))
    if room_code:
        filters.append(MCPublishCRNsCopy.room_code.ilike(f"%{room_code}%"))
    if trainer:
        filters.append(
            or_(
                MCPublishCRNsCopy.trainer_job_id.ilike(f"%{trainer}%"),
                MCPublishCRNsCopy.trainer_name.ilike(f"%{trainer}%"),
            )
        )
    if day_order is not None:
        filters.append(MCPublishCRNsCopy.day_order == day_order)
    if slot_index is not None:
        filters.append(MCPublishCRNsCopy.slot_index == slot_index)

    total = db.scalar(select(func.count()).select_from(MCPublishCRNsCopy).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCPublishCRNsCopy)
        .where(*filters)
        .order_by(
            MCPublishCRNsCopy.crn.asc(),
            MCPublishCRNsCopy.day_order.asc(),
            MCPublishCRNsCopy.slot_index.asc(),
        )
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "crn": crn,
            "course_code": course_code,
            "room_code": room_code,
            "trainer": trainer,
            "day_order": day_order,
            "slot_index": slot_index,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "semester": row.semester,
                "period": row.period,
                "crn": row.crn,
                "course_code": row.course_code,
                "course_name": row.course_name,
                "room_code": row.room_code,
                "trainer_job_id": row.trainer_job_id,
                "trainer_name": row.trainer_name,
                "day_name": row.day_name,
                "day_order": row.day_order,
                "slot_index": row.slot_index,
                "occupancy_count": row.occupancy_count,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/trainers")
def list_run_trainers(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    trainer_job_id: Optional[str] = Query(default=None),
    trainer_name: Optional[str] = Query(default=None),
    crn: Optional[str] = Query(default=None),
    day_order: Optional[int] = Query(default=None, ge=1, le=5),
    slot_index: Optional[int] = Query(default=None, ge=1, le=8),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishTrainersSC.run_id == run_id]

    trainer_job_id = _normalized_query(trainer_job_id)
    trainer_name = _normalized_query(trainer_name)
    crn = _normalized_query(crn)

    if trainer_job_id:
        filters.append(MCPublishTrainersSC.trainer_job_id.ilike(f"%{trainer_job_id}%"))
    if trainer_name:
        filters.append(MCPublishTrainersSC.trainer_name.ilike(f"%{trainer_name}%"))
    if crn:
        filters.append(MCPublishTrainersSC.crn_list.ilike(f"%{crn}%"))
    if day_order is not None:
        filters.append(MCPublishTrainersSC.day_order == day_order)
    if slot_index is not None:
        filters.append(MCPublishTrainersSC.slot_index == slot_index)

    total = db.scalar(select(func.count()).select_from(MCPublishTrainersSC).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCPublishTrainersSC)
        .where(*filters)
        .order_by(
            MCPublishTrainersSC.trainer_job_id.asc(),
            MCPublishTrainersSC.day_order.asc(),
            MCPublishTrainersSC.slot_index.asc(),
        )
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "trainer_job_id": trainer_job_id,
            "trainer_name": trainer_name,
            "crn": crn,
            "day_order": day_order,
            "slot_index": slot_index,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "semester": row.semester,
                "period": row.period,
                "trainer_job_id": row.trainer_job_id,
                "trainer_name": row.trainer_name,
                "day_name": row.day_name,
                "day_order": row.day_order,
                "slot_index": row.slot_index,
                "load_count": row.load_count,
                "crn_count": row.crn_count,
                "crn_list": row.crn_list,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/distribution")
def list_run_distribution(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    day_order: Optional[int] = Query(default=None, ge=1, le=5),
    slot_index: Optional[int] = Query(default=None, ge=1, le=8),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishDistribution.run_id == run_id]
    if day_order is not None:
        filters.append(MCPublishDistribution.day_order == day_order)
    if slot_index is not None:
        filters.append(MCPublishDistribution.slot_index == slot_index)
    total = db.scalar(select(func.count()).select_from(MCPublishDistribution).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCPublishDistribution)
        .where(*filters)
        .order_by(
            MCPublishDistribution.day_order.asc(),
            MCPublishDistribution.slot_index.asc(),
        )
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "filters": {
            "day_order": day_order,
            "slot_index": slot_index,
        },
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "semester": row.semester,
                "period": row.period,
                "day_name": row.day_name,
                "day_order": row.day_order,
                "slot_index": row.slot_index,
                "occupied_cells": row.occupied_cells,
                "total_cells": row.total_cells,
                "occupancy_ratio": row.occupancy_ratio,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/artifacts")
def list_run_artifacts(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    artifact_type: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCRunOutputArtifact.run_id == run_id]
    if artifact_type:
        filters.append(MCRunOutputArtifact.artifact_type == artifact_type)

    total = db.scalar(select(func.count()).select_from(MCRunOutputArtifact).where(*filters)) or 0
    offset = (page - 1) * size
    rows = db.execute(
        select(MCRunOutputArtifact)
        .where(*filters)
        .order_by(MCRunOutputArtifact.created_at.desc())
        .offset(offset)
        .limit(size)
    ).scalars().all()

    return {
        "run_id": run_id,
        "total": total,
        "page": page,
        "size": size,
        "has_next": offset + size < total,
        "items": [
            {
                "id": row.id,
                "run_id": row.run_id,
                "artifact_type": row.artifact_type,
                "file_name": row.file_name,
                "content_type": row.content_type,
                "file_size": row.file_size,
                "checksum": row.checksum,
                "storage_path": row.storage_path,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }


@router.get("/{run_id}/export.xlsx", dependencies=[Depends(require_mutation_access)])
def download_run_export_xlsx(
    run_id: str,
    created_by: str = Query(default="api-user"),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    try:
        artifact = export_run_xlsx(db=db, run_id=run_id, triggered_by=created_by)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Excel export failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
            ),
        ) from exc
    except OSError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Excel export failed بسبب مشكلة كتابة الملف: {exc}",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "Excel export failed بسبب خطأ غير متوقع "
                f"({exc.__class__.__name__}): {exc}"
            ),
        ) from exc
    return FileResponse(
        path=artifact["absolute_path"],
        filename=artifact["file_name"],
        media_type=artifact["content_type"],
    )


@router.get("/{run_id}/export.pdf", dependencies=[Depends(require_mutation_access)])
def download_run_export_pdf(
    run_id: str,
    created_by: str = Query(default="api-user"),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    try:
        artifact = export_run_pdf(db=db, run_id=run_id, triggered_by=created_by)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "PDF export failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
            ),
        ) from exc
    except OSError as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed بسبب مشكلة كتابة الملف: {exc}",
        ) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=(
                "PDF export failed بسبب خطأ غير متوقع "
                f"({exc.__class__.__name__}): {exc}"
            ),
        ) from exc
    return FileResponse(
        path=artifact["absolute_path"],
        filename=artifact["file_name"],
        media_type=artifact["content_type"],
    )
