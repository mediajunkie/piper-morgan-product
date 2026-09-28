# 2026-09-28 0815 — prog (Coding Agent) — #1595 unit 4b (#1897/#1606): additive "plan" outcome

**Role**: prog (Coding Agent), model Sonnet 5. Dispatched by Lead Developer, in the Lead's
worktree (`/Users/xian/Development/piper-morgan-worktrees/lead`, branch `claude/lead-cycle`).
No git index touched at any point (per dispatch instruction — no staging/commit performed).
No live LLM calls anywhere in this unit — all router behaviour exercised with stubbed
`inversion_router.route`; no flag/env defaults changed. The Lead runs the before/after
single-op routing-accuracy measurement separately (PM-approved) — explicitly NOT run here.

## Task

Build #1595 unit 4b: the additive `RoutingDecision.outcome="plan"` + `operations: List[Dict]`
grammar shape, exactly per Arch's ruling, plus the smallest honest wiring of that plan into
the unit-4 rail loop (#1897's actual fix — a message that never splits at surface 1 loses one
half either way today; a plan lets the router answer such a message with an ordered list of
operations instead of one).

## Read first

- `mailboxes/lead/read/rule-arch-to-lead-cc-ppm-1595-unit4b-grammar-shape-additive-plan-outcome-not-urgent-2026-09-26.md`
  — the spec. Additive `outcome="plan"` + `operations: List[Dict]`, never touching the
  single-op contract; prompt copy change (single-op stays default, plan is the exception
  clause); per-element validation identical to single-op validation; explicitly flagged the
  JSON-repair-retry interaction with a list response as UNSOLVED and mine to solve.
- `docs/internal/architecture/current/intent-routing-stack.md` in full for the #1595 chain,
  especially the unit-4 block (`_maybe_dispatch_multi_intent_inversion`, Arch's three
  sequencing rules, the #1896 split stand-down / peek-not-take coupling) and its own
  "Denominator" paragraph naming the exact residual this unit closes.
- GitHub #1897 (the measured fact: 4 phrasings, all read+write, none split at surface 1 — the
  legacy path drops the write half, the inversion path answers one half and drops the other)
  and #1606 (corpus source, NOT closed by this unit — its repo half is `set_default_repo`,
  already allowlisted separately by unit 3c).
- `services/intent_service/inversion_router.py` in full.
- `services/intent_service/inversion_live.py::consult_inversion_live` + the unit-4 rail loop
  in `services/intent/intent_service.py::_maybe_dispatch_multi_intent_inversion`.
- `tests/unit/services/intent_service/test_inversion_router_1595.py`,
  `test_inversion_live_1595.py`, `test_inversion_multi_intent_unit4_1595.py` — read in full to
  learn the stubbing idioms (`ScriptedLLM`, `_stub_route`, `_route_by_segment`, the `svc`
  SimpleNamespace, the `sm`/`mem_prefs`/`todo_boundary` fixture set) before adding to them.

## 1. `RoutingDecision` shape (inversion_router.py)

Added `operations: List[Dict[str, Any]] = field(default_factory=list)`, populated ONLY on a
plan decision, never alongside `operation`/`args` (a plan decision leaves those at their
single-op defaults). `route_label` renders a plan as `PLAN[op1→op2→...]` (arrow chain — order
is load-bearing to what a plan means downstream, never a bag). Docstring extended in place;
every existing field and every existing outcome value is byte-identical.

## 2. Prompt change — exact before/after text

**Before** (`_SYSTEM_PROMPT`):
```
"You are the intent router for Piper Morgan, a product-management "
"assistant. Your ONLY job is to select which single operation should "
"handle the user's message. You never answer the message yourself.\n\n"
"Rules:\n"
"- Choose exactly ONE operation name from the provided catalog, or "
f"{NONE_ROUTE} when no catalog operation applies (the message is "
"conversational, out of scope, or best answered in prose), or "
f"{CLARIFY_ROUTE} when the message is genuinely ambiguous between "
"materially different operations.\n"
"- If the message contains a refusal or topic change while a flow is "
"active, route the user's actual words, not the flow's expectation.\n"
"- Extract obvious arguments (issue numbers, project names, times, "
"repo names) into args as simple key/value strings.\n"
"- Respond with STRICT JSON only — a single object, no prose, no "
"markdown fences:\n"
'{"operation": "<name>", "args": {}, "confidence": <0.0-1.0>, '
'"rationale": "<at most 15 words>"}'
```

