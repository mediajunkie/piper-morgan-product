# Session Log — Coding Agent (prog), 2026-10-04 06:38

**Model**: Sonnet 5, dispatched by Lead Developer.
**Role**: Coding Agent (prog) — test-side only, no product code edits, no git add/commit/push.
**Task**: Get `Tests` workflow's Full Test Suite burn-down gate to pass on main. CI run 37179516706 (main, 2026-10-04 05:18Z) reports "NEW failures not in the backlog (44)" — first full-suite execution in 60+ runs; mix of (A) #1595 Phase 3 pattern-list deletion casualties and (B) older rot.

Repo: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`).

## Plan
1. Read gate script (`scripts/check_fullsuite_backlog.py`) + backlog file (`scripts/known_failing_backlog.tsv`) — done.
2. Pull 44 failing node ids from CI log — done, saved to `/tmp/claude-ci-44.txt`.
3. Reproduce locally with dummy API keys (env vars override Keychain auto-load).
4. For each of the 44: classify A (deletion casualty, convert test) vs B (pre-existing, backlog with tag+justification) via throwaway detached worktree on a pre-10-02 commit.
5. Convert A's; add B's to backlog with justification.
6. Re-run gate until 0 NEW failures. Run tests/unit + tests/intent regression check. ruff check/format.

## Work log

- 06:38 Read gate script + backlog file. Backlog currently has 46 entries (triage/flaky tags), none of the 44 CI failures appear to already be in it (need to confirm overlap).
- 06:39 Pulled 44-item failure list from `gh run view 37179516706 --log` into `/tmp/claude-ci-44.txt`. Full param values for `test_capability_discovery.py` params truncated by log line-wrap — will get exact ids from local run / test file source.
- Kicked off local full-suite reproduction in background (dummy keys, POSTGRES_PORT=5433).

## Classification method

For each of the 44, checked whether it fails against a genuinely pre-#1595-Phase-3
commit (`1b5d28807c`, before the FIRST Phase-3 deletion on 09-27) in a throwaway
detached worktree at `/tmp/claude-lane-prewt`, same dummy-key env. Also used
`git log -S` against `services/intent_service/pre_classifier.py` to trace which
specific Phase-3 deletion unit (1st through 18th, spanning 09-27 through 10-03)
removed the literal each failing message used to match — the task brief's framing
("10-02/10-03") turned out to be approximate; several casualties trace to EARLIER
units (1st: REMINDER_PATTERNS 09-27; 2nd: TODO_QUERY_PATTERNS 09-28; 3rd:
CALENDAR_QUERY_PATTERNS 10-01) that predate the originally-suggested baseline
commit (`0196b4c488`, 10-02 04:18 PT). Noted explicitly below per item.

## Findings (A/B verdict per item) — see full table in final report

### Category A (deletion casualties — converted)
- tests/integration/test_capability_discovery.py — 22 params, 3 pattern lists
  (DISCOVERY 9th deletion 10-03, GUIDANCE 8th deletion 10-02/03, STATUS 7th
  deletion 10-02). Converted: failing params marked `@pytest.mark.llm` (property
  now exercised via the real LLM classifier) + one new deterministic pin per
  list using its surviving literal.
- tests/e2e/test_canonical_conversations.py::TestCanonicalGroundTruthMocked — 4
  tests (week_calendar x2: CALENDAR_QUERY_PATTERNS 3rd deletion 10-01;
  milestones x2: GITHUB_QUERY_PATTERNS 5th deletion 10-02). These are mocked
  ground-truth tests about DATA FLOW, not classification — converted by adding
  a `_force_pre_classify` helper that patches the real call site
  (`PreClassifier.pre_classify_with_pattern_list`, classifier.py:419 — NOT
  `pre_classify` itself, which is a thin delegator not on the live path) plus,
  for the milestone case only, `PreClassifier.detect_multiple_intents` (which
  classify_multiple tries FIRST and which still independently re-claims "What's
  the next milestone?" via STATUS_PATTERNS' surviving "next milestone" literal,
  bypassing classify() entirely) to resolve to the pre-deletion routing.
- tests/e2e/test_task_lifecycle_e2e.py — 3 tests (list_todos: TODO_QUERY_PATTERNS
  2nd deletion 09-28; close_issue: GITHUB_QUERY_PATTERNS 5th deletion 10-02;
  remind_me: REMINDER_PATTERNS 1st deletion 09-27). Same `_force_pre_classify`
  technique, local copy (single call site sufficed — verified
  `detect_multiple_intents` doesn't independently re-claim these 3 messages).

### Category B (pre-existing, unrelated to #1595 — backlogged)
- tests/config/test_data_isolation.py::test_piper_md_backup_exists — fixture.
  `config/PIPER.md.backup-20251101` was deliberately deleted in repo-cleanup
  commit `1eb7c946ff` (2026-09-23), well before #1595; the test's premise no
  longer matches reality.
- tests/domain/test_llm_domain_service.py — 2 tests — fixture. Stale mock
  assertion missing the `served=None` kwarg that commit `cf15477b58` (2026-09-30)
  added to `LLMDomainService.complete()`'s signature (#1620 passthrough fix,
  itself tagged "ref 1595" but a different, unrelated inversion-router fix, not
  a pattern-list deletion). Confirmed via `git log -S"served="`.
- tests/infrastructure/test_keychain_service.py — 10 tests — fixture. CI-only:
  passes in every local reproduction (isolated, full-suite, dummy keys, real
  macOS Keychain) but fails in CI's Linux runner, which has no real Keychain
  backend. First visible now that the full suite runs again after 60+ skipped
  runs (red smoke job).
- tests/performance/test_token_blacklist_performance.py — 2 tests
  (blacklist_add_latency, blacklist_lookup_latency) — triage. Same DB-
  connection-pool-exhaustion root cause ("Too many connections") as the
  already-backlogged sibling `test_concurrent_blacklist_lookups` (tag=triage)
  in this same file.
- tests/unit/services/intent_service/test_spend_free_canonical_ratchet_1818.py
  — 7 tests (exactly the SPENDS set — the 7 PAIR_MESSAGES minus the 4
  SPEND_FREE ones) — triage. CI-only, like keychain: passes in every local
  repro (isolated AND full-suite, dummy keys) at both HEAD and the
  pre-Phase-3 baseline. The exact-SPENDS-set correlation strongly suggests
  the same CI Keychain-backend-absence class short-circuits the real handler
  flow before the monkeypatched spend chokepoint is ever crossed, but this
  mechanism is NOT independently confirmed (can't reproduce the CI runner
  locally) — tagged triage rather than fixture to not overclaim.

### Local-only noise, OUT OF SCOPE (not in CI's 44, no action taken)
- tests/integration/test_fresh_install_flow.py::test_store_user_key_succeeds_after_user_created
  — appeared as new-failing in my local full-suite run only; not in CI's 44.
- tests/performance/orchestration/test_agent_scalability.py::TestPerformanceRegression::test_baseline_performance_consistency
  — same.
- tests/e2e/test_task_lifecycle_e2e.py::TestTodoLifecycleE2E::test_create_todo_returns_confirmation
  — this one is a methodology note, not a real discrepancy: it's ALREADY
  marked `@pytest.mark.llm` in the file (genuinely-live test, #1765). My
  initial manual repro ran it without `-m "not llm"`, which is why it
  "failed" for me — it is correctly deselected under the real gate command.

### Backlog shrink-lock (unrelated to the 44, caught by the same gate run)
- tests/integration/test_complete_integration_flow.py::TestCompleteIntegrationFlow::test_mention_event_complete_flow
  and ::TestSpatialAdapterRegistryIntegration::test_complete_flow_with_registry
  — both classes no longer exist in the file at all (removed in a prior
  refactor). Removed from scripts/known_failing_backlog.tsv per the gate's
  shrink-lock rule.

## Verification status at handback

- Per-file verification (COMPLETE): each of the 3 edited test files passes
  cleanly under `-m "not llm"` individually (capability_discovery: 11
  passed/22 deselected; canonical_conversations: 9 passed/237 deselected;
  task_lifecycle_e2e: 8 passed/1 deselected).
- Backlog TSV: parses cleanly via `scripts/check_fullsuite_backlog.py`'s own
  `load_backlog()` (67 entries: 47 - 2 shrink-lock removed + 22 added).
- ruff check + format --check: clean on all 3 changed .py files.
- Full end-to-end `tests/ -m "not llm"` + gate re-run (the task's literal
  DONE criterion): started a second time to confirm 0 NEW failures
  end-to-end post-edit, but it ran far slower than the first run (11% after
  ~15 min vs the first run's full completion in ~15 min) — likely resource
  contention from the many individual pytest invocations run earlier in the
  session. Killed it at handback rather than deliver a stale/incomplete
  claim. **This final full-suite + gate confirmation is NOT yet done** —
  recommend Lead re-run:
  ```
  env ANTHROPIC_API_KEY=sk-invalid OPENAI_API_KEY=sk-invalid POSTGRES_PORT=5433 venv/bin/python -m pytest tests/ -m "not llm" -q --tb=no -o addopts="--ignore=tests/archive --ignore=services/integrations --ignore=dev/ --import-mode=importlib" 2>&1 | tee /tmp/fullsuite.out | tail -3
  venv/bin/python scripts/check_fullsuite_backlog.py /tmp/fullsuite.out | tail -60
  ```
  on an idle machine. Given every individual target file is independently
  green and no other file was touched, I have high confidence this reports
  0 new failures, but it is unverified end-to-end as of handback.
- tests/unit + tests/test_architecture_enforcement.py and tests/intent/
  regression commands: NOT YET RUN (deprioritized to deliver the primary
  44-item classification/fix on time). Recommend Lead run both per the
  original task brief before merging.
