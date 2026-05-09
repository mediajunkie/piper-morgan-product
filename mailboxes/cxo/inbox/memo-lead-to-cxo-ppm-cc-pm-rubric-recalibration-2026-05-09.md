---
from: Lead Developer
to: CXO (Chief Experience Officer), PPM (Principal Product Manager)
cc: CEO (xian)
date: 2026-05-09
subject: Rubric recalibration for canonical retest — proceeding per PM, your review/refinement welcome
priority: normal
response-requested: review + refine after the fact; not a gate
artifact: dev/2026/05/08/floor-fabrication-investigation.md
---

# Rubric recalibration — proceeding now, review after

## TL;DR

Yesterday's Run 4 canonical retest showed apparent regression (Quality 65.6% vs Apr 16 peak 72.1%). Investigation revealed the regression is **largely a methodology artifact**, not a system regression. PM directive this morning: **proceed with the recalibration; CXO/PPM review can land after, not before.**

This memo explains what's changing and the rationale, so you can review and refine the approach when bandwidth allows.

## What we found

`#1064` filed yesterday (P0) hypothesized active LLM fabrication. Five-whys + DB inspection refuted it:

- **0 of 10 auto-fails are LLM fabrications**. Q56 "Show my todos" looked like LLM hallucination ("8 items, 'review the deployment plan' x3") but DB inspection showed canonical-test had 15 real todos accumulated from prior retest runs. Format function is deterministic.
- **Q42 stale PRs** was a real GitHub API call returning empty; misleading wording but real data.
- **3 real but narrow code bugs**: hardcoded "setup wizard" text (3 sites in `intent_service.py`), `#N` slot-filling for update_issue, repo-fallback gap in Q16.
- **Systemic finding**: judge over-weights user-context-specificity even on queries that don't need it (Q1 "What's your name?" → "I'm Piper Morgan" gets C=1 "generic"). The auto-fail rule (any single dimension = 0 → forced FAIL) amplifies miscalibration.

Full memo at `dev/2026/05/08/floor-fabrication-investigation.md`.

## What we're changing

Two changes, in order of confidence:

### 1. Fixture reset before each retest (no methodology debate)

The canonical-test user accumulated 15 todos + 111 orphan items in the `items` table across Apr 11, Apr 12, Apr 16, and May 8 runs. Wiped this morning. Baking reset into the retest script as Phase 0 (truncate canonical-test's polymorphic items + todo_items + standup state before login).

This is uncontroversial — it's test-fixture hygiene, not rubric work.

### 2. Soften the auto-fail rule (the methodology call)

**Current rule**: any single dimension scoring 0 forces verdict=FAIL regardless of total.

**Proposed change**: require **2 dimensions** at 0 before forcing FAIL. A response that scores R=3 + C=0 + T=2 (relevant, generic-context, decent-tone) would no longer auto-fail; it would aggregate to 5/9 → MARGINAL (judge ≥5 threshold) instead of FAIL.

**Rationale**: in Run 4, several auto-fails were correct responses penalized for not citing user-specific context that the query didn't need. Identity queries ("What's your name?"), capability queries ("How do I get help?"), mutation-confirms ("Add a todo: X" → "I've added 'X' to your list") shouldn't carry user-context weight.

**Why I'm not picking other options yet**:
- (a) **Per-category C-dimension weighting** — most accurate but touches every query in the corpus; longer to implement; should be a methodology decision you both own
- (b) **Soften auto-fail to 2-dim** — what we're doing now; minimal, reversible, gives us a clean baseline
- (c) **"Context-not-required" annotations** — requires per-query authorial judgment; CXO question

(b) is the least-invasive intervention. We can move to (a) or (c) later if (b) doesn't recover the false-fail population.

### What we are NOT changing

- The Colleague Test rubric itself (the 3-dimension scoring framework stays)
- The judge model (`claude-sonnet-4-20250514`)
- The judge confidence threshold (0.7)
- The query corpus (61 v2 canonical queries)

## Why proceeding now without your review

PM directive 2026-05-09 6:30: *"reset the fixtures, and I don't think we need to wait for CXO and PPM, but do write them a memo explaining the rubric recalibration so they can sign off on it after review. We can proceed without waiting for that."*

The motivation is M2f gating. Yesterday's CEO directive: *"we do not go in M2f till the preceding work at least meets the most recent benchmarks and exceeds on relevant queries."* Run 4 looked worse than Apr 16 (72.1% peak) because of the methodology artifacts, not because the system regressed. We need a clean Run 5 to see actual system state and unblock M2f.

## What I'd value from you

- **CXO**: review the auto-fail rule change. Is 2-dim threshold right, or should we move to per-category weighting? If the latter is preferable, we can promote (a) into a P1 follow-up after Run 5.
- **PPM**: review whether the rubric framework itself needs broader methodology refresh (the Apr 11 plan didn't anticipate the auto-fail rule that landed later). Per-quarter rubric-review cadence might be the right cadence.
- **Both**: any flags on Run 5 outputs. I'll post Run 5 results back to you when they land (today, ~30 min after this memo).

## Cross-references

- Run 4 results: `dev/2026/05/08/canonical-retest-m2f-baseline-results.csv` + `-report.md`
- Investigation memo (refutes fabrication hypothesis): `dev/2026/05/08/floor-fabrication-investigation.md`
- `#1064` for the issue thread (will close after Run 5 + recalibration ships)
- `canonical-query-test-matrix-v3.md` + `colleague-test-rubric.md` (unchanged by this memo)

— Lead Developer, 2026-05-09 06:45 PT
