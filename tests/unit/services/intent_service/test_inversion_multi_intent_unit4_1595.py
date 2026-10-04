"""#1595 unit 4 — a turn surface 1 SPLITS is routed sibling-by-sibling through
the ONE #1124 rail (Arch's shape (ii), ruled 2026-09-25, sequencing rules
approved 2026-09-26).

What this closes: #1896's stand-down stopped the live consult from answering
one half of a two-part turn and silently dropping the other — correct, but it
also meant a split turn could never take the inversion at all. Unit 4 replaces
the stand-down FOR THE TURNS IT HANDLES: each sibling consults on its OWN text
segment (derived from the claim spans surface 1 now retains — no second regex
pass, no new pattern literal, ``TestExtractionPatternRatchet`` untouched), and
the resulting siblings run SEQUENTIALLY through ``_dispatch_action_rail``, the
same block the single-intent path runs. **No second dispatch site**: shape (i)
(a rail leg inside ``IntentOrchestrator._execute_single``) was ruled out
precisely because it would add one; ``MAX_DISPATCH_SITES`` is unchanged.

Arch's three sequencing rules, each pinned below:

1. READ siblings first (message order), then the FIRST write/destructive one.
2. Pause = stop — the sibling that arms a pending action ends the turn, and
   every sibling after it is NAMED in the reply, never queued for auto-run.
3. No cross-sibling state.

⚠️ LAYER HONESTY (m-43), inherited from the sibling flip files: the router is a
DETERMINISTIC stub keyed by segment text, so these tests prove *the path, the
ordering, the pause and the reply composition* — they do NOT prove the live
constrained router draws better operations per segment than the whole-message
draw did. That is observable only live, in ``inversion_live_decision``
telemetry (which now carries ``sibling_index``/``sibling_count``). What is NOT
faked here is the splitter: ``PreClassifier.detect_multiple_intents`` is the
real one on every test, so every message below actually splits in production.

⚠️ DENOMINATOR, stated rather than left to be discovered — the shapes the
dispatch's own acceptance list named could not be built as written, and the
reason is a property of surface 1, not of this path (measured 2026-09-26):
**surface 1's splitter cannot emit a WRITE or DESTRUCTIVE sibling at all.**
Every action in its ``pattern_groups`` is a read lane, and the #1527/#1756/
#1794/#1881 guards make those lanes DECLINE a destructive ask outright — so
"what are my todos and delete my hydrate reminder" comes back as ONE intent
(the todos half) and "delete my hydrate reminder and what are my todos" as
ZERO. A destructive sibling therefore exists only when a CONSULT produces one,
which is exactly what tests 3/4/5 below construct. Residual, filed not hidden:
because those two phrasings do not split, they never reach the #1896 guard
either — the whole-message consult can still answer the delete half and drop
the todos half. Closing that needs the router to return an ordered PLAN
(option (b)), not this unit.
"""

import contextlib
import datetime as _dt
from types import SimpleNamespace
from uuid import uuid4

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import SessionActivityDB  # noqa: E402
from services.domain.models import Todo  # noqa: E402
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service import inversion_live  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.intent_service.inversion_live import (  # noqa: E402
    MULTI_INTENT_SPLIT_STAND_DOWN,
    consult_inversion_live,
    sibling_segments,
)
from services.intent_service.inversion_router import RoutingDecision  # noqa: E402
from services.intent_service.pre_classifier import PreClassifier  # noqa: E402
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.intent_service.workflow_dispatcher import (  # noqa: E402
    FLIP_WRITE_ALLOWLIST,
    get_action_workflows,
)
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.shared_types import EffectClass  # noqa: E402

_USER = "3f7b8a52-1595-4b00-9e00-000000001595"  # valid UUID: survives principal parsing

# The three real split turns this file uses. Each is verified to split by the
# REAL splitter in TestTheShapesAreReal below — a test built on a message that
# doesn't actually split would pass vacuously (#1829's shape).
#
# #1595 Phase 3 (second deletion, 2026-09-27): every turn here used to pair
# "what are my todos" (TODO_QUERY_PATTERNS) with a second claim — that list's
# literals are now deleted, so surface 1 can no longer claim the todos half at
# all (confirmed: detect_multiple_intents("what are my todos and ...") now
# returns 0 intents, not 1). TURN_READ_FIRST, TURN_ISSUES_FIRST, and
# TURN_TWO_NAMED collapse onto the SAME still-splitting phrase — deliberately
# redundant text, not a bug: each test class below still proves something
# DIFFERENT by choosing a different CONSULT mapping over the same two
# segments (which sibling is READ/WRITE/kept/consulted is a per-test choice,
# not a property of the turn text). list_todos_query survives in every test
# that dispatches it for REAL — the consult stub freely RENAMES a segment's
# dispatched action regardless of what surface 1 originally called it, so
# "list_todos_query, backed by the todo_boundary fixture" is still reachable
# by remapping whichever segment a test needs it on.
#
# #1595 Phase 3 (fifth deletion, 2026-10-02): the first segment used to be
# "what are my open issues" (GITHUB_QUERY_PATTERNS) — that list's 64 literals
# are now deleted too, so surface 1 can no longer claim it at all (confirmed:
# the paired turn collapsed from 2 intents to 1, same shape as the second
# deletion's TODO casualty above). Swapped to "what branch are we on"
# (LOCAL_GIT_STATUS_PATTERNS, unaffected by any of the five deletions to
# date, category QUERY, action local_git_status_query — a registered
# effect=READ rail key, confirmed via direct probe of
# get_action_workflows()). SESSION_ACTIVITY_QUERY_PATTERNS (the second
# segment) is untouched.
#
# #1595 Phase 3 (fourteenth deletion, 2026-10-03): SESSION_ACTIVITY_QUERY_
# PATTERNS is now `[]` too — "what did we create this session" no longer
# claims at all, degrading this pair's second half the same way the fifth
# deletion degraded the first half. Swapped the SECOND segment to "what we
# discussed yesterday was helpful" (MEMORY_PATTERNS' surviving
# `\bwhat (i|we) (said|talked|discussed)\b` literal, action get_memory — a
# registered effect=READ rail key, read_floor entry point, confirmed via
# direct probe of get_action_workflows()). The FIRST segment is ALSO swapped
# pre-emptively, from "what branch are we on" to "are we behind upstream at
# all" (LOCAL_GIT_STATUS_PATTERNS' surviving `\bbehind (?:main|origin|
# upstream|master)\b` literal — the EIGHTEENTH deletion (PARTIAL,
# scheduled later in this same batch) keeps only this one literal alive, so
# "what branch are we on" would break AGAIN the moment that deletion lands;
# this pairing survives it). Both halves measured directly via
# PreClassifier.detect_multiple_intents + sibling_segments against the live
# PreClassifier, not assumed.
TURN_READ_FIRST = "are we behind upstream at all and what we discussed yesterday was helpful"
TURN_ISSUES_FIRST = "are we behind upstream at all and what we discussed yesterday was helpful"
TURN_TWO_NAMED = "are we behind upstream at all and what we discussed yesterday was helpful"
#   #1595 Phase 3 (Arch's 2026-10-01 ruling): "what time is it" stopped being
#   an unrailed example once get_current_time got a rail entry
#   (get_current_time_entry, flip_group read_temporal) — swapped to a
#   PROVENANCE phrase (explain_suggestion, CANONICAL disposition, no
#   WorkflowEntry, deterministic surface-1 match via PROVENANCE_PATTERNS'
#   r"\bwhy did you (...suggest...)\b") so this turn still has a genuinely
#   unrailed second half.
#   #1595 Phase 3 (fourteenth deletion, 2026-10-03): this constant's first
#   half, "what branch are we on", is UNCHANGED here deliberately — it still
#   claims today (LOCAL_GIT_STATUS_PATTERNS is not yet touched by THIS
#   deletion). It WILL stop claiming once the eighteenth deletion (PARTIAL,
#   later in this same batch) lands; re-verify this constant's behavior at
#   that point rather than assuming it still holds.
TURN_UNRAILED_HALF = "what branch are we on and why did you suggest that"

