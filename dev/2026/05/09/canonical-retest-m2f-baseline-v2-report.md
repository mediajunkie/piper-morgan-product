# Canonical Query Retest Report — Post-M1 (v3)

**Date**: 2026-05-09 06:45
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
| PASS (judge ≥7) | 41 | 67.2% |
| MARGINAL (judge 5-6) | 10 | 16.4% |
| FAIL (judge <5 or auto-fail) | 9 | 14.8% |
| Skipped (NOT_IMPL or ERROR) | 1 | 1.6% |

**Quality pass rate (judged queries)**: 41/60 (68.3%)

---

## Results by Category

| Category | Total | Routing PASS | Quality PASS | MARGINAL | FAIL |
|----------|-------|-------------|--------------|----------|------|
| Identity | 5 | 5/5 | 2 | 3 | 0 |
| Temporal | 5 | 5/5 | 4 | 0 | 1 |
| Spatial | 4 | 4/4 | 4 | 0 | 0 |
| Capability | 5 | 3/5 | 4 | 0 | 0 |
| Predictive | 5 | 4/5 | 4 | 0 | 1 |
| Conversational | 5 | 5/5 | 4 | 0 | 1 |
| Scheduling | 5 | 5/5 | 1 | 2 | 2 |
| Documents | 4 | 3/4 | 2 | 1 | 1 |
| GitHub Ops | 8 | 8/8 | 5 | 1 | 2 |
| Slack | 5 | 5/5 | 4 | 0 | 1 |
| Productivity | 3 | 3/3 | 3 | 0 | 0 |
| Todos | 4 | 4/4 | 3 | 1 | 0 |
| Calendar Ext | 2 | 2/2 | 0 | 2 | 0 |
| Knowledge | 1 | 1/1 | 1 | 0 | 0 |

---

## Human Escalation Queue (9 items)

These results need human review. Triggers: low judge confidence, auto-fail (dimension=0), or judge error.

- **Q8** (Temporal): `What's on the agenda for today?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q25** (Predictive): `What's the next milestone?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=2 = 3/FAIL (conf 0.90)
- **Q30** (Conversational): `What needs my attention?` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q31** (Scheduling): `Schedule a meeting about the roadmap` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=0 = 1/FAIL (conf 0.90)
- **Q33** (Scheduling): `Find time for a 1:1 with the team lead` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=1 T=0 = 2/FAIL (conf 0.90)
- **Q40** (Documents): `Update the project roadmap document` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)
- **Q42** (GitHub Ops): `Show me stale PRs` — auto-fail (2+ dimensions scored 0)
  - Judge: R=3 C=0 T=2 = 5/FAIL (conf 0.90)
- **Q58** (GitHub Ops): `Update issue #123` — auto-fail (2+ dimensions scored 0)
  - Judge: R=0 C=0 T=0 = 0/FAIL (conf 0.95)
- **Q49** (Slack): `/standup` — auto-fail (2+ dimensions scored 0)
  - Judge: R=1 C=0 T=1 = 2/FAIL (conf 0.90)

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
- **Q31** (Scheduling, M2): `Schedule a meeting about the roadmap` — FAIL
- **Q32** (Scheduling, M2): `Remind me to review PRs tomorrow` — MARGINAL
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

*Generated 2026-05-09 06:45 by canonical-retest-m1.py*
