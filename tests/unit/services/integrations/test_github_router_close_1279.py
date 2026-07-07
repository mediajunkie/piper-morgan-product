"""#1279 — GitHubIntegrationRouter.close() + the fresh-router-per-request callers.

The router's ``initialize()`` (via the MCP adapter's ``configure_github_api``)
opens an aiohttp ``ClientSession``; nothing ever closed it, so every
fresh-router-per-request caller (the places route, Radar's WorkItem/Place
providers) leaked one session per call. This file covers the new ``close()``
(delegates to the adapter's idempotent ``disconnect()``, never raises) and
proves both Radar providers close the router on success AND on failure —
the leak's regression guard. The places route gets the same try/finally
shape; its route-level behavior is covered by test_places_1192.py.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.github_integration_router import (
    GitHubIntegrationRouter,
)


def _router_with_mock_adapter() -> GitHubIntegrationRouter:
    router = GitHubIntegrationRouter()
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.disconnect = AsyncMock()
    return router


class TestRouterClose:
    async def test_close_delegates_to_adapter_disconnect(self):
        router = _router_with_mock_adapter()
        await router.close()
        router.mcp_adapter.disconnect.assert_awaited_once()

    async def test_close_safe_with_no_adapter(self):
        router = GitHubIntegrationRouter()
        router.mcp_adapter = None
        await router.close()  # must not raise

    async def test_close_never_raises_on_adapter_failure(self):
        router = _router_with_mock_adapter()
        router.mcp_adapter.disconnect = AsyncMock(side_effect=RuntimeError("boom"))
        await router.close()  # swallowed + logged — cleanup must not mask the request

    async def test_close_resets_initialized_so_reuse_reinitializes(self):
        router = _router_with_mock_adapter()
        router._initialized = True
        await router.close()
        assert router._initialized is False

    async def test_close_actually_closes_a_real_session_shape(self):
        """End-to-end through the REAL adapter object (not a mocked disconnect):
        a session-like object wired where configure_github_api puts it must be
        closed and nulled by router.close() — the literal leak, plugged."""
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        router = GitHubIntegrationRouter()
        router.mcp_adapter = GitHubMCPSpatialAdapter()
        fake_session = MagicMock()
        fake_session.close = AsyncMock()
        router.mcp_adapter._session = fake_session

        await router.close()

        fake_session.close.assert_awaited_once()
        assert router.mcp_adapter._session is None


class TestWorkItemProviderClosesRouter:
    """The Radar WorkItem provider constructs a fresh router per call (#1239);
    it must close it whether the fetch succeeds or blows up mid-way."""

    def _mock_router(self, *, configured=True):
        router = MagicMock()
        router.config_service.is_configured.return_value = configured
        router.initialize = AsyncMock()
        router.get_open_issues = AsyncMock(return_value=[])
        router.close = AsyncMock()
        return router

    async def test_closes_router_on_success(self):
        from services.radar.feed_factory import WorkItemProvider

        router = self._mock_router()
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ), patch(
            "services.integrations.github.repo_resolver.read_user_github_handle",
            new=AsyncMock(return_value=None),
        ):
            await WorkItemProvider().list_for_user("u1")
        router.close.assert_awaited_once()

    async def test_closes_router_when_fetch_raises(self):
        from services.radar.feed_factory import WorkItemProvider

        router = self._mock_router()
        router.get_open_issues = AsyncMock(side_effect=RuntimeError("github down"))
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ), patch(
            "services.integrations.github.repo_resolver.read_user_github_handle",
            new=AsyncMock(return_value=None),
        ):
            result = await WorkItemProvider().list_for_user("u1")
        assert result == []  # graceful degradation preserved
        router.close.assert_awaited_once()

    async def test_unconfigured_short_circuit_never_initializes(self):
        """The pre-existing no-session fast path stays intact: unconfigured →
        return [] before initialize (and close isn't required — no session)."""
        from services.radar.feed_factory import WorkItemProvider

        router = self._mock_router(configured=False)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await WorkItemProvider().list_for_user("u1")
        assert result == []
        router.initialize.assert_not_awaited()


class TestPlaceProviderClosesRouter:
    """Radar's Place provider also constructs a fresh candidate router per call —
    it must be closed even when it never graduates to a github source."""

    async def test_closes_candidate_even_when_unconfigured(self):
        from services.radar.feed_factory import PlaceProvider

        router = MagicMock()
        router.initialize = AsyncMock()
        router.config_service.is_configured.return_value = False
        router.close = AsyncMock()

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ), patch(
            "services.place.place_service.PlaceService"
        ) as MockService:
            MockService.return_value.get_visible_places = AsyncMock(return_value=[])
            await PlaceProvider().list_for_user("11111111-1111-1111-1111-111111111111")

        router.close.assert_awaited_once()
