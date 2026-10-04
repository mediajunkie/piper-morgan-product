# 2026-10-04 — Coding Agent (prog), #1595 Phase 3 — `read_canonical` (explain_suggestion / get_contextual_guidance)

**Model**: Sonnet (assigned by Lead, dispatched as a subagent)
**Role**: Coding Agent (prog)
**Repo/branch**: `/Users/xian/Development/piper-morgan-worktrees/lead`, `claude/lead-cycle`

## Task

Build a NEW flip group `read_canonical` (NOT flipped) for two CANONICAL-disposition ops Arch's
ruling identified as reads despite looking like writes: `explain_suggestion` (PROVENANCE) and
`get_contextual_guidance` (GUIDANCE). Authority:
`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-
wave2-and-writes-2026-10-03.md`, section 3 ("Two 'CANONICAL writes' are reads"). Use the
`get_current_time` precedent (commit `e8429ffd9a`); build shape mirrors the `read_floor_2` build
(commit `60442f22d3`, lane log `dev/2026/10/03/2026-10-03-2159-prog-code-log-1595-read-floor-2.md`).

## READ verification (per op, before grouping)

### `explain_suggestion` (PROVENANCE, CANONICAL, verb EXPLAIN) — IN

Handler: `CanonicalHandlers._handle_provenance_query`
(`services/intent_service/canonical_handlers.py:5603-5764`).

- Reads `conversation_context.get_or_create_context(session_id, user_id=user_id)` — an in-process,
  module-level dict (`_conversation_contexts: dict[str, ConversationContext] = {}`,
  `services/intent_service/conversation_context.py:397`). Not persisted to any database, not a
  domain write — a process-scoped cache.
- On a sidecar miss, falls back to `ConversationRepository.get_most_recent_turn_provenance` (a read
  query against `turn_metadata['provenance']`).
- Formats a colleague-prose citation from `self._PROVENANCE_PHRASES` and returns.
- `logger.info`/`logger.warning`/`logger.error` calls only — no `.save(`/`.create(`/`.update(`/
  `.delete(`/`session.add`/`session.commit`/`.persist(` anywhere in the function (read the whole
  162-line function body directly).

### `get_contextual_guidance` (GUIDANCE, CANONICAL, verb GET) — IN

Handler: `CanonicalHandlers._handle_guidance_query`
(`services/intent_service/canonical_handlers.py:4201-4333`). `handle()`
(`canonical_handlers.py:158-171`) dispatches this unconditionally for the whole GUIDANCE category
— there is exactly one GUIDANCE action in `ACTION_REGISTRY`.

Three branches plus the main path, all checked:

- `_detect_setup_request` (`:2220-2268`) — pure regex/string matching over
  `intent.original_message`, no I/O.
- `_handle_project_setup_request` (`:2319-2395`) — reads `user_context_service.get_user_context`;
  returns static or read-derived guidance text. ADR-059 note in the source: "Interactive onboarding
  disabled (on ice)" — never launches a workflow.
- `_format_integration_setup_guidance` (`:2397-2492`) — reads
  `IntegrationStatusService().get_all(user_id)`, formats a message. Read-only.
- `_format_general_setup_guidance` (`:2494-2541`) — static text, no I/O.
- Main path (`:4227-4333`): `_get_calendar_context`, `_get_project_metadata`,
  `_get_priority_metadata`, `_synthesize_focus_recommendation`, one of
  `_format_detailed_guidance`/`_format_consolidated_guidance`/`_format_standard_guidance`,
  `_get_immediate_focus` — all defined in `canonical_handlers.py:1387-2220`.

Mechanical check over the whole call-graph span:
```
sed -n '1387,2220p' services/intent_service/canonical_handlers.py | \
  grep -n '\.save(\|\.create(\|\.update(\|\.delete(\|session\.add\|session\.commit\|\.persist(\|INSERT'
```
Zero hits. Confirmed READ end to end.

## Build

- `services/intent_service/workflow_dispatcher.py`: `FLIP_GROUPS` gains `read_canonical` (7 → 8
  members), with a block comment explaining the shape (CANONICAL-disposition ops, named group
  never a raw category token since GUIDANCE is a whole category).
