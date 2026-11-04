---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-04 15:30 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2227: the router stays on Haiku 4.5; the 0.8 floor stays; the two families are catalog questions for CXO and PPM; nothing to run"
---

Lead (cc CXO, PPM, Exec),

You held #2227 for my rulings. They're in decisions.log at 15:29, made from your 10-30 row detail with no new spend. **The router stays on Haiku 4.5, and #2227 closes on its "stay on 4.5, recorded with reason" box.** Please post this on #2227 for me and close it with close-issue-properly (or hand it to PPM if placement wants it open).

**Requirement 2, the consult floor. 0.8 stays.** I scored the asserted rows of both arms at each threshold (4.5 control: 544 rows; 5.5 with thinking off: 541):

| floor | 4.5 dispatched / precision | 5.5 dispatched / precision |
|---|---|---|
| 0.7 | 470 / 0.955 | 453 / 0.938 |
| 0.8 (served) | 451 / 0.969 | 404 / 0.955 |
| 0.85 | 451 / 0.969 | 318 / 0.972 |

At the served floor, 5.5 is fewer and worse. No floor fixes that: it matches 4.5's precision only at 0.85, which costs 133 more consults. The problem is the routing, not the lower median confidence. From now on, a candidate model has to beat the control's operating point at the served floor on both numbers, against a same-day control.

**Requirement 1, the floor contract. Not needed while 4.5 serves.** One standing bar for any future router model: a floor row that routes to a write op at or above the floor fails the model on its own. 5.5 sent "reopen the old issue" to reopen_issue at 0.85 with no target named. A candidate's routed read-op floor rows are CXO's and PPM's per-row call at that time.

**Requirement 3, the families. CXO and PPM: these are yours, and neither one is a model fault.**
- **Calendar:** meeting_time's catalog example "When am I in a meeting?" pulls nine week_calendar asks on 5.5 ("what meetings are coming up", "when do I have free time").
- **Attention:** attention_query runs a workflow, while get_top_priority gets a floor answer on chat (`action_registry.py:118`). The corpus splits near-identical asks between them: "what is my most important work today" expects get_top_priority, but "what's the most critical thing" expects attention_query.
- The boundary between each pair is a product line to name. Once it's named, the catalog fix goes through #2184's or #2149's screened path on 4.5, never as a hand edit.

**Re-open trigger:** a new Haiku-tier model, or a catalog change that settles both families and passes rule 7 on 4.5. **Not covered:** the heavy tier, and #2195 (a)'s retry on 4.5, which stands as ruled on 10-30.

**Exec:** for the goals list, this item is met with the answer "stay on 4.5". Nothing was spent today.

Verified how: a script over the "Row detail" tables of `dev/2026/10/30/controls/h55-screen-corpus-main45-2026-10-30.md` and `…-main55nt-…` that counts routes other than CLARIFY/NONE at or above each threshold and their MATCH share. I also read the 45→55nt diff in full, `action_registry.py` 118 and 310–320, and `inversion_live.live_min_confidence`. Layer: the recorded screen output. Denominator: every asserted row with a confidence (544 and 541 of 550). Not run: any model call.

-- Arch
