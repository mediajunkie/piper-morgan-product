#!/usr/bin/env python3
"""Validate docs/internal/design/tier1-corpus-manifest.csv (#2355).

One row per Tier 1 corpus item: source, tier, last-verified date, re-verify
window, owner. Errors fail (exit 1). Rows that are unverified or past their
window are reported, and fail only with --strict, because Lead's deploy check
decides what to enforce at deploy.

Checks: header, field counts, unique ids, enums, dates, windows are positive
integers, every source path exists (a source is `path`, `path#heading` or
`path::symbol`, several joined by "; "), and no source lies under the
never-indexed trees (dev/, mailboxes/, omnibus-logs/, agent memory).
Written by Docs 2026-11-13 as a proposal for Lead to adapt.
Concept: docs/internal/design/tier1-corpus-manifest.md
"""

import csv
import datetime
import os
import sys

PATH = "docs/internal/design/tier1-corpus-manifest.csv"
HEADER = [
    "id",
    "part",
    "topic",
    "source",
    "source_kind",
    "tier",
    "status",
    "last_verified",
    "reverify_window_days",
    "owner",
    "voice_pass",
    "notes",
]
PARTS = {"a", "b", "c", "d", "candidate"}
STATUS = {"candidate", "unverified", "verified"}
KINDS = {"doc", "generated"}
VOICE = {"pending", "passed", "returned"}
OWNERS = {"docs", "lead", "cio", "cxo", "arch", "ppm"}
EXCLUDED = ("dev/", "mailboxes/", "docs/omnibus-logs/", ".claude-pm/", "memory/")


def sources(cell):
    for part in cell.split(";"):
        part = part.strip()
        if part:
            yield part.split("::")[0].split("#")[0]


def main(argv):
    strict = "--strict" in argv
    today = datetime.date.today()
    errors, notes = [], []
    with open(PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if rows[0] != HEADER:
        sys.exit(f"ERROR: header is {rows[0]}, expected {HEADER}")
    seen = set()
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(HEADER):
            errors.append(f"row {n}: {len(r)} fields")
            continue
        d = dict(zip(HEADER, r))
        rid = d["id"]
        if not rid or rid in seen:
            errors.append(f"row {n}: id {rid!r} empty or repeated")
        seen.add(rid)
        for col, ok in (
            ("part", PARTS),
            ("status", STATUS),
            ("source_kind", KINDS),
            ("voice_pass", VOICE),
            ("owner", OWNERS),
        ):
            if d[col] not in ok:
                errors.append(f"{rid}: {col}={d[col]!r}")
        if d["tier"] != "1":
            errors.append(f"{rid}: tier={d['tier']!r} (this manifest is Tier 1 only)")
        if not d["reverify_window_days"].isdigit() or int(d["reverify_window_days"]) < 1:
            errors.append(f"{rid}: reverify_window_days={d['reverify_window_days']!r}")
        for p in sources(d["source"]):
            if p.startswith(EXCLUDED):
                errors.append(f"{rid}: source {p} is under a never-indexed tree")
            elif not os.path.exists(p):
                errors.append(f"{rid}: source {p} does not exist")
        lv = d["last_verified"]
        if d["status"] == "verified" and not lv:
            errors.append(f"{rid}: status verified but no last_verified date")
        if lv:
            try:
                age = (today - datetime.date.fromisoformat(lv)).days
                if age > int(d["reverify_window_days"] or 0):
                    notes.append(
                        f"{rid}: verified {lv}, {age} days ago, past its {d['reverify_window_days']}-day window"
                    )
            except ValueError:
                errors.append(f"{rid}: last_verified={lv!r}")
        elif d["status"] != "candidate":
            notes.append(f"{rid}: unverified")
    for e in errors:
        print("ERROR", e)
    for m in notes:
        print("NOTE ", m)
    count = len(rows) - 1
    print(f"{PATH}: {count} rows, {len(errors)} error(s), {len(notes)} note(s)")
    return 1 if errors or (strict and notes) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
