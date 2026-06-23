#!/usr/bin/env python
"""WS-9 collapse (#1233 / RECONNECT Phase-1 P0) — unify PM's two test identities into one
canonical owner_id, settling the FK target for WS-1.

Context: PM is the sole human on this DB (PM-confirmed 2026-06-21). `m1-test` (009afc8c,
47 convs) is the active/canonical identity; `xian` (a25db09c, 1 conv) is a stray test record
with the same human behind it. This re-points xian's scattered content to m1-test, deletes
stale ancillary rows, and LEAVES audit history intact.

Collision analysis (verified 2026-06-21): every affected table is PK-on-`id` (re-pointing the
owner column never collides on the PK). The only extra unique is `projects(owner_id, name)` →
on a name clash we keep the canonical row + drop xian's. `user_trust_profiles` has NO
user_id-unique → we delete xian's stale row rather than create a duplicate.

DRY-RUN by default (no writes). Pass --apply to execute (single transaction). Idempotent:
re-running after apply finds 0 xian rows and is a no-op. The xian users row is LEFT as a
tombstone (audit_logs still references it; WS-1 simply anchors to m1-test).
"""
import argparse
import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
os.environ.setdefault("POSTGRES_PORT", "5433")
from sqlalchemy import create_engine, text  # noqa: E402

CANON = "009afc8c-bbb0-4391-8265-1575c0812949"  # m1-test (keep)
MERGE = "a25db09c-6d79-41e4-8d82-87b6a005bbb0"  # xian (collapse into canonical)

# (table, owner-column, action): repoint | repoint_projects | delete | leave
PLAN = [
    ("conversations", "user_id", "repoint"),
    ("documents", "owner_id", "repoint"),
    ("learned_patterns", "user_id", "repoint"),
    ("lists", "owner_id", "repoint"),
    ("projects", "owner_id", "repoint_projects"),   # UNIQUE(owner_id,name): keep canonical on clash
    ("user_trust_profiles", "user_id", "delete"),   # no user_id-unique → delete stale, don't dup
    ("token_blacklist", "user_id", "delete"),       # logout artifact — meaningless to re-point
    ("audit_logs", "user_id", "leave"),             # history integrity — do not rewrite
]


def _engine():
    u = os.getenv("POSTGRES_USER", "piper")
    p = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    h = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "piper_morgan")
    return create_engine(f"postgresql+psycopg2://{u}:{p}@{h}:{port}/{db}")


def _count(c, table, col, owner):
    return c.execute(
        text(f'SELECT COUNT(*) FROM "{table}" WHERE CAST("{col}" AS text) = :o'), {"o": owner}
    ).scalar()


def main():
    ap = argparse.ArgumentParser(description="WS-9 identity collapse (xian -> m1-test)")
    ap.add_argument("--apply", action="store_true", help="execute (default: dry-run)")
    apply = ap.parse_args().apply

    eng = _engine()
    mode = "APPLY" if apply else "DRY-RUN"
    print(f"=== WS-9 collapse {mode}: xian {MERGE} -> m1-test {CANON} ===")
    with eng.begin() as c:  # one transaction; in dry-run only SELECTs run -> empty commit
        for table, col, action in PLAN:
            n = _count(c, table, col, MERGE)
            if action == "leave":
                print(f"  {table}.{col}: {n} -> LEAVE (history)")
                continue
            if n == 0:
                print(f"  {table}.{col}: 0 -> nothing (idempotent)")
                continue
            if action == "repoint":
                if apply:
                    c.execute(
                        text(f'UPDATE "{table}" SET "{col}" = :c WHERE CAST("{col}" AS text) = :m'),
                        {"c": CANON, "m": MERGE},
                    )
                print(f"  {table}.{col}: {n} -> re-point to canonical [{mode}]")
            elif action == "repoint_projects":
                if apply:
                    # drop xian's project rows that would clash on (owner_id, name) with canonical
                    c.execute(
                        text(
                            "DELETE FROM projects p WHERE CAST(p.owner_id AS text) = :m AND EXISTS "
                            "(SELECT 1 FROM projects q WHERE CAST(q.owner_id AS text) = :c AND q.name = p.name)"
                        ),
                        {"m": MERGE, "c": CANON},
                    )
                    c.execute(
                        text("UPDATE projects SET owner_id = :c WHERE CAST(owner_id AS text) = :m"),
                        {"c": CANON, "m": MERGE},
                    )
                print(f"  projects.owner_id: {n} -> re-point (delete-on-name-clash) [{mode}]")
            elif action == "delete":
                if apply:
                    c.execute(
                        text(f'DELETE FROM "{table}" WHERE CAST("{col}" AS text) = :m'), {"m": MERGE}
                    )
                print(f"  {table}.{col}: {n} -> DELETE stale [{mode}]")

        # post-state (within the txn so APPLY shows the result before commit)
        print("--- post-state: xian residual rows (audit_logs expected to remain) ---")
        for table, col, _ in PLAN:
            print(f"  {table}.{col}: {_count(c, table, col, MERGE)}")
    if not apply:
        print("DRY-RUN complete — no changes written. Re-run with --apply to execute.")


if __name__ == "__main__":
    main()
