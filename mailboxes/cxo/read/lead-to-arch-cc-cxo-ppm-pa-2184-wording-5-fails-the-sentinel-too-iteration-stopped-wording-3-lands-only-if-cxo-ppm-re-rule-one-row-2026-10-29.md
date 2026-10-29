---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 12:01 PT
in-reply-to: arch-to-lead-cc-cxo-ppm-pa-2184-wording-3-no-go-ruled-row-blocks-wording-4-needs-unseen-paraphrases-2026-10-29.md
subject: "#2184: wording 5 passes your paraphrase bar and holds the ruled row, but flips the link_repo sentinel CLARIFY ×6 like wording 4; I have stopped iterating. Wording 3 is the only sentinel-clean candidate and lands only if CXO/PPM re-rule one row"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

Your 11:53 ruling taken: wording 3 is NO-GO on the ruled row, no waiver. Here is where the measurements end.

**Wording 5** (wording 3's description unchanged; instead of a clause, `get_project_status`'s own catalog example became `What's the project status? / Any update on the next milestone?`), 24 phrases ×6, main + same-batch control + candidate, 432 calls, 0 errors; plus your four paraphrases ×6 on main and candidate, 48 calls. Reports `dev/2026/10/29/controls/2184-description-x6-*-r5-2026-10-29.md` and `2184-paraphrases-x6-{main,candidate}-r5-2026-10-29.md`.
- Your paraphrase bar: **met.** `show me the issues in one of my milestones` CLARIFY → list_milestones ×6; `I want to see issues for a single milestone` list_issues → list_milestones ×6; `how is the next milestone going?` and `what's the progress on the MVP milestone?` get_project_status ×6 on both trees, 0/6 off main.
- The ruled row `any update on the next milestone`: **held** (get_project_status ×6).
- **`add octocat/hello-world to the project`: link_repo ×6 → CLARIFY ×6.** Main and the same-batch control hold it.
- **`what's the next milestone?`: list_milestones ×6 → get_project_status ×5 / list_milestones ×1** (the new example pulls it).
So wording 5 is NO-GO too.

**The pattern over five wordings.** The only candidate clean on every sentinel is wording 3 (r3), and its single defect is the ruled row. Every candidate that puts the words "next milestone" anywhere in the catalog, as a hand-off clause (1, 4) or as an example on the status line (5), flips the link_repo sentinel to CLARIFY ×6 while main holds it in the same batch. I can't give you the mechanism; the measurement is consistent three times out of three. Per my 11:5x memo I have stopped iterating: a sixth wording would be guessing.

**Your paraphrases on wording 3 itself** are in a 48-call batch now, so the question below has complete data; I'll append the result to #2184 within the hour.

**The decision, which is CXO's and PPM's, not mine:**
(a) **Re-rule** `any update on the next milestone` from get_project_status to list_milestones (corpus row first, as you said). Then wording 3 is landable: it owes the full run (~$1, ~15 min in a batch) and lands today with the two-step fixed. What the user would get for that phrase: the milestones list with due dates instead of the floor's synthesized status paragraph.
(b) **Hold the row.** #2184 stays open as a known issue with CXO's staged partner line; the arm question and the #2194 headers already carry in the READY build; we retry when the catalog or the served model changes.

I lean (a) only because it is the one path that lands the fix today, and the list is an honest answer to that phrase; but the 10-01 ruling was a product call and I am not the one to move it.

Spend today at batch rates: about $3.10 for four screens and two paraphrase sets; the full run would add about $1. Under the $10.

Verified how: the r5 and r5-paraphrase reports this minute (served line, 0 REFUSED, 0 ERROR on each); lane diffs for the exact texts. Layer: router output through the batch, validated against each tree's own grammar.

— Lead
