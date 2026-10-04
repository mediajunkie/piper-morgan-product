# 2026-10-04 08:28 — prog (Coding Agent) — #1595 Phase 3: complete_todo rail entry

Model: Sonnet. Dispatched by Lead (lead role, worktree `claude/lead-cycle`).

## Task

Build a rail entry + #1677 allowlist admission for `complete_todo` (EXECUTION,
verb COMPLETE, previously no WorkflowEntry at all), per Arch's ruling
`mailboxes/lead/read/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-wave2-and-writes-2026-10-03.md`
§4. NOT flipped (no live-category / flag change).

## Step 1 — effect class from the handler: WRITE

`todo_handlers.handle_complete_todo` (todo_handlers.py:994-1117) calls
`self.todo_service.complete_todo(todo_id=…, user_id=…)` (line 1102) →
`TodoManagementService.complete_todo` (todo_management_service.py:240) →
`TodoRepository.complete_todo` (todo_repository.py:330-354), which sets
`status=COMPLETED`, `completed=True`, `completed_at=now()` — an UPDATE on the
existing row, nothing deleted. `TodoRepository.reopen_todo` (:356-378) /
`TodoManagementService.reopen_todo` (:272) reverse every one of those fields.
The row stays selectable via `list_todos(include_completed=True)` (the
`list_completed_todos` action, action_mapper.py:85). Reversible status flip
→ **WRITE**, never DESTRUCTIVE, per Arch's handler-read test.

Caveat noted, not blocking: `reopen_todo` exists at the service/repo layer but
is NOT wired to any chat action today — grep-verified zero hits for
`reopen_todo` in `services/intent_service/` or `services/intent/`. A user
cannot currently say "reopen todo 3." This is a chat-affordance gap, not a
handler-behavior question — Arch's test is about what completing DOES to the
row, and the data-layer answer (status flip, not deletion) is unambiguous.
Flagging as a discovered-work candidate for Lead to action separately.

## Step 2 — #1677 conditions

1. **Registered** — added `complete_todo_entry` to `get_action_workflows()`
   with `action_triggered=True`; alias family from ActionMapper
   (action_mapper.py:93-96): `complete_todo` / `finish_todo` /
   `mark_complete` / `mark_done`, all canonicalizing to `complete_todo` —
   matches ACTION_REGISTRY's canonical (action_registry.py:210/437).
2. **Effect correct by behavior** — see Step 1 above; read from
   `todo_handlers.py` / `todo_management_service.py` / `todo_repository.py`,
   not a docstring.
3. **Reaches consent** — `needs_consent` derives True (WRITE) and the rail's
   consent block (`_dispatch_action_rail`, intent_service.py ~L15901-15916)
   DOES evaluate it via `consent_gate.evaluate_consent`. **This condition is
   technically satisfied but surfaces a severe, pre-existing gap — see
   BLOCKING FINDING below.**

## BLOCKING FINDING — do not flip/merge as-is

Wiring `complete_todo` onto the #1509 WRITE-consent rail, exactly as
specified, breaks the single most natural phrasing for completing a todo.

**Root cause**: `collaboration_gate.classify_framing`'s `_EXECUTE_RE` verb
list (collaboration_gate.py:133-141) is
`create|file|open|make|add|submit|log|update|change|set|edit|modify|rename|comment|reply|post|remind|use|append|assign|schedule|mark|move`.
It contains **"mark" but not "complete," "finish," "done," or "clear."** Any
`complete_todo`-classified message that doesn't start with "mark" (e.g.
**"complete my hydrate reminder," "complete todo 1"**) classifies as
AMBIGUOUS framing, not EXECUTE. Under the default (non-execute) WorkingMode,
`decide_consent` returns COLLABORATE for WRITE+AMBIGUOUS, which arms a
generic `consent_check` held turn (intent_service.py ~L16000-16010) instead
of completing immediately — and, for the #1605 clear-family candidate-WRITE
guess ("clear my reminders" classified as `complete_todo`), it preempts the
`maybe_handle_clear_family` seam inside `run_complete_todo_workflow` entirely
(that seam never runs because the generic consent-check returns first).

