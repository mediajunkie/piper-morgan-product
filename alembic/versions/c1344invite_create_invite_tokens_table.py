"""create invite_tokens table (#1344 alpha-registration gate)

Revision ID: c1344invite
Revises: b1229bindings
Create Date: 2026-07-03

#1344 (Arch Gap-A closure, HOST/Arch/Lead contract 2026-07-03): create_user requires a
valid, unused invite token. token is the PK directly (natural key, normalized-uppercase
Crockford Base32); used_at NULL = valid/unused, set atomically by a single conditional
UPDATE at registration (never check-then-write — see services/auth/invite_token_service.py
for why). This table holds no tester identity — HOST's roster (gitignored, outside this DB)
owns the token-to-identity mapping.

ADDITIVE: creates exactly one new table; touches nothing else.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from services.database.models import CrossDialectUUID

# revision identifiers, used by Alembic.
revision: str = "c1344invite"
down_revision: Union[str, Sequence[str], None] = "b1229bindings"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create invite_tokens (#1344). Additive only."""
    op.create_table(
        "invite_tokens",
        sa.Column("token", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("used_by_user_id", CrossDialectUUID(), nullable=True),
        sa.ForeignKeyConstraint(["used_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("token"),
    )


def downgrade() -> None:
    """Drop invite_tokens."""
    op.drop_table("invite_tokens")
