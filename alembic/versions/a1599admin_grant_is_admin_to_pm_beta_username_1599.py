"""Grant is_admin to PM's beta account, username dinp (#1599) — fail-loud, never a silent no-op.

#1599's root cause: migration cd320b81e4c6 targeted `xian@example.com`, a
placeholder that matched nothing, and the zero-row UPDATE succeeded silently.
Months later every route gated on `require_admin` 403'd everyone, including
the only user who mattered, and nothing had ever said so.

This migration encodes that lesson structurally: **a grant that matches zero
rows raises**, failing the release loudly at deploy time instead of shipping
an invisible no-op. (m-44: an all-clear that measured nothing must not look
like success.)

PM ruling (relayed by Janus, 2026-08-12 ~8:50 PT, recorded on #1599): proper
migration, not a one-off psql grant. PM confirmed in-conversation 2026-08-12:
the beta login is USERNAME-based and the account is username 'dinp' (email
was the wrong key to ask about — the UI doesn't use it to log in). The
username column carries a UNIQUE index, so it identifies exactly one row.
PM's stated future plan, recorded on the issue and deliberately NOT built
here: a separate real/admin account (username 'xian', xian@pipermorgan.ai)
at production time, distinct from the alpha/beta test accounts.

Revision ID: a1599admin
Revises: l1466slack
Create Date: 2026-08-12
"""

import os

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a1599admin"
down_revision = "l1466slack"
branch_labels = None
depends_on = None

# PM's real beta login, confirmed by PM in-conversation 2026-08-12 (username,
# not email — the login UI is username-based). Module constant, not
# env-derived: a migration must be deterministic and reviewable.
PM_ADMIN_USERNAME = "dinp"


def upgrade() -> None:
    """Set is_admin on PM's account; refuse to succeed if nothing matched.

    The zero-row check is STRICT only where the account must exist: the Fly
    release environment (FLY_APP_NAME is set on release machines). On dev
    and CI Postgres — fresh databases where PM's account legitimately does
    not exist (the Security Test Suite runs `alembic upgrade head` from
    scratch) — the grant is a warned no-op, never a failure. The mutation is
    identical everywhere; only the assertion's strictness is env-keyed.
    """
    result = op.get_bind().execute(
        sa.text("UPDATE users SET is_admin = true WHERE username = :username"),
        {"username": PM_ADMIN_USERNAME},
    )
    if result.rowcount == 0:
        msg = (
            f"#1599 admin grant matched ZERO rows for username {PM_ADMIN_USERNAME!r}. "
            "A placeholder address matching nothing and succeeding anyway is "
            "the exact failure this migration exists to fix."
        )
        if os.environ.get("FLY_APP_NAME"):
            raise RuntimeError(
                msg + " Refusing to no-op silently on a production release: "
                "either the username is wrong or the account does not exist; "
                "fix the constant or create the account, then redeploy."
            )
        print(f"WARNING (non-release environment, expected on fresh DBs): {msg}")


def downgrade() -> None:
    op.get_bind().execute(
        sa.text("UPDATE users SET is_admin = false WHERE username = :username"),
        {"username": PM_ADMIN_USERNAME},
    )
