"""#1595 unit 3 — the SECOND named write flips through the Inversion:
``create_reminder``, via the same #1677 allowlist mechanism ``create_todo``
used (never a relaxed effect check, never a ``flip_group``).

The corpus row this closes (#1559, deposited turn-1 case): "remind me at
<time> <day> to X" has NO deterministic pre-classifier claim — the adjacency
gap in ``REMINDER_PATTERNS`` (``\\bremind\\s+me\\s+(?:to|about)\\b`` requires
to/about IMMEDIATELY after "remind me"; "remind me **at 3pm tomorrow** to X"
misses it) is frozen by policy, so the turn rides the live LLM classifier,
which drew ``create_reminder`` only some of the time (turn 1 executed, turn 2
floored on the denser-TEMPORAL-vocabulary sibling phrase). The fix is the
same shape as #1677's: route the shape through the inversion's constrained
router instead of patching the classifier prompt or widening a pre-classifier
regex (both routing-moratorium violations).

This file is a SIBLING of ``test_inversion_write_allowlist_1677.py``, not an
extension of it — that file is create_todo-specific by construction (its
docstring, ``_MSG``/``DEFECT_SHAPES``, and ``TestFlippedTurnReachesTheRail``
are all keyed to todo-create phrasings and the create_todo alias family). The
SHARED constant (``FLIP_WRITE_ALLOWLIST``) and its closed-set/denominator
assertions live in that file, updated in the same commit as this one — both
files must agree on the closed set, and both are run together.

⚠️ LAYER HONESTY (m-43), same caveat as #1677's file: the unit layer uses a
DETERMINISTIC router fake, so these tests prove *the flip routes a
create-reminder operation to create_reminder* — they do NOT prove the live
constrained router draws create_reminder more reliably than the classifier
did for the #1559 phrasings. That is observable only live, in the
``inversion_live_decision`` telemetry, once the flag is actually set (out of
scope for this unit — declaration + pins only).
"""

import contextlib
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
from services.domain.models import Intent  # noqa: E402
from services.intent_service import consent_gate, inversion_live  # noqa: E402
from services.intent_service.inversion_live import (  # noqa: E402
    consult_inversion_live,
)
from services.intent_service.inversion_router import (  # noqa: E402
    RoutingDecision,
    derive_routing_grammar,
)
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.intent_service.workflow_dispatcher import (  # noqa: E402
    FLIP_WRITE_ALLOWLIST,
    get_action_workflows,
)
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.shared_types import (  # noqa: E402
    EffectClass,
    IntentCategory,
    Outwardness,
)

_USER = "3f7b8a52-1559-4b00-9e00-000000001559"  # valid UUID: survives principal parsing
_SESSION = "sess-1559-write-flip"

# The #1559 corpus phrasing, verbatim as given for this unit: the deposited
# turn-1 acceptance case is "remind me at 3pm tomorrow to review the PR"; this
# is the sibling shape the task names for this test file.
_MSG = "remind me at 3pm tomorrow to call the vendor"


# ---------------------------------------------------------------------------
# Fixtures (inherited wholesale from the #1677 flip set, same shape)
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


@pytest.fixture(autouse=True)
def _no_real_user_tz(monkeypatch):
    """handle_create_reminder calls ``get_user_timezone(user_id)`` — on any
    storage failure it fail-safes to None (#1572), but the real path can
    attempt a DB connection (``db.initialize()``) this unit layer has no
    business making. Patched directly so this test proves the ROUTING + WRITE
    path (what this unit is about), not timezone resolution (its own
    coverage elsewhere) — same isolation discipline the create_todo tests
    apply by never touching a real handler dependency they don't need."""
    import services.utils.user_timezone as tz_mod

    async def _none(user_id):
        return None

    monkeypatch.setattr(tz_mod, "get_user_timezone", _none)


