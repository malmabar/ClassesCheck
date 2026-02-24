from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.db.base import Base


class MCCode(Base):
    __tablename__ = "mc_codes"
    __table_args__ = (
        Index("ix_mc_codes_run_id", "run_id"),
        Index("ix_mc_codes_crn", "crn"),
        Index("ix_mc_codes_trainer_job_id", "trainer_job_id"),
        Index("ix_mc_codes_room_code", "room_code"),
        Index("ix_mc_codes_run_day_slot", "run_id", "day_order", "slot_index"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    source_row_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_source_ss01_rows.id", ondelete="SET NULL"),
        nullable=True,
    )
    semester: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    course_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    course_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    crn: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    section_type: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    day_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    day_order: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    time_value: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    time_hhmm: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    slot_index: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    building_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    room_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    room_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    registered_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    trainer_job_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trainer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_morning: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_evening: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

