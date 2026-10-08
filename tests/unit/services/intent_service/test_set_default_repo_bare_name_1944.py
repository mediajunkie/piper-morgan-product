"""1944 — "my default repo should be test-piper-morgan" resolves a bare repo
name against the user's OWN registered repositories.

PM live, alpha v169 (2026-10-05 16:33): the ask named a repo PM had already
registered (mediajunkie/test-piper-morgan) and got the owner/name nudge.
This is a lookup against the user's data, not a new phrase pattern: one
registered match → set it; several → name them and ask; none → the
existing nudge.

Layer: the handler with the session factory and repo registry mocked.
"""

from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1944-4b00-9e00-000000001944"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action="set_default_repo",
        original_message=message,
        confidence=0.95,
        context={"original_message": message, "user_id": _USER},
    )


def _registry(monkeypatch, full_names, current_default=None, account_repos=()):
    """Mock the session scope + RepositoryRepository.list_by_owner, and the
    ConnectorConfigService write; return the write mock."""

    @asynccontextmanager
    async def _scope():
        yield MagicMock()

    monkeypatch.setattr("services.intent.intent_service.AsyncSessionFactory.session_scope", _scope)
    repo_repo = MagicMock()
    repo_repo.list_by_owner = AsyncMock(
        return_value=[SimpleNamespace(full_name=n) for n in full_names]
    )
    monkeypatch.setattr(
        "services.database.repositories.RepositoryRepository", lambda session: repo_repo
    )
    writer = MagicMock()
    writer.set_default_repo = AsyncMock(return_value=None)
    writer.get_default_repo = AsyncMock(return_value=current_default)
    monkeypatch.setattr(
        "services.connectors.config_service.ConnectorConfigService", lambda session: writer
    )
    adapter = MagicMock()
    adapter.search_user_repositories = AsyncMock(
        return_value=SimpleNamespace(repositories=[{"full_name": n} for n in account_repos])
    )
    monkeypatch.setattr(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter", lambda: adapter
    )
    return writer


@pytest.mark.asyncio
async def test_pm_bare_name_resolves_to_the_one_registered_repo(intent_service, monkeypatch):
    writer = _registry(
        monkeypatch, ["mediajunkie/piper-morgan-product", "mediajunkie/test-piper-morgan"]
    )
    result = await intent_service._handle_set_default_repo(
        _intent("my default repo should be test-piper-morgan"), "wf-1"
    )
    assert result.success is True
    writer.set_default_repo.assert_awaited_once_with(_USER, "mediajunkie/test-piper-morgan")
    assert "mediajunkie/test-piper-morgan" in result.message


@pytest.mark.asyncio
async def test_bare_name_matching_several_asks_which(intent_service, monkeypatch):
    writer = _registry(monkeypatch, ["alpha/tools", "beta/tools"])
    result = await intent_service._handle_set_default_repo(
        _intent("set my default repo to tools"), "wf-1"
    )
    writer.set_default_repo.assert_not_awaited()
    assert result.requires_clarification is True
    assert "alpha/tools" in result.message and "beta/tools" in result.message


@pytest.mark.asyncio
async def test_bare_name_with_no_match_keeps_the_nudge(intent_service, monkeypatch):
    writer = _registry(monkeypatch, ["mediajunkie/piper-morgan-product"])
    result = await intent_service._handle_set_default_repo(
        _intent("my default repo should be nonesuch"), "wf-1"
    )
    writer.set_default_repo.assert_not_awaited()
    assert "doesn't look like an `owner/name` repo" in result.message


@pytest.mark.asyncio
async def test_owner_name_form_is_unchanged(intent_service, monkeypatch):
    writer = _registry(monkeypatch, [])
    result = await intent_service._handle_set_default_repo(
        _intent("set my default repo to mediajunkie/piper-morgan-product"), "wf-1"
    )
    writer.set_default_repo.assert_awaited_once_with(_USER, "mediajunkie/piper-morgan-product")
    assert result.success is True


# ── 1944 reopen (PM 2026-10-07): the name the user picked in Settings → GitHub ──


@pytest.mark.asyncio
async def test_bare_name_resolves_against_the_current_default_with_no_registered_repos(
    intent_service, monkeypatch
):
    """PM chose the default in the UI and never linked the repo to a project:
    chat must still know the name."""
    writer = _registry(monkeypatch, [], current_default="mediajunkie/test-piper-morgan")
    result = await intent_service._handle_set_default_repo(
        _intent("my default repo should be test-piper-morgan"), "wf-1"
    )
    writer.set_default_repo.assert_awaited_once_with(_USER, "mediajunkie/test-piper-morgan")
    assert "mediajunkie/test-piper-morgan" in result.message


@pytest.mark.asyncio
async def test_bare_name_resolves_against_the_connected_accounts_repos(intent_service, monkeypatch):
    """The same source the Settings → GitHub dropdown lists."""
    writer = _registry(
        monkeypatch,
        [],
        current_default=None,
        account_repos=["mediajunkie/piper-morgan-product", "mediajunkie/test-piper-morgan"],
    )
    result = await intent_service._handle_set_default_repo(
        _intent("my default repo should be test-piper-morgan"), "wf-1"
    )
    writer.set_default_repo.assert_awaited_once_with(_USER, "mediajunkie/test-piper-morgan")
    assert "mediajunkie/test-piper-morgan" in result.message


@pytest.mark.asyncio
async def test_a_failing_account_lookup_still_answers_with_the_nudge(intent_service, monkeypatch):
    writer = _registry(monkeypatch, [])
    adapter = MagicMock()
    adapter.search_user_repositories = AsyncMock(side_effect=RuntimeError("github down"))
    monkeypatch.setattr(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter", lambda: adapter
    )
    result = await intent_service._handle_set_default_repo(
        _intent("my default repo should be test-piper-morgan"), "wf-1"
    )
    writer.set_default_repo.assert_not_awaited()
    assert "owner/name" in result.message
