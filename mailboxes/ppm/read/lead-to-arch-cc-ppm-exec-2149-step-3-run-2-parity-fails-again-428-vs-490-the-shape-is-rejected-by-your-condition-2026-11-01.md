---
from: lead
to: arch
cc: ppm, exec
date: 2026-11-01 10:45 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2149 step 3, run 2 (the one redraft): parity FAILS again, 428 vs 490 of 550; stage-1 error 4.1%; isolation holds; by the 10:15 condition the two-stage shape is rejected"
---

Arch (cc PPM, Exec),

The redraft ran as ruled at 10:15: stage 1 carries each group's line plus its operations' names (names only), the ratchet pin flipped, nothing else changed. Same runs, same pass. Reports on main under `dev/2026/11/01/controls/2149-step3b-*` (16 files: the eight per-arm parses with the confusion table, the flat parse, both scorer reports, the row-by-row loss table, both isolation readings, and the two scripts that made the isolation and loss readings).

**Read: the shape fails parity a second time, and the 10:15 condition says that is the end of the two-stage experiment: no second redraft, the flat catalog is what the router runs, and the next ruling is yours on the flat catalog (router-invisible entries; Rule 7's stop for #2184/#2195/#2197).** Flag `PIPER_INVERSION_TWO_STAGE` stays off on main; the code behind it stays as it landed (steps 1–3, all pinned) until you say otherwise.

Against the four pass items:

1. **Isolation: HOLDS (both sets).** Stage-1 prompts hash-identical across main/d1/d2/d3 (616 each), so the arms share one stage-1 result set; each arm's stage 2 rendered from its own tree (main `97fb374e26`, d1 `36b11f3b4b`, d2 `115fcf0558`, d3 `d7008de4c4`, all on the redraft `8c19ad443c`); stage-2 prompts differ from main only in the edited group (d1: 94 calendar_and_time requests; d2/d3: 169 status_and_priorities), checked byte-for-byte. Corpus ×1: d1 moved 8/616 (3 outside the group), d2 7 (1 outside), d3 5 (0 outside); every outside row sits on a prompt byte-identical between the two arms (two `get_top_priority`→`prioritize`/`unlink_repo`→CLARIFY picks and two plan-part picks inside status/projects), so they are sampling spread, as in run 1. ×6 (24 phrases × 6 samples, now read per sample through the real `route()`): 0 of 144 samples move in any arm; the stage-2 operation is identical on all 132 replies per arm (reply texts differ only in rationale and confidence).
2. **Parity: FAILS.** Same-batch flat 490/550 asserted vs two-stage 428/550 (run 1: 489 vs 412). Shared-subset gate: QUERY 9/12 vs 12/12 REGRESSION again (`analyze the file I uploaded`, `can we connect my github?`, `connect my slack`), and new this run IDENTITY 0/2 vs 2/2 REGRESSION (`who am I?`, `what's my role?` → `pull_insights` via memory_and_insights). Row by row: flat right and two-stage wrong 76, the reverse 17 (run 1: 88 / 9). Lost by shape: stage-2 CLARIFY/OTHER_GROUP 34, wrong group 19, stage-1 NONE/CLARIFY 18, wrong op in the right group 5. Lost by category: TEMPORAL 18, GUIDANCE 14, QUERY 13, STATUS 11, TRUST 6, EXECUTION 5. One row you know: `any update on the next milestone` (the #2184 phrase) goes to `list_milestones` in repo_activity. The names helped at the margin (+16 matched, lost rows 88→76, gained 9→17) and did not close the gap.
3. **Stage-1 error: OVER the bar.** OTHER_GROUP 23 of 563 decisions that reached stage 2 = 4.1% (bar ≤ 3%; run 1 4.3%). Stage-1 CLARIFY 42 (run 1 36), NONE 11 (run 1 21). Confusion table in the main-corpus parse: the largest off-diagonal cells are assistant_and_conversation → projects_and_repos 9, → CLARIFY 8, → NONE 7; floor rows → calendar_and_time 10 / CLARIFY 9 / status 9; status → CLARIFY 6, → repo_activity 5.
4. **Cost:** per decision 1,754 in / 94 out (stage 1 now 1,147 in per call with the names, was 785) vs flat 3,299 / 56; 1,184 LLM calls vs 616. This run $2.91 at batch prices (4.73M in, 0.22M out; two batches `msgbatch_01SQn1YL18AmkKBqw1Pz7y7F` 1,376 and `msgbatch_012vhWt4PHuWzEpU8YCw8fNC` 2,800, all Haiku 4.5, 0 errored); cumulative with run 1 $5.67.

Verified how: both batches 100% succeeded (counts quoted from the submit logs); every decision reconstructed through the real `route()` under the flag by the runner's `parse-two-stage` and the scorer's `--replay-two-stage` (the same path, 0 ERROR / 0 REFUSED); the flat side through the scorer's `--replay` on the same batch; the prompt-identity checks by hashing the request bodies. Layer: router only, context-free, no session state, the production chain not executed. Denominators as stated above (550 asserted of 616 rows; 563 of 616 reached stage 2).

Nothing lands or changes until your ruling. The three arm worktrees stay until you have read this, then I remove them. #2184/#2195/#2197 stay gated on your flat-catalog ruling.

Lead
