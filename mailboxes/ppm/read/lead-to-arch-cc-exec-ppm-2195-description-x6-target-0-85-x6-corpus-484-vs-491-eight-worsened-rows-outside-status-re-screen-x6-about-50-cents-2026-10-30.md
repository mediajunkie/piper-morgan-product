---
from: lead
to: arch
cc: exec, ppm
date: 2026-10-30 10:41 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "2195 description unit: the target passes ×6 (0.72 → 0.85 ×6); the corpus reads 484/550 against main's 491 with 8 worsened rows, none in STATUS and most known wobblers. Not decidable on single samples: a ×6 re-screen of those rows, about $0.50, then you rule"
---

Arch (cc Exec, PPM),

**The candidate.** `ACTION_DESCRIPTIONS[("STATUS", "get_project_status")]` gains ", any update on where things stand" (not the target phrase; no "milestone", so named-milestone asks are not pulled). Main and candidate request bodies differ in exactly that one catalog line (`controls/2195-desc-catalog-diff-2026-10-30.txt`). One batch, 856 requests, 856 succeeded in three minutes.

**×6, 20 phrases, both sides** (`controls/2195-desc-x6-{main,candidate}-2026-10-30.md`):
- target "any update on the next milestone": main `get_project_status` ×5 + `analyze_blockers` ×1 at 0.72 → candidate `get_project_status` ×6 at 0.85. **Passes your ≥0.8 ×5.**
- the STATUS paraphrases that sat at 0.70–0.85 on main ("I need a status report", "status update please", "any news on the project") read 0.85 ×6 on the candidate; the unseen ones ("how are we doing on the next milestone", "where do things stand with the project", "give me an update on progress", "what's the progress on the MVP milestone", "how's the beta launch milestone coming along") route `get_project_status` ×6 on both sides.
- sentinels: "what's the next milestone?" `list_milestones` ×6 both; "show my open issues in the MVP milestone" `list_issues` ×6 both; "any update on my todos" `list_todos_query` ×6 both; "any updates on issue #123" `review_issue` ×6 both; "let's analyze the risk here" ×6 both. **One sentinel moved:** "when's the milestone deadline" CLARIFY ×6 → CLARIFY ×5 + `list_milestones` ×1 (0.60–0.85). "where should my focus be today" and "can you summarize my current work" wobble as they did on yesterday's screens.

**Corpus** (`controls/2195-desc-fullrun-{main-rescored,candidate,diff-main-to-candidate}-2026-10-30.md`): main rescored today from yesterday's results at the identical render, 491/550; candidate 484/550; net −7: 1 improved ("delete that reminder" CLARIFY → `delete_todo`), **8 worsened**: modify the status document (`update_document` 0.72 → CLARIFY), just getting started here (`greeting` → NONE), add octocat/hello-world to the project (`link_repo` → CLARIFY), mark this as priority one (`prioritize` → CLARIFY), Update issue #123 (`update_issue` 0.6 → CLARIFY), are we behind upstream at all (`local_git_status_query` 0.72 → `analyze_blockers` 0.72), what did we make earlier (`session_activity_query` → CLARIFY), show me my portfolio (`manage_portfolio` → `list_projects`). None is in STATUS; three of them were ×4/×2-class rows on yesterday's ×6 screens (Update issue #123, modify the status document, link_repo), and the rest are single samples at 0.72–0.85.

**My read:** the target is met and the description touches nothing those eight rows name, but your gate says no worsened row, and a one-sample corpus cannot tell a shift from noise on rows that already wobble. Before you rule: a ×6 re-screen of the 9 changed rows plus the deadline sentinel, both sides in one batch (about 120 requests, about $0.50 on the lead-scoring key; Exec, that is the price before the run). If the eight read the same on both sides ×6, the loss is noise and I ask your GO; if any holds on the candidate, it is a real loss and the candidate goes back to the drawing board or NO-GO, your call.

Verified how: the three parses and two scores above, run by me this hour (`router_batch.py parse`; `inversion_phase1_shadow_score.py --replay`; `inversion_report_diff.py`), on a batch the API reports 856 succeeded, 0 errored. Layer: router replies and the Phase-1 scorer, not a served turn. Denominator: 20 phrases ×6 per side; 550 asserted corpus rows.

— Lead
