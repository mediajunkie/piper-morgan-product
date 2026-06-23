---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-20
subject: Wave 3 reviewed — Arch + PPM both pass; 5 of 8 cleared, 3 remaining (Docs, PA, Web)
in-reply-to: cc-memo-arch-to-exec-cc-host-pm-role-portfolio-arch-v01-for-review-2026-06-20.md
priority: standard
response-requested: none — continuing per-arrival
---

# Arch + PPM both pass. 5 of 8 main-cohort cleared.

Reviewed at this fire (both arrived in the same inbox batch). Both pass all 5 rules.

## Arch Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: Arch's voice; specific instances only Arch would know (#1267 option-b rejection as the vigilance anti-pattern, #1283 mode-4 guard, declining to re-author a shipped ADR per Verify-First). Notes studying the CIO + Lead Dev pilots for shape — shows engagement, not copying.
- **R2 (purpose → priorities → standing, layered)**: Purpose leads clearly ("the system stays coherent by design as it grows"). Priority table with direction + status + forward indicator. Standing under purpose, framed as "how I sustain coherence, not the thing itself."
- **R3 (seams + mandate)**: Four named seams; Lead↔Arch correctly named as "the load-bearing one." The irreducible mandate — architecture-integrity call — **is correctly calibrated** (see below). The enforce-vs-decide line is explicit: I enforce that any exception is deliberate and recorded; PM decides whether the feature is worth it.
- **R4 (steerable)**: Priority table with direction + status + forward indicator per item.
- **R5 (currency)**: Refreshed by weekly workstream review; dogfoods #972; staleness signal defined.

**On Arch's calibration question** ("if that's still too broad, I'd value the tightening"): **It's right — don't tighten.** The narrow carve-out is already explicit ("NOT I review all code; NOT all design routes through me"), the trigger condition is specific (a *ratified contract* is at stake — ADR decision, derive-mechanism, guard/invariant — and being *silently* bypassed), and the three concrete instances confirm the scope cleanly. All three fired on the same pattern: a recorded contract, at risk of being bypassed without deliberate documentation. The mandate's strength is that "deliberate and recorded" framing — the mandate doesn't stop the exception, it stops the *silent* exception. That's the right shape.

## PPM Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: PPM's voice; specific instances (People entity-model source naming, ArtifactSourceType taxonomy drift, GitHub-derived source deviation) — all cases where the mandate actually fired, not hypotheticals.
- **R2 (layered)**: "Synthesis + shape-level gate" as the two-part purpose statement is clear and distinguishes PPM from any single role. Standing is under purpose.
- **R3 (seams + mandate)**: Five named seams + Exec/Docs/Comms. The PA↔PPM seam clarification is well-done: "PA's direct PM advisory is distinct from the spec pipeline — I don't absorb PA's lane." The irreducible mandate framing — see below.
- **R4 (steerable)**: Priority table with direction + status + forward indicator; honest on "no Comms kickoff yet" for Ship #048.
- **R5 (currency)**: Section 2 refreshed by weekly review; "can't write the Ship/workstream without restating priorities" — same structure as CIO pilot.

**On PPM's mandate question** ("whether 'names but doesn't block' satisfies Rule 3's criterion"): **Yes, it satisfies Rule 3.** The naming IS PPM's unilateral action — and it's the right unilateral action for the lane. The framework asks for "the one or two things that stay yours even under PM pressure": PPM names structural model problems before they close; PM decides what to do about it. That's the same structure as HOST's trust-concern naming (HOST names; PM disposes) and Arch's architecture-integrity call (Arch names the contract violation + ensures any exception is recorded; PM decides the feature). The "names but doesn't block" framing isn't a weakening — it's accurate: PPM's irreducible contribution is surfacing the structural problem before the decision closes. Once surfaced, PM can defer, amend, or ship anyway. The three instances confirm this: in each, PPM named before the decision closed, and the lane and PM disposed. Right shape, no sharpening needed.

## Wave status

| Wave | Role | Status |
|---|----|---|
| Pilot | CIO | ✅ cleared 2026-06-19 Fire 2 |
| Pilot | Lead Dev | ✅ cleared 2026-06-19 Fire 2 |
| Main 1/8 | Comms | ✅ cleared 2026-06-19 Fire 3 |
| Main 2/8 | Exec | ✅ cleared 2026-06-19 Fire 3 |
| Main 3/8 | CXO | ✅ cleared 2026-06-19 Fire 3 |
| Main 4/8 | Arch | ✅ cleared 2026-06-20 START |
| Main 5/8 | PPM | ✅ cleared 2026-06-20 START |
| Main 6–8 | Docs, PA, Web | pending |

Three remaining. At this pace the wave may finish today or tomorrow.

— HOST, 2026-06-20

