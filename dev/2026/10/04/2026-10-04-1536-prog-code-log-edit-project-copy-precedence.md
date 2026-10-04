# 2026-10-04 15:36 — Coding Agent (prog) — edit-project copy + precedence fix

**Model**: Sonnet (dispatched by Lead, Sonnet tier)
**Role**: Coding Agent (prog), one-shot dispatch, no own session log beyond this entry per lane rules.
**Repo**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Authority**: CXO's ruling, `mailboxes/lead/inbox/rule-cxo-to-lead-cc-arch-ppm-edit-project-honest-copy-notfound-copy-ok-1930-still-live-2026-10-04.md` §2.

## Task

CXO's §2, two parts (plus one optional):
1. Rename `edit_unavailable` action → `edit_project_unavailable`; copy → CXO's verbatim, no "yet":
   "I can't edit a project's details from chat. I can show, add, archive, restore, and search your projects."
2. Precedence: the edit/update sniff in `_handle_portfolio_query` (`services/intent_service/canonical_handlers.py`)
   must claim the turn BEFORE the archive/delete/restore/list/add/search operation sniffs, so a message
   carrying both an edit verb and a co-occurring literal (e.g. "add") can't be misrouted.
3. (Optional) add "Add a project" to the `portfolio_help` fallback menu since add is wired.

## What landed before this dispatch (context)

Commit `5d8ec5c1a3` ("product(portfolio, todos): the delete/edit copy stops promising…") had already
added the edit/update branch, but as the LAST operation-detection check (after list/add/search), with
action `edit_unavailable` and copy "I can't edit projects yet. I can archive, restore, add, or search
projects instead." — differing from CXO's spec on both copy and precedence.

## Changes

### 1. Copy + action rename (`services/intent_service/canonical_handlers.py`)

Before:
```python
"message": (
    "I can't edit projects yet. I can archive, restore, "
    "add, or search projects instead."
),
...
"action": "edit_unavailable",
```

After:
```python
"message": (
    "I can't edit a project's details from chat. I can "
    "show, add, archive, restore, and search your "
    "projects."
),
...
"action": "edit_project_unavailable",
```

### 2. Precedence — moved the sniff to run FIRST

The update/edit detection block used to be the LAST `if not operation:` check (after archive, delete,
restore, list, add, search). Moved it to be the FIRST check, immediately after `operation = None` /
`project_name = None` is initialized, and BEFORE the archive-pattern loop (which previously ran
unconditionally and had to be wrapped in `if not operation:` to make this safe).

Where it now sits vs. every other sniff (post-edit line numbers in
`services/intent_service/canonical_handlers.py`):

| Order | Check | Line (approx, post-edit) |
|---|---|---|
| 1st | **update/edit (leading-verb)** | ~4385 |
| 2nd | archive (`ARCHIVE_PATTERNS`, now guarded by `if not operation:`) | ~4421 |
| 3rd | delete (`DELETE_PATTERNS`) | ~4455 |
| 4th | restore (`RESTORE_PATTERNS`) | ~4466 |
| 5th | list/show / list_archived | ~4477 |
| 6th | add/create | ~4494 |
| 7th | search | ~4499 |

Dispatch (the `if operation == "..."` branches that actually return) is unaffected in relative order —
since `operation` is a single mutually-exclusive value set once by the first matching detection block,
only the detection ORDER matters for precedence, not the dispatch-branch order. Verified this is in fact
true by the test suite (see Tests below).

### 3. The sniff rule itself — leading-verb, not bare substring

Old condition: `any(word in message_lower for word in ["update", "edit"]) and "project" in message_lower`
— a bare substring check anywhere in the message.

New condition:
```python
_leading_tokens = message_lower.split()
if (
    _leading_tokens
    and _leading_tokens[0] in ("update", "edit")
    and "project" in message_lower
):
    operation = "update"
```

