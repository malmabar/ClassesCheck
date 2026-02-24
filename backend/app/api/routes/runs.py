from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

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


router = APIRouter(prefix="/api/v1/mc/runs", tags=["mc-runs"])


def _ensure_run_exists(db: Session, run_id: str) -> None:
    run_exists = db.scalar(select(func.count()).select_from(MCRun).where(MCRun.id == run_id)) or 0
    if run_exists == 0:
        raise HTTPException(status_code=404, detail="Run not found.")


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
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)

    total = db.scalar(
        select(func.count()).select_from(MCSourceSS01Row).where(MCSourceSS01Row.run_id == run_id)
    ) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCSourceSS01Row)
        .where(MCSourceSS01Row.run_id == run_id)
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
        "has_next": offset + size < total,
        "items": items,
    }


@router.get("/{run_id}/codes")
def list_run_codes(
    run_id: str,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)

    total = db.scalar(
        select(func.count()).select_from(MCCode).where(MCCode.run_id == run_id)
    ) or 0
    offset = (page - 1) * size

    rows = db.execute(
        select(MCCode)
        .where(MCCode.run_id == run_id)
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


@router.post("/{run_id}/publish")
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
        raise HTTPException(
            status_code=500,
            detail=(
                "Publish failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
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
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishHallsCopy.run_id == run_id]
    if room_code:
        filters.append(MCPublishHallsCopy.room_code == room_code)

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
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishCRNsCopy.run_id == run_id]
    if crn:
        filters.append(MCPublishCRNsCopy.crn == crn)

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
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishTrainersSC.run_id == run_id]
    if trainer_job_id:
        filters.append(MCPublishTrainersSC.trainer_job_id == trainer_job_id)

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
    db: Session = Depends(get_db),
):
    _ensure_run_exists(db, run_id)
    filters = [MCPublishDistribution.run_id == run_id]
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


@router.get("/{run_id}/export.xlsx")
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
        raise HTTPException(
            status_code=500,
            detail=(
                "Excel export failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
            ),
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Excel export failed بسبب مشكلة كتابة الملف: {exc}",
        ) from exc
    return FileResponse(
        path=artifact["absolute_path"],
        filename=artifact["file_name"],
        media_type=artifact["content_type"],
    )


@router.get("/{run_id}/export.pdf")
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
        raise HTTPException(
            status_code=500,
            detail=(
                "PDF export failed بسبب مشكلة قاعدة البيانات "
                f"({exc.__class__.__name__}). "
                "تأكد من تنفيذ: alembic -c backend/alembic.ini upgrade head"
            ),
        ) from exc
    except OSError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"PDF export failed بسبب مشكلة كتابة الملف: {exc}",
        ) from exc
    return FileResponse(
        path=artifact["absolute_path"],
        filename=artifact["file_name"],
        media_type=artifact["content_type"],
    )
