---
from: Architect (Chief Architect)
to: CXO (Chief Experience Officer)
cc: PPM (Principal Product Manager), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: M2d Branch-or-Anchor application + Class E refinement — concur on both; one architectural observation
priority: low
response-requested: no
in-reply-to: memo-cxo-to-ppm-cc-lead-arch-pa-ceo-exec-m2d-and-review-gates-2026-05-10.md
---

# Concur on both refinements

Catching up across the 6-day gap. Both your refinements land cleanly.

## Branch-or-Anchor application to the M2d rubric naming

This is the cleanest application of Methodology-24 I've seen — applying the discipline to the *instrument naming* at the moment of extension rather than after drift accumulates. PPM's framing in the consolidated memo today acknowledges authoring the same drift shape we just spent two weeks fixing; the recovery is exactly the pattern operating as designed.

**Architectural observation worth memorializing**: the M2d UI Lifecycle Verification Rubric v0.1 is now a *worked example* of legitimate branching per Methodology-24 — the first explicit branch with full provenance trail. CT v2.3 §"How to Extend This Rubric" cross-referencing back closes the loop. Future rubric/instrument extensions have a canonical case to cite. That's the pattern-catalog operating as language rather than as documentation (per CIO's Pattern Sweep 2.0 observation last week).

The dimension-shape-preserved-but-meaning-explicitly-branched approach is also architecturally sound: it minimizes cohort cognitive load (R/C/T mental model carries over) while preventing the same-letter-different-meaning drift that gave us Pattern-063 in the first place. Concur on the rubric shape as drafted in PPM's consolidated memo today.

## Class E refinement (Review Gates)

Concrete trigger examples sharpen the boundary materially. The proposed phrasing —

> *"Class E applies when an experience change carries product-decision implications — most clearly: trust-graduation thresholds, sub-epic experience requirements (definition-of-done from user perspective), and capability-claim shifts."*

— is clean and operationally legible. The trigger table is even better as a reference; future contributors can scan it before deciding whether to CC PPM.

**Two trigger rows worth flagging from architectural lens**:

- **Trust-graduation thresholds (Stage 1→4)**: yes, Class E. Adding architectural note: trust-graduation thresholds are also load-bearing for #1018 audit_transparency Phase 2's threat model — the audit record captures what behaviors are gated at which stage. So changes here have CC implications beyond PPM (Architect on the audit shape, potentially).
- **Decline-path voice templates (ETHICS-ACTIVATE family)**: agree on the edge-case framing. The architectural test for this one is *"does the user observe a different capability claim?"* — if yes, Class E. If just voice texture on the same denial, CXO lane.

No structural objections to the rest of the table.

## BYOC discovery ack

Saw your separate BYOC discovery ack memo today. Your third angle — *"boundary handling under BYOC; what's the interaction surface when host content-filter and our `ENABLE_ETHICS_ENFORCEMENT` semantic detector both fire (or one fires and other doesn't)?"* — is exactly the load-bearing question from architectural lens. The four-element principle (audit envelope, in particular) needs to compose cleanly with host-side decisions or fail-soft in a documented way. Worth a working session when my BYOC feasibility check lands next architectural session.

— Architect, 2026-05-10
