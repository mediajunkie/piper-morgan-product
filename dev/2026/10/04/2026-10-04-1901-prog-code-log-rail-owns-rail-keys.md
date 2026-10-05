# 2026-10-04 1901 — prog (Coding Agent) — rail-owns-rail-keys generalization

**Model**: Sonnet 5 (dispatched by Lead)
**Repo**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Authority**: Arch's ruling, `mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-exec-cio-canonical-must-not-claim-any-rail-key-hold-read-portfolio-flip-pard-findings-2026-10-04.md` §1
**Hard rules observed**: no git add/commit/push/stash/checkout --/reset; no LLM calls; no flag/env/`CURRENT_LIVE_CATEGORIES` change.

## Task

Generalize `CanonicalHandlers.can_handle` (commit `610983fb96`'s `needs_confirm`-only
decline, services/intent_service/canonical_handlers.py) so a canonical-category intent
whose action is ANY rail key declines, not just confirm-needing ones — "the rail owns
every rail key" (#1124's documented order). Measure blast radius honestly; find and fix
every ACTION_REGISTRY row the drift oracle (`test_registry_disposition_matches_live_runtime`)
now requires to flip CANONICAL → WORKFLOW; report what the canonical path does that the
rail path doesn't, and STOP-and-report (not paper over) any clear regression. Build Arch's
two pins. Update `intent-routing-stack.md`.

## What shipped

