# Session log — Coding Agent (prog), model Sonnet, dispatched by Lead

**Date**: 2026-10-03
**Task**: #1595 Phase 3 — deletions THIRTEEN through EIGHTEEN in the pre-classifier deletion
ratchet, six lists, done sequentially: CONTEXTUAL_QUERY_PATTERNS (FULL), SESSION_ACTIVITY_QUERY_PATTERNS
(FULL), INSIGHT_PULL_PATTERNS (FULL), GET_DEFAULT_REPO_PATTERNS (FULL), PRODUCTIVITY_QUERY_PATTERNS
(FULL), LOCAL_GIT_STATUS_PATTERNS (PARTIAL — 11 of 12). Worked in
`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`. No commits made
(hard rule: Lead reviews and commits).

## Summary

Ceiling `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]`: **201 → 155** (46 literals
deleted across the six lists: 13 + 6 + 7 + 5 + 4 + 11). AFTER `--all` gate confirms all five FULL
lists at `0 literals / 0 rows / NO ROWS`, LOCAL_GIT_STATUS_PATTERNS at `1 literal / 1 row / NO-GO`
(the one survivor, as designed for a partial). `scripts/pattern_literal_counts.py` confirms
`TOTAL: 155`.

## Per-list account

### 13. CONTEXTUAL_QUERY_PATTERNS — FULL (13 literals; 201 → 188)
BEFORE: GO (deletable), 13/13 MATCH. 0 unexercised, 0 shadowed, 0 reabsorptions post-deletion.
Ledger entry appended. 6 pins converted in `test_contextual_query_handlers.py` (never deleted;
added `TestContextualQueryInversionRoutesSurvive`). Targeted suite: 283 passed.

### 14. SESSION_ACTIVITY_QUERY_PATTERNS — FULL (6 literals; 188 → 182)
BEFORE: GO (deletable), 6/6 MATCH/agreeing-REVIEW. 0 unexercised, 0 reabsorptions. Widest fallout
of the smaller lists: `session_activity_query` had been the recurring "second real surface-1
claim" half of a two-pattern multi-intent fixture in `test_inversion_multi_intent_unit4_1595.py`
and the flip-1 "legacy chain" denominator in `test_inversion_live_1595.py`. Both swapped to a NEW
pairing (`local_git_status_query` + `get_memory`, via LOCAL_GIT_STATUS_PATTERNS' `behind` literal
+ MEMORY_PATTERNS' `discussed` literal) chosen deliberately to survive the EIGHTEENTH deletion too
— this paid off exactly as planned. One real risk found by running, not assumed: `get_memory`'s
read_floor rail entry reaches a live LLM call (`UnboundLLMKeyError` in this harness) — mocked
`_handle_floor_with_context` for the one test that needed a "real dispatch" proof. 1 pin converted
in `test_session_activity_recall_1394.py`. Targeted suite: 215 passed.

### 15. INSIGHT_PULL_PATTERNS — FULL (7 literals; 182 → 175)
BEFORE: GO (deletable), 8/8 MATCH/agreeing-REVIEW (`pull_insights`, FLOOR-disposition, live ONLY
because READ_FLOOR itself joined `CURRENT_LIVE_CATEGORIES` same-day). 0 unexercised.
**⚠️ ONE disagreeing reabsorption found**: "what insights do you have about my productivity" ->
PRODUCTIVITY_QUERY_PATTERNS/productivity_query. Assessed as TEMPORARY and self-resolving (not a
STOP) because PRODUCTIVITY_QUERY_PATTERNS is itself deleted two lists later in this exact batch,
and the row's own frozen router evidence (MATCH pull_insights@0.95, live) independently proves it
safe regardless — same shape as the fourth deletion's (TEMPORAL/CALENDAR) precedent for
disagreeing-but-scheduled-to-resolve reabsorptions. Documented in `known_reabsorptions`, flagged
here for Lead's confirmation. 1 pin converted in `test_pre_classifier.py`. Targeted suite: 339
passed.

### 16. GET_DEFAULT_REPO_PATTERNS — FULL (5 literals; 175 → 170)
BEFORE: GO (deletable), 5/5 MATCH/agreeing-REVIEW. 1 literal unexercised and PROVABLY SHADOWED by
its own earlier sibling (the task's known shadowing) — both deleted together, no deposit needed. 0
reabsorptions. 2 pins converted in `test_get_default_repo_1327.py`, including noting
`ACTION_EXAMPLES`' now-stale example as a pre-existing registry shape (shipped_query/
close_issue_query already carry it since the fifth deletion). Targeted suite: 314 passed.

### 17. PRODUCTIVITY_QUERY_PATTERNS — FULL (4 literals; 170 → 166)
BEFORE: GO (deletable), 5/5 MATCH/agreeing-REVIEW/mis-serve. The mis-served row is the EXACT phrase
flagged in #15 — deleting this list **resolves** that reabsorption (confirmed empirically: both
entry surfaces now None/None). Updated #15's ledger entry with `resolved_by` in the same session.
2 pins converted in `test_productivity_query_handlers.py`. Targeted suite: 114 passed; re-ran
`test_pre_classifier.py` + `test_get_default_repo_1327.py` (61 passed) to confirm no disturbance.

