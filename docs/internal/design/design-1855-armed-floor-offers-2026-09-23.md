# #1855 design — the floor never offers what it hasn't armed

**Status**: proposal (Lead, 2026-09-23) for Arch + CXO ruling; pairs with epic 3's floor
contract. **The defect**: PM, 2026-09-23, twice — the floor wrote *"Want me to add 'One Job'
with the Design-in-Product/one-job repo to your projects now?"*, PM said *"Yes, please."*, and
nothing was armed, so the bare affirmative had nothing to bind to and the honest no-result
fallback fired. #1837 closed this seam for ONE offer (the standup interview, via
`interview_offer_accepted`); the general case is still open and it is the most user-visible
trust break we have: the system opens a conversation it cannot continue.

## What already exists (and why the floor bypasses both)

| Rail | Owner | What "yes" means | Where the floor stands |
|---|---|---|---|
| `LastOffer` (`conversation_context.py:51`, #852) | one-turn memory, always cleared | *continue/elaborate* on `continuation_hint` | `offer_type="contextual"` only; **`"actionable"` is reserved-for-future-use and was never built** |
| Pending-offer store (#846 one-slot, `WorkflowOffer`, `set_pending_offer`) | the soft-invocation seam | *invoke a named workflow* (Architect's bright-line rule: if "yes" invokes a named workflow, arm it here) | armed only by `soft_invocation.detect(...)` — never by floor prose |
| Acceptance predicate (`acceptance.py`, #1694 (b)) | consumes bare affirmatives | accepts **exactly-armed** offers | correct: it refused to bind PM's "yes" because nothing was armed |

The floor's LLM prose is the one producer of offers that touches neither rail. The predicate's
refusal is right; the *offer* was the lie.

## The rule (one sentence, CXO's contract)

**The floor may SUGGEST an action in the imperative, but may only ASK "want me to X?" when X
is armed this turn.** An unarmed offer-question is a contract violation, not a style choice.

## Mechanism (two layers; the first is enough to stop the bleeding)

1. **Enforcement at the floor's output seam (mechanical, honest, cheap).** After the floor
   composes its reply and before it returns: run an *offer-shaped question* detector over the
   text — the narrow family `Want me to …?` / `Would you like me to …?` / `Should I …?` /
   `Shall I …?` (anchored, sentence-final `?`, the same literal-scanning discipline as
   `TestUnarmedAskSiteRatchet`). If a match exists AND nothing is armed this turn (no
   `WorkflowOffer` set, no `interview_offer_accepted`-class flag, no `LastOffer`), rewrite
   the sentence to the imperative-suggestion form the #1856 fix already uses:
   *"To do that, say: add project One Job with repo Design-in-Product/one-job."*
   The user keeps the affordance; the system stops promising a binding it can't honor. Log
   `floor_unarmed_offer_rewritten` with the original sentence so the corpus lane sees every
   instance (#1595's default sink).
2. **Arming for real (the completion).** When the floor CAN name the workflow and its args —
   the #1856 extractor already produces `{name, repo}` for add-project; the Inversion's slot
   emission is the general form — it arms a `WorkflowOffer` in the #846 store *and then* may
   ask the question. `LastOffer.offer_type="actionable"` is the reserved seat for exactly this
   and should either be built as the thin adapter onto the #846 store or deleted as a
   never-used reservation (Arch's call; I lean delete — one store, not two).

## Why not "teach the predicate to guess"

Binding a bare "yes" to a *guessed* action is the #1694 anti-pattern in reverse: it converts a
visible no-result into an invisible wrong-action. The predicate's exactly-armed rule is the
correct half; the fix belongs on the producer side.

## Tests that would pin it

- Detector: each phrasing in the family matches; imperative sentences and non-offer questions
  ("What's the repo?") don't — narrow by construction, same as the ask-site census.
- Seam: a floor reply containing an unarmed offer-question is rewritten and logged; the same
  reply with a `WorkflowOffer` armed passes through untouched.
- PM's transcript as the fixture: turn "Want me to add 'One Job' … now?" with nothing armed
  → rewritten to the imperative; the next-turn "Yes, please." then has no offer to mis-bind and
  the honest fallback never fires because the user was never invited to say yes.

## Blast radius / not in scope

The detector touches only the floor's final text; handlers' own armed offers (standup interview,
reminder clarify) are already armed and pass through. Not in scope: the false-trails class of
the floor *describing* capabilities that don't exist ("we can set it up as your default repo") —
that is #1522's copy-honesty lane, adjacent but different (an offer vs a claim).
