# 2026-09-27 06:55 — Coding Agent (prog), Sonnet — #1595 unit 3c / #1606 set-default-repo allowlist

**Role**: Coding Agent (prog), dispatched by Lead Dev. **Model**: Sonnet 5. **Worktree**:
`/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) — did NOT
commit, stage, or touch the git index per dispatch instructions; reporting back to Lead via
SubagentHandback for Lead to review/commit.

## Task

Put `set_default_repo` (rail entry `set_default_repo_entry`, `services/intent_service/
workflow_entries.py` ~L1549) on the #1677 named-write allowlist, following the exact procedure
the two prior allowlist commits established (`a3180731c4` create_reminder / `70f7dd5159`
delete_todo): re-run Arch's three conditions, add `flip_write_allowlist_key`, extend
`FLIP_WRITE_ALLOWLIST` to four keys, sibling test file, doc paragraph, gates.

## Precedents read in full

- `git show a3180731c4` — create_reminder allowlist entry + `workflow_entries.py`/dispatcher diff.
- `git show 70f7dd5159` — delete_todo (DESTRUCTIVE) allowlist entry + confirm-provenance pattern.
- `docs/internal/architecture/current/intent-routing-stack.md` — #1677 section (lines 734-816)
  and both prior additions' paragraphs.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py`,
  `..._create_reminder_1559.py`, `..._delete_todo_1606.py` — full read, used as the template.
- `gh issue view 1606 --comments` — confirmed the corpus phrasing and that the set-default-repo
  half was explicitly named as the next unit ("a WRITE that nobody has run Arch's three
  allowlist conditions against").

## Arch's three conditions — re-run, evidence

1. **Registered on the rail, `action_triggered=True`.** `get_action_workflows()["set_default_repo"]`
   exists (`workflow_entries.py` line ~2094: `"set_default_repo": set_default_repo_entry`). No
   alias family — `ActionMapper` has nothing that canonicalizes to it; it's reached via the
   pre-classifier's `SET_DEFAULT_REPO_PATTERNS` (emits the literal action string directly,
   `pre_classifier.py` ~L1379-1393) and via the LLM/inversion routers targeting the same name.
   `derive_routing_grammar()` confirmed to emit `"set_default_repo"` as a grammar name
   (`TestRouterChoiceSet.test_set_default_repo_is_a_grammar_name`, passing).
2. **Effect correct BY BEHAVIOR — WRITE, not DESTRUCTIVE.** Read `_handle_set_default_repo`
   (`services/intent/intent_service.py` ~L7305-7406) and `ConnectorConfigService.set_default_repo`
   (`services/connectors/config_service.py` ~L52-61): the handler parses an owner/name token,
   then calls `ConnectorConfigService(session).set_default_repo(user_id, full_name)`, which reads
   the owner's github config blob, sets `config["default_repository"] = value` (overwriting any
   prior value while **preserving other keys**, per its own docstring), and upserts the blob back.
   One key in a JSONB blob is replaced; nothing is deleted anywhere in the call chain. This is an
   overwrite of a preference, not a data-loss operation — the user can set it back with the same
   command (same shape as the `set_timezone` precedent already on the rail as WRITE). **Did not
   need to STOP on the DESTRUCTIVE question** — confirmed WRITE, matches the entry's pre-existing
   declared effect (unchanged by this work).
3. **Reaches `consent_gate.evaluate_consent`.** Read `_dispatch_action_rail`
   (`services/intent/intent_service.py` ~L15717-15794, the block #1595 unit 4 extracted verbatim
   from `_process_intent_internal` on 2026-09-26): entry-agnostic, keyed on `_rail_entry.effect`/
   `.outwardness`, unconditional for any `needs_consent`-deriving entry. Proven live, not just
   read, in `TestFlippedTurnReachesTheRail.test_flipped_turn_reaches_the_handler_and_consent_is_
   evaluated` (consent spy asserts exactly one call with `EffectClass.WRITE` / `Outwardness.PRIVATE`
   / the exact message / the exact principal).

## Discovered work — filed, not fixed (#1898)

While writing the full-rail test, discovered `_handle_set_default_repo` reads
`intent.context.get("original_message", "")` **only** — no fallback to the top-level
`Intent.original_message` field the way `handle_create_reminder` / `handle_delete_todo` do
(`intent.original_message or intent.context.get("original_message", "")`).
`consult_inversion_live` builds its Intent with `original_message` set **only** at the top level
(`services/intent_service/inversion_live.py` ~L765-781 — `context` carries only
`inversion_live`/`inversion_args`). Verified behaviorally (not just read): called
`_handle_set_default_repo` directly with an Intent shaped exactly as the inversion builds one —
`success: True`, `message: "That doesn't look like an owner/name repo…"`,
`requires_clarification: True`, `set_default_repo awaited: 0`. The write silently does not
happen under the flip — not unsafe, but functionally the allowlist entry does not yet close
#1606's corpus row live.

Per Discovered Work Discipline (CLAUDE.md, non-negotiable — "not my problem" is never valid),
filed **#1898** with the repro, the one-line suggested fix, and acceptance criteria:
https://github.com/mediajunkie/piper-morgan-product/issues/1898

Decided NOT to fix it in this unit: out of the dispatched task's explicit scope (allowlist entry
only), and the fix touches a shared handler with its own callers/history that deserves its own
reviewed change rather than a drive-by inside an allowlist commit. Documented prominently in the
new test file, the routing-stack doc paragraph, and the epic-0 progress log so it's never mistaken
for "closed."

## Changes

- `services/intent_service/workflow_entries.py` — `set_default_repo_entry` comment block extended
  with the #1595 unit 3c re-run of all three conditions (registration/alias-family absence,
  effect-by-behavior, consent-reachability) plus the QUERY-category-sweep caveat;
  `flip_write_allowlist_key="set_default_repo"` added to the constructor.
