"""
Tests for Issue #902: Reopen issue functionality and close issue fallback fix.

Covers:
- Pre-classifier patterns for close and reopen
- Reopen handler: mock GitHubIntegrationRouter, verify state="open"
- Close handler still works
- Fallback messages are helpful, not misleading
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """Create IntentService instance for testing"""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            service = IntentService()
            return service


@pytest.fixture
def fallback_service():
    """Lightweight IntentService for sync fallback testing (no __init__)."""
    return IntentService.__new__(IntentService)


# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestPreClassifierClosePatterns:
    """Verify close issue patterns still classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "close issue #123",
            "close issue 456",
            "close the completed issue",
            "please close issue #789",
        ],
    )
    def test_close_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\bclose issue\s*#?\d+\b",
                r"\bclose.*completed.*issue\b",
                r"\bclose.*issue\b",
            ],
        )
        assert result is True


class TestPreClassifierReopenPatterns:
    """Verify reopen issue patterns classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "reopen issue #456",
            "reopen issue 789",
            "re-open issue #789",
            "reopen the closed issue",
            "re-open that issue",
        ],
    )
    def test_reopen_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\breopen\s+issue\s*#?\d+\b",
                r"\bre-open\s+issue\s*#?\d+\b",
                r"\breopen\s+.*issue\b",
                r"\bre-open\s+.*issue\b",
            ],
        )
        assert result is True


class TestPreClassifierConfirmationPatterns:
    """Issue #902: Verify confirmation patterns for close/reopen classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "yes, close #123",
            "confirm close #456",
            "sure, close #789",
        ],
    )
    def test_close_confirmation_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\bclose issue\s*#?\d+\b",
                r"\bclose.*completed.*issue\b",
                r"\bclose.*issue\b",
                r"\b(yes|confirm|sure),?\s*close\s*#?\d+\b",
            ],
        )
        assert result is True

    @pytest.mark.parametrize(
        "message",
        [
            "yes, reopen #123",
            "confirm reopen #456",
            "sure, reopen #789",
        ],
    )
    def test_reopen_confirmation_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message,
            [
                r"\breopen\s+issue\s*#?\d+\b",
                r"\bre-open\s+issue\s*#?\d+\b",
                r"\breopen\s+.*issue\b",
                r"\bre-open\s+.*issue\b",
                r"\b(yes|confirm|sure),?\s*reopen\s*#?\d+\b",
            ],
        )
        assert result is True


# ---------------------------------------------------------------------------
# Reopen handler tests
# ---------------------------------------------------------------------------


