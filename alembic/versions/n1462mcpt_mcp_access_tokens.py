"""#1462 unit 1: mcp_access_tokens — fail-closed caller identity for the MCP server.

Bearer-token-in, real-user-out (Arch's #1462 condition 1: "no identity, no read;
never default to anonymous"). Only the SHA-256 hash of the raw token is stored
(`token_hash`, UNIQUE) — the raw token is minted by scripts/mint_mcp_token.py,
shown once to the operator's terminal, and never written to this table.
`user_id` is NOT NULL (no row resolves to an anonymous owner); `revoked_at` and
`expires_at` are the two refusal paths the verifier checks alongside "no such
hash" (services/mcp/server/identity.py).

Additive and reversible.

Revision ID: n1462mcpt
Revises: m1797drop
Create Date: 2026-09-26
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "n1462mcpt"
down_revision = "m1797drop"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mcp_access_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_mcp_access_tokens_user_id", "mcp_access_tokens", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_mcp_access_tokens_user_id", table_name="mcp_access_tokens")
    op.drop_table("mcp_access_tokens")