# Their segments, as sibling_segments derives them (message order). Measured
# via PreClassifier.detect_multiple_intents + inversion_live.sibling_segments
# against the live PreClassifier (2026-10-03, fourteenth deletion), not
# assumed: segment 0 runs from the start of the turn up to (not including)
# the second segment's own pattern match, which for MEMORY_PATTERNS'
# `\bwhat (i|we) (said|talked|discussed)\b` begins at "what" — so segment 0
# keeps the trailing "and" exactly as the prior pairing did.
SEG_ISSUES_AND = "are we behind upstream at all and"
SEG_SESSION = "what we discussed yesterday was helpful"


def _todo(text):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=_dt.datetime(2026, 9, 25, 9, 0, tzinfo=_dt.timezone.utc),
    )


# ---------------------------------------------------------------------------
# Fixtures (the #1606/#1667 flip set, unchanged shapes)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    import services.database.session_factory as sf

    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    return store


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()


@pytest.fixture
def todo_boundary(monkeypatch):
    """The owner-scoped todo list, deterministic; delete EXPLOSIVE unless a
    test arms it. Two of the rows are named for what the SEGMENTS of the split
    turns resolve to, which is how a per-sibling confirm can name a real item:
    "are we behind upstream at all and" → "upstream check" (fuzzy match,
    0.33 score — #1595 Phase 3 fourteenth deletion, 2026-10-03: was "what
    branch are we on and" against LOCAL_GIT_STATUS_PATTERNS' own
    `\\bwhat branch are we on\\b` literal, now its surviving `\\bbehind
    (?:main|origin|upstream|master)\\b` literal, since the EIGHTEENTH
    deletion scheduled later in this same batch keeps only that one
    literal), "what we discussed yesterday was helpful" → "discussed
    yesterday" (fuzzy match, 0.4 score — was "what did we create this
    session" → "create session" against SESSION_ACTIVITY_QUERY_PATTERNS,
    which is `[]` now; both verified in
    TestTheShapesAreReal::test_segments_resolve_the_named_targets)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo("upstream check"), _todo("discussed yesterday"), _todo("hydrate")],
        "deleted": [],
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation ran "
                "without a confirmed yes on a multi-intent sibling turn"
            )
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


class _LogRecorder:
    def __init__(self):
        self.events = []

    def _rec(self, level):
        def _log(event, **fields):
            self.events.append((level, event, fields))

        return _log

    def __getattr__(self, name):
        if name in ("info", "warning", "error", "debug"):
            return self._rec(name)
        raise AttributeError(name)

    def decisions(self):
        return [f for _lvl, ev, f in self.events if ev == "inversion_live_decision"]


@pytest.fixture
def log_rec(monkeypatch):
    rec = _LogRecorder()
    monkeypatch.setattr(inversion_live, "logger", rec)
    return rec


def _route_by_segment(monkeypatch, mapping, confidence=0.95):
    """Deterministic router: segment text → operation name (None ⇒ the router
    declines that segment, which is the 'consult returned None' case)."""
    from services.intent_service import inversion_router as ir

    seen = []

    async def _route(utterance, session_state=None, **kwargs):
        seen.append(utterance)
        op = mapping.get(utterance.strip())
        if op is None:
            return RoutingDecision(outcome="none", operation=None, confidence=None)
        return RoutingDecision(outcome="operation", operation=op, confidence=confidence)

    monkeypatch.setattr(ir, "route", _route)
    return seen


def _service(monkeypatch, *, explosive_classifier=True):
    service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    if explosive_classifier:

        async def _boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — the unit-4 path must REPLACE "
                "the legacy multi-intent block for the turns it handles"
            )

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)
    return service


def _sid(tag):
    return f"sess-1595-u4-{tag}"


# ---------------------------------------------------------------------------
# 0. The shapes are REAL — the denominator for everything below
# ---------------------------------------------------------------------------


class TestTheShapesAreReal:
    def test_the_three_turns_split_into_two_rail_dispatchable_reads(self):
        rail = get_action_workflows()
        for turn, actions in (
            (TURN_READ_FIRST, ["local_git_status_query", "get_memory"]),
            (TURN_ISSUES_FIRST, ["local_git_status_query", "get_memory"]),
            (TURN_TWO_NAMED, ["local_git_status_query", "get_memory"]),
        ):
            result = PreClassifier.detect_multiple_intents(turn)
            got = sorted(i.action for i in result.intents)
            assert got == sorted(actions), turn
            for action in actions:
                assert action in rail and rail[action].effect == EffectClass.READ

    def test_segments_are_derived_in_message_order(self):
        # TURN_READ_FIRST and TURN_ISSUES_FIRST are the same phrase now (see
        # the constants block) — both assertions are the same check on the
        # same text, kept as two lines for structural parity with the two
        # named turns each test class below still references.
        assert [
            (i.action, s) for i, s in sibling_segments(TURN_READ_FIRST, _split(TURN_READ_FIRST))
        ] == [("local_git_status_query", SEG_ISSUES_AND), ("get_memory", SEG_SESSION)]
        assert [
            (i.action, s) for i, s in sibling_segments(TURN_ISSUES_FIRST, _split(TURN_ISSUES_FIRST))
        ] == [("local_git_status_query", SEG_ISSUES_AND), ("get_memory", SEG_SESSION)]

    def test_a_greeting_keeps_its_own_words_and_is_not_returned(self):
        """The greeting anchor still bounds segment 0, so 'hi piper,' does not
        ride into the first substantive half — but the greeting itself is not
        a sibling to dispatch."""
        turn = f"hi piper, {TURN_READ_FIRST}"
        segments = sibling_segments(turn, _split(turn))
        assert [i.action for i, _ in segments] == [
            "local_git_status_query",
            "get_memory",
        ]
        # #1595 Phase 3 fifth deletion (2026-10-02): was GITHUB_QUERY_
        # PATTERNS (whose own match started LATER in the string with the
        # greeting prefix — "open issues and", not the full SEG_ISSUES_AND).
        # LOCAL_GIT_STATUS_PATTERNS' literal requires the FULL "what branch
        # are we on" phrase (no shorter-prefix match exists for it), so the
        # greeting prefix does NOT shift where this segment starts — it is
        # the full SEG_ISSUES_AND, measured not assumed. The load-bearing
        # property is unchanged: the greeting's own words never ride into
        # the dispatched segment.
        #
        # #1595 Phase 3 fourteenth deletion (2026-10-03): the new
        # SEG_ISSUES_AND literal (`\bbehind (?:main|origin|upstream|
        # master)\b`) does NOT have that "no shorter-prefix match" property
        # — its own regex match begins mid-phrase at "behind", so WITH a
        # greeting prefix, segment 0 is the SHORTER "behind upstream at all
        # and" (measured, not assumed), not the full SEG_ISSUES_AND. The
        # load-bearing property this test exists to pin is unchanged
        # either way: the greeting's own words ("hi piper,") never ride
        # into the dispatched segment.
        assert segments[0][1] == "behind upstream at all and"

    def test_segments_resolve_the_named_targets_the_confirm_tests_rely_on(self):
        from services.intent_service.destructive_confirm import _named_delete_target

        assert _named_delete_target(SEG_ISSUES_AND) == "are behind upstream"
        assert _named_delete_target(SEG_SESSION) == "what discussed yesterday was helpful"

    def test_single_intent_and_unsplittable_turns_get_no_segments(self):
        assert sibling_segments("what are my todos", _split("what are my todos")) is None

    def test_surface_one_emits_no_write_or_destructive_sibling(self):
        """The measured fact the file docstring's denominator rests on: every
        action the multi-intent splitter can emit is a READ (or not on the rail
        at all). A destructive sibling can only come from a consult."""
        rail = get_action_workflows()
        emitted = set()
        for turn in (
            TURN_READ_FIRST,
            TURN_ISSUES_FIRST,
            TURN_TWO_NAMED,
            TURN_UNRAILED_HALF,
            "can you summarize my current work and delete my hydrate reminder",
            "delete my hydrate reminder and can you summarize my current work",
            "delete my hydrate reminder and delete my stretch reminder",
        ):
            emitted |= {i.action for i in PreClassifier.detect_multiple_intents(turn).intents}
        non_read = {a for a in emitted if a in rail and rail[a].effect != EffectClass.READ}
        assert non_read == set(), non_read

    def test_the_destructive_phrasings_the_dispatch_named_do_not_split(self):
        """Stated as a pin, not a footnote: these are the turns unit 4 was
        asked to cover and CANNOT, because surface 1 never splits them.

        #1595 Phase 3 (second deletion, 2026-09-27): "what are my todos"
        stopped being one of the two illustrative phrasings — TODO_QUERY_
        PATTERNS' deletion means it no longer claims at all, so the ORIGINAL
        first case (1 claim: the read half only) degraded to 0 claims,
        collapsing the distinction this test existed to show. Swapped for
        "what are my open issues" (GITHUB_QUERY_PATTERNS, unaffected AT THE
        TIME) — same shape: the read-first phrasing still claims its one
        read half, the write-first phrasing still claims nothing (the
        destructive blocker fires before GITHUB_QUERY_PATTERNS can claim,
        same #1794 guard family as #1756/#1881).

        #1595 Phase 3 (fifth deletion, 2026-10-02): GITHUB_QUERY_PATTERNS is
        now `[]` too — "what are my open issues" no longer claims at all,
        degrading THIS test's distinction the same way TODO_QUERY_PATTERNS'
        deletion degraded the original. Swapped again, to "give me my
        standup" (STATUS_PATTERNS) — NOT "what branch are we on"
        (LOCAL_GIT_STATUS_PATTERNS, used elsewhere in this file for the
        rail-dispatchable-READ property): LOCAL_GIT_STATUS_PATTERNS is NOT a
        member of `_READ_LANE_GROUPS` (confirmed by direct inspection of
        pre_classifier.py), so the #1794-family destructive-ask guard this
        test exists to pin does NOT suppress its claim in the write-first
        ordering (measured: "delete my hydrate reminder and what branch are
        we on" still returns 1 intent, not 0) — STATUS_PATTERNS IS a
        `_READ_LANE_GROUPS` member, so it reproduces the exact property
        this test is about. get_project_status has no WorkflowEntry
        (floor-routed, #925) so this phrase is deliberately NOT reused for
        the rail-dispatchability tests elsewhere in this file.

        #1595 Phase 3 (seventh deletion, 2026-10-02, PARTIAL): STATUS_PATTERNS'
        \bmy standup\b literal is gone too (52 of 56 deleted). Swapped again
        to "can you summarize my current work" (matches the surviving
        \bcurrent work\b literal) — STATUS_PATTERNS, and therefore
        `_READ_LANE_GROUPS` membership and the no-WorkflowEntry property,
        are both unchanged by a PARTIAL deletion that keeps the list alive;
        measured directly (both orderings below), not assumed."""
        assert (
            len(
                PreClassifier.detect_multiple_intents(
                    "can you summarize my current work and delete my hydrate reminder"
                ).intents
            )
            == 1
        )
        assert (
            PreClassifier.detect_multiple_intents(
                "delete my hydrate reminder and can you summarize my current work"
            ).intents
            == []
        )


def _split(message):
    return PreClassifier.detect_multiple_intents(message)


# ---------------------------------------------------------------------------
# 1. DEFAULT-EMPTY — a two-part turn is the pre-change turn
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDefaultEmpty:
    async def test_flag_unset_does_zero_unit4_work_and_takes_the_legacy_path(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        def _boom(*a, **k):
            raise AssertionError(
                "sibling_segments called with the flag unset — the unit-4 "
                "seam must cost one ContextVar read and nothing else"
            )

        monkeypatch.setattr(inversion_live, "sibling_segments", _boom)

        from services.intent_service import inversion_router as ir

        async def _never(*a, **k):
            raise AssertionError("router consulted with the flag unset")

        monkeypatch.setattr(ir, "route", _never)

        service = _service(monkeypatch, explosive_classifier=False)
        calls = []
        real = service.intent_classifier.classify_multiple

        async def _spy(msg, **k):
            calls.append(msg)
            return await real(msg, **k)

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _spy)

        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("dark"), user_id=_USER
        )
        assert calls == [TURN_READ_FIRST], "the legacy multi-intent block did not run"
        assert result.intent_data.get("multi_intent_inversion") is None

    async def test_flag_on_but_no_sibling_routed_is_the_same_turn(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The specified fallback, verified as an A/B rather than asserted:
        every consult returning None must produce the SAME reply the
        flag-unset turn produces."""
        service_dark = _service(monkeypatch, explosive_classifier=False)
        dark = await service_dark.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("ab-dark"), user_id=_USER
        )

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(monkeypatch, {})  # every segment declines
        service_live = _service(monkeypatch, explosive_classifier=False)
        live = await service_live.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("ab-live"), user_id=_USER
        )

        assert live.message == dark.message
        assert live.intent_data.get("multi_intent_inversion") is None


# ---------------------------------------------------------------------------
# 2. TWO READ SIBLINGS — both routed, both dispatched, one reply
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTwoReadSiblings:
    async def test_both_siblings_dispatch_in_message_order_into_one_reply(
        self, sm, mem_prefs, todo_boundary, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        seen = _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
        )
        dispatched = []
        service = _service(monkeypatch)
        real_rail = service._dispatch_action_rail

        async def _spy(intent, **kwargs):
            dispatched.append((intent.action, kwargs["message"]))
            return await real_rail(intent, **kwargs)

        monkeypatch.setattr(service, "_dispatch_action_rail", _spy)

        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("two-reads"), user_id=_USER
        )
        # One consult per SEGMENT, never one for the whole message.
        assert seen == [SEG_ISSUES_AND, SEG_SESSION]
        # Rule 1 with two reads: message order, and each sibling dispatched
        # with its OWN segment (rule 3 — no sibling sees another's text).
        assert dispatched == [
            ("list_todos_query", SEG_ISSUES_AND),
            ("session_activity_query", SEG_SESSION),
        ]
        assert result.intent_data.get("multi_intent_inversion") is True
        assert result.success is True
        # Both halves are in ONE reply.
        assert "upstream check" in result.message  # the todo list half
        assert result.message.count("\n") or len(result.message) > 40

    async def test_every_decision_line_names_the_sibling(
        self, sm, mem_prefs, todo_boundary, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
        )
        service = _service(monkeypatch)
        await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("telemetry"), user_id=_USER
        )
        lines = log_rec.decisions()
        stand_down = [f for f in lines if f["reason"] == MULTI_INTENT_SPLIT_STAND_DOWN]
        siblings = [f for f in lines if "sibling_index" in f]
        assert len(stand_down) == 1, "the whole-message consult must still stand down"
        assert [(f["sibling_index"], f["sibling_count"]) for f in siblings] == [(0, 2), (1, 2)]
        assert all(f["route"] == "inversion" and f["reason"] is None for f in siblings)


