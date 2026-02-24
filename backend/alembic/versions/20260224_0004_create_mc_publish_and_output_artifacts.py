"""create publish and output artifact tables

Revision ID: 20260224_0004
Revises: 20260222_0003
Create Date: 2026-02-24 03:20:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260224_0004"
down_revision: Union[str, None] = "20260222_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CORE_SCHEMA = "mc_core"


def upgrade() -> None:
    op.create_table(
        "mc_run_output_artifact",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("artifact_type", sa.String(length=32), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("content_type", sa.String(length=120), nullable=True),
        sa.Column("file_size", sa.Integer(), nullable=True),
        sa.Column("checksum", sa.String(length=64), nullable=True),
        sa.Column("storage_path", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_run_output_artifact"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_run_output_artifact_run_id",
        "mc_run_output_artifact",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_publish_halls_copy",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=True),
        sa.Column("period", sa.String(length=16), nullable=True),
        sa.Column("room_code", sa.String(length=64), nullable=True),
        sa.Column("building_code", sa.String(length=64), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("day_order", sa.SmallInteger(), nullable=True),
        sa.Column("slot_index", sa.SmallInteger(), nullable=True),
        sa.Column("occupancy_count", sa.Integer(), nullable=False),
        sa.Column("crn_count", sa.Integer(), nullable=False),
        sa.Column("crn_list", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_publish_halls_copy"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_halls_copy_run_id",
        "mc_publish_halls_copy",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_halls_copy_run_room_day_slot",
        "mc_publish_halls_copy",
        ["run_id", "room_code", "day_order", "slot_index"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_publish_crns_copy",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=True),
        sa.Column("period", sa.String(length=16), nullable=True),
        sa.Column("crn", sa.String(length=32), nullable=True),
        sa.Column("course_code", sa.String(length=64), nullable=True),
        sa.Column("course_name", sa.String(length=255), nullable=True),
        sa.Column("room_code", sa.String(length=64), nullable=True),
        sa.Column("trainer_job_id", sa.String(length=64), nullable=True),
        sa.Column("trainer_name", sa.String(length=255), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("day_order", sa.SmallInteger(), nullable=True),
        sa.Column("slot_index", sa.SmallInteger(), nullable=True),
        sa.Column("occupancy_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_publish_crns_copy"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_crns_copy_run_id",
        "mc_publish_crns_copy",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_crns_copy_run_crn_day_slot",
        "mc_publish_crns_copy",
        ["run_id", "crn", "day_order", "slot_index"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_publish_trainers_sc",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=True),
        sa.Column("period", sa.String(length=16), nullable=True),
        sa.Column("trainer_job_id", sa.String(length=64), nullable=True),
        sa.Column("trainer_name", sa.String(length=255), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("day_order", sa.SmallInteger(), nullable=True),
        sa.Column("slot_index", sa.SmallInteger(), nullable=True),
        sa.Column("load_count", sa.Integer(), nullable=False),
        sa.Column("crn_count", sa.Integer(), nullable=False),
        sa.Column("crn_list", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_publish_trainers_sc"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_trainers_sc_run_id",
        "mc_publish_trainers_sc",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_trainers_sc_run_trainer_day_slot",
        "mc_publish_trainers_sc",
        ["run_id", "trainer_job_id", "day_order", "slot_index"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_publish_distribution",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=True),
        sa.Column("period", sa.String(length=16), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("day_order", sa.SmallInteger(), nullable=True),
        sa.Column("slot_index", sa.SmallInteger(), nullable=True),
        sa.Column("occupied_cells", sa.Integer(), nullable=False),
        sa.Column("total_cells", sa.Integer(), nullable=False),
        sa.Column("occupancy_ratio", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_publish_distribution"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_distribution_run_id",
        "mc_publish_distribution",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_publish_distribution_run_day_slot",
        "mc_publish_distribution",
        ["run_id", "day_order", "slot_index"],
        unique=False,
        schema=CORE_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_mc_publish_distribution_run_day_slot",
        table_name="mc_publish_distribution",
        schema=CORE_SCHEMA,
    )
    op.drop_index(
        "ix_mc_publish_distribution_run_id",
        table_name="mc_publish_distribution",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_publish_distribution", schema=CORE_SCHEMA)

    op.drop_index(
        "ix_mc_publish_trainers_sc_run_trainer_day_slot",
        table_name="mc_publish_trainers_sc",
        schema=CORE_SCHEMA,
    )
    op.drop_index(
        "ix_mc_publish_trainers_sc_run_id",
        table_name="mc_publish_trainers_sc",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_publish_trainers_sc", schema=CORE_SCHEMA)

    op.drop_index(
        "ix_mc_publish_crns_copy_run_crn_day_slot",
        table_name="mc_publish_crns_copy",
        schema=CORE_SCHEMA,
    )
    op.drop_index(
        "ix_mc_publish_crns_copy_run_id",
        table_name="mc_publish_crns_copy",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_publish_crns_copy", schema=CORE_SCHEMA)

    op.drop_index(
        "ix_mc_publish_halls_copy_run_room_day_slot",
        table_name="mc_publish_halls_copy",
        schema=CORE_SCHEMA,
    )
    op.drop_index(
        "ix_mc_publish_halls_copy_run_id",
        table_name="mc_publish_halls_copy",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_publish_halls_copy", schema=CORE_SCHEMA)

    op.drop_index(
        "ix_mc_run_output_artifact_run_id",
        table_name="mc_run_output_artifact",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_run_output_artifact", schema=CORE_SCHEMA)
