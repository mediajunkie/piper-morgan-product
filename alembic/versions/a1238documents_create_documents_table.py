"""#1238 (ADR-071 P2): create documents table — relational anchor for the ChromaDB doc store

Revision ID: a1238documents
Revises: a1252memstandupowner
Create Date: 2026-06-16

The doc store (`pm_knowledge` ChromaDB collection) is ChromaDB-only — no relational
row backs each document. ADR-071 D2 mandates an owner-anchored row for every content
store; this table is that row's explicit home (Arch ruling 2026-06-16: the
`is_global_pm_domain` D1-exemption marker lives on the DB row, NOT ChromaDB metadata,
so the D5 AST guard + SQL can both see it).

Additive + reversible: a brand-new table, no data touched. One row per ingested
document, linked to its ChromaDB chunks by `chromadb_base_id` (the `pdf_<hash>` base
of the per-chunk ids). Backfill of the existing doc(s) is a separate idempotent step
(scripts/backfill_documents_1238.py), not this migration.

Index names mirror the SQLAlchemy `index=True` convention (`ix_documents_<col>`) so the
model and migration stay drift-free.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1238documents"
down_revision: Union[str, Sequence[str], None] = "a1252memstandupowner"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the documents table (additive; no data touched)."""
    op.create_table(
        "documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chromadb_base_id", sa.String(length=255), nullable=False),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "is_global_pm_domain",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("source", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_chromadb_base_id", "documents", ["chromadb_base_id"], unique=True)
    op.create_index("ix_documents_owner_id", "documents", ["owner_id"], unique=False)
    op.create_index(
        "ix_documents_is_global_pm_domain", "documents", ["is_global_pm_domain"], unique=False
    )


def downgrade() -> None:
    """Reversible: drop the indexes + the table."""
    op.drop_index("ix_documents_is_global_pm_domain", table_name="documents")
    op.drop_index("ix_documents_owner_id", table_name="documents")
    op.drop_index("ix_documents_chromadb_base_id", table_name="documents")
    op.drop_table("documents")
