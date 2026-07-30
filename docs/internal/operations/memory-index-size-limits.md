# The memory index's size limits, and why they can't be fixed by editing

**Status**: operations reference. Moved here from `MEMORY.md`'s own header on 2026-07-30 by Comms, because the header explaining the line limit was itself consuming ~10% of the line budget.
**Subject**: `~/.claude-pm/projects/-Users-xian-Development-piper-morgan-product/memory/MEMORY.md` — the shared index loaded into every agent's context.

---

## Two independent read limits, and both truncate SILENTLY

Trailing entries vanish for every agent that loads the file, with no error and no sign anything is missing.

1. **~24KB of bytes.** It had reached 41.4KB — roughly 40% of entries invisible, including most of the `reference` bucket — before HOST caught it 2026-07-25.
2. **~200 LINES.** A separate ceiling that the byte count does **not** imply. Found by PA 2026-07-26 at 194 lines *while the byte guard was reporting a comfortable green.*

`scripts/rebuild-memory-index.py` now refuses to write past either and warns from 90%. A PostToolUse hook also warns on edit.

### ⚠️ The platform changelog claims this was fixed. **It does not hold for the line limit.** (HOST, tested 2026-07-30)

Claude Code **v2.1.210**: *"Memory writes that leave a MEMORY.md index over its read limit now produce an explicit error instead of silent truncation."* We run **2.1.220**. Read at face value, that retires this whole page.

**It does not.** Tested on a live seat at 2.1.220 — snapshot, pad past the ceiling, observe, restore byte-identical (sha verified):

| probe | resulting file | expected if the fix applied | actual |
|---|---|---|---|
| write that **crosses** 200 lines | 201 lines | explicit error | **succeeded, silently** |
| write while **already over** | 202 lines | explicit error | **succeeded, silently** |

**Limit of this finding, stated so nobody over-reads it**: both probes sat at ~19.6KB, well under the 25KB byte ceiling. The v2.1.210 error may be **byte-scoped** and simply never have covered lines. That reading and "the fix is broken" are not distinguishable from this evidence, and **the operational consequence is the same either way** — the limit we are near is the line limit, and it is silent.

**Do not stand down on this page's strength of a changelog entry.** A documented fix is a claim about a mechanism, not the mechanism. The probe costs ninety seconds; re-run it after any Claude Code upgrade.

### The built-in reminder is not ours, its target is unreachable, and its count is stale

The *"compact it to under 140 lines now"* nudge is **built into Claude Code** (v2.1.186), delivered as `hook_additional_context` / `hookName: "PostToolUse:Edit"`. It is **not** one of our hooks — all six in the project and user settings layers use `matcher: "Bash"` and none touch memory. **We cannot soften its wording**; our counterweight has to live in `MEMORY.md`'s own header, which is where an agent reads it at the moment it fires.

Two defects in it, both measured 2026-07-30:

1. **Its target is unreachable and it doesn't know that.** "Under 140 lines" against 170 one-line entries has a floor of 170. It requests deletion of ~30 memories in formatting language.
2. **Its line count is stale.** It reported `187` on both probes above — while the file was `201`, then `202`. An agent who complies is told a number that does not move, and the plausible next step is to **cut deeper**. Nobody has hit this because nobody has complied.

**Track record so far: three agents told to prune, three refused and escalated** — PA (194 lines, 07-26), CXO (192, 07-29), Comms (193, 07-30). Good outcome, unsafe design: what protects the shared pool today is judgment repeatedly exercised *against* a mechanism with hands. A norm that every agent must re-derive when they trip it is not yet a mechanism.

## Why the line limit cannot be fixed by shortening text

**One entry = one line.** So the floor is the number of memories on disk, before any header at all. The arithmetic is worth stating plainly because it keeps getting re-derived under time pressure:

| Date | Memories on disk | Line floor | Header | Total | Headroom to 200 |
|---|---|---|---|---|---|
| 2026-07-26 (PA) | ~163 | 163 | ~31 | 194 | 6 |
| 2026-07-30 (Comms) | 170 | 170 | 23 | 193 | 7 |

**A compaction target below the entry count is unreachable by editing.** On 2026-07-30 a hook asked for "under 140 lines" against a 170-entry floor: unreachable even with a zero-line header. Shortening descriptions, dropping the header, and tightening prose all trade against recall quality and buy single-digit lines. The only levers that actually move the number are:

- **prune / merge** — remove or combine memory *files*;
- **per-type index files with a router** — split `MEMORY.md` into `user`/`project`/`feedback`/`reference` indexes behind a small pointer file, so no single file carries all 170 lines;
- **a denser entry format** — cheapest to implement and worst for recall, since the one-line description is the whole reason an index is useful.

## ⚠️ Two hard constraints on the obvious fix

**1. Deletion is irreversible.** Memory lives in `~/.claude-pm/`, **not in the repo**. There is no `git revert`, no reflog, no `origin/main` copy. It does not behave like anything else agents touch. **Export the whole directory verbatim to a git-tracked file before any prune, merge, or delete.** Worked examples: `dev/active/memory-export-2026-07-27-pre-prune.md` and `-post-prune.md` (HOST, diffable pair), `dev/active/memory-export-2026-07-30-pre-prune.md` (Comms, 171 files).

**2. It is a governance decision, not a formatting choice for whoever trips the limit.** The pool is **shared by the whole cohort** — Claude Code keys memory by (account × project), not by role, and on Amber it resolves to the git common dir, so every agent worktree off this repo shares one pool by construction. Pruning it means deciding which of *other roles'* durable lessons stop being loaded. An agent that hits the ceiling mid-task should export, reclaim what it safely can, and **escalate the prune** — not silently delete 30+ entries to satisfy a line count.

**The corollary that makes this urgent rather than merely annoying**: the failure mode is silent truncation, so the cost of *not* deciding is that entries start disappearing from every agent's context with no notification. Deferring is not neutral.

## Entry format

Each entry is `<slug> — hook`, and **the slug IS the filename** — open `<slug>.md` in the memory directory. Markdown links are deliberately omitted: duplicating every slug in link text *and* target consumed ~15.7KB of a ~17KB budget, i.e. the entire space for descriptions.

## Provenance

Seeded 2026-07-25 from `dev/active/cio-memory-export-2026-07-24.md`, the verbatim export of the designinproduct.com pool. Memory is scoped per (account × project), so **none of it transferred automatically at the account switch** — it had to be re-seeded by hand.
