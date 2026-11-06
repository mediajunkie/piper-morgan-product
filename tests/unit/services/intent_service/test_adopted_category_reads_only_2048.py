"""#2048 follow-up — an ADOPTED category runs READ operations only.

Arch's ruling (ADR-080 D4, #2048 comment 6219111038, 2026-10-16): after
``_adopt_canonical_portfolio_category`` gives a QUERY/GUIDANCE
``manage_portfolio`` turn the PORTFOLIO category, ``_handle_portfolio_query``'s
operation sniff must not WRITE on that turn. CXO's copy (2026-10-16 08:47):

- case 1 (a how-to / question): a statement naming the phrase, no action;
- case 2 (an imperative the classifier mislabelled): ``Archive the project
  "Foo"? (yes/no)``, armed on #846 with the rail op's landing; ``yes``
  executes the rail op, ``no`` gets the decline line.

Arch's three pins: (1) QUERY + "how do I archive my project Foo?" with Foo
existing → Foo is not archived; (2) the same with add → nothing created;
(3) QUERY + "list my projects" → the empty-state line, armed (also held by
``test_manage_portfolio_list_from_code_2048.py``).

⚠️ LAYER HONESTY: the classifier is a deterministic stub; these pins prove the
dispatch for each classification, not which one alpha's model draws. The
portfolio writes are stubbed at ``PortfolioService`` / ``_create_or_report_project``.
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
    ADOPTED_FROM_CONTEXT_KEY,
)
from services.intent_service.canonical_handlers import CanonicalHandlers  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.intent_service.destructive_confirm import (  # noqa: E402
    CONFIRM_PENDING_ACTION_WORKFLOW,
    offer_is_confirm,
)
from services.intent_service.workflow_entries import register_default_workflows  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

_USER = "3f7b8a52-2048-4b00-9e00-00000000204b"
FLOOR = "FLOOR-SENTINEL"

# CXO 2026-10-16 08:47, verbatim.
# CXO's final case-1 lines (2026-10-16), verbatim.
ARCHIVE_HOW_TO = (
    "To archive a project, say 'archive project Foo'. "
    "You can restore it any time with 'restore project Foo'."
)
ADD_HOW_TO = "To add a project, say 'add project' and a name."
# CXO 09:1x: a named add question echoes the name.
ADD_HOW_TO_NAMED = "To add a project called Foo, say 'add project Foo'."
RESTORE_HOW_TO = "To restore an archived project, say 'restore project Foo'."
ARCHIVE_CONFIRM = 'Archive the project "Foo"? (yes/no)'
ARCHIVE_DECLINE = 'Okay, I won\'t archive "Foo". Nothing has been changed.'
EMPTY_LINE = "You don't have any active projects yet. Would you like to add a project?"


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
def writes(monkeypatch):
    """Foo exists (active, and archived for restore); every portfolio write
    and the repo link/unlink are recorded instead of run."""
    from services.onboarding.portfolio_service import PortfolioService

    log: list = []
    foo = SimpleNamespace(id="11111111-2048-4b00-9e00-000000000001", name="Foo", is_archived=False)

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


def _service(monkeypatch, *, category, action="manage_portfolio"):
    service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    calls = []

    async def _classify(message, *a, **k):
        calls.append(message)
        return Intent(
            category=category,
            action=action,
            confidence=0.9,
            original_message=message,
            context={"original_message": message},
        )

    monkeypatch.setattr(service.intent_classifier, "classify", _classify)

    # Surface 1 claims several of these phrasings itself today, as
    # PORTFOLIO/manage_portfolio (the classified legacy path, which still
    # writes; Arch's #1595 Phase 3 tail). These pins model the turn surface 1
    # does NOT claim, so the LLM classifier's (category, action) draw decides.
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
    service._classify_calls = calls  # type: ignore[attr-defined]
    return service


def _armed(service, sid):
    return service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)


ADOPTING = [IntentCategory.QUERY, IntentCategory.GUIDANCE]


# ---------------------------------------------------------------------------
# Arch's pins 1 and 2 (case 1: a how-to writes nothing, asks nothing)
# ---------------------------------------------------------------------------


class TestHowToWritesNothing:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ADOPTING, ids=lambda c: c.value)
    async def test_pin1_how_do_i_archive_foo_archives_nothing(
        self, monkeypatch, sm, writes, category
    ):
        service = _service(monkeypatch, category=category)
        sid = f"sess-2048b-arch-{category.value}"
        result = await service.process_intent(
            "how do I archive my project Foo?", session_id=sid, user_id=_USER
        )
        assert writes == [], "an adopted how-to archived the project"
        assert result.message == ARCHIVE_HOW_TO, result.message
        assert result.intent_data["action"] == "adopted_write_how_to"
        assert _armed(service, sid) is None, "a statement must arm nothing"

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message",
        ["how would I add a project called Foo?", "how do I create a new project named Foo?"],
    )
    @pytest.mark.parametrize("category", ADOPTING, ids=lambda c: c.value)
    async def test_pin2_how_would_i_add_creates_nothing(
        self, monkeypatch, sm, writes, category, message
    ):
        service = _service(monkeypatch, category=category)
        sid = f"sess-2048b-add-{category.value}-{len(message)}"
        result = await service.process_intent(message, session_id=sid, user_id=_USER)
        assert writes == [], "an adopted how-to created a project"
        assert result.message == ADD_HOW_TO_NAMED, result.message
        assert _armed(service, sid) is None

    @pytest.mark.asyncio
    async def test_how_do_i_restore_foo_restores_nothing(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-restore"
        result = await service.process_intent(
            "how do I restore project Foo?", session_id=sid, user_id=_USER
        )
        assert writes == []
        assert result.message == RESTORE_HOW_TO, result.message

    @pytest.mark.asyncio
    async def test_a_nameless_imperative_gets_the_phrase_not_a_write(self, monkeypatch, sm, writes):
        """No name to confirm: CXO's add line (it never carries a name)."""
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-noname"
        result = await service.process_intent("add a project", session_id=sid, user_id=_USER)
        assert writes == []
        assert result.message == ADD_HOW_TO
        assert _armed(service, sid) is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message,expected",
        [
            (
                "how do I archive a project?",
                "To archive a project, say 'archive project' and its name.",
            ),
            (
                "how do I archive one of my projects?",
                "To archive a project, say 'archive project' and its name.",
            ),
            (
                "how do I restore an archived project?",
                "To restore an archived project, say 'restore project' and its name.",
            ),
        ],
    )
    async def test_no_name_archive_restore_use_the_generic_form(
        self, monkeypatch, sm, writes, message, expected
    ):
        service = _service(monkeypatch, category=IntentCategory.GUIDANCE)
        sid = f"sess-2048b-generic-{len(message)}"
        result = await service.process_intent(message, session_id=sid, user_id=_USER)
        assert writes == []
        assert result.message == expected, result.message
        assert _armed(service, sid) is None


