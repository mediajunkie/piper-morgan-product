"""2327: ``floored_action_counts``, the out-of-vocabulary floored action counter.

Follows u2342reason. Arch ruled it on 2026-11-14 (issue 2327): a floored action name
that is in no vocabulary is a handler-gap candidate (the 2270 class), and the audit
must be readable by a seat without a served-log read. One row per (name, site, UTC
day) holding a count and nothing else (HOST's content bar): no user, no message text.

Additive: one new table. Nothing existing is altered, dropped or rewritten.

Downgrade drops the table.

Revision ID: v2327floored
Revises: u2342reason
Create Date: 2026-11-14
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "v2327floored"
down_revision = "u2342reason"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "floored_action_counts",
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.Column("site", sa.String(length=64), nullable=False),
        sa.Column("day", sa.Date(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("name", "site", "day"),
    )


def downgrade() -> None:
    op.drop_table("floored_action_counts")
