"""
Tests for Multi-Intent Detection and Handling (Issue #595).

This module tests the proper parsing and handling of messages containing
multiple intents, such as "Hi Piper! What's on my agenda?"

The multi-intent system supports:
- Detection of multiple intents in a single message
- "Handle all" strategy (process all detected intents)
- Proper priority ordering (substantive > conversational)
- Greeting acknowledgment when combined with substantive intents

This detection logic is designed to be reusable for #427
(Unified Conversation Model).
"""

import pytest

from services.domain.models import Intent
from services.intent_service.pre_classifier import MultiIntentResult, PreClassifier
from services.shared_types import IntentCategory


class TestMultiIntentResult:
    """Test the MultiIntentResult dataclass."""

    def test_empty_result(self):
        """Empty result has no intents and is not multi-intent."""
        result = MultiIntentResult()
        assert len(result.intents) == 0
        assert result.is_multi_intent is False
        assert result.primary_intent is None
        assert result.secondary_intents == []
        assert result.has_greeting is False
        assert result.has_substantive_intent is False

    def test_single_intent_result(self):
        """Single intent result is not multi-intent."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[intent],
            original_message="What's on my agenda?",
            is_multi_intent=False,
        )
        assert len(result.intents) == 1
        assert result.is_multi_intent is False
        assert result.primary_intent == intent
        assert result.secondary_intents == []

    def test_multi_intent_result(self):
        """Multiple intents properly detected."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi Piper! What's on my agenda?",
            is_multi_intent=True,
        )
        assert len(result.intents) == 2
        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.has_substantive_intent is True

    def test_primary_intent_prefers_substantive(self):
        """Primary intent should be substantive over conversational."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        # Order doesn't matter - substantive should be primary
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi! What's on my agenda?",
            is_multi_intent=True,
        )
        assert result.primary_intent.category == IntentCategory.QUERY
        assert result.primary_intent.action == "meeting_time"

    def test_secondary_intents_excludes_primary(self):
        """Secondary intents should exclude the primary."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        query = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, query],
            original_message="Hi! What's on my agenda?",
            is_multi_intent=True,
        )
        secondary = result.secondary_intents
        assert len(secondary) == 1
        assert secondary[0].category == IntentCategory.CONVERSATION
        assert secondary[0].action == "greeting"

    def test_all_conversational_uses_first(self):
        """When all intents are conversational, use first as primary."""
        greeting = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
        )
        thanks = Intent(
            category=IntentCategory.CONVERSATION,
            action="thanks",
            confidence=1.0,
        )
        result = MultiIntentResult(
            intents=[greeting, thanks],
            original_message="Hi! Thanks!",
            is_multi_intent=True,
        )
        assert result.primary_intent.action == "greeting"


