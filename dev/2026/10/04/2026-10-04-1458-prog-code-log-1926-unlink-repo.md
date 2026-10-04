# Session log — #1926 unlink_repo (DESTRUCTIVE rail entry)

**Role**: Coding Agent (prog)
**Model**: Sonnet (assigned by Lead)
**Dispatched by**: Lead
**Date**: 2026-10-04
**Repo/worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) — work only, no commit/push (Lead reviews and commits).

## Task

#1595 Phase 3 + #1926 — the UNLINK third of Arch's `manage_repos` split: a DESTRUCTIVE rail entry
`unlink_repo` that confirms first, built to CXO's five constraints. NOT flipped (no live-category or
flag change).

## Authority read in full

- CXO's ruling: `mailboxes/lead/read/ruling-cxo-to-arch-lead-1926-unlink-confirms-via-destructive-gate-link-and-list-do-not-confirm-2026-10-03.md`
- Arch's §2: `mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-wave2-and-writes-2026-10-03.md`
- `gh issue view 1926` (CXO's ruling recorded there too)

## What was built

### 1. The hoist (`services/intent_service/canonical_handlers.py`)

- `_resolve_unlink_repo_target(intent, user_id)` — hoisted the legacy UNLINK branch's repo-name +
  unlink-pattern project-name extraction regexes (no new patterns) plus project/repo DB lookups. Shared
  by execute and confirm-arm.
- `_resolve_unlink_repo_confirmation(intent, user_id)` — confirm-gate-only: delegates to the above, then
  does the ONE extra read execute-time doesn't need (`get_project_links` → link-existence +
  `is_primary`), for CXO's constraint 2.
- `_handle_unlink_repo(intent, session_id, user_id)` — the execute path: resolve, then
  `unlink_from_project` (unchanged legacy behaviour), same success/not-linked copy as before.
- `_handle_repo_management`'s UNLINK branch is now `if operation == "unlink": return await
  self._handle_unlink_repo(...)` — the dead `async with` session block it used to sit inside (only ever
  reached for "unlink", since list/link already returned) was deleted outright. Also removed the now-dead
  `ProjectRepository`/`RepositoryRepository`/`AsyncSessionFactory`/`domain` imports from
  `_handle_repo_management`'s top (unused after all three ops were hoisted).

### 2. The confirm builder (`services/intent_service/destructive_confirm.py`)

- `is_unlink_repo_action(action)` — single-member family predicate (mirrors `is_delete_todo_action`).
- `UnlinkRepoGate` dataclass (`offer` | `passthrough_result`).
- `build_unlink_repo_confirmation(intent, canonical_handlers, user_id)` — calls
  `_resolve_unlink_repo_confirmation`; on failure returns `passthrough_result` (nothing armed); on
  success builds CXO's exact copy (ask + conditional is_primary clause + never-mind exit) and arms the
  `#1190` carrier with `DESTRUCTIVE_CONFIRM_KIND`.

### 3. The rail wiring (`services/intent/intent_service.py`, `_dispatch_action_rail`)

