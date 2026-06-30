"""#1327 gap 2 — repo-scoped chat handlers prefer the per-user OAuth connector.

The branches / labels / releases / "review issue #N" handlers now read via the OAuth
connector (`GitHubMCPSpatialAdapter.{list_branches,list_labels,list_releases,get_issue}_connector`)
when the user has a binding, falling back to the native PAT ONLY when not connected
(CONNECT_REQUIRED), and degrading honestly otherwise — REPO_UNRESOLVED renders a "which repo?"
nudge, UNREACHABLE an honest message; never a silent PAT fallback that hides connection state
(#1231). Mirrors the #1322 issues/PRs handler cutover.

Milestones are intentionally NOT here — github-mcp-server has no milestone tool, so that
handler stays native (a separate test would only assert the native path is unchanged).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GitHubIssueResult,
    GitHubRepoScopedResult,
)
from services.shared_types import IntentCategory

_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
_BRANCHES = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_branches_connector"
_LABELS = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_labels_connector"
_RELEASES = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_releases_connector"
_ISSUE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.get_issue_connector"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(action, msg):
    return Intent(category=IntentCategory.QUERY, action=action, context={"original_message": msg})


def _connect_required():
    return DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED,
        user_message="Connect GitHub to continue.",
        action_hint="/api/v1/settings/integrations/github/connect",
    )


def _unreachable():
    return DegradationResponse(
        reason=DegradationReason.UNREACHABLE,
        user_message="GitHub's MCP server is unreachable right now.",
    )


def _which_repo():
    return DegradationResponse(
        reason=DegradationReason.REPO_UNRESOLVED,
        user_message="Which repo? I couldn't tell which repository you mean — name one.",
    )


# ── Branches (pattern handler) ──
class TestBranchesHandler:
    @pytest.mark.asyncio
    async def test_uses_connector_when_bound(self, intent_service):
        items = [
            {"name": "main", "protected": True, "commit_sha": "a"},
            {"name": "feature/x", "protected": False, "commit_sha": "b"},
        ]
        result = GitHubRepoScopedResult(items=items, resolved_repo="octo/hello")
        with patch(_BRANCHES, new=AsyncMock(return_value=result)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_branches_query(
                    _intent("list_branches_query", "show branches"), "wf"
                )
        assert res.success
        assert "2 branch" in res.message
        assert "main" in res.message
        native.assert_not_called()  # connector hit → native PAT never touched

    @pytest.mark.asyncio
    async def test_falls_back_to_native_when_not_connected(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_connect_required())
        native_router = MagicMock()
        native_router.list_branches_via_mcp = AsyncMock(
            return_value={"branches": [{"name": "main", "protected": True}], "default_branch": "main"}
        )
        with patch(_BRANCHES, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE, return_value=native_router):
                res = await intent_service._handle_list_branches_query(
                    _intent("list_branches_query", "show branches"), "wf"
                )
        assert res.success
        assert "main" in res.message  # served from the transitional native fallback
        native_router.list_branches_via_mcp.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_honest_degrade_when_unreachable(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_unreachable())
        with patch(_BRANCHES, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_branches_query(
                    _intent("list_branches_query", "show branches"), "wf"
                )
        assert "unreachable" in res.message.lower()
        native.assert_not_called()  # connected → no silent PAT fallback (#1231)

    @pytest.mark.asyncio
    async def test_which_repo_when_unresolved(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_which_repo())
        with patch(_BRANCHES, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_branches_query(
                    _intent("list_branches_query", "show branches"), "wf"
                )
        assert "which repo" in res.message.lower()
        native.assert_not_called()  # connected but no repo → ask, never native get-all


# ── Labels ──
class TestLabelsHandler:
    @pytest.mark.asyncio
    async def test_uses_connector_when_bound(self, intent_service):
        items = [{"name": "bug", "description": "broke"}, {"name": "enhancement", "description": ""}]
        result = GitHubRepoScopedResult(items=items, resolved_repo="octo/hello")
        with patch(_LABELS, new=AsyncMock(return_value=result)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_labels_query(
                    _intent("list_labels_query", "what labels"), "wf"
                )
        assert res.success
        assert "2 label" in res.message
        assert "bug" in res.message
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_to_native_when_not_connected(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_connect_required())
        native_router = MagicMock()
        native_router.list_labels_via_mcp = AsyncMock(return_value=[{"name": "bug", "description": ""}])
        with patch(_LABELS, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE, return_value=native_router):
                res = await intent_service._handle_list_labels_query(
                    _intent("list_labels_query", "what labels"), "wf"
                )
        assert "bug" in res.message
        native_router.list_labels_via_mcp.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_which_repo_when_unresolved(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_which_repo())
        with patch(_LABELS, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_labels_query(
                    _intent("list_labels_query", "what labels"), "wf"
                )
        assert "which repo" in res.message.lower()
        native.assert_not_called()


# ── Releases ──
class TestReleasesHandler:
    @pytest.mark.asyncio
    async def test_uses_connector_when_bound(self, intent_service):
        items = [
            {"tag_name": "v1.2.0", "name": "1.2.0", "prerelease": False, "published_at": "2026-06-01T0:0:0Z"},
        ]
        result = GitHubRepoScopedResult(items=items, resolved_repo="octo/hello")
        with patch(_RELEASES, new=AsyncMock(return_value=result)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_releases_query(
                    _intent("list_releases_query", "recent releases"), "wf"
                )
        assert res.success
        assert "v1.2.0" in res.message
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_to_native_when_not_connected(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_connect_required())
        native_router = MagicMock()
        native_router.list_releases_via_mcp = AsyncMock(
            return_value=[{"tag_name": "v9.9.9", "name": "9", "prerelease": False, "published_at": None}]
        )
        with patch(_RELEASES, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE, return_value=native_router):
                res = await intent_service._handle_list_releases_query(
                    _intent("list_releases_query", "recent releases"), "wf"
                )
        assert "v9.9.9" in res.message
        native_router.list_releases_via_mcp.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_honest_degrade_when_unreachable(self, intent_service):
        degrade = GitHubRepoScopedResult(degradation=_unreachable())
        with patch(_RELEASES, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_list_releases_query(
                    _intent("list_releases_query", "recent releases"), "wf"
                )
        assert "unreachable" in res.message.lower()
        native.assert_not_called()


# ── Review issue #N ──
class TestReviewIssueHandler:
    @pytest.mark.asyncio
    async def test_uses_connector_when_bound(self, intent_service):
        issue = {
            "number": 42,
            "title": "An issue",
            "state": "open",
            "body": "Body",
            "labels": ["bug"],
            "assignees": ["octo"],
            "html_url": "http://x/42",
        }
        result = GitHubIssueResult(item=issue, resolved_repo="octo/hello")
        with patch(_ISSUE, new=AsyncMock(return_value=result)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_review_issue_query(
                    _intent("review_issue_query", "review issue #42"), "wf"
                )
        assert res.success
        assert "#42" in res.message
        assert "An issue" in res.message
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_to_native_when_not_connected(self, intent_service):
        degrade = GitHubIssueResult(degradation=_connect_required())
        native_router = MagicMock()
        native_router.initialize = AsyncMock()
        native_router.config_service = MagicMock()
        native_router.config_service.is_configured = MagicMock(return_value=True)
        native_router.get_issue = AsyncMock(
            return_value={"number": 42, "title": "Native issue", "state": "open", "body": "b"}
        )
        with patch(_ISSUE, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE, return_value=native_router):
                res = await intent_service._handle_review_issue_query(
                    _intent("review_issue_query", "review issue #42"), "wf"
                )
        assert "Native issue" in res.message
        native_router.get_issue.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_honest_degrade_when_unreachable(self, intent_service):
        degrade = GitHubIssueResult(degradation=_unreachable())
        with patch(_ISSUE, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_review_issue_query(
                    _intent("review_issue_query", "review issue #42"), "wf"
                )
        assert "unreachable" in res.message.lower()
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_which_repo_when_unresolved(self, intent_service):
        degrade = GitHubIssueResult(degradation=_which_repo())
        with patch(_ISSUE, new=AsyncMock(return_value=degrade)):
            with patch(_NATIVE) as native:
                res = await intent_service._handle_review_issue_query(
                    _intent("review_issue_query", "review issue #42"), "wf"
                )
        assert "which repo" in res.message.lower()
        native.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_issue_number_asks_for_one(self, intent_service):
        # No #N in the message → graceful ask, connector never called.
        with patch(_ISSUE, new=AsyncMock()) as conn:
            res = await intent_service._handle_review_issue_query(
                _intent("review_issue_query", "review the issue"), "wf"
            )
        assert res.requires_clarification
        conn.assert_not_called()
