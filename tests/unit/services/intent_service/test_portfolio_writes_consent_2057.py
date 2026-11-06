"""#2057 — every portfolio write passes the consent gate; a question never writes.

Arch's ruling (2026-10-16 09:03, issue comment 6219485412; ADR-080 D3/D4):

1. The legacy ``manage_portfolio`` / ``manage_repos`` write branches
   (add, archive, restore; link, unlink) dispatch to their rail ops
   (``add_project``, ``archive_project``, ``restore_project``, ``link_repo``,
   ``unlink_repo``), so the #1509/#1510 consent gate decides, whichever surface
   claimed the turn.
2. A question never writes, in either working mode: ``classify_framing``
   gains ``question`` (after the anchored imperative check), and on a WRITE a
   question-framed turn never executes and the declared execute mode never
   escalates it. The reply is CXO's how-to line.

Surface 1 is LIVE in the end-to-end pins below (the real ``PreClassifier``;
the LLM is an explosive stub, so any turn surface 1 did not claim fails
loudly). The writes are recorded at ``PortfolioService`` /
``_create_or_report_project`` / the repo link/unlink methods.

⚠️ LAYER HONESTY: these pins prove dispatch and the gate for each phrasing;
they run no LLM, no real database rows, and no browser render.
"""

import contextlib
from types import SimpleNamespace

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
from services.intent.intent_service import (  # noqa: E402
    IntentProcessingResult,
    IntentService,
)
from services.intent_service.adopted_category_reads_only import (  # noqa: E402
    RAIL_DISPATCH_KEY,
)
from services.intent_service.canonical_handlers import CanonicalHandlers  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.intent_service.collaboration_gate import (  # noqa: E402
    FRAMING_COMPOSE,
    FRAMING_EXECUTE,
    FRAMING_QUESTION,
    WorkingMode,
    classify_framing,
)
from services.intent_service.consent_gate import (  # noqa: E402
    ConsentDecision,
    decide_consent,
    evaluate_consent,
)
from services.intent_service.workflow_entries import register_default_workflows  # noqa: E402
from services.shared_types import EffectClass, IntentCategory, Outwardness  # noqa: E402

_USER = "3f7b8a52-2057-4b00-9e00-000000002057"
_FOO_ID = "11111111-2057-4b00-9e00-000000000001"
FLOOR = "FLOOR-SENTINEL"

# CXO's lines (2026-10-16 08:55; the named add line 09:1x), verbatim.
ARCHIVE_HOW_TO = (
    "To archive a project, say 'archive project Foo'. "
    "You can restore it any time with 'restore project Foo'."
)
RESTORE_HOW_TO = "To restore an archived project, say 'restore project Foo'."
ADD_HOW_TO_NAMED = "To add a project called Foo, say 'add project Foo'."

MODES = [WorkingMode.COLLABORATE, WorkingMode.EXECUTE]


# ---------------------------------------------------------------------------
# Fixtures
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


