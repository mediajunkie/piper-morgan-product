"""#2205 part 2: a GitHub write goes only to a repository the USER designated.

Arch (2026-10-29 13:48): "a write goes only to a target the user designated, either named
in that turn or a default the user set or confirmed. A code-picked repository may serve a
read, never a write." A3 on alpha b9a8a43600 created in mediajunkie/7cups-testbot, the
oldest repo #1590's read-time recovery had stored with the same call a user's choice uses.

The default now carries its source (``default_repository_source`` in the same
``connector_configs`` JSON blob: no schema change): ``user`` (Settings, chat, the answer to
the write ask, the setup wizard) or ``auto`` (#1314 / #1590). A write with no repository in
the turn and no ``user`` default asks CXO's line (13:54, final): "Which repository should I
create this in? Say owner/name, and I'll keep it as your default." The answer is stored with
source ``user`` and the held write runs there. A legacy default with no source is not
``user``: each existing user is asked once.

LAYER: the real ``ConnectorConfigService`` + resolver against in-memory SQLite (the
``connector_configs`` table only); the create/close handlers by direct call with the
router patched at its seam; the answer turn through ``process_intent``.
"""

from __future__ import annotations

import contextlib
import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.config_service import ConnectorConfigService  # noqa: E402
from services.database.models import ConnectorConfig  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.domain.models import Intent  # noqa: E402
from services.integrations.github import repo_resolver as rr  # noqa: E402
from services.intent.intent_service import (  # noqa: E402
    WRITE_TARGET_CREATE_QUESTION,
    WRITE_TARGET_ISSUE_QUESTION,
    WRITE_TARGET_NO_SESSION_LINE,
    IntentService,
)
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

_ALPHA = "11111111-1111-1111-1111-111111111111"
TITLE = "Add search to the main navigation bar"
AUTO = "mediajunkie/7cups-testbot"
CHOSEN = "mediajunkie/piper-test"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

ASK = "Which repository should I create this in? Say owner/name, and I'll keep it as your default."


