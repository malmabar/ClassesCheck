from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, Optional, Set, Tuple

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.codes import MCCode
from app.models.publish import (
    MCPublishCRNsCopy,
    MCPublishDistribution,
    MCPublishHallsCopy,
    MCPublishTrainersSC,
)
from app.models.run import MCRun, MCRunLog, RunStatus
from app.services.schema_guard import ensure_publish_schema
from app.services.time_slots import resolve_period_and_slots


DAY_LABEL_BY_ORDER: Dict[int, str] = {
    1: "الأحد",
    2: "الاثنين",
    3: "الثلاثاء",
    4: "الأربعاء",
    5: "الخميس",
}


def _safe_text(value: Optional[str]) -> str:
    return str(value or "").strip()


def _resolve_slots(code: MCCode) -> list[int]:
    slot_resolution = resolve_period_and_slots(
        time_value=code.time_value,
        time_hhmm=code.time_hhmm,
        section_type=code.section_type,
        period_hint=code.period,
    )
    resolved = [slot for slot in slot_resolution.slot_indices if 1 <= slot <= 8]
    if not resolved and code.slot_index is not None and 1 <= int(code.slot_index) <= 8:
        resolved = [int(code.slot_index)]
    return sorted(set(resolved))


def _ensure_publish_preconditions(db: Session, run: MCRun) -> None:
    checks_finished_count = db.scalar(
        select(func.count())
        .select_from(MCRunLog)
        .where(
            MCRunLog.run_id == run.id,
            MCRunLog.code == "CHECKS_FINISHED",
        )
    ) or 0
    if checks_finished_count == 0:
        raise ValueError("Run checks must be executed before publishing.")


