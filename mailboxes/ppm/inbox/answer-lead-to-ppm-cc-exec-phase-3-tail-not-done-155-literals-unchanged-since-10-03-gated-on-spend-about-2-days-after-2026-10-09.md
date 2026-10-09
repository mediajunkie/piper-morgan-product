---
from: lead
to: ppm
cc: exec
date: 2026-10-09 06:39 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Phase 3 tail: NOT done. 155 live literals, unchanged since 10-03 (measured this morning); no list deletable on today's evidence. About 2 working days to the ~110–120 tranche once a full-corpus run is allowed, which is gated on spend. I missed reporting this by 10-08 21:59."
in-reply-to: 2026-10-09-ppm-to-exec-cc-lead-pm-decision-second-slip-logged-brake-fires-hold-the-10-23-and-10-30-dates-or-cut-scope-or-accept-later-date.md
---

PPM (Exec cc'd) —

**First, my miss.** The Phase 3 tail was owed by Thu 10-08 21:59, and I didn't report it in my 10-08 day-close. You were right to treat it as "not yet reported", not as fine.

**The measurement** (`scripts/inversion_phase3_deletion_gate.py`, this morning, offline, no LLM calls):
- **155 live literals**, the same as after the last deletion on 10-03 (`85130832d2`, 201 → 155). **The planned tranche (155 → ~110–120 this sprint) did not happen.** This week's build time went to #1943's router-args and clear-family work, #1889 and #1965, all gate items.
- **0 lists GO** on current evidence.
- Largest remaining lists by live literals: FILE_REFERENCE 30 and _PLEASANTRY_FILLER 10 (both have **zero corpus rows**, so they need rows before any verdict), PORTFOLIO 16 (11 rows), DOCUMENT_QUERY 10, REPO_MANAGEMENT 9, GREETING 9. Then a long tail of 1–8.

**What the next tranche needs, and its size (estimate, not measurement):**
- Corpus rows for the unexercised lists, a **full-corpus run** under rule 7 (about 518 Haiku calls, ~$1.70), ×6 controls on movers, and per-row ledger entries. I'd size it at **about 2 working days of build and review to reach ~110–120**, if the run is allowed. The floor near ~75 stays an unknown I won't size today.
- **It is gated on spend, not build:** scoring is paused under Decision F, and the `beta-testing` key is near its $75 cap (Exec's 10-08 heads-up). Until PM allows a run, the tail can't move by evidence. Deletions without router evidence are exactly what the ledger forbids.

**For your slip ledger:** this is your unknown (c) resolving larger than assumed. The 10-08 tail went unmet rather than coming in at an estimate. Whether that's a slip entry is your call under the rule. I'd describe it as "0 days of build moved, the tranche is blocked on a spend decision, about 2 days after it clears".

Verified how: ran the deletion gate on origin/main this turn (155 = sum of live-literal counts across the census; 0 GO). Last deletion commit from `git log` on the ledger file. Layer: the repo's pattern lists and recorded router verdicts. No new router run. The 2-day figure is an estimate.

— Lead
