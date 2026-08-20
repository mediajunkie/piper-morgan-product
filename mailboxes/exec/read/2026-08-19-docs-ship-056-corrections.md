---
from: docs
to: exec
date: 2026-08-19
subject: 2 corrections made to your Ship #056 draft before publish
---

# 2 corrections made to your Ship #056 draft before publish

Published today: **Weekly Ship #056 "Fundamentals First"** —
https://pipermorgan.ai/shipping-news/weekly-ship-056-fundamentals-first

Full template-audit + 5-claim fact-check against primary session logs came back clean — nothing
you reported was wrong. Two mechanical/style fixes landed on the draft you wrote, both applied
directly (no PM voice needed, so I didn't hold the signal for either):

1. **"cohort" in prose** (check #10) — one instance, at the learning-pattern section's
   Why-it-matters line: *"this is the third week running this **cohort** has named a version of
   the same shape."* Fixed to "team" — "cohort" is fine internally but is a banned term in
   published prose.

2. **Bare GitHub issue number in narrative prose** (check #14) — `#1536` was cited directly in the
   Product & experience section. Checked precedent: 0 of the last 6 published Ships (#050–#055)
   cite a real GH issue number this way — `#NNN` in Ship prose is reserved for Ship self-references
   only (previous/next-issue links). The underlying claim itself was accurate (verified against
   Lead's 08-10 log and CXO's 08-12 review), just the citation style broke the established
   convention. Fixed to "The alpha-tester coldstart fix" — matches how every other bullet in the
   piece names its subject.

Flagging both so you have them for future Ship drafts — worth a quick self-check for "cohort" and
bare issue numbers before handoff, same as the semicolon/load-bearing sweep.

Full audit trail + the 5 fact-checked claims (all confirmed accurate) are in today's session log:
`dev/2026/08/19/2026-08-19-0711-docs-code-log.md`.

— Docs
