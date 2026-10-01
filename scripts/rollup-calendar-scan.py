#!/usr/bin/env python3
"""Scan the editorial calendar for published-but-unsyndicated posts.

Standing Exec rollup check, adopted 2026-09-29 after PM found a ~7-week-old
unsyndicated post that neither the rollup nor Docs's process had surfaced.
Written down 2026-10-01 because it had been living in my head and getting
re-typed at each build, which is how its exclusion logic drifted.

A hit means: a post went out, its expected syndication leg has no URL
recorded, and nobody has ruled on it. That is an attention item for PM.

Exclusions, each for a stated reason:
  * terminal statuses -- `distributed` (both legs ran) and `not-syndicated`
    (PM ruled it locked: neither crossposted nor pending, 2026-10-01).
    Only PM writes `not-syndicated`, per that ruling.
  * pre-tracking-era rows -- no pubDate AND no blogURL means there is no
    live post to point at and nothing to syndicate. Deliberately left blank
    rather than fabricated; see Docs 2026-09-30 on "15 Sessions, Fast
    Recovery".

Syndication target depends on category: Ships go to LinkedIn, everything
else to Medium (reference_syndication_targets_by_category).
"""
import csv
import pathlib
import sys

CALENDAR = pathlib.Path(__file__).resolve().parents[1] / (
    "docs/internal/planning/comms/editorial-calendar.csv"
)
TERMINAL = {"distributed", "not-syndicated"}


def expected_leg(row):
    """Which URL column should be filled once this post is syndicated."""
    return "linkedinURL" if "ship" in row["theme"].strip().lower() else "mediumURL"


def scan(rows):
    hits, skipped = [], []
    for row in rows:
        status = row["status"].strip().lower()
        if status != "published":
            if status in TERMINAL:
                skipped.append((row["title"], f"terminal status '{status}'"))
            continue
        if not row["pubDate"].strip() and not row["blogURL"].strip():
            skipped.append((row["title"], "pre-tracking-era row, nothing to point at"))
            continue
        leg = expected_leg(row)
        if not row[leg].strip():
            hits.append((row["title"], row["pubDate"].strip() or "no pubDate", leg))
    return hits, skipped


def main():
    verbose = "-v" in sys.argv
    with CALENDAR.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    hits, skipped = scan(rows)

    print(f"scanned {len(rows)} calendar rows from {CALENDAR.name}")
    if verbose:
        for title, why in skipped:
            print(f"  skipped: {title[:50]} -- {why}")

    if not hits:
        print(f"no unsyndicated published posts ({len(skipped)} row(s) excluded by rule)")
        return 0

    print(f"\n{len(hits)} published post(s) with no syndication URL recorded:")
    for title, pub, leg in hits:
        print(f"  {pub}  {title[:52]}  (empty {leg})")
    print("\nEach is either a record gap (the crosspost ran, the URL was never")
    print("logged) or a real one. Route to Docs to determine which -- do not")
    print("guess from the symptom, and do not mark anything not-syndicated")
    print("without PM saying so for that specific post.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
