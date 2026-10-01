# 2026-10-01 1252 — prog (Coding Agent), Sonnet — #1914 complete_todo clause-boundary bug

Dispatched by Lead Developer. Worktree: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`). No git index touched per dispatch instructions — Lead owns commit.

## Task

GitHub #1914: PM live transcript (alpha v156, 2026-10-01 11:25 PT) — "Mark the first one complete and leave the second one pending." → `complete_todo`'s target extractor swallowed the whole tail ("and leave the second one pending.") as the completion target instead of stopping at the clause boundary, and "the first one" had no candidate list to bind against.

## Root cause (confirmed before writing any fix)

`TodoIntentHandlers._extract_completion_text` runs 5 regex patterns in order via `re.search` (not anchored to message start). For "Mark the first one complete and leave the second one pending.", pattern index 1 (`(?:complete|finish|done with)\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)`) matched mid-string at the bare word "complete" (not the "Mark ... complete" structure), and its lazy capture had nothing to stop at except end-of-string — so it captured "and leave the second one pending." verbatim, including the trailing period. Confirmed by hand-tracing the regex and by `git log`/issue text match.

## Fix — two bounded pieces, both in `services/intent_service/todo_handlers.py`

**1. Clause-boundary split, applied BEFORE any extraction runs** (new module-level `_split_completion_clause`, `_CLAUSE_JOINER_RE`, `_QUOTE_SPAN_RE`, `_in_quoted_span`):

- `_CLAUSE_JOINER_RE` matches an unquoted `and` / `and then` / `but` / `then` immediately followed (via lookahead) by a no-op/imperative verb: `leave`, `keep`, `don't`/`do not`, `skip`, `ignore`, `wait(on)`, `hold off (on)`, `stop`. Deliberately narrow — an "and" followed by anything NOT in this list is left alone, because it may be part of the todo's own text.
- Before accepting a boundary, `_in_quoted_span` checks the match start isn't inside a quoted span (`_QUOTE_SPAN_RE`, same shape as `reminder_clear`'s named-target regex). A quoted/named title containing "and" is never split.
- `handle_complete_todo` now computes `primary_message, noop_tail = _split_completion_clause(original_message)` up front and runs **both** the number-path (`_extract_todo_id`) and text-path (`_extract_completion_text`) extraction against `primary_message`, not `original_message`.
- Every return path in `handle_complete_todo` is wrapped in a local `_reply()` closure that appends `" Left the other one as is."` whenever `noop_tail` is truthy — the no-op clause is acknowledged once, on success or failure, never silently dropped and never acted on.

Verified by hand (not a guess): `_split_completion_clause("Mark the first one complete and leave the second one pending.")` → `("Mark the first one complete", "leave the second one pending.")`, and `_extract_completion_text("Mark the first one complete")` → `"first one"` (confirmed via a throwaway `venv/bin/python -c` probe before writing tests).

**2. Ordinal/positional binding via the #1906 binder, reused not reimplemented:**

- New `_ORDINAL_SHAPE_RE` (detection only: ordinal words or `#N`) decides whether to attempt position binding.
- New `TodoIntentHandlers._due_reminder_todos(user_id)` — same filter `get_due_reminders` applies (reminder_date set, not completed, `reminder_date <= now`), but returns the full `Todo` rows in list order instead of just text, so position binding has ids to act on. Kept separate from `get_due_reminders` rather than refactored into it — that method's error-path logging (`todo_count`, `reminders_considered`) is a distinct, already-depended-on contract; didn't want to risk it for an unrelated feature. A query failure fails open to `[]` (never a crash).
- When `completion_text` looks ordinal AND `_due_reminder_todos` returns a non-empty list (the floor's "flagging N reminders" copy renders from the exact same `get_due_reminders`/`list_todos` filter), `handle_complete_todo` imports `reminder_clear._resolve_pick_target` (lazy import, matching this module's existing style) and binds by position over `[t.text for t in due_candidates]` / `[_reminder_due_iso(t) for t in due_candidates]`. On `("bound", idx)` it uses `due_candidates[idx]` directly — no re-fetch, no re-resolve.
- If ordinal-shaped but `_due_reminder_todos` is empty, skip straight to a tailored clarify: `"I couldn't find a todo matching '{completion_text}' — I don't have a list to count against right now. Try 'show my todos' to see the numbers, then 'complete todo 1'."` — per dispatch instructions, this keeps the honest clarify shape but points the copy at the ordinal form that actually works.
- If ordinal binding doesn't resolve (empty due list, or `_resolve_pick_target` returns `ambiguous`/`none`), falls through to the existing fuzzy `_find_best_matching_todo` unchanged — no behavior change for any non-ordinal, non-clause-boundary message.

No reimplementation of ordinal/status/name binding logic — `_resolve_pick_target`, `_ordinal_index`, `_overdue_status`, `_name_index` in `services/intent_service/reminder_clear.py` are untouched, only imported.

## Extraction-ratchet scope check (explicit, per dispatch instructions)

This is argument extraction **inside the `complete_todo` action handler** (an already-claimed execution surface), not a new pre-classifier pattern or corpus-deposit candidate — `TestExtractionPatternRatchet` in `tests/test_architecture_enforcement.py` governs pre-classifier/routing-layer pattern growth, not handler-internal regex. Ran the full architecture-enforcement suite (below) — it passed with no ratchet-count change, confirming this reading rather than asserting it from memory.

