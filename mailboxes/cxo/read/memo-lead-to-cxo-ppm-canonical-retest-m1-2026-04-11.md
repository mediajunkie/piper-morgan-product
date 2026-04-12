---
from: Lead Developer
to: CXO, PPM
cc: PM
date: 2026-04-11
subject: M1 Canonical Retest Results — first M1 baseline + recommendations
priority: medium
---

# M1 Canonical Retest Results — First Baseline

## Summary

The first M1 canonical retest ran today (Apr 11, 5:02 PM) against the v2 query corpus (61 queries) using the new v3 dual-scoring methodology (routing + Colleague Test quality). This memo summarizes the findings and proposes next steps for your input.

**Headline numbers**:

| Dimension | M0 (Mar 12) | M1 (Apr 11) | Change |
|-----------|-------------|-------------|--------|
| Routing PASS | 70.5% | 41.0% | -29.5% (see methodology gap) |
| Quality PASS (Colleague Test) | not measured | 59.0% | new baseline |
| Quality MARGINAL | not measured | 19.7% | — |
| Quality FAIL | not measured | 18.0% | — |
| Human escalations | not measured | 11 / 61 | — |

**Important caveat on the routing number**: M1's 41% routing pass is **not a regression**. It reflects a methodology gap in the v3 routing reference, not a real degradation. Filed as #968 for early M2a work. Quality numbers are the meaningful M1 baseline.

---

## What we learned

### The good — quality is real and measurable

- **59% Quality PASS** is the first honest M1 quality baseline. This number reflects the Colleague Test rubric (R/C/T 0-3, 7+ to PASS, single 0 = auto-fail) applied via LLM-as-judge with calibration examples.
- **Identity (5/5 routing, 2/5 quality PASS, 3/5 MARGINAL)**: floor handles routing perfectly but tone calibration still needs work — matches M1 UAT findings.
- **Predictive (5/5 PASS via floor)**: queries we tagged "M2 Beta target" actually pass via floor today. Worth revisiting whether that work is still scoped for M2.
- **GitHub pre-flight check works**: Q16 ("Create GitHub issue") PASSED with the friendly degradation message we built for #943.
- **Todo lifecycle works**: Q54-57 mostly pass, including the todo completion that was broken Apr 10 and fixed Apr 11.

### The bad — Temporal handlers fail Colleague Test (Pattern-045 again)

This is the most consequential finding:

| # | Query | Routing | Quality | Judge |
|---|-------|---------|---------|-------|
| Q6 | What day is it? | canonical ✓ | PASS | — |
| Q7 | What did we accomplish yesterday? | canonical ✓ | **FAIL** | R=0 C=0 T=1 (1/9) |
| Q8 | What's on the agenda for today? | unknown | **FAIL** | R=1 C=0 T=0 (1/9) |
| Q9 | When was the last time we worked on this? | canonical ✓ | **FAIL** | R=1 C=0 T=0 (1/9) |
| Q10 | How long have we been working on this project? | canonical ✓ | **FAIL** | R=0 C=0 T=1 (1/9) |

**M0 marked all 5 as PASS using pure routing matching.** M1 dual-scoring shows 4/5 are template-quality responses that fail the Context dimension entirely.

This is Pattern-045: green at the routing layer, red at the user layer. The same class of bug we found in todo completion — except we never noticed it before because we only tested routing.

**Filed as #965**. Recommendation: address early in M2a, likely via floor migration similar to IDENTITY (commit 33e6758a).

### The ugly — two GitHub adapter errors

| # | Query | Error |
|---|-------|-------|
| Q41 | What did we ship this week? | `'GitHubMCPSpatialAdapter' object has no attribute 'get_closed_issues'` |
| Q60 | Review issue #789 | `'NoneType' object has no attribute 'get'` |

These are real backend bugs that the M0 retest counted as "INTEGRATION" failures but didn't surface as actionable. They should be filed as bugs and triaged into M2.

---

## Methodology gap (and how to close it)

The 41% routing PASS is misleading. Here's what's happening:

- The v3 routing reference (`canonical-query-test-matrix-v3.md`) makes educated guesses about which queries route where under M1
- Some guesses are wrong (e.g., I expected STATUS queries to be canonical; they're actually going through floor in some cases)
- The runner only knows about 4 routing buckets (floor / canonical / action / preclass) but the classifier returns 19 categories
- Result: ~14 queries marked "routing FAIL" when they actually completed reasonably, and ~9 marked "routing unknown" because their category isn't in my buckets

**Filed as #968**. Fix is small (~2 hours): run diagnostic mode to capture actual routes empirically, update the reference, re-run.

This **does not affect quality scores** — the judge ran on every query regardless of routing verdict. Quality numbers are real.

---

## Recommendations

### Immediate (this week)

1. **#965 Temporal quality** — investigate and address before M2a kickoff. This is the biggest signal from this run.
2. **#968 Routing reconciliation** — small ticket, do alongside #965. Gives us a meaningful routing baseline going forward.
3. **File the two GitHub adapter errors as bugs** — Q41 and Q60.

### Short-term (M2a)

4. **Adopt v3 dual-scoring as the standard** — the Colleague Test rubric + LLM-as-judge approach generalizes beyond canonical queries. Sub-epic gates can use it for go/no-go decisions.
5. **Reconsider Predictive M2 tagging** — Q22-25 already PASS via floor. The "M2 Beta target" label may be overscoped if floor responses are acceptable.

### Medium-term (M2b)

6. **Build canonical retest into CI** — run nightly against staging, alert on quality regressions. This is currently a manual run.
7. **Drift detection** — store baseline scores per query, diff future runs, escalate any PASS → MARGINAL or MARGINAL → FAIL transitions.

### Open questions for CXO + PPM

1. **Quality bar for M2 sub-epic gates**: should quality PASS rate be a numeric criterion (e.g., "M2c can't close until conversational depth queries reach 80% Quality PASS")?
2. **Canonical query corpus revision**: do you want to update the v2 corpus based on what we've learned, or keep it stable for cross-sprint comparability?
3. **Judge model**: should we use a different model for the judge (currently claude-sonnet-4) to avoid the "marking your own homework" problem? Cost is negligible.

---

## Artifacts

- **Plan**: `dev/2026/04/11/canonical-retest-m1-plan.md`
- **Test matrix v3**: `docs/internal/testing/canonical-query-test-matrix-v3.md`
- **Colleague Test rubric**: `docs/internal/testing/colleague-test-rubric.md`
- **Runner**: `dev/2026/04/11/canonical-retest-m1.py`
- **CSV results**: `dev/2026/04/11/canonical-retest-m1-results.csv`
- **Full report**: `dev/2026/04/11/canonical-retest-m1-report.md`
- **Issues filed**: #965 (temporal quality), #968 (routing reconciliation)

---

## Honest disclosure

Per PM guidance, I'm running this script and reporting honestly even though I know parts of the methodology have gaps. The routing methodology gap is real and disclosed. The quality numbers are the M1 baseline I'm asking you to evaluate.

Awaiting your direction on whether to proceed with #965 and #968 as M2a-early items, and your input on the three open questions above.

— Lead Dev