@pytest.fixture
def writes(monkeypatch):
    """Foo exists; every portfolio write and repo link/unlink is recorded."""
    from services.onboarding.portfolio_service import PortfolioService

    log: list = []
    foo = SimpleNamespace(id=_FOO_ID, name="Foo", is_archived=False)

    async def _find(self, name=None, user_id=None, **kwargs):
        return foo if (name or "").lower() == "foo" else None

    async def _archive(self, project_id=None, user_id=None, **kwargs):
        log.append(("archive", project_id))
        return SimpleNamespace(message="Archived 'Foo'.", status=SimpleNamespace(value="ok"))

    async def _restore(self, project_id=None, user_id=None, **kwargs):
        log.append(("restore", project_id))
        return SimpleNamespace(message="Restored 'Foo'.", status=SimpleNamespace(value="ok"))

    async def _list(self, user_id=None, **kwargs):
        # #2271 (Arch 11-06 12:51, ruling (b)): archive acts only on an EXACT name
        # among the ACTIVE list, so Foo must be on it (it was found only by the
        # tolerant lookup before, which now offers instead of acting).
        return [foo]

    async def _archived(self, user_id=None, **kwargs):
        return []

    async def _create(self_, name, repo_name, session_id, user_id, **kwargs):
        log.append(("create", name))
        return {
            "message": f"Added '{name}'.",
            "intent": {"category": "portfolio", "action": "add_project", "context": {}},
            "requires_clarification": False,
        }

    async def _link(self_, intent, session_id, user_id=None):
        log.append(("link", intent.context.get("original_message")))
        return {"message": "linked", "intent": {"action": "link_repo"}}

    async def _unlink(self_, intent, session_id, user_id=None):
        log.append(("unlink", intent.context.get("original_message")))
        return {"message": "unlinked", "intent": {"action": "unlink_repo"}}

    monkeypatch.setattr(PortfolioService, "find_project_by_name", _find)
    monkeypatch.setattr(PortfolioService, "archive_project", _archive)
    monkeypatch.setattr(PortfolioService, "restore_project", _restore)
    monkeypatch.setattr(PortfolioService, "list_active_projects", _list)
    monkeypatch.setattr(PortfolioService, "list_archived_projects", _archived)
    monkeypatch.setattr(CanonicalHandlers, "_create_or_report_project", _create)
    monkeypatch.setattr(CanonicalHandlers, "_handle_link_repo", _link)
    monkeypatch.setattr(CanonicalHandlers, "_handle_unlink_repo", _unlink)
    return log


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _service(monkeypatch, *, classified=None):
    """Surface 1 live. ``classified`` = (category, action) stubs the classifier
    for a turn surface 1 does not claim (the LLM's draw)."""
    service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    rail_actions: list = []
    original_rail = IntentService._dispatch_action_rail

    async def _spy(self_, intent, **kwargs):
        rail_actions.append(intent.action)
        return await original_rail(self_, intent, **kwargs)

    monkeypatch.setattr(IntentService, "_dispatch_action_rail", _spy)

    if classified is not None:
        category, action = classified

        async def _classify(message, *a, **k):
            return Intent(
                category=category,
                action=action,
                confidence=0.9,
                original_message=message,
                context={"original_message": message},
            )

        monkeypatch.setattr(service.intent_classifier, "classify", _classify)
        from services.intent_service.pre_classifier import MultiIntentResult, PreClassifier

        monkeypatch.setattr(
            PreClassifier,
            "detect_multiple_intents",
            staticmethod(lambda message: MultiIntentResult(original_message=message)),
        )

    async def _floor(self_, intent, *a, **k):
        return IntentProcessingResult(
            success=True, message=FLOOR, intent_data={"action": intent.action}
        )

    monkeypatch.setattr(IntentService, "_handle_floor_with_context", _floor)
    monkeypatch.setattr(IntentService, "_handle_unknown_intent", _floor)
    service._rail_actions = rail_actions  # type: ignore[attr-defined]
    return service


def _armed(service, sid):
    return service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)


def _set_mode(prefs, mode):
    prefs[_USER] = {"working_mode": mode.value}


# ---------------------------------------------------------------------------
# Part 2, framing: a question is QUESTION; an imperative stays EXECUTE
# ---------------------------------------------------------------------------


class TestQuestionFraming:
    @pytest.mark.parametrize(
        "message",
        [
            "how do I archive my project Foo?",
            "how would I add a project called Foo?",
            "how can I restore project Foo",
            "how do I restore project Foo?",
            "what happens if I archive project Foo",
            "is there a way to archive Foo",
            "should I archive project Foo",
            "do I archive Foo here",
            "Foo archived?",
        ],
    )
    def test_questions_read_question(self, message):
        assert classify_framing(message) == FRAMING_QUESTION

    @pytest.mark.parametrize(
        "message",
        [
            "can you archive Foo?",
            "could you please archive project Foo?",
            "archive project Foo",
            "archive project Foo?",
            "add project Foo",
            "restore project Foo",
        ],
    )
    def test_anchored_imperatives_stay_execute(self, message):
        """The anchored imperative check runs first (Arch)."""
        assert classify_framing(message) == FRAMING_EXECUTE

    @pytest.mark.parametrize(
        "message", ["help me write a ticket about the login bug", "let's draft a ticket"]
    )
    def test_compose_unchanged(self, message):
        assert classify_framing(message) == FRAMING_COMPOSE

    def test_a_wh_word_without_an_auxiliary_is_not_a_question(self):
        """ "when I get home remind me ..." is a reminder, not a question."""
        assert classify_framing("when I get home remind me to call mom") != FRAMING_QUESTION


