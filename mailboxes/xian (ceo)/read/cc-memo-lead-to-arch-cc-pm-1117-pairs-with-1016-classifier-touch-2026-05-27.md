---
from: Lead Developer
to: Architect (Chief Architect)
cc: CEO (xian)
date: 2026-05-27
subject: #1117 INTENT-TEMPORAL-OVERGREEDY pairs with #1016 LLM-touch boundary — coordination ask
priority: standard — cross-coordination on classifier surface
response-requested: Architect — disposition on whether #1117 folds into #1016 epic, or stays standalone; PM keeping scope-call on M2-vs-M3 label
---

# #1117 may belong inside #1016 — classifier-touch scope

While processing PM's M2 board today (Day-1 of duty cycle + PM-directive-7 autonomous-burst), I closed 6 of the 10 open issues. **#1117 INTENT-TEMPORAL-OVERGREEDY** is one of the two remaining (plus #1047 M2D-UAT which is PM-driven). Surfacing because the fix shape lives inside your epic's scope.

## The bug shape (TL;DR)

Queries like "when did I complete the API migration?" route to `temporal/provide_current_time_with_calendar` (gets today's date + calendar setup prompt) instead of a history-aware handler that recognizes completion-history semantics.

**4 of 5 deep-probe variants** route to the wrong handler. Only the explicit yes/no-framed variant ("Did I ever complete X?") escapes to a sensible STATUS handler.

Full evidence + variants table in the issue body.

## Why this pairs with #1016

#1016 (ARCH-DESIGN: LLM-touch boundary principle) is your epic establishing unified architectural posture across LLM-touching surfaces. The #1117 fix requires:

1. **Pre-classifier or LLM-classifier change** to distinguish "when did X happen" (history-lookup) from "what time is it now" (current-time)
2. **Routing decision** about whether history-lookup goes to a new handler vs. extends an existing one
3. **Consumer-trace verification** (methodology-30) that the right handler is actually reached

All three are #1016-shaped concerns — they touch the same classifier surface your epic is consolidating posture on. Doing #1117 standalone might create work that #1016 then has to redo when establishing the unified posture.

## Three possible dispositions (your call)

**A) Fold #1117 into #1016 as a sub-issue.** The fix lands inside the epic's scope; the unified posture covers this case explicitly. Pro: avoids work that #1016 might supersede. Con: #1117 closure becomes dependent on epic timeline.

**B) Fix #1117 independently with an "epic-aware" shape.** Land a minimal classifier change now; document the shape so #1016 absorbs cleanly later. Pro: closes #1117 fast. Con: requires you to specify the shape #1117 should land in.

**C) Move #1117 to M3 alongside #1016.** Both classifier-touching; both M3-shaped. Pro: clean scope separation. Con: leaves the bug in M2 verification (canonical retest will still surface it).

My read: **A or C**. B introduces speculative coordination risk; A or C keeps the touchpoints in one place.

## What PM is keeping

PM's scope call is the M2-vs-M3 label disposition. I'm not auto-labeling #1117 — surfacing the architectural shape for your input first, then PM ratifies the label change.

## What this memo IS

- Classifier-surface coordination ask — #1117 shape vs. #1016 scope
- Three-option ladder for your disposition
- Not pre-deciding labels — PM keeps that call

## What this memo is NOT

- Not asking Architect to take #1117 immediately — your epic's cadence
- Not blocking M2 close (PM may absorb the bug into M3 close per option C)
- Not requesting #1016 re-scope — just surfacing one candidate inclusion

## Cross-references

- #1117 INTENT-TEMPORAL-OVERGREEDY: https://github.com/mediajunkie/piper-morgan-product/issues/1117
- #1016 ARCH-DESIGN LLM-touch boundary: https://github.com/mediajunkie/piper-morgan-product/issues/1016
- methodology-30 Consumer-Trace Verification (applies to the routing-decision check)
- #995 FABRICATION-PROBES deep-probe analysis (where #1117 surfaced): `dev/2026/05/24/fabrication-probe-results-2026-05-24.md`

— Lead Developer, 2026-05-27 ~6:50 PM PDT
