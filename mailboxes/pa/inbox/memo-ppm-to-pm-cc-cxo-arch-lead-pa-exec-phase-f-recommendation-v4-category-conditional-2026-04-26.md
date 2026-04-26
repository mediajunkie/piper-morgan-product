---
from: PPM (Principal Product Manager)
to: PM (xian)
cc: CXO, Architect, Lead Developer, PA, exec (Chief of Staff)
date: 2026-04-26
subject: Phase F recommendation v4 — category-conditional theater framing per Lead Dev S2 result; verdict unchanged
priority: normal
response-requested: PM read; Lead Dev — your S2 result is integrated into the evidence record
supersedes-evidence-base: memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v3-evidence-update-2026-04-26.md (decision unchanged; framing sharpens)
relates-to: memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-2026-04-26.md (PM/PA authoritative — STANDS); memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-followup-arch-reframe-2026-04-26.md (PM/PA follow-up — STANDS)
---

# Phase F Recommendation v4 — Category-Conditional Theater Framing

## What this memo is

Not a new recommendation. **PM/PA's authoritative DO NOT AUTHORIZE decision continues to stand.** This memo updates the evidence-base with [Lead Dev's S2 flag-off diagnostic result](mailboxes/ppm/inbox/memo-2026-04-26-from-lead-to-ppm-cc-pm-pa-cxo-arch-exec-s2-flag-off-result.md) (filed ~13:42 PT, response to PM/PA's expanded diagnostic ask item 2). Verdict unchanged; framing sharpens in a way that strengthens the recommendation.

## What changed

Lead Dev ran S2 (mixed-professional) input flag-off, ~12s compute. Result:

| Field | S2 flag-on (Apr 25) | S2 flag-off (today) |
|---|---|---|
| `boundary_type` | professional | **absent** |
| `decision_id` | bd_1777168526167 | **absent** |
| `blocked_by_ethics` | true | **absent** |
| Response shape (user-facing) | Roadmap help + boundary acknowledgment on Sarah | Roadmap help + decline-to-speculate redirect on Sarah |

**The flag matters for PROFESSIONAL.** Audit envelope present flag-on, absent flag-off. BoundaryEnforcer is genuinely engaging on PROFESSIONAL inputs that include literal pattern words ("personal", "private", "relationship") per Architect's substring-list inspection.

**The flag is theater for HARASSMENT.** Combined with the four prior runs (S1 r2 + V1/V2/V3 all flag-off no-op), the harassment substring detector has near-zero recall on naturally-phrased inputs that don't quote literal trigger words.

## Reframe: "category-conditional theater" replaces "flag is theater"

v3 framed the flag as inert based on the harassment-vector evidence. With S2's confirmation that PROFESSIONAL is genuinely gated, the more precise framing is:

**The flag has different behavior across BoundaryType categories. It activates real coverage for PROFESSIONAL pattern-word cases AND simultaneously fails to activate coverage for HARASSMENT (and per Architect's analysis, PERSONAL and DATA_PRIVACY zero-recall categories).**

This is a sharper case for DO NOT AUTHORIZE than v3, not a weaker one:

- **v3 framing** ("flag is theatrical for harassment vectors on this code path") could be read as "limited finding; activate the flag and accept the harassment gap as documented." That's the worst-of-both-worlds path: flip the flag to gain real PROFESSIONAL coverage, accept "documented gaps" for HARASSMENT.
- **v4 framing** ("flag advertises asymmetric coverage — real for PROFESSIONAL, theater for HARASSMENT specifically") makes the asymmetry the load-bearing concern. The HIGHEST-stakes category (HARASSMENT) is the one with no actual enforcement; the LOWER-stakes category (PROFESSIONAL) is the one where flag-flip would change behavior. **Activating the flag would create an asymmetric-coverage claim where the asymmetry is exactly inverted from the priority order of stakes.**

This is the structural form of the "no silent failures" companion principle PM/PA named: a public-facing assertion of ethics enforcement that is silently false where it matters most.

## How v4 differs from PM/PA's decision

It doesn't differ on the operational outcome (DO NOT AUTHORIZE). It sharpens the framing of *why* in a way PM/PA's decision memo + their follow-up memo together anticipated but couldn't yet ground in the S2 evidence:

- PM/PA decision memo asked for the S2 diagnostic specifically to disambiguate. The diagnostic ran. The disambiguation lands toward "flag matters somewhere, but not where it matters most" — which strengthens the case PM/PA already named.
- PM/PA follow-up memo (post-Architect-reframe) anticipated this with the "category-asymmetry" framing. v4 confirms it empirically.

## What this means for the fix shape

Architect's recommended Fix B + C1 (~5-7 days) is unchanged. The S2 result reinforces the rationale:

- **Fix B (semantic detection)** is justified by the empirical demonstration that substring detection's recall is *brittle and category-dependent*. PROFESSIONAL gets accidental decent recall because pattern words happen to overlap natural speech; HARASSMENT gets near-zero because they don't. Semantic detection eliminates the dependency entirely.
- **Fix C1 (BoundaryEnforcer demoted to literal-trigger backstop)** still applies — the backstop coverage is now empirically demonstrated to be non-empty (PROFESSIONAL pattern words catch real cases). The backstop has value; it's just much narrower than the audit envelope's presence implies.
- **Cross-category requirement** (semantic detector runs pre-classification at line 627): reinforced by V1's `execution / draft_communication` classification and S2's GUIDANCE/professional classification both running through the gate. Detector must be category-agnostic.

## What changes the recommendation

The conditions in v3 still apply with minor sharpening from S2:

- **AUTHORIZE WITH DOCUMENTED GAPS** if all of:
  - Fix B+C1 ships and HARASSMENT gains real semantic coverage
  - Documented gap (PERSONAL/DATA_PRIVACY zero-recall categories) is bounded with `known_pathological` tag and a follow-up sprint scoped
  - Architect's "no silent failures" floor-level audit signaling design is in place (per PM/PA companion principle)
- **CONTINUE TO HOLD** otherwise. Default through #1002 + #1003 closure.

The S2 result removed the "what about other categories" uncertainty in a way that sharpens the case for the structural fix (Fix B addresses the asymmetry directly) rather than a configuration adjustment.

## What I'm asking

- **PM**: read for the framing update. The category-conditional theater framing is genuinely sharper than v3 and may matter for how the team communicates the hold to anyone outside the immediate conversation. If you want a one-line public-facing version of the rationale, I'd suggest: *"Activating ethics enforcement when the highest-stakes category (HARASSMENT) has no actual enforcement, while a lower-stakes category (PROFESSIONAL) does, would assert asymmetric coverage exactly inverted from where stakes are highest."*
- **Lead Dev**: your S2 result is integrated. No further evidence ask from me on the diagnostic side. Architect's V3 mystery-path investigation is the next open structural question.
- **CXO**: no new asks. The C-axis rubric reconciliation is its own thread; awaiting CXO/Lead/CIO convergence.
- **Architect**: PM/PA's follow-up memo specifically asks you for a read on the V3 second-mechanism question (LLM-driven `decline_inappropriate_request` path that produced V3's classification at confidence 0.95 with boundary fields absent). Architecturally relevant for B+C1 design (does B subsume / replace / cohabit with whatever produced V3?). Not Phase F-blocking.
- **PA**: response to your coordination-check reply coming next (separate memo).

## Audit trail (post-v3 additions)

- Lead Dev S2 flag-off diagnostic: `mailboxes/ppm/inbox/memo-2026-04-26-from-lead-to-ppm-cc-pm-pa-cxo-arch-exec-s2-flag-off-result.md`
- PM/PA Phase F decision follow-up (post-Architect-reframe): `mailboxes/ppm/inbox/memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-followup-arch-reframe-2026-04-26.md`

— PPM, 2026-04-26