# ---------------------------------------------------------------------------
# 3 + 4. READ + an allowlisted DESTRUCTIVE — rule 1 order, rule 2 pause
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestReadPlusDestructive:
    async def test_read_answered_then_the_confirm_arms_and_nothing_is_deleted(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """Test 3: destructive sibling SECOND in the message. The read runs,
        then the delete arms its title-bound confirm; nothing is deleted and
        no sibling is deferred (there is nothing after the write)."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "list_todos_query", SEG_SESSION: "delete_todo"},
        )
        service = _service(monkeypatch)
        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("read-then-del"), user_id=_USER
        )
        assert todo_boundary["deleted"] == []
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert 'Delete todo: "discussed yesterday"? (yes/no)' in result.message
        # The read half is still in the reply, and it LEADS.
        assert result.message.index("upstream check") < result.message.index("Delete todo")
        assert "haven't touched" not in result.message  # nothing was deferred

    async def test_read_runs_first_even_when_the_write_is_first_in_the_message(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """Test 4 — rule 1, the load-bearing half: the destructive sibling is
        FIRST in the user's words and still runs last, so the read answer is
        never lost to the pause."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "delete_todo", SEG_SESSION: "list_todos_query"},
        )
        dispatched = []
        service = _service(monkeypatch)
        real_rail = service._dispatch_action_rail

        async def _spy(intent, **kwargs):
            dispatched.append(intent.action)
            return await real_rail(intent, **kwargs)

        monkeypatch.setattr(service, "_dispatch_action_rail", _spy)

        result = await service.process_intent(
            message=TURN_ISSUES_FIRST, session_id=_sid("write-first"), user_id=_USER
        )
        assert dispatched == ["list_todos_query", "delete_todo"]
        assert todo_boundary["deleted"] == []
        assert 'Delete todo: "upstream check"? (yes/no)' in result.message
        assert "haven't touched" not in result.message

    async def test_the_confirmed_yes_deletes_exactly_the_named_row(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The arm is a REAL #1190 arm on the real session store — the next
        turn's crisp yes completes it through the unchanged confirm carrier."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "list_todos_query", SEG_SESSION: "delete_todo"},
        )
        service = _service(monkeypatch)
        sid = _sid("yes")
        await service.process_intent(message=TURN_READ_FIRST, session_id=sid, user_id=_USER)
        todo_boundary["allow_delete"] = True
        yes = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert len(todo_boundary["deleted"]) == 1
        assert "discussed yesterday" in yes.message


