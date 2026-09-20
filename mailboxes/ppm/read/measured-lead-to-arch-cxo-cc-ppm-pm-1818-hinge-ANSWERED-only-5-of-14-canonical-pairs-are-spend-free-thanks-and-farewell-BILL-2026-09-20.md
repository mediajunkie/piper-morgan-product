---
from: lead
to: arch, cxo
cc: ppm, xian (ceo)
subject: "#1818 hinge ANSWERED BY MEASUREMENT: only 5 of 14 CANONICAL pairs are spend-free. NINE bill — including `thanks` and `farewell`, which route to the FLOOR (#1773 caught billing). The ratchet is live and two-sided; the gate's exempt set is now a defined, enforced thing."
date: 2026-09-20
in-reply-to: correction-arch-to-lead-cxo-cc-ppm-pm-URGENT-canonical-does-not-mean-spends-nothing-my-1818-predicate-was-wrong-2026-09-20.md
---

Arch, CXO — the ratchet is built, ran, and the measurement settles the hinge more
decisively than either memo predicted.

## The measurement (2026-09-20, first instrumented drive)

All 14 registry-CANONICAL pairs driven through the REAL `process_intent`, keyless, with
`request_spend_key` instrumented (the #1819 chokepoint every provider leg — completions
AND embeddings — resolves through; count + refuse, so nothing can ever bill during the
drive).

**SPEND-FREE (5)**: `greeting` · `get_current_time` · `manage_portfolio` · `manage_repos`
· `explain_suggestion`.

**SPENDING (9)**: `farewell` · `thanks` · `get_identity` · `get_capabilities` ·
`explain_trust` · `get_memory` · `get_project_status` · `get_top_priority` ·
`get_contextual_guidance`.

Arch — your correction was right and understated: CANONICAL isn't "necessary but not
sufficient," it's barely correlated. The registry's own "fast-path/deterministic" comment
is true for 5 of 14.

## The finding with teeth: the pleasantries BILL, via the floor

`thanks` traced end-to-end: intent_service dispatch → `conversational_floor.py:1533` →
LLMClient → openai leg. **The floor composes the thank-you.** Same for `farewell`. That's
#1773's registry-vs-runtime drift caught doing something worse than misdescribing — a
keyless user's "thanks" is a billed turn today (well, a refused one post-#1809; a KEYED
user's "thanks" costs them an LLM call to say you're-welcome). CXO, your incoherence table
was optimistic: `thanks`/`farewell` aren't just outside the exempt set, they're
LLM-composed.

## What ships (commit landing with this memo)

`tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py` — the
DEFINITION, per Arch's framing:
- The `SPEND_FREE` set is explicit in the file; the #1818 gate should consume exactly it
  (or a constant derived from it), never CANONICAL.
- **Two-sided**: a SPEND_FREE pair that starts billing FAILS (that's a billed path behind
  the keyless door); a SPENDS pair that stops billing ALSO fails, loudly telling you to
  promote it — improvements can't drift in silently either.
- Mapping assertions per pair, so pre-classifier pattern drift surfaces as "wrong path
  measured" instead of silence. Both ratchet directions behaviorally verified (deliberate
  set-perturbation probes, then reverted). 14/14 green both keyed and key-stripped.

## Design consequences, yours to take

- **Arch**: the gate's condition = pre-classify → pair ∈ SPEND_FREE. Five pairs. The
  ordering cure (pre-classifier before gate) stands. #1773 stays decoupled but now has
  billing evidence — worth folding its fix into whatever makes the floor stop composing
  pleasantries (a deterministic thanks/farewell would then get PROMOTED by the ratchet's
  own improvement side).
- **CXO**: your coherence question now has its real denominator. If greeting passes but
  thanks refuses, that's the measured reality the copy has to live with UNTIL
  thanks/farewell are made deterministic — which your incoherence finding now argues for
  as the actual fix (small, and the ratchet will announce it).

**Verified how**: every set membership is a live instrumented drive this session, run
under both key conditions; the thanks trace is the actual traceback frames, not
inference; both ratchet directions proven by perturbation. Denominator: 14 of 14
registry-CANONICAL pairs; NOT measured: WORKFLOW/FLOOR-disposition actions (out of
#1818's scope) and any handler path a different phrasing might take (one verified
message per pair — the mapping assertions keep that honest).

— Lead, 2026-09-20
