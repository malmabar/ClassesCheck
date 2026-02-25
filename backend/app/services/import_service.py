from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.run import MCRun, MCRunInputArtifact, MCRunLog, RunStatus
from app.models.source import MCImportReject, MCSourceSS01Row
from app.services.run_lifecycle import build_run_idempotency_key, find_latest_idempotent_run


REQUIRED_SS01_COLUMNS = [
    "الفصل التدريبي",
    "القسم",
    "المقرر",
    "اسم المقرر",
    "الرقم المرجعي",
    "نوع الشعبة",
    "اليوم",
    "الوقت",
    "مبنى",
    "قاعة",
    "سعة",
    "مسجلين",
    "رقم المدرب",
    "اسم المدرب",
]

VALID_PERIODS = {"صباحي", "مسائي"}


def _to_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    cleaned = str(value).strip()
    if cleaned == "":
        return None
    try:
        return int(float(cleaned))
    except ValueError:
        return None


def _decode_csv(file_bytes: bytes) -> tuple[str, str]:
    for encoding in ("utf-8-sig", "utf-8", "cp1256"):
        try:
            return file_bytes.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    raise ValueError("Unable to decode CSV. Supported encodings: UTF-8, Windows-1256.")


def _detect_delimiter(text: str) -> str:
    sample = "\n".join(text.splitlines()[:20])
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        return dialect.delimiter
    except csv.Error:
        return ","