### 18. LOCAL_GIT_STATUS_PATTERNS — PARTIAL (11 of 12; 166 → 155)
BEFORE: GO (partial), 11 `[OK]` + 1 `[FAIL]` (survivor: "are we behind upstream at all",
router=analyze_blockers@0.72 < threshold). 0 unexercised, 0 reabsorptions. **Widest pin fallout of
the whole batch** — "what branch are we on" had been this epic's go-to stand-in example for "a
still-claiming LOCAL_GIT_STATUS_PATTERNS phrase" across many unrelated files. Swapped everywhere to
"are we behind upstream at all". Biggest single fix: `test_read_lane_destructive_greed_1756.py`'s
`STATUS_READS` secretly carried 7 LOCAL_GIT_STATUS phrases alongside its real STATUS ones — split
out into `LOCAL_GIT_STATUS_READS_NOW_UNCLAIMED` with a new
`TestLocalGitStatusReadsNowDeclineAtSurfaceOne` class. `test_inversion_multi_intent_unit4_1595.py`
and `test_inversion_live_1595.py` needed NO further changes — already pre-emptively fixed during
#14's own work, confirmed by re-running. Targeted suite: 621 passed (largest single-list run in
the batch).

## AFTER `--all` gate (quoted)

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'DELETE_TODO', 'READ_FLOOR',
'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 496 rows total = 67 claimed + 429 unclaimed

list                                     literals   rows      verdict
----------------------------------------------------------------------
CONTEXTUAL_QUERY_PATTERNS                       0      0      NO ROWS
GET_DEFAULT_REPO_PATTERNS                       0      0      NO ROWS
INSIGHT_PULL_PATTERNS                           0      0      NO ROWS
LOCAL_GIT_STATUS_PATTERNS                       1      1        NO-GO
PRODUCTIVITY_QUERY_PATTERNS                     0      0      NO ROWS
SESSION_ACTIVITY_QUERY_PATTERNS                 0      0      NO ROWS
(other lists unchanged by this batch, omitted here — see full --all output)
```

## Final ceiling

`pattern_literal_counts.py` → `TOTAL: 155 (35 lists)`. `TestExtractionPatternRatchet.CEILINGS["pre-classifier"]`
updated to `155` with full dated-comment trail in `tests/test_architecture_enforcement.py`.

## Full-suite verification (run after all six)

Full unit tree (pytest.ini's -x/--maxfail overridden):
```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q \
  -p no:cacheprovider -m "not llm" \
  -o addopts="--ignore=tests/archive --ignore=*/archive/* --ignore=services/integrations/*/tests \
  --ignore=services/mcp/server/test_*.py --ignore=dev/ --tb=short --import-mode=importlib"
```
Result: **12235 passed, 228 skipped, 3 deselected, 1 xfailed, 0 failed** (260.40s). Baseline was 0
failed; this run is 0 failed — clean.

`tests/intent/`:
```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -p no:cacheprovider -m "not llm" \
  -o addopts="--import-mode=importlib --tb=line"
```
Result: **205 passed, 2 skipped, 93 deselected, 0 failed** (30.49s). Baseline was 0 failed; clean.

`ruff check` + `ruff format --check` on every changed `.py` file (18 files): all clean, no
reformatting needed after the one `tests/unit/test_inversion_phase3_deletion_1595.py` reformat
(applied, re-verified).

`git diff --numstat` on `scripts/inversion_phase3_deleted_patterns.json`: **246 insertions, 0
deletions** — pure insertion maintained across all six ledger entries plus the one `resolved_by`
addition to entry #15.

## Files changed

- `services/intent_service/pre_classifier.py` — six pattern-list edits (tombstones/partial)
- `scripts/inversion_phase3_deleted_patterns.json` — six new ledger entries + one `resolved_by` update
- `tests/test_architecture_enforcement.py` — ceiling trail, 201 → 155
- `tests/unit/test_inversion_phase3_deletion_1595.py` — ledger-count pin renamed/extended to nineteen entries
- `docs/internal/architecture/current/intent-routing-stack.md` — six new dated sections
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — six dated entries + batch summary
- 16 test files with converted pins (listed per-list above); full list in `git status --short`

## Flagged for Lead's review

1. **#15's temporary disagreeing reabsorption** (INSIGHT_PULL_PATTERNS → PRODUCTIVITY_QUERY_PATTERNS,
   resolved by #17 in this same session) — handled per established project precedent
   (TEMPORAL/CALENDAR), not treated as a STOP, since it self-resolved within this exact dispatch.
   Please confirm this judgment call was the right one.
2. No other STOPs hit. All six lists landed as specified in the dispatch.

## Verified how

Every claim above is from a command actually run this session (gate script invocations, direct
`claim_for_phrase`/`pre_classify` probes, `pattern_literal_counts.py`, `git diff --numstat`, `ruff`,
and the two pytest suites quoted verbatim). Layer: deterministic/unit; zero LLM calls anywhere in
this unit (confirmed — the one place an LLM call would have fired, `get_memory`'s read_floor path
in a real-dispatch test, was caught by running it and mocked out, not assumed safe).
