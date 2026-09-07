"""#1723 — GitHubMCPSpatialAdapter.list_repositories + the async-ified chain above it.

Layer named (m-43): the adapter tests mock ``_call_github_api`` (the REST
transport helper — the #1039/#1040 sibling idiom); signature, endpoint,
normalization, and failure shape are real. The chain tests drive the REAL
``GitHubDomainService`` and REAL router methods with the layer below each
mocked, pinning that the four-hop chain (adapter → router → domain service →
caller) is awaitable end-to-end — the operation went async with this
implementation (the sync Protocol signature was a PyGithub-era fossil an
aiohttp adapter cannot honor without blocking the loop).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter


@pytest.fixture
def adapter() -> GitHubMCPSpatialAdapter:
    a = GitHubMCPSpatialAdapter()
    a._call_github_api = AsyncMock(return_value=[])
    return a


class TestAdapterListRepositories:
    async def test_endpoint_is_the_authenticated_users_repos(self, adapter):
        await adapter.list_repositories()
        adapter._call_github_api.assert_awaited_once_with(
            "user/repos", {"per_page": 100, "sort": "updated"}
        )

    async def test_returns_normalized_repo_dicts(self, adapter):
        adapter._call_github_api.return_value = [
            {
                "id": 42,
                "name": "hello-world",
                "full_name": "octocat/hello-world",
                "description": "My first repo",
                "html_url": "https://github.com/octocat/hello-world",
                "private": False,
                "archived": False,
                "updated_at": "2026-09-01T00:00:00Z",
                "watchers": 9000,  # extraneous REST fields are dropped
            },
            {
                "id": 43,
                "name": "spoon-knife",
                "full_name": "octocat/spoon-knife",
                "description": None,  # None → "" (the caller string-matches)
                "html_url": "https://github.com/octocat/spoon-knife",
                "private": True,
                "archived": True,
                "updated_at": None,
            },
        ]
        repos = await adapter.list_repositories()
        assert len(repos) == 2
        # The live caller's navigation (_get_project_metadata): name + full_name
        assert repos[0]["name"] == "hello-world"
        assert repos[0]["full_name"] == "octocat/hello-world"
        assert repos[1]["description"] == ""
        assert repos[1]["private"] is True and repos[1]["archived"] is True
        assert "watchers" not in repos[0]

    async def test_empty_response_returns_empty_list(self, adapter):
        adapter._call_github_api.return_value = None
        assert await adapter.list_repositories() == []

    async def test_exception_returns_empty_list(self, adapter):
        adapter._call_github_api.side_effect = RuntimeError("api boom")
        assert await adapter.list_repositories() == []


class TestChainIsAwaitableEndToEnd:
    """The async-ification pin: every hop awaits the one below it."""

    async def test_domain_service_awaits_the_router(self):
        from services.domain.github_domain_service import GitHubDomainService

        agent = MagicMock()
        agent.list_repositories = AsyncMock(return_value=[{"name": "r", "full_name": "o/r"}])
        service = GitHubDomainService(github_agent=agent)
        repos = await service.list_repositories()
        assert repos == [{"name": "r", "full_name": "o/r"}]
        agent.list_repositories.assert_awaited_once()

    async def test_router_lazy_inits_then_awaits_the_adapter(self):
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        router = GitHubIntegrationRouter()
        router.initialize = AsyncMock()  # lazy-init seam (token load)
        router.mcp_adapter = MagicMock()
        router.mcp_adapter.list_repositories = AsyncMock(return_value=[{"name": "r"}])
        repos = await router.list_repositories()
        assert repos == [{"name": "r"}]
        router.initialize.assert_awaited_once()
        router.mcp_adapter.list_repositories.assert_awaited_once_with()
