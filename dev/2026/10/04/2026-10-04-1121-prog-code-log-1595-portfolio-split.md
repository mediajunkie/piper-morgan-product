# 2026-10-04 11:21 — prog (Coding Agent) — #1595 Phase 3: `manage_portfolio` WRITE split

Model: Sonnet. Dispatched by Lead (lead role, worktree `claude/lead-cycle`).

## Task

Build Arch's `manage_portfolio` rail split per the 2026-10-04 ruling
(`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-execute-vocab-coverage-portfolio-split-file-reference-2026-10-04.md`
§2) and the effect inventory it rules on
(`dev/2026/10/04/manage-portfolio-effect-inventory-2026-10-04.md`). The split:
`list_projects` (READ: active list + search), the existing
`list_archived_projects` (retire the in-handler branch in its favour),
`archive_project` and `restore_project` (WRITE, separate ops), `add_project`
(WRITE). Delete: no rail entry, pending #1930. NOT flipped (no live-category
or flag change).

## What was built

- **`archive_project`** (WRITE) — hoisted from `_handle_portfolio_query`'s
  ARCHIVE branch into `CanonicalHandlers._handle_archive_project`.
- **`restore_project`** (WRITE) — hoisted from the RESTORE branch into
  `CanonicalHandlers._handle_restore_project`.