@pytest_asyncio.fixture
async def store(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorConfig.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _set(maker, value, source=None):
    async with maker() as s:
        svc = ConnectorConfigService(s)
        if source is None:  # a legacy default: written before the source key existed
            await svc.set_config(_ALPHA, "github", {"default_repository": value})
        else:
            await svc.set_default_repo(_ALPHA, value, source=source)
        await s.commit()


async def _read(maker):
    async with maker() as s:
        return await ConnectorConfigService(s).get_config(_ALPHA, "github")


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _create_intent(message=f"Create an issue: '{TITLE}'", **extra):
    ctx = {"original_message": message, "user_id": _ALPHA, "title": TITLE, **extra}
    return Intent(
        category=IntentCategory.EXECUTION,
        action="create_issue",
        original_message=message,
        confidence=1.0,
        context=ctx,
    )


def _create_patches(create):
    return [
        patch(
            "services.intent_service.collaboration_gate.gate_holds",
            new=AsyncMock(return_value=False),
        ),
        patch(
            "services.configuration.piper_config_loader.piper_config_loader.load_github_config",
            return_value=MagicMock(default_labels=[]),
        ),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.find_open_issue_by_title", new=AsyncMock(return_value=None)),
        patch(f"{ROUTER}.create_issue", new=create),
    ]


def _landed(repo):
    return {"number": 4, "title": TITLE, "html_url": f"https://github.com/{repo}/issues/4"}


@pytest.mark.asyncio
class TestTheSourceIsStored:
    async def test_auto_pick_is_stored_as_auto(self, store):
        repos = [
            {"full_name": AUTO, "created_at": "2017-01-01T00:00:00Z", "archived": False},
            {"full_name": CHOSEN, "created_at": "2026-01-01T00:00:00Z", "archived": False},
        ]
        await rr.apply_default_default_if_unset(_ALPHA, repos)
        cfg = await _read(store)
        assert cfg["default_repository"] == AUTO
        assert cfg["default_repository_source"] == "auto"

    async def test_a_chat_or_settings_set_is_user(self, store):
        await _set(store, CHOSEN, source="user")
        assert (await _read(store))["default_repository_source"] == "user"

    async def test_clearing_the_default_clears_its_source(self, store):
        await _set(store, CHOSEN, source="user")
        async with store() as s:
            await ConnectorConfigService(s).set_default_repo(_ALPHA, None, source="user")
            await s.commit()
        cfg = await _read(store)
        assert "default_repository" not in cfg and "default_repository_source" not in cfg

    @pytest.mark.parametrize(
        "value,source,expected",
        [
            (CHOSEN, "user", CHOSEN),
            (AUTO, "auto", None),
            (AUTO, None, None),  # legacy, no source: not user for writes (asked once)
        ],
    )
    async def test_write_target_is_only_a_user_default(self, store, value, source, expected):
        await _set(store, value, source=source)
        assert await rr.get_user_write_target(_ALPHA) == expected

    async def test_no_default_no_write_target(self, store):
        assert await rr.get_user_write_target(_ALPHA) is None

    async def test_reads_still_resolve_an_auto_default(self, store, monkeypatch):
        monkeypatch.delenv(rr.ENV_DEFAULT_REPO, raising=False)
        await _set(store, AUTO, source="auto")
        resolved = await rr.resolve_repo(user_id=UUID(_ALPHA))
        assert resolved.full_name == AUTO and resolved.source == "user_default"


@pytest.mark.asyncio
class TestCreateAsksUnlessTheUserChose:
    async def test_auto_default_asks_and_calls_no_create(self, store, service):
        await _set(store, AUTO, source="auto")
        sid = f"s-2205w-{uuid.uuid4()}"
        create = AsyncMock(return_value=_landed(AUTO))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            out = await service._handle_create_issue(_create_intent(), "wf", sid, user_id=_ALPHA)
        assert out.message == ASK == WRITE_TARGET_CREATE_QUESTION
        create.assert_not_awaited()
        offer = service.workflow_offer_service._pending_offers.get(sid)
        assert offer is not None
        assert offer["question"] == ASK
        assert offer["pending_action"]["persist_default"] is True

    async def test_legacy_default_with_no_source_asks(self, store, service):
        await _set(store, AUTO, source=None)
        create = AsyncMock(return_value=_landed(AUTO))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            out = await service._handle_create_issue(
                _create_intent(), "wf", f"s-2205w-{uuid.uuid4()}", user_id=_ALPHA
            )
        assert out.message == ASK
        create.assert_not_awaited()

    async def test_user_default_creates_there_without_asking(self, store, service):
        await _set(store, CHOSEN, source="user")
        create = AsyncMock(return_value=_landed(CHOSEN))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            out = await service._handle_create_issue(
                _create_intent(), "wf", f"s-2205w-{uuid.uuid4()}", user_id=_ALPHA
            )
        assert out.message == f'Created issue #4, "{TITLE}", in {CHOSEN}.'
        assert create.await_args.kwargs["owner"] == "mediajunkie"
        assert create.await_args.kwargs["repo_name"] == "piper-test"

    async def test_a_repo_named_in_the_turn_needs_no_ask(self, store, service):
        await _set(store, AUTO, source="auto")
        create = AsyncMock(return_value=_landed(CHOSEN))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            out = await service._handle_create_issue(
                _create_intent(repository=CHOSEN), "wf", f"s-{uuid.uuid4()}", user_id=_ALPHA
            )
        assert out.message.startswith("Created issue #4")
        assert (await _read(store))["default_repository"] == AUTO  # a one-off keeps nothing

    async def test_the_answer_is_kept_as_the_user_default_and_the_create_runs_there(
        self, store, service
    ):
        await _set(store, AUTO, source="auto")
        sid = f"s-2205w-{uuid.uuid4()}"
        create = AsyncMock(return_value=_landed(CHOSEN))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            asked = await service._handle_create_issue(_create_intent(), "wf", sid, user_id=_ALPHA)
            assert asked.message == ASK
            answered = await service.process_intent(message=CHOSEN, session_id=sid, user_id=_ALPHA)
        assert create.await_count == 1
        assert create.await_args.kwargs["owner"] == "mediajunkie"
        assert create.await_args.kwargs["repo_name"] == "piper-test"
        assert f"in {CHOSEN}" in answered.message
        cfg = await _read(store)
        assert cfg["default_repository"] == CHOSEN
        assert cfg["default_repository_source"] == "user"
        assert await rr.get_user_write_target(_ALPHA) == CHOSEN  # asked once

    async def test_no_session_says_what_is_needed_without_a_question(self, store, service):
        await _set(store, AUTO, source="auto")
        create = AsyncMock()
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            out = await service._handle_create_issue(_create_intent(), "wf", None, user_id=_ALPHA)
        assert out.message == WRITE_TARGET_NO_SESSION_LINE
        assert "?" not in out.message
        create.assert_not_awaited()


@pytest.mark.asyncio
class TestIssueWritesAskToo:
    async def test_close_with_an_auto_default_asks_and_does_not_close(self, store, service):
        await _set(store, AUTO, source="auto")
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="close_issue",
            original_message="yes, close #7",
            confidence=1.0,
            context={"original_message": "yes, close #7", "user_id": _ALPHA},
        )
        update = AsyncMock()
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=update),
        ):
            out = await service._handle_close_issue_query(intent, "wf", f"s-2205w-{uuid.uuid4()}")
        assert out.message == WRITE_TARGET_ISSUE_QUESTION.format(number=7)
        assert out.message == (
            "Which repository is #7 in? Say owner/name, and I'll keep it as your default."
        )
        update.assert_not_awaited()


