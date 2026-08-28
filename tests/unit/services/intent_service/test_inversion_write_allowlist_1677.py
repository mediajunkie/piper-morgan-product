"""#1677 option (d) — a NAMED write flips through the Inversion, via an
explicit allowlist rather than a relaxed effect check.

The defect (#1677, measured 2026-08-22 with the real classifier, cache off):
"add todo …" has NO deterministic pre-classifier claim, so every todo-create
turn rides the live LLM classifier — whose prompt teaches ``create_ticket`` by
example and carries no ``create_todo`` example. ``add todo buy oat milk`` drew
create_ticket 2/3; ``Add a todo: P1GT-life-<hex>`` drew it 1/3. The user gets
"GitHub isn't connected yet" instead of a saved todo.

Option (d), PM-chosen 2026-08-28: don't patch the classifier prompt or add
pre-classifier surface — route the shape through the successor system, whose
constrained router picks from the derived grammar instead of free-generating
an action name. Arch's ruling (2026-08-25) set the mechanism and it is not
negotiable: **extend both enforcement points to accept READ *or* membership in
a small, explicit, individually-reviewed allowlist** — never relax
``EffectClass.READ`` to ``READ or WRITE``, which would drop the protection
that caught ``create_issue``-filed-under-QUERY for every future write.

Pinned here, in the order the guard is actually assembled:

1. THE CONSTANT — the allowlist is a named, singleton-today frozenset, and a
   typo'd key raises rather than failing safe-but-silent.
2. THE STRUCTURAL GUARD (``WorkflowEntry.__post_init__``) — an unallowlisted
   non-READ entry with a flip_group is STILL unconstructible (the #1685-era
   pin, unchanged); an allowlisted one is constructible.
3. THE DISPATCH GUARD (``inversion_live``) — create_todo flips; create_issue
   (WRITE) and delete_todo (DESTRUCTIVE) still cannot, even when named
   directly; default-empty is still byte-identically dark.
4. THE RAIL, END TO END — under the flip an "add todo …" turn reaches the SAME
   rail handler with the consent gate still evaluated (#1685's spy idiom,
   re-run under the new router).
5. THE #1677 DEFECT SHAPE — the exact phrasings that drew create_ticket.

⚠️ LAYER HONESTY (m-43), stated because this file could otherwise be read as
proving more than it does. The unit layer uses a DETERMINISTIC router fake, so
these tests prove *the flip routes a create-todo operation to create_todo* —
they do NOT prove the live constrained router picks create_todo more often
than the classifier did. What the unit layer CAN show non-fakely, and does
(``test_create_ticket_is_not_even_in_the_grammar``), is that the classifier's
specific failure output is unavailable to the inversion router at all:
``create_ticket`` is not a grammar name — it canonicalizes to ``create_issue``
— so the router's choice set differs in kind from free generation. True
draw-distribution improvement is observable only live, against the real
router, and belongs in the flip's own telemetry (``inversion_live_decision``),
not in this file.
"""

import contextlib
import sys
from pathlib import Path
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
    WorkflowEntry,
    flip_write_allowed,
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

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))

_USER = "3f7b8a52-1677-4b00-9e00-000000001677"  # valid UUID: survives principal parsing
_SESSION = "sess-1677-write-flip"

# The #1677 measurement table, verbatim — the phrasings that drew create_ticket
# from the live classifier, plus the two that held, so the fix is pinned on the
# whole family and not only the broken members.
DEFECT_SHAPES = (
    "add todo buy oat milk",  # 2/3 create_ticket — the worst draw
    "Add a todo: buy oat milk",  # 3/3 create_todo, conf 0.97 — must not regress
    "Add a todo: P1GT-life-a1b2c3",  # 1/3 create_ticket — ticket-shaped content
    "Add a todo: P1GT-a1b2c3",  # 3/3 create_todo — must not regress
)
_MSG = DEFECT_SHAPES[0]