@pytest.fixture
def svc():
    return SimpleNamespace(workflow_offer_service=WorkflowOfferService(), intent_classifier=None)


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService.create_todo boundary: records every write.
    handle_create_reminder calls the SAME service method create_todo uses
    (todo_handlers.py's TodoIntentHandlers.todo_service is a
    TodoManagementService instance either way)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {"created": []}

    async def _create(self, user_id, text, priority="medium", **kwargs):
        row = SimpleNamespace(
            id=uuid4(),
            text=text,
            priority=priority,
            user_id=user_id,
            reminder_date=kwargs.get("reminder_date"),
        )
        state["created"].append(row)
        return row

    monkeypatch.setattr(TodoManagementService, "create_todo", _create)
    return state


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
        return [(lvl, f) for lvl, ev, f in self.events if ev == "inversion_live_decision"]


@pytest.fixture
def log_rec(monkeypatch):
    rec = _LogRecorder()
    monkeypatch.setattr(inversion_live, "logger", rec)
    return rec


def _stub_route(monkeypatch, decision):
    from services.intent_service import inversion_router as ir

    calls = []

    async def _route(utterance, session_state=None, **kwargs):
        calls.append(SimpleNamespace(utterance=utterance, session_state=session_state))
        return decision

    monkeypatch.setattr(ir, "route", _route)
    return calls


def _explosive_route(monkeypatch):
    from services.intent_service import inversion_router as ir

    async def _boom(*a, **k):
        raise AssertionError("inversion router consulted — must not be on this path")

    monkeypatch.setattr(ir, "route", _boom)


def _explosive_snapshot(monkeypatch):
    from services.intent_service import snapshot_assembly as sa

    async def _boom(*a, **k):
        raise AssertionError("snapshot assembled — flag-off consult must do zero work")

    monkeypatch.setattr(sa, "assemble_session_snapshot", _boom)


def _decision(operation, confidence=0.9):
    return RoutingDecision(outcome="operation", operation=operation, confidence=confidence)


async def _consult(svc, monkeypatch, log_rec, *, cats, operation, message=_MSG, confidence=0.9):
    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", cats)
    calls = _stub_route(monkeypatch, _decision(operation, confidence))
    out = await consult_inversion_live(
        message, session_id=_SESSION, user_id=_USER, intent_service=svc
    )
    return out, calls, log_rec.decisions()


# ---------------------------------------------------------------------------
# 1. THE ENTRY — allowlisted, no flip_group, canonical name matches
# ---------------------------------------------------------------------------


class TestEntryDeclaration:
    def test_allowlist_includes_create_reminder(self):
        assert "create_reminder" in FLIP_WRITE_ALLOWLIST

    def test_real_rail_create_reminder_declares_the_key_and_no_group(self):
        """create_reminder flips by NAME (or its registry category), never by
        a wave — the same shape as its create_todo sibling: no flip_group, so
        no group token sweeps a write in."""
        wf = get_action_workflows()
        entry = wf["create_reminder"]
        assert entry.flip_write_allowlist_key == "create_reminder"
        assert entry.flip_group is None
        assert entry.effect == EffectClass.WRITE
        assert entry.outwardness == Outwardness.PRIVATE
        assert entry.action_triggered is True

    def test_alias_family_shares_the_same_entry_object(self):
        wf = get_action_workflows()
        ids = {id(wf[k]) for k in ("create_reminder", "set_reminder", "add_reminder")}
        assert len(ids) == 1


