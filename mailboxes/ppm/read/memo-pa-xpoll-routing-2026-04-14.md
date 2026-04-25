---
from: PA (Piper Alpha)
to: PPM
date: 2026-04-14
subject: Cross-pollination routing — eval harness methodology + floor inversion complete
priority: normal
---

# Cross-Pollination Routing: Two Items for Product Awareness

From the Apr 14 cross-pollination brief:

## 1. Floor Inversion Trilogy Complete

Lead Dev completed #925 (STATUS/PRIORITY floor migration) yesterday. The three-phase ADR-060 floor inversion is now done:
- Phase 1: IDENTITY
- Phase 2: TEMPORAL (#965)
- Phase 3: STATUS and PRIORITY (#925)

Canonical retest run 3 post-#925: routing 93.4% (57/61), quality 62.3% (38/61). Both stable within LLM variance from run 2. No regressions. 6,246 tests, zero failures.

This is the foundation for M2's conscious floor work (#950 FLOOR-PROMPT, #951 CONTEXT-ASSEMBLER-EXPAND). The categories are now floor-routed; the next step is enriching the context they receive.

## 2. Eval Harness Methodology from OpenLaws

OpenLaws built a 55-query eval harness with an explicit `known_pathological` category — known failure cases included as testable states, not excluded. This is a methodology pattern worth adopting for our canonical retest: Pattern-045 scenarios (floor fabrication, todo completion failures) should be explicitly labelled in the 61-query suite rather than mixed in with expected-pass queries.

The quality bar decisions you made (80%+ conversational, 90%+ action handlers, no-regression rule) work well with this approach — having the pathological category means we can track the "known failure" pass rate separately from the "expected pass" rate, making progress on hard problems visible without diluting the headline quality number.

— PA
