---
from: ppm
to: exec
date: 2026-10-09
subject: Phase 3 tail now 129 (ceiling) / 99 (routing) — recount not a slip; tripwire reading is a PM question
type: ask
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

**PM-needed item (a question only PM can answer; please vet and surface).**

Lead landed 26 rule-10 deletions today. Lead's gate reports ceiling 129, routing tail 99 (Lead's figures; I re-counted the ceiling only: `scripts/pattern_literal_counts.py` TOTAL 129, 36 lists).

**Ledgered as a recount, not a slip** (`docs/internal/planning/beta-gate-standard.md`): no admission, no tranche change, nothing larger than assumed. Slips stay 4, 0 days moved. Dates unchanged (Fri 10-23 / Fri 10-30).

**The question for PM:** PM's tripwire is "Epic 0 evidence tranche not done by Tue 10-14." Our band (~110–120) was set on the ceiling, and the ceiling is 129, so on that reading it is not yet in band. The routing tail (99) is inside it. I have made the Tue 10-14 check read the ceiling as the headline with routing beside it, and I will not redefine "done" myself. Which does PM mean: ceiling in band, routing tail in band, or something else? Lead says going below 129 needs router/catalog work (descriptions, 11 unscored clear-family rows, #1935 for the 3 delete survivors). This is a heads-up, not a trip: Lead re-measures Mon 10-12, and if the tripwire trips Tue 10-14 I bring it the same day.

Not yet on alpha; the deletions reach users on the next promotion.

Verified how: method: ran the literal counter this fire and read Lead's 15:41 memo; layer: repo literal count, not the gate run or alpha; denominator: 36 lists / 129 literals. Lead's 99 and 26 deletions are quoted, not re-run.
