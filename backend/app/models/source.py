from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.db.base import Base


class MCSourceSS01Row(Base):
    __tablename__ = "mc_source_ss01_rows"
    __table_args__ = (
        Index("ix_mc_source_ss01_rows_run_id", "run_id"),
        Index("ix_mc_source_ss01_rows_crn", "crn"),
        Index("ix_mc_source_ss01_rows_trainer_job_id", "trainer_job_id"),
        Index("ix_mc_source_ss01_rows_room_code", "room_code"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)

    training_term: Mapped[Optional[str]] = mapped_column(String(128))
    training_unit: Mapped[Optional[str]] = mapped_column(String(128))
    term_part: Mapped[Optional[str]] = mapped_column(String(128))
    department: Mapped[Optional[str]] = mapped_column(String(128))
    course_code: Mapped[Optional[str]] = mapped_column(String(64))
    course_name: Mapped[Optional[str]] = mapped_column(String(255))
    credit_hours: Mapped[Optional[int]] = mapped_column(Integer)
    accounting_hours: Mapped[Optional[int]] = mapped_column(Integer)
    lecture_hours: Mapped[Optional[int]] = mapped_column(Integer)
    lab_hours: Mapped[Optional[int]] = mapped_column(Integer)
    other_hours: Mapped[Optional[int]] = mapped_column(Integer)
    contact_hours: Mapped[Optional[int]] = mapped_column(Integer)
    crn: Mapped[Optional[str]] = mapped_column(String(32))
    section_type: Mapped[Optional[str]] = mapped_column(String(128))
    ivr_and_self_service: Mapped[Optional[str]] = mapped_column(String(64))
    day_name: Mapped[Optional[str]] = mapped_column(String(32))
    time_value: Mapped[Optional[str]] = mapped_column(String(32))
    schedule_type: Mapped[Optional[str]] = mapped_column(String(64))
    building_code: Mapped[Optional[str]] = mapped_column(String(64))
    room_code: Mapped[Optional[str]] = mapped_column(String(64))
    room_capacity: Mapped[Optional[int]] = mapped_column(Integer)
    max_reserved_seats: Mapped[Optional[int]] = mapped_column(Integer)
    reserved_already: Mapped[Optional[int]] = mapped_column(Integer)
    reserved_remaining: Mapped[Optional[int]] = mapped_column(Integer)
    waitlist_max: Mapped[Optional[int]] = mapped_column(Integer)
    waitlist_registered: Mapped[Optional[int]] = mapped_column(Integer)
    waitlist_remaining: Mapped[Optional[int]] = mapped_column(Integer)
    registered_count: Mapped[Optional[int]] = mapped_column(Integer)
    available_count: Mapped[Optional[int]] = mapped_column(Integer)
    trainer_job_id: Mapped[Optional[str]] = mapped_column(String(64))
    trainer_name: Mapped[Optional[str]] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class MCImportReject(Base):
    __tablename__ = "mc_import_rejects"
    __table_args__ = (
        Index("ix_mc_import_rejects_run_id", "run_id"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    row_number: Mapped[int] = mapped_column(Integer, nullable=False)
    reason_code: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_message: Mapped[str] = mapped_column(Text, nullable=False)
    raw_row_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
