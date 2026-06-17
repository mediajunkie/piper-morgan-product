"""#1267: create project_integrations table — the missing create-migration

Revision ID: a1267projintegrations
Revises: a1238documents
Create Date: 2026-06-17

`ProjectIntegrationDB` (services/database/models.py) existed as a model and had
ALTER migrations (`4d1e2c3b5f7a` owner_id, `d73b3722eb03` timestamptz) but **NO
`create_table` migration** — it was only ever created via `Base.metadata.create_all()`
(test-only path; no production caller). Both alters are IF-EXISTS-defensive, so a
fresh `alembic upgrade head` ran clean, SILENTLY skipped the never-created table,
and `GET /api/v1/projects` 500'd on the missing relation whenever a project had
integrations to eager-load (#1267, PM UAT 2026-06-17).

This migration is the table's home in the chain. It is **idempotent**, which is what
lets it repair already-deployed at-head DBs (the Beta-blocker population) as well as
fresh ones — a mid-chain insert (the `4ba89dbf5347` work_items precedent) would only
help DBs built from base, not DBs already stamped past the insert point:
  - table ABSENT  → create it with the full current schema (incl. `owner_id`).
  - table PRESENT → ensure `owner_id` exists (a create_all'd table from the current
    owner_id-less model lacks it; `4d1e2c3b5f7a` added it only where the table already
    existed when that migration ran). Keeps every DB consistent with the model, which
    now declares `owner_id` (ADR-071 D2; #1252 D2 fold).

Enum: the `integrationtype` PG type is created via an idempotent ``DO``-block (the
`8e4f2a3b9c5d` idiom — survives re-run / diamond deps) and the column references it
with ``postgresql.ENUM(create_type=False)`` so ``create_table`` does NOT re-emit
``CREATE TYPE`` (the generic ``sa.Enum`` ignores ``create_type`` → DuplicateObject).
Labels are the member NAMES (GITHUB/JIRA/LINEAR/SLACK) — the default mapping of
``Enum(IntegrationType)`` in the model, verified against the dev DB's create_all type.

#1252 D2 increment. ADR-071 D1 classification: project_integrations is user-content
(project-scoped config; projects are owner-anchored) → `owner_id` nullable (m-40
grace), NOT `is_global_pm_domain`.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1267projintegrations"
down_revision: Union[str, Sequence[str], None] = "a1238documents"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Member NAMES (not values) — the default Enum(IntegrationType) mapping, verified
# against the dev DB's create_all-produced `integrationtype` type.
_ENUM_LABELS = ("GITHUB", "JIRA", "LINEAR", "SLACK")
_OWNER_INDEX = "ix_project_integrations_owner_id"


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "project_integrations" not in inspector.get_table_names():
        # Fresh DB: create the full table (the #1267 fix — never migration-created).
        # Create the enum type idempotently first (8e4f idiom), then reference it with
        # create_type=False so create_table doesn't try to recreate it.
        op.execute(
            """
            DO $$ BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'integrationtype') THEN
                    CREATE TYPE integrationtype AS ENUM ('GITHUB', 'JIRA', 'LINEAR', 'SLACK');
                END IF;
            END $$;
            """
        )
        op.create_table(
            "project_integrations",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("project_id", sa.String(), nullable=False),
            sa.Column(
                "type",
                postgresql.ENUM(*_ENUM_LABELS, name="integrationtype", create_type=False),
                nullable=False,
            ),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("config", sa.JSON(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
            sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
            sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(_OWNER_INDEX, "project_integrations", ["owner_id"])
    else:
        # Existing DB (create_all / 2026-06-17 dev repair): table present. Ensure
        # owner_id exists so every DB matches the model (which now declares it).
        existing_cols = {c["name"] for c in inspector.get_columns("project_integrations")}
        if "owner_id" not in existing_cols:
            op.add_column(
                "project_integrations",
                sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
            )
            op.create_foreign_key(
                "fk_project_integrations_owner_id",
                "project_integrations",
                "users",
                ["owner_id"],
                ["id"],
            )
            existing_indexes = {ix["name"] for ix in inspector.get_indexes("project_integrations")}
            if _OWNER_INDEX not in existing_indexes:
                op.create_index(_OWNER_INDEX, "project_integrations", ["owner_id"])


def downgrade() -> None:
    # Inverse of "the table is created here": drop it (and its enum). Reversible by
    # convention; downgrading past this revision means project_integrations should
    # not exist.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "project_integrations" in inspector.get_table_names():
        op.drop_table("project_integrations")
    op.execute("DROP TYPE IF EXISTS integrationtype")
