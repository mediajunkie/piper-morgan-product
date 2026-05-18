#!/usr/bin/env python3
"""Validate editorial-calendar.csv structure.

Catches CSV escape errors (unquoted commas in altText/caption/notes),
field-count drift (rows with != 18 fields), and header mismatch.

Usage:
    python3 scripts/validate-editorial-calendar.py

Exit codes:
    0 — all rows valid
    1 — validation error(s) found (details printed to stderr)
    2 — calendar file not found

Wired into:
    - Manual invocation by Docs after any /update-calendar pass
    - Optional pre-commit hook (future enhancement; see header comment)

Rationale: May 17 incident — hand-edit of calendar row introduced an
unescaped comma in altText (field count drifted to 19; should have been
18). The /update-calendar skill v1.0 procedure ended with `grep TITLE
editorial-calendar.csv` for a visual check, but grep + awk can't catch
escape errors on quoted fields. The Python csv module DOES parse
correctly; this script wraps it as a one-shot validator.

publish-to-blog skill v0.11 mandates calling this kind of CSV-parser
verification after any calendar mutation. This script is the canonical
implementation.
"""

import csv
import sys
from pathlib import Path

CALENDAR = Path('docs/internal/planning/comms/editorial-calendar.csv')
EXPECTED_FIELDS = 18
EXPECTED_HEADER = [
    'title', 'theme', 'status', 'workDate', 'endWorkDate', 'pubDate',
    'mediumURL', 'liPubDate', 'linkedinURL', 'canonicalSite',
    'blogURL', 'blogPath', 'cartoon', 'chatDate', 'draftPath',
    'notes', 'altText', 'caption',
]


def main() -> int:
    if not CALENDAR.exists():
        print(f"ERROR: {CALENDAR} not found (run from repo root)", file=sys.stderr)
        return 2

    errors: list[str] = []
    row_count = 0

    with CALENDAR.open() as f:
        reader = csv.reader(f)
        for line_no, row in enumerate(reader, 1):
            row_count += 1

            if line_no == 1:
                # Header row
                if row != EXPECTED_HEADER:
                    errors.append(
                        f"Line 1 (header) mismatch:\n"
                        f"  got:      {row}\n"
                        f"  expected: {EXPECTED_HEADER}"
                    )
                continue

            if len(row) != EXPECTED_FIELDS:
                title_preview = row[0][:60] if row else '<empty row>'
                errors.append(
                    f"Line {line_no}: {len(row)} fields (expected {EXPECTED_FIELDS}) "
                    f"— title={title_preview!r}"
                )

    if errors:
        print(f"❌ editorial-calendar.csv: {len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"   {e}", file=sys.stderr)
        return 1

    data_rows = row_count - 1  # subtract header
    print(f"✓ editorial-calendar.csv: {data_rows} data rows + 1 header, all {EXPECTED_FIELDS} fields, clean")
    return 0


if __name__ == '__main__':
    sys.exit(main())
