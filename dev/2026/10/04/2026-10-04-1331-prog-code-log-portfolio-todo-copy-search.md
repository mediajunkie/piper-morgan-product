# 2026-10-04 13:31 — prog (Coding Agent) — four units: delete copy (#1930), edit-literal honesty (#1933), complete_todo disambiguation (#1930 §1), search_projects READ (#1933 §1)

Model: Sonnet. Dispatched by Lead (lead role, worktree `claude/lead-cycle`).

## Task

Build four separately-landed units from CXO's and Arch's 2026-10-04 rulings:
- `mailboxes/lead/read/rule-cxo-to-lead-cc-arch-ppm-1930-copy-now-wire-later-1931-out-of-chat-ok-complete-no-shall-i-2026-10-04.md`
- `mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-list-projects-reuse-live-entry-edit-literals-stay-my-miss-1933-endorsed-2026-10-04.md`
- Context: `dev/2026/10/04/manage-portfolio-effect-inventory-2026-10-04.md`

Another lane was concurrently editing `scripts/inversion_phase3_deletion_gate.py` and
`tests/unit/test_inversion_phase3_deletion_1595.py` — not touched here (confirmed via
`git status` throughout: neither ever appeared in my diff).

## Unit 1 — delete copy (#1930 step 1, CXO's ruling §2)

**File:** `services/intent_service/canonical_handlers.py`, `_handle_portfolio_query`'s
`operation == "delete"` branch (now ~4652-4727) + the docstring (~4343-4349).

The live prompt said "Are you sure you want to delete 'X'? This action cannot be undone."
and armed `awaiting_confirmation` — but nothing anywhere ever reads that context back and
calls `PortfolioService.delete_project(confirmed=True)` (verified: no caller exists in
`services/`). The product was misreporting its own capability.

**What changed:** resolves the project first (existing `find_project_by_name`,
`include_archived=True`), then:
- **not found** — unchanged copy ("I couldn't find a project called '{name}'. Would you
  like me to list your projects?", `action: project_not_found`, unchanged per CXO: "Not
  found keeps today's copy").
- **found, already archived** — says so, does NOT re-offer archiving: *"'{name}' is
  already archived — it's off your active list. I still can't delete it from chat. Say
  'restore {name}' if you'd like it back as active."* `action: delete_unavailable`,
  `context: {already_archived: True}`.
- **found, active** — CXO's exact copy: *"I can't delete projects from chat yet. I can
  archive '{name}' instead: it leaves your active list and you can say 'restore {name}'
  to bring it back. Say 'archive {name}' if you'd like that."* `action:
  delete_unavailable`, `context: {already_archived: False}`.

Both found cases: `requires_clarification: False`, no `awaiting_confirmation`, no
`delete_confirm` action — arms nothing.

**Docstring fix (same commit):** the stale line `"Delete my project X" →
PortfolioService.delete_project()"` corrected to say delete is NOT supported from chat yet
and point at the branch below.

**Pins:** `tests/unit/services/intent_service/test_portfolio_delete_copy_1930.py` (7
tests) — never arms for any resolution outcome (found/active, found/archived, not
found), CXO's exact copy, already-archived doesn't re-offer, not-found copy unchanged,
docstring no longer makes the false claim.

#1930 step 2 (wiring delete through the #1190 DESTRUCTIVE tier) is CXO's named follow-up,
not built here.

## Unit 2 — edit/update literals kept, honest reply (#1933 §2, Arch's ruling)

**File:** `services/intent_service/canonical_handlers.py`, new operation-detection branch
(~4441-4457) + early-return (~4544-4565).

Arch's own prior ruling ("dead claims, delete the update/edit literals") was wrong — Lead's
surface-2 probe found deleting them sends "edit my project description" to
`update_document_query` 10/10 on both legs (a WRITE on the wrong object). The literals are
protective, not dead.

**What changed:** kept `PORTFOLIO_PATTERNS`' update/edit literals untouched (no
pre_classifier change). Added an in-handler keyword sniff — `any(word in message_lower for
word in ["update", "edit"]) and "project" in message_lower` — same shape as the existing
list/add/search sniffs (no new `TestExtractionPatternRatchet` hit). Sets
`operation = "update"`, which early-returns *"I can't edit projects yet. I can archive,
restore, add, or search projects instead."* — imperative, non-interrogative,
`requires_clarification: False`, `action: edit_unavailable`. #1932 tracks the real
capability; this is copy only.

