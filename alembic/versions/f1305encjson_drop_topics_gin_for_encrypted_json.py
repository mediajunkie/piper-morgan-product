"""drop idx_conversations_topics_gin — topics is EncryptedJSON now (#1305)

Revision ID: f1305encjson
Revises: e441reset
Create Date: 2026-07-07

#1305 encrypts the PII-bearing JSON/JSONB columns via the EncryptedJSON
TypeDecorator (app-layer; column types unchanged — ciphertext is stored as
valid JSON). The ONE schema change is dropping `idx_conversations_topics_gin`:
the sweep (proposal memo 2026-07-07, Arch-ratified) found ZERO server-side
queries against `topics` — its only consumer filters in Python after ORM load,
which transparent decryption preserves — so the index was already dead weight,
and after encryption it would index ciphertext strings while *looking*
load-bearing. Dropping it here, with this paper trail, prevents a future
engineer from "restoring" a GIN index that never worked on encrypted data.

No other DDL: the 7 columns' encryption is enforced at the ORM layer, and the
#1305 backfill script (scripts/backfill_encrypt_json_1305.py) converts existing
plaintext rows. Reversible: downgrade recreates the index (only meaningful on
still-plaintext data — i.e., before the backfill ran).
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f1305encjson"
down_revision: Union[str, Sequence[str], None] = "e441reset"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop the unqueried (and soon ciphertext-blind) topics GIN index."""
    op.execute("DROP INDEX IF EXISTS idx_conversations_topics_gin")


def downgrade() -> None:
    """Recreate the GIN index (meaningful only on plaintext-topics data)."""
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversations_topics_gin "
        "ON conversations USING gin (topics)"
    )