- **`add_project`** (WRITE) — wraps the EXISTING `_handle_add_project`
  (#1856; no hoist needed, already its own method). Added a self-contained
  no-user_id guard (default `None`) so the method is correct when dispatched
  directly via the rail, mirroring `_handle_list_repos`'s own guard.
- **`list_archived` retirement** — `_handle_portfolio_query` now delegates
  to the EXISTING `run_archived_projects_query_workflow` (workflow_entries.py,
  #1570) directly, converting its `IntentProcessingResult` back into the
  handler's `Dict` shape. One source for both call paths.

## NOT built: `list_projects` — BLOCKING COLLISION, reported not resolved

The dispatch's own HOW section anticipated this exact scenario ("if a
`list_projects` entry ALREADY exists, report what it is and reuse/align
rather than duplicate — STOP if they conflict"). It exists:
`workflow_entries.py`'s `_query_cohort` list already registers
`["list_projects", "show_projects"]` aliasing ONE `WorkflowEntry` around
`IntentService._handle_projects_query` — QUERY category, `flip_group=
"read_status"`, rendered via `format_projects_conscious`, active-list ONLY
(no search).

This is a REAL key collision, not a name coincidence: `_default_entries` is
built as one Python dict literal (where this unit's new keys —
`archive_project`/`restore_project`/`add_project`/`list_repos`/etc. — live),
and a `for entry, aliases in _query_cohort: _default_entries[alias] = entry`
loop runs LATER in the SAME module, unconditionally assigning
`_default_entries["list_projects"]`. Placing a same-named PORTFOLIO entry
inside the earlier literal would be silently clobbered by that loop — proven,
not assumed: verified live (`register_default_workflows();
get_action_workflows()["list_projects"]` resolves to the pre-existing QUERY
entry, `effect=READ`, `flip_group="read_status"`, confirmed unchanged by this
build) and pinned as a regression guard
(`test_portfolio_write_split_1595.py::test_list_projects_collision_survives_untouched`).

**Not resolved unilaterally** — naming is Lead/Arch's call per the dispatch's
own instruction. Recommend: either pick a disambiguated name for the
PORTFOLIO active-list+search op (e.g. `list_portfolio_projects`), or rule on
extending/reusing the EXISTING `list_projects` entry (it would need a search
capability added, and its ACTION_REGISTRY category/flip_group story
reconsidered for the PORTFOLIO-vs-QUERY question).

## Verbs added to `_EXECUTE_RE`

`archive` and `restore` — caught immediately by `TestExecuteVocabCoverage`
(added for `complete_todo` in the prior unit), exactly the recurrence Arch's
ruling predicted ("link/archive/restore will each hit this in turn").
`add_project`'s verb is `CREATE` ("add"), already covered — no vocabulary
change needed for it. Verified live:
`classify_framing("archive the item")` / `classify_framing("restore the
item")` / `classify_framing("create the item")` all read `"execute"`.

## Registry disposition

CANONICAL for all three new ops (`("PORTFOLIO", "archive_project")`,
`("PORTFOLIO", "restore_project")`, `("PORTFOLIO", "add_project")`) — same
verified reasoning as `list_repos`: `CanonicalHandlers.can_handle()` claims
the WHOLE PORTFOLIO category unconditionally, so `WORKFLOW` would fail
`test_registry_disposition_matches_live_runtime`. Two new `Verb` enum
members (`ARCHIVE`, `RESTORE`); `add_project` reuses `Verb.CREATE`.
`ACTION_EXAMPLES`/`ACTION_DESCRIPTIONS` rows added for router-grammar
description coverage.

## Collision checks (router names)

`archive_project`, `restore_project`, `add_project` — none were existing
`ACTION_REGISTRY`/`WORKFLOW_REGISTRY` keys prior to this build (grep-verified
over `services/intent_service/action_registry.py`,
`services/intent_service/workflow_entries.py`,
`services/intent_service/workflow_dispatcher.py`; none appear anywhere
except as pre-existing `intent.action` Dict-envelope labels inside
`canonical_handlers.py`, unaffected by rail registration). `list_projects`:
the one real collision, documented above, left unbuilt.

## #1920 cross-family note

All three carry registry category PORTFOLIO, which DIFFERS from the
reminder/todo carriers' own EXECUTION family — unlike `complete_todo`/
`delete_todo` (same-family, decline), a router-named
`archive_project`/`restore_project`/`add_project` turn now becomes ELIGIBLE
to cross-family-release an armed EXECUTION carrier, exactly like
`close_issue_query` already does. Pinned in
`test_inversion_cross_family_release_1920.py`
(`test_registry_category_for_the_new_portfolio_writes`,
`TestCrossFamilyWriteRelease::test_portfolio_write_releases_an_execution_carrier`,
parametrized over all three ops).

## An unrelated pre-existing ratchet interaction, found and resolved

Hoisting the ARCHIVE/RESTORE branches' "I couldn't find a project called
'…'. Would you like me to list your [archived] projects?" messages (+ their
`offer_hint` `offer_text` literals, separate literals with overlapping text)
into the two new methods would have registered as TWO NEW unarmed-ask-site
holders under `TestUnarmedAskSiteRatchet` (#1766) — forbidden ("NEVER add a
row — a new unarmed ask site must arm instead", shrink-only). Rewrote both
as imperative, non-interrogative copy instead — the SAME fix #1856 already
applied to `add_project`'s own no-name case ("not an ask at all"). Verified
no existing test pins the old text for these specific archive/restore
not-found/no-name paths (grep across `tests/`) before changing it; this is
the one deliberate user-facing copy deviation from byte-identical in this
build, required by the ratchet, not a style choice.

This also dropped the TOTAL interrogative-literal count scanned by
`TestUnarmedAskSiteRatchet`'s `test_scan_space_is_populated` sanity floor
(measured 42 before this unit, 38 after — verified via a temporary
`git stash`/`git stash pop` round-trip to get the true before/after numbers)
below its `>= 40` floor — a REAL reduction (4 literals removed: the
message + offer_hint text for both archive and restore not-found branches),
not scanner breakage. Lowered the floor 40 → 35 with a dated comment
explaining the shift; 38 still satisfies the comment's own "(dozens exist)"
characterization.

`_handle_portfolio_query`'s own `KNOWN_UNARMED_ASK_SITES` row shrunk 11 → 7
(same fingerprint text, no new holders) — updated with a dated comment.

## Files changed

- `services/intent_service/action_registry.py` — new `ActionDisposition`
  rows (3), `ACTION_EXAMPLES`/`ACTION_DESCRIPTIONS` rows (3), two new `Verb`
  members (`ARCHIVE`, `RESTORE`), three `ACTION_TO_VERB` rows.
- `services/intent_service/canonical_handlers.py` — `_handle_archive_project`,
  `_handle_restore_project` (new methods); `_handle_portfolio_query` dispatch
  changes (early-return for archive/restore/list_archived; dead bodies
  removed from inside the old session-scope block; delete/search untouched);
  `_handle_add_project` gained a no-user_id guard.
- `services/intent_service/collaboration_gate.py` — `archive|restore` added
  to `_EXECUTE_RE`.
- `services/intent_service/workflow_dispatcher.py` — `FLIP_WRITE_ALLOWLIST`
  gains `archive_project`/`restore_project`/`add_project`, each with a full
  three-conditions comment block.
- `services/intent_service/workflow_entries.py` — `run_archive_project_workflow`/
  `run_restore_project_workflow`/`run_add_project_workflow` (entry points),
  `archive_project_entry`/`restore_project_entry`/`add_project_entry`
  (WorkflowEntry objects), registered in `_default_entries`; module comment
  documenting the `list_projects` collision.
- `tests/test_architecture_enforcement.py` — `TestUnarmedAskSiteRatchet`:
  `_handle_portfolio_query` row shrunk 11→7; `test_scan_space_is_populated`
  floor lowered 40→35, both with dated comments.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py`
  — both change-detector tests (`test_allowlist_is_exactly_…`,
  `test_no_other_rail_entry_declares_a_key`) grown to include the three new
  keys.
- `tests/unit/services/intent_service/test_inversion_cross_family_release_1920.py`
  — new pins (registry-category + cross-family-release) for the three ops.
- `tests/unit/services/intent_service/test_portfolio_write_split_1595.py`
  (new file) — registration shape, CANONICAL disposition, EXECUTE
  classification, entry-point delegation (all three ops), missing-context
  → `None`, legacy-dispatch delegation (archive/restore), `list_archived`
  delegation, and the `list_projects` collision-survival regression guard.
- `docs/internal/architecture/current/intent-routing-stack.md` — new
  "`manage_portfolio` WRITE split" section.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — dated
  progress-log entry appended.
- `docs/internal/architecture/decisions/decisions.log` — dated entry
  appended.

No LLM calls. No flag/env/`CURRENT_LIVE_CATEGORIES`/deploy change. No new
`elif intent.action` dispatch branch (`MAX_DISPATCH_SITES` unchanged — every
shape above is an entry, never a branch). No new extraction regexes (all
project-name extraction reuses the EXISTING `ARCHIVE_PATTERNS`/
`RESTORE_PATTERNS`, just relocated into the hoisted methods).
`PORTFOLIO_PATTERNS` literals NOT touched (the dead update/edit claims are a
separate lane, per the dispatch's hard rule).

## Tests — all four required gates, final tails

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q ...
-> 12292 passed, 228 skipped, 3 deselected, 1 xfailed, 166 warnings in 246.43s

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -m "not llm" ...
-> 205 passed, 2 skipped, 93 deselected

env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY PYTHON_KEYRING_BACKEND=... venv/bin/python -m pytest
  tests/unit/services/intent_service/ tests/test_architecture_enforcement.py -q ...
-> 5131 passed, 3 deselected, 1 xfailed, 21 warnings in 135.08s

venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q ...
-> 45 passed — no ledger-verdict change; gate not patched.
```

`ruff check` + `ruff format --check` on every changed `.py` file: clean.

## Discovered work

None filed as a new GH issue — the `list_projects` naming collision is
reported in this log + the handback + the scope-doc entry for Lead/Arch to
rule on, not something I should unilaterally resolve by inventing a name.

## Memory & briefing surfaces referenced this session

**Referenced**: Arch's §2 ruling memo (the split + the four answered
questions); the effect inventory doc (branch-by-branch citations); the
prior `read_portfolio`/`complete_todo` lane logs (hoist shape, #1677
allowlist comment-block template, `TestExecuteVocabCoverage`'s existence
and scope); `test_inversion_cross_family_release_1920.py`'s existing
`test_cross_family_write_releases` (template for the new pin).

**Loaded but not referenced**: ROSTER.md, BRIEFING-CURRENT-STATE.md.

**Wanted but not found**: none.

## Verified how

Method: ran all four dispatch-specified pytest invocations verbatim (final
tails above), plus a temporary `git stash push -u`/`git stash pop`
round-trip to measure the TRUE before/after interrogative-literal count
(42 → 38) rather than assuming the delta, `ruff check`/`ruff format --check`
on every changed `.py` file, and a direct `grep` across `tests/` for any
pin on the archive/restore not-found/no-name copy before changing it (none
found). Layer: unit-test + static-tool layer (no live LLM calls, no server
restart, no manual chat-path click-through). Denominator: 4/4 required
gates run and green; 3/3 new WRITE ops built per Arch's four-question
ruling, 1/4 split ops (`list_projects`) explicitly NOT built and reported;
all `.py` files `git status --short` lists as modified/new, ruff-clean.
