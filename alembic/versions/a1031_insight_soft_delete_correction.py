"""add_insight_is_deleted_and_user_correction_columns_issue_1031

Issue #1031 Phase 1: support per-user soft-delete + free-text correction
on insights.

Per #1031 PM audit dispositions May 3:
- Q1 soft delete: insights store `is_deleted` flag (default False); list
  queries default `exclude_deleted=True`. Reset-all flips the flag for
  the user's insights rather than DELETE.
- Q2 free-text correction: when user clicks "Correct" on the Insight
  Journal page, their correction text is stored as `user_correction`
  alongside the insight (no schema for structured taxonomy).

Revision ID: a1031softdelete
Revises: a1035insights
Create Date: 2026-05-03 15:35:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


revision: str = "a1031softdelete"
down_revision: Union[str, Sequence[str], None] = "a1035insights"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add is_deleted + user_correction columns to insights table."""
    op.add_column(
        "insights",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "insights",
        sa.Column("user_correction", sa.Text(), nullable=True),
    )

    # Index for the common query: exclude_deleted scoped to a user.
    op.create_index(
        "idx_insights_user_not_deleted",
        "insights",
        ["user_id", "is_deleted"],
    )


def downgrade() -> None:
    """Drop is_deleted + user_correction columns."""
    op.drop_index("idx_insights_user_not_deleted", table_name="insights")
    op.drop_column("insights", "user_correction")
    op.drop_column("insights", "is_deleted")
