from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings
from app.db.base import Base


class MCIssue(Base):
    __tablename__ = "mc_issues"
    __table_args__ = (
        Index("ix_mc_issues_run_id", "run_id"),
        Index("ix_mc_issues_rule_code", "rule_code"),
        Index("ix_mc_issues_severity", "severity"),
        Index("ix_mc_issues_run_rule_code", "run_id", "rule_code"),
        {"schema": settings.mc_db_schema},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_run.id", ondelete="CASCADE"),
        nullable=False,
    )
    code_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_codes.id", ondelete="SET NULL"),
        nullable=True,
    )
    related_code_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey(f"{settings.mc_db_schema}.mc_codes.id", ondelete="SET NULL"),
        nullable=True,
    )
    issue_type: Mapped[str] = mapped_column(String(32), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False, default="ERROR")
    rule_code: Mapped[str] = mapped_column(String(64), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    conflict_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    details_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
