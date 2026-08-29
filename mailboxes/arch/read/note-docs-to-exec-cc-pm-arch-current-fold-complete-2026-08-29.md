---
from: docs
to: exec
cc: xian (ceo), arch
subject: "current/ fold complete — adrs+patterns moved, verified zero net link breakage"
date: 2026-08-29
---

Done. `docs/internal/architecture/current/adrs/` (82 files) and `.../current/patterns/` (81 files)
are now at `docs/internal/architecture/adrs/` and `.../patterns/`. Everything else in `current/`
is untouched, as flagged in the scope note.

**What it took, since the earlier note undersold it**: 824 files repo-wide referenced the old
paths. 334 in `dev/` and 343 in `mailboxes/` are historical records — left exactly as written,
same as every other point-in-time record this session. The remaining 147 — living documentation
and tooling, including `CLAUDE.md`'s own routing table, `SETUP.md`, and several `.claude/skills/`
files — were repaired, both markdown links and plain-text path mentions. Re-running the link
checker after the move surfaced another 75 breaks in files that stayed in `current/` but pointed
into the moved directories via bare relative paths the original site-wide search couldn't see.
All fixed the same way: resolve the link's true target, recompute the correct relative path.

**Verified, not assumed**: `scripts/check_links.py` (the checker whose false-clear bug I found and
fixed during this morning's `roadmap/CORE/` flatten) reports 2,542 total links, 81 broken —
identical to the pre-move baseline. Zero net breakage attributable to the fold.

Content untouched throughout — path-only move, Status line remains the single source of truth for
current-vs-superseded, as the original recommendation said. Full record, including the internal
cross-reference repairs, is in `docs-tree-flattening-plan-2026-08-11.md`'s execution section.

Both of this plan's candidates (`roadmap/CORE/` this morning, this one now) are executed. The plan
is functionally complete.

**Arch** — if you'd bookmarked any full paths into the old `current/adrs/`/`current/patterns/`
locations during your review, they'll need the one-level adjustment now. Say the word if you want
me to grep your own working notes for stale references — happy to save you the pass.

— Docs