class TestQuestionConsentCells:
    @pytest.mark.parametrize("mode", MODES, ids=lambda m: m.value)
    @pytest.mark.parametrize("outwardness", list(Outwardness), ids=lambda o: o.value)
    def test_write_question_collaborates_in_both_modes(self, mode, outwardness):
        assert (
            decide_consent(EffectClass.WRITE, FRAMING_QUESTION, mode, outwardness=outwardness)
            is ConsentDecision.COLLABORATE
        )

    @pytest.mark.parametrize("mode", MODES, ids=lambda m: m.value)
    def test_read_and_destructive_cells_unchanged(self, mode):
        assert decide_consent(EffectClass.READ, FRAMING_QUESTION, mode) is ConsentDecision.PROCEED
        assert (
            decide_consent(EffectClass.DESTRUCTIVE, FRAMING_QUESTION, mode)
            is ConsentDecision.CONFIRM
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("hint", ["execute", "ambiguous", "compose"])
    async def test_a_router_hint_never_turns_a_question_into_a_write(self, prefs, hint):
        """Execute mode + a router 'execute' hint on a PRIVATE write (where a
        valid hint normally replaces the regex read): still COLLABORATE."""
        _set_mode(prefs, WorkingMode.EXECUTE)
        verdict = await evaluate_consent(
            EffectClass.WRITE,
            "how do I archive my project Foo?",
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=hint,
        )
        assert verdict is ConsentDecision.COLLABORATE


# ---------------------------------------------------------------------------
# Arch's pins, surface 1 LIVE: questions write nothing, in either mode
# ---------------------------------------------------------------------------


class TestQuestionsNeverWrite:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("mode", MODES, ids=lambda m: m.value)
    @pytest.mark.parametrize(
        "message,expected",
        [
            ("how do I archive my project Foo?", ARCHIVE_HOW_TO),
            ("what happens if I archive project Foo?", ARCHIVE_HOW_TO),
            ("how do I restore project Foo?", RESTORE_HOW_TO),
            ("how would I add a project called Foo?", ADD_HOW_TO_NAMED),
        ],
    )
    async def test_surface_one_question_writes_nothing(
        self, monkeypatch, sm, writes, prefs, mode, message, expected
    ):
        _set_mode(prefs, mode)
        service = _service(monkeypatch)
        sid = f"sess-2057-q-{mode.value}-{len(message)}"
        result = await service.process_intent(message, session_id=sid, user_id=_USER)
        assert writes == [], f"a question wrote ({mode.value} mode): {writes}"
        assert result.message == expected, result.message
        assert _armed(service, sid) is None, "a how-to statement must arm nothing"
        # It reached the rail op (the legacy branch no longer answers writes).
        assert service._rail_actions and service._rail_actions[-1] in {
            "archive_project",
            "restore_project",
            "add_project",
        }, service._rail_actions

    @pytest.mark.asyncio
    @pytest.mark.parametrize("mode", MODES, ids=lambda m: m.value)
    async def test_surface_one_unlink_question_gets_a_statement_not_a_confirm(
        self, monkeypatch, sm, writes, prefs, mode
    ):
        """Surface 1 names unlink_repo directly; a question gets the repo
        statement before the #1190 confirm would arm."""
        _set_mode(prefs, mode)
        service = _service(monkeypatch)
        sid = f"sess-2057-unlink-q-{mode.value}"
        result = await service.process_intent(
            "how do I unlink repo acme/widgets from project Foo?", session_id=sid, user_id=_USER
        )
        assert writes == []
        assert (
            result.message
            == "To unlink a repo from a project, say 'unlink repo acme/widgets from <project name>'."
        )
        assert _armed(service, sid) is None


# ---------------------------------------------------------------------------
# Imperatives still write, and only through the rail op
# ---------------------------------------------------------------------------


class TestImperativesWriteThroughTheRail:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message,write,rail",
        [
            ("archive project Foo", ("archive", _FOO_ID), "archive_project"),
            ("restore project Foo", ("restore", _FOO_ID), "restore_project"),
            ("add project Foo", ("create", "Foo"), "add_project"),
        ],
    )
    async def test_surface_one_imperative_executes_via_the_rail_op(
        self, monkeypatch, sm, writes, message, write, rail
    ):
        """Collaborate mode (the default): an explicit imperative is the
        consent (the gate's existing EXECUTE cell), so the rail op runs."""
        service = _service(monkeypatch)
        sid = f"sess-2057-imp-{rail}"
        await service.process_intent(message, session_id=sid, user_id=_USER)
        assert writes == [write], writes
        assert rail in service._rail_actions, service._rail_actions

    @pytest.mark.asyncio
    async def test_can_you_archive_foo_stays_an_imperative(self, monkeypatch, sm, writes):
        """Surface 1 does not claim it; the classifier's PORTFOLIO draw
        reaches the legacy handler, which hands it to archive_project."""
        service = _service(monkeypatch, classified=(IntentCategory.PORTFOLIO, "manage_portfolio"))
        sid = "sess-2057-can-you"
        await service.process_intent("can you archive Foo?", session_id=sid, user_id=_USER)
        assert writes == [("archive", _FOO_ID)], writes
        assert "archive_project" in service._rail_actions

    @pytest.mark.asyncio
    async def test_ambiguous_legacy_write_now_meets_the_consent_check(
        self, monkeypatch, sm, writes
    ):
        """Before #2057 the legacy branch archived this unasked. Now the
        collaborate gate holds it and arms the generic consent check."""
        service = _service(monkeypatch)
        sid = "sess-2057-ambiguous"
        result = await service.process_intent(
            "I would like to archive project Foo", session_id=sid, user_id=_USER
        )
        assert writes == [], "an ambiguous legacy write executed without consent"
        assert result.intent_data.get("consent_check_pending") is True, result.intent_data
        armed = _armed(service, sid)
        assert armed is not None and armed["pending_action"]["action"] == "archive_project"

    @pytest.mark.asyncio
    async def test_ambiguous_legacy_write_proceeds_in_declared_execute_mode(
        self, monkeypatch, sm, writes, prefs
    ):
        _set_mode(prefs, WorkingMode.EXECUTE)
        service = _service(monkeypatch)
        await service.process_intent(
            "I would like to archive project Foo", session_id="sess-2057-amb-exec", user_id=_USER
        )
        assert writes == [("archive", _FOO_ID)]

    @pytest.mark.asyncio
    async def test_classified_link_goes_through_link_repo(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, classified=(IntentCategory.PORTFOLIO, "manage_repos"))
        await service.process_intent(
            "link repo acme/widgets to project Foo", session_id="sess-2057-link", user_id=_USER
        )
        assert writes == [("link", "link repo acme/widgets to project Foo")]
        assert "link_repo" in service._rail_actions

    @pytest.mark.asyncio
    async def test_classified_unlink_meets_the_destructive_confirm(self, monkeypatch, sm, writes):
        """The legacy unlink branch unlinked unconfirmed; through unlink_repo
        the #1190 name-bound confirm arms and nothing is unlinked this turn."""

        async def _resolved(self_, intent, user_id):
            return {
                "ok": True,
                "repo_name": "acme/widgets",
                "project_name": "Foo",
                "is_primary": False,
            }

        monkeypatch.setattr(CanonicalHandlers, "_resolve_unlink_repo_confirmation", _resolved)
        service = _service(monkeypatch, classified=(IntentCategory.PORTFOLIO, "manage_repos"))
        sid = "sess-2057-unlink"
        result = await service.process_intent(
            "unlink repo acme/widgets from project Foo", session_id=sid, user_id=_USER
        )
        assert writes == []
        assert "unlink_repo" in service._rail_actions
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert _armed(service, sid)["pending_action"]["action"] == "unlink_repo"


# ---------------------------------------------------------------------------
# The legacy branch itself never writes (a caller without the rail)
# ---------------------------------------------------------------------------


class TestLegacyBranchNoLongerWrites:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message,rail",
        [
            ("archive project Foo", "archive_project"),
            ("restore project Foo", "restore_project"),
            ("add project Foo", "add_project"),
        ],
    )
    async def test_handler_returns_the_rail_key_and_a_statement(self, sm, writes, message, rail):
        """The multi-intent orchestrator calls CanonicalHandlers.handle
        directly (no rail); it now gets a statement, not a write."""
        handlers = CanonicalHandlers()
        intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="manage_portfolio",
            confidence=1.0,
            original_message=message,
            context={"original_message": message},
        )
        result = await handlers.handle(intent, "sess-2057-direct", _USER)
        assert writes == []
        assert result[RAIL_DISPATCH_KEY] == rail
        assert "say '" in result["message"], result["message"]
