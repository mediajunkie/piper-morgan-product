"""
Tests for HonestFailureHandler.

Issue #619: GRAMMAR-TRANSFORM: Intent Classification
Phase 5: Honest Failure
Pattern: Pattern-054 (Honest Failure)
"""

import pytest

from services.domain.models import Intent
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)
from services.intent_service.intent_types import IntentClassificationContext
from services.shared_types import IntentCategory, InteractionSpace, PerceptionMode


class TestHonestFailureHandler:
    """Test HonestFailureHandler."""

    @pytest.fixture
    def handler(self):
        return HonestFailureHandler()

    @pytest.fixture
    def basic_context(self):
        return IntentClassificationContext(
            message="do the thing with the stuff",
            user_id="user-1",
            place=InteractionSpace.WEB_CHAT,
        )

    @pytest.fixture
    def casual_settings(self):
        return {"formality": "casual", "verbosity": "medium"}

    @pytest.fixture
    def professional_settings(self):
        return {"formality": "professional", "verbosity": "concise"}

    @pytest.fixture
    def terse_settings(self):
        return {"formality": "terse", "verbosity": "minimal"}

    # --- Classification Failure Tests ---

    def test_failure_creates_understanding(self, handler, basic_context, casual_settings):
        """Failure creates IntentUnderstanding, not exception."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        # Returns understanding, not raises exception
        assert result is not None
        assert result.intent.category == IntentCategory.CONVERSATION
        assert result.intent.action == "clarification_needed"

    def test_failure_narrative_is_warm(self, handler, basic_context, casual_settings):
        """Failure narrative uses warm language."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should express difficulty, not failure
        assert "having trouble" in narrative or "not quite" in narrative
        # Should NOT be technical
        assert "error" not in narrative
        assert "failed" not in narrative
        assert "exception" not in narrative

    def test_failure_suggests_followup(self, handler, basic_context, casual_settings):
        """Failure suggests how to proceed."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
        )
        assert result.follow_up_suggestion is not None
        # Should ask for clarification
        assert "?" in result.follow_up_suggestion

    def test_terse_failure_is_brief(self, handler, basic_context, terse_settings):
        """Terse context gets brief failure message."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=terse_settings,
        )
        assert len(result.understanding_narrative) < 30
        assert result.follow_up_suggestion == "Please clarify."

    # --- Low Confidence Tests ---

    def test_low_confidence_expresses_uncertainty(self, handler, basic_context, casual_settings):
        """Low confidence expressed as uncertainty."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_files",
            confidence=0.3,
        )
        result = handler.handle_low_confidence(
            intent=intent,
            context=basic_context,
            place_settings=casual_settings,
        )
        narrative = result.understanding_narrative.lower()
        # Should express uncertainty
        assert "think" in narrative or "might" in narrative or "not sure" in narrative

    def test_low_confidence_asks_confirmation(self, handler, basic_context, professional_settings):
        """Low confidence asks for confirmation."""
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_item",
            confidence=0.4,
        )
        result = handler.handle_low_confidence(
            intent=intent,
            context=basic_context,
            place_settings=professional_settings,
        )
        # Should ask if understanding is correct
        assert result.follow_up_suggestion is not None
        assert "?" in result.follow_up_suggestion

    # #1759: the vague-intent tests were excised with handle_vague_intent,
    # deleted as part of the dead clarify-carrier machinery (#1730 Gap-2
    # ruling). handle_classification_failure / handle_low_confidence tests
    # above cover the surviving members.

    # --- Experience Tests ---

    def test_no_technical_jargon(self, handler, basic_context, casual_settings):
        """Responses should avoid technical jargon."""
        result = handler.handle_classification_failure(
            context=basic_context,
            place_settings=casual_settings,
            error_detail="JSONDecodeError: Invalid JSON",
        )
        narrative = result.understanding_narrative.lower()
        follow_up = (result.follow_up_suggestion or "").lower()

        # Technical terms should NOT appear in user-facing text
        assert "json" not in narrative
        assert "decode" not in narrative
        assert "exception" not in narrative
        assert "json" not in follow_up


class TestCreateGracefulErrorResponse:
    """Test the factory function."""

    def test_factory_creates_response(self):
        """Factory function creates graceful response."""
        context = IntentClassificationContext(
            message="broken request",
            place=InteractionSpace.WEB_CHAT,
        )
        settings = {"formality": "warm"}

        result = create_graceful_error_response(
            context=context,
            place_settings=settings,
            error=ValueError("something broke"),
        )

        assert result is not None
        assert result.intent.action == "clarification_needed"
        # Error detail stored for debugging but not shown
        assert "_error_detail" in result.intent.context


class TestContractorTest:
    """Verify responses pass the 'Contractor Test'."""

    def test_failure_sounds_professional(self):
        """Failure responses should sound professional."""
        handler = HonestFailureHandler()
        context = IntentClassificationContext(
            message="test",
            place=InteractionSpace.SLACK_CHANNEL,
        )
        settings = {"formality": "professional"}

        result = handler.handle_classification_failure(
            context=context,
            place_settings=settings,
        )

        narrative = result.understanding_narrative

        # Should NOT sound like a children's app
        assert "Oops" not in narrative
        assert "Uh oh" not in narrative
        assert "!" not in narrative  # No exclamation in errors

        # SHOULD sound like a professional colleague
        assert "I'm" in narrative  # First person
