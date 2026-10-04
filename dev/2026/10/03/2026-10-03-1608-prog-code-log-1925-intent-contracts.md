# Session log — prog (Coding Agent), 2026-10-03

**Model**: Sonnet (assigned by Lead)
**Dispatched by**: Lead Developer
**Task**: GitHub issue #1925 — 18 tests (17 under `tests/intent/`, 1 under `tests/e2e/`) failing on main since the #1595 Phase 3 pattern-list deletions.
**Scope**: test-only. No product code under `services/`/`web/` touched. No real LLM calls made. No commits (Lead reviews/commits).

## Summary

Repro'd 17 failures in `tests/intent/ -m "not llm"` (issue's 18th listed failure,
`tests/e2e/test_original_message_1460_e2e.py::test_multi_intent_schedule_turn_reaches_agenda_aggregation`,
is outside `tests/intent/` and outside the issue's own AC — see "Scope note" below; left untouched).

Root cause confirmed: `TEMPORAL_PATTERNS` and `PRIORITY_PATTERNS` in
`services/intent_service/pre_classifier.py` are now `[]` (fully deleted by #1595 Phase 3) — no
surface-1 literal can claim either category anymore, so any example phrase for them is Stage-2
(LLM)-only. `STATUS_PATTERNS` and `GUIDANCE_PATTERNS` still have survivors, but the shared example
phrases in `tests/intent/test_constants.py::CATEGORY_EXAMPLES` no longer matched any of them.

Fix pattern, per category of failure:
1. **STATUS / GUIDANCE** (6 tests): swapped the example phrase in the shared `CATEGORY_EXAMPLES`
   dict to one a current surviving literal claims deterministically. Verified via
   `PreClassifier.pre_classify_with_pattern_list()` before committing to the phrase. One shared
   edit fixes all 6 call sites across 3 files.
2. **TEMPORAL / PRIORITY, plain accuracy/bypass tests** (4 tests): property tested IS classification
   accuracy itself, and there's no deterministic survivor — marked `@pytest.mark.llm` with a comment
   naming the #1595 deletion, per the issue's own guidance.
3. **TEMPORAL / PRIORITY, authenticated leak-isolation tests** (6 tests, across accuracy/bypass/
   multiuser/performance/no_timeouts): property is turn-isolation across authenticated users, NOT
   classification accuracy. `process_intent`'s outer turn-recording seam
   (`get_or_create_context` + `conv_ctx.add_turn`, `services/intent/intent_service.py` ~L765-819)
   runs and mutates the per-user context *before* the classifier is reached and raises — confirmed by
   reading the code. So tolerating the now-expected classification failure (same idiom
   `test_multiuser_contracts.py` already used for its other 7 LLM-only categories, extended to cover
   TEMPORAL/PRIORITY too) still lets the leak-isolation assertions run meaningfully. No mocking
   needed; reused the suite's own existing precedent instead of introducing a new seam.
4. **test_no_timeouts.py** (2 tests): same idea, but this file's local `IntentService()` fixture
   never initializes `ServiceContainer`, so the failure signature is "Container not initialized"
   rather than the #1831 stub's "No LLM providers configured" — tolerated both.

## Before / after

**Before** (repro of the task's step 1 command):
```
17 failed, 192 passed, 2 skipped, 89 deselected, 54 warnings in 33.75s
```
(17, not 18 — the 18th listed failure is `tests/e2e/test_original_message_1460_e2e.py::...`, outside
`tests/intent/`; see Scope note.)

**After**:
```
205 passed, 2 skipped, 93 deselected, 52 warnings in 28.62s
```
0 failed. Deselected grew 89→93 (the 4 tests newly marked `@pytest.mark.llm`: `test_temporal_accuracy`,
`test_priority_accuracy`, `test_temporal_no_bypass`, `test_priority_no_bypass`). 192→205 passed = 13 of
the 17 now pass deterministically; the other 4 moved to the llm-deselected bucket. 13 + 4 = 17. ✓

`tests/unit/services/test_pre_classifier.py`: 36 passed (unchanged, confirming no drift from this
session's edits — I made none to that file or to `pre_classifier.py`).

## Per-test table (all 17, within AC scope)

| Test | Property | Fix | Justification (1 line) |
|---|---|---|---|
| `test_accuracy_contracts.py::test_temporal_accuracy` | classification accuracy | llm-mark | No TEMPORAL survivor exists; property IS accuracy, so only the live tier can prove it. |
| `test_accuracy_contracts.py::test_priority_accuracy` | classification accuracy | llm-mark | Same — no PRIORITY survivor. |
| `test_accuracy_contracts.py::test_status_accuracy` | classification accuracy | swap (CATEGORY_EXAMPLES) | STATUS still has a survivor (`\bcurrent work\b`); new phrase matches it. |
| `test_accuracy_contracts.py::test_guidance_accuracy` | classification accuracy | swap (CATEGORY_EXAMPLES) | GUIDANCE still has a survivor (`\bset up.*projects?\b`); new phrase matches it. |
| `test_accuracy_contracts.py::TestAccuracyContractsAuthenticated::test_temporal_accuracy_does_not_leak_turns_across_authenticated_users` | leak isolation (not accuracy) | tolerate expected failure, keep leak asserts | Turn-recording seam runs before the classifier raises; property doesn't depend on classification succeeding. |
| `test_bypass_contracts.py::test_temporal_no_bypass` | classification occurred (no bypass) | llm-mark | Assertion requires a real non-placeholder result; only the live tier produces one now. |
| `test_bypass_contracts.py::test_priority_no_bypass` | classification occurred (no bypass) | llm-mark | Same reasoning. |
| `test_bypass_contracts.py::test_status_no_bypass` | classification occurred (no bypass) | swap (CATEGORY_EXAMPLES) | Shared STATUS swap above. |
| `test_bypass_contracts.py::test_guidance_no_bypass` | classification occurred (no bypass) | swap (CATEGORY_EXAMPLES) | Shared GUIDANCE swap above. |
| `test_bypass_contracts.py::TestBypassContractsAuthenticated::test_temporal_no_bypass_does_not_leak_turns_across_authenticated_users` | leak isolation (not bypass) | tolerate expected failure, keep leak asserts | Same turn-recording-seam argument as the accuracy sibling. |
| `test_multiuser_contracts.py::TestMultiUserContractsAuthenticated::test_temporal_multiuser_authenticated` | leak isolation | moved TEMPORAL out of `_PRE_CLASSIFIED_DETERMINISTICALLY` | File already has a built-in Stage-2-tolerant path for LLM-only categories; TEMPORAL now belongs there. |
| `test_multiuser_contracts.py::TestMultiUserContractsAuthenticated::test_priority_multiuser_authenticated` | leak isolation | moved PRIORITY out of `_PRE_CLASSIFIED_DETERMINISTICALLY` | Same mechanism. |
| `test_multiuser_contracts.py::TestMultiUserContractsAuthenticated::test_status_multiuser_authenticated` | leak isolation | swap (CATEGORY_EXAMPLES) | STATUS stays in the deterministic set; new phrase resolves it there. |
| `test_multiuser_contracts.py::TestMultiUserContractsAuthenticated::test_guidance_multiuser_authenticated` | leak isolation | swap (CATEGORY_EXAMPLES) | GUIDANCE stays in the deterministic set; new phrase resolves it there. |
| `test_performance_contracts.py::TestPerformanceContractsAuthenticated::test_temporal_performance_does_not_leak_turns_across_authenticated_users` | performance bound + leak isolation | tolerate expected failure; kept performance assert (measures the fast failure, not a hang); dropped success assert | Perf threshold still meaningful ("didn't hang"); success isn't required for either named property. |
| `test_no_timeouts.py::TestNoTimeoutErrors::test_no_workflow_timeout_errors` | absence of 'No workflow type found'/timeout errors | tolerate the specific classification-layer failure strings, keep catching anything else | The now-raised error is a different layer (classification config), not the workflow/timeout regression this test guards (m-43). |
| `test_no_timeouts.py::TestNoTimeoutErrorsAuthenticated::test_query_fallback_does_not_leak_turns_across_authenticated_users` | leak isolation | tolerate expected failure (local fixture's own "Container not initialized" + the #1831 stub string), keep leak asserts | Same turn-recording-seam argument; this file's fixture has a second, distinct failure signature. |

## Scope note: the 18th failing test (not fixed, by design)

`tests/e2e/test_original_message_1460_e2e.py::test_multi_intent_schedule_turn_reaches_agenda_aggregation`
is listed in #1925's "Failing tests" but lives outside `tests/intent/`, and #1925's AC is explicit:
"0 failures in `tests/intent/ -m 'not llm'`" — this file isn't under that path. Investigated anyway to
be safe: its failure mode is different in kind — it drives the real ASGI app and makes a **real**
provider call that gets a 401 (`API key is invalid`), not the `tests/intent/conftest.py` #1831 stub.
Under this task's hard rule ("make NO real LLM calls," "do not change product code"), there is no
test-only fix available here: the message no longer resolves at Stage 1 (`TEMPORAL_PATTERNS` is `[]`),
and reaching a correct `provide_agenda` outcome depends on the real classifier/orchestrator routing,
which is product-code territory. Flagging as a discovered gap for Lead/PM — did not create a
tracking issue myself since #1925 already names it; worth deciding whether it needs its own issue
once #1925 closes on the `tests/intent/` AC.

## Files changed (test-only)

- `tests/intent/test_constants.py` — STATUS/GUIDANCE example-phrase swap + comment explaining why
  TEMPORAL/PRIORITY are untouched.
- `tests/intent/contracts/test_accuracy_contracts.py` — llm-mark ×2, leak-test tolerance ×1.
- `tests/intent/contracts/test_bypass_contracts.py` — llm-mark ×2, leak-test tolerance ×1.
- `tests/intent/contracts/test_multiuser_contracts.py` — `_PRE_CLASSIFIED_DETERMINISTICALLY` set
  updated (removed TEMPORAL, PRIORITY; comment updated).
- `tests/intent/contracts/test_performance_contracts.py` — leak-test tolerance ×1 (kept perf assert).
- `tests/intent/test_no_timeouts.py` — tolerance for both tests' classification-layer failure modes.

## Verification

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -p no:cacheprovider -m "not llm" \
  -o addopts="--import-mode=importlib --tb=line"
# 205 passed, 2 skipped, 93 deselected, 52 warnings in 28.62s

venv/bin/python -m pytest tests/unit/services/test_pre_classifier.py -q -p no:cacheprovider
# 36 passed in 0.57s

venv/bin/ruff check <6 changed files>      # All checks passed!
venv/bin/ruff format --check <6 changed files>  # 6 files already formatted
```

## git status note

`git status --short` shows 4 files modified that I did NOT touch (pre-existing in this shared
worktree before my session started, unrelated inversion-epic-0-corpus work — confirmed by diff
content, not by assumption):
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`
- `scripts/build_inversion_corpus_phase0.py`
- `tests/fixtures/inversion_corpus_phase0.yaml`
- `tests/unit/test_inversion_phase3_deletion_1595.py`

Lead should verify these are expected (likely own concurrent work in this shared worktree) before
staging/committing my 6 files — do not let them get swept into the same commit without review.

## No STOP triggered. No new discovered-work issue filed (the one gap found — the e2e test — is
already named inside #1925 itself; recommending Lead decide whether it needs a split-off issue).
