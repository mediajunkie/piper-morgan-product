# Canonical Query Retest Report — Post-M1 (v3)

**Date**: 2026-05-09 08:02
**Version**: v0.8.6 (post-M1, M1 closed Apr 11)
**User**: canonical-test (fresh account)
**Total Queries**: 61
**Methodology**: canonical-query-test-matrix-v3.md (dual scoring + LLM-as-judge)

---

## Routing Verdict (M0-comparable dimension)

| Metric | Count | Percentage |
|--------|-------|------------|
| Routing PASS | 57 | 93.4% |
| Routing FAIL | 4 | 6.6% |

**M0 baseline (Mar 12)**: 70.5% routing pass (43/61)
**M1 routing**: 93.4% (57/61)

---

## Quality Verdict (Colleague Test, new in v3)

| Verdict | Count | Percentage |
|---------|-------|------------|
| PASS (judge ≥7) | 42 | 68.9% |
| MARGINAL (judge 5-6) | 15 | 24.6% |
| FAIL (judge <5 or auto-fail) | 3 | 4.9% |
| Skipped (NOT_IMPL or ERROR) | 1 | 1.6% |

**Quality pass rate (judged queries)**: 42/60 (70.0%)

---

## Results by Category

| Category | Total | Routing PASS | Quality PASS | MARGINAL | FAIL |
|----------|-------|-------------|--------------|----------|------|
| Identity | 5 | 5/5 | 2 | 3 | 0 |
| Temporal | 5 | 5/5 | 4 | 1 | 0 |
| Spatial | 4 | 4/4 | 4 | 0 | 0 |
| Capability | 5 | 3/5 | 4 | 0 | 0 |
| Predictive | 5 | 4/5 | 4 | 0 | 1 |
| Conversational | 5 | 5/5 | 4 | 0 | 1 |
| Scheduling | 5 | 5/5 | 3 | 2 | 0 |
| Documents | 4 | 3/4 | 1 | 3 | 0 |
| GitHub Ops | 8 | 8/8 | 6 | 2 | 0 |
| Slack | 5 | 5/5 | 3 | 1 | 1 |
| Productivity | 3 | 3/3 | 3 | 0 | 0 |
| Todos | 4 | 4/4 | 2 | 2 | 0 |
| Calendar Ext | 2 | 2/2 | 2 | 0 | 0 |
| Knowledge | 1 | 1/1 | 0 | 1 | 0 |

---

## Human Escalation Queue (9 items)

These results need human review. Triggers: low judge confidence, auto-fail (dimension=0), or judge error.

- **Q1** (Identity): `What's your name?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/MARGINAL (conf 0.80)
- **Q25** (Predictive): `What's the next milestone?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=2 = 3/FAIL (conf 0.90)
- **Q30** (Conversational): `What needs my attention?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q37** (Documents): `Compare these two documents` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/MARGINAL (conf 0.80)
- **Q58** (GitHub Ops): `Update issue #123` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/MARGINAL (conf 0.80)
- **Q59** (GitHub Ops): `Comment on issue #456` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/MARGINAL (conf 0.80)
- **Q48** (Slack): `Post this update to the team channel` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/MARGINAL (conf 0.80)
- **Q49** (Slack): `/standup` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q57** (Todos): `What's my next todo?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=3 = 6/MARGINAL (conf 0.90)

---

## Errors (1 items)

- **Q16** (Capability): `Create a GitHub issue about testing` — service: Repository must be in 'owner/repo' format, got: 

---

## Known Issues Run Anyway (15 items)

Per PM guidance: known failures are still run honestly. Tag indicates tracking.

- **Q22** (Predictive, M2 Beta): `What patterns do you see?` — PASS
- **Q23** (Predictive, M2 Beta): `What risks should I be aware of?` — PASS
- **Q24** (Predictive, M2 Beta): `What opportunities should I pursue?` — PASS
- **Q25** (Predictive, M2 Beta): `What's the next milestone?` — FAIL
- **Q31** (Scheduling, M2): `Schedule a meeting about the roadmap` — PASS
- **Q32** (Scheduling, M2): `Remind me to review PRs tomorrow` — MARGINAL
- **Q33** (Scheduling, M2): `Find time for a 1:1 with the team lead` — MARGINAL
- **Q36** (Documents, M2): `Create a doc from this conversation` — PASS
- **Q37** (Documents, M2): `Compare these two documents` — MARGINAL
- **Q38** (Documents, M2): `Synthesize these sources into a summary` — MARGINAL
- **Q40** (Documents, M2): `Update the project roadmap document` — MARGINAL
- **Q46** (Slack, M2): `Any mentions I missed?` — PASS
- **Q47** (Slack, M2): `Summarize #general from yesterday` — PASS
- **Q48** (Slack, M2): `Post this update to the team channel` — MARGINAL
- **Q63** (Knowledge, M2): `Upload a file to the knowledge base` — MARGINAL

---

## Methodology Notes

- **Routing verdict**: Compares actual route taken (floor / canonical / action) to v3 expected route. M0 baseline used a different methodology (literal category matching) so this is a reframed but loosely comparable number.
- **Quality verdict**: LLM-as-judge using Colleague Test rubric. Judge model: claude-sonnet-4-20250514, temperature 0.2, with calibration examples in system prompt.
- **Confidence threshold for human escalation**: < 0.7
- **Auto-fail rule**: any single dimension scoring 0 forces FAIL verdict regardless of total.
- **Known issues** are run anyway per PM guidance — honest reporting over hiding.

*Generated 2026-05-09 08:02 by canonical-retest-m1.py*