# ---------------------------------------------------------------------------
# Fixtures (inherited wholesale from the #1595/#1667 flip set)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda c: SessionActivityDB.__table__.create(c, checkfirst=True)
        )
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
def svc():
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(), intent_classifier=None
    )


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService.create_todo boundary: records every write (#1685)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {"created": []}

    async def _create(self, user_id, text, priority="medium", **kwargs):
        row = SimpleNamespace(id=uuid4(), text=text, priority=priority, user_id=user_id)
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
        return [
            (lvl, f) for lvl, ev, f in self.events if ev == "inversion_live_decision"
        ]


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
    return RoutingDecision(
        outcome="operation", operation=operation, confidence=confidence
    )


async def _consult(svc, monkeypatch, log_rec, *, cats, operation, message=_MSG,
                   confidence=0.9):
    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", cats)
    calls = _stub_route(monkeypatch, _decision(operation, confidence))
    out = await consult_inversion_live(
        message, session_id=_SESSION, user_id=_USER, intent_service=svc
    )
    return out, calls, log_rec.decisions()


# ---------------------------------------------------------------------------
# 1. THE CONSTANT — named, small, and expensive to extend on purpose
# ---------------------------------------------------------------------------


class TestAllowlistConstant:
    def test_allowlist_is_exactly_create_todo_today(self):
        """A CHANGE-DETECTOR on purpose (Arch's ruling: 'small, explicit,
        individually-reviewed'). Adding a name must break this assertion so the
        addition is visible in review — and the constant's own comment carries
        the three verification conditions the new name owes."""
        assert FLIP_WRITE_ALLOWLIST == frozenset({"create_todo"})

    def test_the_three_conditions_are_written_beside_the_constant(self):
        """The comment is the mechanism (nothing else forces the verification),
        so its absence is a defect. Checked by content, not by line number."""
        src = Path("services/intent_service/workflow_dispatcher.py").read_text(
            encoding="utf-8"
        )
        block = src.split("FLIP_WRITE_ALLOWLIST: frozenset")[0]
        for phrase in (
            "CONFIRMED REGISTERED",
            "READING THE HANDLER'S",
            "consent_gate.evaluate_consent",
        ):
            assert phrase in block, f"allowlist comment lost condition: {phrase}"

    def test_read_entries_need_no_key(self):
        entry = WorkflowEntry(entry_point=lambda **k: None, effect=EffectClass.READ)
        assert entry.flip_write_allowlist_key is None
        assert flip_write_allowed(entry) is True  # READ, unchanged

    def test_unknown_key_raises_rather_than_failing_silently_safe(self):
        """A typo'd key fails SAFE at dispatch (the write just never flips) and
        is therefore invisible — it would sit there looking reviewed while
        naming nothing."""
        with pytest.raises(ValueError) as exc:
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=EffectClass.WRITE,
                flip_write_allowlist_key="create_todoo",
                description="typo'd allowlist key",
            )
        assert "create_todoo" in str(exc.value)
        assert "create_todo" in str(exc.value)  # names the real vocabulary


# ---------------------------------------------------------------------------
# 2. THE STRUCTURAL GUARD — relaxed by exactly one named exception
# ---------------------------------------------------------------------------


class TestConstructorGuard:
    @pytest.mark.parametrize("effect", [EffectClass.WRITE, EffectClass.DESTRUCTIVE])
    def test_unallowlisted_non_read_with_flip_group_still_unconstructible(self, effect):
        """THE #1685-era pin, and it must stay green: extending the guard for a
        named write must not become a general opening. An entry nobody put on
        the allowlist cannot be brought into existence carrying a group."""
        with pytest.raises(ValueError) as exc:
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=effect,
                flip_group="read_status",
                description="a write pretending it can flip",
            )
        msg = str(exc.value)
        assert "read_status" in msg and effect.name in msg
        assert "READ-only" in msg  # says WHY
        assert "flip_write_allowlist_key" in msg  # and names the one exception

    def test_allowlisted_write_with_a_group_is_constructible(self):
        """The exception, exercised: the same construction the guard refuses
        above succeeds once the entry declares a reviewed name."""
        entry = WorkflowEntry(
            entry_point=lambda **k: None,
            effect=EffectClass.WRITE,
            flip_group="read_status",
            flip_write_allowlist_key="create_todo",
            description="allowlisted named write",
        )
        assert flip_write_allowed(entry) is True

    def test_real_rail_create_todo_declares_the_key_and_no_group(self):
        """create_todo flips by NAME (or its registry category), never by a
        wave: it carries no flip_group, so no group token sweeps a write in."""
        wf = get_action_workflows()
        entry = wf["create_todo"]
        assert entry.flip_write_allowlist_key == "create_todo"
        assert entry.flip_group is None
        assert entry.effect == EffectClass.WRITE

    def test_no_other_rail_entry_declares_a_key(self):
        """The denominator, stated (m-43): ONE entry object on the whole rail
        claims an allowlist name. If this grows, it grew in review."""
        wf = get_action_workflows()
        declared = {
            k for k, e in wf.items() if e.flip_write_allowlist_key is not None
        }
        assert declared == {"create_todo", "add_todo", "new_todo"}, (
            "the create_todo alias family shares ONE entry object; anything "
            "else here is a second allowlisted operation"
        )
        assert len({id(wf[k]) for k in declared}) == 1


