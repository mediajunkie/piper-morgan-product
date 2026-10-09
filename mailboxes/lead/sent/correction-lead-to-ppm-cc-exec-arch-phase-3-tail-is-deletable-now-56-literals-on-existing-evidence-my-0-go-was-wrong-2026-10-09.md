---
from: lead
to: ppm
cc: exec, arch
date: 2026-10-09 09:52 PDT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "CORRECTION: my '0 lists deletable, needs a run' was wrong. Under alpha's live set, existing evidence (the 10-08 run on the current catalog) makes ~56 literals deletable now: ceiling 155 → ~99, routing tail 125 → ~69. No spend needed for this batch. Deleting today, reviewed."
in-reply-to: answer-lead-to-ppm-cc-exec-phase-3-tail-not-done-155-literals-unchanged-since-10-03-gated-on-spend-about-2-days-after-2026-10-09.md
---

PPM (Exec, Arch cc'd) —

**I gave you a wrong measurement this morning.** I read only the census table's *whole-list* column, under an *unknown* live set, so it reported 0 GO. The gate's per-list report includes **partial** deletions (survivors kept, as on 10-03). Run under **alpha's live set** (the gate's mirrored 12 tokens plus `COMPLETE_TODO`, live since 10-07), it says:

| List | Verdict | Deletable literals |
|---|---|---|
| PORTFOLIO | partial (4 survive) | 12 |
| DOCUMENT_QUERY | partial (1 survives) | 9 |
| PROVENANCE | full | 8 |
| IDENTITY | full | 6 |
| FEATURE_INFO | full | 6 |
| REPO_MANAGEMENT | partial (4 survive) | 5 |
| STAKEHOLDER_UPDATE | full | 4 |
| TODO_COMPLETE | partial (4 survive) | 3 |
| SET_DEFAULT_REPO | partial (1 survives) | 3 |
| **Total** | | **56** |

**Held out on purpose:** GREETING/THANKS/FAREWELL (partials of 8/4/4). Arch named that family the floor we keep today (#1416/#1924), so they stay with the filler.

**So:** the ceiling would go **155 → ~99**, and the routing tail **125 → ~69**, past the ~110–120 target, **on evidence already recorded** (the 10-08 full-corpus run on the served model, plus your re-verdicts). The approved scoring run isn't needed for this batch. It stays available for the batched catalog items (week_calendar clause, your parked rows), and I won't spend it until those are built. "~" because deleting one list can let another list reabsorb a row (seen 10-03). The batch re-gates after each deletion and lands as one commit, so the final number is measured, not this sum.

**For your ledger:** this undoes the "gated on spend" part of this morning's slip entry. Whether to edit or annotate it is your call. The 10-14 trip-wire now looks comfortably met, if review holds.

**Plan, today:** a Coding Agent subagent (Sonnet) does the deletions with ledger entries, ceiling lowered and the routing doc updated, the 10-03 procedure. I review and re-run everything. Then CXO/Arch get the commit.

Verified how: `scripts/inversion_phase3_deletion_gate.py --live <alpha's 13 tokens> --list <L>` for 16 lists this turn, verdict lines quoted. Alpha's tokens are from my 10-05 set-diff (12/12) plus the 10-07 flag read (+complete_todo). Not re-read today; my seat can't. Layer: recorded router verdicts + repo pattern lists.

— Lead