The DESTRUCTIVE tier already solved the clear-family half of this problem:
`destructive_confirm.build_todo_delete_confirmation` (destructive_confirm.py
~L506-514) explicitly detects a clear-family ask and passes through
(`offer=None`) so `run_delete_todo_workflow`'s own `maybe_handle_clear_family`
keeps first claim. **No equivalent bypass exists on the WRITE/COLLABORATE
path** — the nearest analog, `collaboration_gate.is_draft_collaboration_action`
/ `DRAFT_COLLABORATION_ACTIONS` (intent_service.py ~L16004, collaboration_gate.py:82-102),
is scoped to the create-issue draft family and doesn't cover `complete_todo`.

**Evidence** (confirmed via direct test runs against this diff):
- `tests/unit/services/intent_service/test_reminder_delete_live_emission_1527.py::TestPmProbeRoundPhrasings::test_complete_probe_phrasing_still_completes_no_confirm` —
  "complete my hydrate reminder" now gets held (consent_check) instead of
  completing. This is NOT a clear-family edge case — it's the plain
  completion probe, proving the regression is general, not limited to
  "clear"-verb ambiguity.
- `test_reminder_clear_verb_anchor_1653.py`, `test_reminder_clear_verb_1605.py`,
  `test_reminder_clear_pick_target_1906.py`, `test_soft_offer_survival_clobber_1753.py` —
  50 failures total, every one traced to the same root: the `_arm_verb_question`
  helper (or equivalent) stubs classification of a clear-family message as
  `complete_todo`, expecting `maybe_handle_clear_family`'s
  `CLEAR_VERB_QUESTION_KIND` / `CLEAR_CORRECTION_KIND` offer to arm; instead
  the generic rail consent-check arms (`kind == "consent_check"`).

