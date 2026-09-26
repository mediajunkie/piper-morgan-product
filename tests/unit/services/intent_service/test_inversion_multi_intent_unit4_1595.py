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
TURN_READ_FIRST = "what are my todos and what did we create this session"
TURN_ISSUES_FIRST = "what are my open issues and what are my todos"
TURN_TWO_NAMED = "what are my open issues and what did we create this session"
TURN_UNRAILED_HALF = "what are my todos and what time is it"

# Their segments, as sibling_segments derives them (message order).
SEG_TODOS_AND = "what are my todos and"
SEG_SESSION = "what did we create this session"
SEG_ISSUES_AND = "what are my open issues and"
SEG_TODOS = "what are my todos"


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
    "what are my open issues and" → "open issues", "what did we create this
    session" → "create session" (both verified in
    TestTheShapesAreReal::test_segments_resolve_the_named_targets)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo("open issues"), _todo("create session"), _todo("hydrate")],
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
            (TURN_READ_FIRST, ["list_todos_query", "session_activity_query"]),
            (TURN_ISSUES_FIRST, ["list_issues_query", "list_todos_query"]),
            (TURN_TWO_NAMED, ["list_issues_query", "session_activity_query"]),
        ):
            result = PreClassifier.detect_multiple_intents(turn)
            got = sorted(i.action for i in result.intents)
            assert got == sorted(actions), turn
            for action in actions:
                assert action in rail and rail[action].effect == EffectClass.READ

    def test_segments_are_derived_in_message_order(self):
        assert [
            (i.action, s) for i, s in sibling_segments(TURN_READ_FIRST, _split(TURN_READ_FIRST))
        ] == [("list_todos_query", SEG_TODOS_AND), ("session_activity_query", SEG_SESSION)]
        assert [
            (i.action, s) for i, s in sibling_segments(TURN_ISSUES_FIRST, _split(TURN_ISSUES_FIRST))
        ] == [("list_issues_query", SEG_ISSUES_AND), ("list_todos_query", SEG_TODOS)]

    def test_a_greeting_keeps_its_own_words_and_is_not_returned(self):
        """The greeting anchor still bounds segment 0, so 'hi piper,' does not
        ride into the first substantive half — but the greeting itself is not
        a sibling to dispatch."""
        turn = f"hi piper, {TURN_READ_FIRST}"
        segments = sibling_segments(turn, _split(turn))
        assert [i.action for i, _ in segments] == [
            "list_todos_query",
            "session_activity_query",
        ]
        assert segments[0][1] == SEG_TODOS_AND

    def test_segments_resolve_the_named_targets_the_confirm_tests_rely_on(self):
        from services.intent_service.destructive_confirm import _named_delete_target

        assert _named_delete_target(SEG_ISSUES_AND) == "what are open issues"
        assert _named_delete_target(SEG_SESSION) == "what create session"

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
            "what are my todos and delete my hydrate reminder",
            "delete my hydrate reminder and what are my todos",
            "delete my hydrate reminder and delete my stretch reminder",
        ):
            emitted |= {i.action for i in PreClassifier.detect_multiple_intents(turn).intents}
        non_read = {a for a in emitted if a in rail and rail[a].effect != EffectClass.READ}
        assert non_read == set(), non_read

    def test_the_destructive_phrasings_the_dispatch_named_do_not_split(self):
        """Stated as a pin, not a footnote: these are the turns unit 4 was
        asked to cover and CANNOT, because surface 1 never splits them."""
        assert (
            len(
                PreClassifier.detect_multiple_intents(
                    "what are my todos and delete my hydrate reminder"
                ).intents
            )
            == 1
        )
        assert (
            PreClassifier.detect_multiple_intents(
                "delete my hydrate reminder and what are my todos"
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
            {SEG_TODOS_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
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
        assert seen == [SEG_TODOS_AND, SEG_SESSION]
        # Rule 1 with two reads: message order, and each sibling dispatched
        # with its OWN segment (rule 3 — no sibling sees another's text).
        assert dispatched == [
            ("list_todos_query", SEG_TODOS_AND),
            ("session_activity_query", SEG_SESSION),
        ]
        assert result.intent_data.get("multi_intent_inversion") is True
        assert result.success is True
        # Both halves are in ONE reply.
        assert "open issues" in result.message  # the todo list half
        assert result.message.count("\n") or len(result.message) > 40

    async def test_every_decision_line_names_the_sibling(
        self, sm, mem_prefs, todo_boundary, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(
            monkeypatch,
            {SEG_TODOS_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
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
            {SEG_TODOS_AND: "list_todos_query", SEG_SESSION: "delete_todo"},
        )
        service = _service(monkeypatch)
        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("read-then-del"), user_id=_USER
        )
        assert todo_boundary["deleted"] == []
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert 'Delete todo: "create session"? (yes/no)' in result.message
        # The read half is still in the reply, and it LEADS.
        assert result.message.index("open issues") < result.message.index("Delete todo")
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
            {SEG_ISSUES_AND: "delete_todo", SEG_TODOS: "list_todos_query"},
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
        assert 'Delete todo: "open issues"? (yes/no)' in result.message
        assert "haven't touched" not in result.message

    async def test_the_confirmed_yes_deletes_exactly_the_named_row(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The arm is a REAL #1190 arm on the real session store — the next
        turn's crisp yes completes it through the unchanged confirm carrier."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status,delete_todo")
        _route_by_segment(
            monkeypatch,
            {SEG_TODOS_AND: "list_todos_query", SEG_SESSION: "delete_todo"},
        )
        service = _service(monkeypatch)
        sid = _sid("yes")
        await service.process_intent(message=TURN_READ_FIRST, session_id=sid, user_id=_USER)
        todo_boundary["allow_delete"] = True
        yes = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert len(todo_boundary["deleted"]) == 1
        assert "create session" in yes.message


# ---------------------------------------------------------------------------
# 5. TWO DESTRUCTIVE SIBLINGS — one confirm, the other NAMED, never queued
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestPauseStopsTheTurn:
    EXPECTED = (
        'Delete todo: "open issues"? (yes/no)\n'
        "\n"
        "I'll ask about that first — I haven't touched "
        '"what did we create this session" yet; say yes/no, then tell me '
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
        assert bound_context["delete_todo_resolved"]["text"] == "open issues"
        # And the yes deletes exactly one row — the one the user was shown.
        todo_boundary["allow_delete"] = True
        yes = await service.process_intent(
            message="yes", session_id=_sid("two-del-store"), user_id=_USER
        )
        assert len(todo_boundary["deleted"]) == 1
        assert "open issues" in yes.message
        assert "create session" not in yes.message


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
        and nothing is dropped."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(monkeypatch, {SEG_SESSION: "session_activity_query"})
        dispatched = []
        service = _service(monkeypatch)
        real_rail = service._dispatch_action_rail

        async def _spy(intent, **kwargs):
            dispatched.append((intent.action, bool((intent.context or {}).get("inversion_live"))))
            return await real_rail(intent, **kwargs)

        monkeypatch.setattr(service, "_dispatch_action_rail", _spy)

        result = await service.process_intent(
            message=TURN_READ_FIRST, session_id=_sid("one-none"), user_id=_USER
        )
        # Sibling 0 kept its surface-1 Intent (no inversion marker); sibling 1
        # is the consult's.
        assert dispatched == [("list_todos_query", False), ("session_activity_query", True)]
        assert result.intent_data.get("multi_intent_inversion") is True

    async def test_a_sibling_the_rail_cannot_serve_declines_the_whole_turn(
        self, sm, mem_prefs, todo_boundary, monkeypatch
    ):
        """The other half of the same question, and the one that matters:
        ``get_current_time`` is not a rail key at all, so serving only the
        todos half would be #1896's dropped half wearing a new coat. The path
        declines and the legacy chain does the whole turn."""
        assert "get_current_time" not in get_action_workflows()
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        _route_by_segment(monkeypatch, {SEG_TODOS_AND: "list_todos_query"})
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
    async def test_set_default_repo_is_write_and_not_allowlisted(self):
        entry = get_action_workflows()["set_default_repo"]
        assert entry.effect == EffectClass.WRITE
        assert entry.flip_write_allowlist_key is None
        assert "set_default_repo" not in FLIP_WRITE_ALLOWLIST

    async def test_a_sibling_consult_naming_it_is_refused_like_any_other(
        self, sm, mem_prefs, monkeypatch, log_rec
    ):
        """A sibling consult is not a relaxed consult — the #1677 effect guard
        holds per sibling exactly as it does for a whole message.

        ⚠️ #1606 IS NOT CLOSED BY THIS UNIT. Its corpus row ("please clear the
        reminders except for 'Review the PR' — also, can you set my default
        repo conversationally?") needs BOTH halves routed; the repo half is
        ``set_default_repo``, a WRITE nobody has run Arch's three allowlist
        conditions against. Closing #1606 needs that separate unit-3 style
        allowlist entry — and, independently, the turn does not split at
        surface 1 at all (pinned in TestTheShapesAreReal), so it would need
        option (b)'s router-returned plan as well."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "set_default_repo")
        _route_by_segment(monkeypatch, {SEG_SESSION: "set_default_repo"})
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
            {SEG_TODOS_AND: "list_todos_query", SEG_SESSION: "session_activity_query"},
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
        assert seen == [SEG_TODOS_AND, SEG_SESSION]
        # Neither sibling's dispatch message is the whole turn, and neither
        # carries the other's text.
        for gate_message, original in messages:
            assert gate_message != TURN_READ_FIRST
            assert original != TURN_READ_FIRST
        assert SEG_SESSION not in messages[0][0]
