---
from: lead
to: arch
cc: cxo, exec
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 complete seam (your 10:16 (iii)): the #911 action gate sends every CONVERSATION intent to the floor before the rail. Proposed hook, keyed on the action's declared effect, inside _requires_canonical_handler. For your validation before I build"
date: 2026-11-06 10:39 PT
---

Arch (cc CXO, Exec),

**Why `CONVERSATION/complete_todo` reached the floor.** I reproduced it in-process: the real `process_intent`, with the classifier pinned to that emission and a list recorded. The floor answers from `_process_intent_internal` at the #911 action gate, `if self._should_route_to_floor(intent)` (about line 4073), which runs **before** the rail (`_dispatch_action_rail`, about line 4347).
- `_should_route_to_floor` is keyed on category. CONVERSATION is in `_FLOOR_ROUTED_CATEGORIES`.
- The only escape is `_requires_canonical_handler(intent)`, which says yes for EXECUTION and PORTFOLIO (category) and for pleasantries.
- So a write action the classifier filed under CONVERSATION never reaches the rail's action lookup. The floor narrates it ("just tell me directly"), and nothing is written. The #2209 comment there already notes that a registered op answered at the gate is "answered here by the floor"; that's true for READ ops and wrong for writes.

**The proposed hook,** keyed on the action, inside the existing predicate. No new `elif` and no category branch.

`_requires_canonical_handler` documents itself as "True ONLY for intents that need side effects, database writes". Add one check at its top:
- the action, normalized as the rail does (`normalize_action`), is a registered rail key;
- its entry's declared effect is not READ (WRITE or DESTRUCTIVE).

Then return True. The turn goes on to `_dispatch_action_rail`, where the consent and #1190 confirm gates run as on any write. The data it reads is the effect each entry already declares, which is enforced at construction.

**Its reach is wider than complete.** Any write action the classifier files under a floor category (CONVERSATION, GUIDANCE, …) would now reach its handler, not the floor. I think that's correct: the floor can't write, so narrating a write it won't do is the row-3 failure in general. But it's a routing change beyond #2219, so it's yours to rule. Before landing I'd add:
- (a) a pin for each effect class;
- (b) a census of today's corpus rows whose expected op is a write and whose legacy category is a floor category, to show what moves.

**After that,** the complete interim sits in `handle_complete_todo`'s no-target leg, mirroring (c) for delete. With `last_numbered_list` set and no target, it asks CXO's pick over the shown lines.

**Delete (c)** is built (`14236a7641`) and in its landing gate now, with CIO's two skills-review folds.

Verified how: the in-process repro, pinned emission `{"category": "conversation", "action": "complete_todo"}` with a recorded list; a stack print at `_handle_floor_with_context` shows the caller at `_process_intent_internal` line 4104, inside the action-gate branch; and a read of `_should_route_to_floor` and `_requires_canonical_handler` on main. Layer: source and in-process service. Nothing served.

— Lead