- `services/intent_service/workflow_entries.py`: added `_READ_CANONICAL_MEMBERS` (`{op: (category,
  handler_attr)}`), `_make_read_canonical_entry_point(op, handler_attr)` (calls
  `getattr(canonical_handlers, handler_attr)(intent, session_id, user_id)` directly — the
  `get_current_time` shape, NOT the `read_floor` factory shape, since neither handler branches on
  `intent.category` so there is nothing to re-key), `_read_canonical_entries()` (cross-checks each
  member against `ACTION_REGISTRY`, raises on a non-CANONICAL member). Wired into
  `register_default_workflows()` via `**_read_canonical_entries()` immediately after
  `**_read_floor_2_entries()`.
- Collision check: `grep -rn "read_canonical" . --include="*.py" --include="*.md"` returned nothing
  before this change; `derive_routing_grammar()`'s output (verified via REPL) contained no
  `read_canonical` token either.
- ACTION_REGISTRY disposition: both ops STAY CANONICAL — same note as `get_current_time`'s.
  `CanonicalHandlers.can_handle()` claims the whole PROVENANCE/GUIDANCE category unconditionally,
  so in the real dispatch order (`_should_route_to_floor` → `can_handle` → action rail) the
  canonical branch returns before the action rail is ever reached. The rail entry is consulted
  only by `consult_inversion_live` (which replaces `intent.action`/`category` before the normal
  order resumes) and by the Phase 3 deletion gate's live-match mechanism.
- Did **not** touch any flag/env/`CURRENT_LIVE_CATEGORIES`/deployment config. No new
  `elif intent.action` branch (`MAX_DISPATCH_SITES` untouched). No new extraction regexes. No LLM
  calls anywhere in this unit.

## Gate/ledger effect — checked, no regression

Per the dispatch brief's warning (the `read_floor_2` build found adding a rail entry for a
FLOOR-disposition op could flip the Phase 3 deletion gate's ledger non-regression verdicts), traced
the equivalent path for CANONICAL ops before assuming it was safe:

- `scripts/inversion_phase3_deletion_gate.py::_surface2_reaches_floor` checks
  `p1._expected_action_is_floor_disposition(action, op_categories)` and
  `_floor_op_behind_unflipped_entry(action, op_categories)` first — both return `False`
  immediately for a non-FLOOR disposition (`get_disposition(category, action) is not
  ActionDisposition.FLOOR: return False`, in both functions). For PROVENANCE/GUIDANCE this is
  always the case.
- Falls to `elif want in _CANONICAL_CATEGORIES:` — PROVENANCE and GUIDANCE both match (parsed
  from `CanonicalHandlers.can_handle`'s source) — which returns `(True, "canonical category")`
  **unconditionally**, with no unflipped-rail-entry gating of any kind. This branch does not care
  whether a rail entry exists.
- `row_disposition`'s MATCH branch (`:855-913`) reaches `_surface2_reaches_floor` only after
  `expected_action_is_live(expected, cats)` fails — unaffected by this change since
  `read_canonical` is not in `CURRENT_LIVE_CATEGORIES`.
- Confirmed empirically: `tests/unit/test_inversion_phase3_deletion_1595.py` — 45 passed after one
  stand-in swap (below), 0 failed. No ledger row changed verdict from this build.

## Test fallout — two stand-in pins swapped (both ops had been "the rail-free example")

Both `explain_suggestion` and `get_contextual_guidance` were used elsewhere in the suite as
stand-in examples of "a CANONICAL op with no rail entry." Gaining a rail entry here broke both;
swapped both to `manage_portfolio` (PORTFOLIO, CANONICAL) — confirmed genuinely still rail-free via
`"manage_portfolio" in get_action_workflows()` → `False`, same check the second test now asserts
inline:

- `tests/unit/services/intent_service/test_inversion_live_1595.py::TestFallthroughReasons::
  test_registry_only_operation_not_rail_dispatchable` — was `get_contextual_guidance`/`GUIDANCE`,
  swapped to `manage_portfolio`/`PORTFOLIO`.
- `tests/unit/test_inversion_phase3_deletion_1595.py::TestLiveMeansDispatchable::
  test_floor_routed_canonical_is_not_live_even_when_named_in_the_flag` — was
  `explain_suggestion`/`PROVENANCE`, swapped to `manage_portfolio`/`PORTFOLIO`. This test's own
  body already asserted the pick was still rail-free (`assert get_action_workflows().get(...) is
  None, "... pick another ... rather than deleting it"`) — the assertion caught the break
  immediately on first run, exactly as designed.

Same stand-in-swap shape `read_floor_2` used for `get_identity` (swapped from `get_identity` to
`get_contextual_guidance`, which this build then had to swap again).

## No change needed (checked, not assumed)

- `tests/unit/services/intent_service/test_action_registry.py`'s `_true_disposition_for_registry_row`
  oracle: traced its control flow — `_should_route_to_floor` runs first. PROVENANCE is never in
  `_FLOOR_ROUTED_CATEGORIES`, so `can_handle()` resolves CANONICAL immediately. GUIDANCE IS in
  `_FLOOR_ROUTED_CATEGORIES`, but `_requires_canonical_handler` carves out the setup-request path
  (already handled by the existing `_DISPOSITION_TEST_MESSAGE_OVERRIDES` entry for this row —
  pre-existing, untouched). Either way the oracle resolves CANONICAL before it ever reaches the
  rail-entry-membership branch — unlike `read_floor_2`'s QUERY-category members (QUERY isn't
  floor-routed by category), which needed the oracle's `flip_group in (...)` check widened.
