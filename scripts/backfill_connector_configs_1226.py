#!/usr/bin/env python
"""WS-1 (#1226 / #1199) P3a — backfill the flat github_preferences.json into connector_configs.

Seeds the DB-backed store (ADR-070 D4) from the live flat file so the migrated readers
(repo_resolver, standup) see the existing values without requiring a re-save in the settings
UI. The whole per-user blob is copied (default_repository + selected_repositories +
github_username — every field the flat readers consult), keyed by owner_id.

WS-9 identity: maps the collapsed xian id (a25db09c) -> the canonical m1-test id (009afc8c)
so both flat-file entries land on the single settled identity. Idempotent (ON CONFLICT
upsert on the unique(owner_id, connector)). DRY-RUN by default; pass --apply to execute.

NOTE: explicit .env path (find_dotenv() crashes when the interpreter frame is ambiguous —
hit repeatedly this sprint); explicit CAST()s because the bound params are Python strings.
"""
import argparse
import json
import os

from dotenv import load_dotenv

load_dotenv("/Users/xian/Development/piper-morgan/piper-morgan-product/.env")
os.environ.setdefault("POSTGRES_PORT", "5433")
from sqlalchemy import create_engine, text  # noqa: E402

PREFS_FILE = "data/github_preferences.json"
# WS-9 collapse map: xian -> m1-test (canonical). Unlisted keys map to themselves.
COLLAPSE = {"a25db09c-6d79-41e4-8d82-87b6a005bbb0": "009afc8c-bbb0-4391-8265-1575c0812949"}

_UPSERT = text(
    "INSERT INTO connector_configs (id, owner_id, connector, config, created_at, updated_at) "
    "VALUES (gen_random_uuid(), CAST(:owner AS uuid), 'github', CAST(:cfg AS jsonb), now(), now()) "
    "ON CONFLICT (owner_id, connector) DO UPDATE SET config = EXCLUDED.config, updated_at = now()"
)


def _engine():
    u = os.getenv("POSTGRES_USER", "piper")
    p = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    h = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "piper_morgan")
    return create_engine(f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{db}")


def main():
    ap = argparse.ArgumentParser(description="WS-1 backfill github prefs -> connector_configs")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    apply = ap.parse_args().apply

    if not os.path.exists(PREFS_FILE):
        print(f"No {PREFS_FILE} — nothing to backfill.")
        return
    with open(PREFS_FILE) as f:
        prefs = json.load(f)

    # collapse-map + merge per canonical owner (last write wins; identical values here)
    merged = {}
    for key, cfg in prefs.items():
        owner = COLLAPSE.get(key, key)
        merged.setdefault(owner, {}).update(cfg or {})

    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== WS-1 backfill {mode}: {len(prefs)} json keys -> {len(merged)} owner(s) ===")
    eng = _engine()
    with eng.begin() as c:  # one txn; dry-run runs only the post-state SELECT
        for owner, cfg in merged.items():
            print(f"  owner {owner}: github <- {cfg} [{mode}]")
            if apply:
                c.execute(_UPSERT, {"owner": owner, "cfg": json.dumps(cfg)})
        print("--- post-state: connector_configs github rows ---")
        rows = c.execute(
            text(
                "SELECT CAST(owner_id AS text), config FROM connector_configs "
                "WHERE connector='github' ORDER BY owner_id"
            )
        )
        for owner_id, config in rows:
            print(f"  {owner_id}: {config}")
    if not apply:
        print("DRY-RUN complete — no writes. Re-run with --apply to execute.")


if __name__ == "__main__":
    main()