**After**:
```
"You are the intent router for Piper Morgan, a product-management "
"assistant. Your ONLY job is to select which operation(s) should "
"handle the user's message. You never answer the message yourself.\n\n"
"Rules:\n"
"- Choose exactly ONE operation name from the provided catalog — or, if "
"the message genuinely asks for more than one distinct operation, "
"return them in order as a plan (see the plan form below) — or "
f"{NONE_ROUTE} when no catalog operation applies (the message is "
"conversational, out of scope, or best answered in prose), or "
f"{CLARIFY_ROUTE} when the message is genuinely ambiguous between "
"materially different operations.\n"
"- Only use the plan form when at least two DISTINCT operations are "
"genuinely being requested. A single request, even if phrased with "
"multiple parts or clauses, is still a single operation.\n"
"- If the message contains a refusal or topic change while a flow is "
"active, route the user's actual words, not the flow's expectation.\n"
"- Extract obvious arguments (issue numbers, project names, times, "
"repo names) into args as simple key/value strings.\n"
"- Respond with STRICT JSON only, no prose, no markdown fences. The "
"default reply is a single object:\n"
'{"operation": "<name>", "args": {}, "confidence": <0.0-1.0>, '
'"rationale": "<at most 15 words>"}\n'
"- For a genuine multi-operation request only, reply with a plan "
"object instead:\n"
'{"outcome": "plan", "operations": [{"operation": "<name>", "args": {}, '
'"confidence": <0.0-1.0>, "rationale": "<at most 15 words>"}, ...]}'
```

Also the catalog header in `build_routing_prompt`, which is the literal phrase Arch's memo
quoted ("the prompt says 'choose exactly one name'"):

**Before**: `"Operation catalog (choose exactly one name):"`

**After**: `"Operation catalog (choose exactly one — or, for a genuine multi-operation "
"request, return an ordered plan; see the system instructions):"`

Single-op stays the DEFAULT and FIRST clause in both the rule text and the JSON-shape
ordering; the plan is introduced as the exception in both places (pinned by
`test_plan_rule_in_prompt_is_the_exception_not_the_default`, which asserts the single-op JSON
form's string index precedes the plan form's in `_SYSTEM_PROMPT`).

**Repair-retry prompt (attempt 2)** — Arch's flagged gap, now shape-aware:

*Before*: `"Reply again with STRICT JSON only, exactly one object of the form {...}."` (hard-coded
single-op — would have silently told a model that correctly reached for a plan on attempt 1 to
collapse to one operation on the repair).

*After*: `"Reply again with STRICT JSON only — either a single object of the form {...}, or,
only if the message genuinely asks for 2 or more distinct operations, a plan object of the
form {"outcome": "plan", "operations": [{...}, ...]}."`

## 3. Validation rules, as implemented

- `_validate_operation_element` factored out of the old `_parse_and_validate` body — validates
  ONE operation object (vocabulary check against `grammar.is_valid_route`, `args` must be a
  dict if present, `confidence` numeric and clamped to [0,1]). Used identically by the
  single-op path and by every element of a plan.
- `_parse_and_validate` branches on `parsed.get("outcome") == "plan"`:
  - `operations` must be a list, length ≥ 2, else refused (same parse-failure/repair path a
    bad single object gets).
  - every element validated via `_validate_operation_element`; the FIRST invalid element
    refuses the WHOLE plan (never partial acceptance).
  - a validated element naming `NONE`/`CLARIFY` refuses the whole plan (sentinels are not
    operations — a plan-specific rule beyond what the grammar's `is_valid_route` alone would
    catch, since `is_valid_route` accepts them for the single-op case).
  - fewer than 2 DISTINCT operation names among the validated elements refuses the whole plan
    (a plan whose elements collapse to one repeated operation is not a plan).
  - the non-plan branch (no `"outcome"` key, or `"outcome"` != `"plan"`) is UNCHANGED —
    delegates straight to `_validate_operation_element`, byte-identical return shape.
- `_extract_json_object` replaces the one-level-of-nesting `_JSON_OBJECT_RE` regex with a
  string-aware balanced-brace scanner (tracks quoted strings incl. escaped quotes so an
  internal `{`/`}` inside a string value is never mistaken for structure). Necessary, not
  cosmetic: a plan's own `operations[i].args` is a THIRD brace level (plan → operations[i] →
  args), which the old regex's fixed one-level repeat group could not represent at all.
  Verified byte-identical on every single-op reply the old regex already matched (all
  pre-existing router tests pass unchanged).