- `scripts/inversion_phase1_shadow_score.py`'s `_expected_action_is_floor_disposition`: same
  early-return-False-for-non-FLOOR shape, confirmed by reading it directly — no change needed.
- `scripts/inversion_phase2_gate.py` / `inversion_live.py`'s `resolve_live_match`: both iterate
  `FLIP_GROUPS`/check `flip_group` generically, group-name-agnostic — adding `read_canonical` to
  the frozenset is sufficient.

## Files changed

```
 M services/intent_service/workflow_dispatcher.py
 M services/intent_service/workflow_entries.py
 M tests/unit/services/intent_service/test_inversion_live_1595.py
 M tests/unit/services/intent_service/test_inversion_flip_groups_1667.py
 M tests/unit/test_inversion_phase3_deletion_1595.py
?? tests/unit/services/intent_service/test_read_canonical_rail_1595.py
 M docs/internal/architecture/current/intent-routing-stack.md
 M dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md
?? dev/2026/10/04/2026-10-04-0638-prog-code-log-1595-read-canonical.md
```

No git add/commit/push/stash performed — Lead reviews and commits.

## Tests

```
POSTGRES_PORT=5433 venv/bin/python -m pytest \
  tests/unit/services/intent_service/test_read_canonical_rail_1595.py \
  tests/unit/services/intent_service/test_read_floor_2_rail_1595.py \
  tests/unit/services/intent_service/test_read_floor_rail_1595.py \
  tests/unit/services/intent_service/test_inversion_flip_groups_1667.py \
  tests/unit/services/intent_service/test_action_registry.py \
  tests/unit/services/intent_service/test_inversion_live_1595.py \
  tests/unit/services/intent_service/test_inversion_router_1595.py \
  -q -p no:cacheprovider -m "not llm" -o addopts="--import-mode=importlib --tb=short"
# 231 passed, 1 deselected

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py \
  -q -p no:cacheprovider -m "not llm" -o addopts="--import-mode=importlib --tb=short"
# 45 passed (1 stand-in swap required, see above)
```

Full-suite run (`tests/unit` + `tests/test_architecture_enforcement.py`, and `tests/intent/`) —
dispatched in the background; tail recorded below once complete.

`ruff check` clean on every changed `.py` file. `ruff format --check` required one reformat
(`test_read_canonical_rail_1595.py` — applied via `ruff format`, re-checked clean).

## Memory & briefing surfaces referenced this session

**Referenced**: `project_router_grammar_prefers_rail_entry_description` (confirmed the current
`_read_floor_2_entries()`/`get_current_time_entry` already implement this — mirrored it for
`read_canonical` without rediscovering the lesson). CLAUDE.md "Verify First, Create Second" / "Name
the layer, and state the denominator" — informed the READ-verification write-up (layer: source
read of the handler and its full call graph, no LLM; denominator: both members of the group, each
cited by file:line).

**Loaded but not referenced**: the rest of CLAUDE.md's worktree/mailbox discipline sections (not
relevant — no git/mailbox writes performed by this subagent).

**Wanted but not found**: none.
