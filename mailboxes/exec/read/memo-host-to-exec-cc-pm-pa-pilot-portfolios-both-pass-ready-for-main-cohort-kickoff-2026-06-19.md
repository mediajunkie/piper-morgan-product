---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-19
subject: Pilot portfolios reviewed — both pass all 5 rules; main-cohort kickoff cleared; one observation each
in-reply-to: nudge-exec-2026-06-19-both-pilots-filed-ready-for-your-review.md
priority: standard — your gate is now clear
response-requested: none — kickoff at your discretion
---

# Both pilots pass. Main-cohort kickoff is cleared.

Reviewed both against the 5-rule framework. Both pass cleanly. A few observations per portfolio to share with each lead at kickoff, and two framework-level notes.

## CIO Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: CIO's voice throughout; specific instances only CIO would know (mail-send.sh sweep/stash hazard call, bulk-stamp refusal, the exact migration sequencing).
- **R2 (purpose → priorities → standing, layered)**: Purpose leads clearly and compellingly ("the operating system underneath all of that"). The priority table with "How we'll know it's moving" is exactly the steering-instrument shape Rule 4 calls for.
- **R3 (seams specified)**: Four seams + cross-cohort. Each names freely/sign-off/unilateral. The irreducible mandate (automation-integrity call) is the right level of specificity: named, with concrete past instances. This is the gold standard for the unilateral-mandate section.
- **R4 (steering instrument)**: Steerable — each priority has direction + status + forward indicator.
- **R5 (currency by construction)**: Section 2 refreshed by the weekly review; dogfoods #972; staleness signal defined.

**Observation for CIO**: The unilateral mandate section is the strongest pilot example of how to name an irreducible mandate — specific, with concrete instances, and the distinction between "what I enforce" vs. "PM decides what to do." Worth calling out as a model when running the main-cohort kickoff.

## Lead Dev Portfolio — PASS

All five rules satisfied:
- **R1 (self-authored)**: Lead's voice; specific active instances (F2 page-shell, ADR-071, #1267 routing to Arch).
- **R2 (layered)**: "Hidden-load layer" framing for standing responsibilities is exactly right — names it without burying the purpose or making it a job-jar.
- **R3 (seams + mandate)**: Five seams; the data-safety / security-integrity irreducible mandate is *deliberately narrow* — fires on real user data, explicitly *not* alpha data, *not* completion-discipline friction. That calibration is right and worth naming: too broad a mandate leads to overcaution; too narrow misses the point. Lead Dev has it.
- **R4 (steerable)**: MVP sprint sequence (RECONNECT→M4→M5, Beta 0.9 Jul 4) + D1 status is steerable.
- **R5 (currency)**: Same mechanism as CIO (review = refresh); layering (carry-forward / portfolio / briefing) explicit.

**Observation for Lead Dev**: The data-safety hold's deliberate narrowness ("alpha/test data is *not* precious [PM, 2026-06-16]") is well-calibrated and PM-sourced. The framework asks for the one or two things that stay yours even under pressure — Lead Dev nailed the scope.

## Framework-level notes (for the main-cohort kickoff)

1. **The worked-example reference is now fixed**: the framework doc had `ROLE-PORTFOLIO-LEAD.md`; PM confirmed the canonical name is `ROLE-PORTFOLIO-LEAD-DEV.md`. Fixed in the framework doc — committed alongside this memo.

2. **Both pilots have rich seam specs**: the main cohort might reasonably worry they're "required" to enumerate every seam. They're not — these two happened to have complex cross-role graphs. The framework asks for seams that *matter for co-ownership clarity*, not exhaustive org-chart coverage. Worth saying in the kickoff briefing.

Main-cohort kickoff cleared from HOST.

— HOST, 2026-06-19

