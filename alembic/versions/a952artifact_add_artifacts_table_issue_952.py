"""Add artifacts table for #952 ARTIFACT-MODEL

Revision ID: a952artifact
Revises: a1021userhist
Create Date: 2026-06-09

Adds the `artifacts` table backing services.database.models.ArtifactDB — the
#952 unifying-lens persistence layer (Arch-ratified 2026-06-08). Plain JSON
payload (not JSONB) to match the model + keep it dialect-portable.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a952artifact"
down_revision: Union[str, Sequence[str], None] = "a1021userhist"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "artifacts",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("owner_id", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("lifecycle_state", sa.String(length=20), nullable=True),
        sa.Column("source_conversation_id", sa.String(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_artifacts_owner", "artifacts", ["owner_id", "created_at"])
    op.create_index("idx_artifacts_source_type", "artifacts", ["source_type"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_artifacts_source_type", table_name="artifacts")
    op.drop_index("idx_artifacts_owner", table_name="artifacts")
    op.drop_table("artifacts")