## 4. Consumption — the rail-loop wiring, and the honest gap

Arch's ruling explicitly deferred consumption ("did not design or verify the actual JSON-
repair-retry interaction with a list response... flag this to whoever builds it, not solved
here" — that line was about the repair prompt, but the same "not solved here" framing applies
to the whole dispatch side). I built the smallest wiring that reuses unit 4's OWN hand-off
mechanism rather than inventing a second one.

**`inversion_live.py`**: new `PLAN_STAND_DOWN` reason constant (sibling to
`MULTI_INTENT_SPLIT_STAND_DOWN`) and `_resolve_plan_for_dispatch(operations, grammar, cats,
threshold)`, which validates EVERY element against the SAME four dispatch conditions a
single-op decision is checked against inside `consult_inversion_live` (live match via one of
the three #1667 naming surfaces, confidence ≥ threshold, rail-dispatchable, the #1677 effect
guard — READ or an individually allowlisted WRITE). ALL-OR-NOTHING: one non-dispatchable
element returns `(None, "plan_<reason>")` and the WHOLE plan is declined — this is stricter
than unit 4's own "a sibling the rail can't serve declines the whole turn" rule, and for a
structural reason, not a stylistic one: a real sibling that a consult declines falls back to
its OWN surface-1 Intent (surface 1 already claimed that half deterministically); a plan
element has no surface-1 Intent of its own to fall back to, because the whole plan came from
ONE whole-message router call. There is nothing to fall back to, so nothing partial can be
served honestly.

`LiveRouteProvenance` gains `plan_operations: Optional[Tuple[Dict[str, Any], ...]] = None`. In
`consult_inversion_live`, a `decision.outcome == "plan"` at the WHOLE-MESSAGE level
(`multi_intent_sibling is None`) that validates fully publishes `reason=PLAN_STAND_DOWN` plus
`plan_operations` — mirroring the #1896 split stand-down's own shape exactly (the consult
still returns `None`, since no single `Intent` can represent 2+ operations; the provenance
record is the hand-off, peeked not taken, same as the split path). A sibling consult
(`multi_intent_sibling` set) that itself decodes a plan declines with
`reason="plan_in_sibling_unsupported"` — no segment-within-a-segment mechanism exists, and
building one was out of scope for "smallest change."

**`intent_service.py`**: `_maybe_dispatch_multi_intent_inversion`'s top guard now accepts
EITHER `MULTI_INTENT_SPLIT_STAND_DOWN` or `PLAN_STAND_DOWN`. For the plan case
(`is_plan = stand_down.reason == PLAN_STAND_DOWN`), `finals`/`routed_count` are built directly
from `stand_down.plan_operations` — no per-element consult loop, since everything was already
validated at the whole-message consult. From `rail = get_action_workflows()` onward, EVERY
line is the SAME shared code the split path already proved (rail-dispatchability check,
reads-first/first-write ordering, the sequential `_dispatch_action_rail` loop, pause-defers-
the-rest with `_compose_deferred_sibling_line`, reply composition via the orchestrator's
`_aggregate_messages`, provenance republish, `_apply_soft_offer`). Diff shape: one `if
is_plan: ... else: <original split code, unchanged> ...` branch producing `finals`, then
identical code after.

**The honest gap, found and documented rather than hidden**: a plan element carries no
independent text SEGMENT of the user's own words — unlike a real sibling, whose segment is a
literal slice of the message (from `sibling_segments`' claim-span mechanism). I use the
router's own per-element `rationale` (falling back to the bare operation name if absent) as
BOTH the deferred-sibling label in the reply AND the element's `Intent.original_message`. This
matters beyond cosmetics, confirmed by direct measurement during this build: feeding the WHOLE
multi-clause message into a delete-todo element's `original_message` (my first attempt) fed
`destructive_confirm._named_delete_target` the string `"what are my todos and delete my
hydrate reminder"`, which stopword-strips to `"what are hydrate"` — a fragile 1-of-3-word fuzzy
match that happened to still clear the 0.3 threshold in this specific case (verified via direct
call: `fuzzy_todo_match_score("what are hydrate", "hydrate") == 0.333`), but is not a match I'd
trust in general (a different todo whose own text happened to contain "what" or "are" would
score too, or the SAME target words appearing near a different plan element's clause could
misfire). Switching to `rationale` alone (`"delete hydrate reminder"` → `_named_delete_target`
→ `"hydrate"`, exact) fixed this cleanly and is what shipped. Still an honest limitation to
name: a rationale is the router's short paraphrase, not the user's own words, so anything that
echoes it back verbatim in a confirm or a deferred-line quote is echoing the router's phrasing.

No new dispatch site: `self._dispatch_action_rail(` appears exactly once in
`_maybe_dispatch_multi_intent_inversion`'s source (pinned by
`test_no_second_dispatch_site_for_the_plan_path`); `dispatch_workflow` does not appear in it at
all (unchanged from unit 4). `MAX_DISPATCH_SITES`/`TestExtractionPatternRatchet` untouched (no
new `*_PATTERNS` literal anywhere in this unit).

