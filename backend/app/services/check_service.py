from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.codes import MCCode
from app.models.issues import MCIssue
from app.models.run import MCRun, MCRunLog, RunStatus
from app.services.time_slots import resolve_period_and_slots


def _safe_text(value: Optional[str]) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _conflict_key(entity: str, key_value: str, day_order: int, code_id: int) -> str:
    return f"{entity}:{key_value}|day:{day_order}|code:{code_id}"


def _collect_code_conflicts(
    grouped_by_slot: Dict[Tuple[str, int, int], List[MCCode]],
) -> Dict[Tuple[str, int, int], Dict[str, List[int]]]:
    """
    Collapse repeated slot-level overlaps into one issue per code/entity/day.

    This prevents repeated counting for the same code when a conflict spans
    multiple consecutive slots.
    """
    code_conflicts: Dict[Tuple[str, int, int], Dict[str, set[int]]] = defaultdict(
        lambda: {"peer_ids": set(), "slot_indices": set()}
    )

    for (entity_key, day_order, slot_index), grouped_codes in grouped_by_slot.items():
        unique_ids = sorted({c.id for c in grouped_codes if c.id is not None})
        if len(unique_ids) <= 1:
            continue
        for current_id in unique_ids:
            peers = [peer_id for peer_id in unique_ids if peer_id != current_id]
            key = (entity_key, day_order, current_id)
            code_conflicts[key]["peer_ids"].update(peers)
            code_conflicts[key]["slot_indices"].add(slot_index)

    return {
        key: {
            "peer_ids": sorted(payload["peer_ids"]),
            "slot_indices": sorted(payload["slot_indices"]),
        }
        for key, payload in code_conflicts.items()
    }


def _add_issue(
    db: Session,
    run_id: str,
    code_id: Optional[int],
    related_code_id: Optional[int],
    issue_type: str,
    rule_code: str,
    message: str,
    conflict_key: Optional[str],
    details: Optional[dict] = None,
    severity: str = "ERROR",
) -> None:
    db.add(
        MCIssue(
            run_id=run_id,
            code_id=code_id,
            related_code_id=related_code_id,
            issue_type=issue_type,
            severity=severity,
            rule_code=rule_code,
            message=message,
            conflict_key=conflict_key,
            details_json=json.dumps(details, ensure_ascii=False) if details else None,
        )
    )


