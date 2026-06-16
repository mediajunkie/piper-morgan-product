"""#1252 P7 (ADR-071 D2): add owner_id (UUID) to conversational_memory_entries + standup_conversations

Revision ID: a1252memstandupowner
Revises: a1252convowner
Create Date: 2026-06-16

Completes the m-40 additive step for the remaining String-`user_id` P7 tables
(after insights + conversations). Adds a canonical `owner_id` UUID column
ALONGSIDE `user_id` and backfills it (owner_id = user_id::uuid). Nullable,
FK-less. As of 2026-06-16: conversational_memory_entries has 0 rows (backfill is
a no-op), standup_conversations has 36 rows all with valid-UUID user_ids. The
WHERE-guard leaves any theoretical non-UUID as NULL rather than failing.

Out of additive scope (deferred to the breaking/naming pass): `feedback.user_id`
is ALREADY postgresql.UUID + FK (needs only a name → owner_id later);
`artifacts.owner_id` is already named owner_id but String (a breaking type change).
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1252memstandupowner"
down_revision: Union[str, Sequence[str], None] = "a1252convowner"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_UUID_RE = "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
_TABLES = ["conversational_memory_entries", "standup_conversations"]


def upgrade() -> None:
    """Add owner_id (UUID, nullable) + index to each table, then backfill."""
    for tbl in _TABLES:
        op.add_column(tbl, sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True))
        op.create_index(f"idx_{tbl}_owner", tbl, ["owner_id"])
        op.execute(f"UPDATE {tbl} SET owner_id = user_id::uuid WHERE user_id ~ '{_UUID_RE}'")


def downgrade() -> None:
    """Reversible: drop the index + the additive column on each table."""
    for tbl in _TABLES:
        op.drop_index(f"idx_{tbl}_owner", table_name=tbl)
        op.drop_column(tbl, "owner_id")
