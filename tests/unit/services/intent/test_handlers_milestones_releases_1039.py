"""Handler tests for _handle_list_milestones_query + _handle_list_releases_query (Issue #1039)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory


def _make_intent() -> Intent:
    """Build a minimal Intent for handler tests."""
    return Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        confidence=1.0,
        original_message="show milestones",
    )


def _make_release_intent() -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action="list_releases_query",
        confidence=1.0,
        original_message="recent releases",
    )


@pytest.fixture
def intent_service():
    """Lightweight service instance with mocked deps."""
    from services.intent.intent_service import IntentService

    service = IntentService.__new__(IntentService)
    service.logger = MagicMock()
    return service


@pytest.fixture(autouse=True)
def _releases_connector_not_connected():
    """#1327 cutover: the releases handler now prefers the OAuth connector. These #1039 tests
    exercise the NATIVE-PAT render path, so force the connector to report CONNECT_REQUIRED →
    the handler falls back to native, unchanged. (Milestones have NO connector tool → that
    handler is untouched by #1327 and needs no patch.)"""
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubRepoScopedResult

    cr = GitHubRepoScopedResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED,
            user_message="Connect GitHub to continue.",
            action_hint="/api/v1/settings/integrations/github/connect",
        )
    )
    with patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_releases_connector",
        new=AsyncMock(return_value=cr),
    ):
        yield


class TestListMilestonesHandler:
    """_handle_list_milestones_query — Issue #1039."""

    async def test_populated_milestones_response(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_milestones_via_mcp = AsyncMock(
                return_value=[
                    {
                        "title": "v1.0",
                        "number": 1,
                        "state": "open",
                        "due_on": "2026-06-01T00:00:00Z",
                        "open_issues": 3,
                        "closed_issues": 7,
                    },
                    {
                        "title": "v0.9",
                        "number": 2,
                        "state": "open",
                        "due_on": None,
                        "open_issues": 1,
                        "closed_issues": 0,
                    },
                ]
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_list_milestones_query(
                _make_intent(), workflow_id="wf-1"
            )

        assert result.success is True
        assert "2 open milestones" in result.message
        assert "v1.0" in result.message
        assert "2026-06-01" in result.message  # ISO time stripped
        assert "no due date" in result.message  # for v0.9
        assert result.intent_data["context"]["milestone_count"] == 2

    async def test_single_milestone_singular_grammar(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_milestones_via_mcp = AsyncMock(
                return_value=[
                    {
                        "title": "Solo",
                        "number": 1,
                        "state": "open",
                        "due_on": None,
                        "open_issues": 1,
                        "closed_issues": 0,
                    }
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_milestones_query(
                _make_intent(), workflow_id="wf-1"
            )
        assert "1 open milestone**" in result.message  # singular (with markdown bold)
        assert "1 open issue)" in result.message  # singular issue too

    async def test_empty_milestones_returns_friendly_message(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_milestones_via_mcp = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_milestones_query(
                _make_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "don't have any open milestones" in result.message
        assert result.intent_data["context"]["milestone_count"] == 0

    async def test_top_5_truncation(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_milestones_via_mcp = AsyncMock(
                return_value=[
                    {
                        "title": f"M{i}",
                        "number": i,
                        "state": "open",
                        "due_on": f"2026-0{(i % 9) + 1}-01T00:00:00Z",
                        "open_issues": i,
                        "closed_issues": 0,
                    }
                    for i in range(1, 8)
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_milestones_query(
                _make_intent(), workflow_id="wf-1"
            )
        assert "and 2 more" in result.message
        assert result.intent_data["context"]["milestone_count"] == 7

    async def test_exception_returns_graceful_message(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            MockRouter.side_effect = RuntimeError("router boom")
            result = await intent_service._handle_list_milestones_query(
                _make_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "wasn't able to fetch" in result.message
        assert "error" in result.intent_data["context"]


class TestListReleasesHandler:
    """_handle_list_releases_query — Issue #1039."""

    async def test_populated_releases_with_stable_headline(self, intent_service):
        """Q5 disposition: latest non-prerelease surfaced as 'Current version'."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_releases_via_mcp = AsyncMock(
                return_value=[
                    {
                        "tag_name": "v1.1.0-beta",
                        "name": "v1.1.0 Beta",
                        "published_at": "2026-05-04T08:00:00Z",
                        "prerelease": True,
                        "draft": False,
                    },
                    {
                        "tag_name": "v1.0.0",
                        "name": "v1.0.0 Stable",
                        "published_at": "2026-05-01T12:00:00Z",
                        "prerelease": False,
                        "draft": False,
                    },
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_releases_query(
                _make_release_intent(), workflow_id="wf-1"
            )
        assert "Current version" in result.message
        assert "v1.0.0" in result.message  # stable headline
        assert "(pre-release)" in result.message  # flag inline for the beta
        assert result.intent_data["context"]["release_count"] == 2
        assert result.intent_data["context"]["latest_version"] == "v1.0.0"

    async def test_all_prereleases_no_stable_headline(self, intent_service):
        """All-prerelease repos get count headline, not 'Current version'."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_releases_via_mcp = AsyncMock(
                return_value=[
                    {
                        "tag_name": "v0.1.0-alpha",
                        "name": "Alpha",
                        "published_at": "2026-05-04T08:00:00Z",
                        "prerelease": True,
                        "draft": False,
                    },
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_releases_query(
                _make_release_intent(), workflow_id="wf-1"
            )
        assert "Current version" not in result.message
        assert "all pre-releases" in result.message
        assert result.intent_data["context"]["latest_version"] is None

    async def test_empty_releases_friendly_message(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_releases_via_mcp = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_releases_query(
                _make_release_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "don't have any releases yet" in result.message
        assert result.intent_data["context"]["release_count"] == 0

    async def test_recent_releases_top_5(self, intent_service):
        """Top 5 sorted by published_at desc; truncation message for >5."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_releases_via_mcp = AsyncMock(
                return_value=[
                    {
                        "tag_name": f"v{i}.0",
                        "name": f"v{i}.0",
                        "published_at": f"2026-0{(i % 9) + 1}-01T00:00:00Z",
                        "prerelease": False,
                        "draft": False,
                    }
                    for i in range(1, 8)
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_releases_query(
                _make_release_intent(), workflow_id="wf-1"
            )
        assert "and 2 more" in result.message
        assert result.intent_data["context"]["release_count"] == 7

    async def test_exception_graceful_path(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            MockRouter.side_effect = RuntimeError("router boom")
            result = await intent_service._handle_list_releases_query(
                _make_release_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "wasn't able to fetch" in result.message
        assert "error" in result.intent_data["context"]
