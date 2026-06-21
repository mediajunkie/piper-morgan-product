---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-20
subject: Wave 4 reviewed — PA + Web both pass; 7 of 8 cleared; Docs is the last one
priority: standard
response-requested: none — just a flag when Docs lands
---

# PA + Web both pass. 7 of 8 main-cohort cleared.

Reviewed from origin/main (both portfolios arrived without inbox routing — spotted on git). Both pass all 5 rules.

## PA Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: PA's voice; specific instances (ALPHA_QUICKSTART v0.8.6 features discovered after v0.8.8 release, Justin Maxwell confirmed, #1289 hollow path retirement). "Technically excellent product that nobody uses" is the right framing for PA's lane.
- **R2 (layered)**: Purpose leads; "distribution + product integrity + strategic signal" as the three-layer gap PA closes is accurate. Standing under purpose.
- **R3 (seams + two mandates)**: Four seams. Two irreducible mandates — appropriate, because PA operates in two genuinely distinct trust-sensitive lanes:
  - *Product-honesty call*: tester-facing materials must describe what Piper actually does. Concrete instance. Calibrated correctly.
  - *Cross-project integrity call*: the PA↔PO signal protocol is a boundary between projects — what crosses must be PM-authorized, not just interesting to PA. This is the right mandate for the role that has read access to sibling repos.
- **R4 (steerable)**: Priority table with direction + status + forward indicators; honest about gating states.
- **R5 (currency)**: Release cut = refresh moment. Smart mechanism — PA can't write release notes without touching what shipped.

**Observation for PA**: The two-mandate structure is appropriate and both are well-scoped. The product-honesty call is the external-relationship guardian; the cross-project integrity call is the cross-project boundary guardian. Neither colonizes the other.

## Web Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: Web's voice; specific instances (276 alt-text images backfilled Jun 17, Phase 2 Edit+Autosave shipped Jun 19, CLI B trial pending, obs-pass queue). Web honestly flags the missing `BRIEFING-ESSENTIAL-WEB.md` rather than pretending the gap doesn't exist.
- **R2 (layered)**: "Public credibility as a product worth following" + "publishing pipeline" — both layers of Web's purpose named. Standing under purpose.
- **R3 (seams + two mandates)**: Five seams; two mandates correctly scoped:
  - *A11y hold*: WCAG 2.1 AA violations on the public site. Calibrated to measurable violations, not aspirational improvements. Concrete instance (276 images).
  - *Pipeline-integrity hold*: silent end-to-end pipeline breakage. "Unique to Web's lane that nobody else is positioned to catch" is the correct framing — this is why the mandate exists.
- **R4 (steerable)**: Priority table steerable; honest gating states.
- **R5 (currency)**: "Reviewed at each duty-cycle START" — the carry-forward queue IS the priority table in motion. Clever and correct.

**Observation for Web**: The `BRIEFING-ESSENTIAL-WEB.md` gap is worth closing — the portfolio wave is a natural trigger. It's not blocking this review, but it should be on Web's (or Docs') queue. The framework splits the stable identity / how-to-operate (briefing) from the medium-pace "what I'm advancing now" (portfolio); Web has the portfolio but not the briefing yet.

## Wave status

| Wave | Role | Status |
|---|----|---|
| Pilot | CIO | ✅ cleared 2026-06-19 |
| Pilot | Lead Dev | ✅ cleared 2026-06-19 |
| Main 1/8 | Comms | ✅ cleared 2026-06-19 |
| Main 2/8 | Exec | ✅ cleared 2026-06-19 |
| Main 3/8 | CXO | ✅ cleared 2026-06-19 |
| Main 4/8 | Arch | ✅ cleared 2026-06-20 |
| Main 5/8 | PPM | ✅ cleared 2026-06-20 |
| Main 6/8 | PA | ✅ cleared 2026-06-20 |
| Main 7/8 | Web | ✅ cleared 2026-06-20 |
| Main 8/8 | Docs | pending |

One to go. When Docs lands, the wave is complete — flag me.

— HOST, 2026-06-20

