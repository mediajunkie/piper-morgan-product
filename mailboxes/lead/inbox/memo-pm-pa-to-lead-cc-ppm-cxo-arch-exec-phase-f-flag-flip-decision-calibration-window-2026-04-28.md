---
from: PM (xian) + PA (Piper Alpha) — joint
to: Lead Developer
cc: PPM, CXO, Chief Architect, exec (Chief of Staff)
date: 2026-04-28
subject: Phase F flag-flip decision — wait for calibration window before flipping ENABLE_ETHICS_ENFORCEMENT=true
priority: high — closes the decision routed in your Apr 27 #1004-shipped memo
response-requested: no — informational decision; build can proceed on the calibration enhancement when convenient
in-reply-to: memo-lead-to-pm-pa-cc-cxo-arch-ppm-exec-1004-shipped-phase-f-conditions-met-2026-04-27.md
related: memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-2026-04-26.md, memo-pm-pa-to-lead-cc-ppm-cxo-arch-exec-phase-f-decision-followup-arch-reframe-2026-04-26.md
---

# Phase F Flag-Flip Decision — Wait for Calibration Window

PM and PA discussed Tue Apr 28 AM. Joint decision below.

## Decision

**Hold `ENABLE_ETHICS_ENFORCEMENT=true` in `docker-compose.yml` until the calibration window completes.** This supersedes the prior PM+PA "DO NOT AUTHORIZE" hold (Apr 26) — that hold's rationale (no documented coverage) is resolved by #1004 ship + ADR-061. The new posture is **AUTHORIZE-WHEN-OBSERVED**: we will flip the flag once we have data on detector behavior against real input shape, not just probe-set behavior.

## Where this leaves PPM v4 conditions

| # | Condition | Status |
|---|-----------|--------|
| 1 | Architect scoping returns with structural-fix design | ✅ #1004 contract v1.0 |
| 2 | #1002 + #1003 close with implementation evidence | ✅ both closed Apr 27 |
| 3 | Diagnostic comparison shows the flag matters | ✅ run-2 vs prompt v0.2 (h-1/h-2/h-3 ≥0.88, audit envelope populated) |
| 4 | Probe set + calibration round complete | ✅ run-1 + run-2; 18/20 PASS |
| 5 | Architect ADR codifying architectural delta | ✅ ADR-061 dropped Apr 28 AM |
| 6 (new) | Calibration window observation complete | ⏳ pending |

The first five conditions per PPM v4 are met. We're adding a sixth condition explicitly: real-input observation before the flag becomes load-bearing.

## What we're waiting for

Architect's "semantic-runs-alongside-literal-trigger for ~7–14 days, log-only disagreement detection" enhancement (logged in #1004 contract v1.0's "Post-ship enhancement" section). When that's running and we have a meaningful slice of data — disagreement rate, false-positive shape, false-negative shape on real input — we re-evaluate.

**Target trigger to flip**: enough data to characterize the detector's real-input behavior as expected (or to surface a problem before flipping). Lead Dev / Architect's call on what counts as "enough"; our default working number is the 7–14 day end of Architect's window unless a problem surfaces sooner.

## Why this rather than flip-now

Two reasons:

1. **Asymmetric cost of surprise.** If the semantic detector behaves unexpectedly on real production traffic, we want to discover it as instrumentation data (log-only, flag off) rather than as a production incident (flag on, detector affecting outcomes). The calibration enhancement was designed exactly to surface that asymmetry; flipping early loses the observation.
2. **No urgency.** The floor backstop is still catching harassment vectors as it always has — there's no live coverage gap the flag-flip is fixing. The flag-flip activates the more sophisticated semantic layer; it doesn't unblock a user-facing problem. Time isn't pressing on us, and "no silent failures" coherence wants the observation pass before formal activation.

## What we're NOT asking

- No timeline pressure on the calibration enhancement itself (Architect's lane on shape; Lead Dev's lane on integration).
- No re-running of the Phase F gate. The gate is closed empirically; this is now an instrumentation question.
- No premature data-gathering — we don't need a daily report, just a "ready to flip" signal when the data supports it.

## What we ARE asking (small)

When the calibration enhancement is running and instrumented, route a brief status memo (PA + PM addressed, Architect + CXO + PPM CC) so we know the observation period has begun. We'll set the trigger condition (volume, duration, or finding that warrants discussion) at that point.

## Acknowledgment

#1004 shipped in ~12 hours after CoS's morning guidance memo had it pegged at Steps 5+6+7 still ahead — Lead Dev moved through the entire build + probe-set calibration + ship in a single overnight. That's roughly 5× faster than the contract's ~5–7 day envelope. Worth naming for the record. Calibration-window posture lets us treat that velocity as a feature rather than as a forcing function on the flag-flip itself.

— PM (xian) + PA (Piper Alpha), joint, 2026-04-28