Added `elif is_unlink_repo_action(intent.action):` beside the existing `if
is_delete_todo_action(intent.action):` branch (NOT a new `if/elif intent.action in [...]` dispatch
site — verified against `TestPreFloorDispatchSiteRatchet`'s regex, which only matches that exact shape).
A `passthrough_result` returns the honest copy directly; an `offer` arms the same
`workflow_offer_service` store every other confirm uses.

### 4. Registry/rail registration

- `services/intent_service/action_registry.py`: `("PORTFOLIO", "unlink_repo")` → CANONICAL (PORTFOLIO
  is claimed whole by `can_handle()`, same as `list_repos`/`link_repo`); `ACTION_EXAMPLES`,
  `ACTION_DESCRIPTIONS`, new `Verb.UNLINK`, `ACTION_TO_VERB["unlink_repo"]`.
- `services/intent_service/workflow_entries.py`: `run_unlink_repo_workflow` + `unlink_repo_entry`
  (`effect=DESTRUCTIVE`, `outwardness=PRIVATE`, `action_triggered=True`,
  `flip_write_allowlist_key="unlink_repo"`, no `flip_group`), registered under `"unlink_repo"`.
- `services/intent_service/workflow_dispatcher.py`: `FLIP_WRITE_ALLOWLIST` gains `"unlink_repo"` with
  its own three-conditions-plus-DESTRUCTIVE-build-condition comment block (all re-run, not cited).

## CXO's five constraints → how met + pin

| # | Constraint | How met | Pin |
|---|---|---|---|
| 1 | Only unlink confirms | `needs_confirm` derives from `EffectClass.DESTRUCTIVE` alone; `link_repo`/`list_repos` are WRITE/READ | `TestOnlyUnlinkConfirms::test_link_repo_and_list_repos_do_not_need_confirm` |
| 2 | Resolve before arming, never after the yes | `_resolve_unlink_repo_confirmation` runs BEFORE any question is built; failure → `passthrough_result`, nothing armed | `TestResolveBeforeArming` (5 legs: missing-both, project-not-found, repo-not-found, not-linked incl. an `AssertionError` guard on `unlink_from_project` firing during arm, fully-resolved-arms) |
| 3 | Copy, verbatim (incl. is_primary clause) | Built in `build_unlink_repo_confirmation`; success copy unchanged, verified by direct call to `_handle_unlink_repo` | `TestCopy` (4 tests) |
| 4 | Exit copy at the prompt site | "...or say 'never mind' and I'll leave it linked." appended to the question; `detect_bare_exit` already resolves bare "never mind" | `TestExitCopyAtThePromptSite` + `TestRailEndToEnd::test_never_mind_declines_and_leaves_it_linked` |
| 5 | No widening to "disconnect my GitHub" | `is_unlink_repo_action` family has exactly one member; no pre_classifier/regex touched | `test_is_unlink_repo_action_is_a_single_member_family` |

Plus: resolve-before-arming ordering (not-found never arms) — covered by `TestResolveBeforeArming`.
"Yes" executes — `TestRailEndToEnd::test_yes_executes_and_unlinks`. "No"/"never mind" leaves it linked
— `TestRailEndToEnd::test_no_declines_and_leaves_it_linked` /
`test_never_mind_declines_and_leaves_it_linked`.

## The vocab-coverage decision

`TestExecuteVocabCoverage` (`tests/test_architecture_enforcement.py`) requires every
WRITE-or-allowlisted-DESTRUCTIVE rail entry's registered verb to classify EXECUTE via
`collaboration_gate._EXECUTE_RE`. `unlink_repo`'s verb ("unlink") is not in that regex's alternation.
**Decision: exempt, not patch** — followed the test's own precedent for `delete_todo` (its sole prior
exemption): `consent_gate.decide_consent`'s matrix returns `CONFIRM` for DESTRUCTIVE in every
framing/mode cell, so `_EXECUTE_RE`'s classification has ZERO effect on `unlink_repo`'s consent outcome
— the regex's own contract comment scopes coverage to WRITE-effect actions, not DESTRUCTIVE. Added
`"unlink_repo"` to `EXEMPT_ALLOWLISTED_DESTRUCTIVE` with identical reasoning. Verified honestly: the
test's own `test_exemption_list_stays_accurate` would fail (and catch a stale exemption) if "unlink"
were ever added to `_EXECUTE_RE`.

## Why no full `process_intent` end-to-end test

PORTFOLIO is claimed WHOLE by `CanonicalHandlers.can_handle()` — true for EVERY PORTFOLIO rail entry
today (`link_repo`/`archive_project` et al. included, not something this unit introduces). A classified
(or inversion-replaced) `unlink_repo` Intent therefore hits `can_handle()`'s PORTFOLIO claim BEFORE
`_dispatch_action_rail` is ever reached — measured directly: the first draft of `TestRailEndToEnd` tried
exactly that and got the generic "portfolio_help" copy back instead of a confirm. The architecturally
honest boundary is `_dispatch_action_rail` itself, called directly (the same method the #1595
multi-intent sibling loop already calls N times per turn) to arm the REAL session-scoped offer store;
the "yes"/"no"/"never mind" second turn then goes through the genuine, unmodified offer-acceptance seam
in `process_intent` (which runs before classification/canonical, so it's unaffected by the PORTFOLIO
claim).

