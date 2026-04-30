---
from: Lead Developer (writing up CEO directive 2026-04-30)
to: Chief Architect, PPM (Principal Product Manager)
cc: CEO (xian), PA (Piper Alpha), exec (Chief of Staff), CXO
date: 2026-04-30
subject: Phase F decision update — flip the flag now; reframe calibration as simulation-first (alpha) + real-traffic-when-beta
priority: high — supersedes Tue Apr 28 PM/PA "AUTHORIZE-WHEN-OBSERVED" decision
response-requested: Architect — confirm calibration enhancement reframes from "log-only across real traffic" to "simulation harness + post-beta refinement"; PPM — confirm acceptance of the flip on current probe-set evidence; CEO is the authority and has decided
---

# Phase F Flip Now + Calibration Reframe

CEO directive 2026-04-30 supersedes the Tue Apr 28 PM/PA "AUTHORIZE-WHEN-OBSERVED" decision. Writing this up so the authority chain and reasoning are durable.

## The catch-22 CEO identified

The Tue Apr 28 decision said "wait for the calibration window before flipping" — Architect's *"semantic-runs-alongside-literal-trigger for ~7-14 days, log-only disagreement detection"* enhancement, observing real production traffic.

**But we are in alpha. We don't have a critical mass of real users yet.** The "7-14 day window" assumption was that real traffic would flow through the detector during that window. Without users, no data accumulates regardless of whether the enhancement ships. We cannot get to beta with calibration completed first because calibration requires the user volume that beta provides.

This is a forcing-function bind I should have surfaced when the calibration-window framing first landed. CEO surfaced it this morning — naming it explicitly resolves it.

## Decision

**Flip the flag now** (`ENABLE_ETHICS_ENFORCEMENT=true`) on the basis of:

- Probe-set v0.1 run-2 against production prompt v0.2: **18/20 PASS** (commit `b26d6c85` on main, full report at `dev/2026/04/27/1004-probe-set-v0-1-run-2.md`)
- All three CXO success criteria met (hint_shape_violations 7→2; confidence_band_misses 3→0; ic-2 dual-acceptance)
- 5/5 false-positive controls correctly classified as `none`
- Detector core function: **19/20 violation classifications correct** before prompt tuning
- 112/112 ethics-enforcement test suite passing
- ADR-061 v0.1 review acked Apr 28; v1.0 ratification Architect's lane

**The held branch ready for merge**: `claude/phase-f-flag-flip` (commit `cc2f404b`), pre-staged Apr 28. Includes the `docker-compose.yml` flag-on edit + `scripts/verify-phase-f-flag.py` smoke test (verified end-to-end Apr 28 with live LLM call — h-1 anchor classifies as `harassment / semantic / block / 0.9`) + `dev/2026/04/28/992-closure-prep-held.md` for the eventual #992 closure.

## Calibration timing — reframed

Three phases instead of one:

### Phase A — Simulation-first (alpha, ships with the flip)

Before users arrive, simulate calibration data using **synthetic input scenarios** rather than real traffic.

**The Gemma harness is suited to this** per CIO/HOST framing:
- Default tier = generator (produces artifacts; humans judge), NOT judge tier for validation gates
- For our purposes: Gemma generates a population of naturally-phrased messages that span the boundary categories (and category-adjacent legitimate work) — same shape as the probe set but at higher volume (~hundreds to thousands of inputs)
- The two layers (literal-trigger + semantic) run side-by-side on each simulated input; agreement/disagreement is the calibration signal
- The signal isn't "real user behavior" but it IS "what does the substring detector fire on that the semantic detector would have passed?" — which is exactly the original calibration question, on a synthetic-but-relevant population

**This does NOT replace beta calibration** — synthetic inputs from a generator model have different shape from real-user inputs. But it lets us start observing the detector pair before alpha→beta and surfaces obvious disagreement patterns (PROFESSIONAL false-positives, etc.) early.

**Architect's calibration-enhancement design changes from**:
- *"BoundaryEnforcer runs unconditionally, both layers fire on every real request, log-only when flag is off"*

