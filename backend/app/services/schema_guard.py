from __future__ import annotations

from typing import Sequence

from sqlalchemy import inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base
from app.models.publish import (
    MCPublishCRNsCopy,
    MCPublishDistribution,
    MCPublishHallsCopy,
    MCPublishTrainersSC,
)
from app.models.run import MCRunOutputArtifact


_PUBLISH_TABLES: Sequence = (
    MCRunOutputArtifact.__table__,
    MCPublishHallsCopy.__table__,
    MCPublishCRNsCopy.__table__,
    MCPublishTrainersSC.__table__,
    MCPublishDistribution.__table__,
)


def ensure_publish_schema(db: Session) -> None:
    bind = db.get_bind()
    if bind is None:
        return
    engine: Engine = bind.engine if hasattr(bind, "engine") else bind
    inspector = inspect(engine)
    existing = set(inspector.get_table_names(schema=settings.mc_db_schema))
    missing = [table for table in _PUBLISH_TABLES if table.name not in existing]
    if missing:
        Base.metadata.create_all(bind=engine, tables=missing, checkfirst=True)
