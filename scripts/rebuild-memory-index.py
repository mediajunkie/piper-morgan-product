#!/usr/bin/env python3
"""Rebuild the shared memory pool's MEMORY.md index from the actual directory listing.

WHY THIS EXISTS, and why it refuses to write past a size limit
--------------------------------------------------------------
Two failure modes, both silent, both hit on 2026-07-25:

1. INDEX DRIFT. The pre-migration index had 146 entries against 162 real files — it was
   hand-maintained, so it fell behind and nothing said so. Cure: generate from `ls`, never
   from a prior index. A rebuild cannot under-report what's on disk.

2. SILENT READ TRUNCATION (the subtler one). MEMORY.md has a hard read limit of ~24KB and is
   truncated past it with NO error — trailing entries simply vanish for every agent that loads
   the file. The first filesystem-generated index was 41.4KB, so ~40% of entries (most of the
   `reference` bucket) were invisible while the file itself was provably complete. Verifying
   "166 indexed == 166 on disk" passed cleanly and proved nothing, because the completeness
   was checked at the wrong layer.

   Cure: slug-only entry lines (markdown links duplicate every slug in link text AND target,
   which cost 15.7KB of a ~17KB budget — the entire space for descriptions), short descriptions,
   and a hard guard that REFUSES to write an oversized index rather than emitting one that
   degrades quietly. Fail loudly beats truncate silently.

Found by HOST 2026-07-25; generator hardened by CIO the same day so a rebuild can't reintroduce it.
Run after adding or removing memories.
"""

import re
from pathlib import Path

MEMDIR = Path(
    "/Users/xian/.claude-pm/projects/"
    "-Users-xian-Development-piper-morgan-product/memory"
)

TYPE_ORDER = ["user", "project", "feedback", "reference", "(untyped)"]
TYPE_HEADING = {
    "user": "User — who xian is",
    "project": "Project — ongoing work, goals, constraints",
    "feedback": "Feedback — how this cohort works, and the corrections behind it",
    "reference": "Reference — external pointers and environment facts",
    "(untyped)": "Untyped",
}


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    desc, mtype = None, None
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm = text[3:end] if end != -1 else ""
        m = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
        if m:
            desc = m.group(1).strip().strip('"').strip("'")
        m = re.search(r"^\s*type:\s*(\w+)\s*$", fm, re.MULTILINE)
        if m:
            mtype = m.group(1).strip()
    if not desc:
        # fall back to first non-empty, non-frontmatter, non-heading line
        body = text.split("\n---", 1)[-1] if text.startswith("---") else text
        for line in body.split("\n"):
            s = line.strip()
            if s and not s.startswith("#") and not s.startswith("---"):
                desc = s
                break
    if not desc:
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        desc = m.group(1).strip() if m else "(no description)"
    # collapse + truncate
    desc = re.sub(r"\s+", " ", desc)
    desc = re.sub(r"\*\*(.+?)\*\*", r"\1", desc)
    if len(desc) > 60:
        desc = desc[:57].rsplit(" ", 1)[0] + "…"
    return desc, (mtype or "(untyped)")


files = sorted(p for p in MEMDIR.glob("*.md") if p.name != "MEMORY.md")
buckets = {}
for p in files:
    desc, mtype = parse(p)
    buckets.setdefault(mtype, []).append((p.name, desc))

out = []
out.append("# Memory index — Piper Morgan cohort (pipermorgan.ai / Amber)")
out.append("")
out.append(
    f"**{len(files)} memories on disk.** Generated from the actual directory listing, "
    "never from a prior index."
)
out.append("")
out.append(
    "**Each entry is `<slug> — hook`. The slug IS the filename** — open `<slug>.md` in this "
    "directory. Markdown links are deliberately omitted: duplicating every slug in link text "
    "*and* target consumed ~15.7KB of a ~17KB budget, i.e. the entire space for descriptions."
)
out.append("")
out.append(
    "⚠️ **This file has a hard read limit (~24KB) and is SILENTLY TRUNCATED past it** — trailing "
    "entries vanish for every agent that loads it, with no error and no sign anything is missing. "
    "It had reached 41.4KB (~40% of entries invisible, including most of the `reference` bucket) "
    "before HOST caught it 2026-07-25. **Keep every entry to ONE short line; put detail in the "
    "topic file, never here.** Rebuild with `scripts/rebuild-memory-index.py`, which refuses to "
    "write an oversized index rather than emitting one that degrades quietly."
)
out.append("")
out.append(
    "**Provenance**: seeded 2026-07-25 from `dev/active/cio-memory-export-2026-07-24.md`, "
    "the verbatim export of the designinproduct.com pool. Memory is scoped per "
    "(account × project), so none of it transferred automatically at the account switch. "
    "This is the whole cohort's shared pool, not one role's — Claude Code keys memory by "
    "account and project, not by role, and on Amber it resolves to the git common dir, so "
    "every agent worktree off this repo shares it by construction."
)
out.append("")

for t in TYPE_ORDER:
    if t not in buckets:
        continue
    rows = sorted(buckets[t])
    out.append(f"## {TYPE_HEADING[t]} ({len(rows)})")
    out.append("")
    for name, desc in rows:
        out.append(f"- {name[:-3]} — {desc}")
    out.append("")

body = "\n".join(out)
LIMIT = 24000
if len(body) > LIMIT:
    raise SystemExit(
        f"REFUSING TO WRITE: index is {len(body):,} bytes, over the ~{LIMIT:,} silent-read-truncation "
        f"limit. Past this, trailing entries vanish for every agent that loads the file, with no error. "
        f"Shorten descriptions or drop a field — do NOT just write it."
    )
(MEMDIR / "MEMORY.md").write_text(body, encoding="utf-8")
print(f"index rebuilt: {len(files)} entries, {len(body):,} bytes ({LIMIT-len(body):,} under the limit)")
for t in TYPE_ORDER:
    if t in buckets:
        print(f"  {t:12s} {len(buckets[t])}")