1. **`services/intent_service/canonical_handlers.py::can_handle`** — `if entry is not
   None: return False` (was `if entry is not None and needs_confirm: return False`). The
   `needs_confirm` incident (#1926) stays in the comment as what found the gap.
2. **`services/intent_service/action_registry.py`** — flipped CANONICAL → WORKFLOW for
   every canonical-category row that has a rail entry: `("TEMPORAL", "get_current_time")`,
   `("GUIDANCE", "get_contextual_guidance")`, `("PROVENANCE", "explain_suggestion")`,
   `("PORTFOLIO", "list_repos"/"search_projects"/"archive_project"/"restore_project"/
   "add_project"/"link_repo")`. `unlink_repo` was already WORKFLOW (#1926, unchanged).
   `manage_portfolio`/`manage_repos`/`greeting` stay CANONICAL — verified NOT rail keys
   (no `WorkflowEntry` registered under those names).
3. **`services/intent_service/workflow_entries.py`** — the `_read_canonical_entries()`
   validator required CANONICAL and would have raised `ValueError` at
   `register_default_workflows()` time (breaking the whole suite) once #2 landed; flipped
   its required disposition to WORKFLOW with an updated docstring. Corrected EVERY stale
   "STAYS CANONICAL / PORTFOLIO claimed WHOLE" comment block above the affected entries
   (get_current_time, read_canonical pair, read_portfolio pair, the WRITE-split trio,
   link_repo, and a pre-existing stale comment on unlink_repo's own block that was already
   wrong before today — left uncorrected through the #1926 build, fixed now).
4. **Tests updated** (disposition-flip assertions + docstrings, all citing the
   generalization): `test_read_canonical_rail_1595.py` (assertion + the validator's
   negative-test action, since `list_todos_query` is WORKFLOW now and no longer trips the
   check — swapped to `("ANALYSIS","analyze_blockers")`, FLOOR, which still does),
   `test_read_portfolio_rail_1595.py`, `test_portfolio_search_projects_read_1595.py`,
   `test_portfolio_write_split_1595.py`, `test_canonical_handlers_provenance_1030.py`
   (direct `can_handle` fact: `explain_suggestion` True → False).
5. **New pin file**: `tests/unit/services/intent_service/test_rail_owns_rail_keys_generalized_1926.py`
   — Arch's two pins, both verified for real (4 tests, all pass):
   - (a) a dispatched `list_repos` Intent via the live-consult seam
     (`consult_inversion_live` monkeypatched) through a full `process_intent` turn returns
     the repo list, not `portfolio_help`.
   - (b) a dispatched `archive_project` Intent, same seam, through a full `process_intent`
     turn actually calls `consent_gate.evaluate_consent` (spied, call-through) with
     `EffectClass.WRITE` — could not happen before this generalization.
6. **`docs/internal/architecture/current/intent-routing-stack.md`** — new major section
   ("`can_handle` generalized...") with the full before/after table, the production
   mechanism each flipped row goes through, every verified loss, the two pins, and the
   multi-intent orchestrator finding below. Corrected two stale inline passages (the
   #1926 unit's own "PORTFOLIO is claimed WHOLE" testing-boundary note and its "STAYS
   CANONICAL" disposition line) that the generalization falsified.

## Blast radius table (category rail key → before/after → disposition)

| Rail key | Category | can_handle before | can_handle after | Disposition |
|---|---|---|---|---|
| get_current_time | TEMPORAL | True | False | CANONICAL→WORKFLOW |
| get_contextual_guidance | GUIDANCE | True | False | CANONICAL→WORKFLOW |
| explain_suggestion | PROVENANCE | True | False | CANONICAL→WORKFLOW |
| list_repos | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| search_projects | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| archive_project | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| restore_project | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| add_project | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| link_repo | PORTFOLIO | True | False | CANONICAL→WORKFLOW |
| unlink_repo | PORTFOLIO | False (#1926) | False (unchanged) | WORKFLOW (unchanged) |
| manage_portfolio | PORTFOLIO | True | True (unchanged — not a rail key) | CANONICAL |
| manage_repos | PORTFOLIO | True | True (unchanged — not a rail key) | CANONICAL |
| greeting | CONVERSATION | True | True (unchanged — not a rail key) | CANONICAL |

Full "what produced this intent before / what path now" narrative is in the doc update —
short version: the rail entry for every flipped row already wrapped the SAME canonical
handler method directly; before today it was reachable only via `consult_inversion_live`
or the Phase 3 deletion gate's live-match mechanism, never via `_dispatch_action_rail` on
the unreplaced path. After today it's reachable there too, through the SAME handler.

## What's lost (verified by reading each handler, not assumed)

- **`_is_generic_canonical_response` floor-fallback safety net** — real loss, scoped to
  `get_contextual_guidance`'s non-setup synthesis branch (the only flipped row whose
  output can match `_GENERIC_CANONICAL_SIGNATURES`, all GUIDANCE-specific templates like
  "Focus: Deep work"). That branch's generic canned response no longer reroutes to the
  floor's richer context-aware answer.
- **`offer_hint` (#852 continuation-tracking)** — dropped by every rail adapter's dict→
  `IntentProcessingResult` conversion. Concretely lost: `get_contextual_guidance`'s
  setup-guidance branches, and the not-found branches of `archive_project`/
  `restore_project`/`search_projects`. `list_repos`/`link_repo`/`add_project`/
  `explain_suggestion` never set it (verified), so no loss there.
- **`multi_intent_greeting`'s "Hi there!" prefix** — no longer applies when one of these
  ops is a sibling paired with a greeting.
- **`action_required`/`ftux_interview_offer`** — verified NOT applicable to any flipped
  row (STATUS/PRIORITY-only and greeting-only respectively, both unaffected categories).

## The bigger finding — multi-intent orchestrator regression (STOP-and-report, not papered over)

`IntentService._is_orchestratable_sibling` also calls `can_handle`. Every flipped row now
returns False from it, same as a genuinely floor-routed STATUS/PRIORITY sibling. Verified
directly (`svc._is_orchestratable_sibling(archive_project_intent)` → `False`):

- **TEMPORAL**: "what time is it and what's the status of my projects?" used to
  orchestrate both siblings; now BOTH land in `_floor_routed_siblings`, and the fallback
  picks whichever comes first in message order — if that's the TEMPORAL one, the single-
  intent fallback answers only the time via the rail handler and silently drops the STATUS
  half (the floor, which would have answered both, is never reached).
- **More serious — PORTFOLIO WRITEs**: `_side_effecting` filters from `_orchestratable`,
  which no longer contains ANY of `archive_project`/`restore_project`/`add_project`/
  `link_repo`. The #1763 protection this exact code exists for ("a side-effecting sibling
  must never be dropped in favour of a conversational answer") no longer recognizes these
  writes. In a multi-intent message naming both one of these writes and a floor-routed
  topic, if the floor-routed sibling comes first in message order, the write never
  dispatches — the user is told (by the floor's guess) that something happened when it
  didn't. Order-dependent, not universal — easy to miss in ad hoc testing.

This was NOT anticipated by Arch's ruling (which assessed the single-intent path only).
**Left unfixed, not papered over**: the 7 failing assertions in
`test_multi_intent_floor_sibling_1763.py` were NOT edited to expect the regressed
behavior. They fail consistently across all three required test runs (same 7, every
time). Fixing this needs a design decision outside this unit's scope — give
`_is_orchestratable_sibling` its own predicate (e.g. "has any deterministic handler,
canonical OR rail") rather than reusing `can_handle`, or accept the narrower behavior with
a tracked follow-up issue. **Flagging to Lead/Arch for that decision now.**

## Tests

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q ...
  7 failed, 12446 passed, 228 skipped, 3 deselected, 1 xfailed, 174 warnings in 263.30s
  (all 7 failures: test_multi_intent_floor_sibling_1763.py, the orchestrator finding above)

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q ...
  205 passed, 2 skipped, 93 deselected, 52 warnings in 33.46s

env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
  POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/ tests/test_architecture_enforcement.py -q ...
  7 failed (same 7), 5200 passed, 3 deselected, 1 xfailed, 29 warnings in 140.68s
```

`ruff check` + `ruff format --check` on all 10 changed/new files: clean.

**Verified how**: ran each pytest command above this session and quoted its actual final
line (not recalled from an earlier run); the 4 new pin tests run and pass in isolation;
the `svc._is_orchestratable_sibling(...)` claims in the orchestrator finding were run
directly in a `python -c` probe this session, output quoted above (`False`/`False`). Layer:
unit tests + direct interpreter probes against the real `IntentService`/
`CanonicalHandlers`, DB layer mocked where touched — never a live LLM/router call.

## Files changed

- `services/intent_service/canonical_handlers.py`
- `services/intent_service/action_registry.py`
- `services/intent_service/workflow_entries.py`
- `docs/internal/architecture/current/intent-routing-stack.md`
- `tests/unit/services/intent_service/test_read_canonical_rail_1595.py`
- `tests/unit/services/intent_service/test_read_portfolio_rail_1595.py`
- `tests/unit/services/intent_service/test_portfolio_search_projects_read_1595.py`
- `tests/unit/services/intent_service/test_portfolio_write_split_1595.py`
- `tests/unit/services/intent_service/test_canonical_handlers_provenance_1030.py`
- `tests/unit/services/intent_service/test_multi_intent_floor_sibling_1763.py` (one fact
  assertion corrected; the 7 regression assertions left failing/documented, NOT edited)
- NEW: `tests/unit/services/intent_service/test_rail_owns_rail_keys_generalized_1926.py`

No commits made (hard rule). All changes are uncommitted working-tree edits in this
worktree, ready for Lead's review.

## Resumed per Arch 21:3x — split predicate (a) + adapter parity (b) (2026-10-04, 22:14)

**Model**: Sonnet 5 (dispatched by Lead, fresh Coding Agent instance — the parked unit above was a
separate dispatch).

Authority: `mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-exec-take-a-split-predicate-adapter-parity-
lands-with-it-b-uses-0926-sequencing-2026-10-04.md`. Brought commit `e874361ebd` into
`claude/lead-cycle` via `git cherry-pick -n e874361ebd` (clean auto-merge on
`services/intent_service/canonical_handlers.py`; main's `7f134f991b` intent-prefix skip in
`_handle_portfolio_query` was already an ancestor of HEAD, confirmed present in the working tree
post-cherry-pick — `git merge-base --is-ancestor 7f134f991b HEAD` true), `git reset -q` to unstage only.

### (a) Split predicate

Added `CanonicalHandlers.claims_category(intent)` — the category-only check `can_handle` used to do
inline, now factored out, NOT rail-aware. `can_handle` is now `if not self.claims_category(intent):
return False` followed by its existing rail-key decline — behavior unchanged, implementation
delegates.

Switched BOTH multi-intent-orchestrator callers to `claims_category`:
- `IntentService._is_orchestratable_sibling` (`services/intent/intent_service.py` ~16130)
- `IntentOrchestrator._execute_single` (`services/intent_service/orchestrator.py` ~196)

Docstrings on `claims_category`, `can_handle`, and both switched call sites all name the known cost
(PORTFOLIO writes inside multi-intent skip #1509 consent — pre-existing, not new) and cross-reference
each other.

**Every OTHER caller of `can_handle`** (`git grep -n "can_handle(" -- services web`):
- `services/intent/intent_service.py:2763` (main single-intent canonical branch) — **kept on
  `can_handle`**. This is the one path that DOES go through `_dispatch_action_rail`, so it needs the
  rail-aware decline; switching it to `claims_category` would resurrect the original bug (PORTFOLIO
  whole-category swallow before the rail/consent gate).
- `services/intent/intent_service.py:16156` (`_is_orchestratable_sibling`) — **switched to
  `claims_category`**. No rail dispatch in this path (goes straight to `CanonicalHandlers.handle()`);
  a rail-aware decline here reproduces the #1763 multi-intent regression.
- `services/intent_service/orchestrator.py:196` (`_execute_single`) — **switched to
  `claims_category`**. Same reason as above — dispatches to `self._handlers.handle(...)` directly, no
  rail adapter.
- All other grep hits are comments/docstrings naming the method, not calls.

**#1763 pins**: `tests/unit/services/intent_service/test_multi_intent_floor_sibling_1763.py` — 18/18
green after the predicate switch, UNEDITED except:
1. The one disposition-fact assertion the ORIGINAL parked build already corrected (TEMPORAL
   `get_current_time`: `can_handle()` → False is a fact about `can_handle` itself post-generalization,
   not about multi-intent orchestration behavior) — left as-is, matches the task's "stays only if it's a
   fact about dispositions" exception.
2. ONE collateral fix this session made:
   `test_predicate_failure_defaults_to_skipping_orchestration` mocked
   `intent_service.canonical_handlers.can_handle` to raise, to prove a raising predicate defaults to
   `False` (floor-safe). Since `_is_orchestratable_sibling` now calls `claims_category`, not
   `can_handle`, the mock target had to move to `claims_category` to still test the real code path —
   this is NOT a regression-assertion edit, it's keeping a test aimed at the method actually called.
   Diff is additive (new docstring note) + one line (`can_handle` → `claims_category` as the mocked
   attribute).

### (b) Adapter parity

Added `services.intent_service.workflow_entries._finalize_canonical_rail_result` — ONE shared
dict→`IntentProcessingResult` conversion, used by every canonical-wrapping rail adapter
(`run_get_current_time_workflow`, the `read_canonical` factory covering `explain_suggestion` +
`get_contextual_guidance`, `run_list_repos_workflow`, `run_search_projects_workflow`,
`run_archive_project_workflow`, `run_restore_project_workflow`, `run_add_project_workflow`,
`run_link_repo_workflow`, `run_unlink_repo_workflow` — 9 functions, 10 ops) in place of each adapter's
own ad hoc inline `IntentProcessingResult(...)` build. It:
1. Runs `IntentService._is_generic_canonical_response` on the dict FIRST; on a match, resolves
   formality baseline + trust stage and reroutes through `IntentService._handle_floor_with_context`
   (the SAME floor-fallback the main dispatch branch runs) instead of ever building the rail result.
2. Otherwise calls the NEW `IntentService._track_offer_hint` (extracted out of the main dispatch
   branch's inline #852 block, `intent_service.py` just above `_requires_canonical_handler` — same
   method now runs from both the main path and every rail adapter, one implementation) and returns
   `IntentProcessingResult(message=..., intent_data=canonical_result.get("intent"), workflow_id=None,
   requires_clarification=...)`.

`offer_hint` is not a field on `IntentProcessingResult` on the main path either — carrying it through
means running the SAME side effect (`_track_offer_hint`), not adding a field. `action_required`/
`ftux_interview_offer`/`multi_intent_greeting` confirmed (re-checked, not re-assumed) not applicable to
any of the 10 ops — `action_required` is set only by `_handle_status_query`/`_handle_priority_query`/
`_handle_spatial_project_list` (none of which this unit touches), `ftux_interview_offer` only by
`_handle_conversation_query` (greeting), `multi_intent_greeting` is multi-intent-aggregation-only and
already out of scope since (a) keeps the orchestrator off `can_handle`.

**Parity test**: NEW file
`tests/unit/services/intent_service/test_rail_adapter_canonical_parity_1926.py` — for each of the 10
ops, two independently-computed results (a standalone mirror of the main-path logic written fresh in
the test file, vs. the real registered rail adapter, both driven off the SAME stubbed canonical-handler
return value) compared on message/action/`requires_clarification`/offer_hint-tracking-outcome across 2
fixtures each (found + not-found/clarification, the latter carrying `offer_hint`) = 20 cases, plus 1
dedicated test for the generic-response floor reroute (only `get_contextual_guidance` can trigger it,
verified by reading every handler — see the ORIGINAL build's "What's lost" section above) = **21
total, denominator = 10 adapters × 2 fixtures + 1 generic case**. Sanity-checked the pin is live, not
vacuous: temporarily deleted the `_track_offer_hint` call from `_finalize_canonical_rail_result` → 10
tests went red with `AssertionError: rail adapter did not track offer_hint (#852 parity loss)`;
restored → green again.

**Collateral fixes found by the full suite run** (none are behavior regressions — all are
test-fixture/introspection code that assumed the pre-split shape of `can_handle`'s source or signature):
1. `scripts/inversion_phase3_deletion_gate.py::_canonical_categories()` — regex-introspected
   `inspect.getsource(CanonicalHandlers.can_handle)` for `IntentCategoryEnum.XXX` literals. After the
   split those literals live in `claims_category`, not `can_handle` (which now just delegates) — the
   regex would have silently returned an EMPTY frozenset. Fixed to introspect `claims_category`.
   Caught by `tests/unit/test_inversion_phase3_surface2_floor_1595.py::test_match_on_a_non_live_op_needs_the_probe`.
2. `tests/unit/services/intent_service/test_orchestrator.py` — `mock_handlers` fixture only stubbed
   `can_handle`; `_execute_single` now calls `claims_category`, so the MagicMock's auto-generated
   `claims_category` attribute returned a truthy default regardless of the test's intent. Added
   `handlers.claims_category = MagicMock(return_value=True)` to the fixture (default, matches the
   existing `can_handle` default) and switched `test_unhandleable_intent`'s override to
   `claims_category.return_value = False` (the predicate that method actually gates on now).
3. Four existing lightweight adapter tests (`test_portfolio_search_projects_read_1595.py`,
   `test_portfolio_write_split_1595.py` ×3, `test_read_canonical_rail_1595.py` ×2,
   `test_read_portfolio_rail_1595.py`) stub `intent_service` as a bare `SimpleNamespace(canonical_
   handlers=...)` with no other methods. `_finalize_canonical_rail_result` now calls
   `intent_service._is_generic_canonical_response(...)` and `intent_service._track_offer_hint(...)` —
   added no-op stubs for both (`lambda *a, **k: False` / `lambda *a, **k: None`) to each fixture so
   these stay thin "calls the handler directly" checks rather than silently requiring the full parity
   test's heavier setup.

### Tests (all run this session, final lines quoted verbatim)

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q ...
  12478 passed, 228 skipped, 3 deselected, 1 xfailed, 174 warnings in 257.14s (0:04:17)

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q ...
  205 passed, 2 skipped, 93 deselected, 52 warnings in 31.60s

env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
  POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/ \
  tests/test_architecture_enforcement.py -q ...
  5232 passed, 3 deselected, 1 xfailed, 29 warnings in 140.22s (0:02:20)
```

`ruff check` + `ruff format --check` on all 18 changed/new files: clean (one file needed
`ruff format` applied — `test_rail_adapter_canonical_parity_1926.py` — then reverified clean).

`docs/internal/architecture/current/intent-routing-stack.md` updated with a new section ("Unparked:
the split predicate (a) + adapter parity (b)") documenting both pieces, the known-cost framing, every
`can_handle` caller's disposition + reason, and the parity test's denominator.

**Verified how**: ran each pytest/ruff command above this session and quoted its actual final line;
the offer_hint-regression sanity check (delete the call, confirm 10 reds, restore, confirm green) was
run directly this session, not recalled. Layer: unit tests + direct interpreter probes against the real
`IntentService`/`CanonicalHandlers`/`IntentOrchestrator`, DB layer mocked at the handler-method boundary
(same boundary the existing lightweight adapter tests already mock at) — never a live LLM/router call.

**Hard rules observed**: no git add/commit/push/stash/checkout --/reset --hard; `git reset -q` (no
args) used once, immediately after the cherry-pick, to unstage only; no LLM calls; no flag/env/
`CURRENT_LIVE_CATEGORIES` change.

No commits made (hard rule). All changes are uncommitted working-tree edits in this worktree, ready
for Lead's review.
