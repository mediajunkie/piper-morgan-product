"""#2205 part 3: the repository chosen in the setup wizard is the user's default.

xian, 2026-10-29: he chose a repository in the wizard's Projects step (before GitHub was
connected) and the resolver never used it; #1590 recovery guessed the oldest repo. Arch
(13:58): ``create_setup_project`` linked the repo to the project, a store the resolver has
not read since #1315 retired its project path. Ruling: one store, one resolver: the wizard
WRITES the user's default with source ``user`` unless the user already designated one; no
project-scoped read path is revived. Not backfilled for existing accounts (they get CXO's
ask once on their first write).

LAYER: the real route function with the real ``ConnectorConfigService`` over in-memory
SQLite (the project/repository repositories mocked; they are #860/#866's, unchanged), then
the real create handler reading the same store. DENOMINATOR: no default, an auto default,
a user default; the following create.
"""

from __future__ import annotations

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

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
from services.domain.models import Repository as DomainRepo  # noqa: E402
from services.integrations.github import repo_resolver as rr  # noqa: E402
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

pytestmark = pytest.mark.asyncio

_USER = "33333333-3333-3333-3333-333333333333"
WIZARD = "mediajunkie/piper-test"
AUTO = "mediajunkie/7cups-testbot"
EARLIER = "mediajunkie/chosen-earlier"
TITLE = "Add search to the main navigation bar"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


@pytest_asyncio.fixture
async def maker(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorConfig.__table__.create(c, checkfirst=True))
    mk = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with mk() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield mk
    await engine.dispose()


async def _config(mk):
    async with mk() as s:
        return await ConnectorConfigService(s).get_config(_USER, "github")


async def _set(mk, value, source):
    async with mk() as s:
        await ConnectorConfigService(s).set_default_repo(_USER, value, source=source)
        await s.commit()


async def _run_wizard(mk, github_repo=WIZARD):
    from web.api.routes.setup import SetupProjectRequest, create_setup_project

    @contextlib.asynccontextmanager
    async def _fresh():
        async with mk() as s:
            yield s

    projects = MagicMock()
    projects.create = AsyncMock(return_value=MagicMock(id=str(uuid.uuid4())))
    repos = MagicMock()
    repos.create_repository = AsyncMock(
        return_value=DomainRepo(
            id=str(uuid.uuid4()), owner_id=_USER, provider="github", full_name=github_repo
        )
    )
    repos.link_to_project = AsyncMock()
    not_checked = SimpleNamespace(validated=False, exists=None, error="github not connected")
    with (
        patch("web.api.routes.setup.AsyncSessionFactory.session_scope_fresh", new=_fresh),
        patch("services.database.repositories.ProjectRepository", return_value=projects),
        patch("services.database.repositories.RepositoryRepository", return_value=repos),
        patch(
            "services.infrastructure.github_repo_validator.validate_github_repo_for_account",
            new=AsyncMock(return_value=not_checked),
        ),
        patch("services.infrastructure.github_repo_validator.apply_validation_metadata"),
    ):
        out = await create_setup_project(
            SetupProjectRequest(project_name="Piper", github_repo=github_repo),
            SimpleNamespace(sub=_USER),
        )
    assert out.success is True
    repos.link_to_project.assert_awaited_once()  # the project link is kept (it has readers)


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


class TestWizardWritesTheUserDefault:
    async def test_no_default_the_wizard_repo_becomes_the_user_default(self, maker):
        await _run_wizard(maker)
        cfg = await _config(maker)
        assert cfg["default_repository"] == WIZARD
        assert cfg["default_repository_source"] == "user"
        assert await rr.get_user_write_target(_USER) == WIZARD

    async def test_an_auto_default_is_replaced_by_the_wizard_choice(self, maker):
        await _set(maker, AUTO, "auto")
        await _run_wizard(maker)
        cfg = await _config(maker)
        assert (cfg["default_repository"], cfg["default_repository_source"]) == (WIZARD, "user")

    async def test_a_user_default_is_never_overwritten(self, maker):
        await _set(maker, EARLIER, "user")
        await _run_wizard(maker)
        cfg = await _config(maker)
        assert (cfg["default_repository"], cfg["default_repository_source"]) == (
            EARLIER,
            "user",
        )

    async def test_then_a_create_with_no_repo_goes_there_without_asking(self, maker, service):
        await _run_wizard(maker)
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_issue",
            original_message=f"Create an issue: '{TITLE}'",
            confidence=1.0,
            context={
                "original_message": f"Create an issue: '{TITLE}'",
                "user_id": _USER,
                "title": TITLE,
            },
        )
        landed = {"number": 1, "title": TITLE, "html_url": f"https://github.com/{WIZARD}/issues/1"}
        create = AsyncMock(return_value=landed)
        with (
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
        ):
            out = await service._handle_create_issue(
                intent, "wf", f"s-2205-wiz-{uuid.uuid4()}", user_id=_USER
            )
        assert out.message == f'Created issue #1, "{TITLE}", in {WIZARD}.'
        assert (create.await_args.kwargs["owner"], create.await_args.kwargs["repo_name"]) == (
            "mediajunkie",
            "piper-test",
        )


class TestTheA1RepoSentenceLosesItsFact:
    """CXO 14:04 (A1): "no GitHub repo is linked to your account yet" came from the floor's
    ``github_repo_unconfigured`` directive, armed by ``ContextAssembler.
    _compute_high_priority_issues`` when ``_github_repo_resolves`` is False. After the
    wizard writes the default, the repo resolves (path 2) even before GitHub is connected,
    so that directive is not armed; the separate ``github_connected`` fact still says
    GitHub is not connected."""

    async def test_the_wizard_repo_resolves_before_github_is_connected(self, maker, monkeypatch):
        from uuid import UUID

        from services.intent_service.context_assembler import ContextAssembler

        monkeypatch.delenv(rr.ENV_DEFAULT_REPO, raising=False)
        rr.reset_recovery_guard()
        assembler = ContextAssembler.__new__(ContextAssembler)
        assert await assembler._github_repo_resolves(_USER) is False
        await _run_wizard(maker)
        assert await assembler._github_repo_resolves(_USER) is True
        resolved = await rr.resolve_repo(user_id=UUID(_USER))
        assert resolved.full_name == WIZARD