# ---------------------------------------------------------------------------
# Case 2: a mislabelled imperative asks the armed confirm; yes / no
# ---------------------------------------------------------------------------


class TestImperativeAsksTheArmedConfirm:
    @pytest.mark.asyncio
    async def test_archive_foo_under_query_asks_and_arms(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-confirm"
        result = await service.process_intent("archive project Foo", session_id=sid, user_id=_USER)
        assert writes == [], "the confirm turn wrote"
        assert result.message == ARCHIVE_CONFIRM, result.message
        armed = _armed(service, sid)
        assert armed is not None, "the yes/no question was not armed"
        assert armed["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert armed["question"] == ARCHIVE_CONFIRM
        assert armed["pending_action"]["action"] == "archive_project"
        assert offer_is_confirm(armed), "a yes/no confirm must ride the strict detector"

    @pytest.mark.asyncio
    async def test_yes_executes_the_rail_ops_landing(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, category=IntentCategory.GUIDANCE)
        sid = "sess-2048b-yes"
        await service.process_intent("please archive Foo", session_id=sid, user_id=_USER)
        assert writes == []
        second = await service.process_intent("yes", session_id=sid, user_id=_USER)
        assert writes == [("archive", "11111111-2048-4b00-9e00-000000000001")], second.message
        assert second.message == "Archived 'Foo'.", second.message
        assert service._classify_calls == ["please archive Foo"], "the 'yes' was re-classified"

    @pytest.mark.asyncio
    async def test_no_declines_and_writes_nothing(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-no"
        await service.process_intent("archive project Foo", session_id=sid, user_id=_USER)
        second = await service.process_intent("no", session_id=sid, user_id=_USER)
        assert writes == []
        assert second.message == ARCHIVE_DECLINE, second.message
        assert _armed(service, sid) is None

    @pytest.mark.asyncio
    async def test_add_foo_under_query_confirms_then_yes_creates(self, monkeypatch, sm, writes):
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-add-yes"
        first = await service.process_intent("add project Foo", session_id=sid, user_id=_USER)
        assert writes == []
        # CXO 09:1x: the add confirm uses the add flow's wording.
        assert first.message == 'Add a project called "Foo"? (yes/no)', first.message
        assert _armed(service, sid)["pending_action"]["action"] == "add_project"
        await service.process_intent("yes", session_id=sid, user_id=_USER)
        assert writes == [("create", "Foo")]

    @pytest.mark.asyncio
    async def test_add_foo_no_declines_with_the_add_flow_wording(self, monkeypatch, sm, writes):
        """CXO 09:1x: no -> "Okay, I won't add "Foo". Nothing has been changed."."""
        service = _service(monkeypatch, category=IntentCategory.QUERY)
        sid = "sess-2048b-add-no"
        await service.process_intent("add project Foo", session_id=sid, user_id=_USER)
        second = await service.process_intent("no", session_id=sid, user_id=_USER)
        assert writes == []
        assert second.message == 'Okay, I won\'t add "Foo". Nothing has been changed.'


# ---------------------------------------------------------------------------
# Reads run as before; classified PORTFOLIO is untouched; repos
# ---------------------------------------------------------------------------


class TestReadsAndScope:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("category", ADOPTING, ids=lambda c: c.value)
    async def test_pin3_list_my_projects_still_answers_the_empty_state(
        self, monkeypatch, sm, writes, category
    ):
        from services.onboarding.portfolio_service import PortfolioService

        async def _empty(self, user_id=None, **kwargs):
            return []

        # #2271: the shared fixture now lists Foo as active (archive resolves by
        # exact name on that list); this pin is about the EMPTY state, so it says so.
        monkeypatch.setattr(PortfolioService, "list_active_projects", _empty)
        service = _service(monkeypatch, category=category)
        sid = f"sess-2048b-list-{category.value}"
        result = await service.process_intent("list my projects", session_id=sid, user_id=_USER)
        assert result.message == EMPTY_LINE, result.message
        assert _armed(service, sid) is not None, "the empty state's question was not armed"
        assert writes == []

    @pytest.mark.asyncio
    async def test_classified_portfolio_imperative_archives_via_the_rail(
        self, monkeypatch, sm, writes
    ):
        """#2057: the classified-PORTFOLIO write now goes through the
        archive_project rail op and its consent gate; an explicit imperative
        is the consent, so it still archives (pins:
        test_portfolio_writes_consent_2057.py)."""
        service = _service(monkeypatch, category=IntentCategory.PORTFOLIO)
        sid = "sess-2048b-classified"
        result = await service.process_intent("archive project Foo", session_id=sid, user_id=_USER)
        assert writes == [("archive", "11111111-2048-4b00-9e00-000000000001")]
        assert result.message == "Archived 'Foo'."

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message,expected",
        [
            (
                "link repo acme/widgets to project Foo",
                "To link a repo to a project, say 'link repo acme/widgets to <project name>'.",
            ),
            (
                "unlink repo acme/widgets from project Foo",
                "To unlink a repo from a project, say 'unlink repo acme/widgets from <project name>'.",
            ),
        ],
    )
    async def test_adopted_repo_writes_give_the_phrase(
        self, monkeypatch, sm, writes, message, expected
    ):
        service = _service(monkeypatch, category=IntentCategory.QUERY, action="manage_repos")
        sid = f"sess-2048b-repo-{len(message)}"
        result = await service.process_intent(message, session_id=sid, user_id=_USER)
        assert writes == [], "an adopted repo write executed"
        assert result.message == expected, result.message
        assert _armed(service, sid) is None


class TestTheFlag:
    @pytest.mark.parametrize("category", ADOPTING, ids=lambda c: c.value)
    def test_adoption_stamps_the_classifier_category(self, category):
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
        intent = Intent(category=category, action="manage_portfolio", context={})
        service._adopt_canonical_portfolio_category(intent)
        assert intent.category is IntentCategory.PORTFOLIO
        assert intent.context[ADOPTED_FROM_CONTEXT_KEY] == category.value

    def test_classified_portfolio_is_not_stamped(self):
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
        intent = Intent(category=IntentCategory.PORTFOLIO, action="manage_portfolio", context={})
        service._adopt_canonical_portfolio_category(intent)
        assert ADOPTED_FROM_CONTEXT_KEY not in intent.context
