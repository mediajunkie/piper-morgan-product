"""#1595 unit 3b — the THIRD named op flips through the Inversion, and the
FIRST DESTRUCTIVE one: ``delete_todo``, via the same #1677 allowlist
mechanism ``create_todo``/``create_reminder`` used (never a relaxed effect
check, never a ``flip_group``).

Arch's Q1 floor ruling (2026-09-25, replying to Lead's #1595 question):
"#1677's 'WRITE' was never a categorical ceiling — extend the allowlist to a
DESTRUCTIVE op, individually verified, same as create_todo/create_reminder
were." The shared #1190 gate (``needs_confirm = effect == DESTRUCTIVE``) is
keyed on the entry's DECLARED effect, not on which router proposed the
operation — ``inversion_live``'s flip path fetches the IDENTICAL
``WorkflowEntry`` object the legacy classifier dispatches through, same
registry, same effect, same downstream gates. Arch's one build-time
condition for a DESTRUCTIVE flip (not asked of the two WRITE entries): the
rendered confirm prompt must pull its identifying detail from the SAME
slot-extraction path the legacy dispatch uses — proven here, not assumed,
in ``TestConfirmProvenanceParity``.

The corpus row this closes (#1606, PM live 2026-08-12): "please clear the
reminders except for 'Review the PR' — also, can you set my default repo
conversationally?" The 2026-09-25 shadow score
(docs/internal/architecture/current/inversion-phase1-shadow-score-2026-09-25.md)
shows the live constrained router draws ``delete_todo`` @0.9 for this
phrasing, and ``delete_todo`` @0.9 for the sibling "delete my hydrate
reminder" — ``delete_todo`` (not ``clear_reminders_delete``, which is
offer-only / ``action_triggered=False`` and unreachable by a fresh
classification) is the operation actually named for this shape, and is
what this allowlist entry addresses.

This file is a SIBLING of ``test_inversion_write_allowlist_1677.py`` and
``test_inversion_write_allowlist_create_reminder_1559.py``, not an
extension of either — the SHARED constant (``FLIP_WRITE_ALLOWLIST``) and
its closed-set/denominator assertions live in the 1677 file, updated in the
same commit as this one; all three files must agree on the closed set and
are run together.

⚠️ LAYER HONESTY (m-43), same caveat as the sibling files': the unit layer
uses a DETERMINISTIC router fake, so these tests prove *the flip routes a
delete-todo operation to delete_todo, and the confirm it arms matches the
legacy confirm* — they do NOT prove the live constrained router draws
delete_todo more reliably than the classifier did for the #1606 phrasings.
That is observable only live, in the ``inversion_live_decision`` telemetry,
once the flag is actually set (out of scope for this unit — declaration +
pins only).
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
from services.domain.models import Intent, Todo  # noqa: E402
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service import consent_gate, inversion_live  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
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

_USER = "3f7b8a52-1606-4b00-9e00-000000001606"  # valid UUID: survives principal parsing
_SESSION = "sess-1606-write-flip"

# The #1606 corpus phrasing is the two-part clear/question message; the
# sibling shape this unit's dispatch tests exercise (mirroring the sibling
# files' convention of a plain, unambiguous single-op message for the
# dispatch-guard class) is the taught-and-denied phrase PM hit live
# (2026-08-29, #1527): "delete my hydrate reminder" — @0.9 in the same
# 2026-09-25 shadow score row that scored #1606's own phrasing.
_MSG = "delete my hydrate reminder"


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
# Fixtures (inherited wholesale from the #1677/#1559 flip sets, same shape)
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
def svc():
    return SimpleNamespace(workflow_offer_service=WorkflowOfferService(), intent_classifier=None)


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic (the hydrate
    reminder is row 1, mirroring the #1527 fixture); delete EXPLOSIVE until
    a test arms it — nothing may mutate on an unconfirmed turn, flipped or
    legacy alike."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo("hydrate"), _todo("Review the PR")],
        "deleted": [],
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes (flipped or legacy path)"
            )
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
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
# 1. THE ENTRY — allowlisted, no flip_group, canonical name matches, DESTRUCTIVE
# ---------------------------------------------------------------------------


class TestEntryDeclaration:
    def test_allowlist_includes_delete_todo(self):
        assert "delete_todo" in FLIP_WRITE_ALLOWLIST

    def test_real_rail_delete_todo_declares_the_key_and_no_group(self):
        """delete_todo flips by NAME (or its registry category), never by a
        wave — the same shape as create_todo/create_reminder: no
        flip_group, so no group token sweeps a write in. Effect is
        DESTRUCTIVE, not WRITE — this is the first entry on the allowlist
        for which that distinction matters."""
        wf = get_action_workflows()
        entry = wf["delete_todo"]
        assert entry.flip_write_allowlist_key == "delete_todo"
        assert entry.flip_group is None
        assert entry.effect == EffectClass.DESTRUCTIVE
        assert entry.outwardness == Outwardness.PRIVATE
        assert entry.action_triggered is True

    def test_alias_family_shares_the_same_entry_object(self):
        wf = get_action_workflows()
        ids = {
            id(wf[k])
            for k in (
                "delete_todo",
                "remove_todo",
                "cancel_todo",
                "delete_reminder",
                "remove_reminder",
                "cancel_reminder",
            )
        }
        assert len(ids) == 1

    def test_destructive_entry_still_needs_confirm(self):
        """The property the whole exercise turns on: DESTRUCTIVE derives
        needs_confirm True — a flipped delete_todo turn must ARM a confirm,
        never execute in one turn the way the WRITE allowlist entries do."""
        wf = get_action_workflows()
        entry = wf["delete_todo"]
        assert entry.needs_consent is True
        assert entry.needs_confirm is True


# ---------------------------------------------------------------------------
# 2. THE DISPATCH GUARD — mirrors create_todo/create_reminder's
#    TestDispatchGuard one for one
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDispatchGuard:
    async def test_named_delete_todo_flips(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="delete_todo", operation="delete_todo"
        )
        assert isinstance(out, Intent)
        assert out.action == "delete_todo"
        # EXECUTION from ACTION_REGISTRY — NOT the QUERY fall-through, which
        # would be a lie about a destructive write in the Intent itself.
        assert out.category is IntentCategory.EXECUTION
        assert out.original_message == _MSG
        assert f["reason"] is None and f["live_match"] == "operation"
        assert len(calls) == 1

    async def test_category_surface_reaches_the_allowlisted_destructive_write_too(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The same honest consequence create_todo/create_reminder carry:
        delete_todo carries registry category EXECUTION, so flipping that
        category sweeps it in as well — the allowlist bounds WHICH writes,
        never WHICH surface names them."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="EXECUTION", operation="delete_todo"
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category"

    async def test_sub_threshold_still_blocks_the_named_destructive_op(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        out, _, [(_, f)] = await _consult(
            svc,
            monkeypatch,
            log_rec,
            cats="delete_todo",
            operation="delete_todo",
            confidence=0.5,
        )
        assert out is None and f["reason"] == "sub_threshold"

    async def test_unnamed_delete_todo_does_not_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Allowlisted != live. A flag naming a READ wave (e.g. read_status)
        must never sweep delete_todo in — no wave carries a write (or a
        destructive write); the allowlist says only 'may flip when named'
        (op or its own registry category)."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation="delete_todo"
        )
        assert out is None
        assert f["live_match"] is None and f["reason"] == "not_live_categorized"

    async def test_default_empty_is_still_byte_identically_dark(self, monkeypatch, svc, log_rec):
        """Unchanged by the third write flip: unset => zero work, not even a
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
# 3. THE RAIL, END TO END — same handler, confirm ARMED (never a delete)
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.mark.asyncio
class TestFlippedTurnReachesTheRail:
    async def _run(self, monkeypatch, message, *, spy_calls, confidence=0.95):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "delete_todo")
        calls = _stub_route(monkeypatch, _decision("delete_todo", confidence))
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

        async def _boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — the flip must REPLACE the "
                "classifier draw that #1606 is about"
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
        return result, calls, service

    async def test_flipped_delete_todo_arms_the_confirm_and_deletes_nothing(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        spy: list = []
        result, calls, service = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(calls) == 1, "the inversion router was not consulted"
        # The core DESTRUCTIVE-vs-WRITE distinction this unit adds: the
        # flipped turn must ARM, not execute.
        assert result.success is True
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        assert todo_boundary["deleted"] == [], (
            "a flipped delete_todo turn deleted a row on the classifying "
            "turn — the #1190 confirm gate did not hold"
        )
        # A confirmed "yes" completes the SAME flow a legacy-classified
        # confirm would (the pending offer is armed on the real session store).
        todo_boundary["allow_delete"] = True
        sid = f"{_SESSION}-{abs(hash(_MSG))}"
        yes_result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert len(todo_boundary["deleted"]) == 1
        assert "hydrate" in yes_result.message

    async def test_consent_gate_is_still_evaluated_under_the_flip(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        """The third of Arch's allowlist conditions, held live rather than
        cited — same as the WRITE entries' pin, re-run here for delete_todo:
        a flipped destructive op must still be EVALUATED, and the verdict
        must be CONFIRM (not PROCEED — DESTRUCTIVE never proceeds silently,
        execute framing or not). A silent pass and an unevaluated action are
        indistinguishable from the transcript (m-44), hence the spy."""
        spy: list = []
        result, _, _ = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(spy) == 1, (
            "consent_gate.evaluate_consent was not consulted on a flipped "
            "delete_todo turn — the flip must not bypass the shared rail's gate"
        )
        effect, msg, principal, outwardness = spy[0]
        assert effect is EffectClass.DESTRUCTIVE
        assert outwardness is Outwardness.PRIVATE
        assert msg == _MSG and str(principal) == _USER
        assert result.intent_data.get("destructive_confirmation_pending") is True


# ---------------------------------------------------------------------------
# 4. Structural fact underneath the claim — same class as the sibling files'
#    grammar pin
# ---------------------------------------------------------------------------


class TestRouterChoiceSet:
    def test_delete_todo_is_a_grammar_name(self):
        """delete_todo must actually be a name the router can choose — not
        merely allowlisted in the abstract."""
        grammar = derive_routing_grammar()
        assert "delete_todo" in set(grammar.names())


# ---------------------------------------------------------------------------
# 5. CONFIRM PROVENANCE PARITY — Arch's one build-time condition for a
#    DESTRUCTIVE flip, proven rather than assumed.
# ---------------------------------------------------------------------------


def _stub_legacy_classification(monkeypatch, service, message, action="delete_todo"):
    """Deterministic surface-2 emission (the #1666/#1527 idiom) — an Intent
    that reached the rail via the LEGACY classifier, never the inversion."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)
    return intent


@pytest.mark.asyncio
class TestConfirmProvenanceParity:
    """Arch's extra condition, verbatim: 'when you allowlist a DESTRUCTIVE
    op, confirm the rendered confirm prompt pulls its identifying detail
    (the specific title/item) from the same slot-extraction path the legacy
    dispatch uses — not a differently-shaped inversion-specific confirm copy
    that could drop the identifying detail the user needs to catch a
    misparse before confirming.'

    Two tests, same assertion (the rendered confirm question text), two
    DIFFERENT Intent provenances (inversion-consulted vs. legacy-classified)
    — the confirm strings are then compared for equality directly. Both
    must equal the literal title-bound confirm ``build_todo_delete_
    confirmation`` renders for "delete my hydrate reminder" against the
    shared ``todo_boundary`` fixture's list (the #1527 pin's own literal:
    ``'Delete todo: "hydrate"? (yes/no)'``), proving the SAME slot-
    extraction path (``intent.original_message`` / ``intent.context[
    "original_message"]`` → ``_named_delete_target`` →
    ``resolve_named_todo_target`` against the owner-scoped list) runs
    regardless of which router produced the Intent.
    """

    _EXPECTED_CONFIRM = 'Delete todo: "hydrate"? (yes/no)'

    async def _run_flipped(self, monkeypatch, todo_boundary, session_suffix):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "delete_todo")
        _stub_route(monkeypatch, _decision("delete_todo", 0.95))
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

        async def _boom(*a, **k):
            raise AssertionError("classify_multiple consulted on the flipped provenance leg")

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)

        result = await service.process_intent(
            message=_MSG, session_id=f"{_SESSION}-{session_suffix}", user_id=_USER
        )
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert todo_boundary["deleted"] == []
        return result.message

    async def _run_legacy(self, monkeypatch, todo_boundary, session_suffix):
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
        _stub_legacy_classification(monkeypatch, service, _MSG)

        async def _boom_router(*a, **k):
            raise AssertionError(
                "inversion router consulted on the legacy provenance leg — "
                "PIPER_INVERSION_LIVE_CATEGORIES is unset for this test"
            )

        from services.intent_service import inversion_router as ir

        monkeypatch.setattr(ir, "route", _boom_router)

        result = await service.process_intent(
            message=_MSG, session_id=f"{_SESSION}-{session_suffix}", user_id=_USER
        )
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert todo_boundary["deleted"] == []
        return result.message

    # --- Test 1: the FLIPPED (inversion-consulted) Intent provenance -------
    async def test_flipped_confirm_matches_the_expected_title_bound_text(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        flipped = await self._run_flipped(monkeypatch, todo_boundary, "flip-provenance")
        assert flipped == self._EXPECTED_CONFIRM

    # --- Test 2: the LEGACY (classifier-produced) Intent provenance --------
    async def test_legacy_confirm_matches_the_expected_title_bound_text(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        legacy = await self._run_legacy(monkeypatch, todo_boundary, "legacy-provenance")
        assert legacy == self._EXPECTED_CONFIRM

    # --- Direct equality, self-contained (both legs run inside ONE test, so
    #     this does not depend on inter-test ordering or shared state) ------
    async def test_flipped_and_legacy_confirm_strings_are_identical(
        self, mem_prefs, todo_boundary, monkeypatch
    ):
        """Arch's condition, proven directly: build both provenances inside
        one test and compare the two rendered confirm strings for equality
        — the assertion the condition is actually about, not merely each
        leg matching a shared literal independently."""
        flipped = await self._run_flipped(monkeypatch, todo_boundary, "combined-flip")
        legacy = await self._run_legacy(monkeypatch, todo_boundary, "combined-legacy")
        assert flipped == legacy == self._EXPECTED_CONFIRM
