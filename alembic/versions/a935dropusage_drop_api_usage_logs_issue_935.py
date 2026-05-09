"""drop_api_usage_logs_issue_935

Revision ID: a935dropusage
Revises: a900partialcapture
Create Date: 2026-05-09

#935 (May 9 2026): Drop the api_usage_logs table. Created by migration
68166c68224b for #271 CORE-KEYS-COST-TRACKING. APIUsageTracker is being
removed as dead code (call chain unreachable in production: callers of
LLMDomainService.complete() don't pass a session, so the INSERT path
never fires; table has 0 rows). Cost tracking is a beta-readiness
concern that we'll re-design with concrete scope when we actually need it.

The downgrade re-creates the table to match 68166c68224b's upgrade for
clean rollback if PM reverses the disposition.

See `dev/2026/05/09/935-issue-audit.md` for the full investigation.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a935dropusage"
down_revision: Union[str, Sequence[str], None] = "a900partialcapture"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop api_usage_logs table + its composite indexes."""
    # Drop composite indexes first (Postgres handles index drop on table drop
    # automatically, but being explicit is friendlier to anyone reading the
    # downgrade history).
    op.drop_index("idx_api_usage_logs_provider_created", table_name="api_usage_logs")
    op.drop_index("idx_api_usage_logs_user_created", table_name="api_usage_logs")
    op.drop_table("api_usage_logs")


def downgrade() -> None:
    """Re-create api_usage_logs (mirrors 68166c68224b's upgrade)."""
    op.create_table(
        "api_usage_logs",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(255), nullable=False, index=True),
        sa.Column("provider", sa.String(50), nullable=False, index=True),
        sa.Column("model", sa.String(100), nullable=False, index=True),
        sa.Column("prompt_tokens", sa.Integer, nullable=False, server_default="0"),
        sa.Column("completion_tokens", sa.Integer, nullable=False, server_default="0"),
        sa.Column("total_tokens", sa.Integer, nullable=False, server_default="0"),
        sa.Column("estimated_cost", sa.DECIMAL(10, 6), nullable=False, server_default="0.0"),
        sa.Column("conversation_id", sa.String(255), index=True),
        sa.Column("feature", sa.String(100), server_default="chat"),
        sa.Column("request_id", sa.String(255), index=True),
        sa.Column("response_time_ms", sa.Integer),
        sa.Column(
            "created_at",
            sa.TIMESTAMP,
            nullable=False,
            server_default=sa.func.current_timestamp(),
            index=True,
        ),
    )
    op.create_index("idx_api_usage_logs_user_created", "api_usage_logs", ["user_id", "created_at"])
    op.create_index(
        "idx_api_usage_logs_provider_created",
        "api_usage_logs",
        ["provider", "created_at"],
    )
