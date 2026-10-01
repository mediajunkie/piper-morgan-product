# 2026-10-01 0830 — prog (Coding Agent) — #1595 Phase 3 TEMPORAL sort + get_current_time rail entry

**Model**: Sonnet (Claude Sonnet 5)
**Role**: prog (Coding Agent), dispatched by Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Scope**: implement Arch's 2026-10-01 TEMPORAL ruling (two parts: per-row sort of the 48
TEMPORAL_PATTERNS deposit rows, then a READ rail entry for `get_current_time` in flip_group
`read_temporal`). NO LLM calls made anywhere in this session (confirmed: the gate scripts run
read scored reports / the live router stub in tests, never a live LLM client). No flag/env
changes. Did not touch the git index (dispatcher instruction — no staging/commit performed).

## Read first (per dispatch prompt)

- `mailboxes/lead/read/rule-arch-to-lead-cc-ppm-cxo-temporal-give-get-current-time-a-rail-entry-and-the-gate-has-a-false-live-path-2026-10-01.md`
  — Arch's ruling in full: (a) a rail entry, not a procedure amendment, because the deletion
  gate's GO premise ("post-deletion the row lands where the router sends it") holds only for
  rail keys, and `get_current_time` had none; (b) sort the 48 TEMPORAL rows' expectations BEFORE
  the entry ships, since the pre-classifier's own code comment says it "assigns get_current_time
  to ALL temporal queries" including conversational ones; (c) a separate gate defect —
  `expected_action_is_live` checked naming only (op/canonical/group/category), never rail
  membership or the effect guard, so `--live get_current_time` would read a false GO. (c) was
  already fixed earlier the same day (commit `feb620262e`, visible in git log at session start) —
  confirmed via `tests/unit/test_inversion_phase3_deletion_1595.py::TestLiveMeansDispatchable`
  already existing with the fix landed; this unit's job was (a)+(b).
- `docs/internal/architecture/current/intent-routing-stack.md` §Phase 3 + the deletion-history
  subsections (First/Second deletion), to learn the established conventions (tombstone pattern,
  ledger entries, `# RULED .../SORTED ...` inline-comment format already used by CXO+PPM's
  same-day PRIORITY/CALENDAR re-sort).
- `services/intent/intent_service.py` ~15360–15420: `_requires_canonical_handler`'s TEMPORAL
  floor/keyword split (`_TEMPORAL_FLOOR_KEYWORDS` regex) — confirmed this is a MESSAGE-CONTENT
  split, independent of which corpus row claims a phrase; `_should_route_to_floor` (~15433) and
  the real `_process_intent_internal` dispatch order (`_should_route_to_floor` →
  `canonical_handlers.can_handle` → `_dispatch_action_rail`, call sites at lines ~2766, ~2790,
  ~2962) — this is what let me determine the ACTION_REGISTRY disposition question (below).
- `services/intent_service/canonical_handlers.py`: `CanonicalHandlers.can_handle()` (claims the
  WHOLE TEMPORAL category unconditionally) and `_handle_temporal_query` (the actual canonical
  handler — has its OWN internal agenda/retrospective/last-activity/duration sub-detection before
  falling through to the bare date+time response; returns a `dict`, not `IntentProcessingResult`).