@pytest.mark.asyncio
class TestSourceIsRequired:
    """#2205 condition 2 (Arch 14:39): a permission-bearing value fails closed."""

    async def test_forgetting_the_source_fails_at_call_time(self, store):
        async with store() as s:
            with pytest.raises(TypeError):
                await ConnectorConfigService(s).set_default_repo(_ALPHA, CHOSEN)  # type: ignore[call-arg]
        assert await _read(store) == {}

    async def test_an_unknown_source_is_refused(self, store):
        async with store() as s:
            with pytest.raises(ValueError):
                await ConnectorConfigService(s).set_default_repo(_ALPHA, CHOSEN, source="wizard")
        assert await _read(store) == {}


@pytest.mark.asyncio
class TestTheWriteAskOffersNoDefaultToBind:
    """#2205 condition 3 (Arch 14:39): the carrier binds ``payload["default_repo"]`` on a
    bare "yes" or "…default…"; with ``persist_default`` that would store the auto pick as
    ``user`` and write there (A3 through a "yes"). The write ask never carries one."""

    async def test_the_armed_offer_has_no_default_repo(self, store, service):
        await _set(store, AUTO, source="auto")
        sid = f"s-2205c3-{uuid.uuid4()}"
        with contextlib.ExitStack() as st:
            for p in _create_patches(AsyncMock()):
                st.enter_context(p)
            await service._handle_create_issue(_create_intent(), "wf", sid, user_id=_ALPHA)
        payload = service.workflow_offer_service._pending_offers[sid]["pending_action"]
        assert payload["persist_default"] is True
        assert payload["default_repo"] is None
        assert payload["asked_name"] is None

    async def test_yes_to_the_write_ask_writes_nothing_and_asks_again(self, store, service):
        await _set(store, AUTO, source="auto")
        sid = f"s-2205c3-{uuid.uuid4()}"
        create = AsyncMock(return_value=_landed(AUTO))
        with contextlib.ExitStack() as st:
            for p in _create_patches(create):
                st.enter_context(p)
            await service._handle_create_issue(_create_intent(), "wf", sid, user_id=_ALPHA)
            again = await service.process_intent(message="yes", session_id=sid, user_id=_ALPHA)
        create.assert_not_awaited()
        assert again.message == ASK  # the carrier's bare-yes re-dispatch re-asks
        assert service.workflow_offer_service._pending_offers.get(sid) is not None  # re-armed
        cfg = await _read(store)
        assert (cfg["default_repository"], cfg["default_repository_source"]) == (AUTO, "auto")


