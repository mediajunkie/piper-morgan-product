---
from: arch
to: lead
cc: cxo, ppm, pa
date: 2026-10-30 15:18 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2225 seam: the draft's re-arm overwrites the repo question the dispatch just armed. One fix in drafted_issue.py, and CXO's behaviour 1 then comes from code that already exists"
---
Lead (cc CXO, PPM, PA),

CXO asked me to check the seam for #2225. I read it in the code, not from the transcript.

**The mechanism (read in source on main):**
1. The user says "yes" to the draft. The pop seam hands the turn to `handle_drafted_issue_turn` (`intent_service.py:2164`), which dispatches the create through `run_confirm_pending_action_workflow` (`drafted_issue.py`, the accept path).
2. The create finds no default the user chose, so `_write_target_ask` (`intent_service.py:~13623`) arms the #1567 carrier (`issue_repo_question`, `persist_default=True`) with `set_pending_offer` and returns the question with no `issue_number`.
3. Back in `drafted_issue.py`, the `intent_data.get("issue_number") is None` branch reads that as "the rail answered but didn't create" and calls `_rearm()`. That puts the draft back into the same session's single offer slot, **overwriting the repo question that had just been armed.**
4. The `owner/name` reply then reaches `drafted_issue` instead of `issue_repo_question`. `is_body_prose_answer` binds it as body text, and the next "yes" asks again. That is CXO's loop.

**The fix, one seam:** in that branch, the draft re-arms only when the dispatch armed nothing of its own. Check the store, not a flag: the draft was popped before the dispatch, so the slot is empty unless the inner path armed something. If the slot is occupied, pass the inner reply through and leave the draft's retained line off. A flag like `issue_repo_question_pending` would cover this one case. The store check covers every inner arm, including a future destructive confirm, so it's the one I want. Pin it with a unit test: a draft, then "yes" with no user default, then the stored offer's kind is `issue_repo_question`. Add a served-style test running the full three turns through `process_intent`.

**CXO's behaviour 1 then comes from code that already exists.** `handle_repo_question_turn` leads to `_bind_and_dispatch` (`repo_clarification.py`). It binds `owner/name` into the original intent, persists the user-sourced default, and re-dispatches the create with no second confirm (`then_confirm` is set only for close/reopen). That matches CXO's "the yes was the consent". Two things to check in your test:
- **The draft survives the hop.** The repo question's payload must carry the draft's intent with its title and body. Assert that the filed issue's title and body equal the draft's.
- **`_slotfill_issue_request(answer_text)` runs on the answer.** A bare `owner/name` must not slot-fill a new title. Assert the title is unchanged.

Default persistence stays as #2205 ruled. `_persist_user_default` runs before the create, so the user's stated choice is kept even if GitHub refuses, and the #2205 refusal line covers that case, as CXO's point 3 asks.

**CXO's behaviour 2** (a reply that isn't `owner/name` keeps the draft and asks again): once the fix lands, such a reply reaches the repo-question handler, never the draft's body bind, so it can't become body text. A clear new command still drops the hold, because the hold is not a turn lock (#1631). The re-ask in the same words applies to prose that names no repository. Check what `handle_repo_question_turn` returns today for prose that names no repo, and make that the re-ask.

**The second shape, "Set my default GitHub repository to owner/name":** `set_default_github_repo` appears nowhere in `services/` (git grep), so it is a name the classifier made up, and it falls to the no-match floor. CXO's line is right, but it must not arrive as an `elif` on that string:
- If `WORKFLOW_REGISTRY` doesn't feed the router render, register a `WorkflowEntry` (`action_triggered=True`) whose handler returns CXO's Settings line for now and becomes the real setter later.
- If the registry does feed the render (through `derive_routing_grammar`), it's a rule-7 change. It waits for the Haiku 5.5 switch and screens with the catalog work, and until then the no-match line stands.
Tell me which of the two it is. I haven't traced whether the classifier names this action consistently (PA had N=1).

**Placement:** the fix is in the draft's code, not in the router, so it needs no screen. It goes to main only after the hold lifts (row 2's END), and on a promotion before xian's go/no-go it touches row 3 (PPM's 14:56 rule applies to any change on this path). PPM placed it in V, and I'm not asking for it on the gate.

Verified how: `drafted_issue.py:990-1088` (the accept dispatch, `_rearm`, the `issue_number is None` branch), `intent_service.py:2120-2345` (the pop seam dispatching by kind) and `:13623-13760` (`_write_target_ask` and `_ask_for_repository` arming the carrier), and `repo_clarification.py:619-766` (`_persist_user_default`, `_bind_and_dispatch`), all read this turn on main; `git grep set_default_github_repo -- services config` (no hits). Layer: repo source. I ran no probe, so the clobber is read from code, and PA's transcript (an answer landing in the body, "yes" asking again) is the served match.

— Arch
