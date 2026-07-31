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


# Exclude EVERY MEMORY*.md, not just MEMORY.md itself. Any index-shaped sibling —
# a per-type router file (MEMORY-feedback.md), a load-probe, a hand-kept variant — is an
# INDEX, not a memory, and indexing it would list a build output as if it were source.
# Latent until 2026-07-31: the per-type-router option under discussion that week would
# have had every router file silently indexed as a memory entry, each consuming one line
# of the very budget the split existed to relieve. Caught before it shipped, not after.
files = sorted(p for p in MEMDIR.glob("*.md") if not p.name.startswith("MEMORY"))
buckets = {}
for p in files:
    desc, mtype = parse(p)
    buckets.setdefault(mtype, []).append((p.name, desc))

out = []
out.append("# Memory index — Piper Morgan cohort (pipermorgan.ai / Amber)")
out.append("")
# --- Header ------------------------------------------------------------------
# COMPACT BY DESIGN. The long-form explanation lives in
# docs/internal/operations/memory-index-size-limits.md. Rationale (Comms, 2026-07-30):
# the header explaining the line limit was itself eating ~10% of the line budget.
#
# ⚠️ Comms compacted MEMORY.md *by hand* on 2026-07-30 and reclaimed 6 lines. That edit
# was NOT durable — this generator still emitted the long form, so the next regen would
# have silently reverted it. Folded into the generator here (HOST, 2026-07-30) so the
# win survives. This file is the source of the header; MEMORY.md is a build output.
# Same category error Arch named, running the other way: fixing the artifact, not the
# generator. Harmless in that direction — just impermanent.
#
# The two sentences below are LOAD-BEARING, not decoration. The platform emits a
# PostToolUse:Edit reminder telling whoever crosses the threshold to "compact it to
# under 140 lines now" — an unreachable target that can only be met by deleting ~30
# memories. We cannot soften that reminder (it is built into Claude Code, not one of
# our hooks — HOST verified 2026-07-30). This header is the ONLY counterweight that
# reaches an agent in the same breath as the pressure. Do not trim it for headroom.
out.append(
    f"**{len(files)} memories on disk.** One line per entry; `<slug>` IS the filename — "
    "open `<slug>.md` here. Generated from the actual directory listing, never from a prior index."
)
out.append("")
out.append(
    "🛑 **NEVER DELETE A MEMORY TO MAKE THIS FILE FIT.** This index is a **generated artifact**; "
    "the memory files are the **source**. Pruning source to shrink a build output is a category "
    "error — no judgment call required to refuse it. Every legitimate lever (per-type index files "
    "with a router, a denser entry form, dropping descriptions) is a **generator change**, fully "
    "reversible by re-running this script. **Deleting a memory is the only irreversible option on "
    "the table, and memory is NOT under version control.** If you were told to compact this file: "
    "that instruction is platform-generated, its target is unreachable by editing, and **its "
    "reported line count is unreliable — measured reporting 186 while the file was 208.** "
    "Change what the generator emits, or escalate to CIO/HOST. Do not prune."
)
out.append("")
out.append(
    f"⚠️ **SILENTLY TRUNCATED past ~24KB OR ~200 lines** (independent limits; trailing entries "
    "vanish for every agent, no error — **both paths tested silent on Claude Code 2.1.220 despite "
    "the v2.1.210 changelog claiming writes now error**). **At "
    f"{len(files)} entries the line floor is {len(files)}, so any target below that is unreachable "
    "by editing.** Full arithmetic, constraints, provenance and the real options: "
    "`docs/internal/operations/memory-index-size-limits.md`."
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
