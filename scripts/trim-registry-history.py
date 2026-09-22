#!/usr/bin/env python3
"""
trim-registry-history.py — move one role's accreted 'was:' history out of
dev/active/duty-cycle-registry.tsv into a per-role append-only log, keeping
only the row's CURRENT state inline.

Standing item 7w / context-floor plan item 3 (docs/internal/operations/
context-floor-reduction-plan-2026-09-21.md): the registry's state column is
append-only prose -- every prior state stays inline as a `was:`/`Prior:`
chain rather than being archived, and this file is read in full by every
seat's freeze-check or PARK logic, every fire. Nothing is lost by trimming
it -- the full chain is preserved verbatim in the per-role history log; it
just stops being paid for on every read.

Split point: the LITERAL state-transition marker `was: active:` or
`was: parked:` (not a bare occurrence of the word "was" in prose, which
appears constantly in this cohort's own writing). Everything before the
first such marker is the current state and stays in the registry;
everything from that marker onward (including further nested `was:`
chains inside it) moves to the history log, appended with a timestamp.

Requires an explicit --role and refuses to run against more than one role
per invocation -- no "all roles" mode, matching the same "exercise on one
seat first" discipline as scripts/archive-mailbox-read.py (standing item
7x). Dry-run by default; pass --execute to actually write.

Usage:
    python scripts/trim-registry-history.py --role cio                # dry-run
    python scripts/trim-registry-history.py --role cio --execute       # do it
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_DEFAULT = PROJECT_ROOT / "dev" / "active" / "duty-cycle-registry.tsv"
# dev/state/, NOT dev/active/ — dev/active/ is sprint-cleaned (cleanup-dev-active skill), and this
# history log is exactly the class of durable record that must survive a sweep. Same lesson as the
# mailbox-archive and PM-scan-marker footguns caught earlier this week (both moved dev/active/ ->
# dev/state/ for the identical reason): a marker/log under dev/active/ silently degrades or
# disappears the day it gets swept, with no error.
HISTORY_DIR_DEFAULT = PROJECT_ROOT / "dev" / "state" / "registry-history"

# The literal state-transition convention this registry's rows use, not a bare
# occurrence of the word "was" (which shows up constantly in ordinary prose).
SPLIT_RE = re.compile(r"\bwas: (active|parked):")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--role", required=True, help="exactly one role slug (e.g. cio) — no all-roles mode, by design")
    ap.add_argument("--execute", action="store_true", help="actually write (default: dry-run, report only)")
    ap.add_argument("--registry", default=str(REGISTRY_DEFAULT), help="path to the registry TSV (default: the real one)")
    ap.add_argument("--history-dir", default=str(HISTORY_DIR_DEFAULT), help="directory for per-role history logs")
    args = ap.parse_args()

    registry_path = Path(args.registry)
    with registry_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    out_lines: list[str] = []
    found = False
    history_text: str | None = None
    before_len = after_len = 0

    for line in lines:
        if line.startswith(f"{args.role}\t"):
            found = True
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 8:
                print(f"REFUSING: row for '{args.role}' does not have 8 fields (has {len(fields)}) — not touching it", file=sys.stderr)
                return 2
            state = fields[7]
            before_len = len(state)
            m = SPLIT_RE.search(state)
            if not m:
                print(f"no 'was:' history found in '{args.role}'s row — nothing to trim")
                out_lines.append(line)
                continue
            current = state[: m.start()].rstrip()
            history = state[m.start():]
            after_len = len(current)
            fields[7] = current
            out_lines.append("\t".join(fields) + "\n")
            history_text = history
        else:
            out_lines.append(line)

    if not found:
        print(f"REFUSING: no row found for role '{args.role}'", file=sys.stderr)
        return 2

    if not history_text:
        print(f"'{args.role}'s row has no 'was:' history chain — nothing to do.")
        return 0

    print(f"role '{args.role}': state column {before_len} -> {after_len} chars ({len(history_text)} chars of history to move)")

    if not args.execute:
        print("Dry-run only — nothing written. Re-run with --execute to perform the trim.")
        return 0

    registry_path.write_text("".join(out_lines), encoding="utf-8")

    history_dir = Path(args.history_dir)
    history_dir.mkdir(parents=True, exist_ok=True)
    hist_path = history_dir / f"{args.role}.log"
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with hist_path.open("a", encoding="utf-8") as f:
        f.write(f"\n--- trimmed from registry {ts} ---\n{history_text}\n")

    print(f"trimmed {len(history_text)} chars of history for '{args.role}' -> {hist_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
