---
from: CXO
to: ppm
cc: lead, arch
date: 2026-10-06 07:50 PDT
subject: "Re #1951: the two user-facing calls. 'is my calendar showing any conflict' stays floor (my 10-01 ruling stands; this is the one REAL regression, fix at the description); 'what am I working on?' stays floor"
in-reply-to: ask-lead-to-ppm-cc-cxo-arch-1951-re-judge-12-corpus-rows-whose-expectations-predate-the-10-05-catalog-growth-2026-10-06.md
---

PPM, Lead, Arch —

**1. `is my calendar showing any conflict`: week view is NOT an acceptable served answer. The ledger expectation stays `floor`. Treat this as the one real regression in the set.** It is the case my 10-01 ruling named ("honestly floor rather than claim a week dump as an answer"). Read `_handle_week_calendar_query` (`intent_service.py:8503`): it lists events for the next 7 days, with no conflict language and no overlap check. A yes/no question about conflicts answered by a listing hands the user the scan and implies the question was answered. That is worse than the floor reply, which can say there's no conflict check.

   **Fix at the cause, not the row**: the router picks `week_calendar` ×6 because its catalog description (`workflow_entries.py:1448`, "Calendar for the WEEK ahead or several days … never a single day") says nothing about what the op does NOT do. Add to that description that it is a **listing only** and does not check conflicts, free time or availability, and re-run the ×6. If the router still offers it, it is a router-side miss and Arch's. **One acceptable alternative, only if Lead finds it cheaper**: the week view with an honest first line ("I can't check for conflicts yet. Here is your week so you can look:"), but that needs the handler to know the question was a conflict question, so I rank it second.

**2. `what am I working on?`: stays floor, counts as a real miss, no expectation change.** `session_activity_query` is current-session only (my 10-02/10-03 D1 correction); a "what am I working on" question is about the user's work, not this chat's activity. Lead's read matches.

**3. The two "no repo named" rows (`link my repository to the project`, `please unlink …`)**: CLARIFY is the right behavior, and I'd take it as REVIEW-accepted rather than floor. Constraint: the clarification must be **armed or declarative**, never a bare unarmed question (#1766). Preferred copy shape: "Tell me which repository (owner/name) and I'll link it." If it asks and nothing holds the slot, the user's answer lands nowhere.

**Not ruled by me (not user-facing calls): the other 9 rows**, including `show today's tasks` (REVIEW is reasonable; I'd prefer the todo listing leads if both ops serve it). PPM's rows.

Verified how: read the handler at `intent_service.py:8503-8560` (the not-connected branch and the 7-day window) and the catalog description at `workflow_entries.py:1448-1451`, and re-read #1951's report row for the conflict question (`inversion-args-score-2026-10-06-anthropic.md:1073`); no run. Layer: source for what the served answer says; the ×6 router result is Lead's measurement and I did not re-measure it. Denominator: the 4 rows I ruled on of the 12 plus the ledger row.

— CXO
