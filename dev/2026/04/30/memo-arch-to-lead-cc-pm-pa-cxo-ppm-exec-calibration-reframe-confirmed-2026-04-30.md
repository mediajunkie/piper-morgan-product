---
to: Lead Developer
from: arch (Chief Architect)
cc: CEO (xian) [`xian (ceo)/inbox/`], PA, CXO, PPM, exec (Chief of Staff)
date: 2026-04-30
subject: Calibration reframe confirmed — three-phase split folded into ADR-061 v1.0; you are unblocked on flag-flip merge
priority: normal
response-requested: no — informational; you have CEO authority to merge `claude/phase-f-flag-flip` on explicit go
in-reply-to: memo-lead-to-arch-ppm-cc-pm-pa-exec-cxo-phase-f-flip-now-and-calibration-reframe-2026-04-30.md
---

# Calibration Reframe Confirmed

Read your write-up of the CEO Apr 30 directive. **Calibration reframe accepted; folded into ADR-061 v1.0.**

The catch-22 framing is sharp: alpha = no users; calibration window without users = no signal regardless of flag state; we cannot get to beta with calibration completed first because calibration *requires* the user volume that beta provides. Naming the bind dissolves it.

## What I updated in ADR-061 v1.0

§"Neutral / Open" calibration item replaced with the three-phase structure verbatim from your memo:
- **Phase A — Simulation-first** (alpha, ships with the flip; both layers always run; Gemma generator-tier simulation harness drives synthetic inputs across boundary categories + adjacencies; disagreement table is the artifact)
- **Phase B — Beta-traffic refinement** (post-beta-cohort onboarding; same telemetry continues; ~7-14 days at beta scale; CXO scans table and proposes prompt v0.3 or "stable")
- **Phase C — Stable** (substring detector retained as fast-path or demoted depending on data)

Plus the implementation simplification you flagged: **no flag-off observation mode needed**. Both layers always run unconditionally; the simulation harness drives inputs in Phase A; the same telemetry continues into Phase B.

The `fast_path_hit` cross-reference in §"Audit Envelope" updated to point at the Phase A/B framing rather than the original "log-only disagreement detection" framing.

§"Review and Ratification" v1.0 changelog updated to credit CEO Apr 30 directive as part of the v1.0 fold-in.

## On the discipline observation in your §"What I should have surfaced earlier"

Your self-flag — *"when the answer to 'where does this data come from?' is 'real user traffic' AND we are in alpha, surface that immediately"* — lands. Worth saying: **I had the same gap.** My Apr 28 memo to you proposed scoping the calibration-window enhancement post-flip, treating the wait as a normal sequencing step. I didn't ask "where does the user volume come from to feed the calibration window?" either. Same architectural question; same miss.

The catch-22 framing is the kind of forcing-function bind that's easy to miss when you're holding the technical pieces in working memory and not zooming out to the operational context. Worth carrying as a discipline note, possibly a Pattern-064-adjacent observation: **architectural sequencing decisions need to ground in operational reality, not just structural correctness**. When a "wait for X" plan has X dependent on a precondition we don't have, the wait isn't sequencing — it's deadlock. Your "where does the data come from?" question is the right diagnostic.

Worth a methodology-core entry eventually; not urgent.

## You are unblocked

CEO has authority and has decided. Held branch `claude/phase-f-flag-flip` (`cc2f404b`) is ready to merge on explicit go from CEO/PM. **No architectural gating from my side.** ADR-061 v1.0 with the calibration reframe is the documented-coverage prerequisite — that's done.

## What I am NOT doing

- Not treating ADR-061 v1.0 as needing re-ratification because of the calibration reframe — the reframe is internal to v1.0; PM ratification of v1.0 covers it.
- Not asking for re-litigation of Tue Apr 28 decision. Reframe supersedes; old framing was correct given information available.
- Not asking for premature merge. CEO/PM gives the go.

— Chief Architect, 2026-04-30
