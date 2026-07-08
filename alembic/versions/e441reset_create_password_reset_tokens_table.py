"""create password_reset_tokens table (#441/#1261 beta password recovery)

Revision ID: e441reset
Revises: d075persctx
Create Date: 2026-07-07

#441 Phase 3 / #1261: PM-issued password-reset tokens — the beta auth model's
equivalent of email-based reset (no mailer exists in the product; PM/HOST mint a
code on request over the #1344 invite channel that already works). Faithful
sibling of invite_tokens (natural-key Crockford PK, used_at NULL = valid, atomic
conditional-UPDATE consumption — services/auth/password_reset_service.py) with
two deliberate differences: user_id is NOT NULL (a reset is bound to a specific
account at mint time) and expires_at is NOT NULL (a stale reset code is pure
liability; invites tolerate distribution lag, resets don't need to).

ADDITIVE: creates exactly one new table; touches nothing else.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from services.database.models import CrossDialectUUID

# revision identifiers, used by Alembic.
revision: str = "e441reset"
down_revision: Union[str, Sequence[str], None] = "d075persctx"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create password_reset_tokens (#441/#1261). Additive only."""
    op.create_table(
        "password_reset_tokens",
        sa.Column("token", sa.String(length=32), nullable=False),
        sa.Column("user_id", CrossDialectUUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("token"),
    )
    op.create_index(
        "ix_password_reset_tokens_user_id", "password_reset_tokens", ["user_id"]
    )


def downgrade() -> None:
    """Drop password_reset_tokens."""
    op.drop_index("ix_password_reset_tokens_user_id", table_name="password_reset_tokens")
    op.drop_table("password_reset_tokens")
