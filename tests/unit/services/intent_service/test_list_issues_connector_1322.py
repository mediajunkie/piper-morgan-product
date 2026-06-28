"""#1322 P2 — `_handle_list_issues_query` prefers the per-user OAuth connector.

The chat's "how many open issues?" handler now reads via the OAuth connector
(`GitHubMCPSpatialAdapter.list_open_issues`) when the user has a binding, falling back to
the native PAT ONLY when they haven't connected (CONNECT_REQUIRED), and degrading honestly
(#1231) when connected-but-unreachable — never a silent PAT fallback that hides the real
connection state.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent():
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        context={"original_message": "how many open issues"},
    )


@pytest.mark.asyncio
async def test_uses_connector_issues_when_bound(intent_service):
    conn_issues = [{"number": 7, "title": "Connector issue", "labels": [{"name": "bug"}]}]
    with patch(_CONN, new=AsyncMock(return_value=GitHubIssuesResult(issues=conn_issues))):
        with patch(_NATIVE) as native:
            res = await intent_service._handle_list_issues_query(_intent(), "wf")
    assert res.success
    assert "1 open issue" in res.message
    assert "#7" in res.message
    native.assert_not_called()  # connector hit → native PAT path never touched


@pytest.mark.asyncio
async def test_falls_back_to_native_when_not_connected(intent_service):
    degrade = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED,
            user_message="Connect GitHub to continue.",
            action_hint="/api/v1/settings/integrations/github/connect",
        )
    )
    native_router = MagicMock()
    native_router.initialize = AsyncMock()
    native_router.get_open_issues = AsyncMock(
        return_value=[{"number": 99, "title": "Native issue", "labels": []}]
    )
    with patch(_CONN, new=AsyncMock(return_value=degrade)):
        with patch(_NATIVE, return_value=native_router):
            res = await intent_service._handle_list_issues_query(_intent(), "wf")
    assert res.success
    assert "#99" in res.message  # served from the transitional native fallback
    native_router.get_open_issues.assert_awaited_once()


@pytest.mark.asyncio
async def test_honest_degrade_when_connected_but_unreachable(intent_service):
    degrade = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.UNREACHABLE,
            user_message="GitHub's MCP server is unreachable right now.",
        )
    )
    with patch(_CONN, new=AsyncMock(return_value=degrade)):
        with patch(_NATIVE) as native:
            res = await intent_service._handle_list_issues_query(_intent(), "wf")
    assert "unreachable" in res.message.lower()
    native.assert_not_called()  # connected → no silent PAT fallback (#1231)