# ---------------------------------------------------------------------------
# 5. TWO DESTRUCTIVE SIBLINGS — one confirm, the other NAMED, never queued
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestPauseStopsTheTurn:
    EXPECTED = (
        'Delete todo: "upstream check"? (yes/no)\n'
        "\n"
        "I'll ask about that first — I haven't touched "
        '"what we discussed yesterday was helpful" yet; say yes/no, then tell me '
        "again if you still want it."
    )

    async def _run(self, monkeypatch, sid):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "delete_todo", SEG_SESSION: "delete_todo"},
        )
        service = _service(monkeypatch)
        result = await service.process_intent(
            message=TURN_TWO_NAMED, session_id=_sid(sid), user_id=_USER
        )
        return service, result

    async def test_first_confirm_arms_and_the_second_is_named_verbatim(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        _service_obj, result = await self._run(monkeypatch, "two-del")
        assert result.message == self.EXPECTED
        assert todo_boundary["deleted"] == []

    async def test_the_deferred_sibling_is_not_queued_anywhere(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """Rule 2's real content: the deferred write must not be sitting in
        the one-slot #846 store waiting to fire off the user's next yes. The
        armed offer must name the FIRST target and only that one — a queued Y
        would show up here as a second pending action or a different bind."""
        service, _result = await self._run(monkeypatch, "two-del-store")
        pending = service.workflow_offer_service.peek_pending_offer(
            _sid("two-del-store"), user_id=_USER
        )
        assert pending is not None
        bound = pending["pending_action"]["intent"]
        bound_context = bound["context"] if isinstance(bound, dict) else bound.context
        assert bound_context["delete_todo_resolved"]["text"] == "upstream check"
        # And the yes deletes exactly one row — the one the user was shown.
        todo_boundary["allow_delete"] = True
        yes = await service.process_intent(
            message="yes", session_id=_sid("two-del-store"), user_id=_USER
        )
        assert len(todo_boundary["deleted"]) == 1
        assert "upstream check" in yes.message
        assert "discussed yesterday" not in yes.message


# ---------------------------------------------------------------------------
# 6. A SIBLING THE CONSULT DECLINED — keeps surface 1's Intent
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestConsultDeclinedSibling:
    async def test_it_keeps_surface_ones_intent_and_dispatches_through_the_rail(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """PINNED ANSWER to "legacy path or reported honestly": when the kept
        surface-1 Intent is ITSELF a rail key (it is, for every action this
        splitter emits that the rail knows), it is dispatched through the SAME
        rail alongside the routed sibling. Nothing is reported as unhandled
        and nothing is dropped.

        #1595 Phase 3 (second deletion, 2026-09-27): the ORIGINAL kept
        (unconsulted) sibling was SEG_TODOS_AND, whose own surface-1 claim
        was list_todos_query — TODO_QUERY_PATTERNS' deletion removed that
        claim, so no phrase can produce it as an unconsulted KEPT action any
        more. Swapped which segment plays "kept" vs "consulted": SEG_SESSION
        is now left unmapped (kept as ITS OWN surface-1 claim — originally
        session_activity_query, a real, `sm`-fixture-backed dispatch), and
        SEG_ISSUES_AND is consulted, remapped to list_todos_query (a real,
        todo_boundary-backed dispatch — the consult freely renames a
        segment's action regardless of what surface 1 originally called it,
        so list_todos_query is still reachable here even though it can
        never again be a KEPT action). Same point either way: the kept
        sibling's OWN Intent still dispatches through the rail, nothing
        dropped.

        #1595 Phase 3 (fourteenth deletion, 2026-10-03): SEG_SESSION's own
        surface-1 claim is now get_memory (MEMORY_PATTERNS' surviving
        `\\bwhat (i|we) (said|talked|discussed)\\b` literal; the pattern
        text SEG_SESSION itself resolves to also changed — see the
        constants block). get_memory's rail entry is a read_floor adapter
        (`_make_read_floor_entry_point`), which calls
        `intent_service._handle_floor_with_context` → the conversational
        floor → an LLM completion. Reaching that handler for REAL the way
        session_activity_query's own `_handle_session_activity_query` could
        is a live-LLM call this unit is NOT allowed to make (CLAUDE.md "NO
        LLM calls" + measured: it raises `UnboundLLMKeyError` in this
        harness, surfacing as the SAME "classify_multiple consulted" guard
        failure since the rail dispatch's exception propagates through
        process_intent's error path). `_handle_floor_with_context` is
        mocked here instead — the property this test pins ("the kept
        sibling's OWN Intent still dispatches through the rail, nothing
        dropped") is about the RAIL reaching the handler, not that
        handler's own internals, so a mocked handler still proves it (same
        idiom every other handler-dispatch test in this file already
        uses)."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(monkeypatch, {SEG_ISSUES_AND: "list_todos_query"})
        dispatched = []
        service = _service(monkeypatch)
        real_rail = service._dispatch_action_rail

        async def _spy(intent, **kwargs):
            dispatched.append((intent.action, bool((intent.context or {}).get("inversion_live"))))
            return await real_rail(intent, **kwargs)

        monkeypatch.setattr(service, "_dispatch_action_rail", _spy)
        from unittest.mock import AsyncMock as _AsyncMock

        from services.intent.intent_service import IntentProcessingResult

        monkeypatch.setattr(
            service,
            "_handle_floor_with_context",
            _AsyncMock(
                return_value=IntentProcessingResult(
                    success=True,
                    message="history answer",
                    intent_data={"category": "memory", "action": "get_memory"},
                )
            ),
        )

        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("one-none"), user_id=_USER
        )
        # Sibling 0 (issues) is the consult's; sibling 1 (session) kept its
        # surface-1 Intent (no inversion marker).
        assert dispatched == [("list_todos_query", True), ("get_memory", False)]
        assert result.intent_data.get("multi_intent_inversion") is True

    async def test_a_sibling_the_rail_cannot_serve_declines_the_whole_turn(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The other half of the same question, and the one that matters:
        ``explain_suggestion`` is not a rail key at all, so serving only the
        todos half would be #1896's dropped half wearing a new coat. The path
        declines and the legacy chain does the whole turn.

        #1595 Phase 3 (Arch's 2026-10-01 ruling): was ``get_current_time``
        until this unit gave it a rail entry (get_current_time_entry,
        flip_group read_temporal) — swapped to explain_suggestion (see
        TURN_UNRAILED_HALF's own comment above) for a destination that is
        STILL genuinely unrailed, which is the property this test pins."""
        assert "explain_suggestion" not in get_action_workflows()
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(monkeypatch, {SEG_ISSUES_AND: "list_todos_query"})
        service = _service(monkeypatch, explosive_classifier=False)
        calls = []
        real = service.intent_classifier.classify_multiple

        async def _spy(msg, **k):
            calls.append(msg)
            return await real(msg, **k)

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _spy)

        result = await service.process_intent(
            message=TURN_UNRAILED_HALF, session_id=_sid("unrailed"), user_id=_USER
        )
        assert calls == [TURN_UNRAILED_HALF], "the legacy chain must answer the whole turn"
        assert result.intent_data.get("multi_intent_inversion") is None


# ---------------------------------------------------------------------------
# 7. AN UNALLOWLISTED WRITE STILL CANNOT FLIP — on a sibling consult either
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestUnallowlistedWriteSibling:
    """``create_issue`` is the guard's own worked example (WRITE, filed under
    QUERY in ACTION_REGISTRY — #1677's original evidence that a category flag
    alone is not a READ guarantee); ``set_default_repo`` served this role
    until #1595 unit 3c (2026-09-27) put it ON the allowlist (for #1606's
    own set-default-repo half), which made it stop being an "unallowlisted
    write" example. Swapped rather than deleted: the sibling path needs a
    genuinely-still-unallowlisted write to prove the effect guard holds per
    sibling, and ``create_issue`` is that write, unaffected by unit 3c."""

    async def test_create_issue_is_write_and_not_allowlisted(self):
        entry = get_action_workflows()["create_issue"]
        assert entry.effect == EffectClass.WRITE
        assert entry.flip_write_allowlist_key is None
        assert "create_issue" not in FLIP_WRITE_ALLOWLIST

    async def test_a_sibling_consult_naming_it_is_refused_like_any_other(
        self, sm, mem_prefs, monkeypatch, log_rec
    ):
        """A sibling consult is not a relaxed consult — the #1677 effect guard
        holds per sibling exactly as it does for a whole message.

        ⚠️ #1606 IS STILL NOT CLOSED BY THIS UNIT, though its set-default-repo
        half's ALLOWLIST condition is now met (#1595 unit 3c, 2026-09-27, put
        ``set_default_repo`` on ``FLIP_WRITE_ALLOWLIST`` — see the sibling
        file ``test_inversion_write_allowlist_set_default_repo_1606.py``).
        Two things independently still block it: (1) the turn does not split
        at surface 1 at all (pinned in TestTheShapesAreReal), so closing it
        needs option (b)'s router-returned plan, not this unit; and (2) #1898
        — ``_handle_set_default_repo`` reads its repo argument from
        ``intent.context["original_message"]`` only, which the inversion-built
        Intent never populates, so even a live flip currently degrades to a
        graceful bad-shape nudge rather than the actual write. This test keeps
        proving the GENERIC guard (any unallowlisted write is refused per
        sibling) with ``create_issue``, which #1595 unit 3c did not touch."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "create_issue")
        _route_by_segment(monkeypatch, {SEG_SESSION: "create_issue"})
        svc = SimpleNamespace(workflow_offer_service=WorkflowOfferService(), intent_classifier=None)
        out = await consult_inversion_live(
            SEG_SESSION,
            session_id=_sid("wr"),
            user_id=_USER,
            intent_service=svc,
            multi_intent_sibling=(1, 2),
        )
        assert out is None
        line = log_rec.decisions()[-1]
        assert line["reason"] == "not_read_effect"
        assert (line["sibling_index"], line["sibling_count"]) == (1, 2)


# ---------------------------------------------------------------------------
# 8. AN ARMED TURN — no consults at all, legacy path
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestArmedTurn:
    async def test_armed_turn_never_reaches_the_sibling_path(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")

        from services.intent_service import inversion_router as ir

        async def _never(*a, **k):
            raise AssertionError("router consulted on an armed turn")

        monkeypatch.setattr(ir, "route", _never)

        def _never_segments(*a, **k):
            raise AssertionError("sibling_segments reached on an armed turn")

        monkeypatch.setattr(inversion_live, "sibling_segments", _never_segments)

        service = _service(monkeypatch, explosive_classifier=False)
        sid = _sid("armed")
        service.workflow_offer_service.set_pending_offer(
            sid,
            {
                "workflow_type": "confirm_pending_action",
                "question": 'Delete todo: "hydrate"? (yes/no)',
                "pending_action": {
                    "kind": "destructive_action_confirmation",
                    "intent": {
                        "category": "execution",
                        "action": "delete_todo",
                        "original_message": "delete my hydrate reminder",
                        "context": {},
                    },
                },
            },
            user_id=_USER,
        )
        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("multi_intent_inversion") is None


# ---------------------------------------------------------------------------
# 9. NO SECOND DISPATCH SITE — the structural property Arch ruled on
# ---------------------------------------------------------------------------


class TestNoSecondDispatchSite:
    def test_the_rail_is_invoked_from_exactly_one_place(self):
        """Shape (i) was ruled out because a rail leg inside the orchestrator
        would be a SECOND place that dispatches an action. Shape (ii) reuses
        the one block, so ``dispatch_workflow`` is still called from exactly
        one site in this module, and both callers reach it through
        ``_dispatch_action_rail``.

        Stated rather than hidden: the multi-intent helper DOES consult
        ``get_action_workflows()`` — to read each sibling's declared effect for
        the rule-1 ordering, and to REFUSE the whole path when a sibling isn't
        rail-dispatchable. That is a refusal and an effect lookup, not a
        dispatch; nothing is invoked from it. The dispatch decision itself
        remains in one function, which is the property Arch ruled on."""
        import inspect

        from services.intent import intent_service as mod

        source = inspect.getsource(mod)
        # Three call sites in the module, unchanged by this unit and named so
        # the number is a measurement rather than a magic constant: the
        # CLASSIFIED-turn rail (_dispatch_action_rail, the one under test),
        # the #846 offer-acceptance seam (re-dispatching a stored pending
        # action), and the #300 autonomous-pattern handler. Unit 4 added
        # none — it reuses the first.
        assert source.count("await dispatch_workflow(") == 3
        assert source.count("_action_workflows = get_action_workflows()") == 1
        rail_src = inspect.getsource(mod.IntentService._dispatch_action_rail)
        assert "await dispatch_workflow(" in rail_src
        multi_src = inspect.getsource(mod.IntentService._maybe_dispatch_multi_intent_inversion)
        assert "dispatch_workflow" not in multi_src
        assert "self._dispatch_action_rail(" in multi_src

    def test_the_orchestrator_is_not_involved(self):
        """The siblings never touch ``IntentOrchestrator._execute_single`` /
        ``CanonicalHandlers.can_handle`` — the measured reason option (a) was
        unbuildable (0 of 127 rail keys clear that gate)."""
        import inspect

        from services.intent import intent_service as mod

        body = inspect.getsource(mod.IntentService._maybe_dispatch_multi_intent_inversion)
        code = "\n".join(line for line in body.splitlines() if not line.lstrip().startswith("#"))
        assert "_execute_single" not in code
        assert "can_handle" not in code
        assert "create_plan" not in code
        assert "execute_plan" not in code
        # It DOES reuse the orchestrator's aggregator — the joiner, not the
        # dispatcher.
        assert "_aggregate_messages" in body


# ---------------------------------------------------------------------------
# 10. Rule 3 — no cross-sibling state
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestNoCrossSiblingState:
    async def test_each_sibling_sees_only_its_own_segment(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        seen = _route_by_segment(
            monkeypatch,
            {SEG_ISSUES_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
        )
        messages = []
        service = _service(monkeypatch)
        real_rail = service._dispatch_action_rail

        async def _spy(intent, **kwargs):
            messages.append((kwargs["message"], intent.original_message))
            return await real_rail(intent, **kwargs)

        monkeypatch.setattr(service, "_dispatch_action_rail", _spy)
        await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("no-state"), user_id=_USER
        )
        assert seen == [SEG_ISSUES_AND, SEG_SESSION]
        # Neither sibling's dispatch message is the whole turn, and neither
        # carries the other's text.
        for gate_message, original in messages:
            assert gate_message != TURN_READ_FIRST
            assert original != TURN_READ_FIRST
        assert SEG_SESSION not in messages[0][0]


# ---------------------------------------------------------------------------
# 11. #1595 unit 4b (#1897/#1606) — the ADDITIVE "plan" outcome
# ---------------------------------------------------------------------------

# The exact #1897 shape: surface 1's splitter is read-lane-only (the
# #1527/#1756/#1794/#1881 guards decline a destructive ask outright), so this
# message never splits at all — unit 4's sibling path can never reach it.
# Verified below (TestPlanOutcome.test_the_plan_message_does_not_split_at_surface_one)
# rather than assumed, per the file's own denominator discipline.
PLAN_MESSAGE = "what are my todos and delete my hydrate reminder"


class TestPlanMessageShape:
    """Sync-only (no asyncio marker, mirrors TestNoSecondDispatchSite's own
    plain-class convention for non-async tests in this file)."""

    def test_the_plan_message_does_not_split_at_surface_one(self):
        """The denominator: PLAN_MESSAGE is exactly the shape unit 4's own
        sibling path cannot reach (#1897's measured fact, re-verified here
        rather than assumed)."""
        assert PreClassifier.detect_multiple_intents(PLAN_MESSAGE).intents == []


def _route_plan(monkeypatch, message, operations):
    """Deterministic router stub for the WHOLE-MESSAGE consult: exactly
    ``message`` gets the scripted plan decision; anything else (a sibling
    segment, a retry) gets an explicit NONE so an unexpected extra call is a
    visible mismatch rather than a silent pass."""
    from services.intent_service import inversion_router as ir

    seen = []

    async def _route(utterance, session_state=None, **kwargs):
        seen.append(utterance)
        if utterance == message:
            return RoutingDecision(outcome="plan", operations=list(operations))
        return RoutingDecision(outcome="none", operation=None, confidence=None)

    monkeypatch.setattr(ir, "route", _route)
    return seen


@pytest.mark.asyncio
class TestPlanOutcome:
    """A plan is ANOTHER SOURCE of ordered sibling decisions feeding the SAME
    ``_dispatch_action_rail`` sequencing the split tests above already prove
    (rule 1 order, rule 2 pause, rule 3 no cross-sibling state). These tests
    prove the NEW hand-off from a whole-message plan decision into that
    shared code — not a second copy of the sequencing rules, which are
    unchanged code paths already covered by sections 3-5 above.

    ⚠️ LAYER HONESTY (m-43), inherited from the split suite: the router is a
    scripted stub, so these prove the path/sequencing/hand-off, not that the
    live constrained router reliably emits a correct plan for a given
    message — that is observable only live.
    """

    async def test_read_then_write_dispatches_through_the_rail(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The two-op case: a READ then a WRITE. The read runs, the write
        reaches its #1190 confirm and arms; nothing is deleted; nothing is
        deferred (there is nothing after the one write)."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_plan(
            monkeypatch,
            PLAN_MESSAGE,
            [
                {
                    "operation": "list_todos_query",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "list todos",
                },
                {
                    "operation": "delete_todo",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "delete hydrate reminder",
                },
            ],
        )
        service = _service(monkeypatch)
        result = await service.process_intent(
            message=PLAN_MESSAGE, session_id=_sid("plan-read-write"), user_id=_USER
        )
        assert todo_boundary["deleted"] == []
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert result.intent_data.get("multi_intent_inversion") is True
        assert 'Delete todo: "hydrate"? (yes/no)' in result.message
        assert "haven't touched" not in result.message  # nothing deferred

    async def test_the_confirmed_yes_deletes_exactly_the_named_row(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The arm is a REAL #1190 arm on the real session store — same
        confirm carrier the split path uses, unmodified."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_plan(
            monkeypatch,
            PLAN_MESSAGE,
            [
                {
                    "operation": "list_todos_query",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "list todos",
                },
                {
                    "operation": "delete_todo",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "delete hydrate reminder",
                },
            ],
        )
        service = _service(monkeypatch)
        sid = _sid("plan-yes")
        await service.process_intent(message=PLAN_MESSAGE, session_id=sid, user_id=_USER)
        todo_boundary["allow_delete"] = True
        yes = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert len(todo_boundary["deleted"]) == 1
        assert "hydrate" in yes.message

    async def test_two_writes_first_arms_second_is_named_and_never_queued(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """Rule 2 for a plan: the FIRST write's confirm ends the turn: the
        SECOND write is named in the reply (by its rationale — a plan
        element has no literal user-words segment) and never queued."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "delete_todo")
        _route_plan(
            monkeypatch,
            PLAN_MESSAGE,
            [
                {
                    "operation": "delete_todo",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "delete hydrate reminder",
                },
                {
                    "operation": "delete_todo",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "delete open issues todo",
                },
            ],
        )
        service = _service(monkeypatch)
        result = await service.process_intent(
            message=PLAN_MESSAGE, session_id=_sid("plan-two-writes"), user_id=_USER
        )
        assert todo_boundary["deleted"] == []
        assert 'Delete todo: "hydrate"? (yes/no)' in result.message
        assert "haven't touched" in result.message
        assert "delete open issues todo" in result.message
        pending = service.workflow_offer_service.peek_pending_offer(
            _sid("plan-two-writes"), user_id=_USER
        )
        bound = pending["pending_action"]["intent"]
        bound_context = bound["context"] if isinstance(bound, dict) else bound.context
        assert bound_context["delete_todo_resolved"]["text"] == "hydrate"

    async def test_a_non_plan_stand_down_reason_never_engages_the_rail_loop(self, monkeypatch):
        """Known, DOCUMENTED divergence from the sibling path's own rule: a
        sibling the rail can't serve declines the WHOLE turn (section 6
        above) — a sibling that's merely not-yet-flipped falls back to its
        OWN surface-1 Intent instead, because a real sibling has one. A plan
        element has no surface-1 Intent of its own to fall back to (the whole
        plan came from ONE whole-message router call), so
        ``_resolve_plan_for_dispatch`` is all-or-nothing at the DISPATCH
        validation layer too, not just at the router's PARSE layer — one
        ineligible element (not live, sub-threshold, not rail-dispatchable,
        …) declines the ENTIRE plan; ``consult_inversion_live`` publishes the
        SPECIFIC reason (never ``PLAN_STAND_DOWN``), and this function's own
        top-level guard — the same one that already protects the split path
        — declines without touching the rail loop at all.

        Exercised at THIS layer (calling the function directly with a
        published provenance record) rather than through full
        ``process_intent``, because PLAN_MESSAGE genuinely does not split at
        surface 1 (that is the whole point of #1897) — routing it through the
        real legacy fallback would need a working classifier LLM double,
        which is orthogonal to what this test is proving. The dispatch-time
        validation itself (``_resolve_plan_for_dispatch``'s per-reason
        behavior: not-live, sub-threshold, not-rail-dispatchable, …) is
        proven directly in ``test_inversion_live_1595.py::TestPlanOutcome``,
        against the real ``consult_inversion_live``, stubbed router only."""
        from services.intent_service.inversion_live import (
            LiveRouteProvenance,
            publish_live_route_provenance,
        )

        service = _service(monkeypatch, explosive_classifier=False)
        for reason in ("plan_not_live", "plan_sub_threshold", "plan_not_rail_dispatchable"):
            publish_live_route_provenance(LiveRouteProvenance(routed_live=False, reason=reason))
            result = await service._maybe_dispatch_multi_intent_inversion(
                PLAN_MESSAGE,
                session_id=_sid(f"plan-decline-{reason}"),
                user_id=_USER,
                trust_stage=None,
                formality_baseline=None,
                off_topic_prefix=None,
                restate_suffix=None,
            )
            assert result is None, reason

    async def test_no_second_dispatch_site_for_the_plan_path(self):
        """Same structural property section 9 pins for the split path: the
        plan branch reuses ``_dispatch_action_rail`` and never touches
        ``dispatch_workflow`` or the orchestrator directly."""
        import inspect

        from services.intent import intent_service as mod

        multi_src = inspect.getsource(mod.IntentService._maybe_dispatch_multi_intent_inversion)
        assert "dispatch_workflow" not in multi_src
        assert multi_src.count("self._dispatch_action_rail(") == 1
        assert "PLAN_STAND_DOWN" in multi_src


class TestPlanFloorElement:
    """#1606 — Arch's 2026-10-01 ruling, proof 5(a) in unit form: PM's own
    two-part message routes as [delete_todo → capability question]; the
    capability half is a FLOOR-disposition read, so it runs in the reads
    phase through ``_handle_floor_with_context`` scoped to its own ask, then
    the delete arms its #1190 confirm. The floor is a stub here (the live
    probe is where the real floor's wording is observed — m-43); the rail,
    the confirm carrier and the composition are real.
    """

    _MSG = (
        'please clear the reminders except for "Review the PR" - also, are you '
        "able to set my default repo for me conversationally?"
    )

    async def test_floor_half_answers_first_then_the_delete_arms(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        from services.intent.intent_service import IntentProcessingResult

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "delete_todo")
        _route_plan(
            monkeypatch,
            self._MSG,
            [
                {
                    "operation": "delete_todo",
                    "args": {},
                    "confidence": 0.95,
                    "rationale": "delete hydrate reminder",
                },
                {
                    "operation": "get_capabilities",
                    "args": {},
                    "confidence": 0.85,
                    "rationale": "asks whether Piper can set the default repo conversationally",
                },
            ],
        )
        service = _service(monkeypatch)
        floor_calls = []

        async def _floor(
            intent, session_id, user_id=None, formality_baseline=None, trust_stage=None
        ):
            floor_calls.append(intent)
            return IntentProcessingResult(
                success=True,
                message="Yes — say 'set my default repo to owner/name' and I'll do it.",
                intent_data={"floor": True},
            )

        monkeypatch.setattr(service, "_handle_floor_with_context", _floor)
        result = await service.process_intent(
            message=self._MSG, session_id=_sid("plan-floor"), user_id=_USER
        )
        # Condition 3 — scoped: the floor saw the element's rationale plus the
        # "handled separately" note, never the whole two-part message.
        assert len(floor_calls) == 1
        seen = floor_calls[0].original_message
        assert "set the default repo conversationally" in seen
        assert "handled separately" in seen
        assert "clear the reminders" not in seen
        assert floor_calls[0].context["inversion_floor_element"] is True
        # Condition 4 — execution order, rail text verbatim: the capability
        # answer first, then the delete's own confirm prompt.
        answer_at = result.message.index("set my default repo to owner/name")
        confirm_at = result.message.index('Delete todo: "hydrate"? (yes/no)')
        assert answer_at < confirm_at
        # 5(a): nothing was deleted and nothing says it was.
        assert todo_boundary["deleted"] == []
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert result.intent_data.get("multi_intent_inversion") is True
        assert "deleted" not in result.message.lower()
        assert "haven't touched" not in result.message  # nothing deferred

    async def test_floor_element_is_not_a_dispatch_site_regression(self):
        """The floor call is a method call in the reads phase, not a new
        ``if intent.action in [...]`` chain — the ratchet in
        tests/test_architecture_enforcement.py holds (run there); here, the
        source of the plan loop names the ONE floor entry point."""
        import inspect

        from services.intent.intent_service import IntentService

        src = inspect.getsource(IntentService._maybe_dispatch_multi_intent_inversion)
        assert src.count("_handle_floor_with_context(") == 1
