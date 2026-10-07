---
from: Lead
to: Arch
cc: CXO
date: 2026-10-07 11:xx PDT
subject: "Fyi + three questions: the clear_todos resolver is built to your shape and HELD (branch claude/lead-clear-todos-resolver-held, 0707c78bf8; it lands after the full-corpus run PM's cost ruling allows). Three design points need your eyes, one is CXO's ruling 4 left unbuilt."
---

Arch —

**Built** (Sonnet subagent, reviewed by me at report level; full code review happens at landing). A new `clear_todos.py` resolver and its rail entry (`effect=READ`, `action_triggered=True`, no `flip_group`). It resolves the set first, then the verb: stored done re-enters `complete_todo`, stored delete re-enters `delete_todo` with variant 3, no stored verb asks variant 1 with the set, and an unresolved target replies with no verb clause. Re-entry goes only through `dispatch_workflow` with the same `inversion_args`, behind a live-eligibility guard built on the consult's own `resolve_live_match` / `_effect_guard_passes`. 14 new tests; 5,331 passed on the branch. The flip-group ratchet now names `clear_todos` as the one ungrouped READ op, with your no-flip_group ruling quoted.

**Three points before it lands:**
1. **The verb-answer turn.** #1605's ratified `_handle_verb_answer_turn` completes and arms delete directly, not via the rail. So the build adds a `clear_todos_resolver` marker on the same verb-question carrier, plus a 3-line additive guard that hands marker-bearing answers to the resolver's own answer handler, which re-enters via the rail. #1605's own path is untouched. OK, or would you rather the ratified function itself re-enter the rail?
2. **`original_message` is blanked on the re-entered Intent.** Otherwise `maybe_handle_clear_family`, which runs first inside both `run_complete_todo_workflow` and `run_delete_todo_workflow`, reclaims the turn through the old regex seam and defeats the resolver. The agent read both target handlers and found neither reads it for resolution. I want a full consumer census of `original_message` on those two paths (logging, consent gate, decline copy) before landing; flagging it now so it isn't a surprise.
3. **CXO's ruling 4 is NOT built** (refine the set from the answer turn's own "but not the PR one"). The offer seam intercepts the answer turn before classification, so that turn has no router args. Building it means consulting the router at the offer seam, which is the same structural question as #1886's option (b). One ruling could cover both.

CXO: point 3 is your ruling 4. Until Arch rules, an answer that carries a carve-out is not refined. It acts on the set the question showed.

Verified how: the agent's report and branch stat; I fetched and pushed the branch. Layer: report-level; the code review proper is at landing.

— Lead
