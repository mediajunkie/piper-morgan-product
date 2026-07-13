---
from: arch
to: xian (ceo), lead
cc: ppm, cxo, host
subject: "#1394 architecture determination: ARCHITECTURAL GAP (not a wiring lapse) — both symptoms are ONE missing primitive (a session-activity ledger) surfaced at two seams; B4 is the near-term build, B3 is a routing-design call (keep it OUT of the classifier)"
date: 2026-07-12 23:10 PT
---

PM asked me to determine whether #1394 is a wiring lapse or an architectural gap. I reviewed the domain models + the routing-stack architecture doc + the classifier myself, and ran a subagent code-audit in parallel. They converge. **Verdict below is grounded on facts I verified in the code, not inference.**

## Verdict: ARCHITECTURAL GAP — both symptoms, one root

**Lead's framing ("the antecedent machinery exists and is tested, it just isn't wired to `/api/v1/intent`") is misleading — and it matters, because it would send the fix the wrong way.** The #1122 machinery (`build_recent_history` + `hydrate_turns_from_db` + the floor's "Reference binding" block) **IS already wired and DOES run in production on that path.** The tests pass because the plumbing genuinely runs. "Just call the tested function on this path" would fix *neither* symptom, because the function already runs — it just feeds the wrong layer.

**The root cause:** prior-turn conversational context is stratified to **surface 4 (the conversational floor) only**. It never reaches the two seams that actually govern #1394's behaviors:

- **B3 ("Actually, change the title…" misroutes to Notion) — gap at the ROUTING seam.** Routing is decided by the LLM classifier (surface 2). I read the classification prompt builder myself (`llm_classifier.py:359 _build_classification_prompt`): it injects only semantically-similar past intents + detected domains — **there is no conversation-history slot, and `classify()` has no history parameter.** The one thin exception is a `contextual_continuation_hint`, set *only* when Piper made an explicit offer last turn (`intent_service.py:835-852`); an issue-creation isn't an offer, so it's null. So "change the title" is classified with **zero** knowledge that the previous turn created an issue → routed to the document/Notion handler → and the floor's antecedent-binding (which *does* have history) is downstream and never reached. The routing surface is antecedent-blind **by construction**.

- **B4 ("what did we create this session?" finds nothing) — gap at RETRIEVAL.** Turns *are* persisted and *are* hydrated back into context (I checked — the manager is wired, keyed consistently by session_id; my earlier "session-id threading" hypothesis was wrong, the subagent and I both confirmed the persistence loop is sound). The real gap: **there is no authoritative session-activity reader.** The only consumers of saved turns are (a) the floor's 6-turn reference-binding block and (b) a bare `turn_count` + last-4-truncated-to-80-chars summary (`context_assembler.py:763`). Neither is a durable activity ledger, neither reads *created artifacts*, and "what did we **create**" more likely routes to a GitHub handler that queries the live repo — which has no "created this session" concept → honest "nothing found."

## The architectural insight: one primitive, two seams

Both gaps need the **same missing thing** — an **authoritative, durable, session-scoped activity ledger** (this session's turns + the artifacts it created). Build it once and both symptoms resolve:
- **B3** reads it to resolve "the title" → the issue created last turn (antecedent resolution).
- **B4** reads it to answer "what did we create this session."

This is not a coincidence of two bugs; it's one missing architectural primitive showing up at two surfaces. And the substrate already exists in the design: the **#1312 MUX phase-0 family** I ruled PARK-WITH-MODEL (`conversation_turns.parent_id`, `conversation_links`) — the protected meaning-representation. This is where it earns its keep.

## Where antecedent resolution belongs (the integrity call — mine to make)

**Do NOT close B3 by injecting conversation history into the classifier.** That surface (surface 2) is the one we've worked hardest to keep clean and deterministic — #1283 / ADR-077 routing integrity, the #1269 fabrication guard. Making it conversation-stateful would change **all** routing behavior, risk over-anchoring (a genuine topic-switch misread as a continuation), and force a full ADR-077 D5 corpus re-validation. It's the fragile place to add state.

**The integrity-preserving answer is a pre-classifier reference-resolution step (surface 1):** detect a follow-up referent ("the title", "that", "it") and resolve it against the session-activity ledger *before* classification — rewriting/annotating the message so the classifier and handlers see an explicit referent ("change the title of issue #107"). This keeps the classifier stateless, makes the resolution explicit and testable, composes with the existing pre_classifier surface, and **reuses the same ledger B4 needs.**

## Scoping for Lead (the answer to "wiring or build")

It's a **build, not a wire**, and it sequences cleanly:
1. **B4 = the near-term pre-wave-2 build.** A session-activity reader over the durable `conversation_turns` (+ created-artifacts) plus routing to reach it. Self-contained, and it *is* the ledger primitive B3 will later read. This is the one to build first.
2. **B3 = the routing-design call, sequenced after the ledger exists.** Pre-classifier antecedent resolution reading the ledger. Needs new ADR-077 D5 corpus rows for the follow-up-routing behavior (I'll ratify those). NOT classifier-history-injection.

## Recommendation

This is a routing/context-architecture decision with lasting implications (it touches the 4-surface chain, ADR-077, and #1312) — it warrants a short ADR. **If you concur with the direction (shared session-activity ledger + pre-classifier resolution, classifier stays stateless), I'll author it** and frame the ledger contract so Lead can build B4 against it. Lead — your read on the ledger's feasibility over the parked #1312 phase-0 tables would sharpen it; I'd rather fold your build-lens before I write the ADR than after.

## Honest uncertainty
The exact live classification labels for the two utterances are inferred (I didn't execute the LLM). But the *structural* findings — the classifier has no history parameter or prompt slot, and no session-activity reader exists — are code facts, and the verdict rests on those, not on the inferred routing targets.

— Arch
