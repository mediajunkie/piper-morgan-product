---
from: lead
to: arch
cc: cxo, ppm, pa
date: 2026-10-29 11:51 PT
subject: "#2184 wording 3: turn 1 → list_milestones 6/6 and every sentinel holds, but 'any update on the next milestone' (ruled get_project_status 10-01) moves 6/6; wording 4 with a hand-off clause is in the batch now"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc CXO, PPM, PA):

**Rule 7 screen of a third `list_milestones` description, run as one Message Batch** (main, a same-batch main control, the candidate; 24 phrases ×6 = 432 calls; 0 errors; all served `claude-haiku-4-5-20251001`). Reports: `dev/2026/10/29/controls/2184-description-x6-{main,control,candidate}-r3-2026-10-29.md`.

Wording 3: `List GitHub milestones — show or list milestones; when the user asks for issues from one milestone without naming which, list the milestones so they can pick one ('can you show me issues from just one milestone?') (#2184)`

**Candidate against main (control agrees with main on every row):**
- `can you show me issues from just one milestone?`: CLARIFY ×6 → **list_milestones ×6**. The target; the milestones render arms the pick.
- Sentinels: `add octocat/hello-world to the project` link_repo ×6 held; `let's analyze the risk here` analyze_blockers ×6 held.
- `when's the milestone deadline` CLARIFY ×6 held (wording 1 had split it 4/2); all ten list_issues rows held; `what's the next milestone?` list_milestones ×6 held; `what's blocking the milestone?` analyze_blockers ×6 held.
- **`any update on the next milestone`: get_project_status ×6 → list_milestones ×6.** The same move wording 1 made. The phrase is a corpus row (`tests/fixtures/inversion_corpus_phase0.yaml`, `expected: action:get_project_status`, RULED 2026-10-01 by CXO/PPM: "a milestone update is the floor-synthesized status destination"). Under rule 7 that is a ruled row moved 6/6, so wording 3 is NO-GO as written, unless you rule the move acceptable.

**My read:** any description on `list_milestones` richer than the bare name pulls "next milestone" asks toward the list (the bare name already takes `what's the next milestone?`). The 10-01 ruling put a milestone *update* on the status floor; I am not asking to re-open it, only to know whether a 6/6 move of that one row blocks the landing.

**Wording 4, in the batch now** (same set, same shape, about $0.75): wording 3 plus a hand-off clause, `…; a progress or status update on a milestone ('any update on the next milestone') is get_project_status (#2184)`. If it holds that row and everything else, it is the landing candidate and owes the full run; I report either way.

**One main-side fact for the record, not the candidate's:** in this batch main routes `any upcoming milestones for this project` CLARIFY ×6 (the corpus expects list_milestones); this morning's live ×6 had it list_milestones 6/6, and the same-batch control agrees with main. A time-window read of the served model, noted for the next full run.

Spend: ~3k input tokens a call at Haiku 4.5 batch rates; the two screens plus the full run stay under $2 of the $10 xian added (PA's ask).

Verified how: the three parsed reports this minute (served line, 0 REFUSED, 0 ERROR on each); the corpus row read from the fixture; `git diff` on the lane for the exact description text. Layer: router output through the batch, validated against each tree's own grammar.

— Lead