def publish_run_outputs(
    db: Session,
    run_id: str,
    triggered_by: str = "api-user",
) -> dict:
    ensure_publish_schema(db)

    run = db.get(MCRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    _ensure_publish_preconditions(db, run)

    codes = db.execute(
        select(MCCode).where(MCCode.run_id == run_id).order_by(MCCode.id.asc())
    ).scalars().all()
    if not codes:
        raise ValueError("Run has no derived mc_codes rows.")

    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="PUBLISH_START",
            message="Publishing run outputs into snapshot tables.",
            details_json=json.dumps({"triggered_by": triggered_by}, ensure_ascii=False),
        )
    )

    db.execute(delete(MCPublishHallsCopy).where(MCPublishHallsCopy.run_id == run_id))
    db.execute(delete(MCPublishCRNsCopy).where(MCPublishCRNsCopy.run_id == run_id))
    db.execute(delete(MCPublishTrainersSC).where(MCPublishTrainersSC.run_id == run_id))
    db.execute(delete(MCPublishDistribution).where(MCPublishDistribution.run_id == run_id))

    halls_agg: Dict[Tuple[str, int, int], dict] = {}
    crns_agg: Dict[Tuple[str, int, int], dict] = {}
    trainers_agg: Dict[Tuple[str, int, int], dict] = {}
    occupied_rooms_by_slot: Dict[Tuple[int, int], Set[str]] = defaultdict(set)
    all_rooms: Set[str] = set()

    for code in codes:
        if code.day_order is None:
            continue

        day_order = int(code.day_order)
        if day_order not in DAY_LABEL_BY_ORDER:
            continue
        day_name = _safe_text(code.day_name) or DAY_LABEL_BY_ORDER[day_order]
        slots = _resolve_slots(code)
        if not slots:
            continue

        room_code = _safe_text(code.room_code)
        crn = _safe_text(code.crn)
        trainer_job_id = _safe_text(code.trainer_job_id)

        if room_code:
            all_rooms.add(room_code)

        for slot_index in slots:
            if room_code:
                hall_key = (room_code, day_order, slot_index)
                hall_row = halls_agg.setdefault(
                    hall_key,
                    {
                        "building_code": _safe_text(code.building_code) or None,
                        "day_name": day_name,
                        "occupancy_count": 0,
                        "crns": set(),
                    },
                )
                hall_row["occupancy_count"] += 1
                if crn:
                    hall_row["crns"].add(crn)
                occupied_rooms_by_slot[(day_order, slot_index)].add(room_code)

            if crn:
                crn_key = (crn, day_order, slot_index)
                crn_row = crns_agg.setdefault(
                    crn_key,
                    {
                        "course_code": _safe_text(code.course_code) or None,
                        "course_name": _safe_text(code.course_name) or None,
                        "room_code": room_code or None,
                        "trainer_job_id": trainer_job_id or None,
                        "trainer_name": _safe_text(code.trainer_name) or None,
                        "day_name": day_name,
                        "occupancy_count": 0,
                    },
                )
                crn_row["occupancy_count"] += 1

            if trainer_job_id:
                trainer_key = (trainer_job_id, day_order, slot_index)
                trainer_row = trainers_agg.setdefault(
                    trainer_key,
                    {
                        "trainer_name": _safe_text(code.trainer_name) or None,
                        "day_name": day_name,
                        "load_count": 0,
                        "crns": set(),
                    },
                )
                trainer_row["load_count"] += 1
                if crn:
                    trainer_row["crns"].add(crn)

    for (room_code, day_order, slot_index), data in sorted(halls_agg.items()):
        crns = sorted(data["crns"])
        db.add(
            MCPublishHallsCopy(
                run_id=run_id,
                semester=run.semester,
                period=run.period,
                room_code=room_code,
                building_code=data["building_code"],
                day_name=data["day_name"],
                day_order=day_order,
                slot_index=slot_index,
                occupancy_count=data["occupancy_count"],
                crn_count=len(crns),
                crn_list=", ".join(crns) if crns else None,
            )
        )

    for (crn, day_order, slot_index), data in sorted(crns_agg.items()):
        db.add(
            MCPublishCRNsCopy(
                run_id=run_id,
                semester=run.semester,
                period=run.period,
                crn=crn,
                course_code=data["course_code"],
                course_name=data["course_name"],
                room_code=data["room_code"],
                trainer_job_id=data["trainer_job_id"],
                trainer_name=data["trainer_name"],
                day_name=data["day_name"],
                day_order=day_order,
                slot_index=slot_index,
                occupancy_count=data["occupancy_count"],
            )
        )

    for (trainer_job_id, day_order, slot_index), data in sorted(trainers_agg.items()):
        crns = sorted(data["crns"])
        db.add(
            MCPublishTrainersSC(
                run_id=run_id,
                semester=run.semester,
                period=run.period,
                trainer_job_id=trainer_job_id,
                trainer_name=data["trainer_name"],
                day_name=data["day_name"],
                day_order=day_order,
                slot_index=slot_index,
                load_count=data["load_count"],
                crn_count=len(crns),
                crn_list=", ".join(crns) if crns else None,
            )
        )

    total_room_count = len(all_rooms)
    for day_order in range(1, 6):
        for slot_index in range(1, 9):
            occupied_cells = len(occupied_rooms_by_slot.get((day_order, slot_index), set()))
            ratio = 0.0 if total_room_count == 0 else (occupied_cells / total_room_count) * 100.0
            db.add(
                MCPublishDistribution(
                    run_id=run_id,
                    semester=run.semester,
                    period=run.period,
                    day_name=DAY_LABEL_BY_ORDER[day_order],
                    day_order=day_order,
                    slot_index=slot_index,
                    occupied_cells=occupied_cells,
                    total_cells=total_room_count,
                    occupancy_ratio=round(ratio, 2),
                )
            )

    run.status = RunStatus.PUBLISHED.value
    run.finished_at = datetime.now(timezone.utc)

    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="PUBLISH_FINISHED",
            message="Publish snapshot tables generated successfully.",
            details_json=json.dumps(
                {
                    "halls_rows": len(halls_agg),
                    "crns_rows": len(crns_agg),
                    "trainers_rows": len(trainers_agg),
                    "distribution_rows": 40,
                    "total_rooms": total_room_count,
                },
                ensure_ascii=False,
            ),
        )
    )

    db.commit()

    return {
        "run_id": run_id,
        "status": run.status,
        "halls_rows": len(halls_agg),
        "crns_rows": len(crns_agg),
        "trainers_rows": len(trainers_agg),
        "distribution_rows": 40,
        "total_rooms": total_room_count,
    }
