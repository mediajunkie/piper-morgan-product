# Canonical Query Retest Report — Post-M1 (v3)

**Date**: 2026-10-30 07:04
**Version**: v0.8.6 (post-M1, M1 closed Apr 11)
**User**: web-seed-1386 (fresh account)
**Total Queries**: 61
**Transport**: one fresh UUID session per query (request context built, as in a browser chat; PA 10-22, PPM yes 12:50). Runs before this change had no context.
**Methodology**: canonical-query-test-matrix-v3.md (dual scoring + LLM-as-judge)

---

## Routing Verdict (M0-comparable dimension)

| Metric | Count | Percentage |
|--------|-------|------------|
| Routing PASS | 55 | 90.2% |
| Routing FAIL | 6 | 9.8% |

**M0 baseline (Mar 12)**: 70.5% routing pass (43/61)
**M1 routing**: 90.2% (55/61)
**Routing by the rail entry's effect** (PPM 10-20, the headline): 55/61. **By the classifier's category** (the pre-10-20 reading, for comparison): 54/61 (88.5%).

---

## Quality Verdict (Colleague Test, new in v3)

| Verdict | Count | Percentage |
|---------|-------|------------|
| PASS (judge ≥7) | 39 | 63.9% |
| MARGINAL (judge 5-6) | 20 | 32.8% |
| FAIL (judge <5 or auto-fail) | 2 | 3.3% |
| Skipped (NOT_IMPL or ERROR) | 0 | 0.0% |

**Quality pass rate (judged queries)**: 39/61 (63.9%)

---

## Quality Pass Rate — Expected-Pass vs Known-Pathological (#994)

Per PPM 2026-04-16: aggregate quality conflates "things that should work" with
"things we know can't work yet." The split below makes the per-category thresholds
(≥80% conversational, ≥90% action handlers) meaningful — those targets apply to
the expected-pass set, not the full corpus.

| Bucket | Queries | Judged | PASS | Pass Rate |
|--------|---------|--------|------|-----------|
| **Expected-pass** | 42 | 42 | 23 | **54.8%** |
| Known-pathological | 19 | 19 | 16 | 84.2% |

*The expected-pass quality rate is the headline number for progress tracking.*
*Known-pathological pass rate over time tracks progress on the hard problems.*

---

## AAXT Failure-Mode Distribution (#993)

Six-mode diagnostic taxonomy aligned with Klatch's AAXT harness so
cross-project results are directly comparable. The R/C/T rubric tells
you PASS/FAIL; the failure mode tells you *why*.

| Mode | Count | % of Total |
|------|-------|------------|
| Correct | 31 | 50.8% |
| Reconstructed | 7 | 11.5% |
| Confabulated | 0 | 0.0% |
| Absent | 23 | 37.7% |
| Phantom | 0 | 0.0% |
| Subliminal | 0 | 0.0% |

- **Correct** = accurate and well-formed
- **Reconstructed** = accurate but inferred rather than directly known
- **Confabulated** = hedged invention with uncertainty markers
- **Absent** = honest absence acknowledgement (PASS-shaped on missing data)
- **Phantom** = confident invention (Pattern-045 fail case)
- **Subliminal** = uses knowledge it can't attribute

Phantom counts > 0 should trigger fabrication-probe (#995) re-run.

---

## Results by Category

| Category | Total | Pathological | Routing PASS | Quality PASS | MARGINAL | FAIL |
|----------|-------|--------------|-------------|--------------|----------|------|
| Identity | 5 | 0 | 5/5 | 5 | 0 | 0 |
| Temporal | 5 | 0 | 5/5 | 3 | 2 | 0 |
| Spatial | 4 | 0 | 4/4 | 2 | 2 | 0 |
| Capability | 5 | 0 | 4/5 | 3 | 2 | 0 |
| Predictive | 5 | 4 | 5/5 | 4 | 1 | 0 |
| Conversational | 5 | 0 | 5/5 | 4 | 1 | 0 |
| Scheduling | 5 | 3 | 4/5 | 3 | 1 | 1 |
| Documents | 4 | 4 | 2/4 | 3 | 1 | 0 |
| GitHub Ops | 8 | 4 | 6/8 | 4 | 4 | 0 |
| Slack | 5 | 3 | 5/5 | 4 | 0 | 1 |
| Productivity | 3 | 0 | 3/3 | 2 | 1 | 0 |
| Todos | 4 | 0 | 4/4 | 0 | 4 | 0 |
| Calendar Ext | 2 | 0 | 2/2 | 1 | 1 | 0 |
| Knowledge | 1 | 1 | 1/1 | 1 | 0 | 0 |

---

## Human Escalation Queue (13 items)

These results need human review. Triggers: low judge confidence, auto-fail (dimension=0), or judge error.

- **Q1** (Identity): `What's your name?` — low confidence (0.60)
  - Judge: R=3 C=2 T=2 = 7/PASS (conf 0.60)
- **Q5** (Identity): `What makes you different?` — low confidence (0.65)
  - Judge: R=3 C=2 T=2 = 7/PASS (conf 0.65)
- **Q8** (Temporal): `What's on the agenda for today?` — low confidence (0.60)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.60)
- **Q11** (Spatial): `What projects are we working on?` — low confidence (0.60)
  - Judge: R=3 C=2 T=1 = 6/MARGINAL (conf 0.60)
