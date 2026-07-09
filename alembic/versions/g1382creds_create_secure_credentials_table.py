"""create secure_credentials table (#1382 tier-2 — hosted credential store)

The OS-keychain layer has no backend on hosted Linux (found live 2026-07-08:
every KeychainService op failed on the droplet, killing OAuth token storage and
all keychain reads). This table is the encrypted-at-rest DB fallback behind the
KeychainService seam: `name` is the exact composed key name the service already
generates ({provider}_api_key / {user}_{provider}_api_key), `encrypted_value` is
FieldEncryptionService output under a per-name HKDF context
(secure_credentials.{name}) — no plaintext column exists, ever.

Revision ID: g1382creds
Revises: f1305encjson
Create Date: 2026-07-09
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "g1382creds"
down_revision: Union[str, Sequence[str], None] = "f1305encjson"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "secure_credentials",
        sa.Column("name", sa.String(length=512), primary_key=True),
        sa.Column("encrypted_value", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("secure_credentials")