# ---------------------------------------------------------------------------
# 3. THE DISPATCH GUARD — what flips, what still cannot, and the dark default
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDispatchGuard:
    async def test_named_create_todo_flips(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_todo", operation="create_todo"
        )
        assert isinstance(out, Intent)
        assert out.action == "create_todo"
        # EXECUTION from ACTION_REGISTRY — NOT the QUERY fall-through, which
        # would be a lie about a write in the Intent itself.
        assert out.category is IntentCategory.EXECUTION
        assert out.original_message == _MSG
        assert f["reason"] is None and f["live_match"] == "operation"
        assert len(calls) == 1

    async def test_unallowlisted_write_still_cannot_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """create_issue is the operation the guard was BUILT for: WRITE, but
        filed under QUERY in ACTION_REGISTRY. Naming it directly — the most
        explicit request possible — is still refused. This is the pin that
        proves the change was an allowlist and not a class relaxation."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_issue", operation="create_issue"
        )
        assert out is None
        assert f["reason"] == "not_read_effect"
        assert f["live_match"] == "operation"  # named live, and STILL refused

    async def test_unallowlisted_destructive_still_cannot_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """delete_todo: registered (#1666), DESTRUCTIVE, sibling of the very
        op we allowlisted — the nearest miss there is."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="delete_todo", operation="delete_todo"
        )
        assert out is None and f["reason"] == "not_read_effect"

    async def test_category_surface_reaches_the_allowlisted_write_too(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The honest consequence, pinned rather than discovered later: the
        allowlist bounds WHICH writes may flip, never WHICH SURFACE names
        them. create_todo carries registry category EXECUTION, so flipping
        that category sweeps it in as well. Operators flipping EXECUTION
        should know they are flipping a write."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="EXECUTION", operation="create_todo"
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category"

    async def test_sub_threshold_still_blocks_the_named_write(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_todo", operation="create_todo",
            confidence=0.5,
        )
        assert out is None and f["reason"] == "sub_threshold"

    async def test_unnamed_create_todo_does_not_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Allowlisted ≠ live. The allowlist says 'may flip when named'; a flag
        naming something else leaves create_todo on the legacy chain."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation="create_todo"
        )
        assert out is None
        assert f["live_match"] is None and f["reason"] == "not_live_categorized"

    async def test_default_empty_is_still_byte_identically_dark(
        self, monkeypatch, svc, log_rec
    ):
        """Unchanged by the write flip: unset ⇒ zero work, not even a log line.
        Explosive snapshot AND explosive router — the allowlist lookup must not
        have introduced work before the flag check."""
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        assert log_rec.events == []


