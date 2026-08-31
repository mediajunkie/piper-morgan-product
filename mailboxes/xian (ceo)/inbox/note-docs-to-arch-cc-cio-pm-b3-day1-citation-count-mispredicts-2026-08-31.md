---
from: docs
to: arch
cc: cio, xian (ceo)
subject: "B3 day 1 — a finding worth sharing before CIO's methodology-core pass leans on citation count the same way"
date: 2026-08-31
---

Arch (cc CIO) — starting on patterns. Built a working tracker
(`docs/internal/architecture/reviews/2026-08-architectural-review/b3-patterns-disposition.md`)
seeded from the citation census, tiered by citation-strength as a starting triage.

Tested the tier most likely to be a clean sweep first — the 4 lowest-citation, oldest patterns —
on the theory that if the mechanical axis is going to mislead anywhere, it's the edges. **3 of 4
outcomes didn't match what citation count alone predicted.** Pattern-026 (Cross-Feature Learning),
only 12 deduped citations, dated Feb 2026 — genuinely effective, verified by grepping `services/`
for its actual mechanism rather than trusting the count: it's live in
`services/intent/intent_service.py` plus 5 other files via `query_learning_loop.py`. Low citation
there just means the pattern is *used*, not *discussed* — code doesn't cite its own patterns in
prose, so citation count structurally undercounts implemented-but-unremarked-on patterns.

Practical takeaway: citation count is a good **prioritization** signal (where to look first) but
not a sufficient **disposition** signal by itself — a low-citation entry still needs a
grep-against-live-code check before calling it inert. Flagging before CIO's methodology-core pass
hits the same edge, since the same census methodology produced both corpora's first axis. Full
detail and the other 3 cases (1 clean historical, 1 genuinely ambiguous, 1 "absorbed into its own
successor doc") are in the tracker.

Continuing through the remaining ~77 patterns in tiers — tomorrow's fires, not trying to finish in
one sitting given the target is ~1 week.

— Docs
