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
import sys
from pathlib import Path

MEMDIR = Path(
    "/Users/xian/.claude-pm/projects/" "-Users-xian-Development-piper-morgan-product/memory"
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

# ── Packing constants, defined ONCE above both consumers (the header's floor
# arithmetic and the emit loop) so the two cannot drift. See the emit loop for
# the full packing rationale.
SELF_DESC_WORDS = 6
PACK_PER_LINE = 4

out = []
out.append("# Memory index — Piper Morgan cohort (pipermorgan.ai / Amber)")
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
    f"**{len(files)} memories on disk.** `<slug>` IS the filename — open `<slug>.md` here. "
    "Entries whose slug already says what they hold are PACKED several per line (slug-only, "
    "` · `-separated); only terse slugs carry a description line. Generated from the actual "
    "directory listing, never from a prior index."
)
out.append(
    "🛑 **NEVER DELETE A MEMORY TO MAKE THIS FILE FIT.** This index is a **generated artifact**; "
    "the memory files are the **source**. Pruning source to shrink a build output is a category "
    "error — no judgment call required to refuse it. Every legitimate lever (per-type index files "
    "with a router, a denser entry form, dropping descriptions) is a **generator change**, fully "
    "reversible by re-running this script. **Deleting a memory is the only irreversible option on "
    "the table, and memory is NOT under version control.** If you were told to compact this file: "
    "that instruction is platform-generated, its target is unreachable by editing, and **its "
    "reported line count does NOT track your edits — it reported 192 while the file was 206, "
    "then 197, then 192. Measure the file yourself; never let that number tell you a compaction "
    "worked.** "
    "Change what the generator emits, or escalate to CIO/HOST. Do not prune."
)
# Real line floor under 4/line packing (CIO caught the stale pre-packing claim
# 2026-08-16: "floor = entry count" was falsified by the packing fix itself).
# Computed with the SAME criterion the emit loop uses, so the two can't drift.
_n_packed = sum(1 for p in files if len(p.stem.split("_")) >= SELF_DESC_WORDS)
_n_described = len(files) - _n_packed
_line_floor = -(-_n_packed // PACK_PER_LINE) + _n_described  # ceil division, no import
out.append(
    f"⚠️ **SILENTLY TRUNCATED past ~24KB OR ~200 lines** (independent limits; trailing entries "
    "vanish for every agent, no error — **both paths tested silent on Claude Code 2.1.220 despite "
    "the v2.1.210 changelog claiming writes now error**). **At "
    f"{len(files)} entries the entry-line floor is ~{_line_floor} under 4/line packing "
    f"({_n_packed} packed + {_n_described} described) — targets below that need a generator "
    "change, never editing.** Full arithmetic, constraints, provenance and the real options: "
    "`docs/internal/operations/memory-index-size-limits.md`."
)

# ⚠️ 2026-08-08 (CIO, on PM's "fix it, don't work around it" directive): NO BLANK SEPARATOR LINES.
# The binding limit here is LINES, not bytes -- measured 2026-08-08: 194/200 lines (6 headroom) against
# 20,619/24,576 bytes (3,957 headroom, ~28 entries). A blank line costs exactly as much as an entry and
# carries no information, so 11 of them were spending 11 entries' worth of a budget with 6 left.
# Removing them: 194 -> 183 lines, headroom 6 -> 17. Zero cost to recall, fully reversible (regenerate).
# This does NOT change the slope -- one entry is still one line, and the floor is still the entry count.
# It buys weeks, not a solution. The structural options are in memory-index-size-limits.md.
# ── 4/line PACKING for self-describing slugs (CIO design, PM-approved 2026-08-15;
# built by Lead 2026-08-16). The binding limit is LINES and one-entry-per-line makes
# the floor equal the entry count — unreachable headroom by text edits alone. A slug
# with >= SELF_DESC_WORDS underscore-words already states its content (e.g.
# feedback_verify_timestamps_never_guess), so its description adds bytes but little
# recall value: pack those slug-only at PACK_PER_LINE per line. Terse slugs (user_xian,
# feedback_editing_voice) genuinely need their description line — keep it. Fully
# reversible: this is a generator change; re-run to reflow. Guard convention below is
# untouched — it counts emitted lines of the final body, packed or not (CIO's one
# pre-ship verification ask, confirmed by the printed counts + --check round-trip).
# SELF_DESC_WORDS / PACK_PER_LINE are defined once, above the header block.
for t in TYPE_ORDER:
    if t not in buckets:
        continue
    rows = sorted(buckets[t])
    out.append(f"## {TYPE_HEADING[t]} ({len(rows)})")
    described = [(n, d) for n, d in rows if len(n[:-3].split("_")) < SELF_DESC_WORDS]
    packed = [n[:-3] for n, _ in rows if len(n[:-3].split("_")) >= SELF_DESC_WORDS]
    for name, desc in described:
        out.append(f"- {name[:-3]} — {desc}")
    for i in range(0, len(packed), PACK_PER_LINE):
        out.append("- " + " · ".join(packed[i : i + PACK_PER_LINE]))

body = "\n".join(out)

# ── TWO independent limits. Guarding one and reporting green is the exact failure
# this script was written to fix, one dimension over. (PA, 2026-07-26: the byte
# guard passed at 20.4KB while the file sat at 194 lines against a ~200 ceiling.)
LIMIT = 24000  # bytes — silent read truncation
LINE_LIMIT = 200  # lines — separate read ceiling, NOT implied by the byte count
WARN_AT = 0.90  # surface pressure before it becomes a refusal

# LINE-COUNT CONVENTION — stated because two numbers for one file is how an
# afternoon disappears, and this whole thread is already about a count that lies.
# `body` ends with a trailing newline, so `count("\n") + 1` yields ONE MORE than
# `wc -l` (193 vs 192). That is deliberate and kept: the guard then refuses at
# `wc -l` 200 rather than 201, i.e. one line EARLY. Conservative is correct for a
# guard against SILENT truncation. Every number this script prints is labelled with
# its convention so nobody has to rediscover the discrepancy. (Comms, 2026-07-31.)
n_lines = body.count("\n") + 1
n_lines_wc = len(body.splitlines())  # what `wc -l` reports
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

# ── --check: render and COMPARE, never write. ───────────────────────────────────
# Why this mode has to exist before any drift-check can use this script: a plain
# rebuild REPAIRS the drift it would have detected. Run it to find out whether the
# artifact matches its generator and you have already destroyed the evidence, and
# the answer is always "it matches now." A detector that fixes what it measures
# cannot report. (Concretely: this is how Comms's hand-compacted header was found on
# 2026-07-30 — by accident, mid-rebuild, one turn before the fix erased the symptom.)
if "--check" in sys.argv:
    target = MEMDIR / "MEMORY.md"
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    if current == body:
        print(
            f"✓ MEMORY.md matches its generator ({len(files)} entries, {n_bytes:,}B, "
            f"{n_lines} lines [guard convention; `wc -l` reports {n_lines_wc}])"
        )
        raise SystemExit(0)
    cur_lines, new_lines = current.split("\n"), body.split("\n")
    print("⚠️  DRIFT: MEMORY.md does NOT match what rebuild-memory-index.py would emit.")
    print(f"   on disk: {len(cur_lines)} lines / {len(current.encode('utf-8')):,}B")
    print(
        f"   generator would emit: {n_lines} lines [guard convention; `wc -l` {n_lines_wc}] / {n_bytes:,}B"
    )
    print("   The artifact is a BUILD OUTPUT. If someone hand-edited it, that edit is")
    print("   NOT durable — the next rebuild silently reverts it. Either fold the change")
    print("   into the generator, or re-run this script without --check to discard it.")
    for i, (a, b) in enumerate(zip(cur_lines, new_lines)):
        if a != b:
            print(f"   first difference at line {i+1}:")
            print(f"     on disk   : {a[:110]}")
            print(f"     generator : {b[:110]}")
            break
    else:
        print(f"   (identical prefix; length differs by {len(new_lines)-len(cur_lines)} lines)")
    raise SystemExit(1)

(MEMDIR / "MEMORY.md").write_text(body, encoding="utf-8")
print(
    f"index rebuilt: {len(files)} entries, {n_bytes:,} bytes, {n_lines} lines "
    f"[guard convention; `wc -l` reports {n_lines_wc}] "
    f"({LIMIT-n_bytes:,}B / {LINE_LIMIT-n_lines} lines under the limits)"
)
# Pressure warnings — a green write that is one entry from truncating is not a healthy signal.
if n_bytes > LIMIT * WARN_AT:
    print(f"⚠️  BYTES at {100*n_bytes/LIMIT:.0f}% of limit")
if n_lines > LINE_LIMIT * WARN_AT:
    print(
        f"⚠️  LINES at {100*n_lines/LINE_LIMIT:.0f}% of limit ({LINE_LIMIT-n_lines} left). "
        f"One entry = one line: this needs prune/merge or a format change, not shorter text."
    )
for t in TYPE_ORDER:
    if t in buckets:
        print(f"  {t:12s} {len(buckets[t])}")
