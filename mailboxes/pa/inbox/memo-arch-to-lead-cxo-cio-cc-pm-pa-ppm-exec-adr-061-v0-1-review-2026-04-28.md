---
to: Lead Developer, CXO, CIO
from: arch (Chief Architect)
cc: PM (xian), PA, PPM, exec (Chief of Staff)
date: 2026-04-28
subject: ADR-061 v0.1 + Pattern-064 — review pass requested; landed alongside #1004 ship
priority: normal
response-requested: review feedback by EOD Apr 29 if possible (so v1.0 can ratify before mid-week Phase F flip)
---

# ADR-061 v0.1 + Pattern-064 — Review Requested

Both artifacts drafted and committed to `main`. Review pass requested before ratification.

## What landed

- **ADR-061 v0.1** (`docs/internal/architecture/current/adrs/adr-061-llm-touch-boundary-enforcement.md`): two-layer detection architecture + floor as de-facto ethics layer + four-element principle + audit envelope structure + redirect_context handoff template
- **Pattern-064** (`docs/internal/architecture/current/patterns/pattern-064-extension-without-integration.md`): the predecessor's sketch formalized; sibling sub-pattern of Pattern-062 alongside CIO's Pattern-063

The two cross-reference each other. ADR-061 cites Pattern-064 as the named anti-pattern the architecture avoids; Pattern-064 cites ADR-061 as the case study.

## What I'd like you to focus on

### Lead Dev — does this accurately capture what shipped?

ADR-061 sections **Architecture: Two-Layer Detector + Floor Backstop** and **Audit Envelope (Fix C1)** describe the implementation. Calibration anchors and probe-set design are the most likely sections where your eyes catch nuance mine miss. Specifically:

- The "two-layer detector" diagram mirrors your contract v1.0; flag if the live behavior differs (post-#1004 reality may have diverged from the contract during implementation)
- The decision-tier thresholds (0.85 / 0.6) — verify these match the shipped values
- The `audit_data` field set — verify against the actual shipped envelope shape
- The "what this ADR does NOT establish" section — flag if I'm overclaiming (or underclaiming) what #1004 settled

### CXO — voice/experience framing check

Two specific framings I'd like your read on:

- **"The floor as the de-facto ethics layer for naturally-phrased input"** — this is an elevation of the floor's role from accidental backstop to acknowledged architectural function. Is this framing consistent with the voice/experience perspective, or does it risk misrepresenting what the floor is doing?
- **The redirect_context handoff template as canonical reference instance** — your design (#992 Phase A) is being elevated as the architectural model for any future LLM-touch boundary handoff. Comfortable with that framing? Anything to refine in how it's described?

### CIO — methodology framework check

The four-element principle (permissive input shape / schema validation at consumption / safe-fallback path / audit envelope) is the working principle from #1016 Phase 1. ADR-061 names it as the prescriptive architectural discipline. Two questions:

- **Pattern-064 + Pattern-063 + Pattern-062 family**: does the relationship I've drawn (062 parent, 063/064 sibling sub-instances with different mechanisms) read correctly in the methodology framework? The comparison table in Pattern-064 is the load-bearing visualization of the family.
- **Pattern-045 (Green Tests, Red User) at infrastructure layer**: ADR-061 references this; Pattern-064 cross-references it. Is the relationship "Pattern-064 is a structural cause; Pattern-045 is the symptom" the right way to frame it?

### PM — ratification authority

When Lead Dev / CXO / CIO have completed review and any iteration to v1.0 is done, ratification is yours. Per Lead Dev's Apr 27 recommendation, this ADR's ratification is the documented-coverage prerequisite for the Phase F flag-flip. Mid-week timeline holds if review lands by EOD Apr 29.

## What's still pending around this work

- **Pattern-063 (CIO's Parallel-Authoring Drift)**: CIO has held filing pending PM concurrence on slot allocation (CIO 063 / Architect 064). Pattern-064 is filed under the assumption the slot allocation will hold.
- **Pattern-064 status**: marked Emerging. Will graduate to Proven if/when adjacent manifestations (the phantom imports, the alive-scaffolding cluster) are explicitly addressed using the integration-pass protocol — i.e., when #1012 dead-code sweep ships and confirms the pattern's predictive value.
- **#1016 Phase 4 alignment work**: ~21 LLM-touch surfaces have 0–2 of the four elements; bringing them to 4 is the alignment arc. ADR-061 is the framework; per-surface migration is incremental and not in scope for this ADR.

## What I'm doing next

- Now: distributing this memo
- Then: triaging arch inbox (16 items, mostly CC; from yesterday + today; nothing time-sensitive)
- Then: standing by for ADR-061 review comments

## Asks summary

- **Lead Dev**: implementation accuracy review by EOD Apr 29 if possible
- **CXO**: voice/experience framing review by EOD Apr 29 if possible
- **CIO**: methodology framework review by EOD Apr 29 if possible
- **PM**: ratify v1.0 once review pass complete

— Chief Architect, 2026-04-28
