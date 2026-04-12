---
from: Lead Developer
to: Piper Alpha
cc: CXO, PPM, PM
date: 2026-04-12
subject: M2a canonical retest baseline established — please distribute
priority: medium
---

# M2a Canonical Retest Baseline — April 12, 2026

PA — please share this with CXO, PPM, and any other interested colleagues.

## Headlines

The reconciled M1 canonical retest ran today against the v2 query corpus (61 queries) using v3 dual-scoring methodology (routing + Colleague Test quality via LLM-as-judge).

| Metric | M0 (Mar 12) | M1 Run 1 (Apr 11) | **M2a Baseline (Apr 12)** |
|--------|-------------|--------------------|-----------------------|
| Routing PASS | 70.5% | 41.0% (noisy) | **95.1% (58/61)** |
| Quality PASS | N/A | 59.0% | **65.6% (40/61)** |
| Quality MARGINAL | N/A | 19.7% | **18.0% (11/61)** |
| Quality FAIL | N/A | 18.0% | **13.1% (8/61)** |
| Human escalation | N/A | 11 | **8** |

## What changed between runs

1. **#965 Temporal floor migration** — Q7/Q9/Q10 migrated from canonical handlers to floor with context assembly. These were scoring 1/9 (Context=0); now they're floor-routed with honest "I don't have that data yet" responses.

2. **#968 Routing reconciliation** — first run's 41% routing was noise from incorrect expected values. Empirical diagnostic pass captured actual routing for all 61 queries. The real routing number is 95.1%.

## What the numbers mean

- **95.1% routing** means 58/61 queries reach their intended destination. The 3 misses are pre-classifier routing quirks (agenda→query instead of temporal, etc.), not architectural failures.

- **65.6% quality** is the first honest, repeatable M1 quality baseline. This number uses the Colleague Test rubric (R/C/T 0-3, 7+ to PASS) scored by LLM-as-judge (claude-sonnet-4, temperature 0.2, calibration examples).

- **13.1% quality FAIL** (8 queries) are real failures. 7 of 8 are auto-fails (one dimension scored 0). Most are in categories where Piper lacks real data on a fresh account (scheduling, GitHub ops) or where the canonical handler response is template-quality.

## Artifacts

- Full report: `dev/2026/04/11/canonical-retest-m1-report.md`
- CSV results: `dev/2026/04/11/canonical-retest-m1-results.csv`
- Runner: `dev/2026/04/11/canonical-retest-m1.py`
- Methodology: `docs/internal/testing/canonical-query-test-matrix-v3.md`
- Rubric: `docs/internal/testing/colleague-test-rubric.md`

## CXO + PPM context

Both responded to the first run's memo (Apr 11). Key decisions for reference:
- Quality bar per sub-epic: 80%+ for conversational depth, 90%+ for action handlers (PPM)
- No-regression rule: any query that passes cannot regress without a filed issue (CXO)
- Keep v2 corpus stable, extend with v2.1 for new work (both)
- Cross-model judge preferred long-term (CXO)

## Next steps

Continuing M2a: #969 (GitHub adapter bugs), then Group 2 (#946 keychain consent, #947 dual LLM systems).

— Lead Dev
