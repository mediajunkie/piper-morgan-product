"""ADR-078 D1 (#1394) — the session_activity ledger.

Additive create-table only; no touch to any existing table (the #1312 autogen-empty
invariant stays clean). Holds the owner-scoped record of external artifacts a session
created ('issue_created' → 'owner/repo#107'), read at two seams (B4 recall now, B3
pre-classifier resolution later). Refs are soft Strings (ArtifactDB #952 precedent) —
owner_id NOT NULL is the D1a read-scoping key; the reader, not a DB FK, enforces it.

Revision ID: j1394ledger
Revises: i070abackfill
Create Date: 2026-07-15
"""

import sqlalchemy as sa
from alembic import op

revision = "j1394ledger"
down_revision = "i070abackfill"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "session_activity",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("conversation_id", sa.String(), nullable=False),
        # D1a — the read-scoping key; NOT NULL, never resolved session-alone.
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column(
            "turn_id",
            sa.String(),
            nullable=True,
            comment="Which turn created it (soft ref conversation_turns.id)",
        ),
        sa.Column(
            "action_type",
            sa.String(),
            nullable=False,
            comment="'issue_created' | 'doc_created' | ...",
        ),
        sa.Column(
            "target_ref",
            sa.String(),
            nullable=False,
            comment="External pointer, e.g. 'owner/repo#107' — NOT content",
        ),
        sa.Column(
            "target_title",
            sa.String(),
            nullable=True,
            comment="Human title for antecedent display (B3)",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index(
        "idx_session_activity_owner_conv",
        "session_activity",
        ["owner_id", "conversation_id", "created_at"],
    )
    op.create_index(
        "idx_session_activity_conversation",
        "session_activity",
        ["conversation_id"],
    )


def downgrade() -> None:
    op.drop_index("idx_session_activity_conversation", table_name="session_activity")
    op.drop_index("idx_session_activity_owner_conv", table_name="session_activity")
    op.drop_table("session_activity")