- **Q12** (Spatial): `Show me the project landscape` — low confidence (0.60)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.60)
- **Q21** (Predictive): `What should I focus on today?` — low confidence (0.60)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.60)
- **Q28** (Conversational): `How do I use the calendar feature?` — low confidence (0.60)
  - Judge: R=3 C=2 T=3 = 8/PASS (conf 0.60)
- **Q41** (GitHub Ops): `What did we ship this week?` — low confidence (0.65)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.65)
- **Q44** (GitHub Ops): `Create issues from this meeting's action items` — low confidence (0.60)
  - Judge: R=2 C=1 T=2 = 5/MARGINAL (conf 0.60)
- **Q51** (Productivity): `What's my productivity this week?` — low confidence (0.65)
  - Judge: R=3 C=2 T=1 = 6/MARGINAL (conf 0.65)
- **Q54** (Todos): `Add a todo: review the deployment plan` — low confidence (0.60)
  - Judge: R=3 C=1 T=2 = 6/MARGINAL (conf 0.60)
- **Q55** (Todos): `Complete the PR review todo` — low confidence (0.60)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.60)
- **Q61** (Calendar Ext): `What's my week look like?` — low confidence (0.60)
  - Judge: R=2 C=2 T=1 = 5/MARGINAL (conf 0.60)

---

## Known Issues Run Anyway (15 items)

Per PM guidance: known failures are still run honestly. Tag indicates tracking.

- **Q22** (Predictive, M2 Beta): `What patterns do you see?` — PASS
- **Q23** (Predictive, M2 Beta): `What risks should I be aware of?` — PASS
- **Q24** (Predictive, M2 Beta): `What opportunities should I pursue?` — PASS
- **Q25** (Predictive, M2 Beta): `What's the next milestone?` — PASS
- **Q31** (Scheduling, M2): `Schedule a meeting about the roadmap` — PASS
- **Q32** (Scheduling, M2): `Remind me to review PRs tomorrow` — PASS
- **Q33** (Scheduling, M2): `Find time for a 1:1 with the team lead` — PASS
- **Q36** (Documents, M2): `Create a doc from this conversation` — PASS
- **Q37** (Documents, M2): `Compare these two documents` — PASS
- **Q38** (Documents, M2): `Synthesize these sources into a summary` — PASS
- **Q40** (Documents, M2): `Update the project roadmap document` — MARGINAL
- **Q46** (Slack, M2): `Any mentions I missed?` — PASS
- **Q47** (Slack, M2): `Summarize #general from yesterday` — PASS
- **Q48** (Slack, M2): `Post this update to the team channel` — PASS
- **Q63** (Knowledge, M2): `Upload a file to the knowledge base` — PASS

---

## Known-Pathological Queries (19 items, #994)

These queries are tagged as known-pathological — we expect them to fail
under current conditions (M2 features not shipped, fresh-account lacks real data,
etc.). They run anyway for tracking progress on the hard problems over time.

- **Q22** (Predictive, _M2-beta-pending_): `What patterns do you see?` — PASS
- **Q23** (Predictive, _M2-beta-pending_): `What risks should I be aware of?` — PASS
- **Q24** (Predictive, _M2-beta-pending_): `What opportunities should I pursue?` — PASS
- **Q25** (Predictive, _M2-beta-pending_): `What's the next milestone?` — PASS
- **Q31** (Scheduling, _fresh-account-no-data_): `Schedule a meeting about the roadmap` — PASS
- **Q32** (Scheduling, _M2-feature-pending_): `Remind me to review PRs tomorrow` — PASS
- **Q33** (Scheduling, _fresh-account-no-data_): `Find time for a 1:1 with the team lead` — PASS
- **Q36** (Documents, _M2-feature-pending_): `Create a doc from this conversation` — PASS
- **Q37** (Documents, _M2-feature-pending_): `Compare these two documents` — PASS
- **Q38** (Documents, _M2-feature-pending_): `Synthesize these sources into a summary` — PASS
- **Q40** (Documents, _M2-feature-pending_): `Update the project roadmap document` — MARGINAL
- **Q41** (GitHub Ops, _fresh-account-no-data_): `What did we ship this week?` — MARGINAL
- **Q42** (GitHub Ops, _fresh-account-no-data_): `Show me stale PRs` — PASS
- **Q58** (GitHub Ops, _fresh-account-no-data_): `Update issue #123` — PASS
- **Q60** (GitHub Ops, _fresh-account-no-data_): `Review issue #789` — MARGINAL
- **Q46** (Slack, _M2-feature-pending_): `Any mentions I missed?` — PASS
- **Q47** (Slack, _M2-feature-pending_): `Summarize #general from yesterday` — PASS
- **Q48** (Slack, _M2-feature-pending_): `Post this update to the team channel` — PASS
- **Q63** (Knowledge, _M2-feature-pending_): `Upload a file to the knowledge base` — PASS

---

## Methodology Notes

- **Routing verdict**: Compares actual route taken (floor / canonical / action) to v3 expected route. M0 baseline used a different methodology (literal category matching) so this is a reframed but loosely comparable number.
- **Quality verdict**: LLM-as-judge using Colleague Test rubric. Judge model: claude-sonnet-5-5, default sampling, with calibration examples in system prompt.
- **Confidence threshold for human escalation**: < 0.7
- **Auto-fail rule**: any single dimension scoring 0 forces FAIL verdict regardless of total.
- **Known issues** are run anyway per PM guidance — honest reporting over hiding.

*Generated 2026-10-30 07:04 by canonical-retest-m1.py*