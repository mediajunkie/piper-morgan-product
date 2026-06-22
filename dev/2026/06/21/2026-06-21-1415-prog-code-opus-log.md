# Session Log — Coding Agent (prog) — 2026-06-21 14:15

**Role**: Coding Agent (prog-code-opus)
**Branch**: claude/interesting-beaver-7ee19c (ephemeral worktree)
**Task**: WS-1 P4 (#1199 / #1226) — retire the flat-file + in-memory GitHub-config
stores so the DB-backed `connector_configs` is the SOLE store. Pre-prod → hard-DELETE
retired code (no comment-out). Build on uncommitted changes already in `settings_integrations.py`.
**Instruction**: Do NOT commit. Leave changes uncommitted for PM review.

## Plan (5 tasks, run relevant test file green after each)
1. Fix `tests/unit/web/api/routes/test_settings_github_preferences.py` (patches deleted helpers).
2a. `repo_resolver._resolve_from_user_default` → DB-only (drop flat-file fallback).
2b. `user_preference_manager.get_default_repo` → DB-only; delete `set_default_repo`.
3. `repo_resolver.read_user_github_handle` → async, read `github_username` from DB + env fallback;
    update sole caller `feed_factory.py` + tests.
4. Delete dead machinery (`_read_user_default_repository`, `_GITHUB_PREFERENCES_FILE`, unused imports);
    grep-prove zero remaining flat-file/in-memory refs.

## Pre-work verification (DONE)
- Confirmed `settings_integrations.py` working-tree already has NEW helpers `_load_github_prefs_db`
  / `_save_github_prefs_db` and old `_load/_save_github_preferences` + `_dual_write_*` +
  `GITHUB_PREFERENCES_FILE` deleted (via `git diff` — the Read tool served stale HEAD content,
  `git diff` + grep are authoritative).
- `ConnectorConfigService.get_config` returns a COPY (`dict(row.config)`) → `merged.update()` safe.
- `ConnectorConfigRepository.get` returns None for non-UUID owner (graceful read, m-40).
- DB store key is `DEFAULT_REPO_KEY = "default_repository"`, independent of UPM's
  `DEFAULT_REPO = "default_repo"`.

## Judgment calls (logged at decision time)
- **KEEP `DEFAULT_REPO` constant** in user_preference_manager.py. Reason: it does NOT become
  unused — `tests/domain/test_user_preference_manager_active_repos_1050.py::test_distinct_from_default_repo_key`
  hard-depends on it (`assert ACTIVE_REPOS != DEFAULT_REPO`), and that test guards a still-live
  feature (`get_active_repos`/`set_active_repos`). The constant is also the persisted preference
  key the active_repos docs reference as a sibling. Deleting it would break an out-of-scope test.
  Prompt's instruction was conditional ("if it becomes unused") → keep. Therefore also KEEP
  `TestDefaultRepoConstants` in the 1042 test (it guards the same key).

## ENVIRONMENT GOTCHA (critical — cost ~20 min, now resolved)
The worktree nests under the main checkout. `cd /Users/xian/.../piper-morgan-product`
(bare path) lands in the MAIN checkout (branch `main`), NOT the worktree. The "already done"
uncommitted work lives ONLY in the worktree
(`/Users/xian/.../piper-morgan-product/.claude/worktrees/interesting-beaver-7ee19c`).
- The Read tool initially served stale HEAD content for the modified file; `git diff`+grep are
  authoritative. (Resolved once I read via the worktree path.)
- I accidentally Wrote the new test file to the MAIN checkout first (dirtied
  `main:tests/.../test_settings_github_preferences.py`) → reverted with `git -C $MAIN checkout --`.
- **Discipline for the rest of the session**: every Bash starts `cd $WT`; all Read/Edit/Write use
  the worktree absolute path; pytest runs from worktree cwd so Python imports worktree modules
  (verified: `sys.path[0]`='' → cwd wins → worktree `settings_integrations.py` w/ `_load_github_prefs_db`).
- Run cmd: `cd $WT && env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL POSTGRES_PORT=5433 \
  /Users/xian/.../piper-morgan-product/venv/bin/python -m pytest <args> -p no:cacheprovider`
  (main's venv via absolute path; nested-walk-up makes it work).

## Progress
- Task 1 DONE: `test_settings_github_preferences.py` rewritten — patches `_load_github_prefs_db`
  (AsyncMock); get tests return blob directly; save tests = (a) calls-db-helper-with-payload
  (b) surfaces-db-failure-as-500; deleted `test_returns_empty_for_different_user`,
  `TestGitHubPreferencesFileStorage`, all 5 old save tests + dual-write tests. → 7 passed.
- Task 2a DONE: `repo_resolver._resolve_from_user_default` is DB-only (dropped flat-file
  fallback); docstrings updated. Tests: `test_db_miss_falls_back_to_json`→`test_db_miss_unresolved`;
  `TestUserDefaultPreference` now drives `_read_user_default_repo_from_db`; deleted
  `TestReadUserDefaultRepository`; `TestDefaultProjectResolution._READER` → DB reader (AsyncMock).
  → 30 passed.
- Task 2b DONE: `user_preference_manager.get_default_repo` is DB-only; DELETED
  `set_default_repo`; KEPT `DEFAULT_REPO` constant (judgment call above) with updated docstring.
  Tests: deleted `TestDefaultRepoRoundTrip` + `TestDefaultRepoValidation`; reshaped
  `TestDefaultRepoFromDB` to DB-only (db_value_used + db_miss_returns_none); kept
  `TestDefaultRepoConstants`. → 46 passed (incl. active_repos 1050 which depends on DEFAULT_REPO).
- Task 3 DONE: `read_user_github_handle` → `async def`, reads `github_username` from DB github
  config via ConnectorConfigService (best-effort, env fallback). Caller `feed_factory.py:89`
  → `await`. Tests in `test_radar.py`: 2 handle tests → async + patch DB get_config; added
  `test_handle_reader_db_value_used`. → 16 passed.
- Task 4 DONE: deleted `_read_user_default_repository`, `_GITHUB_PREFERENCES_FILE` const +
  comment, and the now-unused `import json` (os stays — env vars). Fixed a stale warning string.
  Grep proof: all retired identifiers (`_load/_save_github_preferences`,
  `_dual_write_github_prefs_to_db`, `GITHUB_PREFERENCES_FILE`, `_read_user_default_repository`)
  = ZERO in services/+web/. Remaining `github_preferences` hits = API route handler names
  (`get/save_github_preferences` @ `/github/preferences`), structured-log event keys, and
  retirement-narrating docstrings (config_service, models.py ConnectorConfig, repo_resolver,
  settings_integrations) — all legitimate.
- All targeted test files together: **99 passed**. py_compile OK on all 4 edited source files.

## Verification results (all 5 required runs)
1. `test_settings_github_preferences.py` → **7 passed**.
2. `test_repo_resolver_1042.py` → **30 passed**.
3. `test_user_preference_manager_default_repo_1042.py` + `test_user_preference_manager.py`
   (+ ran `_active_repos_1050.py` for the DEFAULT_REPO guard) → **46 passed**.
4. `test_radar.py` (read_user_github_handle) + `test_workitem_source_1239.py` → **16 passed**.
5. Broad smoke `tests/unit tests/domain`:
   - First pass (maxfail=15) stopped at 15 fails. Triaged every non-deselected failure by
     re-running it on the **clean `main` baseline** (worktree nests under main; `git -C $MAIN`).
   - **Every failure fails IDENTICALLY on pristine main → 100% pre-existing, ZERO mine.**
   - Final confirming run deselecting all 19 confirmed-pre-existing failures →
     **8003 passed, 0 failed, 229 skipped** (exit 0).

### Pre-existing failure inventory (all reproduce on clean main; NOT mine)
- **Datetime cluster (the prompt's known ~9)**: 8× `tests/unit/services/standup/test_conversation_state.py`
  (`TestConversationLifecycle`/`TestStateTransitions`/`TestThreePartGatheringTransitions`/`TestCleanup`)
  — `TypeError: can't subtract offset-naive and offset-aware datetimes` at
  `datetime.now(timezone.utc) - conversation.created_at`; + the 1 prompt-deselected
  `test_adapters.py::test_check_active_active_conversation` = the 9-failure cluster.
- **Other pre-existing (10), unrelated to GitHub-config stores, all green-on-main-fail-on-main**:
  - `test_place_service.py::TestGitHubPlace::test_github_place_has_name` (place.name='GitHub' assertion)
  - `test_keychain_scoping_849.py::...test_save_github_token_uses_user_scoped_key`
  - `test_settings_projects_ui.py::TestSettingsProjectsTemplate` ×3 (template content)
  - `test_file_reference_detection.py` ×3 + `test_llm_domain_service.py` ×2
    (`ContainerNotInitializedError` — DI/test-isolation artifact, LLM container not initialized)

## Files changed (8; all uncommitted in worktree, per instruction)
- `web/api/routes/settings_integrations.py` — (pre-existing "already done" work; I verified, did
  NOT edit) handlers use `_load_github_prefs_db`/`_save_github_prefs_db`; old helpers gone.
- `services/integrations/github/repo_resolver.py` — `_resolve_from_user_default` DB-only;
  `read_user_github_handle` async+DB; deleted `_read_user_default_repository`,
  `_GITHUB_PREFERENCES_FILE`, `import json`; fixed stale warning string.
- `services/domain/user_preference_manager.py` — `get_default_repo` DB-only; deleted
  `set_default_repo`; kept `DEFAULT_REPO` const (docstring updated; judgment call).
- `services/radar/feed_factory.py` — 1 line: `await read_user_github_handle(...)`.
- 4 test files updated to match (settings, repo_resolver, default_repo_1042, radar).

## Grep proof (services/ + web/) — retired identifiers = ZERO
`_load_github_preferences`, `_save_github_preferences`, `_dual_write_github_prefs_to_db`,
`GITHUB_PREFERENCES_FILE`, `_read_user_default_repository` → ALL none. Remaining
`github_preferences` hits = API route-handler names (`get/save_github_preferences` @
`/github/preferences`), structured-log event keys, and retirement-narrating docstrings only.

## STATUS: COMPLETE. Did NOT commit (per instruction). Left for PM review.

## Memory & briefing surfaces referenced this session
- **Referenced**: CLAUDE.md "ANTHROPIC_* env strip" (test-run command), "worktree nested
  walk-up" (diagnosing the cwd/checkout confusion), "Verify First / investigate before
  extending" (read whole files + git diff before editing), "Subagent commit verification"
  (checked no stray unstaged code). Memory `feedback_write_new_files_to_worktree_path_in_model_a`
  (write to worktree path, not bare main) — directly relevant to the cwd gotcha I hit.
- **Loaded but not referenced**: most of the role/mailbox/Comms-voice memory (this is a focused
  coding task, not a cycling-role or comms session).
- **Wanted but not found**: a note that `cd <bare-main-path>` from a nested worktree session
  lands in MAIN (not the worktree) — would have saved ~20 min. (The walk-up note covers venv
  resolution but not the cwd/checkout flip.)

<!-- DAY-CLOSED: 2026-06-21 (retroactive — task agent, content-complete, no STOP fire; self-healed at Docs START) -->
