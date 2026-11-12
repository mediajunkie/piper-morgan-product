"""2342: ``status_reason`` on ``connector_bindings`` (ADR-081 D3, GitHub App cutover).

Follows t1680flags. Arch ruled it on 2026-11-11 19:23 (issue 2342): why a binding is
STALE is a stored fact, written when it is observed (``cutover`` or
``refresh_rejected``) and never inferred when a reply is rendered. Nullable, no default:
every existing row is NULL, which reads as "no recorded reason" and keeps the ordinary
re-authorize line.

Schema only. This migration marks no binding and deletes no token. The cutover's data
step is ``scripts/github_app_cutover.py``, run by hand after the App's secrets are set
(Arch 2026-11-12 06:51).

Downgrade drops the column.

Revision ID: u2342reason
Revises: t1680flags
Create Date: 2026-11-12
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "u2342reason"
down_revision = "t1680flags"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "connector_bindings",
        sa.Column("status_reason", sa.String(length=32), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("connector_bindings", "status_reason")
