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

CALIBRATED 2026-11-07: the marker figures don't measure it. Against two blind raters on 220 entries
(20 per role, 10-30 to 11-05), every figure scored kappa 0.11 to 0.12, while the raters agreed with each
other at kappa 0.87. So the headline is now the rater method, and this script runs its two mechanical
halves (the markers doc's "Rater method" section has the brief):
  --sample DIR   draw --per-role entries per role (seeded), write blind packs pack-A/B/C.md and key.json
  --score DIR    read DIR/labels-r1*.json and DIR/labels-r2*.json, print each rater's share per role,
                 their agreement and kappa, and the disagreements for CIO to adjudicate
The marker mode (no --sample/--score) is kept as the v0 record, not as a figure to quote.

Usage: scripts/specialist-share.py [--from YYYY-MM-DD] [--to YYYY-MM-DD] [--role ROLE] [--show N]
                                   [--sample DIR [--per-role 20] [--seed N] | --score DIR]
  --from/--to  window, inclusive (default: the 7 days ending yesterday)
  --show N     also print N example headings per side for each role (to spot-check the markers)

Layer: textual. It says what the logs name, not what the work was. Cost: one read of ~80 logs; a rated
run adds two Sonnet raters (about 90k and 160k tokens on 11-07).
Benefit: the marker figures, none (kappa 0.11, 11-07 calibration). The rater method: inter-rater kappa
0.87 on its first use. Review: the 12-18 run.
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


def role_logs(role: str, start: dt.date, end: dt.date) -> list[Path]:
    logs = []
    d = start
    while d <= end:
        logs += sorted((ROOT / "dev" / d.strftime("%Y/%m/%d")).glob(f"*-{role}-code-log.md"))
        d += dt.timedelta(days=1)
    return logs


CARDS = {"exec": "BRIEFING-ESSENTIAL-CHIEF-STAFF.md", "lead": "BRIEFING-ESSENTIAL-LEAD-DEV.md",
         "arch": "BRIEFING-ESSENTIAL-ARCHITECT.md", "pa": "BRIEFING-piper-alpha.md"}  # fmt: skip
# Three packs so each rater's read stays a size one subagent can take in (11-07: 58k to 73k chars each).
PACKS = {
    "A": ["exec", "lead", "arch", "ppm"],
    "B": ["cxo", "comms", "docs", "pa"],
    "C": ["web", "host", "cio"],
}


def role_card(role: str) -> str:
    name = CARDS.get(role, f"BRIEFING-ESSENTIAL-{role.upper()}.md")
    text = (ROOT / "docs" / "briefing" / name).read_text()
    m = re.search(r"## Role card.*?(?=<!-- /ROLE-CARD -->|\n## )", text, re.S)
    return m.group(0).strip() if m else f"(no role card found in {name})"


def sample(out: Path, start: dt.date, end: dt.date, per_role: int, seed: int, markers) -> None:
    import json
    import random

    rng = random.Random(seed)
    out.mkdir(parents=True, exist_ok=True)
    key = {}
    for pack, roles in PACKS.items():
        parts = [f"# Rater pack {pack}\n"]
        for role in roles:
            pool = [
                (log.name, h, b) for log in role_logs(role, start, end) for h, b in entries(log)
            ]
            picked = rng.sample(pool, min(per_role, len(pool)))
            parts.append(
                f"\n## ROLE: {role}\n\n### Role card (what counts as this role's specialist work)\n\n"
            )
            parts.append(f"{role_card(role)}\n\n### Entries\n")
            for i, (name, head, body) in enumerate(picked, 1):
                eid = f"{role}-{i:02d}"
                lines = [b for b in body if b.strip()]
                parts.append(
                    f"\n#### {eid}  ({name})\nHEADING: {head}\nBODY:\n{chr(10).join(lines)[:1100]}\n"
                )
                pats = markers[role]
                key[eid] = dict(
                    log=name, head=head[:100], pool=len(pool),
                    heading=bool(hits(pats, head)),
                    lead=bool(hits(pats, head + "\n" + (lines[0] if lines else ""))),
                    content=bool(hits(pats, "\n".join([head, *body]))),
                )  # fmt: skip
        (out / f"pack-{pack}.md").write_text("".join(parts))
    (out / "key.json").write_text(json.dumps(key, indent=1))
    print(
        f"sampled {len(key)} entries ({per_role} per role, seed {seed}, {start} to {end}) into {out}"
    )
    print(
        "Next: two raters on pack-A/B/C.md, each writing labels-r1*.json or labels-r2*.json; then --score."
    )


def score(d: Path) -> int:
    import json

    key = json.loads((d / "key.json").read_text())
    raters = []
    for tag in ("r1", "r2"):
        labels = {}
        for f in sorted(d.glob(f"labels-{tag}*.json")):
            labels.update(json.loads(f.read_text()))
        raters.append({k: v["label"] == "S" for k, v in labels.items() if k in key})
    ids = sorted(set(key) & set(raters[0]) & set(raters[1]))
    if not ids:
        sys.exit(f"no ids labelled by both raters in {d}")

    def kappa(x: list[bool], y: list[bool]) -> float:
        n = len(x)
        po = sum(a == b for a, b in zip(x, y)) / n
        px, py = sum(x) / n, sum(y) / n
        pe = px * py + (1 - px) * (1 - py)
        return (po - pe) / (1 - pe) if pe < 1 else 1.0

    r1, r2 = [raters[0][i] for i in ids], [raters[1][i] for i in ids]
    print(
        f"specialist-share --score · {len(ids)} entries labelled by both raters (of {len(key)} sampled)"
    )
    print(f"{'role':<6} {'r1 S':>5} {'r2 S':>5} {'agree':>6}  share (mean of raters)")
    for role in PACKS["A"] + PACKS["B"] + PACKS["C"]:
        rid = [i for i in ids if i.startswith(role + "-")]
        if not rid:
            continue
        s1, s2 = sum(raters[0][i] for i in rid), sum(raters[1][i] for i in rid)
        ag = sum(raters[0][i] == raters[1][i] for i in rid)
        print(
            f"{role:<6} {s1:>5} {s2:>5} {ag:>3}/{len(rid):<3} {100 * (s1 + s2) // (2 * len(rid))}%"
        )
    print(
        f"raters: {sum(a == b for a, b in zip(r1, r2))}/{len(ids)} agree, kappa {kappa(r1, r2):.2f}"
    )
    for m in ("heading", "lead", "content"):
        print(f"marker figure '{m}' against r1: kappa {kappa([key[i][m] for i in ids], r1):.2f}")
    dis = [i for i in ids if raters[0][i] != raters[1][i]]
    print(f"to adjudicate ({len(dis)}): {' '.join(dis)}")
    print(
        "Layer: two model raters reading log text against each role's card. Denominator: the sample, not every entry."
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    yesterday = dt.date.today() - dt.timedelta(days=1)
    ap.add_argument("--from", dest="start", default=str(yesterday - dt.timedelta(days=6)))
    ap.add_argument("--to", dest="end", default=str(yesterday))
    ap.add_argument("--role")
    ap.add_argument("--show", type=int, default=0)
    ap.add_argument("--sample", type=Path)
    ap.add_argument("--per-role", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20261107)
    ap.add_argument("--score", type=Path)
    a = ap.parse_args()
    start, end = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    if a.score:
        return score(a.score)
    markers = load_markers()
    if a.sample:
        sample(a.sample, start, end, a.per_role, a.seed, markers)
        return 0
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
        logs = role_logs(role, start, end)
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
