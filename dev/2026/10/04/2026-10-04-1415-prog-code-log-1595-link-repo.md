# 2026-10-04 14:15 — prog (Coding Agent) — #1595 Phase 3: `manage_repos` WRITE third (`link_repo`)

Model: Sonnet. Dispatched by Lead (lead role, worktree `claude/lead-cycle`).

## Task

Build the LINK third of Arch's `manage_repos` split per the 2026-10-03 ruling
(`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-wave2-and-writes-2026-10-03.md`
§2) and the execute-vocab-coverage memo
(`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-execute-vocab-coverage-portfolio-split-file-reference-2026-10-04.md`
§1: "link-repo can proceed behind the same coverage test"). The split:
`list_repos` (READ, already built — `dev/2026/10/04/2026-10-04-0749-prog-code-log-1595-list-repos-read.md`),
`link_repo` (WRITE, THIS unit, name collision-checked, NOT flipped), `unlink_repo`
(DESTRUCTIVE, separate unit with CXO's #1926 constraints — not built here).

## What was built

- **`link_repo`** (WRITE) — hoisted from `_handle_repo_management`'s LINK
  branch into `CanonicalHandlers._handle_link_repo(intent, session_id, user_id)`.

## The hoist

`_handle_repo_management`'s operation-detection block already extracted
`repo_name` (a generic `([\w.-]+/[\w.-]+)` search, shared with the still-inline
UNLINK branch) and, within the LINK sub-case, `project_name` (the
`link_patterns` regex list). The LINK branch itself (project lookup, repo
find-or-create with #867 soft GitHub validation, already-linked check,
`link_to_project` call, and all five response shapes) lived inside the
function's `async with AsyncSessionFactory.session_scope()` block.

`_handle_link_repo` reuses the exact `repo_match` and `link_patterns` regexes
verbatim — relocated, not duplicated as a shared helper (same shape as the
`list_repos` hoist's project-name extraction). `_handle_repo_management` KEEPS
its own copy of the `repo_match` regex (the still-inline UNLINK branch needs
it) — this is a relocation for LINK only, not a refactor of the shared
extraction. No new extraction pattern; `TestExtractionPatternRatchet` is
unaffected.

`_handle_repo_management` now early-returns `await self._handle_link_repo(intent,
session_id, user_id)` for `operation == "link"`, immediately after the existing
`operation == "list"` early-return and before the `async with` block that now
contains only the UNLINK branch. `_handle_link_repo` is therefore the ONLY
place the link response is built, for both the legacy canonical dispatch
(`manage_repos`) and the new rail op (`link_repo`).

`_handle_link_repo` carries its own `user_id` guard (the same "please sign in"
dict `_handle_repo_management`'s own top-level guard returns) so it's
self-contained for direct rail dispatch — same precedent as `_handle_list_repos`
and `_handle_add_project`.

## Behavior-preservation pin

All existing `tests/unit/services/intent_service/test_repo_management.py` LINK
tests call `handler._handle_repo_management` directly (never `_handle_link_repo`)
and pass unchanged:
`test_link_needs_clarification_no_repo`, `test_link_without_project_falls_to_list`,
`test_link_success`, `test_link_project_not_found`, `test_link_already_linked` —
plus the unaffected `test_no_user_returns_sign_in_message` and all
unlink/list/pattern-detection tests. These tests patch
`services.database.session_factory.AsyncSessionFactory` (the SOURCE module),
so the local `from services.database.session_factory import AsyncSessionFactory`
import inside `_handle_link_repo` picks up the same mock — no test change
needed for the hoist itself, only for the allowlist change-detectors below.

## The write itself

`CanonicalHandlers._handle_link_repo` calls
`RepositoryRepository.link_to_project` (`services/database/repositories.py:946-964`),
which constructs a new `ProjectRepositoryLinkDB` row and `session.add`s it —
an INSERT, additive, nothing deleted or overwritten. `is_primary` is left at
its default (`False`) — the legacy LINK branch never passed it either, so this
hoist changes nothing about that behavior. **CXO's note carried forward, not
altered**: a chat-driven link always writes `is_primary=False`; it never
promotes a repo to primary. A soft-validated repo CREATE
(`RepositoryRepository.create_repository`, #867) may also run first when the
repo isn't already registered for this owner — also additive, not a
separate op (same slot-filling shape as `add_project`'s no-name turns under
Arch's manage_portfolio §2 ruling). Confirmed via
`grep -n '\.save(\|\.create(\|\.update(\|\.delete(\|session\.add\|session\.commit\|\.persist(\|INSERT'`
over `_handle_link_repo`: only `create_repository` + `link_to_project`, both
additive. WRITE, never DESTRUCTIVE.

## Op name — collision-checked

Checked `link_repo` and the surface-2-invented `link_repository` against all
three of: `derive_routing_grammar()`'s operation list, `get_action_workflows()`'s
keys, and `ACTION_REGISTRY`'s keys (grepped for `"link"` in each). Confirmed
live:

```
POSTGRES_PORT=5433 venv/bin/python -c "
from services.intent_service.inversion_router import derive_routing_grammar
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.action_registry import ACTION_REGISTRY
g = derive_routing_grammar()
names = [op.name for op in g.operations]
print('link_repo' in names, 'link_repository' in names)
print([n for n in names if 'link' in n])
print([k for k in get_action_workflows().keys() if 'link' in k])
print([k for k in ACTION_REGISTRY.keys() if 'link' in k[1]])
"
# -> False False
# -> []
# -> []
# -> []
```

Neither name answers to any existing op. Arch's own named surface-2 risk
("link_repository / list_repositories") did NOT materialize here — unlike
`list_repos`, where `list_repositories` IS a live method name elsewhere
(`github_domain_service.py`, `github_integration_router.py`,
`github_adapter.py`) at a different layer with a different meaning.

## Registry / effect / allowlist — the three #1677 conditions, re-run

1. **Registered** — `get_action_workflows()["link_repo"]` exists (this
   unit's `link_repo_entry`, `workflow_entries.py`), `action_triggered=True`.
   No alias family — a single, alias-free key, same shape as
   `set_default_repo`/`archive_project`/`restore_project`/`add_project`.
2. **Effect correct by behavior** — verified above: `link_to_project` INSERTs,
   `create_repository` INSERTs; nothing deleted or overwritten. WRITE, never
   DESTRUCTIVE.
3. **Reaches consent** — `needs_consent` derives `True` for WRITE and the
   SAME entry-agnostic rail block (`intent_service.py`'s `_dispatch_action_rail`)
   that evaluates `create_todo`/`create_reminder`/`delete_todo`/`complete_todo`/
   `archive_project`/`restore_project`/`add_project` evaluates `link_repo` too,
   via `consent_gate.evaluate_consent` (PRIVATE × WRITE × execute framing =
   PROCEED — requires "link" in `_EXECUTE_RE`, added this unit).

`ACTION_REGISTRY` disposition: `("PORTFOLIO", "link_repo")` = CANONICAL — same
verified reasoning as `list_repos`/`archive_project`/`restore_project`/
`add_project`: `PORTFOLIO` is claimed WHOLE by `canonical_handlers.can_handle()`
unconditionally, so `_true_disposition_for_registry_row`
(`test_action_registry.py`) resolves ANY `("PORTFOLIO", *)` row to CANONICAL
before the rail is ever consulted — `WORKFLOW` would fail
`test_registry_disposition_matches_live_runtime`.

## Verbs added

New `Verb.LINK = "link"` member (`action_registry.py`); `ACTION_TO_VERB["link_repo"]
= Verb.LINK`. Added `link` to `collaboration_gate._EXECUTE_RE`'s alternation —
`TestExecuteVocabCoverage` (added for `complete_todo`, grown for
`archive_project`/`restore_project`) swept `link_repo` in immediately on
registration and failed red until the vocabulary was added — exactly the
recurrence Arch's ruling named ("link/archive/restore will each hit this in
turn"). `connect` (the extraction-layer synonym the legacy `link_patterns`
already recognize) was deliberately NOT added: the test only requires the
REGISTERED verb's imperative form to classify EXECUTE, and the registered verb
is `LINK` ("link"), not `CONNECT` — "let the test tell you" (Lead's brief),
and it didn't ask for `connect`.

## #1920 cross-family pin

`link_repo` carries registry category PORTFOLIO — DIFFERENT from the
reminder/todo carriers' own EXECUTION family — so (same as
`archive_project`/`restore_project`/`add_project`) a router-named `link_repo`
turn is ELIGIBLE to cross-family-release an armed EXECUTION carrier. Added:

- `test_registry_category_for_link_repo` (new) —
  `inversion_live.registry_category_for("link_repo") == "PORTFOLIO"`.
- `test_portfolio_write_releases_an_execution_carrier`'s `@pytest.mark.parametrize`
  list grown from `["archive_project", "restore_project", "add_project"]` to
  include `"link_repo"` (four ops now).

Both in `tests/unit/services/intent_service/test_inversion_cross_family_release_1920.py`.

## FLIP_WRITE_ALLOWLIST change-detector pins (grown)

Adding `link_repo` to `FLIP_WRITE_ALLOWLIST` (`workflow_dispatcher.py`) tripped
both intentional change-detector tests in
`test_inversion_write_allowlist_1677.py` — fixed in the same commit:

- `TestAllowlistConstant::test_allowlist_is_exactly_create_todo_create_reminder_delete_todo_and_set_default_repo` —
  the exact-frozenset assertion, grown to nine named writes.
- `TestConstructorGuard::test_no_other_rail_entry_declares_a_key` — the
  denominator (m-43), grown from eight to nine entry objects.

## Files changed

- `services/intent_service/canonical_handlers.py` — hoist + new
  `_handle_link_repo` method.
- `services/intent_service/action_registry.py` — new `("PORTFOLIO", "link_repo")`
  row (CANONICAL), `ACTION_DESCRIPTIONS`, `ACTION_EXAMPLES`, new `Verb.LINK`,
  `ACTION_TO_VERB["link_repo"]`.
- `services/intent_service/collaboration_gate.py` — `link` added to
  `_EXECUTE_RE`.
- `services/intent_service/workflow_entries.py` — `run_link_repo_workflow`,
  `link_repo_entry`, registered in `_default_entries["link_repo"]`.
- `services/intent_service/workflow_dispatcher.py` — `link_repo` added to
  `FLIP_WRITE_ALLOWLIST`, three-conditions comment block.
- `tests/unit/services/intent_service/test_inversion_cross_family_release_1920.py` —
  new test + grown parametrize list.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py` —
  two change-detector pins grown to the new denominator.
- `docs/internal/architecture/current/intent-routing-stack.md` — new
  "`manage_repos` WRITE third" section.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — progress
  log entry.

## Test tails

```
# tests/unit + tests/test_architecture_enforcement.py (full baseline)
12362 passed, 228 skipped, 3 deselected, 1 xfailed, 167 warnings in 252.65s

# tests/intent/
205 passed, 2 skipped, 93 deselected, 52 warnings in 29.30s

# env-stripped intent_service subset (tests/unit/services/intent_service/ + arch-enforcement)
5164 passed, 3 deselected, 1 xfailed, 22 warnings in 137.62s

# tests/unit/test_inversion_phase3_deletion_1595.py — ledger verdict
56 passed in 8.21s — NO CHANGE from before this unit (same 56/0).

# ruff
All checks passed! (check)
1 file already formatted (format --check, after `ruff format` applied the
  single-line signature collapse to the new _handle_link_repo method)
```

Full re-run after the ruff-format pass (targeted subset, to confirm the
reformat changed nothing behaviorally): 129 passed
(`test_repo_management.py` + `TestExecuteVocabCoverage` +
`test_inversion_cross_family_release_1920.py` +
`test_inversion_write_allowlist_1677.py` +
`test_inversion_phase3_deletion_1595.py`).

## Not done in this unit

- **`unlink_repo`** — DESTRUCTIVE, separate unit per CXO's #1926 constraints
  (copy, the `is_primary` clause, never-mind exit, no widening to "disconnect
  my GitHub"). The confirm prompt must pull its identifying detail from the
  SAME extraction the legacy path uses (Arch's §2, "resolve before arming") —
  hoist the existing extraction (`canonical_handlers.py`, now relocated
  slightly by this unit) ahead of the gate, no new regexes.
- **`REPO_MANAGEMENT_PATTERNS`/the corpus** — not touched, per the brief.
- **Any flag/env/`CURRENT_LIVE_CATEGORIES` change** — this unit is NOT
  flipped. The Phase-2 gate and PM flag token are Lead's/Exec's next steps,
  same as every other #1595 Phase 3 WRITE entry.

## Verified how

Method: ran the exact test commands in the brief and read their full tails
(not truncated) this turn; ran the live collision-check script this turn
(output pasted above, not recalled from a prior run); ran `ruff check` +
`ruff format --check`/`ruff format` this turn and reviewed the diff to
confirm the reformat touched only this unit's own added/removed lines.
Layer: source-level test execution (pytest) + static analysis (ruff) +
a live Python REPL probe of the registry/rail/grammar — not a live chat
turn (this entry is NOT flipped, so no end-to-end chat probe is applicable).
Denominator: the four required test commands from the brief, all run to
completion with full tails read; the two change-detector test files found
failing were both fixed and re-verified green in the same session.
