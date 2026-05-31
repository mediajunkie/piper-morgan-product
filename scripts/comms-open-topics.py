#!/usr/bin/env python3
"""Comms open-topics derived view — calendar-based, always current.

This is Layer B of the orphan-prevention framework PM ratified May 24.
It replaces the hand-maintained "drafted-and-awaiting" sections of
`dev/active/comms-open-topics.md` with a derived view computed from
the editorial calendar (the source of truth for what's drafted /
scheduled / published).

Rationale: hand-maintained trackers go stale (the May 10 incident —
tracker named the 4 orphan drafts then went 14 days stale through the
May 17–23 9-beat-slate planning that never consulted it). A derived
view can't go stale because it's computed from the system-of-record
each time it's read. PM 2026-05-29 ratified the binding rule: tie weak
disciplines to strong ones (commit-binding for log currency; calendar
query for tracker currency).

What this view shows:
  1. DRAFTED, awaiting PM voice-pass + scheduling
     (status=`drafted` rows — files exist but aren't yet on the calendar
     with a pubDate)
  2. OVERDUE — status=`queued` with pubDate in the past and URL columns
     empty (publication slipped; needs PM attention)
  3. QUEUED, upcoming next 14 days (heads-up for PM voice-pass cadence)

What this view does NOT cover (use a different tracker for these):
  - Cross-cutting PM topics that aren't tied to specific blog posts
    (conference invitations, deferred conversations, scope-review items).
    These don't have a calendar home; the slimmed-down
    `dev/active/comms-open-topics.md` keeps them.
  - Per-draft voice-pass flags (in-body CONSIDER notes). Those live in
    the draft files themselves; the calendar can't know about them.

Usage:
    python3 scripts/comms-open-topics.py

Exit codes:
    0 — always (read-only view; no error conditions)

Wired into (recommended):
    - Comms session start (check this view first to see what needs attention)
    - PM voice-pass cadence check (what's coming up that needs my pass)
    - Before any pipeline-planning session (Layer C will formalize this)
"""

import csv
import datetime as dt
import sys
from pathlib import Path

CALENDAR = Path('docs/internal/planning/comms/editorial-calendar.csv')
TODAY = dt.date(2026, 5, 30)  # NOTE: deterministic; pass via env or arg if you need today's date
HEADS_UP_DAYS = 14
URL_COLUMNS = ('mediumURL', 'liPubDate', 'linkedinURL', 'blogURL')


def parse_date(s: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(s.strip())
    except (ValueError, AttributeError):
        return None


def has_publish_urls(row: dict) -> bool:
    return any((row.get(c) or '').strip() for c in URL_COLUMNS)


def main() -> int:
    if not CALENDAR.exists():
        print(f"ERROR: {CALENDAR} not found (run from repo root)", file=sys.stderr)
        return 2

    drafted: list[dict] = []
    overdue: list[dict] = []
    upcoming: list[dict] = []
    horizon = TODAY + dt.timedelta(days=HEADS_UP_DAYS)

    with CALENDAR.open() as f:
        for row in csv.DictReader(f):
            status = (row.get('status') or '').strip()
            pubdate = parse_date(row.get('pubDate') or '')

            if status == 'drafted':
                drafted.append(row)
            elif status == 'queued':
                if pubdate is None:
                    # Queued without a pubDate — treat as drafted-and-awaiting
                    drafted.append(row)
                elif pubdate < TODAY and not has_publish_urls(row):
                    overdue.append(row)
                elif TODAY <= pubdate <= horizon:
                    upcoming.append(row)

    print(f"Comms open topics — derived from {CALENDAR}")
    print(f"As of {TODAY.isoformat()} (today)")
    print()

    print(f"## DRAFTED, awaiting PM voice-pass + scheduling ({len(drafted)})")
    print()
    if not drafted:
        print("  (none)")
    else:
        for row in drafted:
            title = row.get('title', '').strip()
            workdate = (row.get('workDate') or '').strip()
            draftpath = (row.get('draftPath') or '').strip() or '(no draftPath)'
            theme = (row.get('theme') or '').strip()
            print(f"  - {title!r}")
            print(f"      theme={theme} | workDate={workdate} | {draftpath}")
    print()

    print(f"## OVERDUE — queued with past pubDate, no publish URLs ({len(overdue)})")
    print()
    if not overdue:
        print("  (none)")
    else:
        for row in overdue:
            title = row.get('title', '').strip()
            pubdate = (row.get('pubDate') or '').strip()
            draftpath = (row.get('draftPath') or '').strip() or '(no draftPath)'
            theme = (row.get('theme') or '').strip()
            days_late = (TODAY - parse_date(pubdate)).days
            print(f"  - {title!r}  [{days_late}d late]")
            print(f"      theme={theme} | pubDate={pubdate} | {draftpath}")
    print()

    print(f"## QUEUED upcoming next {HEADS_UP_DAYS} days ({len(upcoming)})")
    print()
    if not upcoming:
        print("  (none)")
    else:
        upcoming.sort(key=lambda r: r.get('pubDate', ''))
        for row in upcoming:
            title = row.get('title', '').strip()
            pubdate = (row.get('pubDate') or '').strip()
            draftpath = (row.get('draftPath') or '').strip() or '(no draftPath)'
            theme = (row.get('theme') or '').strip()
            print(f"  - {pubdate}  {title!r}")
            print(f"      theme={theme} | {draftpath}")
    print()

    print("---")
    print("For cross-cutting non-calendar PM topics (conference invitations,")
    print("deferred conversations, scope-review items): see")
    print("dev/active/comms-open-topics.md (slimmed to those items only).")
    return 0


if __name__ == '__main__':
    sys.exit(main())
