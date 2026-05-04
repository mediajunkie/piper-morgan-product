"""add_ethics_audit_log_table_issue_1018

Issue #1018 Phase 2: persist ethics audit log to durable storage.

Pre-#1018, `services/ethics/audit_transparency.py` stored entries in an
in-memory Python list (max 10K, lost on restart). User-facing transparency
endpoints could lie after any deploy/crash. This migration adds the
`ethics_audit_log` table that backs the new `EthicsAuditLogDB` model
+ `EthicsAuditRepository`.

Sibling to (not replacement of) the existing `audit_logs` table from
Issue #249 — that one is for security/auth events; this one is for
ethics-decision events (different schema, different access patterns,
different retention).

Revision ID: a1018ethicsaudit
Revises: b942_orchestration_tables
Create Date: 2026-05-02 16:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1018ethicsaudit"
down_revision: Union[str, Sequence[str], None] = "b942_orchestration_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create ethics_audit_log table + indexes for Issue #1018."""

    op.create_table(
        "ethics_audit_log",
        sa.Column("entry_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("session_id", sa.String(length=255), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "details",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column("redacted", sa.Boolean(), nullable=False, server_default=sa.text("true")),
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
        sa.PrimaryKeyConstraint("entry_id"),
    )

    # Per-column indexes (matches Column(..., index=True) declarations).
    op.create_index(
        "ix_ethics_audit_log_event_type", "ethics_audit_log", ["event_type"]
    )
    op.create_index(
        "ix_ethics_audit_log_timestamp", "ethics_audit_log", ["timestamp"]
    )
    op.create_index(
        "ix_ethics_audit_log_session_id", "ethics_audit_log", ["session_id"]
    )
    op.create_index(
        "ix_ethics_audit_log_user_id", "ethics_audit_log", ["user_id"]
    )

    # Composite indexes matching actual query patterns from
    # audit_transparency.py (per Phase 1 design doc).
    op.create_index(
        "idx_ethics_audit_user_time", "ethics_audit_log", ["user_id", "timestamp"]
    )
    op.create_index(
        "idx_ethics_audit_event_time", "ethics_audit_log", ["event_type", "timestamp"]
    )


def downgrade() -> None:
    """Drop ethics_audit_log table + indexes."""

    op.drop_index("idx_ethics_audit_event_time", table_name="ethics_audit_log")
    op.drop_index("idx_ethics_audit_user_time", table_name="ethics_audit_log")
    op.drop_index("ix_ethics_audit_log_user_id", table_name="ethics_audit_log")
    op.drop_index("ix_ethics_audit_log_session_id", table_name="ethics_audit_log")
    op.drop_index("ix_ethics_audit_log_timestamp", table_name="ethics_audit_log")
    op.drop_index("ix_ethics_audit_log_event_type", table_name="ethics_audit_log")

    op.drop_table("ethics_audit_log")
