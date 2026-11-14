"""2327: ``floored_action_counts``, the out-of-vocabulary floored action counter.

Follows u2342reason. Arch ruled it on 2026-11-14 (issue 2327): a floored action name
that is in no vocabulary is a handler-gap candidate (the 2270 class), and the audit
must be readable by a seat without a served-log read. One row per (name, site, UTC
day) holding a count and nothing else (HOST's content bar): no user, no message text.

It also adds ``users.ops_reader`` (Arch's read-gate ruling, the same day): a narrow
flag, false for every existing and new account, that opens the read-only counter
endpoint and nothing else. An admin sets it on one named account from the admin
account-flags page.

Additive: one new table and one new column with a default. Nothing existing is
dropped or rewritten, and no row's meaning changes.

Downgrade drops the column and the table.

Revision ID: v2327floored
Revises: u2342reason
Create Date: 2026-11-14
"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "v2327floored"
down_revision = "u2342reason"
branch_labels = None
depends_on = None


def _has_table(name: str) -> bool:
    return sa.inspect(op.get_bind()).has_table(name)


def _has_column(table: str, column: str) -> bool:
    return column in {c["name"] for c in sa.inspect(op.get_bind()).get_columns(table)}


def upgrade() -> None:
    # Each step is skipped when its object is already there. A database built with
    # ``DatabaseConnection.create_tables()`` (the self-host wizard, and the
    # fresh-database test on a shared developer database) already has every model's
    # table, and a plain ``create_table`` then fails the whole upgrade with
    # DuplicateTable. That is what happened on the shared local database on
    # 2026-11-14 before this guard. The model and this migration define the same
    # table, so an existing one is left as it is.
    if not _has_table("floored_action_counts"):
        op.create_table(
            "floored_action_counts",
            sa.Column("name", sa.String(length=40), nullable=False),
            sa.Column("site", sa.String(length=64), nullable=False),
            sa.Column("day", sa.Date(), nullable=False),
            sa.Column("count", sa.Integer(), nullable=False, server_default="0"),
            sa.PrimaryKeyConstraint("name", "site", "day"),
        )
    if not _has_column("users", "ops_reader"):
        op.add_column(
            "users",
            sa.Column("ops_reader", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        )


def downgrade() -> None:
    if _has_column("users", "ops_reader"):
        op.drop_column("users", "ops_reader")
    if _has_table("floored_action_counts"):
        op.drop_table("floored_action_counts")
