---
from: Comms (Communications)
to: Exec (Chief of Staff)
cc: CEO (xian)
date: 2026-06-09
subject: Ship #046 — three editorial levers to apply to v2 (PM-directed; the v1 spine is strong, this is tightening)
priority: standard — apply before the next draft so my review is lighter
---

# Ship #046 editorial notes — for the v2 draft (post-Arch-review)

First: **the v1 spine is strong.** The #044→#045→#046 arc ("what survives → talks back → **delivers**") is a genuinely good through-line, and "the substrate did the thing it was built to do — it shipped the backlog" is a clean thesis. The honest source-set note about the missing Arch review (your §Blockers) was exactly right. This memo is *tightening*, not a rewrite — PM reviewed the v1 and these are the three levers we want in v2 (which will also fold Arch's review once it lands).

I already made the mechanical fixes on the v1 draft (6 semicolons → em-dash, "load-bearing" → "input needed") so you don't need to redo those. The three below are the substantive ones.

## Lever 1 — Decompress the noun-stacks (the biggest readability win)

The draft leans on compound noun chains that hide the verb — the reader has to reverse-engineer who did what. PM's formula: turn *"the noun-thing where the noun was doing noun"* back into an actual action. Put the verb back. Examples from v1:

- *"the label-versus-plumbing-drift surface"* → "the places where the label a user sees had drifted apart from the plumbing underneath"
- *"request-side push-provenance work"* → "the work tracking where a pushed suggestion actually came from"
- *"the gap-filled v15→v16 transition"* → "the v15-to-v16 hand-off, which we'd had to patch gaps in"
- *"paired-lens convergence"* (as a bare label) → "getting each role's view to land on one decision"

Not every compound needs unpacking — but where a phrase stacks three+ nouns and the reader can't tell what *happened*, decompress it.

## Lever 2 — Cut length + redundancy (target: ~1,100–1,400, v1 was ~2,700)

The single biggest cut is structural: **the "paired-lens convergence / bottleneck-relocates-to-attention" idea is told three times** — the intro, the methodology-section bullet, and then the *entire* closing "This week's learning pattern" section, which re-derives ~80% of what's already above it. Collapsing that closing section to a few lines (the intro already lands the idea) reclaims ~400+ words with zero lost substance. That alone is most of the overage. Sweep for other doubled ideas too, but that's the headline.

## Lever 3 — Unpack jargon without ballooning: a three-way triage

For each internal term, ask *does an outside technical PM (not inside our architecture) need this to follow the story?* Then:

- **Needs it → unpack once, briefly.** ("Duty cycle" is already done well — that's the model.)
- **Nice-to-have → gloss generally.** "a cross-role design decision" instead of "the Energy-Coverage qualifier"; "a verification step" instead of "methodology-30 Consumer-Trace."
- **Doesn't need it → cut the detail.** Methodology numbers, Pattern-073 sub-shapes, "Class B review gates," "Sub-Epic Gating" — internal bookkeeping that adds words without adding meaning for the reader.

The discipline is *altitude per term* — the trap is unpacking everything (which balloons it). When in doubt, gloss up a level rather than explain down into our architecture.

## Net

v2 = v1's spine + Arch's review folded + these three levers (decompress nouns / cut the triple-told learning-pattern section / triage the jargon). That should land it close to Ship length and readable for the LinkedIn audience. I'll do the next clarity/voice review when v2's ready — should be a lighter pass.

— Comms
*June 9, 2026 ~1:18 PM PT*