## 5. Tests — new/changed, file::name → what it asserts

**`tests/unit/services/intent_service/test_inversion_router_1595.py`** (10 new, all under
`TestRouteEnforcement`, stubbed `ScriptedLLM`, zero live calls):
- `test_valid_plan_reply_is_accepted` — a 2-op plan parses in one call; `operation`/`args` stay
  at single-op defaults; `route_label == "PLAN[list_todos_query→delete_todo]"`.
- `test_plan_with_nested_args_parses_past_the_old_one_level_regex` — an element's own nested
  `args` dict (3 brace levels total) parses correctly — the property that made the
  balanced-brace scanner necessary, not just tidier.
- `test_plan_of_fewer_than_two_elements_is_refused_never_partial` — 1-element plan → refused on
  both attempts, `operations == []`.
- `test_plan_naming_an_invented_operation_is_refused_never_partial` — one bad element
  invalidates the whole plan; error names the invented op.
- `test_plan_with_a_malformed_element_is_refused_never_partial` — an element missing
  `"operation"` invalidates the whole plan.
- `test_plan_of_identical_operations_collapses_and_is_refused` — 2 elements, same operation
  name → refused ("DISTINCT" in the error).
- `test_plan_element_naming_none_or_clarify_is_refused` — a `NONE` sentinel as a plan element
  is refused even though `is_valid_route` alone would accept it for a single object.
- `test_first_attempt_malformed_plan_is_repaired_and_accepted` — attempt 1 malformed, attempt 2
  a valid plan → the REPAIRED PLAN is accepted (not collapsed to single-op); repair prompt
  restates both shapes (asserted via substring checks on `llm.calls[1]["prompt"]`).
- `test_repaired_single_object_still_accepted` — the other half of shape-awareness: attempt 1
  malformed, attempt 2 a valid single object → unaffected by the plan addition.
- `test_plan_rule_in_prompt_is_the_exception_not_the_default` — single-op JSON form's string
  index precedes the plan form's in `_SYSTEM_PROMPT`; catalog header carries both.

**`tests/unit/services/intent_service/test_inversion_live_1595.py`** (5 new, `TestPlanOutcome`,
real `consult_inversion_live`, stubbed `ir.route`):
- `test_fully_eligible_plan_hands_off_via_plan_stand_down` — every element passes the four
  dispatch conditions → consult returns `None`; provenance carries
  `reason=PLAN_STAND_DOWN`, `routed_live=False`, `plan_operations` with correct per-element
  `args`/`confidence`/`intent_category`; ONE router call (not one per element); decision log
  line carries `plan_operation_names`.
- `test_one_ineligible_element_declines_the_whole_plan_not_live` — `delete_todo` not named live
  → whole plan declines, `reason="plan_not_live"`, `plan_operations is None`.
- `test_sub_threshold_element_declines_the_whole_plan` — one element below threshold → whole
  plan declines, `reason="plan_sub_threshold"`.
- `test_sibling_consult_asking_for_a_nested_plan_is_unsupported` — `multi_intent_sibling` set +
  a plan decision → `reason="plan_in_sibling_unsupported"`.
- `test_default_empty_flag_costs_zero_work_even_for_a_plan_shaped_message` — flag unset → zero
  work, router never consulted, no log line (same DEFAULT-EMPTY pin as every other outcome).

