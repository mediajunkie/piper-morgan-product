"""Tests for #1159: _handle_comment_issue_query degrades gracefully on a
repo-resolution failure instead of the opaque 'something unexpected happened'.

The classifier routes 'comment on issue N saying X' to comment_issue_query, which
reaches _handle_comment_issue_query. When no repository resolves, the router
raises RuntimeError('...no repo could be resolved.'); the handler should turn
that into a helpful 'which repo?' clarification, NOT the generic error.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _comment_intent():
    return Intent(
        category=IntentCategory.QUERY,
        action="comment_issue_query",
        context={"original_message": "comment on issue 42 saying thanks for the fix"},
    )


class TestCommentIssueGracefulRepoResolution:
    @pytest.mark.llm  # #1452: needs live LLM slot-extraction (CI: 'No LLM providers configured')
    @pytest.mark.asyncio
    async def test_no_repo_resolved_returns_graceful_clarification(self, intent_service):
        """RuntimeError('no repo could be resolved') → 'which repo?' clarification,
        not the generic 'something unexpected happened'."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.add_comment = AsyncMock(
                side_effect=RuntimeError(
                    "Cannot add comment to GitHub issue #42: no repo could be resolved."
                )
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_comment_issue_query(
                _comment_intent(), "workflow-id"
            )

        assert result.success is True
        assert result.requires_clarification is True
        assert result.clarification_type == "repository_required"
        assert "repository" in result.message.lower()
        # The whole point of #1159: NOT the opaque message.
        assert "something unexpected" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_other_errors_still_use_generic_error_path(self, intent_service):
        """A non-repo-resolution failure must NOT be mislabeled as a repo issue —
        it still flows through the generic error result."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.add_comment = AsyncMock(
                side_effect=RuntimeError("GitHub API returned 503 Service Unavailable")
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_comment_issue_query(
                _comment_intent(), "workflow-id"
            )

        # Not the repo-resolution clarification.
        assert result.clarification_type != "repository_required"
        assert "repository" not in result.message.lower()
