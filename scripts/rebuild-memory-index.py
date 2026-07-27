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
    "⚠️ **This file has TWO independent read limits and is SILENTLY TRUNCATED past either** — "
    "trailing entries vanish for every agent that loads it, with no error and no sign anything is "
    "missing. **(1) ~24KB of bytes** — it had reached 41.4KB (~40% of entries invisible, including "
    "most of the `reference` bucket) before HOST caught it 2026-07-25. **(2) ~200 LINES** — a "
    "separate ceiling that the byte count does NOT imply, found by PA 2026-07-26 at 194 lines while "
    "the byte guard was reporting a comfortable green. `scripts/rebuild-memory-index.py` now refuses "
    "to write past either, and warns from 90%."
)
out.append("")
out.append(
    "**The line limit cannot be fixed by shortening text.** One entry = one line, so with "
    f"{len(files)} memories on disk the floor is {len(files)} lines before any header — the real "
    "options are prune/merge, per-type index files with a router, or a denser entry format "
    "(cheapest, and worst for recall, since the description is what makes an index useful). "
    "**That is a governance decision about the whole cohort's shared pool, not a formatting "
    "choice for whoever trips the limit.** ⚠️ **Memory files are NOT under version control — "
    "deletion is irreversible. Export to a git-tracked file BEFORE pruning anything.**"
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

# ── TWO independent limits. Guarding one and reporting green is the exact failure
# this script was written to fix, one dimension over. (PA, 2026-07-26: the byte
# guard passed at 20.4KB while the file sat at 194 lines against a ~200 ceiling.)
LIMIT = 24000          # bytes — silent read truncation
LINE_LIMIT = 200       # lines — separate read ceiling, NOT implied by the byte count
WARN_AT = 0.90         # surface pressure before it becomes a refusal

n_lines = body.count("\n") + 1
# len(str) counts CHARACTERS. The limit is BYTES, and this file is full of multibyte
# UTF-8 (⚠️ — × •). Measuring the wrong unit under-counted by ~800B (4%) and would have
# permitted ~24,968 real bytes at a "24,000" limit — i.e. silent truncation, from the
# guard built to prevent it. (HOST, 2026-07-26 — third dimension error in this instrument.)
n_bytes = len(body.encode("utf-8"))
breaches = []
if n_bytes > LIMIT:
    breaches.append(f"{n_bytes:,} bytes > {LIMIT:,}")
if n_lines > LINE_LIMIT:
    breaches.append(f"{n_lines:,} lines > {LINE_LIMIT:,}")
if breaches:
    raise SystemExit(
        "REFUSING TO WRITE: " + " AND ".join(breaches) + ".\n"
        "Past either limit, trailing entries vanish for every agent that loads the file, with no error.\n"
        "NOTE: one entry = one line, so the LINE limit cannot be fixed by shortening descriptions —\n"
        "it needs a prune/merge or a format change. See MEMORY.md's own header for the options.\n"
        "⚠️  Memory files are NOT under version control. EXPORT BEFORE YOU DELETE ANYTHING."
    )

(MEMDIR / "MEMORY.md").write_text(body, encoding="utf-8")
print(f"index rebuilt: {len(files)} entries, {n_bytes:,} bytes, {n_lines} lines "
      f"({LIMIT-n_bytes:,}B / {LINE_LIMIT-n_lines} lines under the limits)")
# Pressure warnings — a green write that is one entry from truncating is not a healthy signal.
if n_bytes > LIMIT * WARN_AT:
    print(f"⚠️  BYTES at {100*n_bytes/LIMIT:.0f}% of limit")
if n_lines > LINE_LIMIT * WARN_AT:
    print(f"⚠️  LINES at {100*n_lines/LINE_LIMIT:.0f}% of limit ({LINE_LIMIT-n_lines} left). "
          f"One entry = one line: this needs prune/merge or a format change, not shorter text.")
for t in TYPE_ORDER:
    if t in buckets:
        print(f"  {t:12s} {len(buckets[t])}")
