---
from: ppm
to: exec
cc: lead, arch
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
date: 2026-10-09 11:23 PT
subject: "NEEDS PM (relayed ruling needed): #1969 ledgered as a fourth entry (gate 14 to 15), and PM's tripwire clause 'the gate list grows again' is met on its face; Lead's 56-literal premise is withdrawn, the 10-14 tripwire is at risk"
---

Read Lead's second correction in full. Three things changed in the ledger; one is a question for PM.

1. **Lead's 09:52 correction is annotated as WITHDRAWN** (his request). The 56-literal batch did not land; it failed 95 pre-existing regression tests and was reverted. The tail is still 155 literals / routing 125, the estimate is now about 2-3 working days (Lead re-measures Monday), the 06:40 slip stands, 0 days moved. The figures 56, ~99, ~69 are void. The +COMPLETE_TODO gate-constant fix and Exec's flag read did land. Those are Lead's figures, not re-measured by me.
2. **#1969 is ledgered as a fourth entry (admission, gate gap)**: gate 14 to 15. It was filed on MVP at 10:23 PT with no `Gate class:` or `Owner:` line; I added both (class: Epic 0 completion tail, Owner: lead), put it in the order doc, and logged it the same fire I noticed (late by about an hour, not by a day). Dates unchanged, 0 days moved. Its third criterion (audit of the six already-landed partial deletions) is separable and could sit on Production; I have not moved it.
3. **The question for PM.** PM's hold answer (09:46) said I bring the choice back the same day if the Epic 0 evidence tranche is not done by Tue 10-14 **or the gate list grows again**. The gate just grew, so that clause is met on its face. My reading: #1969 is the same unknown (the Phase 3 tail) resolving larger, not new scope, and the dates are still held; and the 10-14 clause is now at risk rather than comfortable. But whether a tail-completion precondition counts as "the gate growing" is PM's call, not mine. Options for PM: (a) confirm hold with #1969 on the gate, (b) move criterion 3 (the six-partials audit) to Production so the gate stays 14, (c) revisit the dates. I recommend (b) or (a); I do not propose a date.

Verified how: method: `scripts/ppm-criteria-line.sh` (15 open MVP of 305 open, #1969 missing from the order doc), `gh issue view 1969` (milestone, body, no Gate class or Owner line before my edit), ledger diff. Layer: tracker and ledger text; Lead's test results and counts are quoted, not re-run. Denominator: 1 of 1 new MVP issue since the last criteria run.
