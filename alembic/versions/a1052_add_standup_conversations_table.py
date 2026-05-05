"""add_standup_conversations_table_issue_1052

Issue #1052 (PRE-900): persist StandupConversation to PostgreSQL.

Pre-#1052, `services/conversation/conversation_handler.py:42-43` stored
StandupConversation entries in module-level singleton dicts (lost on every
restart). Standup sessions in flight when the server restarted disappeared;
partial captures were unrecoverable. This migration adds the
`standup_conversations` table that backs the new `StandupConversationDB`
model + `StandupConversationRepository`.

Sibling pattern to `ethics_audit_log` (#1018, May 2) and `insights`
(#1035, May 3): same in-memory → DB conversion shape; user-scoped queries;
JSONB fields in production / JSON variant in unit tests.

Required for #900 Phase 4 (partial-content persistence on escape/timeout
+ resume).

Revision ID: a1052standupconv
Revises: a1031softdelete
Create Date: 2026-05-04 18:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1052standupconv"
down_revision: Union[str, Sequence[str], None] = "a1031softdelete"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create standup_conversations table + indexes for Issue #1052."""

    op.create_table(
        "standup_conversations",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("session_id", sa.String(length=255), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=50), nullable=False),
        sa.Column("previous_state", sa.String(length=50), nullable=True),
        sa.Column(
            "preferences",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("current_standup", sa.Text(), nullable=True),
        sa.Column(
            "standup_versions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "turns",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column(
            "context",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
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
    op.create_index(
        "ix_standup_conversations_session_id",
        "standup_conversations",
        ["session_id"],
    )
    op.create_index(
        "ix_standup_conversations_user_id",
        "standup_conversations",
        ["user_id"],
    )
    op.create_index(
        "ix_standup_conversations_state",
        "standup_conversations",
        ["state"],
    )

    # Composite indexes matching expected query patterns:
    #   - get_active_for_user(user_id) → user_id + state filter
    #   - get_by_session_id(session_id) → session_id direct lookup
    op.create_index(
        "idx_standup_conv_user_state",
        "standup_conversations",
        ["user_id", "state"],
    )
    op.create_index(
        "idx_standup_conv_session",
        "standup_conversations",
        ["session_id"],
    )


def downgrade() -> None:
    """Drop standup_conversations table + indexes."""

    op.drop_index("idx_standup_conv_session", table_name="standup_conversations")
    op.drop_index("idx_standup_conv_user_state", table_name="standup_conversations")
    op.drop_index("ix_standup_conversations_state", table_name="standup_conversations")
    op.drop_index("ix_standup_conversations_user_id", table_name="standup_conversations")
    op.drop_index("ix_standup_conversations_session_id", table_name="standup_conversations")

    op.drop_table("standup_conversations")
