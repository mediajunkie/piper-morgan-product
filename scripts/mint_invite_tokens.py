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
import sys
from pathlib import Path

# CIO option 3 (2026-10-09): this payload, as deployed in /app, is the permission
# boundary for `fly ssh console -a piper-morgan -C "python /app/scripts/mint_invite_tokens.py`
# — there is no shell to set PYTHONPATH, so the root is put on sys.path here
# (file-relative: /app in the image, the checkout locally), and every argument is
# validated below before any database connection.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv  # noqa: E402

load_dotenv("/Users/xian/Development/piper-morgan/piper-morgan-product/.env")
os.environ.setdefault("POSTGRES_PORT", "5433")
from sqlalchemy import create_engine, text  # noqa: E402

from services.auth.invite_token_service import generate_invite_token  # noqa: E402

_INSERT = text("INSERT INTO invite_tokens (token, created_at) VALUES (:token, now())")


from prod_db import (  # noqa: E402,F401 — shared, side-effect free
    _database_url,
    _redacted,
    _to_sync_url,
)


def _engine():
    url, source = _database_url()
    print(f"--- target: {_redacted(url)}  (resolved via {source})")
    return create_engine(url)


MAX_COUNT = 20  # the wrapper's old bound, now enforced by the payload itself


def _validate(args) -> None:
    """Refuse anything outside the one shape this payload exists for (a mint
    count 1..MAX_COUNT) before any DB connection. Burning lives in its own
    payload, burn_invite_tokens.py (Arch 2026-10-09: one grant per effect class —
    this payload only CREATES rows)."""
    if not 1 <= args.count <= MAX_COUNT:
        raise SystemExit(f"refusing: count must be 1..{MAX_COUNT}")


def main():
    ap = argparse.ArgumentParser(description="#1344 mint alpha invite tokens")
    ap.add_argument("count", type=int, nargs="?", default=0, help="how many tokens to mint")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    args = ap.parse_args()
    _validate(args)

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
