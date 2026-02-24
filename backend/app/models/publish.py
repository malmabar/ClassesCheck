from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, SmallInteger, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.db.base import Base


class MCPublishHallsCopy(Base):
    __tablename__ = "mc_publish_halls_copy"
    __table_args__ = (
        Index("ix_mc_publish_halls_copy_run_id", "run_id"),
        Index(
            "ix_mc_publish_halls_copy_run_room_day_slot",
            "run_id",
            "room_code",
            "day_order",
            "slot_index",
        ),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    semester: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    room_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    building_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    day_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    day_order: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    slot_index: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    occupancy_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crn_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crn_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class MCPublishCRNsCopy(Base):
    __tablename__ = "mc_publish_crns_copy"
    __table_args__ = (
        Index("ix_mc_publish_crns_copy_run_id", "run_id"),
        Index(
            "ix_mc_publish_crns_copy_run_crn_day_slot",
            "run_id",
            "crn",
            "day_order",
            "slot_index",
        ),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    semester: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    crn: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    course_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    course_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    room_code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trainer_job_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trainer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    day_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    day_order: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    slot_index: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    occupancy_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class MCPublishTrainersSC(Base):
    __tablename__ = "mc_publish_trainers_sc"
    __table_args__ = (
        Index("ix_mc_publish_trainers_sc_run_id", "run_id"),
        Index(
            "ix_mc_publish_trainers_sc_run_trainer_day_slot",
            "run_id",
            "trainer_job_id",
            "day_order",
            "slot_index",
        ),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    semester: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    trainer_job_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    trainer_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    day_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    day_order: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    slot_index: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    load_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crn_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crn_list: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


class MCPublishDistribution(Base):
    __tablename__ = "mc_publish_distribution"
    __table_args__ = (
        Index("ix_mc_publish_distribution_run_id", "run_id"),
        Index(
            "ix_mc_publish_distribution_run_day_slot",
            "run_id",
            "day_order",
            "slot_index",
        ),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    semester: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    period: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    day_name: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    day_order: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    slot_index: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    occupied_cells: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_cells: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    occupancy_ratio: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
