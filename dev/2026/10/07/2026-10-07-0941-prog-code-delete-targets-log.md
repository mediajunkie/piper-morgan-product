# Session log — Coding Agent (prog-code) — delete_todo router targets

**Date**: 2026-10-07 (Pacific)
**Role**: Coding Agent (prog)
**Model**: Claude Sonnet 5 (model ID `claude-sonnet-5`)
**Worktree**: `/Users/xian/Development/piper-morgan-product/.claude/worktrees/agent-a3e4edde46437c509` (branch `worktree-agent-a3e4edde46437c509`)
**Task**: GitHub #1943 follow-on — "clear family" build plan piece 1
(`dev/2026/10/07/clear-family-resolver-build-plan-2026-10-07.md`): teach
`delete_todo` to consume router-extracted targets the way `complete_todo`
already does.
**Dispatched by**: Lead Dev subagent dispatch (tier not stated to me in the
prompt; recording per the model I observe — Sonnet 5 — per the log-the-tier
convention).

## Read first

- `dev/2026/10/07/clear-family-resolver-build-plan-2026-10-07.md` — the
  build plan; piece 1 is this session's scope. Piece 2+ (the `clear_todos`
  resolver rail entry, corpus run, retirement of `detect_clear_family_ask`)
  is explicitly out of scope and gated on PM's API-cost ruling (Decision F).
- `services/intent_service/todo_handlers.py` — `handle_complete_todo_targets`
  (#1943) and its supporting module-level helpers (`resolve_router_targets`,
  `_router_target_tokens`, `_is_positional`, `_collapse_titles`,
  `_title_phrase`, `_leaving_line`, `_batch_confirm_question`,
  `_batch_summary`), and `handle_delete_todo` (~line 1583, the #1666
  rail-confirmed single delete this new path sits in front of).
- `services/intent_service/workflow_entries.py` — `run_complete_todo_workflow`
  (how `handle_complete_todo_targets` is hooked before the legacy handler)
  and `run_delete_todo_workflow` (where the new hook had to land — after the
  existing `_rc.maybe_handle_clear_family` and
  `_rc.maybe_handle_explicit_bulk_delete` seams, before
  `todo_handlers.handle_delete_todo`).
