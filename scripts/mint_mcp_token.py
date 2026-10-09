#!/usr/bin/env python
"""#1462 unit 1 — mint an MCP server access token for a single user.

Generates one cryptographically random bearer token (`mcp_` + 32 bytes
URL-safe random), stores ONLY its SHA-256 hash in `mcp_access_tokens`, and
prints the raw token to stdout exactly once — it is never written to this
table, a log line, a file, or an exception (services/mcp/server/identity.py
is the verifier that resolves it back to a user; it hashes-and-looks-up the
same way).

Trust-zone precedent (#1344, mint_invite_tokens.py): this script knows the
identity a token is FOR (unlike an invite token, which is identity-blind by
design) because an MCP token is bound to a real, already-existing user at
mint time — there is no anonymous-owner path anywhere in this credential's
lifecycle (Arch's #1462 condition 1). Delivery of the raw token is still
out-of-band exactly like an invite token: NEVER a mailbox memo, a GH comment,
or any git-tracked file — in-conversation or the gitignored roster only.

DRY-RUN by default; pass --apply to actually insert. Prefer running this via
scripts/mint_mcp_token.sh against PRODUCTION (fly ssh console, same idiom as
scripts/mint_prod_invite.sh) — running this file directly resolves the DB the
same way mint_invite_tokens.py does (app config first, POSTGRES_* env
fallback in dev only, REFUSED in production) and that resolution is the
easiest thing to get wrong from a bare worktree.

Usage:
    python scripts/mint_mcp_token.py --user-email a@b.com --label alpha-tester
    python scripts/mint_mcp_token.py --user-email a@b.com --label alpha-tester --expires-days 30 --apply
  (as deployed: python /app/scripts/mint_mcp_token.py ... — the root is put on sys.path below)
"""

import argparse
import hashlib
import os
import re
import secrets
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# CIO option 3 (2026-10-09): as deployed in /app this payload is the permission
# boundary for `fly ssh console -a piper-morgan -C "python /app/scripts/mint_mcp_token.py`
# — no shell, so the import root is file-relative here and every argument is
# validated before any database connection (_validate below).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dotenv import load_dotenv  # noqa: E402

load_dotenv("/Users/xian/Development/piper-morgan/piper-morgan-product/.env")
os.environ.setdefault("POSTGRES_PORT", "5433")
from sqlalchemy import create_engine, text  # noqa: E402

TOKEN_PREFIX = "mcp_"

_SELECT_USER_BY_EMAIL = text("SELECT id, email FROM users WHERE email = :email")
_SELECT_USER_BY_ID = text("SELECT id, email FROM users WHERE id = :user_id")
_INSERT = text(
    "INSERT INTO mcp_access_tokens (id, user_id, token_hash, label, created_at, expires_at) "
    "VALUES (:id, :user_id, :token_hash, :label, now(), :expires_at)"
)


from prod_db import _database_url, _redacted  # noqa: E402 — shared, side-effect free


def _engine():
    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    return create_engine(url)


def _mask(raw_token: str) -> str:
    return f"{TOKEN_PREFIX}…{raw_token[-4:]}"


_EMAIL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+\-]{0,63}@[A-Za-z0-9.\-]{1,190}")
# No spaces: under `fly ssh console -C` there is no shell, so a spaced label would
# arrive as extra argv and be refused anyway — say so up front instead.
_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:\-]{0,63}")
MAX_EXPIRES_DAYS = 365


def _validate(args) -> None:
    """Refuse anything outside this payload's one shape before any DB connection."""
    if args.user_email is not None and not _EMAIL.fullmatch(args.user_email):
        raise SystemExit("refusing: --user-email is not a plain address")
    if args.user_id is not None:
        try:
            uuid.UUID(args.user_id)
        except ValueError:
            raise SystemExit("refusing: --user-id is not a UUID") from None
    if not _LABEL.fullmatch(args.label or ""):
        raise SystemExit(
            "refusing: --label must start alphanumeric and use only [A-Za-z0-9._:-], max 64 (no spaces)"
        )
    if args.expires_days is not None and not 1 <= args.expires_days <= MAX_EXPIRES_DAYS:
        raise SystemExit(f"refusing: --expires-days must be 1..{MAX_EXPIRES_DAYS}")


def main() -> None:
    ap = argparse.ArgumentParser(description="#1462 unit 1 — mint an MCP access token")
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--user-email", help="mint for the user with this email")
    who.add_argument("--user-id", help="mint for the user with this UUID")
    ap.add_argument(
        "--label",
        required=True,
        help="short label, no spaces (e.g. alpha-tester.claude-desktop)",
    )
    ap.add_argument(
        "--expires-days",
        type=int,
        default=None,
        help="token expires N days from now (default: never)",
    )
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()
    _validate(args)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== #1462 mint MCP access token {mode} ===")

    # Generated up front, held only in this process's memory — never printed
    # or logged before the insert (if any) has actually succeeded.
    raw_token = TOKEN_PREFIX + secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expires_at = (
        datetime.now(timezone.utc) + timedelta(days=args.expires_days)
        if args.expires_days is not None
        else None
    )

    eng = _engine()
    with eng.begin() as c:
        if args.user_email:
            row = c.execute(_SELECT_USER_BY_EMAIL, {"email": args.user_email}).first()
            target = args.user_email
        else:
            row = c.execute(_SELECT_USER_BY_ID, {"user_id": args.user_id}).first()
            target = args.user_id

        if row is None:
            raise SystemExit(
                f"No such user: {target} — refusing to mint against a nonexistent owner "
                "(there is no default/anonymous owner for an MCP token)."
            )

        user_id, email = row[0], row[1]
        print(f"--- user: {email} ({user_id})")
        print(f"--- label: {args.label}")
        print(f"--- expires: {expires_at.isoformat() if expires_at else 'never'}")

        if not args.apply:
            print("DRY-RUN complete — no writes. Re-run with --apply (same args) to insert.")
            return

        token_id = uuid.uuid4()
        c.execute(
            _INSERT,
            {
                "id": str(token_id),
                "user_id": str(user_id),
                "token_hash": token_hash,
                "label": args.label,
                "expires_at": expires_at,
            },
        )

    print("Inserted 1 MCP access token.")
    print()
    print("RAW TOKEN — shown ONCE below. Save it now; it will not be shown again,")
    print("and it is not recoverable from the database (only its hash is stored).")
    print(raw_token)
    print()
    print(f"Masked reference (safe to log or paste): {_mask(raw_token)}")
    print(
        "Deliver this raw token the way an invite token is delivered (#1344): "
        "NEVER in a mailbox memo, GH comment, or any git-tracked file — "
        "in-conversation or the gitignored roster only."
    )


if __name__ == "__main__":
    main()
