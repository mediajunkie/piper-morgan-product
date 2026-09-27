"""#1462 unit 4: the MCP OAuth authorization server's three tables.

`mcp_oauth_clients` (RFC 7591 dynamic client registration — an APPLICATION, no
user_id by design), `mcp_oauth_codes` (the single-use authorization code, the one
row in the flow that carries identity: `user_id` NOT NULL, written only after a
real Piper web session consented), and `mcp_oauth_refresh_tokens` (rotating,
hashed at rest, same NOT-NULL owner discipline).

Access tokens deliberately get NO new table: an OAuth exchange writes an
`mcp_access_tokens` row (unit 1's table, label `oauth:<client_id>`) so
`MCPTokenVerifier` verifies OAuth-minted and operator-minted credentials through
exactly one code path — one verifier, one boundary.

Every column that carries IDENTITY stores only a SHA-256 hex digest — no raw
authorization code, access token, or refresh token is a column anywhere here. The
single exception is `mcp_oauth_clients.client_secret` (an application credential,
not a user credential), encrypted at rest via EncryptedString because the SDK's
ClientAuthenticator does the comparison and requires the value; see the model
docstring for the full reasoning.

Additive and reversible.

Revision ID: o1462oaut
Revises: n1462mcpt
Create Date: 2026-09-26
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "o1462oaut"
down_revision = "n1462mcpt"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "mcp_oauth_clients",
        sa.Column("client_id", sa.String(64), primary_key=True),
        # NULL = public client (PKCE only). Encrypted at rest (EncryptedString,
        # #358-B) rather than hashed — the SDK's ClientAuthenticator does the
        # comparison and needs the value; see the model docstring.
        sa.Column("client_secret", sa.Text(), nullable=True),
        sa.Column("client_secret_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("redirect_uris", postgresql.JSONB(), nullable=False),
        sa.Column("client_name", sa.String(255), nullable=True),
        sa.Column(
            "token_endpoint_auth_method",
            sa.String(32),
            nullable=False,
            server_default="client_secret_post",
        ),
        sa.Column("grant_types", postgresql.JSONB(), nullable=False),
        sa.Column("response_types", postgresql.JSONB(), nullable=False),
        sa.Column("scope", sa.String(255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "mcp_oauth_codes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("code_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("client_id", sa.String(64), nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("redirect_uri", sa.Text(), nullable=False),
        sa.Column(
            "redirect_uri_provided_explicitly",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column("code_challenge", sa.String(255), nullable=False),
        sa.Column("scopes", postgresql.JSONB(), nullable=False),
        sa.Column("resource", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("minted_access_token_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("minted_refresh_token_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index("ix_mcp_oauth_codes_client_id", "mcp_oauth_codes", ["client_id"])
    op.create_index("ix_mcp_oauth_codes_user_id", "mcp_oauth_codes", ["user_id"])

    op.create_table(
        "mcp_oauth_refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("token_hash", sa.String(64), nullable=False, unique=True),
        sa.Column("client_id", sa.String(64), nullable=False),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("scopes", postgresql.JSONB(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_mcp_oauth_refresh_tokens_client_id", "mcp_oauth_refresh_tokens", ["client_id"]
    )
    op.create_index("ix_mcp_oauth_refresh_tokens_user_id", "mcp_oauth_refresh_tokens", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_mcp_oauth_refresh_tokens_user_id", table_name="mcp_oauth_refresh_tokens")
    op.drop_index("ix_mcp_oauth_refresh_tokens_client_id", table_name="mcp_oauth_refresh_tokens")
    op.drop_table("mcp_oauth_refresh_tokens")
    op.drop_index("ix_mcp_oauth_codes_user_id", table_name="mcp_oauth_codes")
    op.drop_index("ix_mcp_oauth_codes_client_id", table_name="mcp_oauth_codes")
    op.drop_table("mcp_oauth_codes")
    op.drop_table("mcp_oauth_clients")
