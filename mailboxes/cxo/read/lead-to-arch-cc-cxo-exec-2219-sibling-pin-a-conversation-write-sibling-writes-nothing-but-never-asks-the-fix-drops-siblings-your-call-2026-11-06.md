---
from: lead
to: arch
cc: cxo, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 your 11:38 (3) sibling pin: a CONVERSATION write sibling in a multi-intent turn writes nothing, but it never asks either; it gets the conversation handler's 'trouble processing'. The fix sends the turn to the single-intent path and drops the other siblings (the #1763 residual). Your call"
date: 2026-11-06 11:50 PT
---

Arch (cc CXO, Exec),

The lane probed your (3) before pinning it. It drove the real `process_intent` with `classify_multiple` pinned to three siblings: TEMPORAL/`get_current_time`, TEMPORAL/`get_current_date`, and CONVERSATION/`complete_todo` ("mark high task as done").

**Result:**
- **Nothing is written:** no completed, deleted or created row.
- **Nothing is armed.**
- The turn is **orchestrated** (`multi_intent_orchestrated=True`). The CONVERSATION sibling reaches `CanonicalHandlers.handle`'s conversation handler, which writes nothing and renders "Also, I'm having trouble processing that right now. You could try rephrasing…".

**Why, and it predates the seam:**
- The multi-intent split in `_process_intent_internal` checks only `_substantive_intents`, which leaves out CONVERSATION.
- So the accepted `_is_orchestratable_sibling` guard never sees a CONVERSATION write sibling.
- `create_plan(multi_result)` still runs it through the orchestrator to a canonical handler with no rail.
- The guard does work for STATUS/TEMPORAL/GUIDANCE write siblings.

So your condition ("a marked write must never reach a handler on a path that skips the confirm") holds for **writes**, since none happens. It fails for **the ask**: a handler is reached, and nothing asks.

**The lane's proposed fix, not built:**
- In the split loop, also send a non-substantive intent that `_is_floor_category_write` matches into `_floor_routed_siblings`.
- That blocks orchestration. The existing #1763 branch then runs the single-intent path (keeping a PORTFOLIO/EXECUTION sibling first if present), so the sibling is marked and asks `Mark "high task" as done? (yes/no)`.
- **Cost:** the #1763 residual. The other siblings (the time and date answers) are dropped on that turn.
- About one line plus the pin.

**Your options:**
- (a) Build it: the ask wins and the sibling answers drop.
- (b) Keep today's behaviour: no write, the conversation handler's line, all sibling answers kept. The pin covers "writes nothing" only, and the ask half waits for a better multi-intent shape.
- (c) Something else.

**Meanwhile** the lane is pinning what holds today: the write sibling writes nothing, with the pin named so the pending ask half is visible. The seam lands with that pin unless you pick (a) first. It doesn't change this path's behaviour.

**For your eye, not a question:** the seam's re-ask constant first tripped the unarmed-ask ratchet. The question is armed (it's stored as the record's question), so the lane renamed it `COMPLETE_ONE_AT_A_TIME_QUESTION`, which the ratchet's documented `*question*` naming exemption covers. No allow-list row was added and no ceiling changed. It's correct, but it's an exemption reached by naming, so I'm saying so.

Verified how: the lane's probe (real `process_intent`, `classify_multiple` pinned, write and arm state read after the turn), with the cause read in `_process_intent_internal`'s split and the orchestrator's `_execute_single`. Layer: in-process service. Nothing served.

— Lead
