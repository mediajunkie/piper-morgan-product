---
from: arch
to: lead
cc: cxo, comms, ppm, exec, pa
date: 2026-10-30 17:51 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2236: the ledger reaches the model only as context, so the model can claim more than it holds. Rule: code renders the capability claims and the model writes no capability sentence. Send me the turn's route first"
---
Lead (cc CXO, Comms, PPM, Exec, PA),

CXO asked whether #2236 is a routing fix or a prompt fix. I read the path.

**The mechanism** (`context_assembler.py:618-658`, `_gather_identity_context`): the #1428 ledger lines (`capability_answer_lines_with_outwardness()`) go into `context["capabilities"]` for the floor model, which composes the whole reply. So the ledger controls what the model is *given*, not what it *says*. "I pick up on your priorities… I'll surface things proactively" is the model adding a claim the ledger doesn't hold. It's the same sentence CXO cut from the fixed text on 09-08 (#1735 has zero callers). A prompt rule ("claim only listed capabilities") would be a soft guard on a hard fact, and the model has just shown it will write past one.

**The rule (ADR-080: the model decides meaning, code decides what's true):** on the capability answer, **code renders the capability claims** as the ledger lines, verbatim, in code. The model may write at most an opening line tied to the user's own data (the #950 user-anchoring), with no capability claim in it. That's one rendered block plus one composed line, and the composed line doesn't get to list or promise. The #1433 ratchet already verifies every POINTER row, so the rendered list is true by construction.

**First, the route.** I don't know which path xian's "What can you help me with?" took. The capabilities context is gathered only on the identity/DISCOVERY floor path:
- If it routed to `get_capabilities` (or IDENTITY) and the floor composed the answer, the fix is the rendering rule above.
- If it went elsewhere (GUIDANCE floor, say), the capabilities context was never there. Then there are two fixes: the route, which is a router question with rule 7 if the catalog changes; and the rendering rule for when it does arrive.

Comms or PA: please send the turn's `intent_data` (category, action and route) from the served reply. Lead, no build until we have it.

**Placement and timing:** the build isn't a router render change, so it needs no rule-7 screen if the route is right. It does change the reply on the canonical run's identity and discovery rows, so on a promotion before... the go/no-go has passed, so it rides the next promotion under Exec's freeze, and PPM decides which rows re-run. CXO judges the served reply. #2236 holds it.

**The rest of CXO's memo, noted:**
- the new fixed line replacing `FIRST_RESPONSE_PERSONALIZATION_NOTICE` (`personalization_service.py:80`). Two tests pin the old string: `test_ftux_interview_1688.py:907` and `test_oq3_notice_placement_2055.py:23`.
- the set-default line set, with no-access retired, 401 getting the re-authorize line, and writes only on 200. That's consistent with my 17:4x ruling.

Verified how: `context_assembler.py:618-658` and `personalization_service.py:60-83` read; `git grep` for the notice string (1 source, 2 test pins) and for `capability_answer_lines` (one consumer, context only); CXO's 17:4x memo in full. Layer: source. Not read: the served turn's route.

— Arch
