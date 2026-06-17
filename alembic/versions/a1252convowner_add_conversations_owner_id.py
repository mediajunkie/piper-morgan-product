"""#1252 P7 (ADR-071 D2): add conversations.owner_id (UUID), backfill from user_id

Revision ID: a1252convowner
Revises: a1252insownerid
Create Date: 2026-06-16

m-40 additive/non-breaking step (sibling of a1252insownerid for insights): add a
canonical `owner_id` UUID column ALONGSIDE the legacy `user_id` string and
backfill it (owner_id = user_id::uuid). Nullable + no FK. All existing user_id
values are valid UUID-strings as of 2026-06-16 (verified: 0 non-UUID across 490
rows); 83 of them reference no current `users.id` row, which is fine for this
FK-less additive column (the orphan-owner disposition only matters when/if a FK
constraint is later added, in the breaking pass). The WHERE-guard leaves any
theoretical non-UUID user_id as NULL rather than failing the migration.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1252convowner"
down_revision: Union[str, Sequence[str], None] = "a1252insownerid"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_UUID_RE = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"


def upgrade() -> None:
    """Add owner_id (UUID, nullable) + index, then backfill from user_id."""
    op.add_column(
        "conversations",
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index("idx_conversations_owner", "conversations", ["owner_id"])
    op.execute(f"UPDATE conversations SET owner_id = user_id::uuid WHERE user_id ~ '{_UUID_RE}'")


def downgrade() -> None:
    """Reversible: drop the index + the additive column (user_id untouched)."""
    op.drop_index("idx_conversations_owner", table_name="conversations")
    op.drop_column("conversations", "owner_id")
