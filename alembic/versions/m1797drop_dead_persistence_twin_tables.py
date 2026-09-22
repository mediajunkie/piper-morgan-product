"""#1797: drop the five dead-persistence-twin tables (create_all residue).

products, features, intents, stakeholders, tasks — zero live consumers of their
models (census in #1797 and the deleting commit), zero rows in every database
checked (local dev + the droplet dump that seeded Fly at the 2026-09-22
cutover), and no create-table migration ever managed them (#1273): they exist
only where create_all ran. The corresponding DB classes are deleted in the same
commit, so create_all can never resurrect them. Downgrade is deliberately a
no-op — there is no schema of record to restore (never migration-managed) and
no data to lose (empty everywhere, counts recorded on the issue).

CASCADE's collateral, named (verified on the local dev DB post-apply): the two
foreign-key CONSTRAINTS on the LIVE work_items table (product_id -> products.id,
feature_id -> features.id) are dropped with their target tables — the columns
and rows on work_items are untouched, and the model's Column defs drop their
ForeignKey() in the same commit so autogenerate stays reconciled (#1312 guard).
Nothing else references the five tables (pg_constraint swept).
"""

from alembic import op

revision = "m1797drop"
down_revision = "a1599admin"
branch_labels = None
depends_on = None

_TABLES = ("tasks", "intents", "stakeholders", "features", "products")


def upgrade() -> None:
    for t in _TABLES:
        op.execute(f'DROP TABLE IF EXISTS "{t}" CASCADE')


def downgrade() -> None:
    # Intentionally a no-op: see module docstring.
    pass
