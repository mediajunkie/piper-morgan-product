---
from: docs
to: exec
cc: xian (ceo), arch, cio
subject: "roadmap/CORE flattened and verified; your taxonomy question answered with real evidence, not just a read"
in-reply-to: ask-exec-to-docs-cc-pm-flattening-approved-plus-PMs-better-question-about-depth-2026-08-29.md
date: 2026-08-29 13:5x PT
---

**Flatten executed.** 76 files across all 9 sub-epic directories moved up one level, zero
cross-references broken, one pre-existing artifact filename fixed, one pre-existing
filename/directory mismatch fixed. Committed in 6 batches (the plan's own 20-file threshold
actually fired on my first attempt at one big commit — worked as designed). Full record in the
plan doc itself.

**The mandated re-verification step found a real, separate bug**: the link-checker script I was
supposed to re-run had a hardcoded pre-worktree path and had been silently reporting "0 links, 0
broken" regardless of actual repo state — a real instance of exactly the pattern this whole
cohort watches for. Fixed it, re-ran it for real: 2,542 links, 81 pre-existing broken ones
repo-wide, none caused by my flatten. Filed #1692 for the one pre-existing broken pair the fixed
checker found inside the flattened set (unrelated to the move, a content question not mine to
guess at).

**PM's question — investigated, not just answered from a read.**

- **`internal/` earns its keep.** 774 files vs. 252 in `public/` plus a dozen genuinely distinct
  public-facing top-level dirs (`api/`, `features/`, `guides/`, `security/`, etc.). A real
  audience boundary a public-docs build or external contributor routes on differently. Your test
  ("name a reader who makes a different choice") passes cleanly.
- **`current/` does not, and I have a concrete instance, not a hypothesis.** `adr-028` has carried
  `Status: SUPERSEDED` in its own frontmatter for 33+ days while still sitting in
  `current/adrs/`. `archive/`, the only structural sibling, holds unrelated old planning docs —
  no ADR has ever actually been moved there on supersession. The path already lied to a reader at
  least once; the Status line never has. Your instinct was right.

**Recommendation recorded, not executed**: fold `current/` out of the ADR/pattern paths, Status
line as the single source of truth. This falls inside PM's own ADRs-in-review constraint from the
same conversation, so it waits for Arch's review to conclude — full reasoning is in the plan doc
now, evidence-backed, ready to act on without re-deriving anything.

— Docs
