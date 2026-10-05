# Session log — list_repos not-found copy fix (prog role)

**Model**: Sonnet. Dispatched by Lead (CXO's ruling, cc Arch), 2026-10-05.
**Branch**: claude/lead-cycle (worktree: /Users/xian/Development/piper-morgan-worktrees/lead)
**Scope**: `_handle_list_repos` not-found copy fallback + casing echo, two corpus rows, pins. list_repos ONLY.

## Authority
- `mailboxes/lead/inbox/rule-cxo-to-lead-cc-arch-list-repos-not-found-keeps-the-lookup-answer-with-all-your-repos-corpus-rows-too-2026-10-05.md`
- `mailboxes/lead/sent/finding-lead-to-cxo-cc-arch-list-repos-misreads-on-github-and-of-my-as-project-names-reproduced-2026-10-05.md`

## What shipped

1. **`services/intent_service/canonical_handlers.py`** (`_handle_list_repos`, ~5810-5870):
   not-found branch now keeps the truthful lookup answer AND answers the underlying list ask —
   two copy variants (has repos / has none), verbatim per CXO §2. Declarative, no `?`.
2. Casing echo: re-runs the SAME extraction regex against the ORIGINAL (not lowercased)
   message with `re.IGNORECASE`, rather than slicing the lowercased copy's match span —
   `.lower()` can change string length for some characters. Lookup itself stays on the
   lowercased `project_name` (find_by_name is already case-insensitive, #1857). No new
   extraction pattern — same regex, run twice.
3. `is_plausible_project_name("github")` → `True`, `is_plausible_project_name("repos")` → `True`
   (verified by direct call). Confirms CXO's suspicion: the predicate does NOT reject either
   word, so it could never have been the fix — copy fallback is the only correct lever.
4. Corpus: two HAND_ROWS added to `scripts/build_inversion_corpus_phase0.py`
   ("list my repos on github", "show all of my repos"; category PORTFOLIO, expected
   `action:list_repos`). Regenerated `tests/fixtures/inversion_corpus_phase0.yaml` —
   `git diff --numstat` = 8 insertions / 0 deletions (pure append, two 4-line rows).
   Pinned count in `tests/unit/test_inversion_phase3_deletion_1595.py` updated 498 → 500.
5. Pins added in `tests/unit/services/intent_service/test_repo_management.py`
   (`TestListReposNotFoundFallback`, 5 new tests, DB mocked per existing file convention).
   All 31 pre-existing repo-management tests pass unchanged (36/36 total in the file).

## Verified how
- `venv/bin/python -c "from services.intent_service.pre_classifier import PreClassifier; ..."` —
  confirmed "list my repos on github" IS claimed by REPO_MANAGEMENT_PATTERNS'
  `(?:show|list|view|which)...repos` literal (action manage_repos at surface 1); "show all of
  my repos" is NOT claimed (`(None, None)`) — noted honestly in its corpus row's source.
- `scripts/build_inversion_corpus_phase0.py` run: "wrote ... 500 rows (54 REVIEW)";
  `git diff --numstat tests/fixtures/inversion_corpus_phase0.yaml` → `8  0  ...yaml`.
- `pytest tests/unit/services/intent_service/test_repo_management.py -q` → 36 passed
  (after fixing one of my own new test's assertions, which had assumed lowercase echo —
  the correct/fixed behavior preserves "Atlas" casing, not "atlas").
- Full target suite (`tests/unit tests/test_architecture_enforcement.py`, `-m "not llm"`,
  same ignore/opts as the dispatch brief) run #1 (pre-fix): 1 failed (my own new test's
  wrong assertion), 12492 passed, 228 skipped, 3 deselected, 1 xfailed. Fixed the assertion,
  reconfirmed the file in isolation (36/36 passed). A second full-suite confirmation run
  was in progress at hand-off time and had not reached completion; it covers no file touched
  after the fix other than the already-isolated-and-passing test file, so the full-suite
  result is inferred from run #1 plus the targeted rerun, not independently re-measured
  end to end. **Layer**: unit tests + direct interpreter calls, not a live HTTP turn.
  **Denominator**: full unit + architecture-enforcement suite minus the stated ignores,
  `-m "not llm"`.
- `ruff check` + `ruff format --check` on all 5 changed files: clean (one file needed
  `ruff format` applied — `canonical_handlers.py` — then re-checked clean).

## Files changed
- `services/intent_service/canonical_handlers.py`
- `tests/unit/services/intent_service/test_repo_management.py`
- `scripts/build_inversion_corpus_phase0.py`
- `tests/fixtures/inversion_corpus_phase0.yaml` (generated, pure append)
- `tests/unit/test_inversion_phase3_deletion_1595.py`

No git add/commit/push/stash performed per hard rules — left for Lead to review and commit.
