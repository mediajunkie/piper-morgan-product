# The memory index's size limits, and why they can't be fixed by editing

**Status**: operations reference. Moved here from `MEMORY.md`'s own header on 2026-07-30 by Comms, because the header explaining the line limit was itself consuming ~10% of the line budget.
**Subject**: `~/.claude-pm/projects/-Users-xian-Development-piper-morgan-product/memory/MEMORY.md` — the shared index loaded into every agent's context.

---

## Two independent read limits, and both truncate SILENTLY

Trailing entries vanish for every agent that loads the file, with no error and no sign anything is missing.

1. **~24KB of bytes.** It had reached 41.4KB — roughly 40% of entries invisible, including most of the `reference` bucket — before HOST caught it 2026-07-25.
2. **~200 LINES.** A separate ceiling that the byte count does **not** imply. Found by PA 2026-07-26 at 194 lines *while the byte guard was reporting a comfortable green.*

`scripts/rebuild-memory-index.py` now refuses to write past either and warns from 90%. A PostToolUse hook also warns on edit.

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
