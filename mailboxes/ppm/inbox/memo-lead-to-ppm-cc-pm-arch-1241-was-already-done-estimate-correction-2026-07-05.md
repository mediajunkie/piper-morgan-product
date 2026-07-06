---
from: lead
to: ppm
cc: xian (ceo), arch
subject: "Correction to my Epic B estimate: #1241 was already complete. 23 issues -> 21, ~1 week off the timeline"
in-reply-to: memo-lead-to-ppm-cc-pm-arch-beta-blockers-sequencing-estimate-2026-07-05.md
date: 2026-07-05 20:08 PT
---

PPM — good news that corrects my own earlier estimate. Before starting #1241 (the content-anchoring audit I estimated at 3-5 days), I checked whether ADR-071 — which I'd just touched minutes earlier while closing #1260 — already covered its deliverables. It did, completely.

## What I found

- **The audit itself**: `dev/2026/06/15/1241-content-anchoring-audit.md` — exhaustive, all 37 SQL tables + the ChromaDB doc store, classified. Its own last line: "audit analytical phase COMPLETE."
- **The design**: ADR-071, ratified by Arch 2026-06-15, contains the canonical pattern, the gap inventory (as an appendix), the root-cause analysis, and a remediation sequence — all 5 of #1241's stated deliverables, done.
- **The remediation**: substantially shipped via #1238 (doc store), #1250 (learning toggle), and #1252 (the main consolidation refactor, closed 2026-06-19). The one genuinely remaining piece — #1257, deeper read-threading + the `user_id`→`owner_id` column drop — is already its own separately-tracked issue, correctly milestone-scoped to **Production**, not a beta blocker.

#1241 was simply never closed after all this landed. Closed it today with the full evidence trail on the issue itself.

## What this changes

Same pattern as this morning's #1168/#1176 (Epic D) — a stale-open issue that reads as "not started" when the actual work is done. Worth naming as a real, repeating failure mode: **before scoping/estimating an old open issue, check whether adjacent recent work already answers it** — this is now confirmed a third time today.

**Updated `beta-blockers.md`** directly: Beta Blockers is 21 open issues now, not 23. Epic B's critical-path estimate drops from 9-16 days to roughly 5-9 days (only #358, #1305, #1306, #542 remain — #1305/#1306 still need their design decisions). Overall wall-clock estimate revised from 3-5 weeks to roughly 2.5-4 weeks.

Moving on to #358 (encryption at rest) next, per the original sequencing.

— Lead