- `services/intent_service/destructive_confirm.py` — the #1190 carrier
  (`CONFIRM_PENDING_ACTION_WORKFLOW`, `CONFIRMED_CONTEXT_KEY`) and the
  existing `TodoDeleteGate`/`build_todo_delete_confirmation` single-delete
  gate (#1666) that `handle_delete_todo` still owns when the router names no
  targets.
- `tests/unit/services/intent_service/test_complete_todo_router_targets_1943.py`
  — the test shape to mirror.

## What was built

1. **Shared, verb-parametrized string helpers** in `todo_handlers.py`:
   - `_confirm_question(verb, targets, left, *, one_item_template=None)` —
     the shared body of the enumerating #1190 confirm. `_batch_confirm_question`
     (complete_todo) now delegates to it with `verb="Complete"`, no
     `one_item_template` (complete_todo never reaches n==1 on this path — a
     single resolved item completes directly, no confirm). New
     `_delete_confirm_question` delegates with `verb="Delete"` and
     `one_item_template='Delete the reminder "{title}"?'` — the n==1 branch
     delete needs because delete is DESTRUCTIVE and always confirms, even
     for one item.
   - `_mutation_summary(verb_past, header_suffix, none_header, fail_verb,
     fail_suffix, done, failed, left)` — the shared body of the post-"yes"
     summary. `_batch_summary` (complete_todo) delegates to it unchanged;
     new `_delete_summary` delegates with "Deleted" / "Deleted nothing:" /
     "delete" / `fail_suffix=""` (no "done" clause) and the "already gone"
     reason is passed by the caller, parallel to complete's "no longer
     there".
   - New `_delete_decline_message(targets)` — CXO strings D5/D6 (the
     Okay-family decline, naming the one title at n==1, else the count).
   - Verified by direct assertion in the new test file that refactoring
     `_batch_confirm_question`/`_batch_summary` into the shared helpers did
     **not** move complete_todo's pinned strings (`test_complete_todo_
     strings_unchanged_by_the_refactor`, plus the full existing 1943 test
     file still passes unchanged).

2. **New carrier keys**: `BATCH_DELETE_IDS_KEY`, `BATCH_DELETE_TEXTS_KEY`,
   `BATCH_DELETE_LEFT_KEY` — delete's own keys on the #1190 pending-action
   record, kept separate from the complete batch keys (both colliding on one
   key would be a problem for the future `clear_todos` resolver, which binds
   either verb).

3. **`TodoIntentHandlers.handle_delete_todo_targets`** — mirrors
   `handle_complete_todo_targets` structurally (confirmed re-entry branch →
   candidate-pool resolution → unresolved-reply branch → exclude-filter →
   confirm-arm branch), with these deliberate departures:
   - **No single-item fast path.** Delete is DESTRUCTIVE in every consent
     cell (Arch's ruling, carried from #1666) — even one resolved target
     with no carve-out arms the confirm; nothing executes in the same turn
     it was named.
   - **Unresolved reply**: identical head-line logic to complete_todo
     ("There's no number N in your X. You have N:" / "I couldn't find
     \"name\" in your X. You have:"), with the empty-`picked` tail changed
     from "Tell me which one, and I'll mark it done." to "Tell me which
     one, and I'll delete it." — the only vocabulary change, no added verb
     clause (the verb is already unambiguous: delete).
   - **Confirmed re-entry**: deletes `self.todo_service.delete_todo` for
     exactly the ids bound onto `BATCH_DELETE_IDS_KEY` at ask time — never
     re-reads `inversion_args`. Verified behaviorally in
     `test_confirmed_reentry_deletes_exactly_the_bound_ids`, which sets
     `list_todos` to raise if called, so the test fails loudly if the
     implementation ever re-resolves instead of using the bound ids.
   - **Pending-offer record**: `kind: "todo_batch_delete"`,
     `action: "delete_todo"`, `decline_message` from
     `_delete_decline_message`.

4. **Hook in `run_delete_todo_workflow`** (`workflow_entries.py`): placed
   after the existing `_rc.maybe_handle_clear_family` and
   `_rc.maybe_handle_explicit_bulk_delete` seams (so #1605/#1696 keep first
   claim on clear-family and bulk-imperative phrasings, unchanged), before
   the legacy `todo_handlers.handle_delete_todo` call — the exact placement
   `run_complete_todo_workflow` uses for its own `#1943` hook. Returns the
   same `IntentProcessingResult` shape (`router_targets: True`,
   `destructive_confirmation_pending` + `requires_clarification` mirroring
   the `armed` flag).

5. **No catalog change.** `git diff --stat` confirms no `description=` text
   moved in `workflow_entries.py` (and `action_registry.py` was untouched).
   The handler only consumes `inversion_args` when the router already sends
   it — nothing here requires a corpus run.

## Rendered outputs (CXO wants real output, not code)

Ran directly against the committed `_delete_confirm_question`:

**1 item:**
```
Delete the reminder "review the pr"? (yes/no)
```

**3 items, one duplicate title, one carve-out** (`_delete_confirm_question`
called with `["check the test card again", "check the test card again",
"review the pr"]`, left=`["revise the pr"]`):
```
Delete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)
```

**7 items** (no carve-out):
```
Delete 7 reminders?
• t0
• t1
• t2
• t3
• t4
• t5
• t6
(yes/no)
```

(Full end-to-end renders, including the leaving-line variant for a 7-item
case and the post-"yes" `_delete_summary` output, are asserted in
`tests/unit/services/intent_service/test_delete_todo_router_targets.py`.)

## Test environment note

This worktree (`.claude/worktrees/agent-a3e4edde46437c509`) has no local
`venv/`. Ran tests/ruff via the `venv/bin/python` at
`/Users/xian/Development/piper-morgan-worktrees/lead/venv` (same repo,
different worktree checkout) with `cwd` set to this worktree so paths/rootdir
resolve against the code actually under test here.

## Acceptance evidence

**Verified how**: ran the exact commands below this session, this turn,
against the committed diff; quoting their actual output (not a prior run).

```
$ venv/bin/python -m pytest tests/unit/services/intent_service tests/test_architecture_enforcement.py tests/test_completion_ratchets.py -q -p no:cacheprovider -rf
...
5317 passed, 1 skipped, 1 xfailed, 29 warnings in 170.48s (0:02:50)
[exited with code 0]
```
(Also ran `tests/unit/services/intent_service` alone and
`test_delete_todo_router_targets.py` + `test_complete_todo_router_targets_1943.py`
alone — all green, no failures, no new skips/xfails beyond the pre-existing
1 skip / 1 xfail in the full intent_service slice.) No architecture-enforcement
ratchet moved — `TestPreFloorDispatchSiteRatchet`/binder-count tests are inside
the run above and passed unchanged; this change added no new dispatch-site
branch (it hooks the existing workflow-dispatcher entry) and no new regex
target binder.

```
$ venv/bin/ruff format --check services/intent_service/todo_handlers.py services/intent_service/workflow_entries.py tests/unit/services/intent_service/test_delete_todo_router_targets.py
Would reformat: services/intent_service/todo_handlers.py
Would reformat: tests/unit/services/intent_service/test_delete_todo_router_targets.py
```
→ ran `ruff format` (no `--check`) on those two files, then re-ran
`--check`: clean, 3 files already formatted. `ruff check` on all three
touched files: `All checks passed!`

```
$ git diff --stat
 services/intent_service/todo_handlers.py    | 290 ++++++++++++++++++++++++++--
 services/intent_service/workflow_entries.py |  28 +++
 2 files changed, 307 insertions(+), 11 deletions(-)
```
(plus the new untracked test file, now committed). `git diff -- services/intent_service/workflow_entries.py services/intent_service/action_registry.py | grep '^[+-].*description='` → no matches: no catalog/description text touched.

## Commit

`e598c56e7835cc8f32b97eaa69f988979a4412ca` on branch
`worktree-agent-a3e4edde46437c509` (this worktree, NOT pushed — per task
instructions, no push, no mailbox writes).

```
 services/intent_service/todo_handlers.py                                       | 290 +++++++++++++-
 services/intent_service/workflow_entries.py                                    |  28 ++
 tests/unit/services/intent_service/test_delete_todo_router_targets.py          | 422 +++++++++++++++++++++
 3 files changed, 729 insertions(+), 11 deletions(-)
```

## Discovered work

None filed. The one thing worth flagging for the Lead/Arch: this piece
leaves `handle_delete_todo`'s own #1666 gate (`TodoDeleteGate` /
`build_todo_delete_confirmation`) completely untouched as the fallback path
for when the router names no targets — exactly as scoped. No new issue
needed; the retirement of the regex-based single-delete gate (if ever
wanted) is explicitly out of this piece's scope and not mentioned in the
build plan as a near-term goal.

## Memory & briefing surfaces referenced this session

- **Referenced**: the build-plan doc (scope/ruling source for D1-D6 strings
  and the provenance rule); `test_complete_todo_router_targets_1943.py` (test
  shape + byte-identical-strings constraint); CLAUDE.md sign-off/worktree
  sections (no-push, no-mailbox task constraints; "Verified how" discipline
  applied above; dispatch-tier logging convention).
- **Loaded but not referenced**: the rest of CLAUDE.md (mailbox discipline,
  branch/worktree registry, GitHub gotchas) — not applicable, this was a
  scoped code-only dispatch with explicit no-push/no-mailbox instructions.
- **Wanted but not found**: nothing — the build plan and the 1943 test file
  were sufficient to mirror the mechanism without needing to read the CXO
  ruling memo directly (it's quoted verbatim in the build plan and the task
  prompt).

## Closed by the dispatching Lead (2026-10-08)
- Reviewed and landed by Lead 10-07 (merge 6083677204); CXO's single-target D1 fix followed (4ea71650df).
<!-- DAY-CLOSED: 2026-10-07 -->