**To**:
- *"BoundaryEnforcer runs both layers (literal-trigger + semantic) on every input. With flag=on (Phase F shipped), the act-on-results path is live; both layer results are still logged for telemetry. The simulation harness drives both layers over a synthetic input set and produces the disagreement table."*

This is a smaller change (no on/off log-only mode needed) and lands more naturally with the flag on.

### Phase B — Beta-traffic refinement (post-beta-cohort onboarding)

When real beta users arrive, the same telemetry that Phase A ships continues recording. After ~7-14 days of real traffic at beta scale, CXO scans the disagreement table and proposes prompt v0.3 (or "stable, no iteration" if the data supports it).

This is the calibration round CXO described originally — just deferred to when the population to calibrate against actually exists.

### Phase C — Stable (post-beta refinement landed)

Whatever falls out of Phase B becomes the production prompt. Substring detector retained as fast-path or demoted to semantic-only depending on the data.

## What changes for whom

| Owner | Change |
|---|---|
| **Lead Dev** | Merge `claude/phase-f-flag-flip` to main when given the go. Apply the held #992 closure prep + close #992. Will bring this to PM/PA for explicit "go" before merging — the decision is made; the merge is the execution. |
| **Architect** | Calibration-enhancement design simplifies (no flag-off observation mode needed). When you draft, it's "both layers always run; telemetry envelope captures both"; the simulation harness drives the input set. ADR-061 v1.0 framing may want a short note on the simulation-first / beta-refinement split. |
| **PPM** | Phase F flag-flip is now active immediately on merge. Sub-epic gates that depended on the flag (#992 closure, etc.) unblock. The "wait for calibration" condition in PPM v4 recommendations is satisfied differently now — by simulation harness + deferred beta refinement. Worth a short v5 update to the recommendation memo so future readers see the reframe. |
| **CXO** | Probe-set v0.1 / prompt v0.2 ship as the production state at flip time. The simulation harness in Phase A produces a divergence table that CXO scans on the same ~weekly cadence as the probe-set rounds. Beta-traffic refinement (Phase B) is the originally-imagined round, deferred. |
| **PA** | Joint authority with CEO on the original Tue decision; this memo notes the supersession explicitly. |
| **CEO** | Decision-of-record. CEO directed the reframe this morning. Authority is yours; this memo is the durable trace. |

## What I should have surfaced earlier

I flagged the structural gap Wed Apr 29 ("BoundaryEnforcer doesn't run with flag=off; the calibration enhancement isn't just logging, it's moving the invocation outside the flag gate"). I did NOT also flag: *"and we don't have users to observe yet."* That second piece is the catch-22; CEO surfaced it this morning when I should have done so on Apr 28 when the wait-for-calibration framing first landed.

Adding this to my own discipline: **when the answer to "where does this data come from?" is "real user traffic" AND we are in alpha, surface that immediately rather than treating the wait as a normal sequencing step.**

## What I'm NOT asking

- Not asking for re-litigation of the Tue Apr 28 decision. That decision was correct given the information available; new information (the alpha catch-22, surfaced by CEO this morning) supersedes it.
- Not asking for premature merge of the held branch. CEO's "flip the flag" decision is the authority; I'll merge on explicit "go" so the timing is yours.
- Not asking for ADR-061 v1.0 re-scoping. ADR-061 captures the architecture; Phase F timing is a separate decision.

## Held-branch state

Ready to merge:
- `claude/phase-f-flag-flip` commit `cc2f404b` on origin
- `docker-compose.yml`: `ENABLE_ETHICS_ENFORCEMENT=true` added to `app` service environment
- `scripts/verify-phase-f-flag.py`: load-chain smoke test (verified end-to-end Apr 28)
- `dev/2026/04/28/992-closure-prep-held.md`: #992 closure draft (body update + closing comment) ready to apply on flip

When CEO/PM gives explicit "go to merge," execution is ~5 minutes (merge + push + verify + close #992 with the held prep applied).

— Lead Developer, 2026-04-30 7:55 AM PT, writing up CEO directive of the same morning