# ── CXO 15:25 (1): a Settings re-save of an UNCHANGED auto default stays auto ──────────


async def _save_settings(store, monkeypatch, default, selected=None):
    from types import SimpleNamespace

    from web.api.routes.settings_integrations import (
        GitHubPreferencesRequest,
        save_github_preferences,
    )

    @contextlib.asynccontextmanager
    async def _fresh():
        async with store() as s:
            yield s

    monkeypatch.setattr(AsyncSessionFactory, "session_scope_fresh", staticmethod(_fresh))
    await save_github_preferences(
        GitHubPreferencesRequest(
            selected_repositories=selected or [AUTO, CHOSEN], default_repository=default
        ),
        SimpleNamespace(sub=_ALPHA),
    )


async def _create_turn(service, create):
    with contextlib.ExitStack() as st:
        for p in _create_patches(create):
            st.enter_context(p)
        return await service._handle_create_issue(
            _create_intent(), "wf", f"s-2205s-{uuid.uuid4()}", user_id=_ALPHA
        )


@pytest.mark.asyncio
class TestSettingsResave:
    async def test_unchanged_auto_default_stays_auto_and_a_create_still_asks(
        self, store, service, monkeypatch
    ):
        await _set(store, AUTO, source="auto")
        await _save_settings(store, monkeypatch, AUTO, selected=[AUTO])  # changed other prefs
        cfg = await _read(store)
        assert (cfg["default_repository"], cfg["default_repository_source"]) == (AUTO, "auto")
        assert cfg["selected_repositories"] == [AUTO]
        create = AsyncMock(return_value=_landed(AUTO))
        out = await _create_turn(service, create)
        assert out.message == ASK
        create.assert_not_awaited()

    async def test_a_changed_value_is_the_users_choice_and_a_create_goes_there(
        self, store, service, monkeypatch
    ):
        await _set(store, AUTO, source="auto")
        await _save_settings(store, monkeypatch, CHOSEN)
        cfg = await _read(store)
        assert (cfg["default_repository"], cfg["default_repository_source"]) == (CHOSEN, "user")
        create = AsyncMock(return_value=_landed(CHOSEN))
        out = await _create_turn(service, create)
        assert out.message == f'Created issue #4, "{TITLE}", in {CHOSEN}.'

    async def test_a_legacy_unchanged_default_stays_non_user(self, store, monkeypatch):
        await _set(store, AUTO, source=None)
        await _save_settings(store, monkeypatch, AUTO)
        assert (await _read(store)).get("default_repository_source") is None
        assert await rr.get_user_write_target(_ALPHA) is None

    async def test_a_first_default_saved_is_the_users_choice(self, store, monkeypatch):
        await _save_settings(store, monkeypatch, CHOSEN)
        assert await rr.get_user_write_target(_ALPHA) == CHOSEN

    async def test_an_unchanged_user_default_stays_user(self, store, monkeypatch):
        await _set(store, CHOSEN, source="user")
        await _save_settings(store, monkeypatch, CHOSEN)
        assert (await _read(store))["default_repository_source"] == "user"


# ── CXO 15:25 (3): close/reopen ask the repository FIRST, then the confirm names it ─────


def _stub_classify(service, action):
    async def _classify(message, *args, **kwargs):
        if message.lower().startswith(("close issue", "reopen issue")):
            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                original_message=message,
                context={"original_message": message},
            )
        raise AssertionError(f"LLM boundary touched (classify {message!r})")

    service.intent_classifier.classify = _classify


def _github_close_patches(update):
    found = ("found", {"number": 7, "title": "Fix login", "state": "open"}, None)
    reopenable = ("found", {"number": 7, "title": "Fix login", "state": "closed"}, None)
    return (
        found,
        reopenable,
        [
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.get_issue", new=AsyncMock(side_effect=AssertionError("no preview"))),
            patch(f"{ROUTER}.update_issue", new=update),
        ],
    )


PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"


@pytest.mark.asyncio
class TestCloseAsksTheRepositoryFirst:
    async def test_auto_default_repo_first_then_confirm_names_it_then_yes_closes_there(
        self, store, service
    ):
        await _set(store, AUTO, source="auto")
        _stub_classify(service, "close_issue_query")
        sid = f"s-2205close-{uuid.uuid4()}"
        update = AsyncMock(
            return_value={"number": 7, "title": "Fix login", "state": "closed", "html_url": ""}
        )
        found, _, patches = _github_close_patches(update)
        with contextlib.ExitStack() as st:
            for p in patches:
                st.enter_context(p)
            st.enter_context(patch(PROBE, new=AsyncMock(return_value=found)))
            first = await service.process_intent(
                message="close issue #7", session_id=sid, user_id=_ALPHA
            )
            assert first.message == (
                "Which repository is #7 in? Say owner/name, and I'll keep it as your default."
            )
            update.assert_not_awaited()

            confirm = await service.process_intent(message=CHOSEN, session_id=sid, user_id=_ALPHA)
            assert CHOSEN in confirm.message
            assert confirm.message == f"Close issue #7 'Fix login' in {CHOSEN}? (yes/no)"
            update.assert_not_awaited()  # no write before both answers
            cfg = await _read(store)
            assert (cfg["default_repository"], cfg["default_repository_source"]) == (
                CHOSEN,
                "user",
            )

            closed = await service.process_intent(message="yes", session_id=sid, user_id=_ALPHA)
        update.assert_awaited_once_with(
            7, state="closed", owner="mediajunkie", repo_name="piper-test"
        )
        assert "Closed issue #7" in closed.message

    async def test_user_default_skips_the_repo_ask_and_the_confirm_still_names_it(
        self, store, service
    ):
        await _set(store, CHOSEN, source="user")
        _stub_classify(service, "close_issue_query")
        sid = f"s-2205close-{uuid.uuid4()}"
        update = AsyncMock(
            return_value={"number": 7, "title": "Fix login", "state": "closed", "html_url": ""}
        )
        found, _, patches = _github_close_patches(update)
        with contextlib.ExitStack() as st:
            for p in patches:
                st.enter_context(p)
            st.enter_context(patch(PROBE, new=AsyncMock(return_value=found)))
            confirm = await service.process_intent(
                message="close issue #7", session_id=sid, user_id=_ALPHA
            )
            assert confirm.message == f"Close issue #7 'Fix login' in {CHOSEN}? (yes/no)"
            update.assert_not_awaited()
            closed = await service.process_intent(message="yes", session_id=sid, user_id=_ALPHA)
        update.assert_awaited_once_with(7, state="closed")  # the router resolves the user default
        assert "Closed issue #7" in closed.message

    async def test_reopen_has_the_same_order(self, store, service):
        await _set(store, AUTO, source="auto")
        _stub_classify(service, "reopen_issue_query")
        sid = f"s-2205reopen-{uuid.uuid4()}"
        update = AsyncMock(
            return_value={"number": 7, "title": "Fix login", "state": "open", "html_url": ""}
        )
        _, reopenable, patches = _github_close_patches(update)
        with contextlib.ExitStack() as st:
            for p in patches:
                st.enter_context(p)
            st.enter_context(patch(PROBE, new=AsyncMock(return_value=reopenable)))
            first = await service.process_intent(
                message="reopen issue #7", session_id=sid, user_id=_ALPHA
            )
            assert first.message.startswith("Which repository is #7 in?")
            confirm = await service.process_intent(message=CHOSEN, session_id=sid, user_id=_ALPHA)
            assert confirm.message == f"Reopen issue #7 'Fix login' in {CHOSEN}? (yes/no)"
            update.assert_not_awaited()
            reopened = await service.process_intent(message="yes", session_id=sid, user_id=_ALPHA)
        update.assert_awaited_once_with(
            7, state="open", owner="mediajunkie", repo_name="piper-test"
        )
        assert "Reopened issue #7" in reopened.message
