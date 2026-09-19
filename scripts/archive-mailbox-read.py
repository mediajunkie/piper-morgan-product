#!/usr/bin/env python3
"""
archive-mailbox-read.py — quarterly archival for mailboxes/{role}/read/.

Standing item 7x (cio-standing-items.md), Exec's process proposal (Sept 11 2026):
`mailboxes/*/read/` accumulates every triaged memo forever (11,510 files cohort-wide
at the time this was filed) with no archival step. This moves memos from COMPLETED
quarters into `read/archive/YYYY-QN/`, leaving the current quarter's memos live in
`read/` directly.

MANIFEST-regen-safe by construction, not by convention: `regenerate-mailbox-manifests.py`
walks `read/` with `Path.iterdir()`, which does not recurse into subdirectories — an
`archive/` subdirectory (and anything under it) is invisible to the MANIFEST regen
without any change to that script. Verified before writing this script, not assumed.

Per Exec's own caution (relayed via cio-standing-items.md row 7x): exercise on ONE
seat first. This script requires an explicit --role and refuses to run against more
than one role in a single invocation — there is no "all roles" mode. Cohort-wide
rollout is a separate, coordinated decision, not a flag on this script.

Dry-run by default. Pass --execute to actually move files.

Usage:
    python scripts/archive-mailbox-read.py --role cio                # dry-run
    python scripts/archive-mailbox-read.py --role cio --execute       # do it
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAILBOXES_ROOT = PROJECT_ROOT / "mailboxes"

_FILENAME_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
MANIFEST_FILENAME = "MANIFEST.md"


def parse_frontmatter(path: Path) -> dict:
    """Same logic as regenerate-mailbox-manifests.py's parse_frontmatter,
    kept independent rather than imported so this script has no import-time
    coupling to that one — deliberate, not an oversight."""
    try:
        with path.open("r", encoding="utf-8") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= 60:
                    break
                lines.append(line.rstrip("\n"))
    except (OSError, UnicodeDecodeError):
        return {}

    if not lines or lines[0].strip() != "---":
        return {}

    fields: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip().lower()] = val.strip()
    return fields


def extract_date(frontmatter: dict, filename: str) -> str:
    raw = frontmatter.get("date", "")
    if raw:
        m = _FILENAME_DATE_RE.search(raw)
        if m:
            return m.group(1)
    m = _FILENAME_DATE_RE.search(filename)
    return m.group(1) if m else ""


def quarter_of(date_str: str) -> str:
    """'2026-07-14' -> '2026-Q3'."""
    year, month = date_str[:4], int(date_str[5:7])
    q = (month - 1) // 3 + 1
    return f"{year}-Q{q}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--role", required=True, help="exactly one role slug (e.g. cio) — no all-roles mode, by design")
    ap.add_argument("--execute", action="store_true", help="actually move files (default: dry-run, report only)")
    ap.add_argument("--current-quarter", default=None, help="override for testing, e.g. 2026-Q3 (default: derived from today's date via --today)")
    ap.add_argument("--today", default=None, help="YYYY-MM-DD override for 'today', for reproducible dry-runs (default: real today)")
    args = ap.parse_args()

    if args.today:
        today = args.today
    else:
        import datetime as _dt
        today = _dt.date.today().isoformat()

    current_q = args.current_quarter or quarter_of(today)

    read_dir = MAILBOXES_ROOT / args.role / "read"
    if not read_dir.is_dir():
        print(f"no read/ directory for role '{args.role}' at {read_dir}", file=sys.stderr)
        return 2

    by_quarter: dict[str, list[Path]] = defaultdict(list)
    undated: list[Path] = []
    already_current_or_future = 0

    for path in sorted(read_dir.iterdir()):
        if path.is_dir():
            continue  # e.g. archive/ itself, or any other subdir — never touched
        if path.name == MANIFEST_FILENAME or path.suffix != ".md":
            continue
        fm = parse_frontmatter(path)
        date_str = extract_date(fm, path.name)
        if not date_str:
            undated.append(path)
            continue
        q = quarter_of(date_str)
        if q >= current_q:
            already_current_or_future += 1
            continue
        by_quarter[q].append(path)

    total_to_move = sum(len(v) for v in by_quarter.values())

    print(f"── archive-mailbox-read · role={args.role} · today={today} · current_quarter={current_q} ──")
    print(f"mode: {'EXECUTE' if args.execute else 'DRY-RUN (pass --execute to actually move files)'}")
    print()
    print(f"{total_to_move} file(s) eligible for archival (completed quarters, strictly before {current_q}):")
    for q in sorted(by_quarter):
        print(f"  {q}: {len(by_quarter[q])} file(s) -> read/archive/{q}/")
    print()
    print(f"left in place: {already_current_or_future} file(s) in {current_q} or later (current quarter stays live)")
    print(f"left in place: {len(undated)} file(s) with no extractable date (never archived — a date-extraction gap, not a decision)")
    if undated:
        for p in undated[:10]:
            print(f"    undated: {p.name}")
        if len(undated) > 10:
            print(f"    ... and {len(undated) - 10} more")

    if not args.execute:
        print()
        print("Dry-run only — nothing moved. Re-run with --execute to perform the moves.")
        return 0

    moved = 0
    for q, paths in sorted(by_quarter.items()):
        dest_dir = read_dir / "archive" / q
        dest_dir.mkdir(parents=True, exist_ok=True)
        for p in paths:
            dest = dest_dir / p.name
            if dest.exists():
                print(f"    SKIP (dest exists, not overwriting): {p.name}", file=sys.stderr)
                continue
            p.rename(dest)
            moved += 1

    print()
    print(f"moved {moved} file(s). Run scripts/regenerate-mailbox-manifests.py --role {args.role} next")
    print("(archive/ subdirectories are invisible to the MANIFEST regen by construction — no flag needed).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
