from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.db.base import Base


class RunStatus(str, enum.Enum):
    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    PUBLISHED = "PUBLISHED"


class MCRun(Base):
    __tablename__ = "mc_run"
    __table_args__ = (
        Index("ix_mc_run_status", "status"),
        Index("ix_mc_run_created_at", "created_at"),
        Index("ix_mc_run_idempotency_key", "idempotency_key"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )
    semester: Mapped[str] = mapped_column(String(64), nullable=False)
    period: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(32), nullable=False, default="v1.1")
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    input_checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    reference_version: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_by: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    logs: Mapped[list[MCRunLog]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )
    input_artifacts: Mapped[list[MCRunInputArtifact]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )
    output_artifacts: Mapped[list[MCRunOutputArtifact]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )


class MCRunLog(Base):
    __tablename__ = "mc_run_log"
    __table_args__ = (
        Index("ix_mc_run_log_run_id", "run_id"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    level: Mapped[str] = mapped_column(String(16), nullable=False, default="INFO")
    code: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    details_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    run: Mapped[MCRun] = relationship(back_populates="logs")


class MCRunInputArtifact(Base):
    __tablename__ = "mc_run_input_artifact"
    __table_args__ = (
        Index("ix_mc_run_input_artifact_run_id", "run_id"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    artifact_type: Mapped[str] = mapped_column(String(32), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    storage_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    run: Mapped[MCRun] = relationship(back_populates="input_artifacts")


class MCRunOutputArtifact(Base):
    __tablename__ = "mc_run_output_artifact"
    __table_args__ = (
        Index("ix_mc_run_output_artifact_run_id", "run_id"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    artifact_type: Mapped[str] = mapped_column(String(32), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    file_size: Mapped[Optional[int]] = mapped_column(nullable=True)
    checksum: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    storage_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    run: Mapped[MCRun] = relationship(back_populates="output_artifacts")


class MCRunLock(Base):
    __tablename__ = "mc_run_lock"
    __table_args__ = (
        UniqueConstraint("semester", "period", name="uq_mc_run_lock_semester_period"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    semester: Mapped[str] = mapped_column(String(64), nullable=False)
    period: Mapped[str] = mapped_column(String(16), nullable=False)
    lock_token: Mapped[str] = mapped_column(String(64), nullable=False)
    locked_by: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    locked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
