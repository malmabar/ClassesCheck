"""create mc_issues table

Revision ID: 20260222_0003
Revises: 20260222_0002
Create Date: 2026-02-22 05:10:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260222_0003"
down_revision: Union[str, None] = "20260222_0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

CORE_SCHEMA = "mc_core"


def upgrade() -> None:
    op.create_table(
        "mc_issues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("run_id", sa.String(length=36), nullable=False),
        sa.Column("code_id", sa.Integer(), nullable=True),
        sa.Column("related_code_id", sa.Integer(), nullable=True),
        sa.Column("issue_type", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False, server_default=sa.text("'ERROR'")),
        sa.Column("rule_code", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("conflict_key", sa.String(length=255), nullable=True),
        sa.Column("details_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["run_id"], [f"{CORE_SCHEMA}.mc_run.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["code_id"], [f"{CORE_SCHEMA}.mc_codes.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["related_code_id"], [f"{CORE_SCHEMA}.mc_codes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name="pk_mc_issues"),
        schema=CORE_SCHEMA,
    )

    op.create_index("ix_mc_issues_run_id", "mc_issues", ["run_id"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_issues_rule_code", "mc_issues", ["rule_code"], unique=False, schema=CORE_SCHEMA)
    op.create_index("ix_mc_issues_severity", "mc_issues", ["severity"], unique=False, schema=CORE_SCHEMA)
    op.create_index(
        "ix_mc_issues_run_rule_code",
        "mc_issues",
        ["run_id", "rule_code"],
        unique=False,
        schema=CORE_SCHEMA,
    )


def downgrade() -> None:
    op.drop_index("ix_mc_issues_run_rule_code", table_name="mc_issues", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_issues_severity", table_name="mc_issues", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_issues_rule_code", table_name="mc_issues", schema=CORE_SCHEMA)
    op.drop_index("ix_mc_issues_run_id", table_name="mc_issues", schema=CORE_SCHEMA)
    op.drop_table("mc_issues", schema=CORE_SCHEMA)
