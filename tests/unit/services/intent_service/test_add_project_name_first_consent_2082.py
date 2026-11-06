"""#2082 — name first; consent arms only on a resolved target (Arch's ruling
2026-10-18 09:28, agreeing with CXO's 08:27 user-side ruling).

Served (Web, alpha 47ba746bee, add_project live): "I'd like to start a new
project" got the generic consent check ("…asking me to add project… Should I
go ahead? (yes/no)") and, after yes, the one-line name ask — the yes consented
to nothing. Now a HELD add_project turn with no name asks for the name first
("What would you like to call it?", the #2080 carrier's words) and writes
``consent_owed`` into the carrier's payload from the gate's verdict; the named
turn arms the one confirm (``Add a project called "X"? (yes/no)``) instead of
writing. PROCEED (an imperative, or direct mode) and name-bearing turns are
unchanged.

Harness: the 2057 file's shape — a real IntentService with the LLM boundary
guarded, the classifier stubbed to the router's add_project draw (surface 1 no
longer owns the phrasing; the live consult is off in this environment, so
the stub stands in for the rail-bound intent), the create recorded.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.database.models import SessionActivityDB
from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.add_project_clarify import (
    ADD_PROJECT_CONFIRM_KIND,
    ADD_PROJECT_NAME_QUESTION_KIND,
)
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.classifier import IntentClassifier
from services.intent_service.collaboration_gate import WorkingMode
from services.intent_service.workflow_entries import register_default_workflows
from services.intent_service.write_confirm_words import ADD_PROJECT_NAME_QUESTION
from services.shared_types import IntentCategory

_USER = "3f7b8a52-2082-4b00-9e00-000000002082"
CONFIRM_KLATCH = 'Add a project called "Klatch"? (yes/no)'
DECLINE_KLATCH = 'Okay — I won\'t add a project called "Klatch". Nothing has been changed.'
DECLARATIVE = "I'd like to start a new project"
IMPERATIVE = "add a new project"


# ---------------------------------------------------------------------------
# Fixtures (the 2057 shape)
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


@pytest.fixture(autouse=True)
def prefs(monkeypatch):
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
def _armed_consult_binds(monkeypatch):
    """The name carrier's armed-turn router consult (#1886(b)) defaults to a
    ``none`` outcome → BIND, so no router call and no key dependence."""
    from services.intent_service import inversion_router as ir
    from services.intent_service.inversion_router import RoutingDecision

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(outcome="none")

    monkeypatch.setattr(ir, "route", _route)


@pytest.fixture
def writes(monkeypatch):
    log: list = []

    async def _create(self_, name, repo_name, session_id, user_id, **kwargs):
        log.append(("create", name))
        return {
            "message": f"Added '{name}'.",
            "intent": {"category": "portfolio", "action": "add_project", "context": {}},
            "requires_clarification": False,
        }

    monkeypatch.setattr(CanonicalHandlers, "_create_or_report_project", _create)
    return log


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _service(monkeypatch):
    """A real IntentService; the classifier stubbed to the router's add_project
    draw for every message (surface 1 no longer owns the add phrasings;
    this is the rail-bound intent the live consult would hand over)."""
    service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

    async def _classify(message, *a, **k):
        return Intent(
            category=IntentCategory.PORTFOLIO,
            action="add_project",
            confidence=0.95,
            original_message=message,
            context={"original_message": message},
        )

    monkeypatch.setattr(service.intent_classifier, "classify", _classify)
    from services.intent_service.pre_classifier import MultiIntentResult, PreClassifier

    monkeypatch.setattr(PreClassifier, "pre_classify", staticmethod(lambda m: None))
    monkeypatch.setattr(
        PreClassifier,
        "pre_classify_with_pattern_list",
        staticmethod(lambda m: (None, None)),
    )
    monkeypatch.setattr(
        PreClassifier,
        "detect_multiple_intents",
        staticmethod(lambda m: MultiIntentResult(intents=[], is_multi_intent=False)),
    )
    return service


def _pending(service, sid):
    return service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)


def _set_mode(prefs, mode):
    prefs[_USER] = {"working_mode": mode.value}


async def _turn(service, sid, text):
    return await service.process_intent(text, session_id=sid, user_id=_USER)


# ---------------------------------------------------------------------------
# Arch's six pins
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_collaborate_declarative_asks_the_name_first_no_consent_offer_no_row(
    monkeypatch, sm, writes, prefs
):
    _set_mode(prefs, WorkingMode.COLLABORATE)
    service = _service(monkeypatch)
    sid = "sess-2082-1"
    result = await _turn(service, sid, DECLARATIVE)
    # #2304: CXO's 11-06 name question (was ADD_PROJECT_ACCEPT_NAME_QUESTION,
    # "What would you like to call it?"), still armed on the #2080 carrier.
    assert result.message == ADD_PROJECT_NAME_QUESTION, result.message
    assert "Should I go ahead" not in result.message
    assert writes == [], writes
    pending = _pending(service, sid)
    assert pending is not None
    assert pending["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert pending["pending_action"]["consent_owed"] is True
    assert pending["question"] == ADD_PROJECT_NAME_QUESTION
    assert result.intent_data.get("consent_owed") is True
    assert result.intent_data.get("consent_check_pending") is None


@pytest.mark.asyncio
async def test_then_a_name_arms_the_one_confirm_and_yes_writes_one_row(
    monkeypatch, sm, writes, prefs
):
    _set_mode(prefs, WorkingMode.COLLABORATE)
    service = _service(monkeypatch)
    sid = "sess-2082-2"
    await _turn(service, sid, DECLARATIVE)
    named = await _turn(service, sid, "Klatch")
    assert named.message == CONFIRM_KLATCH, named.message
    assert writes == [], "the named turn must not write when consent is owed"
    pending = _pending(service, sid)
    assert pending["pending_action"]["kind"] == ADD_PROJECT_CONFIRM_KIND
    assert pending["pending_action"]["name"] == "Klatch"
    done = await _turn(service, sid, "yes")
    assert writes == [("create", "Klatch")], writes
    assert "Klatch" in done.message


@pytest.mark.asyncio
async def test_the_same_chain_with_no_declines_and_writes_nothing(monkeypatch, sm, writes, prefs):
    _set_mode(prefs, WorkingMode.COLLABORATE)
    service = _service(monkeypatch)
    sid = "sess-2082-3"
    await _turn(service, sid, DECLARATIVE)
    await _turn(service, sid, "Klatch")
    declined = await _turn(service, sid, "no")
    assert declined.message == DECLINE_KLATCH, declined.message
    assert writes == [], writes
    assert _pending(service, sid) is None


@pytest.mark.asyncio
async def test_an_imperative_then_a_name_writes_with_no_confirm(monkeypatch, sm, writes, prefs):
    """PROCEED: the imperative is the consent; the name ask arms without the
    flag and the named turn binds and writes, as before #2082."""
    _set_mode(prefs, WorkingMode.COLLABORATE)
    service = _service(monkeypatch)
    sid = "sess-2082-4"
    first = await _turn(service, sid, IMPERATIVE)
    assert writes == []
    pending = _pending(service, sid)
    assert pending["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert pending["pending_action"].get("consent_owed") is False
    assert "Should I go ahead" not in first.message
    named = await _turn(service, sid, "Klatch")
    assert writes == [("create", "Klatch")], writes
    assert "Klatch" in named.message
    assert named.message != CONFIRM_KLATCH


@pytest.mark.asyncio
async def test_direct_mode_declarative_behaves_like_the_imperative(monkeypatch, sm, writes, prefs):
    _set_mode(prefs, WorkingMode.EXECUTE)
    service = _service(monkeypatch)
    sid = "sess-2082-5"
    await _turn(service, sid, DECLARATIVE)
    pending = _pending(service, sid)
    assert pending["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert pending["pending_action"].get("consent_owed") is False
    named = await _turn(service, sid, "Klatch")
    assert writes == [("create", "Klatch")], writes
    assert named.message != CONFIRM_KLATCH


@pytest.mark.asyncio
async def test_consent_owed_survives_the_carriers_re_ask(monkeypatch, sm, writes, prefs):
    """A bare 'yes' at the name ask re-asks (the carrier re-stores the same
    record); the real name afterwards still arms the confirm, never writes."""
    _set_mode(prefs, WorkingMode.COLLABORATE)
    service = _service(monkeypatch)
    sid = "sess-2082-6"
    await _turn(service, sid, DECLARATIVE)
    reasked = await _turn(service, sid, "yes")
    assert "No project has been created yet" in reasked.message, reasked.message
    pending = _pending(service, sid)
    assert pending["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
    assert pending["pending_action"]["consent_owed"] is True
    named = await _turn(service, sid, "Klatch")
    assert named.message == CONFIRM_KLATCH, named.message
    assert writes == [], writes
