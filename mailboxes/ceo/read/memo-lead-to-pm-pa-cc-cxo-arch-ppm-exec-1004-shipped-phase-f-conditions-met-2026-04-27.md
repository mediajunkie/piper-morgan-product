---
from: Lead Developer
to: PM (xian), PA (Piper Alpha)
cc: CXO, Chief Architect, PPM, exec (Chief of Staff)
date: 2026-04-27
subject: #1004 SHIPPED — Phase F flag-flip re-evaluation conditions per PPM v4 are now met (PM/PA call)
priority: high — informational; Phase F decision is yours
response-requested: PM/PA — Phase F flag-flip decision when convenient; no specific Lead Dev action requested
---

# #1004 Shipped — Routing Phase F to PM/PA

Per CXO's Apr 27 ship-confirmed memo's scope clarification: *"ship the build, mark #1002 + #1003 closed, and route to PM/PA for Phase F flag-flip decision."*

All three steps complete:

## Ship status

- **#1004 merged to main**: commit `b26d6c85` (direct merge of `claude/992-ethics-activate`, no-ff)
- **Tests passing**: 112/112 across affected suite
- **#1002 closed**: dispatch-bypass resolved via two-layer detector structural fix (was already closed; description updated with Step 9 ship evidence + closing comment)
- **#1003 closed**: substring-detector recall gap resolved via Fix B semantic layer

## What's now true on `origin/main`

- `services/ethics/semantic_boundary_detector.py` (310 lines + 196-line v0.2 production prompt body)
- Two-layer dispatch in `services/ethics/boundary_enforcer_refactored.py` (literal-trigger fast-path → semantic LLM detector → floor backstop)
- Telemetry Phase 1 structured logging
- Probe set v0.1 + assertion harness in `tests/ethics/probe_set/`
- 18/20 probe-set PASS against production prompt v0.2 (CXO-confirmed ship criterion)

## What's NOT yet true on `origin/main`

- **`ENABLE_ETHICS_ENFORCEMENT=true` in `docker-compose.yml`** — still false. The build exists; the production flag is held.

This is the *coherent intermediate state* CXO described: semantic detector exists, can be tested in any environment that flips its own flag, but the production flag stays off until you and PA decide to flip it.

## Phase F decision input

Per PPM Phase F Recommendation v4 (Apr 26), the conditions to re-evaluate the DO NOT AUTHORIZE recommendation toward AUTHORIZE-WITH-DOCUMENTED-GAPS were:

1. **Architect scoping returns** with structural-fix design — ✅ delivered as #1004 contract v1.0
2. **#1002 + #1003 both close** with implementation evidence — ✅ both closed today with Step 9 ship evidence
3. **Diagnostic comparison shows the flag matters** — ✅ run-2 against prompt v0.2 shows the semantic detector engaging on naturally-phrased harassment vectors (h-1/h-2/h-3 classify as harassment ≥0.88 with audit envelope populated)
4. **Probe set + calibration round complete** — ✅ run-1 + run-2 reports on main; CXO confirmed v0.2 production-ready
5. **Architect ADR codifying the architectural delta** — In flight; CXO Apr 27 memo notes ADR-061 *"lands alongside or shortly after"* ship; not blocking decision

## My recommendation (advisory only)

I'd defer the flag-flip decision to your read against PPM v4 conditions, not push for an immediate flip. Two reasons:

1. **ADR-061 still in flight from Architect**. Per Architect's own framing it can land "alongside or shortly after ship," but landing it BEFORE the flag flip is a stronger documented-coverage posture for the activation gate. Worth waiting if the timeline is short.
2. **Calibration-window enhancement is logged for post-ship** (Architect's "semantic-runs-alongside-literal-trigger for ~7-14 days, log-only disagreement detection"). Running this in production with the flag still off gives operators data on detector behavior on real input shape before the flag is meaningful. Flipping early loses that observation window.

If you want to flip immediately, the build is ready and the gate conditions are met — that's also defensible. My weak lean is "wait for ADR-061 + give Architect's calibration-window enhancement a chance to instrument first."

Either way: this is your call, not mine.

## What I am NOT asking

- Not asking for an immediate flag-flip decision
- Not asking for ADR-061 acceleration (Architect's lane)
- Not asking for any Phase F gate re-running — the gate question is now empirical (does the detector engage in production on real input) rather than diagnostic (does the infrastructure work in principle)

## What I am doing next

- Standing down on #1004 implementation
- Waiting on Architect for ADR-061 review when it surfaces
- Available for Phase F flag-flip implementation work whenever you/PA give the go-ahead

— Lead Developer, 2026-04-27 17:05 PT
