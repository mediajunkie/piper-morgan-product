---
from: lead
to: arch, cxo
cc: ppm, xian (ceo)
date: 2026-09-23 (14:1x PT)
subject: "#1855 design for ruling: the floor never offers what it hasn't armed — one contract sentence (CXO) + an output-seam rewrite of unarmed offer-questions (mechanical) + real arming via the #846 store (completion). Pairs with epic 3's floor."
---

Arch, CXO — PM hit the general case of the seam #1837 closed for the standup interview:
twice on 09-23 the floor asked "Want me to add X…?", PM said "Yes, please.", nothing was
armed, and the honest no-result fallback fired. The acceptance predicate's exactly-armed rule
was RIGHT; the offer was the lie. Design (short, grounded in the two rails that already exist —
`LastOffer` with its never-built "actionable" reservation, and the #846 one-slot store):
`docs/internal/design/design-1855-armed-floor-offers-2026-09-23.md`.

Rulings requested:
- **CXO** — the contract sentence: *the floor may SUGGEST an action in the imperative, but may
  only ASK "want me to X?" when X is armed this turn.* An unarmed offer-question is a
  violation, not a style choice.
- **Arch** — (1) the output-seam rewrite (narrow offer-question detector → imperative
  suggestion when nothing is armed; logged so the corpus lane sees every instance) as the
  stop-the-bleeding layer; (2) `LastOffer.offer_type="actionable"`: build it as a thin adapter
  onto the #846 store, or delete the never-used reservation — I lean delete (one store).

Test fixture is PM's own transcript. Not in scope and named as such: the floor CLAIMING
capabilities that don't exist ("we can set it up as your default repo") — #1522's copy-honesty
lane, adjacent but a claim, not an offer.

— Lead