# ---------------------------------------------------------------------------
# 4. THE RAIL, END TO END — same handler, consent still evaluated
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestFlippedTurnReachesTheRail:
    async def _run(self, monkeypatch, message, *, spy_calls):
        from services.intent.intent_service import IntentService
        from services.intent_service.classifier import IntentClassifier

        class _ExplosiveLLM:
            def __getattr__(self, name):
                raise AssertionError(f"LLM boundary touched ({name})")

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "create_todo")
        calls = _stub_route(monkeypatch, _decision("create_todo", 0.95))
        service = IntentService(
            intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM())
        )

        async def _boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — the flip must REPLACE the "
                "classifier draw that #1677 is about"
            )

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)

        real = consent_gate.evaluate_consent

        async def _spy(effect, msg, user_id, outwardness=Outwardness.PRIVATE):
            spy_calls.append((effect, msg, user_id, outwardness))
            return await real(effect, msg, user_id, outwardness=outwardness)

        monkeypatch.setattr(consent_gate, "evaluate_consent", _spy)

        result = await service.process_intent(
            message=message, session_id=f"{_SESSION}-{abs(hash(message))}",
            user_id=_USER,
        )
        return result, calls

    async def test_flipped_create_reaches_the_same_handler_and_writes_the_row(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        spy: list = []
        result, calls = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(calls) == 1, "the inversion router was not consulted"
        assert result.success is True
        assert result.intent_data["action"] == "create_todo"
        # The actual row — the AC's "creates the row", not just "routed".
        assert len(todo_boundary["created"]) == 1
        assert todo_boundary["created"][0].text == "buy oat milk"

    async def test_consent_gate_is_still_evaluated_under_the_flip(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        """#1685's assertion, re-run against the NEW router. This is the third
        of Arch's allowlist conditions, held live rather than cited: a flipped
        write must still be EVALUATED. A silent pass and an unevaluated action
        are indistinguishable from the transcript (m-44) — hence the spy."""
        spy: list = []
        result, _ = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(spy) == 1, (
            "consent_gate.evaluate_consent was not consulted on a flipped "
            "create_todo turn — the flip must not bypass the shared rail's gate"
        )
        effect, msg, principal, outwardness = spy[0]
        assert effect is EffectClass.WRITE
        assert outwardness is Outwardness.PRIVATE
        assert msg == _MSG and str(principal) == _USER
        # ...and evaluation is not ceremony: one turn, row written, no question.
        assert result.success is True
        assert len(todo_boundary["created"]) == 1


# ---------------------------------------------------------------------------
# 5. THE #1677 DEFECT SHAPE — the regression test proper
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDefectShapesRouteToCreateTodo:
    """The phrasings the probe measured drawing ``create_ticket`` from the live
    classifier (1/3–2/3), pinned to route to create_todo under the flip.

    ⚠️ What this proves and what it does not (m-43, restated at the assertion
    because this is the class most likely to be over-read): the router here is
    a deterministic fake, so this pins THE ROUTING PATH — every one of these
    utterances, given a create_todo operation, reaches the create_todo rail
    handler rather than any ticket path. It does not, and cannot at the unit
    layer, show that the real constrained router picks create_todo more often
    than the classifier did. See ``test_create_ticket_is_not_even_in_the_
    grammar`` for the one non-faked structural fact underneath the claim.
    """

    @pytest.mark.parametrize("message", DEFECT_SHAPES)
    async def test_defect_shape_routes_to_create_todo(
        self, sm, mem_prefs, svc, monkeypatch, log_rec, message
    ):
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_todo",
            operation="create_todo", message=message,
        )
        assert isinstance(out, Intent)
        assert out.action == "create_todo"
        assert out.category is IntentCategory.EXECUTION
        assert out.original_message == message
        assert f["route"] == "inversion" and f["reason"] is None


class TestRouterChoiceSet:
    def test_create_ticket_is_not_even_in_the_grammar(self):
        """The structural half of the #1677 fix, and the only part of this file
        that is not mediated by a fake: the classifier's failure output is not
        in the inversion router's choice set at all. ``create_ticket`` is not a
        grammar name — it canonicalizes to ``create_issue`` — so the router
        cannot emit the string that produced 'GitHub isn't connected yet'. It
        can still CHOOSE create_issue (a different failure, and one that stays
        unflippable per TestDispatchGuard); what it cannot do is free-generate
        a name the way the classifier did."""
        grammar = derive_routing_grammar()
        assert "create_ticket" not in set(grammar.names())
        assert grammar.alias_to_canonical.get("create_ticket") == "create_issue"
        assert "create_todo" in set(grammar.names())