**Pins:** `tests/unit/services/intent_service/test_portfolio_edit_literals_1933.py` (4
tests) — honest reply for 4 phrasings, arms nothing, non-interrogative, literals still
present in `PORTFOLIO_PATTERNS`.

## Unit 3 — complete_todo disambiguation (#1930 §1, CXO's ruling)

**File:** `services/intent_service/todo_handlers.py`, `handle_complete_todo`'s fuzzy-text
leg (~1079-1101).

CXO: an explicit completion of a named item deserves no "shall I?" (already true — not
touched), but an AMBIGUOUS text target (more than one plausible match) DOES ask which one —
disambiguation, not consent, separate from the #1190 gate. "Check what exists today, don't
build a new picker if one exists."

**What changed:** the fuzzy-text leg's single `self._find_best_matching_todo(...)` call
(which silently takes the top-scored match regardless of ties) is replaced with the SAME
resolver the delete gate already asks with — `resolve_named_todo_target`
(`destructive_confirm.py`'s named-target leg uses it too). A unique exact-word-set match
still collapses to one (behaviour-preserving for every single-match case the old call
already handled); `len(matches) > 1` now returns *"I found N todos matching '…': 1. "…",
2. "…". Which one should I complete? Try 'complete todo [number]'."* instead of silently
completing the top-scored one. `_find_best_matching_todo` itself is untouched (still
directly pinned by `test_delete_todo_named_target_1527.py`) — only the one call site in
`handle_complete_todo` changed.

Also re-verified, already true before this change (CXO's other two constraints): the
completion reply NAMES the todo it completed (`format_todo_completed_conscious`) and never
promises an undo from chat.

**Pins:** `tests/unit/services/intent_service/test_complete_todo_disambiguation_1930.py`
(4 tests) — ambiguous target asks which; unique-exact still completes without asking;
reply names the item; no undo promised.

**Ratchet check:** the new disambiguation string does not register as a new
`TestUnarmedAskSiteRatchet` holder — it doesn't END with `?` (continues "...Try 'complete
todo [number]'." afterward), the same shape `destructive_confirm.py`'s existing, unflagged
"Which one should I delete?" clarification already uses. Confirmed by running the full
ratchet suite (below) — no new row needed, none added.

## Unit 4 — search_projects, the READ fourth (#1933 §1, Arch's ruling)

**Files:** `services/intent_service/canonical_handlers.py` (new
`_handle_search_projects` method + early-return), `services/intent_service/
workflow_entries.py` (new `run_search_projects_workflow` + `search_projects_entry`,
registered under `"search_projects"`), `services/intent_service/workflow_dispatcher.py`
(`read_portfolio` group comment widened), `services/intent_service/action_registry.py`
(`("PORTFOLIO", "search_projects")`: CANONICAL + `ACTION_EXAMPLES`/`ACTION_DESCRIPTIONS`/
`ACTION_TO_VERB`).

Arch's ruling resolves the `list_projects` naming collision the earlier #1595 WRITE-split
unit reported blocking: **reuse the LIVE QUERY `list_projects` entry as the active list —
do NOT re-home it** (a re-home is a live behaviour change on alpha for zero gain, since
#1920 releases a router-named READ in any family regardless of registry category). Build
**`search_projects`** as the genuinely new op for the SEARCH branch instead.

**The hoist:** `_handle_portfolio_query`'s SEARCH branch is extracted into
`CanonicalHandlers._handle_search_projects(intent, session_id, user_id)` — same shape as
the archive/restore hoist (early-return before the session-scope block opens; the hoisted
method is now the ONLY place the search response is built, for both the legacy canonical
dispatch and the new rail op).

**One deliberate copy change** (not byte-identical, same #1856/archive/restore precedent):
the old "no results" copy ended "…Would you like to see all your projects?" — re-housing it
unchanged into the new method would have registered a NEW `TestUnarmedAskSiteRatchet`
holder (forbidden). Rewritten imperative: "…Say 'list my projects' to see what you have."
`_handle_portfolio_query`'s own `KNOWN_UNARMED_ASK_SITES` row (in
`tests/test_architecture_enforcement.py`) shrinks **7 → 5** in the same commit (the two
removed literals — message + offer_hint — leave that holder entirely; verified the
holder's representative fingerprint snippet is unchanged, since the surviving 5 literals'
alphabetically-first text was already first among the original 7).

**Rail entry:** `search_projects_entry` (`effect=READ`, `action_triggered=True`,
`flip_group="read_portfolio"`) — **joins `list_repos` in that EXISTING group, not a new
one** (Arch's exact words: "add search_projects to read_portfolio, with no re-home").
Registered in `_default_entries` under `"search_projects"`.

**Registry/group/collision check (as requested):**
- `("PORTFOLIO", "search_projects")`: CANONICAL — verified against
  `test_registry_disposition_matches_live_runtime`'s oracle (parametrized over
  `ACTION_REGISTRY`, passed in the full run below): PORTFOLIO is claimed WHOLE by
  `CanonicalHandlers.can_handle()`, same verified reasoning as `list_repos`/
  `archive_project`/`restore_project`/`add_project` — WORKFLOW would fail that oracle.
  `ACTION_TO_VERB["search_projects"] = Verb.LIST` (same verb as `list_repos`;
  `validate_verb_coverage()` requires every registry row to have one).
- `derive_routing_grammar()` collision: once the rail entry registers, `search_projects`
  is in `covered` (step 1 of the derivation), so the `ACTION_REGISTRY` row is correctly
  SKIPPED at step 2 (no duplicate catalog entry) — same mechanism already used by
  `list_repos`/`archive_project`/etc.
- Name collision check: `git grep -n "search_projects"` over
  `action_registry.py`/`workflow_entries.py`/`workflow_dispatcher.py`/`pre_classifier.py`
  returned nothing before this unit — the name was only a Python method name
  (`PortfolioService.search_projects`/`ProjectRepository.search_projects`, a different
  layer) and the `intent.action` VALUE this handler's own dict has returned since
  #675/#1762 — never previously a registry/rail KEY.
- **⚠️ Widening `read_portfolio` (an EXISTING, already-live flip_group) from one member to
  two is itself a live-behaviour-relevant change for list_repos too**: the prior PM gate
  token (08:07) covered `list_repos` alone. Per Arch's own memo, Exec/PM must re-run the
  Phase-2 gate on the served model and re-send the token naming BOTH members before
  flipping it. **Flagged here for Lead to relay to Exec/PM — not executed by this unit**
  (no flag/env/`CURRENT_LIVE_CATEGORIES` change made).
- Found and fixed a REAL pre-existing regression this widening tripped: `tests/unit/
  services/intent_service/test_read_portfolio_rail_1595.py::
  test_member_registers_as_a_read_entry_in_read_portfolio` asserted `read_portfolio`'s
  membership was EXACTLY `{"list_repos"}` — a deliberate, explicit-membership regression
  guard from the group's original build. Updated `MEMBERS` to `{"list_repos",
  "search_projects"}` and its comment, in the same commit as the widening (not a separate
  "fix a failing test" patch — the guard was doing its job correctly).

**Pins:** `tests/unit/services/intent_service/test_portfolio_search_projects_read_1595.py`
(11 tests) — registration shape, joins list_repos in the same group, CANONICAL
disposition, registered verb, entry-point delegation, missing-context → `None`,
legacy-dispatch delegation, the hoisted method's own read-only rendering (found/no-results/
no-user), non-interrogative no-results copy (message + offer_hint).

Not built: a `list_projects` op (Arch: reuse the live QUERY one).

## Files changed

- `services/intent_service/canonical_handlers.py`
- `services/intent_service/workflow_entries.py`
- `services/intent_service/workflow_dispatcher.py`
- `services/intent_service/action_registry.py`
- `services/intent_service/todo_handlers.py`
- `tests/test_architecture_enforcement.py` (KNOWN_UNARMED_ASK_SITES row, 7 → 5)
- `tests/unit/services/intent_service/test_read_portfolio_rail_1595.py` (MEMBERS widened)
- New: `tests/unit/services/intent_service/test_portfolio_delete_copy_1930.py`
- New: `tests/unit/services/intent_service/test_portfolio_edit_literals_1933.py`
- New: `tests/unit/services/intent_service/test_complete_todo_disambiguation_1930.py`
- New: `tests/unit/services/intent_service/test_portfolio_search_projects_read_1595.py`
- `docs/internal/architecture/current/intent-routing-stack.md` (new `manage_portfolio`
  section documenting all four units)
- `dev/2026/10/04/manage-portfolio-effect-inventory-2026-10-04.md` (dated addendum closing
  out open questions §5, items 1/3/4)

## Tests — all three required gates, final tails

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py \
  -q -p no:cacheprovider -m "not llm" -o addopts="--ignore=tests/archive --ignore=*/archive/* \
  --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ \
  --tb=short --import-mode=importlib"
-> 12359 passed, 228 skipped, 3 deselected, 1 xfailed, 166 warnings in 255.75s (0:04:15)

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -p no:cacheprovider -m "not llm" \
  -o addopts="--import-mode=importlib --tb=line"
-> 205 passed, 2 skipped, 93 deselected, 52 warnings in 31.72s

env -u ANTHROPIC_API_KEY -u OPENAI_API_KEY PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring \
  POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/ \
  tests/test_architecture_enforcement.py -q -p no:cacheprovider -m "not llm" \
  -o addopts="--import-mode=importlib --tb=line"
-> 5161 passed, 3 deselected, 1 xfailed, 21 warnings in 139.13s (0:02:19)
```

One real failure found and fixed mid-lane (not in the final tails above, since both runs
shown are POST-fix): the first full `tests/unit` run caught
`test_read_portfolio_rail_1595.py::test_member_registers_as_a_read_entry_in_read_portfolio`
— the pre-existing explicit-membership regression guard, correctly tripped by widening
`read_portfolio`. Fixed by updating its `MEMBERS` set (see Unit 4 above), re-ran clean.

`ruff check` + `ruff format --check` on every changed/new `.py` file: clean (one
`ruff format` pass needed on 4 files — `action_registry.py`, `workflow_entries.py`, and the
two delete-copy/search-projects test files — for with-statement parenthesization and line
wrapping; re-ran the affected tests after, still clean).

The other lane's two files (`scripts/inversion_phase3_deletion_gate.py`,
`tests/unit/test_inversion_phase3_deletion_1595.py`) were never touched — confirmed via
`git status --short` throughout the session; neither appears in this lane's diff.

## Discovered work

None filed as a new GH issue. The `read_portfolio` PM-gate-token staleness (Exec/PM must
re-run Phase-2 + re-send the token naming both members) is flagged in this log + the
routing-stack doc for Lead to relay — not something I should file or resolve unilaterally,
since it's a gate/token-ownership question for Exec/PM, not a code defect.

## Memory & briefing surfaces referenced this session

**Referenced**: CXO's #1930 ruling memo (exact copy requirements, three constraints on
complete_todo); Arch's #1933 ruling memo (search_projects group placement, the reversed
edit-literal ruling, the effect-aware-deletion rule); the effect inventory doc (branch
citations, open questions §5); the prior `#1595` portfolio-split lane log (hoist shape,
`_FakeScope`/`patch.object` test pattern, `KNOWN_UNARMED_ASK_SITES` shrink precedent);
`test_portfolio_write_split_1595.py` and `test_read_portfolio_rail_1595.py` (structure to
mirror for the new pins, and the regression this lane had to fix in the latter);
`destructive_confirm.py`'s `build_todo_delete_confirmation` (the disambiguation shape to
reuse for complete_todo, verbatim).

**Loaded but not referenced**: ROSTER.md, BRIEFING-CURRENT-STATE.md.

**Wanted but not found**: none.

## Verified how

Method: ran all three dispatch-specified pytest invocations verbatim (final tails above,
each actually executed this session, not recalled from an earlier run), plus the four
new/changed test files individually first (29 tests, all passed) before the full suite;
`ruff check`/`ruff format --check` on every changed `.py` file, re-running affected tests
after the one `ruff format` pass that touched code; a direct `git grep` for `search_projects`
across the registry/rail/pre_classifier surfaces before adding it, to support the
collision-check claim above; manual line-by-line trace of the `KNOWN_UNARMED_ASK_SITES`
alphabetical-fingerprint claim (which of the 7 original literals sorts first, confirming it
survives the 7→5 shrink) rather than asserting it from the test passing alone. Layer:
unit-test + static-registry verification only — no live chat turn, no LLM call, no running
server. Denominator: 4 units, 8 files changed, 4 new test files (26 new tests) + 1 pre-existing
test file's regression fixed, 3 mandated test-gate commands run to completion each with a
0-failure final tail quoted above.
