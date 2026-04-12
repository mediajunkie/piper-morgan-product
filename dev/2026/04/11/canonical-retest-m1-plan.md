# M1 Canonical Retest Plan

**Date**: 2026-04-11
**Author**: Lead Developer
**Approved by**: PM (xian)
**Purpose**: Establish post-M1 baseline against canonical query corpus, with updated quality bar reflecting M1 architecture and decisions.

---

## Background

- **M0 baseline (Mar 12, #884)**: 70.5% pass rate (43/61), pure routing test
- **M1 closure (Apr 11)**: Floor inversion, identity migration to floor, todo completion fixes, GitHub pre-flight, fabrication guardrails
- **No v3 canonical queries spec exists** — the query corpus (v2, 63 queries) didn't change. What needs updating is the **test methodology and matrix**, not the query list.
- **M0 retest script** (`dev/2026/03/12/canonical-retest-884.py`) is stale: pinned to literal `expected_intent` strings, doesn't account for floor-routed categories, has no quality dimension.

## Goals

1. Produce an honest M1 baseline against the v2 canonical query corpus
2. Use a higher quality bar (Colleague Test rubric, not just routing match)
3. Compare to M0 baseline (70.5%) for impact assessment
4. Generate recommendations for CXO + PPM about query corpus revision and methodology

## Non-Goals

- Modifying the canonical query list itself (deferred — recommendations only, leadership decides)
- Hiding known-failing queries (run them honestly, tag with tracking issue)
- Adding new queries from M1 UAT (deferred — recommend, don't merge)

---

## Methodology

### Dual Scoring

Each query gets evaluated on TWO dimensions:

**Routing**: Does the query reach the intended handler/floor path?
- PASS / FAIL
- For floor-routed queries, "intended" = "reaches the floor with non-empty domain context"

**Quality** (Colleague Test rubric):
- Three dimensions, 0-3 each: **Relevance**, **Context**, **Tone**
- 7+ = PASS
- Any single dimension scoring 0 = AUTO-FAIL (regardless of total)

### Quality Verdict Pipeline

1. **Tier A (preliminary, fast)**: Heuristic check — non-empty, non-template, non-error response. Used for first-pass screening.
2. **Tier B (rigorous, primary)**: LLM-as-judge using Colleague Test rubric. Returns score + confidence.
3. **Tier C (escalation)**: Human review for queries where the LLM judge reports low confidence.

PM guidance: "We can use A to reach a preliminary tentative response, but I think we should actually prefer to use B with LLM as judge and a human appealed to for cases where LLM does not feel confident."

### Honest Failure Reporting

Per PM guidance: "Things that we know are going to fail still need to be run. We have to get honest test results. Of course, we can acknowledge that things don't surprise us and that they're known issues and that we're already tracking them, but we don't want to start ignoring them or hiding them just because we already know about them."

Each row in the result matrix includes:
- `routing_pass` / `quality_pass` columns (independent)
- `known_issue` column with tracking issue number if applicable
- `judge_confidence` column for Tier B verdicts

---

## Deliverables

1. **`docs/internal/testing/canonical-query-test-matrix-v3.md`** — Updated test matrix:
   - All 63 queries from v2 corpus
   - Routing expectation reconciled with M1 reality (floor vs canonical handler)
   - Colleague Test criteria for floor-routed queries
   - Known-issue tags for queries we expect to fail

2. **`dev/2026/04/11/canonical-retest-m1.py`** — Updated runner:
   - Hits `/api/v1/intent` like the M0 script
   - Captures routing intent + full response message
   - Calls LLM-as-judge for floor-routed quality scoring
   - Outputs CSV with both routing and quality verdicts
   - Generates summary report comparing to M0 baseline

3. **`dev/2026/04/11/canonical-retest-m1-results.csv`** — Raw results

4. **`dev/2026/04/11/canonical-retest-m1-report.md`** — Summary report:
   - Overall pass rates (routing / quality / both)
   - Category breakdown
   - M0 vs M1 comparison
   - Failure mode classification
   - Recommendations for CXO + PPM (query corpus, methodology, deferrals)

5. **Memo to CXO + PPM** — Summary + recommendations, mailbox-delivered

---

## Execution Steps

1. Draft v3 test matrix (reconcile routing expectations with M1 floor architecture)
2. Update runner script (LLM-as-judge integration, dual scoring, fresh CSV format)
3. Create/recreate fresh test account if needed
4. Run against current server (latest M1 code)
5. Generate CSV + report
6. Spot-check LLM-as-judge verdicts where confidence is low
7. Draft memo to CXO + PPM
8. Commit and mail

---

## Open Questions (for self-resolution during execution)

1. **LLM-as-judge model**: Use the same Anthropic key/model as the server (claude-sonnet-4)? **Decision**: yes, simplest path. Track judge calls separately in report so cost/escalation rate is visible.

2. **Confidence threshold for Tier C escalation**: If judge returns confidence < X, flag for human. **Decision**: start with confidence < 0.7. Tunable in code.

3. **Test account credentials**: M0 used `canonical-test` / `canonical-test-2026`. **Decision**: recreate that account on the current fresh DB so the script can authenticate.

---

## Success Criteria

- All 63 v2 canonical queries executed against current server
- Each query has a routing verdict + quality verdict (Tier B or C)
- Report includes M0 baseline comparison
- Recommendations clearly distinguish "known issues already tracked" from "new findings"
- Memo delivered to CXO + PPM mailboxes

---

*Ready for execution upon completion of doc audit (parallel subagent task).*