**`tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py`** (6 new:
`TestPlanMessageShape` 1 + `TestPlanOutcome` 5, real `process_intent`/`aiosqlite`, stubbed
whole-message `ir.route`):
- `TestPlanMessageShape::test_the_plan_message_does_not_split_at_surface_one` — the denominator:
  `PLAN_MESSAGE` ("what are my todos and delete my hydrate reminder") verified via the REAL
  `PreClassifier.detect_multiple_intents` to return 0 intents post-Phase-3-deletion — the exact
  #1897 shape unit 4's sibling path can never reach.
- `TestPlanOutcome::test_read_then_write_dispatches_through_the_rail` — 2-op plan (read+write):
  read runs, write's #1190 confirm arms (`'Delete todo: "hydrate"? (yes/no)'` — via the
  rationale-derived `original_message`, matching the fix in §4), nothing deferred (nothing
  after the one write), `multi_intent_inversion is True`.
- `::test_the_confirmed_yes_deletes_exactly_the_named_row` — the real #1190 arm on the real
  session store; the next turn's "yes" deletes exactly the named row.
- `::test_two_writes_first_arms_second_is_named_and_never_queued` — 2-op plan, both
  `delete_todo` (mirrors the split suite's own `TestPauseStopsTheTurn` precedent — same
  operation twice, targeting two different rows via two different rationales): first arms,
  second is named verbatim by its rationale in the deferred line, never queued; the pending
  offer's bound `delete_todo_resolved.text` is the FIRST target only.
- `::test_a_non_plan_stand_down_reason_never_engages_the_rail_loop` — direct call to
  `_maybe_dispatch_multi_intent_inversion` (not full `process_intent` — `PLAN_MESSAGE`
  genuinely never splits, so the legacy fallback would need a working classifier LLM double,
  which is orthogonal to what this test proves) across three decline reasons
  (`plan_not_live`/`plan_sub_threshold`/`plan_not_rail_dispatchable`) — the function's top-level
  guard declines every one without touching the rail.
- `::test_no_second_dispatch_site_for_the_plan_path` — structural pin: exactly one
  `self._dispatch_action_rail(` call site in the function's source, `dispatch_workflow` absent,
  `PLAN_STAND_DOWN` present.

Also fixed in passing (pre-existing on the file, unrelated to this unit but caught because my
first read of the file was one line short of its true EOF): restored a dangling assertion
(`assert SEG_SESSION not in messages[0][0]`) to its correct home inside
`TestNoCrossSiblingState::test_each_sibling_sees_only_its_own_segment` after a bad edit
briefly orphaned it — caught by re-running the suite before moving on, not left for the Lead
to find.

## 6. Docs

- `docs/internal/architecture/current/intent-routing-stack.md` — new subsection immediately
  after unit 4's own block (right after its "Denominator" paragraph, before the pre-claim
  shadow probe entry): the plan shape, the prompt clause, validation rules, how the rail
  consumes it (including the all-or-nothing-is-stricter-than-unit-4 distinction), the honest
  gap, and an explicit "what is NOT measured here" closing paragraph naming the Lead's pending
  before/after single-op accuracy measurement as unclaimed by this entry.
- `docs/internal/architecture/decisions/decisions.log` — one entry (2026-09-28 09:1x PT),
  summarizing the shape, the consumption wiring, the known gap, and every gate result below.

## 7. Gates — commands, output, EXIT STATUS

```
$ ruff format services/intent_service/inversion_router.py services/intent_service/inversion_live.py \
    services/intent/intent_service.py tests/unit/services/intent_service/test_inversion_router_1595.py \
    tests/unit/services/intent_service/test_inversion_live_1595.py \
    tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py
1 file reformatted, 5 files left unchanged   [EXIT 0]

$ ruff check --fix <same file set>
All checks passed!   [EXIT 0]

$ env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
    POSTGRES_PORT=5433 venv/bin/python -m pytest tests/unit/services/intent_service/ tests/unit/services/intent/ -q
4978 passed, 15 warnings in 136.02s   [EXIT 0]
(all 15 warnings pre-existing `@pytest.mark.asyncio`-on-sync-test warnings in OTHER files,
unrelated to this unit — confirmed by grep; none in the three files this unit touched)

$ env ... venv/bin/python -m pytest tests/test_architecture_enforcement.py -q
63 passed, 1 xfailed   [EXIT 0]   (the 1 xfailed is pre-existing, unrelated)

$ scripts/run-sweep.sh ratchets
73 passed, 1 xfailed (test_completion_ratchets.py + test_architecture_enforcement.py)   [EXIT 0]
mypy gate (#1436, venv-mypy-gate/): "all 24 ratcheted codes at ceiling" — total=1121, identical
per-code counts to the existing ceiling (arg-type=364, assignment=227, attr-defined=69,
call-arg=3, call-overload=6, dict-item=5, has-type=2, index=10, list-item=2, misc=77,
no-redef=3, operator=63, override=17, return=1, return-value=48, union-attr=141, valid-type=14,
var-annotated=69). NO ratchet moved; none needed updating.
```

