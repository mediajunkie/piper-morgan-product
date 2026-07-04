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


def _engine():
    u = os.getenv("POSTGRES_USER", "piper")
    p = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    h = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "piper_morgan")
    return create_engine(f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{db}")


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
            for token in tokens:
                c.execute(_INSERT, {"token": token})
    for token in tokens:
        print(token)
    if not args.apply:
        print("DRY-RUN complete — no writes. Re-run with --apply to insert these into invite_tokens.")
    else:
        print(f"Inserted {len(tokens)} token(s). Hand these to HOST for the roster.")


if __name__ == "__main__":
    main()
