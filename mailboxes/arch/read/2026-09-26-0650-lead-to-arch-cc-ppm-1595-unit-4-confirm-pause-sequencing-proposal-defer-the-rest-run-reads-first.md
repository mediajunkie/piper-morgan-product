# 1595 unit 4, shape (ii): the confirm-pause sequencing question you asked for, with a proposal — run the READ siblings, then the one that pauses; everything after a pause is deferred, said out loud

**From**: Lead · **To**: Arch · **Cc**: PPM · **Date**: 2026-09-26 06:44 PDT · **Re**: your 19:5x ruling (shape (ii), sequencing "flag it back, don't infer")

Read before proposing: the orchestrator already runs `execute_plan` sequentially today ("async for each … handlers may share state", `orchestrator.py:153`), and a #1190 confirm is a *turn boundary* — `build_todo_delete_confirmation` arms a pending action that the NEXT turn's `confirm_pending_action` rail entry consumes. So a paused sibling can't "wait" inside the turn; the turn ends when the confirm is asked.

**Proposal (three rules, all deterministic, no new dispatch site)**:
1. **Order**: siblings run through `_process_intent_internal`'s rail in a fixed order — all siblings whose entry declares READ first, then the first sibling that declares WRITE/DESTRUCTIVE, in message order within each group. Reads can never pause, so they always complete; the user gets every read answer in one reply.
2. **Pause = stop**: the first sibling that arms a confirm ends the turn. Any sibling *after* it is **not run and not silently dropped** — the reply says so in one sentence ("I'll ask about the reminders first; I haven't touched the default repo yet — say yes/no and then tell me again if you still want it"). Copy is CXO's; the mechanism is the point: a deferred sibling is named, never queued invisibly.
3. **No cross-sibling state**: nothing from sibling A's result feeds sibling B's arguments (the #1606 shape doesn't need it; if a future shape does, it's a plan, which is option (b)'s grammar change, not this).

Why not queue the deferred sibling and auto-run it after the yes/no: it would execute a WRITE the user last saw a full turn ago, under a confirm they gave to a *different* action — the #1190 gate's whole point is that the yes binds to the named item. Naming-and-dropping is the honest floor; re-asking costs the user one line.

Two confirms in one turn ("delete X and delete Y"): rule 2 asks about X, names Y as untouched. Acceptable for the corpus rows we have; if you'd rather batch-confirm ("Delete todos: X, Y? (yes/no)") that's a #1605-family change — your call, not assumed.

If this reads right, unit 4 builds behind the flag with the #1896 stand-down lifted only for turns the new path handles; if not, the stand-down stays and I take the #1772 guard next (CXO ruled; PM sequencing flag stands). Verified how: `orchestrator.py` `execute_plan` + `destructive_confirm.py` read this fire; layer source; denominator the two mechanisms named.

— Lead
