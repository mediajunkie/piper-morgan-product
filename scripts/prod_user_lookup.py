#!/usr/bin/env python3
"""prod_user_lookup.py — READ-ONLY, masked lookup of Piper user accounts in PRODUCTION.

Why (PM 2026-10-09: "not clear to me why these aren't things agents can do
themselves"; yes "once Arch and HOST have reviewed the script, allow HOST's
seat to run it"). Account questions ("does Janne have an account?", "who is
sachio222?") routed through PM's own hands because no seat may read the
production database.

THE BOUNDARY IS THIS FILE IN THE DEPLOYED IMAGE (CIO 2026-10-09, option 3):
the permission rule names the production command itself —
    fly ssh console -a piper-morgan -C "python /app/scripts/prod_user_lookup.py
— with NO ``/bin/sh -c`` wrapper. ``fly ssh console -C`` fork-execs directly, so
anything after the allowed prefix arrives here as argv, never as shell; and what
runs is the reviewed copy in ``/app``, which only a deploy can change. A local
edit to this file changes nothing in production. So everything that limits the
command lives HERE: the import path, the input allowlist, READ ONLY, and the
masked, fixed column set.

Returns, and nothing else:
  username · email MASKED (first character + "…@" + domain) · is_active ·
  setup_complete · created_at · last_login_at
Never: ids, password hashes, preferences, roles, any other table.

Usage:
  python /app/scripts/prod_user_lookup.py <username-or-email>
  python /app/scripts/prod_user_lookup.py --all      # every account, same masked columns
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Replaces PYTHONPATH=/app (there is no shell to set it in). File-relative, so in
# the image this resolves to /app, and locally to the checkout — same code path.
_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "scripts"))

# First character alphanumeric: nothing that could read as a flag reaches the query.
_SAFE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9@._+\-]{0,253}$")
_COLUMNS = "username, email, is_active, setup_complete, created_at, last_login_at"
_USAGE = "usage: prod_user_lookup.py <username-or-email> | --all"


def mask_email(email: str) -> str:
    """'janne@example.com' -> 'j…@example.com'. Never more of the local part than one character."""
    if not email or "@" not in email:
        return "(none)"
    local, _, domain = email.partition("@")
    return f"{local[:1]}…@{domain}"


def parse_args(argv: list[str]) -> str:
    """Exactly one argument: '--all', or one identifier from the safe charset.
    Anything else (extra args, flags, odd characters) is refused before any
    database connection is made."""
    if len(argv) != 1:
        raise SystemExit(_USAGE)
    arg = argv[0]
    if arg == "--all":
        return arg
    if not _SAFE.match(arg):
        raise SystemExit(
            "refusing: identifier must start with a letter or digit and use only [A-Za-z0-9@._+-]"
        )
    return arg


def _fmt(row) -> str:
    username, email, active, setup, created, last_login = row
    return (
        f"username={username} · email={mask_email(email)} · active={active} · "
        f"setup_complete={setup} · created_at={created} · last_login_at={last_login}"
    )


def main(argv: list[str]) -> int:
    who = parse_args(argv)

    # The mint's reviewed production-DB resolution (app config; refuses the
    # localhost fallback in production).
    from mint_invite_tokens import _database_url, _redacted
    from sqlalchemy import create_engine, text

    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})  [READ ONLY]")
    engine = create_engine(url)
    with engine.connect() as conn:
        conn.execute(text("SET TRANSACTION READ ONLY"))
        if who == "--all":
            rows = conn.execute(
                text(f"SELECT {_COLUMNS} FROM users ORDER BY created_at")
            ).fetchall()
            print(f"accounts: {len(rows)}")
        else:
            rows = conn.execute(
                text(
                    f"SELECT {_COLUMNS} FROM users "
                    "WHERE lower(username) = lower(:w) OR lower(email) = lower(:w)"
                ),
                {"w": who},
            ).fetchall()
            print(f"match: {'yes' if rows else 'no'} ({len(rows)})")
        for row in rows:
            print(_fmt(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
