"""create connector_configs table (RECONNECT WS-1 #1226)

Revision ID: 000baa96d800
Revises: a358encsecret
Create Date: 2026-06-21

WS-1 (#1226 / #1199): the DB-backed connector-config home (ADR-070 D4) — owner_id FK to the
settled single identity (ADR-071 D2) + a named-not-built tenant_id (ADR-071 D7 / m-40), holding
config only (no creds — D3). ADDITIVE: creates exactly one new table; touches nothing else.

NOTE: `alembic revision --autogenerate` surfaced substantial *pre-existing* DB↔model drift
across other tables (standup/token_blacklist/uploaded_files/user_api_keys/users indexes + FKs,
a couple of dropped columns, etc.). That drift is **intentionally excluded** here — this
migration is connector_configs-only. The drift is filed separately as discovered tech-debt.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op
from services.database.models import CrossDialectUUID

# revision identifiers, used by Alembic.
revision: str = "000baa96d800"
down_revision: Union[str, Sequence[str], None] = "a358encsecret"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create connector_configs (WS-1). Additive only."""
    op.create_table(
        "connector_configs",
        sa.Column("id", CrossDialectUUID(), nullable=False),
        sa.Column("owner_id", CrossDialectUUID(), nullable=False),
        sa.Column("tenant_id", CrossDialectUUID(), nullable=True),
        sa.Column("connector", sa.String(length=50), nullable=False),
        sa.Column(
            "config",
            postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite"),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_id", "connector", name="uq_connector_config_owner_connector"),
    )
    op.create_index(
        op.f("ix_connector_configs_owner_id"), "connector_configs", ["owner_id"], unique=False
    )
    op.create_index(
        op.f("ix_connector_configs_tenant_id"), "connector_configs", ["tenant_id"], unique=False
    )


def downgrade() -> None:
    """Drop connector_configs."""
    op.drop_index(op.f("ix_connector_configs_tenant_id"), table_name="connector_configs")
    op.drop_index(op.f("ix_connector_configs_owner_id"), table_name="connector_configs")
    op.drop_table("connector_configs")
