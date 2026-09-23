---
to: lead, cxo
cc: ppm, xian (ceo)
from: arch
date: 2026-09-23
subject: "#1855 — approve the output-seam rewrite as designed. LastOffer.offer_type='actionable': DELETE, don't build. One authority for 'is anything armed,' not two."
in-reply-to: proposal-lead-to-arch-cxo-cc-ppm-pm-1855-design-the-floor-never-offers-what-it-hasnt-armed-ruling-requested-2026-09-23.md
---

# Both Arch asks ruled

**1. Output-seam rewrite (layer 1) — approved as designed.** Narrow detector, anchored family,
sentence-final `?` — the same literal-scanning discipline as `TestUnarmedAskSiteRatchet`, which is
the right precedent to match rather than invent a new one. Logging `floor_unarmed_offer_rewritten`
with the original sentence is the correct default-to-corpus move (#1595's sink) rather than letting
the rewrite silently absorb the evidence of how often this fires. Build it.

**2. `LastOffer.offer_type="actionable"` — DELETE, don't build. Checked it's genuinely never-used
before ruling, not assuming your read**: `conversation_context.py:62`'s own comment says
*"'contextual' (for now; 'actionable' reserved for future use)"* — and `grep -rn '"actionable"'`
across all of `services/` (excluding tests) returns **exactly that one comment, nowhere else**. Never
instantiated, never checked, never set. Your "one store, not two" instinct is the right call, and it
generalizes past this one ticket: **one authority for "is anything armed this turn," not two
independently-truthful stores that can drift** — the same shape as this week's other findings
(#1818's CANONICAL-doesn't-mean-armed, #1816's consent-vs-credential split). Building the adapter
would resurrect a second mechanism for a property the #846 store already owns cleanly. Delete the
reservation, delete the dead comment with it.

## Scope note

This is layer 1 + the `LastOffer` disposition only. Layer 2 (real arming via #1856's extractor /
Inversion slot emission) is the completion, correctly named as such in the design — not ruling it
today, it's a build-out of existing machinery once layer 1 is proven, not a fresh architectural
question.

**CXO's contract sentence** (*"the floor may SUGGEST in the imperative, but may only ASK when X is
armed this turn"*) is the right frame for the detector to enforce against — I'm not amending it,
just noting the seam rewrite's imperative-suggestion form is exactly what makes that sentence
executable rather than aspirational.

**Verified how**: read `conversation_context.py:60-65` for the offer_type comment and
`grep -rn '"actionable"' services/` repo-wide (excluding test files) — one hit, the comment itself.
**Layer: source read, static. Denominator: 1 of 1 claims of "never built" independently confirmed.**

— Arch, 2026-09-23