- `services/intent_service/workflow_entries.py`: `_CALENDAR_QUERY_FLIP_GROUPS`/`_CALENDAR_QUERY_COHORT`
  and the standalone `changes_query_entry` pattern (single entry, not a cohort) — mirrored for
  `get_current_time_entry`. `_make_query_dispatch_entry_point`/`_make_user_scoped_query_dispatch_entry_point`
  factories call `getattr(intent_service, handler_attr)` — NOT usable for `_handle_temporal_query`,
  which lives on `canonical_handlers`, not `intent_service`, and returns a dict not
  `IntentProcessingResult` — so a dedicated entry point function was needed (mirrored
  `run_archived_projects_query_workflow`'s lazy-import-IntentProcessingResult pattern, the
  established precedent for this module's circular-import constraint).
- `services/intent_service/action_registry.py` line ~85: `("TEMPORAL", "get_current_time"):
  ActionDisposition.CANONICAL`.
- The two prior same-day lane logs (calendar + temporal deposits,
  `dev/2026/09/30/2026-09-30-2150-...` / `...-2155-...`) — row-shape convention, `notes` field
  precedent, the "report don't invent" discipline for structurally unreachable literals (not
  relevant to THIS unit directly, but establishes the sourcing/verification bar).

## Part 1 — sorted the 48 TEMPORAL_PATTERNS deposit rows

**Method**: ran the gate live (`scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS
--live read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`)
to get the LIVE ROUTER's own answer for each of the 50 claimed rows (2 pre-existing + 48 deposit),
per the dispatch's explicit instruction to use the router's answer as evidence, not authority.
Quoted output (filtered via `grep -vE "^[0-9]{4}-"` per dispatch):

```
live set source: --live = ['CREATE_REMINDER', 'CREATE_TODO', 'READ_REFERENT', 'READ_STATUS', 'READ_STRATEGIC', 'READ_SYNTHESIS', 'READ_TEMPORAL']
corpus denominator: 283 rows total = 232 claimed + 51 unclaimed

## TEMPORAL_PATTERNS
literals: 56  |  rows claimed: 50/283
verdict: NO-GO

[16 MATCH lines (pure time/date), 34 MISMATCH lines — full output in scratchpad,
 summarized in the sort table below]
```

16 MATCH (pure time/date asks → router agrees `get_current_time`), 34 MISMATCH — matches the
dispatch prompt's stated counts exactly.

**Sort table** (phrase → old expected → new expected → why). All 48 deposit rows carried
`action:get_current_time` before this unit (the pre-classifier's over-claim, per Arch's finding).
The 2 pre-existing rows ("when is my next meeting?" → `action:meeting_time`; "what time is it?" →
`category:TEMPORAL`) were ALREADY correctly sorted — no change.

| phrase | old | new | why |
|---|---|---|---|
| what's the time | get_current_time | get_current_time | pure time ask, router MATCH |
| current time please | get_current_time | get_current_time | pure time ask, router MATCH |
| give me the time now | get_current_time | get_current_time | pure time ask, router MATCH |
| tell me the time | get_current_time | get_current_time | pure time ask, router MATCH |
| what day is it | get_current_time | get_current_time | pure date ask, router MATCH |
| what's the date | get_current_time | get_current_time | pure date ask, router MATCH |
| current date please | get_current_time | get_current_time | pure date ask, router MATCH |
| today's date please | get_current_time | get_current_time | pure date ask, router MATCH |
| what's today | get_current_time | get_current_time | pure date ask, router MATCH |
| give me the date and time | get_current_time | get_current_time | pure date+time, router MATCH |
| what day of the week is it | get_current_time | get_current_time | pure date ask, router MATCH |
| tell me the date | get_current_time | get_current_time | pure date ask, router MATCH |
| what date is it | get_current_time | get_current_time | pure date ask, router MATCH |
| remind me today's day | get_current_time | get_current_time | pure date ask, router MATCH |
| pull up my calendar | get_current_time | **week_calendar** | router CLARIFY@0.6 (ambiguous, no day); aligned with the symmetric "pull up my schedule" row (week_calendar@0.85) rather than leave two parallel phrasings disagreeing on router noise |
| show the team calendar | get_current_time | **floor** | Arch's named example — no team-calendar feature; router agrees NONE@0.85 |
| pull up my schedule | get_current_time | **week_calendar** | router week_calendar@0.85 |
| show the team schedule | get_current_time | **floor** | no team-calendar feature; router agrees NONE@0.85 |
| calendar check for today | get_current_time | **meeting_time** | single day ("today"), router meeting_time@0.95 |
| schedule check for today | get_current_time | **meeting_time** | explicit "today"; router gave CLARIFY@0.4 (low confidence) but symmetric sibling "calendar check for today" scored meeting_time@0.95 for the identical construction — treated CLARIFY as router noise |
| walk me through my appointments | get_current_time | **week_calendar** | router week_calendar@0.75, matches Arch's "walk me through my meetings" example class |
| show all appointments | get_current_time | **week_calendar** | Arch's named "all appointments" example; router week_calendar@0.7 |
| walk me through my meetings | get_current_time | **week_calendar** | Arch's explicit named example; router week_calendar@0.85 |
| what are the upcoming meetings | get_current_time | **week_calendar** | "upcoming"; router week_calendar@0.85 |
| when is my team meeting | get_current_time | **meeting_time** | Arch's explicit named single-day example; router meeting_time@0.85 |
| when am i in a meeting | get_current_time | **meeting_time** | single/current; router meeting_time@0.85 |
| meeting check for today | get_current_time | **meeting_time** | single day; router meeting_time@0.95 |
| meeting check for tomorrow | get_current_time | **meeting_time** | single day; router meeting_time@0.95 |
| walk me through my events | get_current_time | **week_calendar** | router week_calendar@0.85 |
| show all events | get_current_time | **week_calendar** | router gave CLARIFY@0.6, disagreed: symmetric sibling "show all appointments" scored week_calendar@0.7 for the identical construction — aligned for consistency |
| what are the upcoming events | get_current_time | **week_calendar** | "upcoming"; router week_calendar@0.75 |
| events check for today | get_current_time | **meeting_time** | single day; router meeting_time@0.95 |
| events check for tomorrow | get_current_time | **meeting_time** | single day; router meeting_time@0.92 |
| when's the next event | get_current_time | **meeting_time** | single/next; router meeting_time@0.85 |
| what did I work on today | get_current_time | **action:session_activity_query** | beyond Arch's 4 named buckets: router names a REAL rail-registered op (WORKFLOW, flip_group read_status) at 0.92 confidence |
| what happened in the meeting yesterday | get_current_time | **floor** | retrospective, no specific item; router NONE@0.95 |
| did I finish the report yesterday | get_current_time | **action:check_completion_status** | beyond the 4 buckets: router names a real (FLOOR-disposition, no rail entry) op at 0.92 — named explicitly rather than collapsed to bare floor since a specific operation genuinely serves it |
| a lot happened yesterday | get_current_time | **action:changes_query** | beyond the 4 buckets: router names a real, already rail-registered op (WORKFLOW, read_temporal) at 0.92 |
| when was the last time I worked on this | get_current_time | **floor** | duration/retrospective; router CLARIFY@0.4 |
| how long have I been working on this | get_current_time | **floor** | Arch's explicit named example; router CLARIFY@0.3 |
| this week's priorities, remind me | get_current_time | **floor** | PRIORITY-shaped ask, not temporal; router proposes a compound PLAN[get_top_priority→create_reminder], not representable as a single `expected:action:X` |
| next week's priorities, remind me | get_current_time | **floor** | same PLAN shape |
| this month's numbers, remind me | get_current_time | **floor** | router PLAN[generate_report→create_reminder], same shape |
| when am i free | get_current_time | **week_calendar** | broad availability, no day; router week_calendar@0.85 |
| when's my next free slot | get_current_time | **meeting_time** | "next" = singular; router meeting_time@0.75 |
| what's my available time | get_current_time | **week_calendar** | router week_calendar@0.7 |
| when do I have free time | get_current_time | **week_calendar** | router week_calendar@0.7 |
| what are my open slots | get_current_time | **week_calendar** | router week_calendar@0.72 |

**Per-destination counts** (48 deposit rows, verified via `inversion_phase0_baseline.load_corpus()`
filtered to `source` containing `TEMPORAL_PATTERNS`, not guessed):

```
14  action:get_current_time   (unchanged)
13  action:week_calendar      (new)
10  action:meeting_time       (new)
 8  floor                     (new)
 1  action:session_activity_query  (new)
 1  action:check_completion_status (new)
 1  action:changes_query      (new)
```
34 rows changed, 14 unchanged — matches `grep -c "SORTED 2026-10-01"` = 34 on the builder file.
Plus the 2 pre-existing (`meeting_time`, `category:TEMPORAL`) unchanged → 16 total MATCH rows,
matching the dispatch's stated "16 MATCH" count.

Each changed row carries `# SORTED 2026-10-01 (Arch's ruling): was action:get_current_time` inline
(mirroring the CXO+PPM `# RULED 2026-09-30/10-01 (CXO+PPM): was action:X` convention already used
on the neighboring PRIORITY/CALENDAR blocks), and rows where I disagreed with the live router
carry an explanatory `notes` entry.

Regenerated: `venv/bin/python scripts/build_inversion_corpus_phase0.py` → 283 rows unchanged (no
row added/removed by this unit — Part 1 is pure `expected` reclassification).
`tests/unit/test_inversion_phase3_deletion_1595.py` — 24 passed (pinned 283-row constant
untouched, correctly).

## Part 2 — the `get_current_time` rail entry

**Where registered**: `services/intent_service/workflow_entries.py`, new standalone
`get_current_time_entry` (mirrors the `changes_query_entry` single-entry pattern, placed right
after `_CALENDAR_QUERY_FLIP_GROUPS`), added to `_default_entries["get_current_time"]` next to the
`changes_query` aliases.

```python
get_current_time_entry = WorkflowEntry(
    entry_point=run_get_current_time_workflow,
    effect=EffectClass.READ,
    description="get_current_time via action dispatch (#1595 Phase 3)",
    requires_context=["intent", "intent_service"],
    action_triggered=True,
    flip_group="read_temporal",
)
```

**Entry point it calls**: new `run_get_current_time_workflow` (same module), which calls
`intent_service.canonical_handlers._handle_temporal_query(intent, session_id, user_id)` — the
EXISTING canonical handler, not reimplemented — and converts its dict return into
`IntentProcessingResult` (the one conversion this entry needs that the other
IntentService-method-backed factories don't, since `_handle_temporal_query` lives on
`CanonicalHandlers` and returns a dict the main canonical-dispatch call site
(`intent_service.py` ~2800) converts inline). `_handle_temporal_query` does its OWN internal
agenda/retrospective/last-activity/duration sub-detection before falling through to the bare
date+time response, so this wrap is safe even for a TEMPORAL-shaped message that isn't literally
"what time is it" — confirmed by reading the handler body (`canonical_handlers.py` lines
~220–244), not assumed.

**ACTION_REGISTRY disposition change: NONE.** `("TEMPORAL", "get_current_time")` stays
`ActionDisposition.CANONICAL`. Verified this is the CORRECT (not merely unchanged) choice by
tracing the real `_process_intent_internal` dispatch order: `_should_route_to_floor` →
`canonical_handlers.can_handle` → `_dispatch_action_rail` (call sites lines ~2766/2790/2962).
`can_handle()` claims the ENTIRE TEMPORAL category unconditionally
(`canonical_categories = {TEMPORAL, GUIDANCE, PORTFOLIO, CONVERSATION, PROVENANCE}`), so for any
TEMPORAL intent that isn't floor-routed by the keyword split, the canonical branch returns
BEFORE `_dispatch_action_rail` is ever reached — this rail entry is structurally unreachable from
the main (non-live-consult) path, same as every other canonical-category action. Confirmed
empirically that NONE of the 6 canonical-category actions had a rail entry before this unit, and
after it only `get_current_time` does (the other 5 — `greeting`, `get_contextual_guidance`,
`manage_portfolio`, `manage_repos`, `explain_suggestion` — remain rail-free). Confirmed changing
the disposition to WORKFLOW would FAIL `test_registry_disposition_matches_live_runtime`
(`tests/unit/services/intent_service/test_action_registry.py`) — ran it to check, not assumed:
56 passed/0 failed with disposition unchanged at CANONICAL. The rail entry is consulted only by
`consult_inversion_live` (which REPLACES `intent.action`/category before the normal dispatch
order resumes — a genuinely different surface) and by the Phase 3 deletion gate's live-match
mechanism — documented in a module-level comment block in `workflow_entries.py` above the new
function, and in the routing-stack doc (below).

**Swapped pin** (dispatch's explicit ask): `test_inversion_phase3_deletion_1595.py::
TestLiveMeansDispatchable::test_floor_routed_canonical_is_not_live_even_when_named_in_the_flag`
used `get_current_time` as its "floor-routed canonical with no rail entry" example — the test's
own comment said to swap when a rail entry landed. Picked `("PROVENANCE", "explain_suggestion")`
from `action_registry.py` (CANONICAL disposition, confirmed via `get_action_workflows()` it still
has no rail entry after this unit's change). Updated the assertion and the
`gate.expected_action_is_live` call's frozenset tokens (`EXPLAIN_SUGGESTION`/`PROVENANCE` in place
of `GET_CURRENT_TIME`/`TEMPORAL`).

**A second, previously-unflagged test broke** (found by running the full `tests/unit/services/
intent_service/` suite, not named in the dispatch prompt):
`test_inversion_multi_intent_unit4_1595.py::TestConsultDeclinedSibling::
test_a_sibling_the_rail_cannot_serve_declines_the_whole_turn` asserted
`"get_current_time" not in get_action_workflows()` as part of proving that a multi-intent turn
with one unrailed sibling declines to the legacy chain entirely. Its test message
(`TURN_UNRAILED_HALF = "what are my open issues and what time is it"`) relied on "what time is
it" being surface-1-claimed as an unrailed `get_current_time`. Swapped the message's second half
to `"why did you suggest that"` (deterministic `PROVENANCE_PATTERNS` match,
`r"\bwhy did you (...suggest...)\b"`, confirmed in `pre_classifier.py`) and the assertion to
`"explain_suggestion" not in get_action_workflows()`, same reasoning as the swap above. Checked
`TURN_UNRAILED_HALF`'s other use site (line ~346, a loop asserting no non-READ actions are
emitted by the splitter) — unaffected either way since `explain_suggestion` isn't in the rail at
all, so that assertion's `a in rail` guard excludes it regardless.

**Mirrored flip-group pin**: the dispatch said to mirror `test_inversion_live_1595.py`'s
flip-group tests, but the actual `read_temporal` flip-group tests live in
`tests/unit/services/intent_service/test_inversion_flip_groups_1667.py`
(`TestWaveTwoReadTemporal`) — confirmed via `grep -rl read_temporal tests/`. Added
`"get_current_time"` to `_READ_TEMPORAL_KEYS` (now 14 keys, not 13 — updated the explanatory
comment), which is asserted exact-equal against `{k for k, e in rail.items() if e.flip_group ==
"read_temporal"}` (`test_read_temporal_keys_count_matches_group_membership`), so this also pins
`get_action_workflows()["get_current_time"].flip_group == "read_temporal"` and (via
`test_every_read_temporal_entry_is_read`) effect READ. Added a new e2e test,
`test_group_flip_dispatches_get_current_time_e2e`, mirroring
`test_group_flip_dispatches_a_calendar_op_e2e` exactly: stubs the router to return
`get_current_time`, sets `PIPER_INVERSION_LIVE_CATEGORIES=read_temporal`, asserts
`consult_inversion_live` returns an `Intent` with `action == "get_current_time"` via
`live_match == "group"` and `flip_group == "read_temporal"`.

## Docs + decisions.log

- `docs/internal/architecture/current/intent-routing-stack.md`: new §"`get_current_time` becomes
  a rail key (2026-10-01, Arch's ruling)" after the Second-deletion section, before `## Pointers`
  — covers the gate's false-live-path finding + fix, the per-row sort rationale and counts, the
  rail entry + entry point, the ACTION_REGISTRY-stays-CANONICAL reasoning in full (so a future
  reader doesn't have to re-derive the dispatch-order trace), what changes live ("what time is it"
  now routed by the Inversion when the flag carries `read_temporal`; surface 1/floor split is the
  fallback), and the two test swaps.
- `docs/internal/architecture/decisions/decisions.log`: one entry appended (2026-10-01 ~07:30
  PDT), summarizing both parts + test/suite evidence, pointing at this log and the doc section.

## Test / gate exit status

- `venv/bin/python scripts/inversion_phase3_deletion_gate.py --list TEMPORAL_PATTERNS --live
  read_status,read_referent,read_synthesis,create_todo,create_reminder,read_strategic,read_temporal`
  (run BEFORE the sort edits, to source the router evidence) → exit 0, 16 MATCH / 34 MISMATCH,
  50/283 rows claimed — quoted above and in the sort table.
- `venv/bin/python scripts/build_inversion_corpus_phase0.py` → 283 rows (59 REVIEW), exit 0, run
  twice (pre- and post-ruff-format) — identical 283 both times.
- `venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q` → **24 passed**,
  exit 0 (run three times across the session: after Part 1 alone, after Part 2's entry
  registration, after the pin swap — clean every time).
- `venv/bin/python -m pytest tests/unit/services/intent_service/ tests/unit/services/intent/ -q`
  → **5013 passed, 15 warnings (pre-existing, unrelated — asyncio-mark and
  coroutine-never-awaited warnings in unrelated test files), exit 0** (run in background due to
  the 120s default tool timeout; completed in 142.03s).
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63 passed, 1 xfailed**,
  exit 0 (the 1 xfailed is the SAME pre-existing xfail the two prior same-day lanes also reported,
  unrelated to this unit).
- `MAX_DISPATCH_SITES` in `tests/test_architecture_enforcement.py` → **0, unchanged** (grep-
  confirmed; no `elif intent.action` branch added — pure `WorkflowEntry` registration per #1124).
- extraction ceiling (`pattern_literal_counts.total_literal_count()`) → **548, unchanged**
  (confirmed by direct call; no `pre_classifier.py` literal touched).
- `scripts/run-sweep.sh ratchets` → **73 passed, 1 xfailed** (completion ratchets +
  architecture enforcement combined), exit 0; mypy gate section: **"all 24 ratcheted codes at
  ceiling (total=1121)"** — identical total to baseline, no regression.
- `venv/bin/ruff format` + `ruff check --fix` on all touched `.py` files → 1 file reformatted
  (`scripts/build_inversion_corpus_phase0.py`, whitespace/line-wrap only — corpus regenerated
  again post-format, same 283 rows, confirmed no string-content change); `ruff format --check` +
  `ruff check` both clean on re-run across all 5 touched `.py` files.
- Re-ran targeted suite after the ruff reformat to confirm nothing regressed:
  `tests/unit/test_inversion_phase3_deletion_1595.py
  tests/unit/services/intent_service/test_inversion_flip_groups_1667.py
  tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py
  tests/unit/services/intent_service/test_action_registry.py` → **192 passed**, exit 0.

## Files touched

- `scripts/build_inversion_corpus_phase0.py` (Part 1: 34 rows' `expected` field changed +
  inline `# SORTED` comments + explanatory `notes`; reformatted by ruff, whitespace only)
- `tests/fixtures/inversion_corpus_phase0.yaml` (regenerated, 283 rows unchanged — pure
  reclassification, no add/remove)
- `services/intent_service/workflow_entries.py` (Part 2: new `run_get_current_time_workflow` +
  `get_current_time_entry` + `_default_entries["get_current_time"]` registration, with a
  module-level comment block explaining the effect/flip_group/disposition reasoning)
- `tests/unit/test_inversion_phase3_deletion_1595.py` (swapped the `TestLiveMeansDispatchable`
  pin's example from `get_current_time` to `explain_suggestion`)
- `tests/unit/services/intent_service/test_inversion_flip_groups_1667.py` (`_READ_TEMPORAL_KEYS`
  13→14, added `"get_current_time"`; new `test_group_flip_dispatches_get_current_time_e2e`)
- `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py` (swapped
  `TURN_UNRAILED_HALF`'s second segment + the `TestConsultDeclinedSibling` assertion from
  `get_current_time` to `explain_suggestion`/"why did you suggest that" — discovered via the
  full-suite run, not named in the dispatch prompt)
- `docs/internal/architecture/current/intent-routing-stack.md` (new §"`get_current_time` becomes
  a rail key" after the Second-deletion section)
- `docs/internal/architecture/decisions/decisions.log` (one entry appended)

**Not touched**: git index (no staging/commit, per dispatcher instruction), any flag/env var, no
LLM client invoked anywhere, `services/intent/intent_service.py` (read-only — confirmed the
dispatch order and the keyword-split comment, never edited), `services/intent_service/
canonical_handlers.py` (read-only — the canonical handler is REUSED, not modified),
`services/intent_service/action_registry.py` (read-only — disposition deliberately left
unchanged, with the reasoning documented in three places: this log, the rail entry's comment
block, and the routing-stack doc).

## Verified how

- **Method**: Part 1's sort evidence came from running the REAL deletion gate against the LIVE
  router (the exact command the dispatch specified) and quoting its per-row verdicts directly —
  not re-derived or guessed. Where I disagreed with the router (6 of 34 changed rows), the
  disagreement and its reasoning is in the row's own `notes` field, not just this log. Part 2's
  dispatch-order claim (why ACTION_REGISTRY stays CANONICAL) was verified three ways: reading the
  actual call-site order in `intent_service.py` (not inferred from a comment), running
  `test_registry_disposition_matches_live_runtime` with the entry registered to confirm it still
  passes at CANONICAL (56 passed), and empirically enumerating all 6 canonical-category actions'
  rail-entry status before and after this unit's change via a direct Python script against
  `get_action_workflows()` — not assumed from the architecture description. The swapped-pin
  example (`explain_suggestion`) was verified rail-free the same way, this session, not carried
  over from memory. All test/gate/ruff commands in this log were run this turn via Bash and their
  output is quoted or counted above, never recalled from an earlier run.
- **Layer measured**: Part 1 is surface-1/live-router corpus-expectation correctness (no LLM
  calls — the gate reads scored reports and the live router stub, confirmed by each script's own
  "no LLM calls" self-report and by the complete absence of any LLM-client invocation in any
  command run this session). Part 2 is static source-reading (dispatch-order trace,
  ACTION_REGISTRY lookup) PLUS live test execution against the real registration (not just a
  static claim) — the `test_group_flip_dispatches_get_current_time_e2e` test exercises the actual
  `consult_inversion_live` code path end-to-end with a stubbed router, not a mock of the
  consult itself.
- **Denominator**: Part 1 — 48/48 deposit rows re-evaluated against live router evidence (34
  changed, 14 confirmed-already-correct), plus the 2 pre-existing rows confirmed already correct
  (0 changed) = 50/50 rows covered, matching the dispatch's stated row count exactly. Part 2 — 1
  rail entry registered and verified via 3 independent checks (direct Python inspection, the
  registry consistency test, the new e2e dispatch test); 2 test files' pins swapped (1 named by
  the dispatch, 1 found via the full-suite run); full-suite denominators: 5013/5013 in
  `tests/unit/services/intent_service/` + `tests/unit/services/intent/` (no subset, no `-k`
  filter), 63/63 (+1 pre-existing xfail) in the full architecture-enforcement file, 24/24 in the
  Phase 3 deletion test file, 73/73 (+1 pre-existing xfail) in the ratchets sweep, mypy gate
  total 1121 unchanged from baseline (not independently re-measured against a prior session's
  number from memory — read directly off this run's own gate output).

## Memory & briefing surfaces referenced this session

- **Referenced**: Arch's mailboxed ruling (full text, the primary directive for this unit's
  scope and acceptance criteria); `docs/internal/architecture/current/intent-routing-stack.md`
  §Phase 3 (mechanism + established conventions — tombstone pattern, `PHASE3_REPORTS` precedence,
  `# RULED/SORTED` inline-comment format); the two prior same-day prog session logs (row-block
  convention, `notes` field precedent — read for format, not content, since this unit's task was
  different in kind); `services/intent_service/workflow_entries.py`'s own extensive in-file
  comments (the `changes_query_entry`/calendar-cohort precedent for how a standalone rail entry
  with a flip_group is documented and registered).
- **Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
  (bounded prog dispatch inside an existing shared worktree — no mailbox write, no sign-off
  merge, no git index touch, per dispatcher scope); the ROSTER/briefing-table sections (role
  already assigned by the dispatch prompt).
- **Wanted but not found**: the dispatch prompt pointed at
  `tests/unit/services/intent_service/test_inversion_live_1595.py` for the flip-group pin to
  mirror, but the actual `read_temporal` flip-group tests live in
  `test_inversion_flip_groups_1667.py` (confirmed via `grep -rl read_temporal tests/`) — used the
  correct file once located; noted here so a future reader isn't misdirected by the same pointer.

## Discovered work

None filed as a separate GitHub issue — both items below are test-maintenance consequences of
this unit's own change, fixed in this same session rather than deferred:
1. `test_inversion_multi_intent_unit4_1595.py::TestConsultDeclinedSibling::
   test_a_sibling_the_rail_cannot_serve_declines_the_whole_turn` broke on the full-suite run
   (not named in the dispatch prompt) because it used `get_current_time` as its "genuinely
   unrailed" example — same shape as the dispatch's named swap, fixed the same way
   (`explain_suggestion`).
2. Noted inline in the sort table: the live router shows mild inconsistency on near-identical
   symmetric phrasings at low confidence (e.g. "pull up my calendar" CLARIFY@0.6 vs "pull up my
   schedule" week_calendar@0.85; "show all events" CLARIFY@0.6 vs "show all appointments"
   week_calendar@0.7; "schedule check for today" CLARIFY@0.4 vs "calendar check for today"
   meeting_time@0.95) — treated as router noise at the low-confidence end and aligned the pairs
   for consistency, documented per-row. Flagging for the Lead/Arch in case this points at a
   router-prompt sharpening opportunity (same shape as the 2026-09-29 "any change to the router's
   prompt is scored on both tables" rule's motivating cases), not acted on further by this unit.
