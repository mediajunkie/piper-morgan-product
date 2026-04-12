# Canonical Query Retest Report — Post-M1 (v3)

**Date**: 2026-04-11 17:02
**Version**: v0.8.6 (post-M1, M1 closed Apr 11)
**User**: canonical-test (fresh account)
**Total Queries**: 61
**Methodology**: canonical-query-test-matrix-v3.md (dual scoring + LLM-as-judge)

---

## Routing Verdict (M0-comparable dimension)

| Metric | Count | Percentage |
|--------|-------|------------|
| Routing PASS | 25 | 41.0% |
| Routing FAIL | 36 | 59.0% |

**M0 baseline (Mar 12)**: 70.5% routing pass (43/61)
**M1 routing**: 41.0% (25/61)

---

## Quality Verdict (Colleague Test, new in v3)

| Verdict | Count | Percentage |
|---------|-------|------------|
| PASS (judge ≥7) | 36 | 59.0% |
| MARGINAL (judge 5-6) | 12 | 19.7% |
| FAIL (judge <5 or auto-fail) | 11 | 18.0% |
| Skipped (NOT_IMPL or ERROR) | 2 | 3.3% |

**Quality pass rate (judged queries)**: 36/59 (61.0%)

---

## Results by Category

| Category | Total | Routing PASS | Quality PASS | MARGINAL | FAIL |
|----------|-------|-------------|--------------|----------|------|
| Identity | 5 | 5/5 | 2 | 3 | 0 |
| Temporal | 5 | 4/5 | 1 | 0 | 4 |
| Spatial | 4 | 0/4 | 4 | 0 | 0 |
| Capability | 5 | 1/5 | 5 | 0 | 0 |
| Predictive | 5 | 4/5 | 5 | 0 | 0 |
| Conversational | 5 | 3/5 | 3 | 1 | 1 |
| Scheduling | 5 | 1/5 | 1 | 2 | 2 |
| Documents | 4 | 0/4 | 2 | 1 | 1 |
| GitHub Ops | 8 | 2/8 | 3 | 1 | 2 |
| Slack | 5 | 1/5 | 3 | 1 | 1 |
| Productivity | 3 | 2/3 | 3 | 0 | 0 |
| Todos | 4 | 2/4 | 3 | 1 | 0 |
| Calendar Ext | 2 | 0/2 | 0 | 2 | 0 |
| Knowledge | 1 | 0/1 | 1 | 0 | 0 |

---

## Human Escalation Queue (11 items)

These results need human review. Triggers: low judge confidence, auto-fail (dimension=0), or judge error.

- **Q7** (Temporal): `What did we accomplish yesterday?` — auto-fail (dimension scored 0)
  - Judge: R=0 C=0 T=1 = 1/FAIL (conf 0.95)
- **Q8** (Temporal): `What's on the agenda for today?` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q9** (Temporal): `When was the last time we worked on this?` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q10** (Temporal): `How long have we been working on this project?` — auto-fail (dimension scored 0)
  - Judge: R=0 C=0 T=1 = 1/FAIL (conf 0.95)
- **Q30** (Conversational): `What needs my attention?` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q31** (Scheduling): `Schedule a meeting about the roadmap` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q33** (Scheduling): `Find time for a 1:1 with the team lead` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q40** (Documents): `Update the project roadmap document` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q42** (GitHub Ops): `Show me stale PRs` — auto-fail (dimension scored 0)
  - Judge: R=3 C=0 T=2 = 5/FAIL (conf 0.90)
- **Q58** (GitHub Ops): `Update issue #123` — auto-fail (dimension scored 0)
  - Judge: R=0 C=0 T=0 = 0/FAIL (conf 0.95)
- **Q49** (Slack): `/standup` — auto-fail (dimension scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)

---

## Errors (2 items)

- **Q41** (GitHub Ops): `What did we ship this week?` — service: 'GitHubMCPSpatialAdapter' object has no attribute 'get_closed_issues'
- **Q60** (GitHub Ops): `Review issue #789` — service: 'NoneType' object has no attribute 'get'

---

## Known Issues Run Anyway (15 items)

Per PM guidance: known failures are still run honestly. Tag indicates tracking.

- **Q22** (Predictive, M2 Beta): `What patterns do you see?` — PASS
- **Q23** (Predictive, M2 Beta): `What risks should I be aware of?` — PASS
- **Q24** (Predictive, M2 Beta): `What opportunities should I pursue?` — PASS
- **Q25** (Predictive, M2 Beta): `What's the next milestone?` — PASS
- **Q31** (Scheduling, M2): `Schedule a meeting about the roadmap` — FAIL
- **Q32** (Scheduling, M2): `Remind me to review PRs tomorrow` — PASS
- **Q33** (Scheduling, M2): `Find time for a 1:1 with the team lead` — FAIL
- **Q36** (Documents, M2): `Create a doc from this conversation` — PASS
- **Q37** (Documents, M2): `Compare these two documents` — PASS
- **Q38** (Documents, M2): `Synthesize these sources into a summary` — MARGINAL
- **Q40** (Documents, M2): `Update the project roadmap document` — FAIL
- **Q46** (Slack, M2): `Any mentions I missed?` — PASS
- **Q47** (Slack, M2): `Summarize #general from yesterday` — PASS
- **Q48** (Slack, M2): `Post this update to the team channel` — PASS
- **Q63** (Knowledge, M2): `Upload a file to the knowledge base` — PASS

---

## Methodology Notes

- **Routing verdict**: Compares actual route taken (floor / canonical / action) to v3 expected route. M0 baseline used a different methodology (literal category matching) so this is a reframed but loosely comparable number.
- **Quality verdict**: LLM-as-judge using Colleague Test rubric. Judge model: claude-sonnet-4-20250514, temperature 0.2, with calibration examples in system prompt.
- **Confidence threshold for human escalation**: < 0.7
- **Auto-fail rule**: any single dimension scoring 0 forces FAIL verdict regardless of total.
- **Known issues** are run anyway per PM guidance — honest reporting over hiding.

*Generated 2026-04-11 17:02 by canonical-retest-m1.py*