**Why I did not fix this myself**: the fix is a shared-infrastructure change
(either widen `collaboration_gate._EXECUTE_RE`'s verb vocabulary — a
framing-classification change affecting every current and future WRITE rail
entry, not just this one — or add `complete_todo` to a new bypass-to-handler
set analogous to `DRAFT_COLLABORATION_ACTIONS`/`is_draft_collaboration_action`).
Either is a policy/architecture call outside "build a rail entry for
complete_todo," and CLAUDE.md's STOP conditions direct me to escalate rather
than decide this myself ("Tests fail for any reason" / "ADR conflicts with
approach" — #1509/#1510 is Arch/PPM-ruled). Recommend Lead route this to Arch:
the two candidate fixes above, Arch's call on which.

**I did NOT revert the build** — the WorkflowEntry, entry point, and
allowlist addition are architecturally correct per Arch's three conditions as
literally stated, and are needed regardless of which fix is chosen. I did
update two **intentional change-detector** tests in
`test_inversion_write_allowlist_1677.py` (`test_allowlist_is_exactly_…` and
`test_no_other_rail_entry_declares_a_key`) to include `complete_todo` — those
are mechanical enumeration assertions designed to be touched on every
addition (per their own docstrings), unrelated to the regression.

## Step 3 — build

Files changed:
- `services/intent_service/workflow_entries.py` — added
  `run_complete_todo_workflow` (entry point, carries the removed elif's exact
  body: principal coercion, #1605 clear-family seam at candidate effect
  WRITE, `handle_complete_todo`); added `complete_todo_entry` WorkflowEntry
  (effect=WRITE, outwardness=PRIVATE, action_triggered=True,
  flip_write_allowlist_key="complete_todo", no flip_group); registered
  `complete_todo` / `finish_todo` / `mark_complete` / `mark_done` aliases in
  `get_action_workflows()`.
- `services/intent_service/workflow_dispatcher.py` — added `complete_todo` to
  `FLIP_WRITE_ALLOWLIST`, with the three-conditions comment block (mirrors
  create_todo/delete_todo/set_default_repo precedent).
- `services/intent/intent_service.py` — removed the
  `elif mapped_action == "complete_todo":` branch (migration completion,
  #1666/#1685 precedent), replaced with an explanatory comment. Note: this
  branch was never counted by `TestPreFloorDispatchSiteRatchet`
  (`MAX_DISPATCH_SITES = 0`) since that ratchet's regex only matches
  `(?:if|elif) intent\.action in \[` — the `mapped_action == "..."` chain is
  a separate legacy surface — so no ratchet-target change was needed.
- `services/intent_service/unwired_writes.py` — updated the stale doc comment
  listing `complete_todo` as still on the elif chain.
- `tests/unit/services/intent_service/test_action_registry.py` — removed
  `complete_todo` from `_LEGACY_EXECUTION_ELIF_ACTIONS` (now `{"list_todos",
  "next_todo"}`) — it's migrated onto the rail, same pattern-commented
  precedent as create_todo/create_reminder/delete_todo.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py` —
  updated the two change-detector tests (allowlist-exactness,
  no-other-entry-declares-a-key denominator) to include `complete_todo`.

Registry disposition: `("EXECUTION", "complete_todo")` was already
`ActionDisposition.WORKFLOW` (action_registry.py:210) — verified via
`_true_disposition_for_registry_row`'s logic
(tests/unit/services/intent_service/test_action_registry.py:191-237): once
registered in `get_action_workflows()` with no `read_floor`/`read_floor_2`
flip_group, the oracle resolves WORKFLOW — matches, no drift. (Unlike the
PORTFOLIO lane Lead flagged, no CANONICAL correction was needed here.)

## #1920 cross-family note (inversion_live.py ~804-830)

`complete_todo`'s ACTION_REGISTRY category is EXECUTION — the SAME family
the cross-family release names explicitly as "the reminder carriers'" own
category. A same-family write declines release (`"same_family_write"`
reason), exactly like `delete_todo` already does — an armed reminder/todo
carrier still RE-ASKS rather than releasing for a completion phrase.
Registering this entry does not change that outcome: before this commit the
decline reason was `"not_rail_dispatchable"` (no entry existed); after, it's
`"same_family_write"` — the carrier never releases either way, only the
logged decline reason changes.

## Gate

`tests/unit/test_inversion_phase3_deletion_1595.py` — **45 passed**, no
`complete_todo` row exists in that ledger (grep-confirmed), no verdict
change. Did not patch the gate.

## Tests

- Targeted gate: 45 passed (above).
- `tests/intent/` (not -llm): **205 passed, 2 skipped, 93 deselected** — clean,
  no overlap with the regressed cluster.
- `tests/unit/ tests/test_architecture_enforcement.py` (not -llm): **52 failed
  → 50 failed** after fixing the two intentional change-detector tests;
  **12210+ passed**. The remaining 50 are the single BLOCKING FINDING above,
  isolated to 5 files: `test_reminder_clear_verb_anchor_1653.py`,
  `test_reminder_clear_verb_1605.py`, `test_reminder_clear_pick_target_1906.py`,
  `test_reminder_delete_live_emission_1527.py`,
  `test_soft_offer_survival_clobber_1753.py`.
- ruff check + format --check on all changed files: clean.

## Discovered work (for Lead to action; not filed as a GH issue by me — out
of scope for this unit, flagging per Discovered Work Discipline)

1. **BLOCKING**: `collaboration_gate._EXECUTE_RE` missing "complete" /
   "finish" / "done" (or a `complete_todo`-scoped bypass analogous to
   `DRAFT_COLLABORATION_ACTIONS`) — needs Arch's ruling before `complete_todo`
   can safely carry `action_triggered=True` on the rail.
2. **Non-blocking**: no chat-reachable "reopen todo" / "uncomplete" action
   exists despite the service/repo layer supporting it fully.

## Memory & briefing surfaces referenced this session

**Referenced**: Arch's §4 ruling memo (task scope + WRITE/DESTRUCTIVE test);
`workflow_dispatcher.py`'s FLIP_WRITE_ALLOWLIST comment block (three
conditions template, mirrored exactly); `workflow_entries.py`'s
create_todo_entry/delete_todo_entry (construction-site pattern mirrored);
`inversion_live.py`'s #1920 docstring (cross-family release note).

**Loaded but not referenced**: ROSTER.md, BRIEFING-CURRENT-STATE.md.

**Wanted but not found**: none.
