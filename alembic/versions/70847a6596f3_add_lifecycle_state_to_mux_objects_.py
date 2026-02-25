"""add lifecycle_state to mux objects issue 718

Revision ID: 70847a6596f3
Revises: 80ce53cc1267
Create Date: 2026-01-27 14:00:41.366912

Adds lifecycle_state column to four MUX object tables:
- features
- work_items
- projects
- todo_items

This enables the MUX lifecycle UI features (#708, #709) to persist
lifecycle state. Column is nullable to maintain backward compatibility
with existing rows.

Valid values match LifecycleState enum:
emergent, derived, noticed, proposed, ratified, deprecated, archived, composted
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "70847a6596f3"
down_revision: Union[str, Sequence[str], None] = "4ba89dbf5347"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tables that need lifecycle_state column
TABLES_WITH_LIFECYCLE = ["features", "work_items", "projects", "todo_items"]


def upgrade() -> None:
    """Add lifecycle_state column to MUX object tables."""
    from sqlalchemy import inspect
    
    conn = op.get_bind()
    inspector = inspect(conn)
    
    for table_name in TABLES_WITH_LIFECYCLE:
        # Check if table exists and if column already exists
        if table_name in inspector.get_table_names():
            columns = [col["name"] for col in inspector.get_columns(table_name)]
            if "lifecycle_state" not in columns:
                op.add_column(table_name, sa.Column("lifecycle_state", sa.String(50), nullable=True))
        # If table doesn't exist (e.g., features was just created), skip it


def downgrade() -> None:
    """Remove lifecycle_state column from MUX object tables."""
    for table_name in TABLES_WITH_LIFECYCLE:
        op.drop_column(table_name, "lifecycle_state")
