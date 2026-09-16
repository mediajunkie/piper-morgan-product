#!/usr/bin/env python3
"""Verify a continue-narrative survey produced a complete per-day ledger.

Root cause this closes: a broad-window survey can return an aggregate
impression ("rich everywhere") that is unauditable — a day that didn't
surface a loud candidate on the first pass can go silently missing, with
nothing to check it against. Real incidents: Aug 21-26 2026 (4 of 6 days
missed, caught only because PM asked), Aug 10-18 2026 (5 of 9 days missed,
same pattern, same session). Both were caught by PM asking "did you miss
it," not by any mechanism. This script is that mechanism.

Ledger format (embedded in the session log by continue-narrative Step 2):

    <!-- NARRATIVE-SURVEY-LEDGER: START=2026-08-10 END=2026-08-18 -->
    | date | verdict | note |
    |---|---|---|
    | 2026-08-10 | candidate | the floor-honesty contract's first day |
    | 2026-08-11 | thin | routine sync + mail triage only |
    ...
    <!-- /NARRATIVE-SURVEY-LEDGER -->

verdict must be exactly "candidate" or "thin". Every calendar day in
[START, END] inclusive must appear exactly once. Anything else is an
incomplete survey, full stop, regardless of how rich the covered days read.

Usage:
    check-narrative-survey-coverage.py --start 2026-08-10 --end 2026-08-18 LOG_FILE [LOG_FILE ...]

Exit 0: every day in range has exactly one candidate/thin verdict.
Exit 1: gap, duplicate, bad verdict, or no ledger block found at all.
"""
import argparse
import re
import sys
from datetime import date, timedelta

LEDGER_RE = re.compile(
    r"<!--\s*NARRATIVE-SURVEY-LEDGER:\s*START=(\d{4}-\d{2}-\d{2})\s+END=(\d{4}-\d{2}-\d{2})\s*-->"
    r"(.*?)"
    r"<!--\s*/NARRATIVE-SURVEY-LEDGER\s*-->",
    re.DOTALL,
)
ROW_RE = re.compile(
    r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(candidate|thin)\s*\|\s*(.*?)\s*\|\s*$",
    re.MULTILINE,
)


def daterange(start, end):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", required=True, type=date.fromisoformat)
    ap.add_argument("--end", required=True, type=date.fromisoformat)
    ap.add_argument("files", nargs="+", help="session log file(s) to scan for the ledger block")
    args = ap.parse_args()

    wanted = {d.isoformat() for d in daterange(args.start, args.end)}
    seen = {}  # date -> (verdict, note, source_file)
    blocks_found = 0

    for path in args.files:
        try:
            text = open(path, encoding="utf-8").read()
        except OSError as e:
            print(f"✗ CANNOT READ {path}: {e}")
            continue
        for m in LEDGER_RE.finditer(text):
            blocks_found += 1
            for row in ROW_RE.finditer(m.group(3)):
                d, verdict, note = row.groups()
                if d in seen:
                    print(f"✗ DUPLICATE ledger row for {d}: already seen in {seen[d][2]}, again in {path}")
                seen[d] = (verdict, note, path)

    if blocks_found == 0:
        print(f"✗ NO LEDGER BLOCK FOUND in: {', '.join(args.files)}")
        print("  A survey with no ledger has proven nothing — this is the exact failure this script exists to catch.")
        sys.exit(1)

    missing = sorted(wanted - seen.keys())
    stray = sorted(seen.keys() - wanted)

    ok = True
    if missing:
        ok = False
        print(f"✗ MISSING {len(missing)} of {len(wanted)} day(s) — no verdict recorded:")
        for d in missing:
            print(f"    {d}")
    if stray:
        print(f"⚠ {len(stray)} ledger row(s) fall outside the claimed [{args.start}, {args.end}] range (not an error, just noting):")
        for d in stray:
            print(f"    {d}")

    n_candidate = sum(1 for v, _, _ in seen.values() if v == "candidate")
    n_thin = sum(1 for v, _, _ in seen.values() if v == "thin")

    if ok:
        print(f"✓ complete: {len(wanted)}/{len(wanted)} days verdicted ({n_candidate} candidate, {n_thin} thin)")
        sys.exit(0)
    else:
        print(f"  {len(seen) - len(stray)}/{len(wanted)} days verdicted — survey is INCOMPLETE, do not present this slate to PM yet")
        sys.exit(1)


if __name__ == "__main__":
    main()
