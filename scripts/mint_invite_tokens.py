#!/usr/bin/env python
"""#1344 — mint a batch of alpha invite tokens.

Generates N tokens (services.auth.invite_token_service — same Crockford Base32
generator the app validates against) and inserts them into invite_tokens.
Prints the raw strings so HOST can record them against tester identities in the
gitignored roster (dev/alpha/alpha-tester-roster.md) — this script has no
knowledge of identities, only tokens (trust-zone separation, #1344).

DRY-RUN by default; pass --apply to actually insert. Idempotent by construction
(each token is freshly random; a collision against an existing token is
astronomically unlikely at 24 Crockford-Base32 chars, but the INSERT would
simply fail on the primary-key conflict rather than silently overwrite).

Usage (run from the repo root; needs PYTHONPATH=. for the services.* imports):
    PYTHONPATH=. python scripts/mint_invite_tokens.py 5           # dry-run, shows 5 tokens
    PYTHONPATH=. python scripts/mint_invite_tokens.py 5 --apply   # actually inserts them
"""

import argparse
import os

from dotenv import load_dotenv

load_dotenv("/Users/xian/Development/piper-morgan/piper-morgan-product/.env")
os.environ.setdefault("POSTGRES_PORT", "5433")
from sqlalchemy import create_engine, text  # noqa: E402

from services.auth.invite_token_service import generate_invite_token  # noqa: E402

_INSERT = text("INSERT INTO invite_tokens (token, created_at) VALUES (:token, now())")


def _database_url() -> tuple[str, str]:
    """Resolve the DB URL the way the APP does, falling back to POSTGRES_*.

    Returns (url, source) — source is printed so the operator always sees which
    database is about to be written to.

    Why this isn't just the POSTGRES_* construction it used to be: those
    defaults point at localhost:5433, i.e. the DEV database. Run from a
    worktree that is correct; run anywhere else it silently mints tokens the
    alpha tester cannot use, and the output looks identical to success. The
    2026-07 batch worked around this with a throwaway script that called
    ``db._build_database_url()``; doing it here instead means there is one
    mint path and it is right in both environments.
    """
    try:
        from services.database.connection import db  # noqa: PLC0415

        url = db._build_database_url()
        # The app speaks asyncpg; this script is sync.
        return url.replace("+asyncpg", ""), "app config (services.database.connection)"
    except Exception:  # noqa: BLE001 — fall back, but say so
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


def main():
    ap = argparse.ArgumentParser(description="#1344 mint alpha invite tokens")
    ap.add_argument("count", type=int, help="how many tokens to mint")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()

    if args.count < 1:
        raise SystemExit("count must be >= 1")

    tokens = [generate_invite_token() for _ in range(args.count)]

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== #1344 mint {mode}: {args.count} token(s) ===")
    if args.apply:
        eng = _engine()
        with eng.begin() as c:
            before = c.execute(text("SELECT count(*) FROM invite_tokens")).scalar()
            for token in tokens:
                c.execute(_INSERT, {"token": token})
            after = c.execute(text("SELECT count(*) FROM invite_tokens")).scalar()
        # The mint and its verification in one transaction — an inserted-count
        # that doesn't match the requested count is visible immediately rather
        # than discovered when a tester's code fails.
        print(f"--- rows: {before} -> {after} (expected +{args.count})")
        if after - before != args.count:
            raise SystemExit(
                f"MINT VERIFICATION FAILED: {after - before} rows added, expected {args.count}"
            )
    for token in tokens:
        print(token)
    if not args.apply:
        print(
            "DRY-RUN complete — no writes. Re-run with --apply to insert these into invite_tokens."
        )
    else:
        print(f"Inserted {len(tokens)} token(s). Hand these to HOST for the roster.")


if __name__ == "__main__":
    main()
