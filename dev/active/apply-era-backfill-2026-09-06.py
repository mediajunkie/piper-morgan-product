#!/usr/bin/env python3
"""Apply Comms' verified era-backfill mapping to blog-metadata.csv's cluster column.

Source: dev/active/era-backfill-2026-09-06.csv (Comms, verified independently by Web
against publishedAt against episodes.ts's 7 era ranges -- 0 ambiguous, exact match
against all 101 already-correctly-clustered posts).

Deliberately skips weekly-ship-44 (not present in blog-metadata.csv -- a separate,
genuine duplicate-JSON-entry bug, filed distinctly, not conflated with this fix).
"""
import csv

BACKFILL_CSV = "/Users/xian/Development/piper-morgan-worktrees/web/dev/active/era-backfill-2026-09-06.csv"
METADATA_CSV = "/Users/xian/Development/piper-morgan-website-worktrees/web/data/blog-metadata.csv"

backfill = {}
with open(BACKFILL_CSV, newline="") as f:
    for row in csv.DictReader(f):
        backfill[row["slug"]] = row["new_cluster"]

with open(METADATA_CSV, newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = 0
unmatched = set(backfill.keys())
for row in rows:
    slug = row["slug"]
    if slug in backfill:
        unmatched.discard(slug)
        new_cluster = backfill[slug]
        if row["cluster"] != new_cluster:
            row["cluster"] = new_cluster
            changed += 1

with open(METADATA_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"rows changed: {changed}")
print(f"total rows written: {len(rows)}")
print(f"backfill slugs not found in blog-metadata.csv (expected: weekly-ship-44): {sorted(unmatched)}")