class TestDetectMultipleIntents:
    """Test PreClassifier.detect_multiple_intents()."""

    # #1924 (2026-10-03): the #1595 Phase 3 deletions emptied the surface-1
    # lists that used to co-claim the substance of these greeting+question
    # messages (CALENDAR_QUERY, TODO_QUERY, STATUS, PRIORITY). The greeting
    # was left as the sole detection and swallowed the question. The #1416
    # rule now holds on this path too: a pleasantry-only detection on a
    # message with substantive residue returns NO intents, so the turn goes
    # to full classification of the whole message (the floor greets AND
    # answers). These pins assert that contract; the greeting must never be
    # the answer to a message that asked something.
    GREETING_PLUS_QUESTION = [
        "Hi Piper! What's on my agenda?",  # the canonical #595 bug case
        "Hello! What's on my calendar today?",
        "Hey, do I have any meetings today?",
        "Good morning! What's my schedule today?",
        "Hi! Show my todos",
        "Hello! What am I working on?",
        "Hey Piper, what should I focus on today?",
    ]

    @pytest.mark.parametrize("message", GREETING_PLUS_QUESTION)
    def test_greeting_never_swallows_the_question(self, message):
        result = PreClassifier.detect_multiple_intents(message)

        assert result.intents == [], (
            f"{message!r}: a greeting-only detection must not claim a message "
            f"that asks something (#1924/#1416), got {result.intents}"
        )
        assert result.primary_intent is None
        # Same answer as the single path for the same message.
        assert PreClassifier.pre_classify(message) is None

    def test_greeting_plus_still_claimed_substance(self):
        """Greeting + a substance surface 1 still claims stays multi-intent
        (ANALYSIS_PATTERNS survivor \bwhat.*obstacle\b)."""
        result = PreClassifier.detect_multiple_intents("Hi Piper! What's the main obstacle here?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True
        assert result.has_substantive_intent is True
        assert result.primary_intent.category == IntentCategory.ANALYSIS
        assert result.primary_intent.action == "analyze_blockers"

    def test_single_greeting_only(self):
        """Pure greeting should detect single intent."""
        result = PreClassifier.detect_multiple_intents("Hello!")

        assert len(result.intents) == 1
        assert result.is_multi_intent is False
        assert result.has_greeting is True
        assert result.has_substantive_intent is False

    def test_single_query_only(self):
        """Pure query without greeting."""
        result = PreClassifier.detect_multiple_intents("What's on my agenda?")

        # #1924: CALENDAR_QUERY_PATTERNS is deleted (#1595 Phase 3); surface 1
        # no longer claims the agenda ask, so it goes to full classification.
        assert result.intents == []

    def test_thanks_plus_query(self):
        """Thanks with query shouldn't be treated as greeting+substantive."""
        result = PreClassifier.detect_multiple_intents("Thanks! What's next?")

        # #1924: thanks-only detection with substantive residue declines (the
        # #1416 rule) rather than answering "you're welcome" to a question.
        assert result.intents == []

    def test_no_intents_detected(self):
        """Message with no matching patterns."""
        result = PreClassifier.detect_multiple_intents("xyzzy plugh")

        assert len(result.intents) == 0
        assert result.is_multi_intent is False
        assert result.primary_intent is None


class TestMultiIntentEdgeCases:
    """Test edge cases in multi-intent detection."""

    def test_emoji_in_greeting(self):
        """Greeting with emoji should still detect multiple intents."""
        result = PreClassifier.detect_multiple_intents("Hi! 👋 What's the main obstacle here?")

        # #1924: swapped from "What's my schedule?" (no longer claimed at
        # surface 1) to an ANALYSIS survivor so the emoji case stays exercised.
        assert result.has_greeting is True
        assert result.has_substantive_intent is True

    def test_multiple_substantive_intents(self):
        """Multiple substantive intents in one message."""
        result = PreClassifier.detect_multiple_intents("What's on my calendar and show my todos")

        # #1924: neither list survives the #1595 Phase 3 deletions; the
        # message goes to full classification (the router splits it).
        assert result.intents == []

    def test_case_insensitive_detection(self):
        """Detection should be case insensitive."""
        result = PreClassifier.detect_multiple_intents("HI PIPER! WHAT'S THE MAIN OBSTACLE HERE?")

        assert result.is_multi_intent is True
        assert result.has_greeting is True

    def test_extra_whitespace_handling(self):
        """Extra whitespace should be handled."""
        result = PreClassifier.detect_multiple_intents("  Hi!   What's the main obstacle here?  ")

        assert result.is_multi_intent is True
        assert result.has_greeting is True

    def test_exclamation_points(self):
        """Multiple exclamation points should be handled."""
        result = PreClassifier.detect_multiple_intents(
            "Hello!!! What's in the way of finishing this???"
        )

        assert result.is_multi_intent is True
        assert result.has_greeting is True


class TestCalendarActionRefinement:
    """Calendar action refinement used to happen at surface 1 in the
    multi-intent path. #1595 Phase 3's third deletion removed
    CALENDAR_QUERY_PATTERNS; the router (read_temporal) chooses the calendar
    operation now. Converted (#1924): these greeting+calendar asks decline at
    surface 1 rather than being answered as a greeting."""

    @pytest.mark.parametrize(
        "message",
        [
            "Hi! What's on my agenda?",
            "Hi! What's my week look like?",
            "Hi! Show my recurring meetings",
        ],
    )
    def test_calendar_asks_decline_to_full_classification(self, message):
        result = PreClassifier.detect_multiple_intents(message)
        assert result.intents == []
        assert result.primary_intent is None


class TestMultiIntentContextMarking:
    """Test that multi-intent context is properly marked."""

    def test_context_includes_multi_intent_flag(self):
        """Detected intents should have multi_intent_detection context."""
        result = PreClassifier.detect_multiple_intents("Hi! What's the main obstacle here?")

        assert result.intents  # non-vacuous (#1924 swapped off the deleted agenda claim)
        for intent in result.intents:
            assert intent.context.get("multi_intent_detection") is True

    def test_context_includes_original_message(self):
        """Detected intents should have original_message in context."""
        message = "Hi Piper! What's the main obstacle here?"
        result = PreClassifier.detect_multiple_intents(message)

        assert result.intents  # non-vacuous (#1924 swapped off the deleted agenda claim)
        for intent in result.intents:
            assert intent.context.get("original_message") == message
