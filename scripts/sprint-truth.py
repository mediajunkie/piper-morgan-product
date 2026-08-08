#!/usr/bin/env python3
"""sprint-truth.py — print the sprint/milestone state from GitHub, with the denominator stated.

WHY THIS EXISTS
---------------
The cohort has repeatedly reported a sprint "complete" while items in it had not been
started. Every instance was the same defect: a TRUE statement about a SUBSET, phrased as
if it were about the whole. "The build queue is empty" is true and does not mean the
sprint is done — it silently excludes Sprint Backlog (never started), Blocked, and
In Review (awaiting verification, usually PM's).

PM, 2026-08-08: "We keep over-reporting completeness on the beta blocker track by
mistaking the denominator... It is not great that I am the only entity on this team with
an accurate sense of what is in this sprint."

So this prints the breakdown, never a single number, and refuses to print a total without
its parts. GitHub is the source of truth; nothing here is maintained by hand.

USAGE
-----
    python3 scripts/sprint-truth.py                 # MVP milestone (the beta gate)
    python3 scripts/sprint-truth.py --milestone Production
    python3 scripts/sprint-truth.py --list          # itemize the not-Done work

Paste the output into any completeness claim. A claim without it is a claim without a
denominator.
"""
import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict

PROJECT = "1"
OWNER = "mediajunkie"

# Statuses that mean "this work is not finished", in the order a reader should see them.
# Ordering is deliberate: the ones most likely to be silently excluded come first.
NOT_DONE_ORDER = ["Sprint Backlog", "Blocked", "In Progress", "In Review"]
GLOSS = {
    "Sprint Backlog": "NOT STARTED — no one has picked these up",
    "Blocked": "stuck on something external",
    "In Progress": "actively being worked",
    "In Review": "built, awaiting verification (usually PM's)",
}


def fetch(limit=1400):
    cmd = ["gh", "project", "item-list", PROJECT, "--owner", OWNER,
           "--limit", str(limit), "--format", "json"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as exc:  # pragma: no cover
        sys.exit(f"FAILED to query the board: {exc}\nThis check measured NOTHING.")
    if out.returncode != 0:
        sys.exit(f"FAILED to query the board (rc={out.returncode}): {out.stderr.strip()}\n"
                 "This check measured NOTHING — do not read its silence as a clear.")
    data = json.loads(out.stdout)
    items = data.get("items", [])
    if not items:
        sys.exit("Board returned ZERO items. That is a query failure, not an empty sprint.")
    return items


def milestone_of(item):
    ms = item.get("milestone")
    return ms.get("title") if isinstance(ms, dict) else ms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--milestone", default="MVP")
    ap.add_argument("--list", action="store_true", help="itemize the not-Done work")
    args = ap.parse_args()

    items = fetch()
    scoped = [i for i in items if milestone_of(i) == args.milestone]
    if not scoped:
        sys.exit(f"No items found in milestone {args.milestone!r} — check the name before believing this.")

    by_status = Counter(i.get("status") or "(no status set)" for i in scoped)
    done = by_status.get("Done", 0)
    not_done = {k: v for k, v in by_status.items() if k != "Done"}
    total_open = sum(not_done.values())

    print(f"MILESTONE: {args.milestone}   (project #{PROJECT}, queried live)")
    print(f"scanned {len(items)} board items; {len(scoped)} carry this milestone\n")

    print(f"NOT DONE — {total_open}")
    ordered = [s for s in NOT_DONE_ORDER if s in not_done]
    ordered += [s for s in sorted(not_done) if s not in NOT_DONE_ORDER]
    for status in ordered:
        gloss = GLOSS.get(status, "")
        print(f"  {not_done[status]:>4}  {status:<16} {gloss}")
    print(f"\n  {done:>4}  Done")

    # The sentence a reporter should copy, rather than composing their own.
    parts = ", ".join(f"{not_done[s]} {s}" for s in ordered)
    print("\n--- paste this, not a single number ---")
    print(f"{args.milestone}: {total_open} not done ({parts}); {done} done.")
    if not_done.get("Sprint Backlog"):
        print(f"NOTE: {not_done['Sprint Backlog']} item(s) have NOT BEEN STARTED. "
              f"Any 'complete' claim must exclude itself explicitly.")

    if args.list:
        print("\n--- the not-Done work, itemized ---")
        grouped = defaultdict(list)
        for i in scoped:
            st = i.get("status") or "(no status set)"
            if st == "Done":
                continue
            c = i.get("content") or {}
            grouped[st].append((c.get("number"), (i.get("title") or "")[:66]))
        for status in ordered:
            print(f"\n{status} ({len(grouped[status])}) — {GLOSS.get(status,'')}")
            for num, title in sorted(grouped[status], key=lambda x: (x[0] or 0)):
                print(f"  #{num}  {title}")


if __name__ == "__main__":
    main()
