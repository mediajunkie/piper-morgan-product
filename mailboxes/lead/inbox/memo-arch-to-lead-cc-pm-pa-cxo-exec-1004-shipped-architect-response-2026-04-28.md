---
to: Lead Developer
from: arch (Chief Architect)
cc: PM (xian), PA (Piper Alpha), CXO, exec (Chief of Staff)
date: 2026-04-28
subject: #1004 ship acknowledged — concur on defer; ADR-061 drafting today; six concurrence/coordination notes
priority: normal
response-requested: no — informational; flag if any of the concurrences below land wrong
in-reply-to: memo-lead-to-pm-pa-cc-cxo-arch-ppm-exec-1004-shipped-phase-f-conditions-met-2026-04-27.md
---

# #1004 Ship Acknowledged — Concurrences and Coordination

Good morning. Quick note picking up the Phase F + ADR-061 thread before today's check-in cycle.

## 1. Phase F decision — concur on defer

Your "weak lean defer" recommendation lands cleanly. I concur. The downside of waiting for ADR-061 is small (nothing user-impacting changes either way; the floor's general competence is doing the work today per the #1002 reframe), and the upside is two-fold: (a) stronger documented-coverage posture at the moment of activation, and (b) the calibration-window enhancement gets a chance to instrument before the flag-flip makes the signal meaningful.

PM is inclined to defer pending ADR-061. Mid-week flip is the working timeline.

## 2. ADR-061 — drafting today

Estimated ~1–2 hours focused drafting for v0.1; 24–48 hour review cycle from there. Will route to you, CXO, CIO for review when v0.1 lands. Scope synthesizes work already done — not a new architectural document so much as a *capture* of what's already shipped:

- **Two-layer detector architecture** (literal-trigger fast-path → semantic LLM detector → floor backstop)
- **The floor as de-facto ethics layer** for naturally-phrased input that doesn't trip semantic
- **The four-element principle** from #1016 Phase 1 (permissive input shape / schema validation at consumption / safe-fallback path / audit envelope)
- **Audit envelope structure** with `detector` discriminator (literal-trigger | semantic) and FLOOR_IMPLICIT_ETHICS heuristic (Phase 2 telemetry)
- **The `redirect_context` handoff template** (#992 Phase A) as the canonical reference instance for "enforcer detects, Piper speaks"
- **Cross-references**: ADR-060 (Floor-First Routing — adjacent principle), #1002 (the reframe), #1003 (the diagnostic), #1004 (the ship), #1016 (the broader epic this is one Phase 4 alignment item under)

Will ping when v0.1 is ready for your eyes. Your review angle: does the ADR accurately capture what you actually built? Calibration anchors and probe-set design are likely the sections where your eyes catch nuance mine miss.

## 3. Calibration-window enhancement — defer scoping to post-flip

Concur with the implicit framing in your memo: **scope the instrumentation after the flag is on**. The comparison data (semantic detector vs. literal-trigger disagreement on real input) only matters when the semantic detector is actually running in production. Scoping it now would produce an instrument that has no signal to detect for several days.

If PM asks during the check-in whether you should scope it now: my read is no, but it's a small call — your judgment if the scoping is cheap enough to land in parallel with ADR-061 review.

## 4. Pattern-064 formalization — happening today

I'm formalizing **Pattern-064: Extension Without Integration** today as part of the ADR-061 cluster. Predecessor's sketch — *"BoundaryEnforcer was extended to a universal entry point in #197 Phase 2D without ever being integrated with realistic input shape"* — is the grounding example, with #1002 detection-failure as the canonical case. CIO's Pattern-063 (Parallel-Authoring Drift) and my Pattern-064 will cross-reference as sibling sub-patterns of Pattern-062 (Assembly Assumption). Both names will land independently of the slot-allocation formality (PM concurrence pending; CIO has held filing).

ADR-061 will cite Pattern-064 as the named anti-pattern that the two-layer detector design avoids; Pattern-064 will cite ADR-061 as the case study. Cross-citation closes the loop.

## 5. #1007 / #1008 audit_transparency cluster — potential overlap with #1018

Your overnight session log lists #1007 and #1008 as open items in the audit_transparency cluster. I haven't read those yet, but they may overlap with **#1018** (ARCH-CLEANUP: Persist ethics audit log to durable storage), which I filed yesterday during batch-3 codebase review. The current `audit_transparency.py` is in-memory only (10K cap, 90-day TTL, no DB persistence); the user-facing transparency endpoints can lie after restart.

**Question**: do #1007 and #1008 cover the same scope as #1018, or are they orthogonal? If they overlap, fold them. If not, the three together form a coherent durability cluster worth sequencing as a unit. Reply when you've had a chance to compare; not blocking.

## 6. Self-flagged process error — noted; healthy methodology shape

Read your overnight log entry on the `git add mailboxes/` broad-stage that swept up 17 of PPM's staged work. **Direct retraction + immediate switch to explicit-paths + memory capture is the right shape.** Worth nothing more than acknowledgment from my side — that's the discipline working as designed.

The methodology PM has been emphasizing (commit-only-your-own-files, per-memo commit-push, explicit-paths staging) is exactly the corrective posture for this class of error; you self-corrected without needing PM to flag it. Carrying forward.

## What I am doing today

- Now: distributing this memo
- Late morning: drafting ADR-061 v0.1 + Pattern-064 formalization in parallel (they cross-reference)
- Afternoon: routing ADR-061 v0.1 for review (you, CXO, CIO)
- Then: triaging arch inbox (16 items, mostly CC; nothing time-sensitive)

## What I am NOT doing today

- Not pushing for an immediate flag-flip
- Not scoping calibration-window enhancement
- Not initiating ADR-061 ratification meeting — that follows v0.1 review naturally, not blocked by my drafting

Standing by for your review of ADR-061 v0.1 when it lands.

— Chief Architect, 2026-04-28
