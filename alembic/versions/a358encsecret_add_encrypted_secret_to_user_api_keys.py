"""#358: add encrypted_secret to user_api_keys (encrypt-at-rest for the user-secret store)

Revision ID: a358encsecret
Revises: a1273coretables
Create Date: 2026-06-20

Additive, nullable column holding the AES-256-GCM encrypted secret (the #358 secret-store
floor / #1185 enabler). Per-user secrets currently live only in the OS keychain
(laptop-only); this column makes them portable to the hosted Linux box (no keychain there).
Nullable so legacy / pre-migration / local-dev rows (keychain-only) keep working —
`UserAPIKeyService.retrieve_user_key` prefers `encrypted_secret` and falls back to keychain.

Idempotent (safe to re-run against an already-migrated DB): add only if absent.
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a358encsecret"
down_revision: Union[str, Sequence[str], None] = "a1273coretables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    insp = sa.inspect(op.get_bind())
    cols = [c["name"] for c in insp.get_columns("user_api_keys")]
    if "encrypted_secret" not in cols:
        op.add_column("user_api_keys", sa.Column("encrypted_secret", sa.Text(), nullable=True))


def downgrade() -> None:
    insp = sa.inspect(op.get_bind())
    cols = [c["name"] for c in insp.get_columns("user_api_keys")]
    if "encrypted_secret" in cols:
        op.drop_column("user_api_keys", "encrypted_secret")
