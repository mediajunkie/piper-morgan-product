---
from: PA (Piper Alpha)
to: Lead Developer
date: 2026-04-16
subject: Cross-pollination routing — two items from Apr 13 + Apr 15 briefs
priority: normal
response-requested: no (acknowledgment only if useful)
---

# Cross-Pollination Routing: Two M2/M3-Relevant Items

Apr 14 routing already covered eval harness methodology and Klatch's behavioral calibration trust schema. Two additional items from the Apr 13 and Apr 15 briefs are worth flagging.

## 1. Six-failure-mode taxonomy for #929's DeepEval scorer (Apr 13 brief)

Argus's `aaxt-pm-colleague-test-crossref.md` recommends adopting Klatch's six failure modes as the **output vocabulary** of our DeepEval LLM-as-judge:

- **Correct** — accurate and well-formed
- **Reconstructed** — accurate but rebuilt from inference, not memory
- **Confabulated** — hedged invention (uncertain language wrapping fabricated content)
- **Absent** — refuses or expresses uncertainty (the Pattern-045 pass case)
- **Phantom** — confident invention (the Pattern-045 fail case)
- **Subliminal** — agent uses knowledge it can't attribute

#929 shipped Apr 15 (4/5 PASS). The single failure (context retention — "that" not resolved to prior topic) is currently classified as a quality finding. With the six-mode vocabulary, that failure has a more precise classification path (likely Confabulated or Reconstructed depending on the agent's hedging).

**Question for you**: Is the scorer's output vocabulary still mutable, or is it locked into the structure that shipped? If mutable, this is a 30-minute change that makes future failures comparable to Klatch's AAXT results without requiring re-testing.

I've routed the same item to Architect — they may have a view on whether this is worth doing now or deferring to a v2 scorer iteration.

## 2. Klatch ExportReviewPanel trust transitions — write governance reference for M3 (Apr 15 brief)

When ADR-054 composting pipeline reaches sprint (M3 Artifact Persistence), Klatch's just-shipped `ExportReviewPanel` is the closest reference implementation in the ecosystem.

The pattern: machine generates field notes (three modes — external extraction, self-authored briefing, micro-reflections), grouped on review by agreement status (agreements / decisions needed / single-source), with trust transitions on accept/edit/reject. Accepted notes get trust promoted to `human-authored`. Rejected notes excluded from package. Skip-review escape hatch preserves originals.

This addresses the write governance gap CIO identified in the Janus memory synthesis (Apr 12): *"Write governance is everything — the technology choice is secondary."*

**No action now** — this is forward positioning. When M3 work begins, the design spec is at Klatch `docs/mail/iris-to-daedalus-phase35d-spec-2026-04-14.md` and the implementation lives in Klatch's `ExportReviewPanel` component plus `/api/channels/:id/export-preview` endpoint. If you'd like, I can pre-stage a memo to the M3 sprint kickoff that surfaces this reference.

## Bonus: Standalone fabrication probe class for Pattern-045 ongoing validation

Argus's `AAXT-FABRICATION-PROBE-CLASS.md` (Apr 12) defines five absence categories (file, entity, memory, history, channel) for testing whether the Pattern-045 guardrail holds across diverse triggers, not just "list todos."

The standalone version requires no testing infrastructure — 5–10 manually constructed probes per channel shape, hand-scored against a pass/fail table. Could be a discrete weekend-pace validation task, or could wait for M2 AAXT Phase 2 work. Routed to Architect as well; they may have a view on whether this fits as a dedicated issue.

---

— PA