- `services/intent_service/workflow_dispatcher.py` — `FLIP_WRITE_ALLOWLIST` extended to
  `{"create_todo", "create_reminder", "delete_todo", "set_default_repo"}` with the matching
  comment block.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_set_default_repo_1606.py`
  (NEW, 12 tests) — entry declaration, dispatch guard (named flip, QUERY-category sweep +
  EXECUTION-does-NOT-sweep negative twin, sub-threshold block, unnamed-wave non-flip,
  default-empty dark), full-rail (consent evaluated; #1898 gap pinned honest — write does NOT
  happen today), grammar-name structural fact.
- `tests/unit/services/intent_service/test_inversion_write_allowlist_1677.py` — closed-set
  assertion and alias-key denominator test updated from three to four keys/objects
  (create_todo/create_reminder/delete_todo/set_default_repo, the last with no alias family).
- `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py` —
  `TestUnallowlistedWriteSibling` used `set_default_repo` as its "still-unallowlisted write"
  example; now allowlisted, so this test failed on first full-suite run (caught it, not assumed
  clean). Swapped the exemplar to `create_issue` (WRITE, filed under QUERY, still unallowlisted —
  #1677's own original worked example) and corrected the docstring's now-stale "#1606 not closed"
  claim (the allowlist condition IS now met; still blocked by the surface-1 split gap AND #1898).
- `docs/internal/architecture/current/intent-routing-stack.md` — one paragraph under the #1677
  section documenting the fourth allowlist entry, its three conditions, the QUERY-category caveat,
  and #1898.
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md` — progress-log line.

## Gates — full output

```
$ venv/bin/python -m pytest tests/unit/services/intent_service/ -q
4874 passed, 15 warnings in 132.37s (0:02:12)     [exit 0]

$ venv/bin/python -m pytest tests/test_architecture_enforcement.py -q
63 passed, 1 xfailed in 11.49s     [exit 0]

$ scripts/run-sweep.sh ratchets
73 passed, 1 xfailed in 18.84s
--- mypy per-code gate (#1436) ---
mypy gate: all 24 ratcheted codes at ceiling (total=1121; ...)     [exit 0, unchanged ceiling]

$ venv/bin/python scripts/inversion_phase2_gate.py --audit | grep -A3 "NAMED-WRITE ALLOWLIST"
  NAMED-WRITE ALLOWLIST (#1677)              : ['create_reminder', 'create_todo', 'delete_todo', 'set_default_repo']
    rail keys declaring an allowlist key     : ['add_reminder', 'add_todo', 'cancel_reminder', 'cancel_todo', 'create_reminder', 'create_todo', 'delete_reminder', 'delete_todo', 'new_todo', 'remove_reminder', 'remove_todo', 'set_default_repo', 'set_reminder']
    ⚠️ These flip when a flag token names the OPERATION or its registry CATEGORY (create_todo is EXECUTION — flipping that category flips this write too). No flip_group sweeps them in.

$ venv/bin/ruff format <touched files>   → 5 files left unchanged (+1 unchanged on the unit4 file)
$ venv/bin/ruff check --fix <touched files>   → All checks passed!
```

No LLM calls made. No flag/env/Fly/deploy changes. Did not commit, stage, or touch the index —
all changes are on-disk in the Lead's worktree, unstaged, for the Lead to review.

## Verified how

- **Method**: read the actual source (handler bodies, registry, rail dispatch code) rather than
  citing prior commits' claims; ran a direct behavioral probe against `_handle_set_default_repo`
  with an Intent shaped exactly as `consult_inversion_live` constructs one (not inferred from
  reading alone) to confirm the #1898 gap; ran the full test files and full gates listed above and
  quoted their actual terminal output in this log, in the same turn as the claims they support.
- **Layer**: unit-test layer for the allowlist/dispatch-guard/consent-reachability claims (deterministic
  router fake, per the sibling files' own m-43 caveat — proves the path, not live draw distribution);
  direct handler-call layer (not curl, not a route test) for the #1898 discovery; static
  `--audit` read for the four-key count; full pytest run (not a subset) for the regression claims.
- **Denominator**: full `tests/unit/services/intent_service/` (4874 tests, not a filtered subset)
  + full `tests/test_architecture_enforcement.py` (63+1) + full `scripts/run-sweep.sh ratchets`
  (73+1 pytest + the 24-code mypy gate). The one full-suite run caught the
  `test_inversion_multi_intent_unit4_1595.py` regression that a narrower "just run my new file"
  check would have missed.

## Discovered issues filed

- **#1898** — `_handle_set_default_repo` doesn't fall back to `intent.original_message`, so a
  flipped turn cannot currently write the row. See above.

## Memory & briefing surfaces referenced this session

- **Referenced**: `docs/internal/architecture/current/intent-routing-stack.md` (the #1677
  section — mechanism, prior two entries' exact paragraph shape, used as the template for this
  entry's paragraph); the two precedent commits (`a3180731c4`, `70f7dd5159`) and their sibling
  test files (structure/naming/fixture conventions mirrored exactly); `dev/2026/09/25/
  inversion-epic0-remaining-scope-2026-09-25.md` (confirmed this was the next planned unit,
  informed the progress-log entry format); CLAUDE.md Discovered Work Discipline (drove filing
  #1898 immediately rather than noting it and moving on).
- **Loaded but not referenced**: role-table / worktree-model / mailbox-discipline sections of
  CLAUDE.md (not applicable — dispatched prog agent, no commit/mailbox actions this session).
- **Wanted but not found**: none — the precedent commits + doc section were sufficient to
  reconstruct the exact procedure without guessing.
