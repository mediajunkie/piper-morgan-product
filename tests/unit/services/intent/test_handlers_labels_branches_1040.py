"""Handler tests for _handle_list_labels_query + _handle_list_branches_query (Issue #1040)."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory


def _make_label_intent() -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action="list_labels_query",
        confidence=1.0,
        original_message="what labels do we use",
    )


def _make_branch_intent() -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action="list_branches_query",
        confidence=1.0,
        original_message="active branches",
    )


@pytest.fixture
def intent_service():
    from services.intent.intent_service import IntentService

    service = IntentService.__new__(IntentService)
    service.logger = MagicMock()
    return service


@pytest.fixture(autouse=True)
def _connector_not_connected():
    """#1327 cutover: branches/labels handlers now prefer the OAuth connector. These #1040
    tests exercise the NATIVE-PAT render path, so force the connector to report
    CONNECT_REQUIRED (not OAuth-connected) → the handler falls back to native, unchanged."""
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
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_labels_connector",
        new=AsyncMock(return_value=cr),
    ), patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_branches_connector",
        new=AsyncMock(return_value=cr),
    ):
        yield


class TestListLabelsHandler:
    """_handle_list_labels_query — Issue #1040."""

    async def test_populated_labels_response(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_labels_via_mcp = AsyncMock(
                return_value=[
                    {"name": "bug", "color": "d73a4a", "description": "Something is broken"},
                    {"name": "enhancement", "color": "a2eeef", "description": ""},
                ]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_labels_query(
                _make_label_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "2 labels" in result.message
        assert "**bug**" in result.message
        assert "Something is broken" in result.message
        assert "**enhancement**" in result.message
        assert result.intent_data["context"]["label_count"] == 2

    async def test_single_label_singular_grammar(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_labels_via_mcp = AsyncMock(
                return_value=[{"name": "bug", "color": "d73a4a", "description": ""}]
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_labels_query(
                _make_label_intent(), workflow_id="wf-1"
            )
        assert "1 label**" in result.message  # singular, with markdown bold close

    async def test_empty_labels_returns_friendly(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_labels_via_mcp = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_labels_query(
                _make_label_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "don't see any labels" in result.message

    async def test_truncates_at_20(self, intent_service):
        many = [{"name": f"label-{i:02d}", "color": "ffffff", "description": ""} for i in range(25)]
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_labels_via_mcp = AsyncMock(return_value=many)
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_labels_query(
                _make_label_intent(), workflow_id="wf-1"
            )
        assert "and 5 more" in result.message
        assert result.intent_data["context"]["label_count"] == 25

    async def test_exception_graceful_path(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            MockRouter.side_effect = RuntimeError("boom")
            result = await intent_service._handle_list_labels_query(
                _make_label_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "wasn't able to fetch" in result.message
        assert "error" in result.intent_data["context"]


class TestListBranchesHandler:
    """_handle_list_branches_query — Issue #1040."""

    async def test_default_branch_first(self, intent_service):
        """Q5 disposition: default-first sort + 'all non-default' baseline."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_branches_via_mcp = AsyncMock(
                return_value={
                    "branches": [
                        {"name": "claude/feature-x", "protected": False, "commit_sha": "a"},
                        {"name": "main", "protected": True, "commit_sha": "b"},
                        {"name": "claude/feature-y", "protected": False, "commit_sha": "c"},
                    ],
                    "default_branch": "main",
                }
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert "default: `main`" in result.message
        # Verify default appears before claude/* branches in output
        msg = result.message
        assert msg.find("**main**") < msg.find("**claude/feature-x**")
        assert "(default, protected)" in msg or "(default)" in msg
        assert result.intent_data["context"]["default_branch"] == "main"
        assert result.intent_data["context"]["branch_count"] == 3

    async def test_no_default_branch_resolved(self, intent_service):
        """Empty default_branch (e.g., resolver returned empty) handles gracefully."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_branches_via_mcp = AsyncMock(
                return_value={
                    "branches": [{"name": "main", "protected": True, "commit_sha": "a"}],
                    "default_branch": "",
                }
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert "default:" not in result.message  # no default-branch parenthetical
        assert "**main**" in result.message
        assert result.intent_data["context"]["default_branch"] is None

    async def test_empty_branches_friendly(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_branches_via_mcp = AsyncMock(
                return_value={"branches": [], "default_branch": ""}
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert "don't see any branches" in result.message
        assert result.intent_data["context"]["branch_count"] == 0

    async def test_truncates_at_20(self, intent_service):
        many = [
            {"name": f"feature-{i:02d}", "protected": False, "commit_sha": ""} for i in range(25)
        ]
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_branches_via_mcp = AsyncMock(
                return_value={"branches": many, "default_branch": ""}
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert "and 5 more" in result.message
        assert result.intent_data["context"]["branch_count"] == 25

    async def test_protected_flag_displayed(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = AsyncMock()
            mock_router.list_branches_via_mcp = AsyncMock(
                return_value={
                    "branches": [{"name": "release/v1", "protected": True, "commit_sha": "a"}],
                    "default_branch": "main",
                }
            )
            MockRouter.return_value = mock_router
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert "(protected)" in result.message

    async def test_exception_graceful_path(self, intent_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            MockRouter.side_effect = RuntimeError("boom")
            result = await intent_service._handle_list_branches_query(
                _make_branch_intent(), workflow_id="wf-1"
            )
        assert result.success is True
        assert "wasn't able to fetch" in result.message
        assert "error" in result.intent_data["context"]
