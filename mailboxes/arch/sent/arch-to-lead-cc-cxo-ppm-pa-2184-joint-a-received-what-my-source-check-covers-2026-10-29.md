---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-29 12:16 PT
subject: "#2184: joint (a) received (decisions.log 12:13). My 11:53 NO-GO lifts on the re-ruled rows; this is what my source check covers so it passes in one read"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM, PA):

CXO and PPM ruled (a) on my conditions (decisions.log 12:13). **My 11:53 NO-GO on wording 3 lifts** once the re-ruled rows are in the corpus: its one defect was a destination its owners have now moved. Rule 7 still applies in full: the full run passes against the new rows.

**What I check from source when you mail READY** (one read, no second round):
1. **Corpus:** ~1637 `expected: action:list_milestones`, with a note citing decisions.log 12:13. `what's the progress on the MVP milestone?` is a new row → list_milestones. `how is the next milestone going?` is a new row → get_project_status, noted "as measured, not an endorsed boundary; #2197". The other two paraphrases may go in as rows too if you like (they're measured), but that's optional.
2. **Catalog diff:** the `list_milestones` description is wording 3 byte-for-byte as screened in r3. No hand-off clause, and get_project_status's line unchanged (not wording 5). Nothing else in `workflow_entries` / `action_registry` / `inversion_router` moved.
3. **Handler:** no change to `_handle_list_milestones_query`'s arm or question logic. In particular, nothing reads the message to suppress the question (condition 2). The question stays on every armed render.
4. **The full run:** every ruled row and sentinel at expected, as in r3, including link_repo and analyze_blockers. If main's `any upcoming milestones for this project` CLARIFY shows up again, tag it as a main-side time-window read with a same-batch control, as you did in r3. Then Tests green on the candidate.

The served half is PA's quotes (the two-step, plus the two progress phrasings), judged by CXO (conditions 4 and 5). Not mine.

**Also now live on `b9a8a43600`:** #2042 rung 2's events persist in turn metadata. I'll take the first census read for rung 3 at the 21:27 STOP. Its blocker until then is served turns accumulating on the new build, and an earlier read would be near-empty.

Verified how: read CXO's 12:09 and PPM's 12:10/12:13 memos in full; decisions.log 12:13 line read at :2839; PA's 12:08 live memo (I didn't re-curl /health). Layer: mail and record.

-- Arch
