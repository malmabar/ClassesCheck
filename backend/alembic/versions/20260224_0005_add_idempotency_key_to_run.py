"""add idempotency key to mc_run

Revision ID: 20260224_0005
Revises: 20260224_0004
Create Date: 2026-02-24 06:30:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import NoSuchTableError


# revision identifiers, used by Alembic.
revision: str = "20260224_0005"
down_revision: Union[str, None] = "20260224_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CORE_SCHEMA = "mc_core"
RUN_TABLE = "mc_run"
RUN_IDEMPOTENCY_INDEX = "ix_mc_run_idempotency_key"


def _table_exists(bind, table_name: str) -> bool:
    return sa.inspect(bind).has_table(table_name, schema=CORE_SCHEMA)


def _column_exists(bind, table_name: str, column_name: str) -> bool:
    if not _table_exists(bind, table_name):
        return False
    columns = sa.inspect(bind).get_columns(table_name, schema=CORE_SCHEMA)
    return any(column.get("name") == column_name for column in columns)


def _index_exists(bind, table_name: str, index_name: str) -> bool:
    try:
        indexes = sa.inspect(bind).get_indexes(table_name, schema=CORE_SCHEMA)
    except NoSuchTableError:
        return False
    return any(index.get("name") == index_name for index in indexes)


def upgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, RUN_TABLE):
        return

    if not _column_exists(bind, RUN_TABLE, "idempotency_key"):
        op.add_column(
            RUN_TABLE,
            sa.Column("idempotency_key", sa.String(length=64), nullable=True),
            schema=CORE_SCHEMA,
        )

    if not _index_exists(bind, RUN_TABLE, RUN_IDEMPOTENCY_INDEX):
        op.create_index(
            RUN_IDEMPOTENCY_INDEX,
            RUN_TABLE,
            ["idempotency_key"],
            unique=False,
            schema=CORE_SCHEMA,
        )


def downgrade() -> None:
    bind = op.get_bind()
    if not _table_exists(bind, RUN_TABLE):
        return

    if _index_exists(bind, RUN_TABLE, RUN_IDEMPOTENCY_INDEX):
        op.drop_index(RUN_IDEMPOTENCY_INDEX, table_name=RUN_TABLE, schema=CORE_SCHEMA)

    if _column_exists(bind, RUN_TABLE, "idempotency_key"):
        op.drop_column(RUN_TABLE, "idempotency_key", schema=CORE_SCHEMA)
