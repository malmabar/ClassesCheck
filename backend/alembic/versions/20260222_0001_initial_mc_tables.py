"""initial mc tables

Revision ID: 20260222_0001
Revises:
Create Date: 2026-02-22 01:55:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260222_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CORE_SCHEMA = "mc_core"
META_SCHEMA = "mc_meta"


def upgrade() -> None:
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {CORE_SCHEMA}")
    op.execute(f"CREATE SCHEMA IF NOT EXISTS {META_SCHEMA}")

    op.create_table(
        "mc_run",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=False),
        sa.Column("period", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("rule_version", sa.String(length=32), nullable=False),
        sa.Column("input_checksum", sa.String(length=64), nullable=True),
        sa.Column("reference_version", sa.String(length=64), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_mc_run"),
        schema=CORE_SCHEMA,
    )
    op.create_index("ix_mc_run_status", "mc_run", ["status"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_run_created_at", "mc_run", ["created_at"], unique=False, schema=CORE_SCHEMA)

    op.create_table(
        "mc_run_log",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("level", sa.String(length=16), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("details_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_run_log"),
        schema=CORE_SCHEMA,
    )
    op.create_index("ix_mc_run_log_run_id", "mc_run_log", ["run_id"], unique=False, schema=CORE_SCHEMA)

    op.create_table(
        "mc_run_input_artifact",
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
        sa.PrimaryKeyConstraint("id", name="pk_mc_run_input_artifact"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_run_input_artifact_run_id",
        "mc_run_input_artifact",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_run_lock",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("semester", sa.String(length=64), nullable=False),
        sa.Column("period", sa.String(length=16), nullable=False),
        sa.Column("lock_token", sa.String(length=64), nullable=False),
        sa.Column("locked_by", sa.String(length=64), nullable=True),
        sa.Column("locked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_mc_run_lock"),
        sa.UniqueConstraint("semester", "period", name="uq_mc_run_lock_semester_period"),
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_source_ss01_rows",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("training_term", sa.String(length=128), nullable=True),
        sa.Column("training_unit", sa.String(length=128), nullable=True),
        sa.Column("term_part", sa.String(length=128), nullable=True),
        sa.Column("department", sa.String(length=128), nullable=True),
        sa.Column("course_code", sa.String(length=64), nullable=True),
        sa.Column("course_name", sa.String(length=255), nullable=True),
        sa.Column("credit_hours", sa.Integer(), nullable=True),
        sa.Column("accounting_hours", sa.Integer(), nullable=True),
        sa.Column("lecture_hours", sa.Integer(), nullable=True),
        sa.Column("lab_hours", sa.Integer(), nullable=True),
        sa.Column("other_hours", sa.Integer(), nullable=True),
        sa.Column("contact_hours", sa.Integer(), nullable=True),
        sa.Column("crn", sa.String(length=32), nullable=True),
        sa.Column("section_type", sa.String(length=128), nullable=True),
        sa.Column("ivr_and_self_service", sa.String(length=64), nullable=True),
        sa.Column("day_name", sa.String(length=32), nullable=True),
        sa.Column("time_value", sa.String(length=32), nullable=True),
        sa.Column("schedule_type", sa.String(length=64), nullable=True),
        sa.Column("building_code", sa.String(length=64), nullable=True),
        sa.Column("room_code", sa.String(length=64), nullable=True),
        sa.Column("room_capacity", sa.Integer(), nullable=True),
        sa.Column("max_reserved_seats", sa.Integer(), nullable=True),
        sa.Column("reserved_already", sa.Integer(), nullable=True),
        sa.Column("reserved_remaining", sa.Integer(), nullable=True),
        sa.Column("waitlist_max", sa.Integer(), nullable=True),
        sa.Column("waitlist_registered", sa.Integer(), nullable=True),
        sa.Column("waitlist_remaining", sa.Integer(), nullable=True),
        sa.Column("registered_count", sa.Integer(), nullable=True),
        sa.Column("available_count", sa.Integer(), nullable=True),
        sa.Column("trainer_job_id", sa.String(length=64), nullable=True),
        sa.Column("trainer_name", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_source_ss01_rows"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_source_ss01_rows_run_id",
        "mc_source_ss01_rows",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_source_ss01_rows_crn",
        "mc_source_ss01_rows",
        ["crn"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_source_ss01_rows_trainer_job_id",
        "mc_source_ss01_rows",
        ["trainer_job_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_source_ss01_rows_room_code",
        "mc_source_ss01_rows",
        ["room_code"],
        unique=False,
        schema=CORE_SCHEMA,
    )

    op.create_table(
        "mc_import_rejects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("reason_code", sa.String(length=64), nullable=False),
        sa.Column("reason_message", sa.Text(), nullable=False),
        sa.Column("raw_row_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_import_rejects"),
        schema=CORE_SCHEMA,
    )
    op.create_index(
        "ix_mc_import_rejects_run_id",
        "mc_import_rejects",
        ["run_id"],
        unique=False,
        schema=CORE_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index("ix_mc_import_rejects_run_id", table_name="mc_import_rejects", schema=CORE_SCHEMA)
    op.drop_table("mc_import_rejects", schema=CORE_SCHEMA)

    op.drop_index("ix_mc_source_ss01_rows_room_code", table_name="mc_source_ss01_rows", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_source_ss01_rows_trainer_job_id", table_name="mc_source_ss01_rows", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_source_ss01_rows_crn", table_name="mc_source_ss01_rows", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_source_ss01_rows_run_id", table_name="mc_source_ss01_rows", schema=CORE_SCHEMA)
    op.drop_table("mc_source_ss01_rows", schema=CORE_SCHEMA)

    op.drop_table("mc_run_lock", schema=CORE_SCHEMA)

    op.drop_index(
        "ix_mc_run_input_artifact_run_id",
        table_name="mc_run_input_artifact",
        schema=CORE_SCHEMA,
    )
    op.drop_table("mc_run_input_artifact", schema=CORE_SCHEMA)

    op.drop_index("ix_mc_run_log_run_id", table_name="mc_run_log", schema=CORE_SCHEMA)
    op.drop_table("mc_run_log", schema=CORE_SCHEMA)

    op.drop_index("ix_mc_run_created_at", table_name="mc_run", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_run_status", table_name="mc_run", schema=CORE_SCHEMA)
    op.drop_table("mc_run", schema=CORE_SCHEMA)