def import_ss01_csv(
    db: Session,
    file_bytes: bytes,
    file_name: str,
    semester: str,
    period: str,
    created_by: str = "api-user",
) -> dict:
    if period not in VALID_PERIODS:
        raise ValueError("period must be one of: صباحي, مسائي")
    if not semester.strip():
        raise ValueError("semester is required.")

    checksum = hashlib.sha256(file_bytes).hexdigest()
    decoded_text, encoding = _decode_csv(file_bytes)
    delimiter = _detect_delimiter(decoded_text)
    normalized_semester = semester.strip()
    idempotency_key = build_run_idempotency_key(
        input_checksum=checksum,
        reference_version="beta6",
        semester=normalized_semester,
        period=period,
        rule_version="v1.1",
        settings_payload={"source": "SS01"},
    )

    existing_run = find_latest_idempotent_run(db=db, idempotency_key=idempotency_key)
    if existing_run is not None:
        inserted_rows = db.scalar(
            select(func.count()).select_from(MCSourceSS01Row).where(MCSourceSS01Row.run_id == existing_run.id)
        ) or 0
        rejected_rows = db.scalar(
            select(func.count()).select_from(MCImportReject).where(MCImportReject.run_id == existing_run.id)
        ) or 0
        db.add(
            MCRunLog(
                run_id=existing_run.id,
                level="INFO",
                code="IMPORT_IDEMPOTENT_HIT",
                message="Skipped duplicate SS01 import due to idempotency key match.",
                details_json=json.dumps(
                    {"idempotency_key": idempotency_key, "triggered_by": created_by},
                    ensure_ascii=False,
                ),
            )
        )
        db.commit()
        return {
            "run_id": existing_run.id,
            "status": existing_run.status,
            "inserted_rows": inserted_rows,
            "rejected_rows": rejected_rows,
            "checksum": checksum,
            "encoding": encoding,
            "delimiter": delimiter,
            "idempotency_key": idempotency_key,
            "idempotent_hit": True,
        }

    reader = csv.DictReader(io.StringIO(decoded_text), delimiter=delimiter)
    if not reader.fieldnames:
        raise ValueError("CSV header row is missing.")

    normalized_fieldnames = [f.strip() if isinstance(f, str) else "" for f in reader.fieldnames]
    missing_columns = [c for c in REQUIRED_SS01_COLUMNS if c not in normalized_fieldnames]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    run = MCRun(
        semester=normalized_semester,
        period=period,
        status=RunStatus.CREATED.value,
        idempotency_key=idempotency_key,
        input_checksum=checksum,
        reference_version="beta6",
        rule_version="v1.1",
        started_at=datetime.now(timezone.utc),
        created_by=created_by,
    )
    db.add(run)
    db.flush()

    db.add(
        MCRunInputArtifact(
            run_id=run.id,
            artifact_type="ss01_csv",
            file_name=file_name,
            content_type="text/csv",
            file_size=len(file_bytes),
            checksum=checksum,
        )
    )
    db.add(
        MCRunLog(
            run_id=run.id,
            level="INFO",
            code="IMPORT_START",
            message="Started SS01 import.",
            details_json=json.dumps(
                {"encoding": encoding, "delimiter": delimiter}, ensure_ascii=False
            ),
        )
    )
    run.status = RunStatus.VALIDATING.value
    run.status = RunStatus.RUNNING.value

    inserted_rows = 0
    rejected_rows = 0

    for row_index, row in enumerate(reader, start=2):
        normalized = {
            (k.strip() if isinstance(k, str) else ""): (v or "").strip()
            for k, v in row.items()
        }
        missing_critical = [col for col in REQUIRED_SS01_COLUMNS if not normalized.get(col)]
        if missing_critical:
            rejected_rows += 1
            db.add(
                MCImportReject(
                    run_id=run.id,
                    row_number=row_index,
                    reason_code="MISSING_REQUIRED_FIELDS",
                    reason_message=f"Missing values in required fields: {', '.join(missing_critical)}",
                    raw_row_json=json.dumps(normalized, ensure_ascii=False),
                )
            )
            continue

        db.add(
            MCSourceSS01Row(
                run_id=run.id,
                row_number=row_index,
                training_term=normalized.get("الفصل التدريبي"),
                training_unit=normalized.get("الوحدة التدريبية"),
                term_part=normalized.get("جزء الفصل"),
                department=normalized.get("القسم"),
                course_code=normalized.get("المقرر"),
                course_name=normalized.get("اسم المقرر"),
                credit_hours=_to_int(normalized.get("الساعات المعتمدة")),
                accounting_hours=_to_int(normalized.get("ساعات المحاسبة")),
                lecture_hours=_to_int(normalized.get("ساعات المحاضرة")),
                lab_hours=_to_int(normalized.get("ساعات المختبر")),
                other_hours=_to_int(normalized.get("ساعات أخرى")),
                contact_hours=_to_int(normalized.get("ساعات الاتصال")),
                crn=normalized.get("الرقم المرجعي"),
                section_type=normalized.get("نوع الشعبة"),
                ivr_and_self_service=normalized.get("كل من الاستجابة الصوتية والخدمة الذاتية متاح"),
                day_name=normalized.get("اليوم"),
                time_value=normalized.get("الوقت"),
                schedule_type=normalized.get("نوع الجدولة"),
                building_code=normalized.get("مبنى"),
                room_code=normalized.get("قاعة"),
                room_capacity=_to_int(normalized.get("سعة")),
                max_reserved_seats=_to_int(normalized.get("الحد الأقصى للمقاعد المحجوزة")),
                reserved_already=_to_int(normalized.get("المحجوزة بالفعل")),
                reserved_remaining=_to_int(normalized.get("المحجوزة المتبقية")),
                waitlist_max=_to_int(normalized.get("الحد الأقصى للائحة الانتظار")),
                waitlist_registered=_to_int(normalized.get("المسجلون على لائحة الانتظار")),
                waitlist_remaining=_to_int(normalized.get("المتبقي على لائحة الانتظار")),
                registered_count=_to_int(normalized.get("مسجلين")),
                available_count=_to_int(normalized.get("متبقي")),
                trainer_job_id=normalized.get("رقم المدرب"),
                trainer_name=normalized.get("اسم المدرب"),
            )
        )
        inserted_rows += 1

    if inserted_rows == 0:
        run.status = RunStatus.FAILED.value
        db.add(
            MCRunLog(
                run_id=run.id,
                level="ERROR",
                code="IMPORT_EMPTY",
                message="No valid SS01 rows were imported.",
            )
        )
    else:
        run.status = RunStatus.SUCCEEDED.value
        db.add(
            MCRunLog(
                run_id=run.id,
                level="INFO",
                code="IMPORT_FINISHED",
                message="SS01 import completed successfully.",
                details_json=json.dumps(
                    {"inserted_rows": inserted_rows, "rejected_rows": rejected_rows},
                    ensure_ascii=False,
                ),
            )
        )
    run.finished_at = datetime.now(timezone.utc)

    db.commit()

    return {
        "run_id": run.id,
        "status": run.status,
        "inserted_rows": inserted_rows,
        "rejected_rows": rejected_rows,
        "checksum": checksum,
        "encoding": encoding,
        "delimiter": delimiter,
        "idempotency_key": idempotency_key,
        "idempotent_hit": False,
    }
