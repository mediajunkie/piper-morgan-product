#!/usr/bin/env python3
"""registry-plist-drift.py — does each seat's registry row match the LaunchAgent that actually fires it?

READ-ONLY. CIO, 2026-11-02. The registry's `cron_expr` is the schedule of record, and the freeze
check reads it (with `first_fire`) to decide when a seat is late. The LaunchAgent plist is what
launchd actually runs. Nothing compared the two: on 11-02 Lead's row said `17 6,9,12,15,18,21`
while com.xian.pm-lead-cycle fired at :46, and a time was relayed from the row that was never a
slot (Pard's 15:10 correction). This prints one line per seat and exits 1 on any mismatch.

Compares minute and hour sets, and checks that `first_fire` is one of the plist's slots. Seats with a row but no plist (or the reverse) are reported, not failed.

Usage: scripts/registry-plist-drift.py [--registry PATH] [--plist-dir DIR]
Exit: 0 all match, 1 a mismatch, 2 nothing to compare (no plists readable).
"""

from __future__ import annotations

import argparse
import os
import plistlib
import sys
from pathlib import Path

PREFIX, SUFFIX = "com.xian.pm-", "-cycle.plist"


def parse_field(field: str) -> list[int]:
    out: set[int] = set()
    for part in field.split(","):
        if "-" in part:
            lo, hi = part.split("-")
            out.update(range(int(lo), int(hi) + 1))
        else:
            out.add(int(part))
    return sorted(out)


def read_registry(path: Path) -> dict[str, dict]:
    rows = {}
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        p = line.split("\t")
        if p[0] == "role" or len(p) < 6:
            continue
        rows[p[0]] = {"cron": p[1], "wake_start": int(p[3]), "first_fire": p[5]}
    return rows


def read_plist(path: Path) -> tuple[list[int], list[int]]:
    with path.open("rb") as fh:
        sci = plistlib.load(fh).get("StartCalendarInterval", [])
    if isinstance(sci, dict):
        sci = [sci]
    return sorted({e["Minute"] for e in sci}), sorted({e["Hour"] for e in sci})


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", type=Path, default=root / "dev/active/duty-cycle-registry.tsv")
    ap.add_argument("--plist-dir", type=Path, default=Path(os.path.expanduser("~/Library/LaunchAgents")))
    args = ap.parse_args()

    reg = read_registry(args.registry)
    plists = {}
    if args.plist_dir.is_dir():
        for f in sorted(args.plist_dir.iterdir()):
            if f.name.startswith(PREFIX) and f.name.endswith(SUFFIX):
                plists[f.name[len(PREFIX) : -len(SUFFIX)]] = f
    if not plists:
        print(f"no {PREFIX}*{SUFFIX} in {args.plist_dir}: nothing compared")
        return 2

    bad = 0
    for role in sorted(set(reg) | set(plists)):
        if role not in plists:
            print(f"{role:6} registry row, no plist (not compared)")
            continue
        if role not in reg:
            print(f"{role:6} plist, no registry row (not compared)")
            continue
        mins, hrs = read_plist(plists[role])
        r = reg[role]
        problems = []
        try:
            rmin, rhr = r["cron"].split()[:2]
            if parse_field(rmin) != mins:
                problems.append(f"minute {rmin} vs plist {mins}")
            if parse_field(rhr) != hrs:
                problems.append(f"hours {rhr} vs plist {hrs}")
        except (ValueError, IndexError):
            problems.append(f"unparseable cron_expr {r['cron']!r}")
        # first_fire must be a slot the plist actually fires (Exec's 06:01 is one, before its
        # wake_start, which is a seat's choice); a time that is no slot gates the freeze check wrong.
        slots = {f"{h:02d}:{m:02d}" for h in hrs for m in mins}
        if r["first_fire"] not in slots:
            problems.append(f"first_fire {r['first_fire']} is not a plist slot")
        if problems:
            bad += 1
            print(f"{role:6} MISMATCH: " + "; ".join(problems))
        else:
            print(f"{role:6} ok ({r['cron']})")
    compared = len(set(reg) & set(plists))
    print(f"{compared} compared: {compared - bad} match, {bad} mismatch")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