class TestReopenIssueHandler:
    """Test _handle_reopen_issue_query handler."""

    @pytest.mark.asyncio
    async def test_reopens_issue_with_confirmed_message(self, intent_service):
        """Verify confirmed reopen passes state='open' to update_issue."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            # Issue #902: "yes" triggers confirmed path
            context={"original_message": "yes, reopen #42"},
        )

        mock_updated_issue = {
            "number": 42,
            "title": "Add search feature",
            "state": "open",
            "html_url": "https://github.com/org/repo/issues/42",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(return_value=mock_updated_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "Reopened issue #42" in result.message
            assert "Add search feature" in result.message
            assert result.intent_data["issue_number"] == 42

            # The critical assertion: state="open"
            # Issue #1042: hardcoded "piper-morgan-product" arg removed; router
            # now resolves repo internally.
            mock_router.update_issue.assert_awaited_once_with(42, state="open")

    @pytest.mark.asyncio
    async def test_unconfirmed_reopen_asks_for_confirmation(self, intent_service):
        """Issue #902: Unconfirmed reopen shows issue title and asks to confirm."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        mock_issue = {
            "number": 42,
            "title": "Add search feature",
            "state": "closed",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_issue = AsyncMock(return_value=mock_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert "Add search feature" in result.message
            assert "confirm" in result.message.lower() or "reopen #42" in result.message
            assert result.requires_clarification is True
            # update_issue should NOT be called yet
            mock_router.update_issue.assert_not_called()

    @pytest.mark.asyncio
    async def test_reopen_already_open_issue(self, intent_service):
        """Issue #902: Reopen on already-open issue returns informative message."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        mock_issue = {
            "number": 42,
            "title": "Add search feature",
            "state": "open",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_issue = AsyncMock(return_value=mock_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert "already open" in result.message.lower()
            mock_router.update_issue.assert_not_called()

    @pytest.mark.asyncio
    async def test_reopen_missing_issue_number(self, intent_service):
        """Test handling when no issue number is present and no search terms."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen that issue"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert result.success is False
            assert "couldn't find any issues matching" in result.message
            assert result.requires_clarification is True

    @pytest.mark.asyncio
    async def test_reopen_github_not_configured(self, intent_service):
        """Test graceful message when GitHub is not configured."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen issue #42"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_reopen_handles_github_error(self, intent_service):
        """Test error handling for GitHub API failures."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            # Confirmed so it reaches the update_issue call
            context={"original_message": "yes, reopen issue #42"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(side_effect=Exception("GitHub API error"))
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "workflow-id")

            assert result.success is False
            assert (
                "reopening that issue" in result.message.lower()
                or "error" in result.message.lower()
            )


# ---------------------------------------------------------------------------
# Close handler still-works test
# ---------------------------------------------------------------------------


class TestCloseIssueHandlerStillWorks:
    """Verify close handler works with confirmation UX."""

    @pytest.mark.asyncio
    async def test_confirmed_close_passes_state_closed(self, intent_service):
        """Issue #902: Confirmed close passes state='closed' to update_issue."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            # "yes" triggers confirmed path
            context={"original_message": "yes, close #123"},
        )

        mock_updated_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "closed",
            "html_url": "https://github.com/org/repo/issues/123",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(return_value=mock_updated_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "Closed issue #123" in result.message
            # Issue #1042: hardcoded "piper-morgan-product" arg removed.
            mock_router.update_issue.assert_awaited_once_with(123, state="closed")

    @pytest.mark.asyncio
    async def test_unconfirmed_close_asks_for_confirmation(self, intent_service):
        """Issue #902: Unconfirmed close shows issue title and asks to confirm."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        mock_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "open",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_issue = AsyncMock(return_value=mock_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert "Fix authentication bug" in result.message
            assert "close #123" in result.message.lower()
            assert result.requires_clarification is True
            mock_router.update_issue.assert_not_called()

    @pytest.mark.asyncio
    async def test_close_already_closed_issue(self, intent_service):
        """Issue #902: Close on already-closed issue returns informative message."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        mock_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "closed",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_issue = AsyncMock(return_value=mock_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert "already closed" in result.message.lower()
            mock_router.update_issue.assert_not_called()


# ---------------------------------------------------------------------------
# Fallback message tests
# ---------------------------------------------------------------------------


class TestFallbackMessages:
    """Test that fallback messages are helpful, not misleading."""

    def test_close_fallback_says_can_not_cant(self, fallback_service):
        """Close fallback should say 'I can close issues!' not 'I can't'."""
        result = fallback_service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="close that completed issue",
        )
        assert "I can close issues!" in result
        assert "can't close" not in result

    def test_reopen_fallback_says_can(self, fallback_service):
        """Reopen fallback should say 'I can reopen issues!'."""
        result = fallback_service._get_contextual_fallback(
            mapped_action="reopen_issue",
            original_message="reopen the issue we discussed",
        )
        assert "I can reopen issues!" in result
        assert "can't" not in result

    def test_close_fallback_suggests_issue_number(self, fallback_service):
        result = fallback_service._get_contextual_fallback(
            mapped_action="close_issue",
            original_message="close the issue",
        )
        assert "#123" in result  # suggests format

    def test_reopen_fallback_suggests_issue_number(self, fallback_service):
        result = fallback_service._get_contextual_fallback(
            mapped_action="reopen_issue",
            original_message="reopen that issue",
        )
        assert "#123" in result  # suggests format


# ---------------------------------------------------------------------------
# Fuzzy match helper tests (Issue #902)
# ---------------------------------------------------------------------------


class TestExtractSearchTerms:
    """Test _extract_search_terms static method."""

    def test_strips_close_command(self):
        result = IntentService._extract_search_terms("close the auth bug", "close")
        assert "close" not in result
        assert "auth" in result
        assert "bug" in result

    def test_strips_reopen_command(self):
        result = IntentService._extract_search_terms("reopen the login issue", "reopen")
        assert "reopen" not in result
        assert "login" in result

    def test_strips_filler_words(self):
        result = IntentService._extract_search_terms(
            "please close the issue about authentication", "close"
        )
        assert "please" not in result
        assert "the" not in result.split()
        assert "authentication" in result

    def test_empty_after_stripping(self):
        result = IntentService._extract_search_terms("close the issue", "close")
        assert result == ""

    def test_preserves_meaningful_words(self):
        result = IntentService._extract_search_terms("close the search feature bug", "close")
        assert "search" in result
        assert "feature" in result
        assert "bug" in result