**Why**: moving the check to run first on its own creates a NEW false positive that didn't exist before —
a bare substring check would now claim "add a project to update later" (a genuine add request that just
happens to mention "update" downstream) as an edit/update ask, which is worse than the pre-existing
ordering bug. The leading-verb requirement (edit/update must be the message's first token) fixes this:
it still catches every true case (all of them lead with the verb) while letting "add a project to update
later" fall through to the add check, since "add" — not "update" — is the first token.

**Phrases tested** (all pinned in
`tests/unit/services/intent_service/test_portfolio_edit_literals_1933.py::TestEditUpdatePrecedence`):

| Phrase | Leading token | Expected | Result |
|---|---|---|---|
| `edit my project description` | `edit` | `edit_project_unavailable` | ✅ true positive |
| `update my project name to Atlas` | `update` | `edit_project_unavailable` | ✅ true positive |
| `edit my project and add a note` | `edit` | `edit_project_unavailable`, never reaches add | ✅ precedence case |
| `update my project` / `update the project` / `edit my project` / `edit the project` | `update`/`edit` | `edit_project_unavailable` | ✅ (pre-existing pins, re-verified) |
| `add a project called Foo` | `add` | reaches `_handle_add_project`, NOT edit_project_unavailable | ✅ true negative, unaffected |
| `archive my project Foo` | `archive` | reaches `_handle_archive_project`, NOT edit_project_unavailable | ✅ true negative, unaffected |
| `add a project to update later` | `add` | reaches `_handle_add_project`, NOT edit_project_unavailable | ✅ false-positive case, avoided |

For the add/archive "unaffected" pins, `_handle_add_project` / `_handle_archive_project` were mocked
(`AsyncMock`) rather than run against a real DB — the test only needs to confirm the operation sniff
routes to them and doesn't short-circuit into the edit floor; full DB-backed behavior for those paths is
already covered elsewhere (`test_add_project_initiation_args_1856.py`, `test_portfolio_write_split_1595.py`,
`test_portfolio_delete_copy_1930.py`).

**Decision**: leading-verb (first token), not "adjacent to the word 'project'" — adjacency fails the true
positives themselves. "edit my project description" and "update my project name to Atlas" both have a
word ("my") between the verb and "project", so an adjacency rule would have rejected the very cases CXO's
ruling needs caught. Leading-verb catches all required true positives and rejects the one false positive
named in the brief, with no new pre_classifier regex — still a plain in-handler string/list check.

### 4. Optional: `portfolio_help` menu gains "Add a project"

Added as the LAST bullet (not reordered in), so the `TestUnarmedAskSiteRatchet` fingerprint (first 60
normalized chars of the literal: `"I can help you manage your projects. You can ask me to: - Sh"`) is
unchanged — verified by direct string comparison before writing the edit. Confirmed via the architecture
enforcement test run below (no ratchet failure).

### 5. Test file updated

`tests/unit/services/intent_service/test_portfolio_edit_literals_1933.py`:
- Updated existing assertions for the new copy/action name.
- Added `TestEditUpdatePrecedence` (7 new test methods) covering all pins above.

## Files changed

- `services/intent_service/canonical_handlers.py` — moved + rewrote the update/edit sniff, renamed the
  action, replaced the copy, added "Add a project" to the `portfolio_help` fallback, docstring update.
- `tests/unit/services/intent_service/test_portfolio_edit_literals_1933.py` — updated assertions for new
  copy/action; added precedence pin tests.

Both ran through `ruff format` + `ruff check` (clean).

## Test tails

Targeted file:
```
13 passed in 0.38s
```

Portfolio/intent cross-check (16 files, 261 tests):
```
261 passed, 12 warnings in 11.51s
```
(warnings are pre-existing `AsyncMockMixin._execute_mock_call was never awaited` noise in unrelated
soft-invocation/inversion tests, not from this change.)

Full `tests/unit` + `tests/test_architecture_enforcement.py` (ran in background, 4m18s — concurrent with
another lane's own full-suite run against the same DB port, hence the runtime):
```
12393 passed, 228 skipped, 3 deselected, 1 xfailed, 171 warnings in 258.07s (0:04:18)
```
No `FAILED` lines (grep for `^FAILED|[0-9]+ passed` matched only the summary line).

`tests/intent/`:
```
205 passed, 2 skipped, 93 deselected, 52 warnings in 28.87s
```

`ruff check` + `ruff format --check` on both changed files: clean (ran `ruff format` then `ruff check`,
both passed with no remaining diffs).

## Scope discipline

No `git add`/commit/push. No LLM calls. No edits to `services/intent_service/pre_classifier.py`,
`tests/test_architecture_enforcement.py`, the corpus, `scripts/check_autoclose_keywords.py`, or
`.claude/hooks` — confirmed by `git status` / `git diff --name-only` before handback.
