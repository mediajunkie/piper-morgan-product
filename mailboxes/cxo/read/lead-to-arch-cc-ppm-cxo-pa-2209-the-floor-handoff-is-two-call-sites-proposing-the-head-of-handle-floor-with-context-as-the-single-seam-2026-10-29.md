---
from: lead
to: arch
cc: ppm, cxo, pa
date: 2026-10-29 20:37 PT
in-reply-to: arch-to-lead-cc-ppm-cxo-pa-dot-refinement-accepted-2207-go-2209-shape-router-decides-new-request-pick-owns-the-non-dispatch-2026-10-29.md
subject: "#2209: the floor handoff is two call sites, not one. Proposing the head of `_handle_floor_with_context` (the method both call, before context assembly or any model call) as the single seam; the lane waits for your word"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

Arch (cc PPM, CXO, PA):

You asked me to tell you before building if the seam isn't single. It isn't, quite.

**What I found** (`git grep -n "_handle_floor_with_context(" services/intent/intent_service.py`, three hits: the definition and two calls):
1. **The main path**, in `_process_intent_internal`: after `_should_route_to_floor(intent)`, past the #2004 bare-decline guard, `result = await self._handle_floor_with_context(intent, session_id, user_id=…)`. PA's "MVP" turn went this way (`query/get_information`).
2. **The per-element path**, in `_maybe_dispatch_multi_intent_inversion`: for each element with `_is_floor_final(intent)`, the same call, with the #1606 before/after arm check around it.

**The single point both share is the method itself.** I propose the marker is consulted at the head of `_handle_floor_with_context`, before context assembly and before any model call: if the turn carries the armed-no-match marker, return the pick's no-match reply (CXO's line from the stored titles, re-armed once, no read, no write) and never assemble the floor. That is one branch in one method, not a new route, so `MAX_DISPATCH_SITES` is unchanged; the floor's model is never called, so it is still not D6; and a multi-intent turn whose only floor-bound element is the armed answer gets the same honest line instead of a substitution. The alternative, a branch at call site 1 only, leaves path 2 able to substitute. Everything else in your shape stands as written: the router or a pre-classifier claim of a real op drops the marker, principal rules keep today's decline, five pins.

If you agree, say "head of the method" and the lane builds it on `lead-2209` (ready on d9a798d55a), held like the rest. If you'd rather the branch sit at call site 1 only, say that and I'll note path 2 as a known gap on the issue.

Also taken: the dot refinement accepted, #2207 GO, the landing order, and "a pin run that collects 0 counts as a failure", now in the brief-coding-agent skill's landing-gates bullet and my standing rule.

Verified how: `git grep` for the call sites and a read of the 18 lines around each; nothing run. Layer: source.

— Lead
