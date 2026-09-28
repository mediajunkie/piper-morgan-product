# Session log — prog (Coding Agent), Claude Code

**Model**: Sonnet 5 (claude-sonnet-5)
**Dispatched by**: Lead Developer, for #1899
**Date**: 2026-09-27
**Scope**: reads-only release for armed-carrier off-intent discriminators (#1899). Reads/writes only
within the assigned files — no git commit/stage/index touch per dispatch instructions (Lead owns the
commit).

## Task

Build the reads-only release CXO ruled (ratified, Arch concurred + confirmed scope = both real
discriminator sites) for `#1899`: `todo_handlers.handle_reminder_task_turn` (#1654) and
`first_contact.handle_ftux_interview_turn` (#1688) each call `PreClassifier.pre_classify` directly
to decide "unrelated command, or the answer to my question?" — a #1595 Phase 3 deletion narrowed
what that deterministic surface can still claim, and `consult_inversion_live` cannot backfill because
it stands down on any turn that popped a pending offer (exactly every carrier turn). Fix: a second,
narrower oracle that consults the Inversion router directly and releases ONLY on a live-flagged,
high-confidence READ verdict.

## What shipped

### 1. New helper: `services/intent_service/inversion_live.py::read_op_claims_turn`

`async def read_op_claims_turn(message, *, session_id, user_id, intent_service) -> Optional[str]`

Consults `inversion_router.route(...)` **directly** (never through `consult_inversion_live` — its
`turn_had_pending_offer` guard is exactly the stand-down this helper exists to route around).
Returns the operation name only when ALL four gates hold, else `None` (bind, unchanged):

1. `decision.outcome == "operation"` (a concrete operation — none/clarify/refused/error all bind).
2. `decision.confidence >= live_min_confidence()` (same operator threshold `consult_inversion_live`
   dispatches on; default 0.8).
3. The rail entry declares READ effect — checked as `entry.effect == EffectClass.READ` directly,
   **deliberately NOT** `_effect_guard_passes(entry, ...)` wholesale: that function also passes an
   individually allowlisted WRITE (`FLIP_WRITE_ALLOWLIST`, e.g. `create_todo`), which is correct for
   live dispatch but wrong here — CXO ruled READ-verdict-only, no exception for any write, allowlisted
   or not.
4. The operation is inversion-routable under the **current** live flag (`resolve_live_match(...)`
   non-`None` against `live_categories()`) — so an unflipped deployment, or any operation nobody has
   reviewed and flagged live, behaves exactly as today: bind. This also makes the flag-off case a
   true zero-work / zero-router-call path (same DEFAULT-EMPTY discipline `consult_inversion_live`
   follows).

A router exception (transport failure, anything) is caught, logged
(`armed_carrier_read_release_declined`, `reason="router_exception"`), and treated as `None` — never
raises into the carrier turn (#1423 discipline, matching `consult_inversion_live`'s own belt-catch).
One structured log line either way: `armed_carrier_read_release` (fired, with
operation/canonical/confidence/live_match) or `armed_carrier_read_release_declined` (any gate held,
with operation/confidence/reason — `router_<outcome>`, `sub_threshold`, `not_rail_dispatchable`,
`not_read_effect`, `not_live`, or `router_exception`).

Placed in `inversion_live.py` (not a sibling module) because it reuses that module's
`live_categories()`, `live_min_confidence()`, `resolve_live_match()`, `_category_by_operation()`
module-level functions directly — no parallel implementation of any of them.

### 2. Wiring — both real sites, same shape

**`services/intent_service/todo_handlers.py::handle_reminder_task_turn`** (~line 1710, after the
existing `PreClassifier.pre_classify` check, before the bind):

```python
claimed = PreClassifier.pre_classify(text)
if claimed is not None:
    ...
    return None

# #1899 — surface 1 declined; a second, narrower oracle catches what
# #1595 Phase 3's deletions no longer let it claim. ...
from services.intent_service.inversion_live import read_op_claims_turn

read_op = await read_op_claims_turn(
    text, session_id=session_id, user_id=user_id, intent_service=intent_service
)
if read_op is not None:
    logger.info(
        "reminder_task_question_command_released",
        session_id=session_id,
        claimed_action=read_op,
    )
    return None

# The turn IS the task.
```

**`services/intent_service/first_contact.py::handle_ftux_interview_turn`** (~line 536, identical
shape, `ftux_interview_command_released` log event, same helper call).

Both docstrings updated with a `#1899:` paragraph explaining the second-oracle addition and why
gating on READ-effect alone is structurally safe (a READ can never sensibly complete "remind me to
___" or stand in for an FTUX answer).

### 3. Tests (deterministic — router always stubbed, zero live LLM calls)

**New file**: `tests/unit/services/intent_service/test_inversion_read_release_1899.py` — 14 cases,
direct unit tests of `read_op_claims_turn` itself:

- `TestReadOpClaimsTurnGates::test_read_op_at_or_above_threshold_releases` — READ @0.8 + live →
  releases `list_reminders_query`.
- `::test_read_op_below_threshold_binds` — READ @0.5 → `None` (gate 2).
- `::test_write_op_high_confidence_binds` — WRITE `create_todo` @1.0, even live-flagged and on
  `FLIP_WRITE_ALLOWLIST` → `None` (gate 3, READ-verdict-only, no write exception).
- `::test_read_op_not_live_flagged_binds` — READ @0.95 but a DIFFERENT group flagged live → `None`
  (gate 4).
- `::test_non_operation_outcomes_bind[none|clarify|refused|error]` — parametrized, all → `None`
  (gate 1).
- `::test_non_rail_operation_binds` — router names an operation with no rail entry → `None`.
- `::test_flag_off_binds_and_router_not_called` — empty/unset flag → `None`, **and asserts the
  router stub was never invoked** (DEFAULT-EMPTY zero-work pin).
- `::test_router_exception_binds_and_never_raises` — stubbed `route` raises `RuntimeError` → `None`,
  no exception escapes.
- `::test_empty_message_binds` — empty message → `None`.
- `TestAdversarialThresholdBoundary::test_boundary_releases_at_exactly_the_threshold` — "what's for
  dinner", stub READ @0.8 (== `live_min_confidence()`) → releases (>= threshold).
- `::test_boundary_binds_just_under_the_threshold` — same phrase, stub @0.79 → binds (< threshold).
  Both carry an explicit class docstring stating this is a **deterministic exercise of the gate's own
  boundary behavior against a scripted stub, NOT a measurement of what the real router would return**
  for that phrasing (unmeasured, needs a live pass, PM budget) — and names the actual defense against
  over-release on an ambiguous question-shaped task subject as (a) gate 3's READ-effect requirement
  (three independent things — real read op, real confidence, real live-flagged group — all have to
  align for a false release) plus (b) the carrier's own pre-existing acceptance-contract
  STATE_QUESTION path, a third disposition this helper never competes with.

**`tests/unit/services/intent_service/test_task_clarify_1654.py`** — `TestTaskTurnHandlerSeam` (calls
`handle_reminder_task_turn` directly, no explosive-LLM svc):
- `test_read_op_release_via_inversion_router` — "list my reminders", stub → `list_reminders_query`
  @0.95, `read_status` live → `result is None` (released).
- `test_write_op_still_binds_as_task` — "buy milk", stub → `create_todo` @1.0 → binds
  (`**buy milk**` in the reply).
- `test_preclassifier_claim_releases_without_calling_router` — "show my todos" (still claimed at
  surface 1) with the live flag deliberately SET to `read_status` (so a wrongly-reached router call
  would be observable) and a call-recording stub → `result is None` **and `calls == []`** (precision
  on cost: the router genuinely isn't consulted when surface 1 already released).

Also **restored** `TestNoTaskClarifyEndToEnd::test_off_intent_command_releases_and_routes** to "list
my reminders" (the phrase the discovered-gap docstring had swapped to "show my todos" for) — now goes
through the real fix end-to-end via `svc.process_intent`: env `create_reminder,read_status`, stub
`route` → `list_reminders_query` @0.95 for the release itself, plus one `_stub_classify_once` call
(same idiom `test_full_restatement_routes_normally` already uses) for the turn's *subsequent*
routing, because releasing the carrier still lands this turn inside `turn_had_pending_offer=True`
(the pop already happened), which stands `consult_inversion_live` down to the LLM-classifier lane for
the rest of the turn — a documented, **different**, unrelated seam #1899 doesn't touch. Asserts
`mock.create_todo.assert_not_awaited()`, `"saved reminders" in r2.message`, and the task-question kind
is gone from stored offers (abandoned, not re-armed).

**`tests/unit/services/intent_service/test_ftux_interview_1688.py`** — `TestHandleFtuxInterviewTurn`
(calls `handle_ftux_interview_turn` directly):
- `test_read_op_release_via_inversion_router` — "list my reminders" → released (`turn is None`, no
  context bind).
- `test_write_op_still_binds_as_answer` — work-talk phrase with stub → `create_todo` @1.0 → still
  binds whole (`route_to_floor` True, context bound verbatim).
- `test_preclassifier_claim_releases_without_calling_router` — "show my todos" with `read_status`
  live + call-recording stub → `turn is None` and `calls == []`.

`test_preclassifier_claimed_command_releases_unbound` (the existing "show my todos" gap-note test)
left unmodified — no gap for that phrase (TODO_QUERY_PATTERNS untouched by the deletion); the new
"list my reminders" case above is what demonstrates #1899's actual recovery at this carrier.

### 4. Docs

- `docs/internal/architecture/current/intent-routing-stack.md` — the "fifth consumer" paragraph
  rewritten: records the fix mechanism (four gates, direct router consult bypassing
  `consult_inversion_live`'s stand-down, cost = one router call only on an armed-answer turn where
  surface 1 already declined), and states plainly that a **WRITE-destination** corpus row deleted in
  a future Phase 3 pass is **still a live erosion risk** for these two carriers — the reads-only
  release structurally cannot and must not cover it. Points at the new test file + both carriers'
  seam tests.
- `docs/internal/architecture/decisions/decisions.log` — one entry appended (after Arch's concur
  entry, file is append-only chronological) recording the ship with the gate list, test counts, and
  full-sweep results.

### 5. Lint / format

`ruff format` (6 files unchanged — already formatted) + `ruff check --fix` (all checks passed, no
fixes needed) on: `inversion_live.py`, `todo_handlers.py`, `first_contact.py`,
`test_task_clarify_1654.py`, `test_ftux_interview_1688.py`, `test_inversion_read_release_1899.py`.

## Gate results (every command run this session, exact tail output)

```
$ venv/bin/python -m pytest tests/unit/services/intent_service/test_inversion_read_release_1899.py -v
14 passed in 0.42s

$ venv/bin/python -m pytest tests/unit/services/intent_service/test_task_clarify_1654.py tests/unit/services/intent_service/test_ftux_interview_1688.py -v
68 passed in 5.26s

$ venv/bin/python -m pytest tests/unit/services/intent_service/ tests/unit/services/intent/ -q
4951 passed, 15 warnings in 138.31s   (exit code 0; warnings are pre-existing unawaited-mock/pytest-marker noise unrelated to this change)

$ venv/bin/python -m pytest tests/test_architecture_enforcement.py -q
63 passed, 1 xfailed in 11.58s
(extraction ceiling confirmed unchanged: tests/test_architecture_enforcement.py:2255 "pre-classifier": 558 — no pattern literals added by this change)

$ venv/bin/python -m pytest tests/unit/test_inversion_phase3_deletion_1595.py -q
19 passed in 2.85s

$ scripts/run-sweep.sh ratchets
73 passed, 1 xfailed in 18.79s
--- mypy per-code gate (#1436) ---
mypy gate: all 24 ratcheted codes at ceiling (total=1121; arg-type=364, assignment=227, attr-defined=69, call-arg=3, call-overload=6, dict-item=5, has-type=2, index=10, list-item=2, misc=77, no-redef=3, operator=63, override=17, return=1, return-value=48, union-attr=141, valid-type=14, var-annotated=69)
```

No ratchet moved (extraction stayed at 558; mypy gate at ceiling for all 24 codes, unchanged from
before this change — the new code is fully typed against the existing signatures it calls).

## Verified how

**Method**: ran every gate command listed above directly this session and quoted its actual tail
output (no command run more than a few minutes before being quoted; nothing carried from an earlier
check). **Layer**: deterministic unit/integration test layer only — the Inversion router
(`inversion_router.route`) is monkeypatched to a fixed `RoutingDecision` in every test that touches
`read_op_claims_turn`, directly or via the two carriers; **no live LLM call was made anywhere in this
session** (confirmed by the explosive-LLM fixture in `test_task_clarify_1654.py`'s `svc` fixture
surviving the restored e2e test, and by the DEFAULT-EMPTY / call-recording tests asserting the router
stub itself was never invoked on the cost-precision paths). The adversarial threshold-boundary pass is
explicitly NOT a live-router measurement — its own test-class docstring says so, because the router's
real behavior on a question-shaped task-intended phrase is genuinely unmeasured here. **Denominator**:
14/14 new helper-gate tests pass; 6/6 new carrier-wiring tests pass (3 per carrier) plus the 1 restored
e2e test; all 4951 tests in `tests/unit/services/intent_service/` + `tests/unit/services/intent/` pass
(full directory run, not a filtered subset); `tests/test_architecture_enforcement.py` 63/63 (+1
xfailed, pre-existing) with the specific extraction-ceiling assertion checked by name; the dedicated
Phase-3-deletion regression file 19/19; `scripts/run-sweep.sh ratchets` — both pytest ratchet files
plus the pinned-venv mypy gate — all 24 ratcheted mypy codes at ceiling, none moved.

**Not done / explicitly out of scope this session**: no git add/commit/push (dispatch instructions —
Lead owns the commit); no live LLM/router call anywhere; no env var or feature-flag default changed in
any non-test file (`PIPER_INVERSION_LIVE_CATEGORIES` is read at call time as before — nothing here
turns any category live by default). Deploy hold remains PM's, per both rulings' own framing.

## Files touched

- `services/intent_service/inversion_live.py` — new `read_op_claims_turn` helper + docstring note.
- `services/intent_service/todo_handlers.py` — wiring in `handle_reminder_task_turn` + docstring.
- `services/intent_service/first_contact.py` — wiring in `handle_ftux_interview_turn` + docstring.
- `tests/unit/services/intent_service/test_inversion_read_release_1899.py` — new file, 14 tests.
- `tests/unit/services/intent_service/test_task_clarify_1654.py` — 3 new seam tests + restored e2e
  test.
- `tests/unit/services/intent_service/test_ftux_interview_1688.py` — 3 new seam tests.
- `docs/internal/architecture/current/intent-routing-stack.md` — fifth-consumer paragraph updated.
- `docs/internal/architecture/decisions/decisions.log` — one entry appended.

## Memory & briefing surfaces referenced this session

**Referenced**:
- `docs/internal/architecture/current/intent-routing-stack.md` — mandatory pre-read per dispatch;
  informed the exact framing of surface 1 / the fifth-consumer gap / the #1595 Phase 3 procedure.
- The two rulings in `mailboxes/lead/inbox/` (CXO's + Arch's) — the exact four-gate mechanism, the
  READ-verdict-only asymmetry, the both-sites scope, the adversarial-boundary ask.
- `tests/unit/services/intent_service/_inversion_pin_helper.py` — the `stub_router_operation` /
  `assert_inversion_routes` idiom mirrored (never call the real router, monkeypatch
  `inversion_router.route` module-level so any local `from ... import route` picks up the patched
  attribute).
- Existing test idioms in `test_task_clarify_1654.py` (`_ExplosiveLLM`, `_stub_classify_once`,
  `_route_reminder_creation_via_inversion`) — informed both the e2e restoration approach and why a
  seam-level (not full e2e) test was the right layer for the new gate coverage.

**Loaded but not referenced**: CLAUDE.md's worktree/mailbox/sign-off sections (dispatch instructions
were explicit: reads/writes only, no git operations, so the commit/push discipline sections did not
apply this session).

**Wanted but not found**: nothing — the two rulings plus the routing-stack doc plus the existing test
files gave complete, unambiguous grounding for every gate decision.