def run_checks_for_run(db: Session, run_id: str, triggered_by: str = "api-user") -> dict:
    run = db.get(MCRun, run_id)
    if not run:
        raise ValueError("Run not found.")

    codes = db.execute(
        select(MCCode).where(MCCode.run_id == run_id).order_by(MCCode.id.asc())
    ).scalars().all()
    if not codes:
        raise ValueError("Run has no derived mc_codes rows.")

    run.status = RunStatus.RUNNING.value
    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="CHECKS_START",
            message="Starting validation checks.",
            details_json=json.dumps({"triggered_by": triggered_by}, ensure_ascii=False),
        )
    )
    db.execute(delete(MCIssue).where(MCIssue.run_id == run_id))

    counts: Dict[str, int] = {
        "trainer_time_conflict": 0,
        "room_time_conflict": 0,
        "capacity_exceeded": 0,
    }
    capacity_seen: set[str] = set()

    # Rule: registered count cannot exceed room capacity.
    for code in codes:
        if code.registered_count is None or code.room_capacity is None:
            continue
        if code.registered_count <= code.room_capacity:
            continue

        capacity_key = _safe_text(code.crn) or f"code:{code.id}"
        if capacity_key in capacity_seen:
            continue
        capacity_seen.add(capacity_key)

        counts["capacity_exceeded"] += 1
        _add_issue(
            db=db,
            run_id=run_id,
            code_id=code.id,
            related_code_id=None,
            issue_type="CAPACITY",
            rule_code="ROOM_CAPACITY_EXCEEDED",
            message=(
                f"Registered ({code.registered_count}) exceeds room capacity ({code.room_capacity}) "
                f"for CRN {code.crn or '-'}."
            ),
            conflict_key=f"room:{_safe_text(code.room_code)}|crn:{_safe_text(code.crn)}",
            details={
                "crn": code.crn,
                "room_code": code.room_code,
                "room_capacity": code.room_capacity,
                "registered_count": code.registered_count,
                "dedupe_key": capacity_key,
            },
        )

    trainer_groups: Dict[Tuple[str, int, int], List[MCCode]] = defaultdict(list)
    room_groups: Dict[Tuple[str, int, int], List[MCCode]] = defaultdict(list)
    code_by_id: Dict[int, MCCode] = {c.id: c for c in codes if c.id is not None}

    for code in codes:
        if code.day_order is None:
            continue

        slot_resolution = resolve_period_and_slots(
            time_value=code.time_value,
            time_hhmm=code.time_hhmm,
            section_type=code.section_type,
            period_hint=code.period,
        )
        resolved_slots = list(slot_resolution.slot_indices)
        if not resolved_slots and code.slot_index is not None and 1 <= code.slot_index <= 8:
            resolved_slots = [code.slot_index]
        if not resolved_slots:
            continue

        trainer = _safe_text(code.trainer_job_id)
        room = _safe_text(code.room_code)
        for slot_index in resolved_slots:
            if trainer:
                trainer_groups[(trainer, code.day_order, slot_index)].append(code)
            if room:
                room_groups[(room, code.day_order, slot_index)].append(code)

    # Rule: a trainer cannot have overlapping classes in same day.
    trainer_code_conflicts = _collect_code_conflicts(trainer_groups)
    for (trainer_job_id, day_order, code_id), payload in sorted(
        trainer_code_conflicts.items(),
        key=lambda item: (item[0][0], item[0][1], item[0][2]),
    ):
        current_code = code_by_id.get(code_id)
        if current_code is None:
            continue
        peer_ids = payload["peer_ids"]
        slot_indices = payload["slot_indices"]
        if not peer_ids:
            continue

        counts["trainer_time_conflict"] += 1
        _add_issue(
            db=db,
            run_id=run_id,
            code_id=code_id,
            related_code_id=peer_ids[0],
            issue_type="CONFLICT",
            rule_code="TRAINER_TIME_CONFLICT",
            message=(
                f"Trainer {trainer_job_id} has overlapping classes "
                f"(day={day_order}, slots={','.join(str(x) for x in slot_indices)})."
            ),
            conflict_key=_conflict_key("trainer", trainer_job_id, day_order, code_id),
            details={
                "trainer_job_id": trainer_job_id,
                "day_order": day_order,
                "slot_indices": slot_indices,
                "code_id": code_id,
                "peer_ids": peer_ids,
                "time_value": current_code.time_value,
            },
        )

    # Rule: a room cannot host overlapping classes in same day.
    room_code_conflicts = _collect_code_conflicts(room_groups)
    for (room_code, day_order, code_id), payload in sorted(
        room_code_conflicts.items(),
        key=lambda item: (item[0][0], item[0][1], item[0][2]),
    ):
        current_code = code_by_id.get(code_id)
        if current_code is None:
            continue
        peer_ids = payload["peer_ids"]
        slot_indices = payload["slot_indices"]
        if not peer_ids:
            continue

        counts["room_time_conflict"] += 1
        _add_issue(
            db=db,
            run_id=run_id,
            code_id=code_id,
            related_code_id=peer_ids[0],
            issue_type="CONFLICT",
            rule_code="ROOM_TIME_CONFLICT",
            message=(
                f"Room {room_code} has overlapping classes "
                f"(day={day_order}, slots={','.join(str(x) for x in slot_indices)})."
            ),
            conflict_key=_conflict_key("room", room_code, day_order, code_id),
            details={
                "room_code": room_code,
                "day_order": day_order,
                "slot_indices": slot_indices,
                "code_id": code_id,
                "peer_ids": peer_ids,
                "time_value": current_code.time_value,
            },
        )

    total_issues = (
        counts["trainer_time_conflict"] + counts["room_time_conflict"] + counts["capacity_exceeded"]
    )

    run.status = RunStatus.SUCCEEDED.value
    run.finished_at = datetime.now(timezone.utc)

    db.add(
        MCRunLog(
            run_id=run_id,
            level="INFO",
            code="CHECKS_FINISHED",
            message="Validation checks completed.",
            details_json=json.dumps(
                {
                    "total_issues": total_issues,
                    "trainer_time_conflict": counts["trainer_time_conflict"],
                    "room_time_conflict": counts["room_time_conflict"],
                    "capacity_exceeded": counts["capacity_exceeded"],
                },
                ensure_ascii=False,
            ),
        )
    )

    db.commit()

    return {
        "run_id": run_id,
        "status": run.status,
        "total_issues": total_issues,
        "trainer_time_conflict": counts["trainer_time_conflict"],
        "room_time_conflict": counts["room_time_conflict"],
        "capacity_exceeded": counts["capacity_exceeded"],
    }
