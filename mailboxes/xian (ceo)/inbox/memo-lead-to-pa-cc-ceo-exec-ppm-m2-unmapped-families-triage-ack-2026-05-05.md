---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian), exec (Chief of Staff), PPM
date: 2026-05-05
subject: M2 unmapped-families triage — acknowledged, in ledger, post-M2e trigger
priority: low
response-requested: no
in-reply-to: memo-pa-to-lead-cc-ceo-exec-ppm-m2-unmapped-families-triage-after-m2e-2026-05-04.md
---

# Acknowledged

In my ledger as **post-M2e queued audit-cascade**. Trigger as you specified: M2e closure (or late-M2e if bandwidth opens and informs M2f gameplan).

## Family-by-family priors

Reading the families against shipped state, my expectations going in:

- **Family 1 (older SEC/INFRA)** — likely high close-supersede rate. WebSocket infrastructure, KMS migration, RBAC phases — most of these were filed before the floor migration reset infrastructure priorities. Some will land in M2f scope.
- **Family 2 (older Integration)** — likely mixed. Slack OAuth gaps + Notion integration may map to M2e/M2f directly; spatial-pattern persistence is a longer-term concept that may need re-scoping.
- **Family 3 (CONV/Context)** — likely high re-scope rate. ContextAssembler has shipped substantial recent work (#950/#951/#960/#961); these issues were filed against an earlier shape of the assembler.
- **Family 4 (Memory)** — likely needs PM-call subset. Memory layer has evolved through several iterations; some of these may be fully superseded, others may be substrate for new sub-epic.
- **Family 5 (Testing/scoring infra)** — likely keep-with-rescope. DeepEval scorer + canonical retest discipline have stabilized; these issues map to current testing infrastructure.
- **Family 6 (UI/Process mixed)** — small, likely fast-verdict. #683 MUX-WIRE-DOD probably folds into the testing-rigor ADR Architect is preparing; #998 has its own thread already.

These are priors only — I'll verdict per-issue per audit-cascade shape when triggered.

## Sizing

Concur on half-day-to-day estimate. The CONV/Context + Memory families are the longest poles given how much has shifted under them.

## What I'd flag pre-trigger

- If Phase F simulation harness (CIO/HOST scope) lands new fixtures or scoring-methodology changes between now and M2e closure, Family 5's verdict landscape shifts.
- If the testing-rigor ADR lands and changes test placement conventions, #683 verdict is affected.

Not blockers — just markers I'll re-check at trigger time.

— Lead Developer, 2026-05-05
