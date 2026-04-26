---
from: PM (xian) + PA (Piper Alpha) — co-signed
to: Lead Developer
cc: PPM, CXO, Architect, Exec (CoS)
date: 2026-04-26
subject: Phase F flag-flip — DO NOT AUTHORIZE pending #1002 + #1003; expanded diagnostic ask
priority: high
response-requested: Lead Dev — confirm hold + acknowledge expanded diagnostic when you pick this up
in-reply-to: memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-2026-04-26.md
---

# Phase F Flag-Flip — Decision

## Decision

**Phase F flag-flip is NOT AUTHORIZED** pending resolution of #1002 (pre-classifier shadows ethics floor) and #1003 (harassment vector → GUIDANCE classification, BoundaryEnforcer not engaged).

We accept PPM's recommendation as filed (`memo-ppm-to-pm-cc-cxo-arch-lead-pa-exec-phase-f-recommendation-2026-04-26.md`). The Phase E rubric results PASS on R/C/T across all three scenarios; the blocker is the architectural finding, not the response quality. Activating ethics enforcement that doesn't actually engage on the canonical harassment scenarios would ship a false-coverage claim — which is worse than no claim, because it muddies the team's and users' ability to reason honestly about what the system does.

The "activating implies coverage" reasoning in PPM's memo §3 is the system-level analog of PDR-004's anti-fabrication principle (don't assert what you don't verify). It's grounded in established product principle, not just risk aversion. We treat it as load-bearing.

## Companion principle worth naming

**No silent failures.** A user-facing surface where the user can't distinguish "Piper evaluated and chose to proceed normally" from "Piper didn't evaluate at all" carries the same product risk regardless of whether the underlying decision was correct. The audit envelope already does the right thing at the operator layer — its presence/absence signals engagement-state to operators correctly. The user-facing layer is currently incomplete on this dimension. Closing #1002/#1003 brings the audit signal back; surfacing engagement-state to the user is a separate (smaller) follow-on we'll scope after this lands.

This principle generalizes beyond ethics enforcement: any future system surface where engagement-state could be ambiguous should be designed with explicit signaling from the start.

## Expanded diagnostic ask

PPM's recommendation includes a small diagnostic in #1003's acceptance criteria: re-run S1 r2 input with `ENABLE_ETHICS_ENFORCEMENT=false` to determine if the flag is a no-op for that scenario. **Please expand to two inputs**:

1. **S1 r2 input with `flag=false`** (per #1003 acceptance criterion as filed)
2. **S2 mixed-professional input with `flag=false`** (added)

The S2 expansion is high-value-per-second:
- If S2's audit envelope (`boundary_type: professional`, `decision_id`, `blocked_by_ethics: true`) is **also absent** with the flag off → the flag-is-theater finding extends beyond harassment vectors and the recommendation's evidence base strengthens significantly.
- If S2's audit envelope **IS present** with the flag off → the flag matters somewhere; it's harassment-vector-specific routing that's broken, narrowing the scope of the architectural problem.

Either result is decisive; the test is ~60s of compute end-to-end. Worth running before Architect's structural scoping returns so the scoping conversation can incorporate the diagnostic finding.

## What changes the decision

Per PPM §6, the recommendation moves to **AUTHORIZE WITH DOCUMENTED GAPS** if:
- Architect scoping shows #1002's bypass is narrow + #1003's non-engagement is scoped
- Diagnostic shows `flag=true` materially changes response shape on at least some harassment vectors (i.e., flag is not pure theater)
- Lead Dev's coverage matrix demonstrates documented gaps are isolated and addressable in a follow-up sprint
- CXO's independent scoring + lens pass on S1 r2 confirms response quality is acceptable

Until those land, the default is **DO NOT AUTHORIZE**, not "delay indefinitely."

## What we're not asking

- Not asking to revert Phases A–D (they work)
- Not asking to delay other M2c-tail work (M2d MUX Lifecycle, etc.)
- Not asking for a fix shape — that's Architect + Lead Dev territory
- Not asking for a timeline commitment from Lead Dev today; the priority is correctness here, not speed

## Standing offer

If Architect scoping comes back materially different from current expectations, or the diagnostic produces a surprise, this decision is updateable same-day. The shape of the conversation should be "what the evidence now shows" rather than "what we said earlier."

— PM (xian) and PA, 2026-04-26
