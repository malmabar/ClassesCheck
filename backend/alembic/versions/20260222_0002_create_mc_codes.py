"""create mc_codes table

Revision ID: 20260222_0002
Revises: 20260222_0001
Create Date: 2026-02-22 04:30:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260222_0002"
down_revision: Union[str, None] = "20260222_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CORE_SCHEMA = "mc_core"


def upgrade() -> None:
    op.create_table(
        "mc_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("source_row_id", sa.Integer(), nullable=True),
        sa.Column("semester", sa.String(length=64), nullable=True),
        sa.Column("period", sa.String(length=16), nullable=True),
        sa.Column("department", sa.String(length=128), nullable=True),
        sa.Column("course_code", sa.String(length=64), nullable=True),
        sa.Column("course_name", sa.String(length=255), nullable=True),
        sa.Column("crn", sa.String(length=32), nullable=True),
        sa.Column("section_type", sa.String(length=128), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("day_order", sa.SmallInteger(), nullable=True),
        sa.Column("time_value", sa.String(length=32), nullable=True),
        sa.Column("time_hhmm", sa.Integer(), nullable=True),
        sa.Column("slot_index", sa.SmallInteger(), nullable=True),
        sa.Column("building_code", sa.String(length=64), nullable=True),
        sa.Column("room_code", sa.String(length=64), nullable=True),
        sa.Column("room_capacity", sa.Integer(), nullable=True),
        sa.Column("registered_count", sa.Integer(), nullable=True),
        sa.Column("trainer_job_id", sa.String(length=64), nullable=True),
        sa.Column("trainer_name", sa.String(length=255), nullable=True),
        sa.Column("is_morning", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_evening", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["source_row_id"], [f"{CORE_SCHEMA}.mc_source_ss01_rows.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_codes"),
        schema=CORE_SCHEMA,
    )

    op.create_index("ix_mc_codes_run_id", "mc_codes", ["run_id"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_codes_crn", "mc_codes", ["crn"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_codes_trainer_job_id", "mc_codes", ["trainer_job_id"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_codes_room_code", "mc_codes", ["room_code"], unique=False, schema=CORE_SCHEMA)
    op.create_index(
        "ix_mc_codes_run_day_slot",
        "mc_codes",
        ["run_id", "day_order", "slot_index"],
        unique=False,
        schema=CORE_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index("ix_mc_codes_run_day_slot", table_name="mc_codes", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_codes_room_code", table_name="mc_codes", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_codes_trainer_job_id", table_name="mc_codes", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_codes_crn", table_name="mc_codes", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_codes_run_id", table_name="mc_codes", schema=CORE_SCHEMA)
    op.drop_table("mc_codes", schema=CORE_SCHEMA)

