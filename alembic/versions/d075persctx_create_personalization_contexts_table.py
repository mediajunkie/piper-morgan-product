"""create personalization_contexts table (ADR-075 Component B, #1366)

Revision ID: d075persctx
Revises: c1344invite
Create Date: 2026-07-06

ADR-075 D2: the DB-backed, owner_id-scoped home for per-user system-prompt
personalization (category-1 config: name/role/timezone/style/focus/portfolio/
standing-priorities) — extends ADR-071's owner_id-anchoring from content rows
to configuration, mirroring connector_configs' shape one layer up. owner_id FK
to the settled identity (ADR-071 D2); a named-not-built tenant_id (ADR-071 D7 /
m-40); `is_seeded_default` distinguishes a lazy-seeded neutral-default row from
one the user has actually customized (ADR-075 OQ-3 / HOST's real-seeded-record
requirement). ADDITIVE: creates exactly one new table; touches nothing else.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from services.database.models import CrossDialectUUID

# revision identifiers, used by Alembic.
revision: str = "d075persctx"
down_revision: Union[str, Sequence[str], None] = "c1344invite"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create personalization_contexts (ADR-075 Component B). Additive only."""
    op.create_table(
        "personalization_contexts",
        sa.Column("id", CrossDialectUUID(), nullable=False),
        sa.Column("owner_id", CrossDialectUUID(), nullable=False),
        sa.Column("tenant_id", CrossDialectUUID(), nullable=True),
        sa.Column(
            "context",
            postgresql.JSONB(astext_type=sa.Text()).with_variant(sa.JSON(), "sqlite"),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column(
            "is_seeded_default",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
        sa.Column(
            "has_seen_personalization_notice",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_id", name="uq_personalization_contexts_owner"),
    )
    op.create_index(
        op.f("ix_personalization_contexts_owner_id"),
        "personalization_contexts",
        ["owner_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_personalization_contexts_tenant_id"),
        "personalization_contexts",
        ["tenant_id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop personalization_contexts."""
    op.drop_index(
        op.f("ix_personalization_contexts_tenant_id"), table_name="personalization_contexts"
    )
    op.drop_index(
        op.f("ix_personalization_contexts_owner_id"), table_name="personalization_contexts"
    )
    op.drop_table("personalization_contexts")
