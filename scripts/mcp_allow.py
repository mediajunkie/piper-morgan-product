#!/usr/bin/env python3
"""#2242 — the ONE writer of the hosted-MCP allowlist.

Who may connect the hosted MCP (``piper-morgan-mcp``) until the Claude connector
is offered is a reserved key in ``users.preferences`` (see
``services/mcp/server/allowlist.py`` for the rule, the three gate points and why
nothing else may write the key). This script is the only thing that sets or
clears it; an enforcement pin keeps it that way.

    python scripts/mcp_allow.py list
    python scripts/mcp_allow.py add    --user-email someone@example.com          # dry-run
    python scripts/mcp_allow.py add    --user-email someone@example.com --apply
    python scripts/mcp_allow.py remove --user-id <uuid> --apply

Writes are atomic JSONB updates (``||`` and ``-``), never a read-modify-write of
the whole dict, so this script cannot drop another writer's keys. The reverse
race (a user-side read-modify-write dropping this key) loses in the closed
direction; ``add`` prints the list it re-reads after writing, and ``list`` is
how an operator checks what actually stuck (Arch's condition 3).

Same shape as ``mint_mcp_token.py``: dry-run by default, ``--apply`` to write,
the target database printed (redacted) before anything happens, and a refusal
rather than a silent fallback when the app's DB config cannot be resolved in
production (``prod_db._database_url``).
"""

from __future__ import annotations

import argparse
import re
import sys
import uuid
from pathlib import Path

# Importable as a module from tests (sys.path insert, like mint_invite_tokens.py)
# and runnable from any cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from sqlalchemy import create_engine, text  # noqa: E402

from services.mcp.server.allowlist import MCP_ALLOW_KEY  # noqa: E402

_EMAIL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+\-]{0,63}@[A-Za-z0-9.\-]{1,190}")

_SELECT_USER_BY_EMAIL = text("SELECT id, email, username FROM users WHERE email = :email")
_SELECT_USER_BY_ID = text("SELECT id, email, username FROM users WHERE id = :user_id")
# The list: accounts whose flag is JSON true (the predicate's own strictness).
_SELECT_LISTED = text(
    "SELECT id, email, username FROM users " "WHERE preferences ->> :key = 'true' ORDER BY email"
)
# Atomic: set the one key, keep every other key as it is.
_ADD = text(
    "UPDATE users SET preferences = coalesce(preferences, '{}'::jsonb) "
    "|| jsonb_build_object(:key, true) WHERE id = :user_id"
)
# Atomic: drop the one key, keep every other key as it is.
_REMOVE = text("UPDATE users SET preferences = preferences - :key WHERE id = :user_id")


def _engine():
    from prod_db import _database_url, _redacted  # shared, side-effect free

    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    return create_engine(url)


def _validate(args) -> None:
    """Refuse anything outside the payload's one shape before any DB connection."""
    if args.command not in ("add", "remove", "list"):
        raise SystemExit("refusing: command must be add, remove or list")
    if args.command == "list":
        if getattr(args, "user_email", None) or getattr(args, "user_id", None):
            raise SystemExit("refusing: list takes no user")
        return
    email = getattr(args, "user_email", None)
    user_id = getattr(args, "user_id", None)
    if bool(email) == bool(user_id):
        raise SystemExit("refusing: give exactly one of --user-email or --user-id")
    if email is not None and not _EMAIL.fullmatch(email):
        raise SystemExit("refusing: --user-email is not a plain address")
    if user_id is not None:
        try:
            uuid.UUID(user_id)
        except ValueError:
            raise SystemExit("refusing: --user-id is not a UUID") from None


def listed(conn) -> list[tuple[str, str, str]]:
    """Every listed account as ``(id, email, username)``, re-read from the table."""
    rows = conn.execute(_SELECT_LISTED, {"key": MCP_ALLOW_KEY}).fetchall()
    return [(str(r[0]), r[1] or "", r[2] or "") for r in rows]


def print_listed(conn) -> None:
    rows = listed(conn)
    print(f"--- listed: {len(rows)}")
    for user_id, email, username in rows:
        print(f"    {email}  {username}  ({user_id})")


def resolve_user(conn, *, user_email: str | None, user_id: str | None):
    if user_email:
        row = conn.execute(_SELECT_USER_BY_EMAIL, {"email": user_email}).first()
        target = user_email
    else:
        row = conn.execute(_SELECT_USER_BY_ID, {"user_id": user_id}).first()
        target = user_id
    if row is None:
        raise SystemExit(f"No such user: {target} — nothing written.")
    return str(row[0]), row[1], row[2]


def add(conn, user_id: str) -> None:
    conn.execute(_ADD, {"key": MCP_ALLOW_KEY, "user_id": user_id})
    # Arch's condition 3: re-read after the write so the operator sees what stuck.
    print_listed(conn)


def remove(conn, user_id: str) -> None:
    conn.execute(_REMOVE, {"key": MCP_ALLOW_KEY, "user_id": user_id})
    print_listed(conn)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="#2242 — the hosted-MCP allowlist (the one writer)")
    sub = ap.add_subparsers(dest="command", required=True)
    for name in ("add", "remove"):
        p = sub.add_parser(name)
        who = p.add_mutually_exclusive_group(required=True)
        who.add_argument("--user-email")
        who.add_argument("--user-id")
        p.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    sub.add_parser("list")
    args = ap.parse_args(argv)
    _validate(args)

    eng = _engine()
    if args.command == "list":
        with eng.begin() as c:
            print_listed(c)
        return

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== #2242 mcp_allow {args.command} {mode} ===")
    with eng.begin() as c:
        user_id, email, username = resolve_user(c, user_email=args.user_email, user_id=args.user_id)
        print(f"--- user: {email}  {username}  ({user_id})")
        print_listed(c)
        if not args.apply:
            print("DRY-RUN complete — no writes. Re-run with --apply (same args) to write.")
            return
        if args.command == "add":
            add(c, user_id)
        else:
            remove(c, user_id)
    print(f"{args.command}: done for {email} ({user_id}).")


if __name__ == "__main__":
    main()
