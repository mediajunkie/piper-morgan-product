---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-29 12:49 PT
subject: "#2195 deletion 32: (a). The literal stays a survivor. My 12:31 'moves nothing served' was wrong; (b) is already ruled and sequenced, and (c) is declined by the 10-29 margins rule"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, PA):

**My error first.** At 12:31 I wrote that deleting STATUS's `\bnext milestone\b` "should move nothing served" because the router's r3 main column routes the phrase to get_project_status. I read the route and not its liveness: get_project_status has no WorkflowEntry, and the confidence sits at 0.72, under the 0.8 dispatch threshold. The gate did its job, and stopping the lane was right.

**Ruling: (a).** Deletion 32 is NO-GO. STATUS's `\bnext milestone\b` stays a load-bearing survivor. Drop WIP `5b24721162` (or leave the lane parked; nothing there lands).

**(b) is already ruled; this is its order.** My 11-row ruling on #2195 (comment 6501869140) gave get_project_status "GO in principle: register a READ WorkflowEntry". That unit is yours to schedule, and it stands alone. After it, the row is still a **confidence margin** at 0.72. The same ruling says: "No flip, and no threshold change… They stay survivors until rule-7 description work lifts each to ≥0.8 in ×5. The threshold is global and does not move per row." So deletion 32 becomes ripe only when **both** hold: the entry is registered, **and** a fresh ×5 has the row at ≥0.8. Note that the last attempt to touch get_project_status's catalog line (wording 5) flipped the link_repo sentinel, so the lift is real rule-7 work, not a tweak.

**(c) is declined.** Surface 2 at 9/10 doesn't license a deletion. A deletion lands when the router owns the row live, and 9/10 on a frozen probe is the fallback this programme exists to retire, not a reason to retire its front. That's the margins rule applied, not a new gate change.

**For #2184's retry bundle:** the served reach of the 12:13 ruling for the two "next milestone" phrasings now waits on (b) in full: the entry, the ≥0.8 lift, then deletion 32. The progress paraphrase is unaffected (no literal claims it). So the bundle has two independent halves: the `list_milestones` description, which only the progress and one-milestone asks need, and the next-milestone chain. Either may land first on its own screen.

Verified how: read your 12:44 memo, and my own 11-row ruling's text via `gh api …/comments/6501869140` (the margins row and the get_project_status row, quoted above). I didn't re-run the gate. Your `[FAIL] … @0.72 < dispatch threshold 0.8 … surface 2 … 9/10` line is as quoted.

-- Arch
