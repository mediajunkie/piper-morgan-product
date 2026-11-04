#!/usr/bin/env python3
"""check-concept-links.py — evaluate mechanisms and their concept docs against each other, both ways.

xian, 2026-10-14 (on the methodology audit, "emphatically approved"): "The reasons exist and point to
mechanisms. The mechanisms point back to their reasons for existing and can be eval'd against them."
This is the textual half of that evaluation. For every process mechanism, it checks:

  1. Does it declare a concept?  A line `Concept: <path>.md` in the file (the sunset-or-renew rule's
     fifth line, since 2026-10-14).
  2. Does that path resolve?      The doc exists in this checkout.
  3. Does the doc point back?     The doc's text names the mechanism (its filename, or a skill's name).

Mechanisms scanned (the audit's classes): .claude/hooks/*.sh and *.py, scripts/git-hooks/*,
.claude/skills/*/SKILL.md, .github/workflows/*.yml, and scripts/*.sh and scripts/*.py.
Scripts in scripts/ include product and build helpers, so they're counted separately and listed only
with --all. A file can name several concept docs on one line; it passes if any one resolves and
points back.

Exit 0 = every declared concept resolves and points back. Exit 1 = at least one BROKEN link (a path
that doesn't exist, or a doc that doesn't name the mechanism). A missing Concept line was due by
2026-11-01 (mechanism-sunset-or-renew.md) and is counted. With --ratchet it is also failed when any
class's missing count differs from its ceiling in RATCHET below: above it, a new mechanism arrived
without a line; below it, a line landed and the ceiling must come down in the same commit. The count
only goes down. scripts/ joined on 2026-11-03 (methodology audit R15; Lead's yes with four conditions):
a product script satisfies it with any existing .md that names it (an ADR, design record, ops recipe or
the current-architecture doc for its area), so its owner writes one pointer sentence, not a new doc.

Usage: scripts/check-concept-links.py [--all] [--ratchet]
  --all      also lists scripts/ files with no Concept line
  --ratchet  exit 1 when any class's missing count differs from its ceiling (asserted exactly)

Layer: textual. It checks that the pointers exist and agree, not that the doc's claims match the
code's behaviour. That part is a reader's job (the audit's spot-checks).

Cost: one read of about 400 files, under a second. Benefit: none yet: measuring (first run 2026-10-14).
Review: 2026-12-08. Owner: CIO.
Concept: docs/internal/operations/mechanism-sunset-or-renew.md
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True
    ).stdout.strip()
)
CONCEPT = re.compile(r"Concept:\s*(.+)")
MD_PATH = re.compile(r"[\w./-]+\.md")

CLASSES = [
    (
        "hooks",
        lambda: sorted(
            p
            for p in (ROOT / ".claude/hooks").glob("*")
            if p.suffix in (".sh", ".py") and p.is_file()
        ),
    ),
    ("git-hooks", lambda: sorted(p for p in (ROOT / "scripts/git-hooks").glob("*") if p.is_file())),
    ("skills", lambda: sorted((ROOT / ".claude/skills").glob("*/SKILL.md"))),
    ("workflows", lambda: sorted((ROOT / ".github/workflows").glob("*.yml"))),
    (
        "scripts",
        lambda: sorted(
            p for p in (ROOT / "scripts").glob("*") if p.suffix in (".sh", ".py") and p.is_file()
        ),
    ),
]


def name_of(p: Path) -> str:
    return p.parent.name if p.name == "SKILL.md" else p.name


def declared(p: Path) -> list[str]:
    try:
        text = p.read_text(errors="replace")
    except OSError:
        return []
    out: list[str] = []
    for m in CONCEPT.finditer(text):
        for path in MD_PATH.findall(m.group(1)):
            if "<" in path:  # a template placeholder such as <doc path>.md
                continue
            out.append(path.removeprefix("./"))  # not lstrip: that ate the dot of .claude/
    return out


def resolve(path: str, mech: Path) -> Path | None:
    for cand in (ROOT / path, mech.parent / path):
        if cand.is_file():
            return cand
    return None


# Missing-Concept ceilings, asserted exactly: frozen 2026-11-01 for the process classes and 2026-11-03
# for scripts (the landing day's count, after that day's lines), and lowered in the commit that adds a
# line or deletes a mechanism, never raised. git-hooks' 2 are pre-commit and pre-push: any edit makes
# the installed copy differ from source until xian reinstalls, so their lines wait for a functional
# edit (hooks-registry.md).
RATCHET = {"hooks": 0, "git-hooks": 2, "skills": 0, "workflows": 0, "scripts": 247}


def main() -> int:
    show_all = "--all" in sys.argv[1:]
    ratchet = "--ratchet" in sys.argv[1:]
    broken: list[str] = []
    totals: dict[str, list[int]] = {}
    missing: dict[str, list[str]] = {}
    for cls, files in CLASSES:
        linked = none = 0
        for p in files():
            rel = str(p.relative_to(ROOT))
            paths = declared(p)
            if not paths:
                none += 1
                missing.setdefault(cls, []).append(rel)
                continue
            name = name_of(p)
            ok = False
            reasons = []
            for path in paths:
                doc = resolve(path, p)
                if doc is None:
                    reasons.append(f"{path} does not exist")
                    continue
                if name in doc.read_text(errors="replace"):
                    ok = True
                    break
                reasons.append(f"{path} does not name {name}")
            if ok:
                linked += 1
            else:
                broken.append(f"BROKEN  {rel}: " + "; ".join(reasons))
        totals[cls] = [linked, none, len(files())]

    for line in broken:
        print(line)
    for cls, rows in missing.items():
        if cls == "scripts" and not show_all:
            continue
        for rel in rows:
            print(f"NO-CONCEPT  {rel}")
    print()
    print(f"{'class':<10} {'linked':>6} {'broken':>6} {'none':>5} {'total':>6}")
    nb = {
        cls: sum(1 for b in broken if b.split()[1].startswith(prefix))
        for cls, prefix in (
            ("hooks", ".claude/hooks"),
            ("git-hooks", "scripts/git-hooks"),
            ("skills", ".claude/skills"),
            ("workflows", ".github/workflows"),
        )
    }
    nb["scripts"] = len(broken) - sum(nb.values())
    for cls, (linked, none, total) in totals.items():
        print(f"{cls:<10} {linked:>6} {nb[cls]:>6} {none:>5} {total:>6}")
    t = [sum(v[i] for v in totals.values()) for i in range(3)]
    print(f"{'all':<10} {t[0]:>6} {len(broken):>6} {t[1]:>5} {t[2]:>6}")
    print(
        "check-concept-links: textual layer (pointers exist and agree), not behaviour. "
        "Missing Concept lines were due 2026-11-01 (mechanism-sunset-or-renew.md)."
    )
    over = [
        f"RATCHET  {cls}: {totals[cls][1]} missing, ceiling {ceiling}"
        + (
            " (a new mechanism has no Concept: line)"
            if totals[cls][1] > ceiling
            else f" (lower RATCHET[{cls!r}] to {totals[cls][1]} in this commit)"
        )
        for cls, ceiling in RATCHET.items()
        if cls in totals and totals[cls][1] != ceiling
    ]
    if ratchet:
        for line in over:
            print(line)
    return 1 if broken or (ratchet and over) else 0


if __name__ == "__main__":
    sys.exit(main())
