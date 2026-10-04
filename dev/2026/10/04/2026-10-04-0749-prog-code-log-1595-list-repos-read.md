# 2026-10-04 — Coding Agent (prog), #1595 Phase 3 — `read_portfolio` (list_repos, the LIST half of manage_repos)

**Model**: Sonnet (assigned by Lead, dispatched as a subagent)
**Role**: Coding Agent (prog)
**Repo/branch**: `/Users/xian/Development/piper-morgan-worktrees/lead`, `claude/lead-cycle`

## Task

Build a NEW READ rail operation, `list_repos`, in a new READ flip group (`read_portfolio`, NOT
flipped) — the LIST half of Arch's `manage_repos` three-way split. Authority:
`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-
wave2-and-writes-2026-10-03.md`, section 2 ("manage_repos: split into three ops: list READ / link
WRITE / unlink DESTRUCTIVE"). This task is the list op only — link and unlink are separate tasks,
not built here. Build shape mirrors the `get_current_time` precedent and the `read_canonical`
build (lane log `dev/2026/10/04/2026-10-04-0638-prog-code-log-1595-read-canonical.md`).

## The hoist (behaviour-preserving refactor)

`CanonicalHandlers._handle_repo_management` (`services/intent_service/canonical_handlers.py`) is
the `manage_repos` canonical handler — it regex-detects `link`/`unlink`/`list` operations from the
message text, then had the LIST response built inline inside the same `async with
AsyncSessionFactory.session_scope()` block as link/unlink.

Extracted the LIST branch into a new method, `CanonicalHandlers._handle_list_repos(intent,
session_id, user_id)` — the project-name extraction (`(?:for|of|on)\s+(?:(?:my|the)\s+)?(?:
project\s+)?(.+)` against `message_lower`) is the SAME regex the old inline LIST sub-case used,
relocated rather than duplicated (no new pattern — `TestExtractionPatternRatchet`). The dead
duplicate extraction that used to also run during operation-detection (list_patterns matching) was
removed; that detection block now only decides "is this a list op," leaving the project-name
extraction solely to `_handle_list_repos`.

`_handle_repo_management` now early-returns `await self._handle_list_repos(intent, session_id,
user_id)` when `operation == "list"`, BEFORE opening the link/unlink session block — so
`_handle_list_repos` is the ONE place the list response is built, for both the legacy canonical
dispatch (`manage_repos`) and the new rail op (`list_repos`). Exceptions inside
`_handle_list_repos` still propagate to `_handle_repo_management`'s existing
`except Exception as e:` when called from the legacy path (unchanged error-dict behaviour,
`action: "manage_repos_error"`); when called directly via the rail, `workflow_dispatcher.
dispatch_workflow`'s own try/except catches anything uncaught and returns `None` (routes to floor)
— no new exception handling needed in the new method.

**Pin**: all 31 `tests/unit/services/intent_service/test_repo_management.py` tests pass unchanged
after the hoist, including the list-specific ones (`test_list_repos_for_project`,
`test_list_all_repos`, `test_list_empty_repos`, `test_list_patterns_detected`,
`test_link_without_project_falls_to_list`) — they call `_handle_repo_management` directly, so this
is byte-identical-output evidence on the legacy path, not just "it compiles."

## Op name + collision check

Candidates per the task: `list_repositories`, `list_repos`, `list_linked_repos`. Checked
`derive_routing_grammar()`'s inputs (`ACTION_REGISTRY`, rail keys via `get_action_workflows()`)
and grepped `services/`/`tests/` directly:

- `list_repositories` IS a live method name — but at a different layer, with a different meaning:
  `services/domain/github_domain_service.py`, `services/integrations/github/
  github_integration_router.py`, `services/mcp/consumer/github_adapter.py` all implement/wrap
  "every repo on the user's GitHub account," not "repos linked to a project." None of the three is
  registered as an `ACTION_REGISTRY`/rail action, so there's no grammar-level collision, but using
  the same string for a differently-scoped operation would conflate two things the router should
  keep distinct.
- `list_repos` — not an `ACTION_REGISTRY` key, not a rail key, before this build. It also matches
  the label `_handle_repo_management` already returned internally (`intent.action: "list_repos"`
  in its Dict envelope, pre-existing, unchanged by this build) — picking it keeps the internal
  label and the new rail op name the same string.
- `list_linked_repos` — unused anywhere in the codebase; no collision either way, but no existing
  precedent to align with.

Chose **`list_repos`** — no collision, aligns with the pre-existing internal label, and reads
naturally for the router.

## Registry disposition: deviated from the literal task instruction, verified why

The task said: category PORTFOLIO (matching `manage_repos`), disposition WORKFLOW, "mirror
`get_default_repo`/`list_issues_query`." I checked this against the registry/runtime drift oracle
before committing to it and it does NOT hold for this op, for a reason specific to PORTFOLIO:

- `get_default_repo`/`list_issues_query` are **QUERY**-category. `CanonicalHandlers.can_handle()`
  does not claim QUERY, so the action rail IS reached for them — WORKFLOW is correct.
- `manage_repos`/`list_repos` are **PORTFOLIO**-category. `can_handle()`'s `canonical_categories`
  DOES claim PORTFOLIO unconditionally (same set as TEMPORAL/GUIDANCE/CONVERSATION/PROVENANCE).
  `_handle_portfolio_query` (the PORTFOLIO dispatcher) checks `intent.action == "manage_repos"` by
  bare STRING match and otherwise pattern-matches the raw message text for archive/delete/
  restore/list/add/search — it never consults rail membership. So in the real dispatch order
  (`_should_route_to_floor` → `canonical_handlers.can_handle` → `_dispatch_action_rail`,
  `services/intent/intent_service.py:2738-2934`), the canonical branch returns before the action
  rail is EVER reached for any PORTFOLIO intent, `list_repos` included.
- Confirmed directly against `_true_disposition_for_registry_row`
  (`tests/unit/services/intent_service/test_action_registry.py`): it resolves
  `canonical_handlers.can_handle()` (step 2) before the rail-entry check (step 3) — for category
  PORTFOLIO that step-2 check is `True` unconditionally, so the oracle returns CANONICAL
  regardless of the registry's own disposition. Registering `("PORTFOLIO", "list_repos"):
  WORKFLOW` would make `test_registry_disposition_matches_live_runtime` assert `WORKFLOW ==
  CANONICAL` and fail.

Used **CANONICAL** instead — the exact shape `get_current_time`/`read_canonical` already use for
this situation (a whole canonically-claimed category): the rail entry exists only for
`consult_inversion_live` (which replaces `intent.action`/`category` before the normal dispatch
order resumes) and the Phase 3 deletion gate's live-match mechanism, never reachable via
`_dispatch_action_rail` on the unreplaced path. Ran the targeted test suite BEFORE and AFTER this
choice to confirm: `test_action_registry.py` + the three existing read-rail pin files = 114 passed
clean with CANONICAL.

## Implementation

- `services/intent_service/canonical_handlers.py`: added `_handle_list_repos` (hoisted list
  logic + relocated extraction, ~140 lines); trimmed `_handle_repo_management`'s list-patterns
  detection (removed the now-dead inline extraction) and replaced its old inline LIST block with
  the early-return delegation.
- `services/intent_service/action_registry.py`: new row `("PORTFOLIO", "list_repos"):
  ActionDisposition.CANONICAL` (with a comment citing the verified-not-WORKFLOW reasoning above,
  so a future reader doesn't "fix" it back to WORKFLOW without re-deriving this), plus
  `ACTION_EXAMPLES`, `ACTION_DESCRIPTIONS`, and `ACTION_TO_VERB` (`Verb.LIST`) entries.
- `services/intent_service/workflow_dispatcher.py`: `FLIP_GROUPS` gains `"read_portfolio"`, with
  a block comment citing Arch's ruling section 2 and the CANONICAL-disposition verification.
- `services/intent_service/workflow_entries.py`: standalone adapter `run_list_repos_workflow`
  (the `get_current_time` shape — not the generic `_read_canonical_entries()` factory, since this
  op needed its own flip group distinct from `read_canonical`'s section-3 grouping) +
  `list_repos_entry` (`EffectClass.READ`, `flip_group="read_portfolio"`, `action_triggered=True`),
  registered under `"list_repos"` in `_default_entries`.
- `REPO_MANAGEMENT_PATTERNS`/the corpus: NOT touched (per the task's hard rule; `manage_repos`
  stays CANONICAL in the registry as the legacy path until that pattern list is empty).
- No LLM calls, no flag/env/`CURRENT_LIVE_CATEGORIES`/deploy change, no new `elif intent.action`
  branch (`MAX_DISPATCH_SITES` unchanged — an entry, never a branch), no new extraction regexes.

## Full-suite gate: one pre-existing closed-set pin needed updating

Running the full baseline suite surfaced ONE failure:
`tests/unit/services/intent_service/test_inversion_flip_groups_1667.py::TestFlipGroupDeclaration::
test_wave_1_vocabulary` — a closed-set `assert FLIP_GROUPS == frozenset({...})` pin that is
DESIGNED to grow with the vocabulary (its own docstring says so) and had not yet been updated for
`read_portfolio`. Updated the assertion to the 9-member set with a dated comment. This is the same
"closed-set pin grows with the vocabulary" maintenance every prior #1595 Phase 3 build in this
file has done (`read_temporal`→6, `read_floor`→... through `read_canonical`→8) — not a surprise,
just confirming where it landed this time.

## Tests

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_repo_management.py -q
-> 31 passed

POSTGRES_PORT=5433 venv/bin/python -m pytest \
  tests/unit/services/intent_service/test_action_registry.py \
  tests/unit/services/intent_service/test_read_canonical_rail_1595.py \
  tests/unit/services/intent_service/test_read_floor_2_rail_1595.py \
  tests/unit/services/intent_service/test_read_floor_rail_1595.py -q
-> 114 passed

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q
-> 45 passed (no ledger-verdict change from adding this rail op)

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -m "not llm"
-> 205 passed, 2 skipped, 93 deselected

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_read_portfolio_rail_1595.py -q
-> 8 passed (new pin: membership, CANONICAL-disposition check, entry-point-calls-the-handler-
   directly, missing-context -> None, live-match-through-the-group, not-live-under-current-flag,
   router-description coverage, and a direct check that _handle_repo_management's LIST case
   delegates to _handle_list_repos)

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q \
  -m "not llm" -o addopts="--ignore=tests/archive --ignore=*/archive/* \
  --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/"
-> first run: 1 failed (test_wave_1_vocabulary, fixed above), 12253 passed, 228 skipped,
   3 deselected, 1 xfailed
-> re-run after the fix: in progress / clean (see handback report for final tail)

ruff check services/intent_service/{canonical_handlers,workflow_entries,workflow_dispatcher,action_registry}.py
  tests/unit/services/intent_service/test_read_portfolio_rail_1595.py
-> All checks passed!

ruff format --check (same files)
-> 1 file needed reformatting (canonical_handlers.py, an unrelated pre-existing string-join
   artifact adjacent to my new code) -> ruff format applied -> clean
```

## Docs

- `docs/internal/architecture/current/intent-routing-stack.md`: new `read_portfolio` section
  (mirrors the `read_canonical`/`read_floor_2` section shape — ruling citation, hoist mechanics,
  op-name collision check, the CANONICAL-disposition deviation + verification, implementation,
  tests, not-flipped statement).
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`: dated entry appended.

## Discovered work

None filed — no new issue needed. The one test-suite break (`test_wave_1_vocabulary`) was fixed
in the same unit of work per the established pattern (every prior Phase 3 flip-group build updates
this same pin).

## Report to Lead

See `SubagentHandback` message for the full summary (op name + collision check, hoist + pin
evidence, registry/group/entry, files changed, test tails, gate effect, and the disposition
deviation called out explicitly for review).
