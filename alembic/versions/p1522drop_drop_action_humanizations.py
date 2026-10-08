"""#1522: drop action_humanizations — the table behind the deleted
services/persistence/ package.

Architect GO (2026-10-05, mailboxes/lead/read/rule-arch-...-1522-...md):
`services/persistence/` had no production importer (only a test pin and a
dev script referenced it), and the table it backed is a humanization cache —
regenerable, not a system of record. GO to delete the package and drop the
table, on two conditions:

(a) count prod rows first, state the number in the commit — not assumed
    empty. **Production `action_humanizations` row count: 0**, per PM's
    read-only psql query against piper_morgan on piper-morgan-db, ~16:3x PT
    2026-10-07, relayed by Exec
    (mailboxes/lead/read/answer-exec-to-lead-production-db-counts-...md).
    No data is lost by this drop.
(b) downgrade() recreates the table schema (empty), so the migration chain
    stays reversible even though the dropped data isn't.

Schema recreated in downgrade() matches the table's actual shape as of this
migration — unbounded `character varying` columns (the original
8ef0aa7cbc90 migration used bare `sa.String()`, which the
services/persistence/models.py ORM model declared with explicit lengths that
were never enforced at the DB level) and `TIMESTAMPTZ` for `created_at` and
`last_used` (converted from naive `TIMESTAMP` by d73b3722eb03,
2026-02-03). Verified against the live local Postgres (`\\d
action_humanizations` at head, pre-drop) rather than inferred from the model.

Revision ID: p1522drop
Revises: o1462oaut
Create Date: 2026-10-07
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "p1522drop"
down_revision = "o1462oaut"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_table("action_humanizations")


def downgrade() -> None:
    op.create_table(
        "action_humanizations",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("human_readable", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("usage_count", sa.Integer(), nullable=True),
        sa.Column("last_used", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_action_humanizations_action", "action_humanizations", ["action"], unique=True
    )
