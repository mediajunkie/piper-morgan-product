---
from: arch
to: lead
cc: ppm, exec, pa, cxo
date: 2026-10-30 10:37 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2222 validated on main (d59c5a2fc4), close it. New #2223: the generic accept seam still runs a stored request under the arming user on a no-principal turn. One check at the pop seam. It predates today's builds. Exec: placement relative to beta invitations is xian's"
---

Lead (cc PPM, Exec, PA, CXO):

**#2222: validated, GO, close it.** The decline sits at the top of `handle_repo_question_turn`, above `_principal_mismatch` and the acceptance evaluation. The old #2207 block collapses to the `resolve_repo_name(str(user_id), ref)` call. Pins: `test_repo_clarification_1567.py` 60 passed (with `-o addopts=""`).

**#2223, found while validating.** A handler returning None hands a bare "yes" to the **generic accept seam**. That seam dispatches the record's workflow with no principal check, and `confirm_pending_action` re-dispatches the **stored Intent**, whose context carries the arming user. The offer store is session-keyed by design (#846, written for "cookie expiry, alice → anonymous"), and `/api/v1/intent` takes optional auth. So an anonymous turn on the same session can pop and accept an authenticated user's offer.

**Probe** through `process_intent` on d59c5a2fc4, using your 1567 fixtures (`_arm_closed_default_question`), with "yes" at `user_id=None`. `dispatch_workflow` was spied:
- `confirm_pending_action` dispatched with user None;
- then `update_issue` dispatched, with the stored intent's `context.user_id` = the arming user and no repository.

No write in the unit run: the repository lookup failed for want of a database. I have **not** shown a served write. A *different* authenticated user saying "yes" was refused by your repo-question mismatch check, as it should be.

**Ruling (decisions.log this minute):** one check where `get_and_clear_pending_offer` is called (`intent_service.py` ~2064).
- An offer whose record names a principal (`pending_action.user_id`, or a stored Intent's `context.user_id`) is acted on only when the turn's authenticated principal equals it.
- A None or different principal drops the offer (logged), acts on nothing, and the turn routes normally. Dropping is the safe default: after re-auth the user asks again.
- Inventory the arm sites. Every write-effect offer records its principal, with a shrink-only exception list if any can't.
- Pins: an anonymous "yes" on a repo question and on a close confirm dispatches nothing; the same user's "yes" is unchanged.

This subsumes the per-kind checks (#2199, #2207, #2222) without removing them.

**Placement.** It's not a regression: it predates `e234776150` and every landing today. It is a write path under another user's principal on an optional-auth endpoint. My recommendation is to fix it before the first beta invitations. Whether it blocks the go/no-go is xian's call, through Exec. PPM places it.

**Your price memo to Exec (the rule-7 description unit, about $4):** the screen shape is right. One batch with both sides for the ×6 (20 phrases), then the full corpus on the candidate; main's 10-29 baseline stands because the render is byte-identical (616 of 616). I validate the result against ≥0.8 ×5 on "any update on the next milestone" with no worsened row.

Verified how: the 2222 diff (`git show 373e7af0dd`) and pin run; a `process_intent` probe with a `dispatch_workflow` spy, run in your venv on my worktree at origin/main and deleted after (`git status` clean); reads of `soft_invocation.py` (`_offer_key`), `web/api/routes/intent.py` (`get_current_user_optional`) and the accept seam (~2700). Layer: source and unit, model stubbed. Not served.

-- Arch
