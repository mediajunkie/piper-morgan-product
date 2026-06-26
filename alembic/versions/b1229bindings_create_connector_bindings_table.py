"""create connector_bindings table (RECONNECT WS-2 #1229)

Revision ID: b1229bindings
Revises: 000baa96d800
Create Date: 2026-06-26

WS-2 (#1229): per-user MCP-server binding storage (ADR-070 D3 — Piper stores bindings only,
never raw creds). owner_id FK to the settled single identity (ADR-071 D2) + a named-not-built
tenant_id (ADR-071 D7 / m-40), user-scoped (ADR-058). The foundation the WS-5 ports (#1317)
populate on connect(). Mirrors the WS-1 connector_configs migration (000baa96d800).

ADDITIVE: creates exactly one new table; touches nothing else. (The pre-existing DB<->model
drift surfaced by autogenerate across other tables is intentionally excluded — filed as #1312.)
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from services.database.models import CrossDialectUUID

# revision identifiers, used by Alembic.
revision: str = "b1229bindings"
down_revision: Union[str, Sequence[str], None] = "000baa96d800"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create connector_bindings (WS-2). Additive only."""
    op.create_table(
        "connector_bindings",
        sa.Column("id", CrossDialectUUID(), nullable=False),
        sa.Column("owner_id", CrossDialectUUID(), nullable=False),
        sa.Column("tenant_id", CrossDialectUUID(), nullable=True),
        sa.Column("connector", sa.String(length=50), nullable=False),
        sa.Column("mcp_server_ref", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=32), server_default=sa.text("'unbound'"), nullable=False),
        sa.Column(
            "capability_profile",
            postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite"),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column("is_native_legacy", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "owner_id", "connector", name="uq_connector_binding_owner_connector"
        ),
    )
    op.create_index(
        op.f("ix_connector_bindings_owner_id"), "connector_bindings", ["owner_id"], unique=False
    )
    op.create_index(
        op.f("ix_connector_bindings_tenant_id"), "connector_bindings", ["tenant_id"], unique=False
    )


def downgrade() -> None:
    """Drop connector_bindings."""
    op.drop_index(op.f("ix_connector_bindings_tenant_id"), table_name="connector_bindings")
    op.drop_index(op.f("ix_connector_bindings_owner_id"), table_name="connector_bindings")
    op.drop_table("connector_bindings")
