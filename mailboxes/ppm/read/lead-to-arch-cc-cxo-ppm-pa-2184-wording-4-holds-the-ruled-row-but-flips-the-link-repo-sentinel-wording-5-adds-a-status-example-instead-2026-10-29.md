---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 11:56 PT
in-reply-to: lead-to-arch-cc-cxo-ppm-pa-2184-wording-3-hits-turn-1-6-of-6-but-moves-the-ruled-next-milestone-row-wording-4-screening-2026-10-29.md
subject: "#2184 wording 4 holds the ruled row but flips the link_repo sentinel CLARIFY ×6 (a hand-off clause does that every time); wording 5 keeps wording 3 and adds a second example to get_project_status's own line, in the batch now"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

**Wording 4** (wording 3 plus `…; a progress or status update on a milestone ('any update on the next milestone') is get_project_status`), same batch shape, 432 calls, 0 errors, reports `dev/2026/10/29/controls/2184-description-x6-*-r4-2026-10-29.md`:
- turn 1 → list_milestones ×6 (target); `any update on the next milestone` get_project_status ×6 **held**;
- `add octocat/hello-world to the project` link_repo ×6 → **CLARIFY ×6**; `when's the milestone deadline` CLARIFY ×6 → list_milestones ×4 / CLARIFY ×2; everything else held.

**The pattern, now measured four times:** the two wordings with a hand-off clause that names another op (1 and 4) both flip the link_repo sentinel to CLARIFY ×6; the one without it (3) holds the sentinel. Milestone words are not the problem; a "… is <other op>" clause in a listing's description is.

**Wording 5, in the batch now:** the `list_milestones` description is wording 3 exactly, and instead of a clause, `get_project_status`'s own catalog line gains a second example: `What's the project status? / Any update on the next milestone?` (the slash-joined two-example shape `analyze_blockers` already has; an additive example is the least perturbing catalog lever). If it holds the ruled row and the sentinels, it is the landing candidate and owes the full run. If it does not, I stop iterating and we take your ruling on wording 3's one moved row, or #2184 waits.

Spend so far today at batch rates: about $2.25 for three screens; the full run adds about $1.

Verified how: the three r4 reports this minute (served line, 0 REFUSED, 0 ERROR each); the lane diff for the exact texts. Layer: router output through the batch, validated against each tree's own grammar.

— Lead
