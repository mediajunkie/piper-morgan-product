"""1680: four consequential-action flags on ``audit_logs`` (Dashboard Criterion E).

Follows s2014items. Arch ruled the carrier on 2026-11-02 (decisions.log, 11:00): the
audit-log row, with the four flags as typed, non-null boolean columns that default to
false, added by one migration and never as keys in ``details`` JSON, so the dashboard
counts them in SQL and a missing flag is a schema error rather than an absent key.

* ``proactive``: Piper initiated the action (not a direct user request)
* ``credits_spent``: the site's own code path called the LLM
* ``external_message``: the action sent something outside Piper (Slack, GitHub)
* ``hard_to_reverse``: the action is irreversible or difficult to undo

Existing rows take ``false`` through the server default; they are not consequential
rows (``event_type <> 'consequential'``), so false is their true value.

Downgrade drops the four columns.

Revision ID: t1680flags
Revises: s2014items
Create Date: 2026-11-02
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "t1680flags"
down_revision = "s2014items"
branch_labels = None
depends_on = None

_FLAGS = ("proactive", "credits_spent", "external_message", "hard_to_reverse")


def upgrade() -> None:
    for name in _FLAGS:
        op.add_column(
            "audit_logs",
            sa.Column(name, sa.Boolean(), nullable=False, server_default=sa.false()),
        )


def downgrade() -> None:
    for name in reversed(_FLAGS):
        op.drop_column("audit_logs", name)
