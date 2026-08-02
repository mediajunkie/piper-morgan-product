#!/usr/bin/env python3
"""Measure editorial-data drift across the product/website surface boundary.

This is the **reproducible measurement backing PDR-007's pre-registered success
criterion**. The criterion exists because Arch pointed out (2026-07-30) that the
PDR's 2-4 week evaluation window had no falsification condition and therefore
could not fail — *"a decision procedure with no falsification condition is m-44's
shape applied to a decision instead of an instrument."*

A threshold nobody can measure the same way twice is the same defect one layer
down, so the measurement lives here rather than in a session log.

PDR-007 criterion — Option A is sufficient (close as adopted-without-migration)
if ALL THREE hold at window end (2026-08-27):

    1. Class 1  — column-shift instances reaching origin/main undetected : 0
    2. Class 2  — unresolvable draftPath values                          : 0
    3. Class 3  — field-level disagreements on the matched set           : <= 17

Classes 1 and 2 are covered by validate-editorial-calendar.py (errors and the
draftPath reference check respectively). THIS script measures Class 3, and
reports 1 and 2 alongside so a single run answers the whole criterion.

Baseline, measured 2026-07-29:
    Class 1: 0 · Class 2: 0 (after 7 repairs) · Class 3: 17 across 365 matched rows

Usage:
    python3 scripts/measure-editorial-drift.py
    python3 scripts/measure-editorial-drift.py --json     # machine-readable
    python3 scripts/measure-editorial-drift.py --verbose  # list every disagreement

Exit codes:
    0 — measurement completed (this script REPORTS; it does not gate)
    2 — a required input file was not found

Deliberately non-gating: it measures, it does not decide. The decision is
PDR-007's, made once at window end against the pre-registered numbers.
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

CALENDAR = Path("docs/internal/planning/comms/editorial-calendar.csv")

# The website repo is a sibling worktree. Try the agent worktree first, then the
# shared checkout — the path differs per agent and per host, so probe rather than
# assume (the same class of assumption that made copy-editorial-calendar.js fragile).
WEBSITE_CANDIDATES = [
    Path("../../piper-morgan-website-worktrees/docs"),
    Path("../piper-morgan-website"),
    Path("/Users/xian/Development/piper-morgan-website"),
]

# Same fact, different name on each side. These aliases are WHY textual comparison
# never surfaced this drift: nothing matches `altText` to `imageAlt`.
ALIASES = [
    ("altText", "imageAlt"),
    ("caption", "imageCaption"),
]


def find_website_root() -> Path | None:
    for c in WEBSITE_CANDIDATES:
        if (c / "data" / "blog-metadata.csv").exists():
            return c
    return None


def slug_from_blogpath(row: dict) -> str | None:
    bp = (row.get("blogPath") or "").strip("/")
    return bp.split("/")[-1] if bp else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--verbose", action="store_true", help="list every disagreement")
    args = ap.parse_args()

    if not CALENDAR.exists():
        print(f"ERROR: {CALENDAR} not found (run from repo root)", file=sys.stderr)
        return 2
    web_root = find_website_root()
    if web_root is None:
        print(
            "ERROR: could not locate the website repo. Tried:\n  "
            + "\n  ".join(str(c) for c in WEBSITE_CANDIDATES),
            file=sys.stderr,
        )
        return 2

    cal = list(csv.DictReader(CALENDAR.open(newline="", encoding="utf-8")))
    wm_rows = list(csv.DictReader((web_root / "data" / "blog-metadata.csv").open(newline="", encoding="utf-8")))
    by_slug = {r["slug"]: r for r in wm_rows}

    matched = 0
    disagreements: list[dict] = []
    for r in cal:
        s = slug_from_blogpath(r)
        if not s or s not in by_slug:
            continue
        matched += 1
        w = by_slug[s]
        for cal_field, web_field in ALIASES:
            a = (r.get(cal_field) or "").strip()
            b = (w.get(web_field) or "").strip()
            if a and b and a != b:
                disagreements.append(
                    {
                        "slug": s,
                        "title": (r.get("title") or "")[:60],
                        "field": f"{cal_field}!={web_field}",
                        "calendar": a[:70],
                        "website": b[:70],
                    }
                )

    # Class 2 — reuse the same definition the validator uses.
    stale_paths = [
        (r.get("title") or "")[:60]
        for r in cal
        if (r.get("draftPath") or "").strip() and not os.path.exists(r["draftPath"])
    ]

    class3 = len(disagreements)
    class2 = len(stale_paths)

    # PDR-007 pre-registered thresholds
    CRITERION = {"class2_max": 0, "class3_max": 17}
    passes = class2 <= CRITERION["class2_max"] and class3 <= CRITERION["class3_max"]

    if args.json:
        print(json.dumps({
            "matched_rows": matched,
            "class2_stale_draftpaths": class2,
            "class3_disagreements": class3,
            "criterion": CRITERION,
            "meets_criterion_2_and_3": passes,
            "note": "Class 1 is measured by validate-editorial-calendar.py exit status",
            "disagreements": disagreements if args.verbose else [],
        }, indent=2))
        return 0

    print(f"Editorial drift — PDR-007 measurement  (website root: {web_root})")
    print(f"  calendar rows matched to a website row : {matched}")
    print()
    print(f"  Class 2  stale draftPath values        : {class2:3}   (criterion: 0)")
    print(f"  Class 3  field-level disagreements     : {class3:3}   (criterion: <= {CRITERION['class3_max']}, baseline 17)")
    print()
    if args.verbose and disagreements:
        for d in disagreements:
            print(f"    {d['slug'][:44]:46} {d['field']}")
            print(f"        calendar: {d['calendar']!r}")
            print(f"        website : {d['website']!r}")
        print()
    for t in stale_paths:
        print(f"    STALE PATH: {t}")
    if stale_paths:
        print()
    verdict = "MEETS" if passes else "FAILS"
    print(f"  Classes 2+3 vs pre-registered criterion : {verdict}")
    print("  Class 1 (column shift) — run: python3 scripts/validate-editorial-calendar.py")
    print()
    print("  This script REPORTS; it does not gate. PDR-007's decision is made once,")
    print("  at window end (2026-08-27), against these pre-registered numbers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
