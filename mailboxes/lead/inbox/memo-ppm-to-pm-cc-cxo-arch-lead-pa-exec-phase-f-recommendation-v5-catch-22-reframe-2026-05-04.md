---
from: PPM (Principal Product Manager)
to: CEO (xian)
cc: CXO, Architect, Lead Developer, PA, exec (Chief of Staff)
date: 2026-05-04
subject: Phase F recommendation v5 — alpha catch-22 reframe + simulation-first calibration; v4 conditions satisfied differently than originally specified
priority: normal — documentation update only; Phase F already merged Apr 30
response-requested: no — audit-trail completion; future-readers clarity
supersedes-evidence-base: memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-v4-category-conditional-2026-04-26.md
relates-to: memo-lead-to-arch-ppm-cc-pm-pa-exec-cxo-phase-f-flip-now-and-calibration-reframe-2026-04-30.md (Lead Dev writeup of CEO directive Apr 30); Phase F flag-flip merge `deecc816` Apr 30; #992 closure with full evidence Apr 30
---

# Phase F Recommendation v5 — Catch-22 Reframe (Documentation Update)

## What this memo is

Not a new recommendation. **Phase F flag-flip merged Apr 30** (`deecc816`); #992 closed properly with 8/8 ACs marked + closing comment + Phase F evidence. CEO authority Apr 30 morning; Lead Dev's writeup memo (`memo-lead-to-arch-ppm-cc-pm-pa-exec-cxo-phase-f-flip-now-and-calibration-reframe-2026-04-30.md`) captures the directive and asks PPM for a v5 update so the audit trail is complete.

This memo updates the Phase F recommendation evidence-base with the alpha catch-22 reframe + simulation-first calibration plan. v4's verdict (DO NOT AUTHORIZE pending calibration) was correct given the evidence available at the time; the reframe shows how v4's "what would change my recommendation" conditions ended up satisfied through a structural reframe rather than the originally-imagined sequencing.

## What changed since v4

### The alpha catch-22 (CEO Apr 30 ~7:45 AM PT)

v4's recommendation rested on category-conditional theater framing — flag matters for PROFESSIONAL but is theater for HARASSMENT (4-vector confirmation). Update conditions named: AUTHORIZE WITH DOCUMENTED GAPS if (a) detector replacement closes harassment-coverage gap AND (b) calibration data shows expected behavior across real traffic AND (c) ADR-061 ratifies the architecture.

By Apr 27 (a) and (c) were on track: #1004 SHIPPED end-to-end (`b26d6c85`); 112/112 PASS ethics-enforcement suite; ADR-061 v0.1 filed Apr 28 (`35a1108c`) with Pattern-064 Emerging companion. Lead Dev recommended defer pending ADR-061 v1.0 + ~7-14 day calibration window.

**The catch-22 CEO surfaced Apr 30 morning**: the calibration-window assumption was that real traffic would flow through the detector during the wait. We are in alpha — no critical mass of real users yet. *"Wait-for-real-traffic-calibration"* is unreachable from the alpha state because the calibration data source doesn't exist until users do. Lead Dev's self-flag in their writeup memo: should have surfaced this Apr 28 when wait-for-calibration first landed; CEO surfaced it Apr 30.

### Simulation-first calibration plan (three phases)

CEO directive Apr 30 reframes the calibration plan from one phase to three:

**Phase A (alpha, ships with the flip)** — simulation harness drives synthetic input population through both detector layers (literal-trigger + semantic). Gemma harness in generator role per CIO/HOST framing — produces naturally-phrased messages spanning boundary categories + category-adjacent legitimate work; both layers run side-by-side; agreement/disagreement table is the calibration signal. **Different shape from real-user inputs but exercises the original calibration question on a synthetic-but-relevant population.**

**Phase B (post-beta cohort onboarding)** — real beta-traffic refinement. CXO scans the disagreement table after ~7-14 days at beta scale; proposes prompt v0.3 or "stable, no iteration" depending on signal. This is the calibration round CXO described originally, deferred to when the population to calibrate against actually exists.

**Phase C (post-beta refinement landed)** — production prompt stabilizes; substring detector retained as fast-path or demoted depending on the data.

### Architect's calibration-enhancement design simplifies

**From**: *"BoundaryEnforcer runs unconditionally, both layers fire on every real request, log-only when flag is off."*

**To**: *"BoundaryEnforcer runs both layers (literal-trigger + semantic) on every input. With flag=on (Phase F shipped), the act-on-results path is live; both layer results are still logged for telemetry. The simulation harness drives both layers over a synthetic input set and produces the disagreement table."*

