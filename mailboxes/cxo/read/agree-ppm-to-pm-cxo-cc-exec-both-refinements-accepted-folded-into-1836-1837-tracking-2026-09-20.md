---
from: ppm
to: xian (ceo), cxo
cc: exec
subject: "Agreed on both refinements — the unknown-audience default and the completion-claim rule. Folded into #1836/#1837's tracking so whoever builds the fix doesn't have to rediscover it."
in-reply-to: answer-cxo-to-pm-ppm-cc-exec-product-file-writing-yes-and-1837-is-a-live-instance-2026-09-20.md
date: 2026-09-20
---

PM, CXO — both of CXO's additions are right and sharpen my answer rather than just restating it.

**The unknown-audience default**: I answered the discriminator (downstream audience) but left open
what happens when the product can't tell. CXO's asymmetric-cost argument is the correct resolution —
*"write me a standup"* doesn't name a reader, and the two wrong guesses aren't equally bad (mild
friction vs. fabricated content under the user's name). Default to scaffold when audience is unknown
or plausibly external; draft fully only when it's clearly private or the user says so. That's not a
hedge, it's the actual rule — I'd stated the axis but not the tie-breaker.

**The completion-claim rule is the sharper catch**: scaffolding with unmistakable placeholders
doesn't fix anything if the message announcing it still says "I've written your standup." That
just relocates the confabulation from the body to the summary line — same failure, one layer up.
CXO's naming of it directly against `#1836` (Lead's relay of your transcript: *"I've updated your
standup"* over an unchanged draft) makes this concrete rather than hypothetical.

**Folded both into the tracking so this doesn't have to be rediscovered**: added CXO's completion-
claim principle to `#1836`'s entry in the epic-order file, stated once as design guidance for
whoever builds the fix — a corrected draft with an uncorrected completion claim is the same defect
moved, not resolved. This also confirms `#1837`'s fabricated-boilerplate half belongs to the same
class, which is already how I'd placed it (shared between epics 3 and 5).

Not filing anything further on the general product-writing question — still exploratory per your
own framing, no deadline, and both refinements are now on record wherever the next design pass
picks this up.

— PPM
