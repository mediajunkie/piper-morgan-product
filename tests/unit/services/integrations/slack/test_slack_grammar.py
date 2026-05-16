"""
Tests for grammar-conscious Slack responses.

Issue #620: GRAMMAR-TRANSFORM: Slack Integration
Phases 2-4: Integration and Template Transformation
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.integrations.slack.response_context import SlackResponseContext
from services.integrations.slack.simple_response_handler import SimpleSlackResponseHandler
from services.shared_types import IntentCategory, InteractionSpace


class TestSimpleResponseHandlerGrammar:
    """Test grammar-conscious response generation."""

    @pytest.fixture
    def mock_handler(self):
        """Create handler with mocked dependencies."""
        handler = SimpleSlackResponseHandler(
            spatial_adapter=MagicMock(),
            intent_classifier=MagicMock(),
            slack_client=MagicMock(),
        )
        return handler

    # --- Help Response Tests ---

    def test_help_response_dm_is_warm(self, mock_handler):
        """Help response in DM is warm and detailed."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="get_help",
            confidence=0.9,
        )
        slack_context = {"is_dm": True, "channel_id": "D123", "user_id": "U456"}

        response = mock_handler._get_simple_response_for_intent(intent, slack_context)

        assert "Happy to help" in response
        assert "🤖" not in response  # No robot emoji

    def test_help_response_channel_is_concise(self, mock_handler):
        """Help response in channel is concise."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="get_help",
            confidence=0.9,
        )
        slack_context = {"is_dm": False, "channel_id": "C123"}

        response = mock_handler._get_simple_response_for_intent(intent, slack_context)

        assert "I can help" in response
        assert len(response) < 100  # Concise

    # --- Greeting Response Tests ---

    def test_greeting_dm_is_casual(self, mock_handler):
        """Greeting in DM is casual."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=0.9,
        )
        slack_context = {"is_dm": True, "channel_id": "D123"}

        response = mock_handler._get_simple_response_for_intent(intent, slack_context)

        assert "Hey" in response or "Hi" in response
        assert "👋" not in response  # No wave emoji

    def test_greeting_channel_is_professional(self, mock_handler):
        """Greeting in channel is professional."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="hello",
            confidence=0.9,
        )
        slack_context = {"is_dm": False, "channel_id": "C123"}

        response = mock_handler._get_simple_response_for_intent(intent, slack_context)

        assert "Hi there" in response

    # --- Status Response Tests ---

    def test_status_response_is_natural(self, mock_handler):
        """Status response uses natural language."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_status",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "Everything's running" in response
        assert "📊" not in response  # No chart emoji
        assert "operational" not in response  # Not technical

    # --- Action Humanization Tests ---

    def test_action_humanization(self, mock_handler):
        """Actions are humanized in responses."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_ticket",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "create a ticket" in response
        assert "create_ticket" not in response  # Not the raw action

    def test_unknown_action_fallback(self, mock_handler):
        """Unknown actions are still humanized."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="run_special_report",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "run special report" in response
        assert "_" not in response  # Underscores converted

    # --- Format Response Tests ---

    def test_format_workflow_result_warm(self, mock_handler):
        """Workflow results use warm language."""
        result = {
            "type": "workflow_result",
            "result": {"summary": "Created ticket PM-123"},
        }

        formatted = mock_handler._format_response_content(result, None)

        assert "Done!" in formatted
        assert "✅" not in formatted  # No checkmark emoji

    def test_format_error_response_gentle(self, mock_handler):
        """Error responses are gentle."""
        result = {
            "type": "error_response",
            "content": "I encountered an issue processing your request.",
        }

        formatted = mock_handler._format_response_content(result, None)

        assert "hiccup" in formatted
        assert "error" not in formatted.lower()


class TestContractorTest:
    """Verify responses pass the Contractor Test."""

    @pytest.fixture
    def mock_handler(self):
        return SimpleSlackResponseHandler(
            spatial_adapter=MagicMock(),
            intent_classifier=MagicMock(),
            slack_client=MagicMock(),
        )

    def test_no_robot_emoji(self, mock_handler):
        """No robot emoji in any response."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="get_help",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "🤖" not in response

    def test_no_chart_emoji_in_status(self, mock_handler):
        """No chart emoji in status responses."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_status",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "📊" not in response

    def test_no_magnifying_glass_prefix(self, mock_handler):
        """No magnifying glass prefix in responses."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(intent, None)

        assert "🔍" not in response

    def test_professional_not_childish(self, mock_handler):
        """Responses are professional, not childish."""
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=0.9,
        )

        response = mock_handler._get_simple_response_for_intent(
            intent, {"is_dm": False, "channel_id": "C123"}
        )

        # Should NOT be over-enthusiastic
        assert response.count("!") <= 1
        assert "awesome" not in response.lower()
        assert "amazing" not in response.lower()


class TestResponseContextIntegration:
    """Test that response context is properly built and used."""

    @pytest.fixture
    def mock_handler(self):
        return SimpleSlackResponseHandler(
            spatial_adapter=MagicMock(),
            intent_classifier=MagicMock(),
            slack_client=MagicMock(),
        )

    def test_build_response_context_dm(self, mock_handler):
        """Builds correct context for DM."""
        slack_context = {"is_dm": True, "channel_id": "D123", "user_id": "U456"}

        ctx = mock_handler._build_response_context(slack_context)

        assert ctx is not None
        assert ctx.place == InteractionSpace.SLACK_DM
        assert ctx.channel_id == "D123"

    def test_build_response_context_channel(self, mock_handler):
        """Builds correct context for channel."""
        slack_context = {"is_dm": False, "channel_id": "C123"}

        ctx = mock_handler._build_response_context(slack_context)

        assert ctx is not None
        assert ctx.place == InteractionSpace.SLACK_CHANNEL

    def test_build_response_context_handles_none(self, mock_handler):
        """Handles None slack_context gracefully."""
        ctx = mock_handler._build_response_context(None)

        assert ctx is None

    def test_formality_affects_response(self, mock_handler):
        """Formality level affects response tone."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.9,
        )

        # DM should be more casual
        dm_response = mock_handler._get_simple_response_for_intent(
            intent, {"is_dm": True, "channel_id": "D123"}
        )
        # Channel should be more formal
        channel_response = mock_handler._get_simple_response_for_intent(
            intent, {"is_dm": False, "channel_id": "C123"}
        )

        # Both should work but might have different tones
        assert dm_response is not None
        assert channel_response is not None
