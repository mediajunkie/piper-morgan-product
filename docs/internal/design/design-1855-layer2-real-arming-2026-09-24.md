# #1855 layer 2 — the floor ARMS what it offers (design, ruling requested)

**Status**: proposal (Lead, 2026-09-24) for Arch + CXO. Layer 1 (2026-09-23) makes an unarmed
offer-question impossible: the floor's output seam rewrites it to an imperative suggestion. That
closed the trust break. Layer 2 is the completion CXO's contract sentence names on its other half —
*"may only ASK 'want me to X?' when X is armed this turn"* — so the floor can, in the cases where
it genuinely knows the command, ask the question honestly and have the bare "yes" bind.

## What layer 1 established that layer 2 builds on

| Piece | Where | What layer 2 reuses |
|---|---|---|
| Detector + three-tier rewrite | `services/intent_service/unarmed_offer.py` | Tier 1 already **binds** a command: it round-trips the floor's own sentence through `extract_add_project_slots` and only emits `To do that, say: add project X with repo Y` when the real extractor parses it. That round-trip IS the arming precondition. |
| "Armed this turn" signal | `IntentService._armed_offer_signal` → `FloorContext.armed_offer` | Reads the #846 store (`peek_pending_offer`) and `LastOffer`. Layer 2 arms through the #846 store, so the seam sees its own arm on the same turn with no new rail. |
| Accept path | `intent_service.py` ~1222 (`get_and_clear_pending_offer` → kind-specific branches → `evaluate_acceptance` → `dispatch_workflow`) | An armed record with a `workflow_type` the dispatcher knows, plus a `pending_action` the carrier can execute, is consumed by machinery that already exists — nothing new on the accept side. |
| The one confirm carrier | `run_confirm_pending_action_workflow` (`workflow_entries.py:227`) — re-dispatches a stored `{intent, action}` with the confirmed marker | The record shape layer 2 must produce. |

## The rule (one sentence)

**The floor may arm — and therefore ask — exactly when tier 1 would have bound a command: the
catalogued action family matched, the slots came out of the floor's own sentence, and the composed
command round-tripped through the real extractor.** Anything less stays a suggestion (layer 1). No
guessing, no "probably meant" — the same exactly-armed discipline the acceptance predicate enforces
on the other side.

## Mechanism

1. **Arm at the seam, not in the prompt.** `enforce_armed_offers` gains a third outcome beside
   *pass* and *rewrite*: **arm**. When tier 1 binds a command AND no offer is armed this turn AND the
   caller passed an arming callback, the seam arms a `WorkflowOffer`-shaped record in the #846 store
   and leaves the question standing (optionally normalizing it to the ratified family). The record:
   ```
   {"workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
    "pending_action": {"kind": "floor_bound_offer",
                       "intent": <Intent built from the bound command via the real classifier/extractor>,
                       "action": "add_project", "command": "add project X with repo Y"},
    "offer_message": <the floor's question>, "ask_rendered": True}
   ```
   `ask_rendered` matters: the #1739 predicate refuses an accept against a record with no rendered
   ask (Arch condition (a)) — the floor's question is that ask.
2. **Binding is via the command string, not a parsed guess.** The record stores the composed
   imperative; on accept, the carrier re-runs it through the ordinary rail (`process_intent` on the
   command text with the confirmed marker), so the action executes by exactly the path the user
   would have taken by typing it. No second implementation of add-project.
3. **Decline / off-intent** follow the existing #1529 semantics (the pop on the next turn is the
   binding; off-intent abandons). Nothing new.
4. **Catalogue growth is the only extension point.** Today the catalogue has one family
   (add-project). Each new family needs: a real extractor that round-trips, a rail action that
   executes from the command text, and a test that the seam arms only on a round-tripped bind. The
   catalogue is a ratchet-shaped list (explicit, tested) — the same discipline as the ask-site census.

## What is deliberately NOT in layer 2

- **`revise_draft()`** — the standup draft-refinement surface bypasses `respond()`. Its offers are
  armed by the standup conversation itself (an active conversation is claimed above
  classification), so it is not an unarmed-offer surface today. It should get the *detector* as a
  guard (log-only) so we learn whether it ever asks an unarmed question — not the arming path.
- **Inversion slot emission as the general binder** — the design named it as "the general form."
  It is; it is also #1595's lane. Layer 2 uses the same round-trip gate with today's extractor and
  leaves the slot-emission binder as the drop-in replacement when the inversion lands. The seam's
  contract doesn't change.
- **A new `offer_type`** — deleted with `"actionable"` per Arch; one store, one authority.

## Rulings requested

- **Arch**: (a) arming from the output seam via the #846 store + the confirm carrier, with the
  command string as the binding — vs. arming inside the handler that produced the prose (the floor
  has no handler; the seam is the only place that sees the sentence). (b) `floor_bound_offer` as a
  new `pending_action.kind` handled by the existing carrier, vs. a dedicated workflow entry.
- **CXO**: when the floor arms, should the question be left as the model wrote it, or normalized
  to one house form (*"Want me to add project X with repo Y? Say yes, or tell me otherwise."*) so the
  user always sees the exact command they are consenting to? I lean normalized — the user consents
  to a command they can read, not to a paraphrase.

## Tests that would pin it

- Seam: PM's fixture with the callback present → the record is armed (peekable), the question
  stands, the log says `floor_offer_armed`; without a round-trip bind → layer-1 rewrite, nothing
  armed (the existing pins). Same sentence with an offer already armed → untouched, no double-arm.
- Accept: next turn "yes" → the carrier dispatches `add project One Job with repo …` through the
  real rail (handler patched at the DB seam) and the reply is the handler's own confirmation.
- Decline / off-intent: record cleared, nothing dispatched, no leak into the next turn's context.
- Denominator pin: the catalogue's entries each have a round-trip test, and a test asserts the
  catalogue is exactly the tested set.

## Blast radius

Only turns where the floor composes an offer-question AND tier 1 binds — today, add-project
phrasings. Everything else is layer 1 behavior unchanged. Rollback is the callback: not passing it
leaves layer 1 exactly as shipped.