class TestScoreIssueMatch:
    """Test _score_issue_match static method."""

    def test_exact_word_overlap(self):
        score = IntentService._score_issue_match("auth bug", "Fix authentication bug")
        assert score == 1  # "bug" matches

    def test_multiple_word_overlap(self):
        score = IntentService._score_issue_match(
            "search feature", "Add search feature to dashboard"
        )
        assert score == 2

    def test_no_overlap(self):
        score = IntentService._score_issue_match("auth bug", "Update README")
        assert score == 0

    def test_empty_search(self):
        score = IntentService._score_issue_match("", "Some issue title")
        assert score == 0

    def test_case_insensitive(self):
        score = IntentService._score_issue_match("Auth", "Fix auth middleware")
        assert score == 1


# ---------------------------------------------------------------------------
# Fuzzy close/reopen integration tests (Issue #902)
# ---------------------------------------------------------------------------


class TestFuzzyCloseIssue:
    """Test fuzzy matching in _handle_close_issue_query when no issue number given."""

    @pytest.mark.asyncio
    async def test_single_fuzzy_match_asks_confirmation(self, intent_service):
        """When exactly 1 open issue matches, ask for confirmation."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close the auth bug"},
        )

        mock_open_issues = [
            {"number": 42, "title": "Fix authentication bug", "state": "open"},
            {"number": 43, "title": "Add search feature", "state": "open"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_issues)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "Did you mean issue #42" in result.message
            assert "Fix authentication bug" in result.message
            assert result.intent_data["matched_issue_number"] == 42

    @pytest.mark.asyncio
    async def test_multiple_fuzzy_matches_lists_options(self, intent_service):
        """When multiple open issues match, list them."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close the auth middleware"},
        )

        mock_open_issues = [
            {"number": 42, "title": "Fix auth middleware crash", "state": "open"},
            {"number": 55, "title": "Auth middleware update needed", "state": "open"},
            {"number": 60, "title": "Add search feature", "state": "open"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_issues)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "I found a few issues" in result.message
            assert "#42" in result.message
            assert "#55" in result.message
            assert "matched_issues" in result.intent_data
            assert len(result.intent_data["matched_issues"]) == 2

    @pytest.mark.asyncio
    async def test_no_fuzzy_matches_returns_helpful_message(self, intent_service):
        """When no issues match the description, return helpful message."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close the quantum entanglement problem"},
        )

        mock_open_issues = [
            {"number": 42, "title": "Fix authentication middleware", "state": "open"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_issues)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "couldn't find any issues matching" in result.message

    @pytest.mark.asyncio
    async def test_no_search_terms_returns_fallback(self, intent_service):
        """When message has no meaningful search terms, return fallback."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close the issue"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "couldn't find any issues matching" in result.message


class TestFuzzyReopenIssue:
    """Test fuzzy matching in _handle_reopen_issue_query when no issue number given."""

    @pytest.mark.asyncio
    async def test_single_fuzzy_match_asks_confirmation(self, intent_service):
        """When exactly 1 closed issue matches, ask for confirmation."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen the search feature"},
        )

        mock_closed_issues = [
            {"number": 99, "title": "Add search feature", "state": "closed"},
            {"number": 100, "title": "Fix login page", "state": "closed"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_closed_issues = AsyncMock(return_value=mock_closed_issues)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "Did you mean issue #99" in result.message
            assert "reopen issue #99" in result.message
            assert result.intent_data["matched_issue_number"] == 99

    @pytest.mark.asyncio
    async def test_multiple_fuzzy_matches_lists_options(self, intent_service):
        """When multiple closed issues match, list them."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="reopen_issue_query",
            context={"original_message": "reopen the auth bug"},
        )

        mock_closed_issues = [
            {"number": 10, "title": "Auth bug on login", "state": "closed"},
            {"number": 20, "title": "Fix auth bug in middleware", "state": "closed"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_closed_issues = AsyncMock(return_value=mock_closed_issues)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_reopen_issue_query(intent, "wf-id")

            assert result.success is False
            assert result.requires_clarification is True
            assert "I found a few issues" in result.message
            assert "#10" in result.message
            assert "#20" in result.message
            assert "Which one would you like to reopen?" in result.message
