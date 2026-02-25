"""create_features_table

Revision ID: 192abbccc4ae
Revises: 80ce53cc1267
Create Date: 2026-02-06 11:36:20.760678

Creates the features table that was missing but referenced by later migrations.
This table stores product features/capabilities.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '192abbccc4ae'
down_revision: Union[str, Sequence[str], None] = '80ce53cc1267'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create features table matching Feature model."""
    op.create_table(
        "features",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("product_id", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("hypothesis", sa.Text(), nullable=True),
        sa.Column("acceptance_criteria", postgresql.JSON(), nullable=True),
        sa.Column("status", sa.String(), nullable=True, server_default="draft"),
        sa.Column("lifecycle_state", sa.String(50), nullable=True),  # Added by 70847a6596f3
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id", name="pk_features"),
        # Foreign key to products is optional - products table may not exist yet
        # sa.ForeignKeyConstraint(["product_id"], ["products.id"], name="fk_features_product_id"),
    )
    
    # Create indexes
    op.create_index("idx_features_product_id", "features", ["product_id"])
    op.create_index("idx_features_status", "features", ["status"])


def downgrade() -> None:
    """Drop features table."""
    op.drop_index("idx_features_status", table_name="features")
    op.drop_index("idx_features_product_id", table_name="features")
    op.drop_table("features")
