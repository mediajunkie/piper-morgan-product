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

Usage (run from the repo root; needs PYTHONPATH=. for the services.* imports):
    PYTHONPATH=. python scripts/mint_mcp_token.py --user-email a@b.com --label "alpha tester"
    PYTHONPATH=. python scripts/mint_mcp_token.py --user-email a@b.com --label "..." --expires-days 30 --apply
"""

import argparse
import hashlib
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

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


def _to_sync_url(url: str) -> str:
    """Same conversion as mint_invite_tokens.py — duplicated rather than
    imported so this script has no import-time dependency on that sibling.

    Two independent differences, both of which bite:
      * driver token: ``postgresql+asyncpg://`` -> ``postgresql://``
      * TLS spelling: asyncpg's ``?ssl=X`` -> libpq's ``?sslmode=X``
    """
    from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit  # noqa: PLC0415

    parts = urlsplit(url.replace("+asyncpg", ""))
    q = [(("sslmode" if k == "ssl" else k), v) for k, v in parse_qsl(parts.query)]
    return urlunsplit(parts._replace(query=urlencode(q)))


def _database_url() -> tuple[str, str]:
    """Resolve the DB URL the way the APP does, falling back to POSTGRES_*.

    Identical shape to mint_invite_tokens.py's _database_url() — see that
    script for the full rationale (app-config-first, dev-only POSTGRES_*
    fallback, REFUSE in production rather than silently mint against
    localhost). Duplicated, not imported, so this script has no import-time
    coupling to the invite-token sibling.
    """
    try:
        from services.database.connection import db  # noqa: PLC0415

        url = db._build_database_url()
        return _to_sync_url(url), "app config (services.database.connection)"
    except Exception as exc:  # noqa: BLE001 — fall back LOUDLY, never silently
        print(f"!!! app-config DB resolution FAILED: {type(exc).__name__}: {exc}")
        if os.getenv("PIPER_ENVIRONMENT", "").lower() == "production":
            raise SystemExit(
                "REFUSING to fall back to POSTGRES_* defaults in production — "
                "that path points at localhost and would mint an unusable token. "
                "Fix the resolution error above instead."
            ) from exc
        print("!!! falling back to POSTGRES_* env (dev-only path)")
        u = os.getenv("POSTGRES_USER", "piper")
        p = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
        h = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5433")
        d = os.getenv("POSTGRES_DB", "piper_morgan")
        return (
            f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{d}",
            "POSTGRES_* env fallback",
        )


def _redacted(url: str) -> str:
    """host:port/db only — never the password, this gets printed."""
    tail = url.rsplit("@", 1)[-1]
    return tail if "@" not in url else tail


def _engine():
    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    return create_engine(url)


def _mask(raw_token: str) -> str:
    return f"{TOKEN_PREFIX}…{raw_token[-4:]}"


def main() -> None:
    ap = argparse.ArgumentParser(description="#1462 unit 1 — mint an MCP access token")
    who = ap.add_mutually_exclusive_group(required=True)
    who.add_argument("--user-email", help="mint for the user with this email")
    who.add_argument("--user-id", help="mint for the user with this UUID")
    ap.add_argument(
        "--label",
        required=True,
        help="short human label for this token (e.g. 'alpha tester — claude desktop')",
    )
    ap.add_argument(
        "--expires-days",
        type=int,
        default=None,
        help="token expires N days from now (default: never)",
    )
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()

    if args.expires_days is not None and args.expires_days < 1:
        raise SystemExit("--expires-days must be >= 1")

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
