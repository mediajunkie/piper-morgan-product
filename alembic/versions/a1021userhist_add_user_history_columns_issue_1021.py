"""add_user_history_columns_issue_1021

Issue #1021 Phase 2.1: extend conversations table with the columns
UserHistoryRepository needs (topics, preview, is_private, turn_count)
to back ConversationSummary / ConversationDetail without a parallel
summary table.

Per #1021 PM audit dispositions May 14:
- Q1 schema shape: γ (extend ConversationDB, not parallel summary table).
- Q2 topics maintenance: heuristic from intents+entities at turn-save.
- Q3 preview maintenance: set on first turn, refreshed on archive
  transition.
- Q4 is_private surface: ship column + repo + chat-actions in this phase.
- Q6 migration scope: include all 3 indexes.

Phase 2.2+ will land the DB-backed UserHistoryRepository, the
heuristic topic-extraction, the chat-action handlers, and the
context_assembler get_history_summary wiring against these columns.

See `dev/2026/05/14/1021-phase-1-design.md` for the full design memo
and `dev/2026/05/14/1021-issue-audit.md` for the Phase 0 audit.

Revision ID: a1021userhist
Revises: a935dropusage
Create Date: 2026-05-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


revision: str = "a1021userhist"
down_revision: Union[str, Sequence[str], None] = "a935dropusage"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add user-history columns + indexes to conversations table."""
    op.add_column(
        "conversations",
        sa.Column(
            "topics",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
    )
    op.add_column(
        "conversations",
        sa.Column(
            "preview",
            sa.Text(),
            nullable=False,
            server_default=sa.text("''"),
        ),
    )
    op.add_column(
        "conversations",
        sa.Column(
            "is_private",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "conversations",
        sa.Column(
            "turn_count",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
    )

    # Pagination: ORDER BY last_activity_at DESC scoped to a user.
    # Postgres can scan a B-tree backwards, no explicit DESC needed.
    op.create_index(
        "idx_conversations_user_last_activity",
        "conversations",
        ["user_id", "last_activity_at"],
    )

    # Privacy filtering on the history list.
    op.create_index(
        "idx_conversations_user_private",
        "conversations",
        ["user_id", "is_private"],
    )

    # Topic search across conversations.
    op.create_index(
        "idx_conversations_topics_gin",
        "conversations",
        ["topics"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    """Drop user-history columns + indexes from conversations table."""
    op.drop_index("idx_conversations_topics_gin", table_name="conversations")
    op.drop_index("idx_conversations_user_private", table_name="conversations")
    op.drop_index("idx_conversations_user_last_activity", table_name="conversations")
    op.drop_column("conversations", "turn_count")
    op.drop_column("conversations", "is_private")
    op.drop_column("conversations", "preview")
    op.drop_column("conversations", "topics")