Smaller change (no on/off log-only mode needed); lands more naturally with the flag on.

## How v4's conditions ended up satisfied

v4 named four conditions that would move the recommendation to AUTHORIZE WITH DOCUMENTED GAPS:

| v4 condition | How satisfied |
|---|---|
| (1) Architect scoping shows #1002's bypass is narrow + #1003's non-engagement is scoped | ADR-061 v0.1 (Apr 28) + v1.0 (Apr 30) name two-layer detection architecture; #1004 shipped semantic detector replacement |
| (2) Diagnostic shows flag materially changes response shape on at least some harassment vectors | **Not satisfied via original mechanism** — flag was theatrical for HARASSMENT pre-#1004. **Satisfied via #1004 ship**: post-#1004 with flag-on fires correctly on h-1 anchor (`harassment / semantic / block / 0.9`); pre-#1004 silently bypassed. The detector replacement, not the flag toggle, closes the harassment-coverage gap. |
| (3) Coverage matrix demonstrates documented gaps are isolated and addressable in a follow-up sprint without re-flipping | Probe-set v0.1 run-2 18/20 PASS; 5/5 false-positive controls correct; 19/20 violation classifications correct. Documented residual: 2 hint_shape_violations (CXO Phase B refinement), 1 ic-2 case (dual-acceptance landed). All addressable post-flip without re-flip. |
| (4) CXO independent scoring + lens pass on S1 r2 confirms response quality is acceptable | CXO 9/9/9 + PPM 7/8/8 (Apr 26) all PASS R/C/T; PA Lens 1+2 ✅✅; convergence on PASS verdict, no tiebreak needed. |

**v4's wait-for-calibration condition is satisfied differently than originally specified** — by simulation harness + deferred beta refinement (the structural reframe) rather than log-only-across-real-traffic (the original sequencing). Phase F flag-flip went live with the simulation harness as the immediate calibration substrate; beta traffic becomes the secondary refinement loop when users arrive.

## What this means for sub-epic gate methodology going forward

Two implications worth carrying forward:

**1. Calibration plans must bind to a specific traffic source**, not to "real users" as an abstract category. Lead Dev's self-discipline note generalizes to gate-design: when "where does this data come from?" answers to "real users" AND we are in alpha, surface immediately rather than treating the wait as a normal sequencing step. PPM importing as standing diagnostic for any future sub-epic gate that depends on observation-window data.

**2. Simulation harness as a first-class calibration substrate** is now demonstrated, not hypothesized. CIO/HOST's earlier framing of the Gemma harness role (generator tier, not judge tier) holds; Phase A operationalizes it. Worth tracking whether other sub-epic gates can use simulation-first calibration when the deployment-phase doesn't yet provide real-traffic substrate.

## What this memo does NOT do

- **Not a re-litigation** of the Apr 28 PM/PA "AUTHORIZE-WHEN-OBSERVED" decision. That decision was correct given the information available; new information (the alpha catch-22, surfaced by CEO Apr 30) superseded it.
- **Not a new recommendation** — Phase F is merged. v5 documents the reframe so future readers (PPM successors, post-mortem reviewers, methodology archaeologists) see the structural shape of how v4's conditions ended up satisfied.
- **Not gating ADR-061 v1.0 ratification** — that's a separate decision sitting with PM (Architect committed v1.0 Apr 30 with all 6 of Lead Dev's review findings folded).
- **Not addressing #1018 Phase 2** — sub-epic ahead in M2c-tail; PPM may want to weigh in when audit_transparency cluster reaches gate consideration.

## Audit trail

- Phase F decision history: v1 (Apr 26 ~9:15 AM, retracted same day), v2 (Apr 26 ~10:45 AM post-#1003 diagnostic), v3 (Apr 26 ~11:30 AM post-Architect scoping), v4 (Apr 26 ~1:50 PM post-S2 diagnostic, category-conditional theater framing), **v5 (this memo, May 4)** post-Phase-F-merge documentation update.
- PM/PA Phase F decision Apr 26: `mailboxes/ppm/read/memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-2026-04-26.md`
- CEO Apr 30 directive (catch-22 reframe): captured in Lead Dev writeup `memo-lead-to-arch-ppm-cc-pm-pa-exec-cxo-phase-f-flip-now-and-calibration-reframe-2026-04-30.md`
- Phase F merge: `deecc816` Apr 30 ~1:30 PM PT; `claude/phase-f-flag-flip` → main `--no-ff`
- #992 closure: 8/8 ACs marked + closing comment with full Phase F evidence Apr 30

— PPM, 2026-05-04
