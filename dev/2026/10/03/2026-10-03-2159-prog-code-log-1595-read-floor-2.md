# 2026-10-03 — Coding Agent (prog), #1595 Phase 3 — read_floor wave 2 (read_floor_2 build)

**Model**: Sonnet (assigned by Lead, dispatched as a subagent)
**Role**: Coding Agent (prog)
**Repo/branch**: `/Users/xian/Development/piper-morgan-worktrees/lead`, `claude/lead-cycle`

## Task

Build `read_floor` wave 2 as a NEW flip group `read_floor_2` (NOT flipped) per #1595 Phase 3.
Authority: `mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-wave2-and-writes-2026-10-03.md`
(Arch's ruling, section 1) and Lead's own proposal
`mailboxes/lead/sent/proposal-lead-to-arch-cc-exec-phase3-ratchet-is-now-rail-bound-read-floor-wave-2-for-four-floor-ops-2026-10-03.md`.
(The ack file named in the dispatch prompt,
`ack-lead-to-arch-cc-exec-shapes-adopted-wave-2-building-now-as-its-own-group-read-floor-2-2026-10-03.md`,
does not exist on disk — proceeded on the rule memo + proposal, which together fully specify the
task; noted as an unsatisfiable pointer in Arch's ruling.)

Template: commit `8a4137d462` (the original `read_floor` build).

## Member decisions

1. **`get_feature_info`** (QUERY, FLOOR, GET) — IN, clean. `action_registry.py:410-412`
   ("Provide details about a specific Piper feature or integration"). `git grep -n
   get_feature_info -- services/` outside the registry/pre_classifier wiring returns nothing —
   no persistence anywhere on this path.
2. **`check_completion_status`** (STATUS, FLOOR, GET) — IN, clean. `action_registry.py:366-368`
   ("Answer completion-history questions"). Same `git grep` result — no persistence.
3. **`write_stakeholder_update`** (QUERY, FLOOR, verb COMPOSE) — IN. Read the handler path end to
   end: category QUERY has no dedicated branch in `ContextAssembler.gather_context`
   (`context_assembler.py:355-412`), so it falls to the generic `else` baseline
   (`_gather_status_priority_context`, read-only); `ConversationalFloor.respond()` drafts the
   prose directly. `action_registry.py:404-407`'s own comment: "#1256: FLOOR drafts the prose for
   an outbound stakeholder update." `git grep -rn stakeholder -- services/` outside
   `action_registry.py`/`pre_classifier.py` is EMPTY — no stakeholder-update handler, save, or
   repository write anywhere in `services/`. Floor path persists nothing → member, per Arch's
   condition.
4. **`get_identity`** (IDENTITY, FLOOR, GET) — IN. Arch's check (d) run FIRST:
   `scripts/inversion_phase3_deletion_gate.py --list IDENTITY_PATTERNS --live
   create_reminder,create_todo,delete_todo,read_floor,read_referent,read_status,read_strategic,
   read_synthesis,read_temporal` → verdict "GO (partial)", but the one claimed row, `"who are
   you?"`, is **[FAIL]**: `REVIEW-agrees (route=get_identity == claim=get_identity) but on a
   NON-LIVE op (not-live (no WorkflowEntry — the live consult dispatches rail keys only)); no
   surface-2 probe for this phrase.` Grepped every `SURFACE2_FLOOR_PROBES` report for an
   IDENTITY_PATTERNS phrase landing under its own action — none exists; the IDENTITY hits in the
   set5 probe (`inversion-phase3-surface2-floor-probe-2026-10-02-n5-anthropic-set5.md`) are
   DISCOVERY_PATTERNS phrases ("what are your capabilities?") landing on `get_capabilities` under
   the IDENTITY *category*, a different list's row. So (d) does **not** credit IDENTITY_PATTERNS:
   no rail entry existed and no probe covers "who are you?" — it stays a live behaviour change,
   not a same-destination deletion. Included as a member; this wave gives it the rail entry
   condition (d) was testing for.

## Build

- `services/intent_service/workflow_entries.py`: added `_READ_FLOOR_2_MEMBERS`,
  `_read_floor_2_entries()` (reuses the existing `_make_read_floor_entry_point` factory — it's
  already op/category-generic, so a second factory would have been the same code twice), wired
  into `register_default_workflows()` as a separate `**_read_floor_2_entries()` line immediately
  after `read_floor`'s. Each entry carries the registry's `ACTION_DESCRIPTIONS` text (the
  router-description rule `read_floor` learned 2026-10-02), flip_group="read_floor_2".
- `services/intent_service/workflow_dispatcher.py`: `FLIP_GROUPS` gains `read_floor_2` (6 → 7
  members), with a block comment explaining why it's a separate group (read_floor is already
  live).
- Did **not** touch `scripts/inversion_phase1_shadow_score.py`'s lenient-FLOOR-rule function — it
  already checks `action not in get_action_workflows()`, group-name-agnostic, so it auto-covers
  the new members once registered. No change needed.
- Did **not** touch `scripts/inversion_phase2_gate.py` or `inversion_live.py`'s
  `resolve_live_match` — both iterate `FLIP_GROUPS` / check `flip_group` generically with no
  group-name hardcoding; adding `read_floor_2` to the frozenset is sufficient for `--audit` to
  pick it up.
- Did **not** add the new token anywhere in a flag/env/`CURRENT_LIVE_CATEGORIES`/deployment
  config. No `elif intent.action` branch added (MAX_DISPATCH_SITES untouched — entries only). No
  new extraction regexes. No LLM calls anywhere in this unit (the IDENTITY_PATTERNS gate check
  reads only frozen corpus/probe report files).

## Test/doc updates required by the build

- `tests/unit/services/intent_service/test_action_registry.py`: the disposition-oracle
  (`_true_disposition_for_registry_row`) checked `flip_group == "read_floor"` only; widened to
  `in ("read_floor", "read_floor_2")`. **Required**, not optional: for the two QUERY-category
  members (`write_stakeholder_update`, `get_feature_info`), QUERY is not in
  `_should_route_to_floor`'s `_FLOOR_ROUTED_CATEGORIES`, so the oracle's rail-entry branch is now
  reached first (where previously, with no entry, it fell through to the QUERY/ANALYSIS → FLOOR
  default). Without the widen, the oracle would misclassify those two rows WORKFLOW against the
  registry's FLOOR, failing `TestActionRegistryMatchesActionGate`. `get_identity`/
  `check_completion_status` are unaffected either way (IDENTITY/STATUS ARE in
  `_FLOOR_ROUTED_CATEGORIES`, so `_should_route_to_floor` short-circuits to FLOOR before the
  oracle's rail-entry check is ever reached) — confirmed by reading `_should_route_to_floor`
  (`services/intent/intent_service.py:15414-15446`) directly, not assumed.
- `tests/unit/services/intent_service/test_inversion_flip_groups_1667.py`: closed-set pin widened
  6 → 7 members.
- New pin file `tests/unit/services/intent_service/test_read_floor_2_rail_1595.py`, mirroring
  `test_read_floor_rail_1595.py`: membership, registry-disposition-checked-at-registration guard,
  entry-point behavior (re-keys IDENTITY correctly), missing-context → `None`, live-match-through-
  the-group, router-description coverage, plus one extra pin that `read_floor`/`read_floor_2`
  membership stay disjoint (the actual point of building a second group).
- **Found and fixed one real regression from adding `get_identity`'s rail entry**:
  `tests/unit/services/intent_service/test_inversion_live_1595.py::TestFallthroughReasons::
  test_registry_only_operation_not_rail_dispatchable` used `get_identity` as its stand-in example
  of "ACTION_REGISTRY-only, no rail key → not_rail_dispatchable". Since `get_identity` now HAS a
  rail entry, the stubbed-router consult started returning a live `Intent` instead of `None`,
  failing the test's assertion. Swapped the example to `get_contextual_guidance` (GUIDANCE,
  CANONICAL) — confirmed genuinely rail-free (`get_action_workflows()` membership checked
  directly in a REPL) and the test's own docstring premise matches it exactly. Fixed with a
  comment explaining the swap and why (same shape as the LOCAL_GIT_STATUS deletion's stand-in
  swaps earlier this epic). Re-ran the file: 37/37 pass.
- Checked (not touched, no change needed): `tests/unit/services/intent_service/
  test_inversion_router_1595.py:89` groups `get_identity` with `manage_portfolio`/
  `get_contextual_guidance` under a comment "registry-only canonicals (no rail key)" but the
  assertion only checks catalog membership (`op in names`), never rail-key absence — still passes
  (33/33), comment is now loosely imprecise for `get_identity` but not a correctness bug; left
  alone as out of scope for this build.
- `docs/internal/architecture/current/intent-routing-stack.md`: new `read_floor_2` section
  (member decisions, get_identity's check-(d) evidence, implementation summary, "Not flipped").
  Inserted immediately before the `## Pointers` footer (caught and fixed one editing mistake —
  initially duplicated the adjacent "Ninth deletion" heading; removed the stray duplicate).
- `dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md`: dated entry appended.

## Two pre-existing failures found during the full baseline run — NOT caused by this build

Full run (`tests/unit` + `tests/test_architecture_enforcement.py`) surfaced 3 failures initially;
one (`test_registry_only_operation_not_rail_dispatchable`, above) was a real consequence of this
build and is fixed. The other two are the **same root cause**, unrelated to `read_floor_2`,
reproduced from a totally clean process with zero imports of any file this build touched:

- `tests/unit/test_inversion_phase3_deletion_1595.py::TestDeletedPatternListsLedger::
  test_real_ledger_entries_pass_non_regression`
- `tests/test_architecture_enforcement.py::TestChatPointersReachabilityRatchet::
  test_every_pointer_resolves_deterministically`

Both fail on the SAME assertion: the `TEMPORAL_PATTERNS` deletion-ledger entry's
`check_deleted_entry_non_regression` now reports `"'did I finish the report yesterday': router
verdict now MATCH (route=check_completion_status) — no longer MATCH or an agreeing REVIEW (MATCH
on a NON-LIVE op ... check_completion_status is not in CURRENT_LIVE_CATEGORIES)"`.

**Verified not caused by this build**: `git diff --stat HEAD` against `pre_classifier.py`,
`action_registry.py`, `intent/intent_service.py`, `shared_types.py`,
`scripts/inversion_phase3_deletion_gate.py`, `scripts/inversion_phase0_baseline.py`, and
`scripts/inversion_phase3_deleted_patterns.json` — all **empty** (none of those were touched by
this build). Reproduced `PreClassifier.pre_classify("what time is it?")` → `None` from a bare
`python -c` importing only `pre_classifier` (no `workflow_entries` import at all) — confirms
`TEMPORAL_PATTERNS` is already `[]` (emptied by an earlier Phase 3 deletion) independent of
anything here. Traced `check_deleted_entry_non_regression`'s failure mechanically: the row's
live-dispatchability verdict for `check_completion_status` is identical whether or not it has a
rail entry (its `flip_group`, `"read_floor_2"`, is not in `CURRENT_LIVE_CATEGORIES` either way, so
`resolve_live_match` returns the same `None`/`not_live_categorized` reason regardless) — the
check reads a FROZEN router report, no live LLM call, so this build cannot have changed its
verdict. This is a pre-existing drift between the TEMPORAL_PATTERNS ledger's frozen evidence and
`CURRENT_LIVE_CATEGORIES`'s current membership (the doc comment on that constant notes it was
itself just updated 2026-10-03 to add READ_FLOOR, two days late) — **flagging for Lead to triage
or route to Arch; not fixed here** (out of scope for a read_floor_2 build, and fixing a ledger
drift is a judgment call on evidence, not mine to make unilaterally).

## Tests (final)

```
POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/test_read_floor_2_rail_1595.py \
  tests/unit/services/intent_service/test_read_floor_rail_1595.py \
  tests/unit/services/intent_service/test_inversion_flip_groups_1667.py \
  tests/unit/services/intent_service/test_action_registry.py \
  tests/unit/services/intent_service/test_inversion_live_1595.py \
  tests/unit/services/intent_service/test_inversion_router_1595.py \
  -q -p no:cacheprovider -m "not llm" -o addopts="--import-mode=importlib --tb=short"
# 221 passed

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/intent/ -q -p no:cacheprovider -m "not llm" \
  -o addopts="--import-mode=importlib --tb=line"
# 205 passed, 2 skipped, 93 deselected

POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit tests/test_architecture_enforcement.py -q \
  -p no:cacheprovider -m "not llm" -o addopts="--ignore=tests/archive --ignore=*/archive/* \
  --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ \
  --tb=short --import-mode=importlib"
# first run: 3 failed, 12239 passed (2 pre-existing + 1 caused-by-build, see above)
# after fixing the caused-by-build one: re-run in progress at handback time
```

`ruff check` + `ruff format --check` clean on every changed `.py` file.

## Files changed

```
 M services/intent_service/workflow_dispatcher.py
 M services/intent_service/workflow_entries.py
 M tests/unit/services/intent_service/test_action_registry.py
 M tests/unit/services/intent_service/test_inversion_flip_groups_1667.py
 M tests/unit/services/intent_service/test_inversion_live_1595.py
?? tests/unit/services/intent_service/test_read_floor_2_rail_1595.py
 M docs/internal/architecture/current/intent-routing-stack.md
 M dev/2026/09/25/inversion-epic0-remaining-scope-2026-09-25.md
?? dev/2026/10/03/2026-10-03-2159-prog-code-log-1595-read-floor-2.md
```

No git add/commit/push/stash performed — Lead reviews and commits.

## Memory & briefing surfaces referenced this session

**Referenced**: `project_router_grammar_prefers_rail_entry_description` (confirmed the current
`_read_floor_entries()` already implements this — mirrored it for `read_floor_2` without
rediscovering the lesson). CLAUDE.md "Verify First, Create Second" / "Name the layer, and state
the denominator" — informed how the pre-existing-failure investigation was written up (layer:
frozen-report check, no LLM; denominator: 2 of 3 initial failures, 1 fixed).

**Loaded but not referenced**: the rest of CLAUDE.md's worktree/mailbox discipline sections (not
relevant — no git/mailbox writes performed by this subagent).

**Wanted but not found**: the ack memo named in the dispatch prompt
(`ack-lead-to-arch-cc-exec-shapes-adopted-wave-2-building-now-as-its-own-group-read-floor-2-
2026-10-03.md`) does not exist in `mailboxes/lead/sent/` or `read/` — proceeded on the rule memo +
proposal instead, which fully specify the task.