## Files changed

- `services/intent_service/canonical_handlers.py`
- `services/intent_service/destructive_confirm.py`
- `services/intent/intent_service.py`
- `services/intent_service/action_registry.py`
- `services/intent_service/workflow_entries.py`
- `services/intent_service/workflow_dispatcher.py`
- `tests/test_architecture_enforcement.py` (EXEMPT_ALLOWLISTED_DESTRUCTIVE)
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py` (denominator → 10)
- `tests/unit/services/intent_service/test_inversion_cross_family_release_1920.py` (new test +
  parametrize list grown to 5)
- `tests/unit/services/intent_service/test_destructive_confirm_1190.py` (DESTRUCTIVE-tier denominator)
- `tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py` (NEW — 22 tests)
- `docs/internal/architecture/current/intent-routing-stack.md` (new dated section)
- `tests/unit/services/intent_service/test_repo_management.py` — **unchanged**, byte-identical pass (31
  passed, zero mock changes needed)

## Test evidence

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_repo_management.py -q
31 passed in 1.12s

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_destructive_confirm_1190.py -q
28 passed in 2.98s

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py -q
22 passed in 0.68s

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q \
  -m "not llm" -o addopts="--ignore=tests/archive --ignore=*/archive/* \
  --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ \
  --tb=short --import-mode=importlib"
12387 passed, 228 skipped, 3 deselected, 1 xfailed, 171 warnings in 255.25s

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -m "not llm" -o addopts="--import-mode=importlib --tb=line"
205 passed, 2 skipped, 93 deselected, 52 warnings in 29.96s

env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
  POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/ \
  tests/test_architecture_enforcement.py -q -m "not llm" -o addopts="--import-mode=importlib --tb=line"
5189 passed, 3 deselected, 1 xfailed, 26 warnings in 139.12s

ruff check <all changed files>: All checks passed!
ruff format --check <all changed files>: 11 files already formatted (1 needed `ruff format`, applied)
```

One failure found and fixed mid-unit (not deferred): the first full-suite run (before the test file's
own denominator fix) failed
`test_destructive_confirm_1190.py::TestDestructiveEnumFlips1190::test_destructive_tier_scope_with_denominator`
— its hand-stated DESTRUCTIVE-tier denominator didn't yet include `unlink_repo`. Added
`UNLINK_REPO_ALIASES` and widened the assertion in the same commit, per the test's own docstring
instruction ("If a new action legitimately joins the tier, update this set in the same commit").

## STOP conditions hit

None. No LLM calls, no flag/env/`CURRENT_LIVE_CATEGORIES` change, no new `elif intent.action in [...]`
dispatch site, no new pre_classifier regex. Timestamps via `date +%H:%M`/`date +%H%M`.

## Memory & briefing surfaces referenced this session

**Referenced**: CXO's #1926 ruling memo (the five constraints, verbatim) — the acceptance criteria for
every design decision; Arch's Phase-3 rail-shapes memo (§2) — the manage_repos split and the
DESTRUCTIVE build condition; `delete_todo`'s existing confirm machinery
(`destructive_confirm.py`/`test_inversion_write_allowlist_delete_todo_1606.py`) — the template for a
custom DESTRUCTIVE confirm builder and its test shape; `link_repo`'s same-day hoist
(`canonical_handlers.py`, `workflow_entries.py`, `workflow_dispatcher.py`) — the template for the WRITE
hoist pattern and registry/allowlist wiring; `test_repo_management.py` — the legacy pin that had to stay
byte-identical.

**Loaded but not referenced**: `docs/briefing/BRIEFING-CURRENT-STATE.md`, the full CLAUDE.md role
table (dispatched directly into this role by Lead, no role-switch needed).

**Wanted but not found**: none — the authority memos cited in the dispatch prompt were complete and
sufficient.
