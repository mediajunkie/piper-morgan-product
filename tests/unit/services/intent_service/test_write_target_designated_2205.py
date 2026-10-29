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
            await ConnectorConfigService(s).set_default_repo(_ALPHA, None)
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
