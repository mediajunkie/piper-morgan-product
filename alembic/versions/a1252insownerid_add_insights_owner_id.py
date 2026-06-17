"""#1252 P7 (ADR-071 D2): add insights.owner_id (UUID), backfill from user_id

Revision ID: a1252insownerid
Revises: a952artifact
Create Date: 2026-06-16

m-40 layer-then-migrate, additive/non-breaking first step: add a canonical
`owner_id` UUID column ALONGSIDE the legacy `user_id` string and backfill it
(owner_id = user_id::uuid). Nullable + no FK (insights survive user deletion,
matching user_id). Readers migrate to owner_id and the user_id column is dropped
in later increments. All existing `user_id` values are valid UUID-strings as of
2026-06-16 (verified: 0 non-UUID across 33 rows); the WHERE-guard tolerates a
theoretical non-UUID by leaving owner_id NULL rather than failing the migration.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1252insownerid"
down_revision: Union[str, Sequence[str], None] = "a952artifact"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_UUID_RE = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"


def upgrade() -> None:
    """Add owner_id (UUID, nullable) + index, then backfill from user_id."""
    op.add_column(
        "insights",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index("idx_insights_owner", "insights", ["owner_id"])
    # Backfill only well-formed UUID strings; leave any (theoretical) non-UUID
    # user_id as NULL owner_id — non-destructive, never fails the migration.
    op.execute(f"UPDATE insights SET owner_id = user_id::uuid WHERE user_id ~ '{_UUID_RE}'")


def downgrade() -> None:
    """Reversible: drop the index + the additive column (user_id untouched)."""
    op.drop_index("idx_insights_owner", table_name="insights")
    op.drop_column("insights", "owner_id")
