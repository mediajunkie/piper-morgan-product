"""#1590 — first-contact produces a demo block once read-time repo recovery lands.

The #1536 demo was silently skipped in production (live Fly logs, v48) because
``resolve_repo`` raised ``UnresolvedRepoError`` for an account whose GitHub
connector was BOUND but whose ``default_repo`` was never set — #1314's auto-default
runs only in the OAuth callback. The demo behaved correctly (CXO item (i): never ask
"which repo?" ahead of data), so the user got the blank generic interface instead.

This is the end-to-end assertion at the first-contact layer (m-43: the gather's
returned context dict, not a curl or a config read): configured connector + zero
default repo + one accessible repo → recovery adopts the repo → the demo block
appears, naming REAL items from the read.
"""

from __future__ import annotations

from typing import Dict, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.integrations.github.repo_resolver import ENV_DEFAULT_REPO, reset_recovery_guard
from services.intent_service.first_contact import gather_first_contact_demo

_STATUS_FC = "services.integrations.integration_status_service.IntegrationStatusService"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
_ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


class _PassthroughCache:
    """#984 seam without a Redis dependency: always compute."""

    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


class _StatefulConfigService:
    def __init__(self, store: Dict[str, str]):
        self._store = store

    async def get_default_repo(self, user_id) -> Optional[str]:
        return self._store.get(str(user_id))

    async def set_default_repo(self, user_id, full_name: str) -> None:
        self._store[str(user_id)] = full_name


class _Ctx:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


@pytest.fixture(autouse=True)
def _clean(monkeypatch):
    monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
    reset_recovery_guard()
    yield
    reset_recovery_guard()


async def test_demo_appears_after_read_time_repo_recovery():
    from services.mcp.consumer.github_adapter import GitHubReposResult

    user_id = str(uuid4())
    store: Dict[str, str] = {}

    status = MagicMock()
    status.is_configured = AsyncMock(return_value=True)

    adapter = MagicMock()
    adapter.search_user_repositories = AsyncMock(
        return_value=GitHubReposResult(
            repositories=[
                {
                    "id": 1,
                    "name": "rocket",
                    "full_name": "acme/rocket",
                    "description": "",
                    "created_at": "2026-01-01T00:00:00Z",
                    "archived": False,
                }
            ]
        )
    )

    router = MagicMock()
    router.initialize = AsyncMock()
    router.close = AsyncMock()
    router.get_open_issues = AsyncMock(
        return_value=[
            {
                "number": 123,
                "title": "Fix the login flow",
                "updated_at": "2026-08-10T00:00:00Z",
                "is_pull_request": False,
                "uri": "https://github.com/acme/rocket/issues/123",
            }
        ]
    )

    with (
        patch(
            "services.connectors.config_service.ConnectorConfigService",
            side_effect=lambda _s: _StatefulConfigService(store),
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            side_effect=lambda *a, **k: _Ctx(),
        ),
        patch(_STATUS_FC, return_value=status),
        patch(_ADAPTER, return_value=adapter),
        patch(_ROUTER, return_value=router),
    ):
        result = await gather_first_contact_demo(user_id, cache=_PassthroughCache())

    demo = result.get("first_contact_demo")
    assert demo, f"expected a first-contact demo block, got {result!r}"
    assert demo["repo"] == "acme/rocket"
    assert demo["items"][0]["title"] == "Fix the login flow"
    # The recovery persisted, so the NEXT read resolves without another search.
    assert store[user_id] == "acme/rocket"
    adapter.search_user_repositories.assert_awaited_once()


async def test_zero_repo_user_still_gets_no_demo_and_no_scope_question():
    """Genuinely-zero-repo account degrades exactly as today (CXO item (i))."""
    from services.mcp.consumer.github_adapter import GitHubReposResult

    user_id = str(uuid4())
    store: Dict[str, str] = {}

    status = MagicMock()
    status.is_configured = AsyncMock(return_value=True)
    adapter = MagicMock()
    adapter.search_user_repositories = AsyncMock(return_value=GitHubReposResult(repositories=[]))

    with (
        patch(
            "services.connectors.config_service.ConnectorConfigService",
            side_effect=lambda _s: _StatefulConfigService(store),
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            side_effect=lambda *a, **k: _Ctx(),
        ),
        patch(_STATUS_FC, return_value=status),
        patch(_ADAPTER, return_value=adapter),
    ):
        result = await gather_first_contact_demo(user_id, cache=_PassthroughCache())

    assert result == {}
    assert store == {}
