"""#1466: Slack user → Piper user principal mapping — slack_identities +
the mint-in-Piper/redeem-in-Slack link-code handshake tables.

Three tables:
- slack_identities — the durable mapping. owner_id FK users;
  UNIQUE(slack_user_id, slack_team_id) so a Slack identity can never resolve
  to two owners (ADR-070 identity boundary). Re-link of an already-linked
  identity is caught at the constraint and answered fail-closed (Arch
  condition 2) — never silent no-op, never owner overwrite.
- slack_link_codes — short-TTL (~10 min) single-use 6-digit codes, third
  member of the InviteToken/PasswordResetToken family (natural-key PK,
  used_at NULL = valid, atomic conditional-UPDATE consumption). Bound to the
  minting user like PasswordResetToken, NOT identity-blind like InviteToken —
  which is why this is a sibling table, not a `kind` column on invite_tokens.
- slack_link_attempts — Arch condition 1: redemption-attempt ledger backing
  the per-slack-user AND per-team bounded-attempts rate limit (6-digit codes
  are ~20 bits over an unauthenticated channel; the limit is REQUIRED, not a
  nice-to-have).

Additive and reversible.

Revision ID: l1466slack
Revises: k1422prefs
Create Date: 2026-08-03
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "l1466slack"
down_revision = "k1422prefs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "slack_identities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "owner_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("slack_user_id", sa.String(32), nullable=False),
        sa.Column("slack_team_id", sa.String(32), nullable=False),
        sa.Column(
            "linked_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "slack_user_id", "slack_team_id", name="uq_slack_identities_user_team"
        ),
    )
    op.create_index(
        "ix_slack_identities_owner_id", "slack_identities", ["owner_id"]
    )

    op.create_table(
        "slack_link_codes",
        sa.Column("code", sa.String(12), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        # NULL = unused/valid. Set atomically by the conditional UPDATE at redemption.
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_slack_link_codes_user_id", "slack_link_codes", ["user_id"])

    op.create_table(
        "slack_link_attempts",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("slack_user_id", sa.String(32), nullable=False),
        sa.Column("slack_team_id", sa.String(32), nullable=False),
        sa.Column(
            "attempted_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        "idx_slack_link_attempts_user_time",
        "slack_link_attempts",
        ["slack_user_id", "attempted_at"],
    )
    op.create_index(
        "idx_slack_link_attempts_team_time",
        "slack_link_attempts",
        ["slack_team_id", "attempted_at"],
    )


def downgrade() -> None:
    op.drop_index("idx_slack_link_attempts_team_time", table_name="slack_link_attempts")
    op.drop_index("idx_slack_link_attempts_user_time", table_name="slack_link_attempts")
    op.drop_table("slack_link_attempts")
    op.drop_index("ix_slack_link_codes_user_id", table_name="slack_link_codes")
    op.drop_table("slack_link_codes")
    op.drop_index("ix_slack_identities_owner_id", table_name="slack_identities")
    op.drop_table("slack_identities")
