#!/usr/bin/env python3
"""Corpus citation census — how often is each pattern / methodology entry actually cited?

Standing item 7a (corpus pruning & consolidation, PM-approved 2026-10-01 "if done carefully with a
thoroughly audited plan"). Step 1 of that plan: re-measure, because the May 2026 figure (~60%
zero-citation) is five months stale. Regenerate this, never copy its numbers forward.

What counts as a citation (stated so the audit can challenge it — m-43, name the layer):
  - An entry's identifier appears in a tracked file OTHER than the entry itself and the catalog
    indexes (README / INDEX / META-PATTERNS / pattern-000-template).
  - Identifier forms: patterns -> "pattern-NNN" / "Pattern-NNN" / "Pattern NNN" (case-insensitive);
    methodology -> "methodology-NN" / "m-NN" (word-bounded; zero-padded or not).
  - Sources are split into LIVE (instructions agents actually load or run: CLAUDE.md, .claude/,
    docs/ excluding omnibus logs, scripts/, services/, tests/, web/) and HISTORICAL (dev/, mailboxes/,
    docs/omnibus-logs/). An entry cited only historically was used once and is not load-bearing now.
    That is the pruning signal, not zero-total.

What this does NOT measure (denominator honesty — m-44):
  - Paraphrased use without the identifier (an agent applying m-43's idea without citing "m-43").
  - Citations in untracked files, the shared memory pool (~/.claude-pm, outside git), or other repos.
  So zero-LIVE is a candidate for review, never a verdict.

Usage: python3 scripts/corpus-citation-census.py [--md]   (TSV by default; --md for a table)
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAT_DIR = "docs/internal/architecture/patterns"
METH_DIR = "docs/internal/development/methodology-core"
INDEX_NAMES = {"README.md", "INDEX.md", "META-PATTERNS.md", "pattern-000-template.md"}
HISTORICAL_PREFIXES = ("dev/", "mailboxes/", "docs/omnibus-logs/")


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True, check=True
    ).stdout
    return [
        f
        for f in out.splitlines()
        if f.endswith((".md", ".py", ".sh", ".yml", ".yaml", ".json", ".txt", ".csv", ".tsv"))
    ]


COMBINED = re.compile(r"\b(?:pattern[- ]0*(\d+)|methodology-0*(\d+)|m-0*(\d+))\b", re.I)


def entries() -> list[tuple[str, int, str]]:
    """(kind, number, path) for every numbered pattern and methodology entry."""
    found = []
    for p in sorted((ROOT / PAT_DIR).glob("pattern-[0-9]*.md")):
        m = re.match(r"pattern-(\d+)", p.name)
        if m and p.name not in INDEX_NAMES:
            found.append(("pattern", int(m.group(1)), f"{PAT_DIR}/{p.name}"))
    for p in sorted((ROOT / METH_DIR).glob("methodology-[0-9]*.md")):
        m = re.match(r"methodology-(\d+)", p.name)
        if m:
            found.append(("methodology", int(m.group(1)), f"{METH_DIR}/{p.name}"))
    return found


def main() -> int:
    md = "--md" in sys.argv
    ents = entries()
    own = {path: (kind, n) for kind, n, path in ents}
    live: dict[tuple[str, int], int] = {(k, n): 0 for k, n, _ in ents}
    hist: dict[tuple[str, int], int] = {(k, n): 0 for k, n, _ in ents}
    # ONE pass per file with ONE combined regex (a per-entry scan was 145 x ~30k files: too slow).
    for f in tracked_files():
        if Path(f).name in INDEX_NAMES:
            continue
        try:
            t = (ROOT / f).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        ids = set()
        for m in COMBINED.finditer(t):
            if m.group(1):
                ids.add(("pattern", int(m.group(1))))
            else:
                ids.add(("methodology", int(m.group(2) or m.group(3))))
        ids.discard(own.get(f))  # an entry citing itself doesn't count
        bucket = hist if f.startswith(HISTORICAL_PREFIXES) else live
        for key in ids:
            if key in bucket:
                bucket[key] += 1
    rows = [(k, Path(p).stem, live[(k, n)], hist[(k, n)]) for k, n, p in ents]
    if md:
        print("| kind | entry | live files | historical files |\n|---|---|---:|---:|")
        for r in rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
    else:
        print("kind\tentry\tlive\thistorical")
        for r in rows:
            print("\t".join(map(str, r)))
    for kind in ("pattern", "methodology"):
        sub = [r for r in rows if r[0] == kind]
        zl = sum(1 for r in sub if r[2] == 0)
        zt = sum(1 for r in sub if r[2] == 0 and r[3] == 0)
        print(
            f"# {kind}: {len(sub)} entries; zero-LIVE {zl} ({zl * 100 // max(len(sub), 1)}%); "
            f"zero-TOTAL {zt} ({zt * 100 // max(len(sub), 1)}%)",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