**Which ratchets moved, and why**: none. `MAX_DISPATCH_SITES` (#1124) — unchanged (0 new
dispatch sites; verified structurally in `test_no_second_dispatch_site_for_the_plan_path` and
by the ratchets-gate pass). `TestExtractionPatternRatchet` (#1595/#1717 argument-extraction
moratorium) — unchanged (no `*_PATTERNS` literal added anywhere; the router's grammar/parser
changes are not regex extraction, they're JSON-schema validation). Mypy gate (#1436) — all 24
codes at their existing ceiling, no drift in either direction.

## Verified how

**Method**: every claim above is the literal output of the command shown in §7, run this
session, this turn — never a remembered or five-minutes-ago result. Every test file change was
read back via `git diff --stat` before the final gate run to confirm no stray edits (this is
how the `TestNoCrossSiblingState` dangling-assertion bug from a bad `Edit` match was caught).

**Layer**: deterministic/source only. Every new and existing test in the three touched files
uses a stubbed `inversion_router.route` (`ScriptedLLM` in the router file, `_stub_route`/
`_route_plan` in the consumption files) — NO live LLM call anywhere in this unit's own tests
(the two `@pytest.mark.llm`-marked tests in `test_inversion_router_1595.py` were explicitly
deselected via `-k "not llm"` in every router-file run, and were never touched by this build).
This proves the parse contract, the dispatch-time validation, the hand-off mechanism, and the
rail-loop sequencing — it does NOT prove the live constrained router reliably reaches for a
plan on a genuinely multi-op message, nor that the new prompt clause is neutral on single-op
routing accuracy. Both are explicitly out of scope per the dispatch instruction (no live LLM
calls; the Lead runs the before/after scorer separately) and are named as pending, not claimed,
in both the docs subsection and this log.

**Denominator**: 3 files touched (`inversion_router.py`, `inversion_live.py`,
`intent_service.py`) + 3 test files touched (one new class each in
`test_inversion_router_1595.py`/`test_inversion_live_1595.py`, one new class-pair in
`test_inversion_multi_intent_unit4_1595.py`) + 2 docs surfaces updated
(`intent-routing-stack.md`, `decisions.log`). 21 new tests total (10 + 5 + 6). Full
`tests/unit/services/intent_service/` + `tests/unit/services/intent/` (4978 tests) run green;
`tests/test_architecture_enforcement.py` (64 tests incl. 1 pre-existing xfail) run green;
`scripts/run-sweep.sh ratchets` (73 tests + the mypy gate) run green. NOT run, by explicit
instruction: the live-corpus before/after scorer (the Lead's, separate, pending) and anything
requiring `ANTHROPIC_API_KEY`/a real model call.

## Memory & briefing surfaces referenced this session

**Referenced**:
- `docs/internal/architecture/current/intent-routing-stack.md` — the full #1595 chain, unit 4's
  mechanism (READ-first, confirm-ends-turn, peek-not-take provenance coupling), and its own
  denominator paragraph that named this unit's exact scope.
- Arch's grammar-shape ruling memo — the load-bearing spec for the router-side changes.
- GitHub #1897/#1606 — the measured defect and corpus source this unit closes/partially
  addresses.
- `tests/unit/services/intent_service/test_inversion_multi_intent_unit4_1595.py`'s own file
  docstring — named the exact residual ("closing that needs the router to return an ordered
  PLAN") this unit was built to close, in advance, by a previous session.

**Loaded but not referenced**: CLAUDE.md's full worktree/mailbox/sign-off discipline sections
(no commits made this session, per dispatch instruction — not applicable); the glossary; the
canonical-ops-recipes doc.

**Wanted but not found**: none — the Arch memo and the routing-stack doc together specified
everything needed for the grammar shape; the consumption wiring's shape was my own design
choice within the "smallest honest version, report the gap" latitude the dispatch explicitly
granted.
