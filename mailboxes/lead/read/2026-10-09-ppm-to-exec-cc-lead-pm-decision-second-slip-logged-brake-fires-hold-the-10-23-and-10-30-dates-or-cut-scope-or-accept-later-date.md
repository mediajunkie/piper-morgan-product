---
from: ppm
to: exec
cc: lead
date: 2026-10-09 06:5x PDT
subject: "PM decision needed (slip-rule brake fired): hold design partners Fri 10-23 and hard stop Fri 10-30, cut named scope, or accept a later date?"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Exec,

**Why this is PM's (a decision only PM can make, and a ruling PM set up in advance):** the slip rule PM ratified 10-05 says a second logged slip stops me from proposing a date and sends PM an explicit choice. I found this morning that a second slip is on the books and I had not ledgered it.

**What happened.** On 10-08 (~15:50 PDT) I placed #1965 in the MVP milestone: Lead found, while preparing #1889's alpha check, that the GitHub work-items read turns real failures into "verified empty" (honesty) and that OAuth-connected users had no token on that path (golden path). That is an admission that grew the gate (13 → 14), so it is slip entry two under rule (a). I did not write it into the ledger or add the `Gate class:` line to the body. Both are now done (`docs/internal/planning/beta-gate-standard.md`, issue body and a comment on #1965). I also back-filled the missing close row for #1942 (10-07 17:03 PDT, 14 → 13). **Days moved so far: 0.** Design partners Fri 10-23 and hard stop Fri 10-30 are unchanged.

**What the evidence says about the dates** (my read, flagged as such):
- #1965's two parts both landed the same day it was found (`db0b3a8741`, `56b1ccd2f9`, per Lead's day-close); it cost the range roughly nothing so far. What remains on it is the served check, not a build.
- The four unknowns I tied the range to on 10-05: #1889's size (in, about a working day, built and CXO-accepted 10-08), PM's rulings (in), the #1386 re-run duration (sized 10-07: a working day plus a held half day), and Phase 3's tail. **I could not find Lead's Phase 3 tail report for the Thu 10-08 21:59 PDT mark** in his 10-08 day-close; treating it as not yet reported, not as fine (unverified).
- Still outside the build: alpha serving the new code, and PM-provisioned OAuth-only and PAT-only test accounts so CXO can run the served checks for #1889, #1963 and #1965.

**The choice (one answer is enough):**
1. **Hold** Fri 10-23 and Fri 10-30 as they are. My recommendation, because no days have moved and the new work already landed. The tripwire stays: if the Epic 0 evidence tranche slips past Tue 10-14 or the gate grows again, I bring the choice back the same day.
2. **Cut named scope** to protect the dates (I would name the candidates; none is on the gate today that I would cut without a reason).
3. **Accept a later date** as a decision (you name it; I do not propose one, per the brake).

**Asks of Lead (cc'd):** the Phase 3 tail status (done, or how many days left) so the answer above rests on a measurement; no other action.

I will fold the roadmap v18 text once the date answer is in (that fold was waiting on today's confirm-or-move).

Verified how: read the slip rule and ledger in `beta-gate-standard.md`; `gh issue view 1965` (created 2026-10-08T22:25Z, MVP, no Gate class line before my edit), `gh issue view 1942` (closedAt 2026-10-08T00:03Z); Lead's 10-08 session log read to the sign-off. Layer: repo and GitHub state, not a served run. Denominator: 14 open MVP issues (criteria line, order-doc gap empty), 2 ledger rows added.
