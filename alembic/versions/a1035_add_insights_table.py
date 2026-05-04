"""add_insights_table_issue_1035

Issue #1035 Phase 2: persist InsightJournal (composted learnings) to durable
storage.

Pre-#1035, `services/mux/composting_pipeline.py` stored SurfaceableInsight
entries in an in-memory Dict (`InsightJournal._insights`), lost on every
restart. Composting cycles produced insights that vanished as soon as the
process exited. This migration adds the `insights` table that backs the
new `InsightDB` model + `InsightRepository`.

Sibling pattern to `ethics_audit_log` (#1018, May 2): same persistence shape
applied to insights instead of audit entries; user-scoped queries; soft
delete deferred to #1031.

Revision ID: a1035insights
Revises: a1018ethicsaudit
Create Date: 2026-05-03 11:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1035insights"
down_revision: Union[str, Sequence[str], None] = "a1018ethicsaudit"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create insights table + indexes for Issue #1035."""

    op.create_table(
        "insights",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("object_id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=False),
        sa.Column(
            "learning",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column("surfaced_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("last_surfaced", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_response", sa.String(length=50), nullable=True),
        sa.Column(
            "min_trust_stage", sa.Integer(), nullable=False, server_default=sa.text("1")
        ),
        sa.Column(
            "connected_insights",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "context_tags",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=True,
            server_default=sa.func.now(),
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Per-column indexes (matches Column(..., index=True) declarations).
    op.create_index("ix_insights_object_id", "insights", ["object_id"])
    op.create_index("ix_insights_user_id", "insights", ["user_id"])

    # Composite indexes matching InsightJournal query patterns:
    #   - get_for_context(user_id, ...) ordered by recency → user_id + created_at
    #   - get_unsurfaced(user_id, ...) → user_id + surfaced_count
    op.create_index(
        "idx_insights_user_created", "insights", ["user_id", "created_at"]
    )
    op.create_index(
        "idx_insights_user_surfaced", "insights", ["user_id", "surfaced_count"]
    )


def downgrade() -> None:
    """Drop insights table + indexes."""

    op.drop_index("idx_insights_user_surfaced", table_name="insights")
    op.drop_index("idx_insights_user_created", table_name="insights")
    op.drop_index("ix_insights_user_id", table_name="insights")
    op.drop_index("ix_insights_object_id", table_name="insights")

    op.drop_table("insights")
