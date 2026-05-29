#!/usr/bin/env python3
"""Reconcile docs/public/comms/drafts/ against editorial-calendar.csv.

This is the mechanical "Layer D" catch-net for the orphan-drafts failure
mode (Pattern-074: Visibility Loss After Premature Retirement). It detects
drift in BOTH directions between the drafts folder (filesystem source of
truth for "what's been drafted") and the calendar (source of truth for
"what's tracked / scheduled").

Three checks:
  1. TRUE ORPHANS    — .md files in drafts/ that no calendar row references
                       via draftPath. These are the "lost drafts" — drafted
                       but untracked. (The May 24-29 incidents: BYOC,
                       Briefing-to-Vision, From-Abstraction, Meta-Observation.)
  2. MISSING DRAFTPATH — drafted/queued rows with an empty draftPath column.
                       The row exists + is scheduled, but the file<->row link
                       isn't recorded ("broken links"). A naive draftPath
                       reconciliation false-flags these as orphans, and a
                       file rename would silently break the link. (May 29
                       found 6: Extension Without Integration, Solo Founder
                       Paradox, When Your AI Makes Things Up, Be Prepared,
                       Relationship-First Ethics, Triad Model.)
  3. STALE DRAFTPATH  — drafted/queued rows whose draftPath points to a file
                       that no longer exists in the repo (renamed/moved
                       without updating the calendar).

Usage:
    python3 scripts/reconcile-drafts-calendar.py

Exit codes:
    0 — clean (no orphans, no missing/stale draftPath on active rows)
    1 — drift found (details printed)
    2 — calendar file or drafts dir not found

Wired into (recommended):
    - Comms manual invocation before any pipeline-planning session
      (the "inventory query" step that prevents planning-from-stale-state)
    - Comms weekly orphan-sweep (e.g., Friday before workstream review)
    - Optional pre-commit hook flagging new drafts/*.md without a calendar
      row (cohort coordination needed — see Comms->Docs process memo
      2026-05-29). That would make Layer D preventive as well as detective.

Companion to validate-editorial-calendar.py (which checks CSV structure;
this checks file<->row correspondence).
"""

import csv
import sys
from pathlib import Path

CALENDAR = Path('docs/internal/planning/comms/editorial-calendar.csv')
DRAFTS_DIR = Path('docs/public/comms/drafts')
DRAFTPATH_COL = 'draftPath'
STATUS_COL = 'status'
TITLE_COL = 'title'
# Statuses for which a draftPath link is expected (active, not-yet-published work).
ACTIVE_STATUSES = {'drafted', 'queued'}


def main() -> int:
    if not CALENDAR.exists():
        print(f"ERROR: {CALENDAR} not found (run from repo root)", file=sys.stderr)
        return 2
    if not DRAFTS_DIR.is_dir():
        print(f"ERROR: {DRAFTS_DIR} not found (run from repo root)", file=sys.stderr)
        return 2

    # Files actually on disk in drafts/
    draft_files = {p.name for p in DRAFTS_DIR.glob('*.md')}

    # Calendar rows: collect draftPath references + per-row checks
    referenced_basenames: set[str] = set()
    missing_draftpath: list[str] = []   # active rows with empty draftPath
    stale_draftpath: list[str] = []     # active rows whose draftPath file is gone

    with CALENDAR.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            draftpath = (row.get(DRAFTPATH_COL) or '').strip()
            status = (row.get(STATUS_COL) or '').strip()
            title = (row.get(TITLE_COL) or '').strip()

            if draftpath:
                referenced_basenames.add(Path(draftpath).name)
                if status in ACTIVE_STATUSES and not Path(draftpath).exists():
                    stale_draftpath.append(f"{title!r} -> {draftpath} (file missing)")
            elif status in ACTIVE_STATUSES:
                missing_draftpath.append(f"{title!r} (status={status})")

    true_orphans = sorted(draft_files - referenced_basenames)

    issues = len(true_orphans) + len(missing_draftpath) + len(stale_draftpath)

    if not issues:
        print(f"✓ drafts<->calendar reconciled: {len(draft_files)} draft files, "
              f"all linked; no missing/stale draftPath on active rows")
        return 0

    print(f"❌ drafts<->calendar drift: {issues} issue(s)\n")

    if true_orphans:
        print(f"TRUE ORPHANS ({len(true_orphans)}) — drafts/*.md with no calendar row referencing them:")
        for name in true_orphans:
            print(f"   - {name}")
        print()

    if missing_draftpath:
        print(f"MISSING DRAFTPATH ({len(missing_draftpath)}) — active rows with empty draftPath column:")
        for item in sorted(missing_draftpath):
            print(f"   - {item}")
        print()

    if stale_draftpath:
        print(f"STALE DRAFTPATH ({len(stale_draftpath)}) — active rows whose draftPath file is gone:")
        for item in sorted(stale_draftpath):
            print(f"   - {item}")
        print()

    return 1


if __name__ == '__main__':
    sys.exit(main())
