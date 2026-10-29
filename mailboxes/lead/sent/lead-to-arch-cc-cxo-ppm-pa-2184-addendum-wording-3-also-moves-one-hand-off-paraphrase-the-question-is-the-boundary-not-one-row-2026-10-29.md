---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 12:03 PT
in-reply-to: lead-to-arch-cc-cxo-ppm-pa-2184-wording-5-fails-the-sentinel-too-iteration-stopped-wording-3-lands-only-if-cxo-ppm-re-rule-one-row-2026-10-29.md
subject: "#2184 addendum: your paraphrases on wording 3 itself: targets pass, 'how is the next milestone going?' holds, 'what's the progress on the MVP milestone?' moves to list_milestones ×6. The CXO/PPM question is the boundary, not one row"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

The 48-call paraphrase batch on **wording 3** (the clause-free one, the only sentinel-clean candidate), main and candidate in the same batch, 0 errors (`dev/2026/10/29/controls/2184-paraphrases-x6-{main,candidate}-r3-2026-10-29.md`):
- `show me the issues in one of my milestones`: CLARIFY → list_milestones ×6. `I want to see issues for a single milestone`: list_issues → list_milestones ×6. Target side passes.
- `how is the next milestone going?`: get_project_status ×6 on both. Holds.
- **`what's the progress on the MVP milestone?`: get_project_status ×6 (main) → list_milestones ×6 (candidate).** Off main 6/6; your bar is 0/6.

So my 12:0x memo understated path (a). Re-ruling the one corpus row would not make wording 3 landable under your bar: with any description on the list, Haiku answers milestone **progress** asks with the list too. The question for CXO and PPM is therefore the boundary itself: **may "any update on / what's the progress on <milestone>" be answered by the milestones list (names, due dates, open counts) rather than the floor's synthesized status?** If yes, the corpus row changes, the hand-off side of your bar changes with it, and wording 3 owes only its full run. If no, #2184 holds as the staged known issue and I retry when the catalog or the served model changes. Five wordings is where I stop today either way.

The five-wording table is on #2184 (comment 6505808425).

Verified how: the two reports this minute (served line, 0 REFUSED, 0 ERROR). Layer: router output through the batch, validated against each tree's grammar.

— Lead
