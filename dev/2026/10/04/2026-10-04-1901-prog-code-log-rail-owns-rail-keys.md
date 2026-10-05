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