# ---------------------------------------------------------------------------
# 2. THE DISPATCH GUARD — mirrors create_todo's TestDispatchGuard one for one
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDispatchGuard:
    async def test_named_create_reminder_flips(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_reminder", operation="create_reminder"
        )
        assert isinstance(out, Intent)
        assert out.action == "create_reminder"
        # EXECUTION from ACTION_REGISTRY — NOT the QUERY fall-through, which
        # would be a lie about a write in the Intent itself.
        assert out.category is IntentCategory.EXECUTION
        assert out.original_message == _MSG
        assert f["reason"] is None and f["live_match"] == "operation"
        assert len(calls) == 1

    async def test_category_surface_reaches_the_allowlisted_write_too(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The same honest consequence create_todo carries: create_reminder
        carries registry category EXECUTION, so flipping that category sweeps
        it in as well — the allowlist bounds WHICH writes, never WHICH
        surface names them."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="EXECUTION", operation="create_reminder"
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category"

    async def test_sub_threshold_still_blocks_the_named_write(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        out, _, [(_, f)] = await _consult(
            svc,
            monkeypatch,
            log_rec,
            cats="create_reminder",
            operation="create_reminder",
            confidence=0.5,
        )
        assert out is None and f["reason"] == "sub_threshold"

    async def test_unnamed_create_reminder_does_not_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Allowlisted != live. A flag naming a READ wave (e.g. read_status)
        must never sweep create_reminder in — no wave carries a write; the
        allowlist says only 'may flip when named' (op or its own registry
        category)."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation="create_reminder"
        )
        assert out is None
        assert f["live_match"] is None and f["reason"] == "not_live_categorized"

    async def test_default_empty_is_still_byte_identically_dark(self, monkeypatch, svc, log_rec):
        """Unchanged by the second write flip: unset => zero work, not even a
        log line. Explosive snapshot AND explosive router — the allowlist
        lookup must not have introduced work before the flag check."""
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        assert log_rec.events == []


# ---------------------------------------------------------------------------
# 3. THE RAIL, END TO END — same handler, consent still evaluated
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestFlippedTurnReachesTheRail:
    async def _run(self, monkeypatch, message, *, spy_calls):
        from services.intent.intent_service import IntentService
        from services.intent_service.classifier import IntentClassifier

        class _ExplosiveLLM:
            def __getattr__(self, name):
                raise AssertionError(f"LLM boundary touched ({name})")

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "create_reminder")
        calls = _stub_route(monkeypatch, _decision("create_reminder", 0.95))
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

        async def _boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — the flip must REPLACE the "
                "classifier draw that #1559 is about"
            )

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)

        real = consent_gate.evaluate_consent

        async def _spy(effect, msg, user_id, outwardness=Outwardness.PRIVATE):
            spy_calls.append((effect, msg, user_id, outwardness))
            return await real(effect, msg, user_id, outwardness=outwardness)

        monkeypatch.setattr(consent_gate, "evaluate_consent", _spy)

        result = await service.process_intent(
            message=message,
            session_id=f"{_SESSION}-{abs(hash(message))}",
            user_id=_USER,
        )
        return result, calls

    async def test_flipped_create_reminder_reaches_the_same_handler_and_writes_the_row(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        spy: list = []
        result, calls = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(calls) == 1, "the inversion router was not consulted"
        assert result.success is True
        assert result.intent_data["action"] == "create_reminder"
        # The actual row — the AC's "creates the row", not just "routed".
        assert len(todo_boundary["created"]) == 1
        assert todo_boundary["created"][0].text == "call the vendor"
        assert todo_boundary["created"][0].reminder_date is not None

    async def test_consent_gate_is_still_evaluated_under_the_flip(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        """The third of Arch's allowlist conditions, held live rather than
        cited — same as #1677's create_todo pin, re-run here for
        create_reminder: a flipped write must still be EVALUATED. A silent
        pass and an unevaluated action are indistinguishable from the
        transcript (m-44), hence the spy."""
        spy: list = []
        result, _ = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(spy) == 1, (
            "consent_gate.evaluate_consent was not consulted on a flipped "
            "create_reminder turn — the flip must not bypass the shared "
            "rail's gate"
        )
        effect, msg, principal, outwardness = spy[0]
        assert effect is EffectClass.WRITE
        assert outwardness is Outwardness.PRIVATE
        assert msg == _MSG and str(principal) == _USER
        # ...and evaluation is not ceremony: one turn, row written, no question.
        assert result.success is True
        assert len(todo_boundary["created"]) == 1


# ---------------------------------------------------------------------------
# 4. Structural fact underneath the claim — same class as #1677's grammar pin
# ---------------------------------------------------------------------------


class TestRouterChoiceSet:
    def test_create_reminder_is_a_grammar_name(self):
        """create_reminder must actually be a name the router can choose —
        not merely allowlisted in the abstract."""
        grammar = derive_routing_grammar()
        assert "create_reminder" in set(grammar.names())
