#!/usr/bin/env python3
"""specialist-share.py — the share of each role's log entries that is its own specialist work.

The staleness runs (10-13, 10-27, 11-06) measured this with one subagent rater per run, and the 11-06
run found the noise between raters about as large as the changes (three method breaks and an undefined
"strict"). This fixes the rater: each role sent words or heading forms that mean "my specialist work",
and they live in docs/internal/research/specialist-markers.md, in a ```markers block this script reads.

An ENTRY is a "## " or "### " heading, or a top-level time bullet ("- 10:13 ..."), plus the lines up
to the next of either, in the role's own
session logs (dev/YYYY/MM/DD/*-{role}-code-log.md). Two counts per role, because headings undercount
some roles (Arch's mail-wake headings name the sender) and over-count others:
  heading   the entry's heading line carries one of the role's markers
  lead      the heading or the first non-blank body line does (the headline figure; Comms's form)
  content   the heading or any body line does (an upper bound: bodies cite rollups, rulings and
            scripts in passing, so it reads 40-80% for most roles on the first run)
It prints both, the top markers that carried each role's share, and its denominator.

A marker matching only a line quoted from another seat still counts (CXO's caution on `served PASS`):
the script can't tell whose verdict a line records. Read the content figure as an upper bound.

Usage: scripts/specialist-share.py [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--role ROLE] [--show N]
  --from/--to  window, inclusive (default: the 7 days ending yesterday)
  --show N     also print N example headings per side for each role (to spot-check the markers)

Layer: textual. It says what the logs name, not what the work was. Cost: one read of ~80 logs.
Benefit: none yet: first run 2026-11-06, against the 11-06 subagent figures. Review: the 12-18 run.
Owner: CIO (script); each role owns its own marker line.
Concept: docs/internal/research/specialist-markers.md
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKERS = ROOT / "docs" / "internal" / "research" / "specialist-markers.md"
HEADING = re.compile(r"^#{2,3} ")
# Lead and others log each unit as a time bullet under a fire heading ("- 10:13 Promotion of ..."),
# so a top-level time bullet also opens an entry.
BULLET = re.compile(r"^- \*{0,2}[0-2][0-9]:[0-5][0-9]\b")


def load_markers() -> dict[str, list[re.Pattern]]:
    text = MARKERS.read_text()
    m = re.search(r"```markers\n(.*?)```", text, re.S)
    if not m:
        sys.exit(f"no ```markers block in {MARKERS}")
    out: dict[str, list[re.Pattern]] = {}
    for line in m.group(1).splitlines():
        role, _, pats = line.partition(":")
        if not pats.strip():
            continue
        out[role.strip()] = [re.compile(p.strip(), re.I) for p in pats.split(" | ") if p.strip()]
    return out


def entries(path: Path):
    head, body = None, []
    for ln in path.read_text(errors="ignore").splitlines():
        if HEADING.match(ln) or BULLET.match(ln):
            if head is not None:
                yield head, body
            head, body = ln, []
        elif head is not None:
            body.append(ln)
    if head is not None:
        yield head, body


def hits(pats: list[re.Pattern], text: str) -> list[str]:
    return [p.pattern for p in pats if p.search(text)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    yesterday = dt.date.today() - dt.timedelta(days=1)
    ap.add_argument("--from", dest="start", default=str(yesterday - dt.timedelta(days=6)))
    ap.add_argument("--to", dest="end", default=str(yesterday))
    ap.add_argument("--role")
    ap.add_argument("--show", type=int, default=0)
    a = ap.parse_args()
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    markers = load_markers()
    roles = [a.role] if a.role else list(markers)

    print(f"specialist-share · {start} to {end} · markers from {MARKERS.relative_to(ROOT)}")
    print(
        f"{'role':<6} {'logs':>4} {'entries':>7} {'heading':>13} {'lead':>13} {'content':>13}  top markers (lead)"
    )
    for role in roles:
        pats = markers.get(role)
        if not pats:
            print(f"{role:<6} no marker line")
            continue
        logs = []
        d = start
        while d <= end:
            logs += sorted((ROOT / "dev" / d.strftime("%Y/%m/%d")).glob(f"*-{role}-code-log.md"))
            d += dt.timedelta(days=1)
        n = h = ld = c = 0
        top: collections.Counter = collections.Counter()
        ex_yes, ex_no = [], []
        for log in logs:
            for head, body in entries(log):
                n += 1
                hh = hits(pats, head)
                first = next((b for b in body if b.strip()), "")
                lh = hits(pats, head + "\n" + first)
                ch = hits(pats, "\n".join([head, *body]))
                h += bool(hh)
                ld += bool(lh)
                c += bool(ch)
                top.update(lh)
                (ex_yes if lh else ex_no).append(head[:90])
        pct = lambda k: f"{k}/{n} ({100 * k // n if n else 0}%)"  # noqa: E731
        tops = ", ".join(f"{p} {k}" for p, k in top.most_common(3))
        print(f"{role:<6} {len(logs):>4} {n:>7} {pct(h):>13} {pct(ld):>13} {pct(c):>13}  {tops}")
        for label, ex in (("  specialist", ex_yes), ("  general   ", ex_no)):
            for e in ex[: a.show]:
                print(f"{label}  {e}")
    print(
        "Layer: textual (what the logs name). Content is an upper bound: a marker in a line quoted from "
        "another seat counts. Denominator: every ##/### heading and top-level time bullet in the window's logs, per role."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