## Tests

New file: `tests/unit/services/intent_service/test_todo_completion_clause_split_1914.py`

- `TestSplitCompletionClause` (pure helper, 6 tests): the PM transcript exactly; `but` without `and`; number-based target with tail; quoted title containing "and leave..." NOT split (proves the quote-span guard does real work, not just coincidence); the task-card's own `"review the PR and ship it"` example (pinned separately since "ship" was never a trigger verb — guards against a future verb-vocabulary widening regressing it); plain message with no boundary.
- `TestCompleteTodoClauseSplitAndOrdinalBinding` (handler-level, mocked `todo_service`, same idiom as #904's `test_todo_completion_lifecycle.py`):
  - PM's exact utterance → completes the first due-reminder candidate by id, never calls `complete_todo` on the second, reply contains "left the other one as is", names the completed todo, never names the untouched one.
  - `"complete the last one"` → binds to the final due candidate.
  - `"complete #2"` → binds by position via the hash-number form.
  - Quoted title with "and" → not split, still resolves via fuzzy matching, no tail-ack in reply.
  - Ordinal with zero due candidates → honest clarify, copy names `'complete todo 1'`, `complete_todo` never called.
  - Plain "complete the PR review" (#904 regression guard) → unaffected, no tail-ack.

## Gate results

`ruff format` — 1 file reformatted (`todo_handlers.py`, a line-wrap on `_ORDINAL_SHAPE_RE`), re-ran tests after to confirm no behavior change.
`ruff check --fix` — All checks passed, no fixes needed beyond format.

```
venv/bin/python -m pytest tests/unit/services/intent_service/test_todo_completion_clause_split_1914.py \
  tests/unit/services/intent_service/test_todo_completion_lifecycle.py \
  tests/unit/services/intent_service/test_reminder_clear_pick_target_1906.py -q
63 passed in 2.75s
EXIT 0

venv/bin/python -m pytest tests/unit/services/intent_service/ tests/unit/services/intent/ -q
5032 passed, 16 warnings in 135.48s
EXIT 0

venv/bin/python -m pytest tests/test_architecture_enforcement.py -q
63 passed, 1 xfailed in 11.82s
EXIT 0

venv/bin/python -m pytest tests/integration/test_todo_complete_chat_path_1603.py -q
3 passed in 0.95s
EXIT 0
```

**Verified how:** every count/exit-status line above is quoted from a test run executed this turn (not recalled from an earlier check); the clause-split and extraction behavior were hand-verified via `venv/bin/python -c` probes against the actual module before any test was written (quoted in the body above), not assumed from reading the regex. Layer: these are unit/handler-level tests against `TodoIntentHandlers` with `todo_service` mocked (same idiom as the pre-existing #904 suite) plus one integration test (`test_todo_complete_chat_path_1603.py`) exercising the chat path — no live LLM call anywhere in this change (dispatch required NO LLM calls; none were made — the fix is pure regex + the existing deterministic `_resolve_pick_target` binder). Denominator: ran the full `tests/unit/services/intent_service/` + `tests/unit/services/intent/` trees (5032 tests) plus the architecture-enforcement suite (64 tests) plus the one directly-relevant integration file — not a narrowed subset.

## Files touched

- `services/intent_service/todo_handlers.py` — clause-split helpers, ordinal-shape detector, `_due_reminder_todos`, rewritten `handle_complete_todo`.
- `tests/unit/services/intent_service/test_todo_completion_clause_split_1914.py` — new.

## Discovered work

None filed. Pre-existing, unrelated working-tree modifications were observed in `tests/fixtures/inversion_corpus_phase0.yaml` and `tests/unit/test_inversion_phase3_deletion_1595.py` at session start — both on the dispatch's explicit do-not-touch list (concurrent lane's work-in-progress). Not touched, not investigated further; flagging for Lead's awareness only.

## Memory & briefing surfaces referenced this session

**Referenced:**
- GitHub issue #1914 body — root cause framing, scope split (extractor = Lead, floor-arming = CXO/out of scope).
- `services/intent_service/reminder_clear.py` module docstring + `_resolve_pick_target`/`_ordinal_index`/`_overdue_status`/`_name_index` — the #1906 binder, reused verbatim per dispatch instruction.
- `services/intent_service/todo_handlers.py` existing `_extract_completion_text`/`_find_best_matching_todo`/`get_due_reminders` — read in full before extending, per "Verify First, Create Second."
- `tests/unit/services/intent_service/test_todo_completion_lifecycle.py` (#904) — test idiom (mocked `todo_service`, `Intent(...)` construction) followed for the new test file.

**Loaded but not referenced:** `docs/internal/architecture/current/intent-routing-stack.md` §armed offers was named in the dispatch as read-first; the actual fix turned out to be handler-internal extraction + a direct reuse of an existing binder, not a routing-stack change, so the doc's armed-offer mechanics weren't load-bearing for the final diff.

**Wanted but not found:** nothing — the dispatch's pointers (todo_handlers.py, reminder_clear.py, the two test files) were sufficient.
