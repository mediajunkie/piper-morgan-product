"""
Issue #102: Tests for calendar-aware greeting responses in ConversationHandler.

Tests verify:
- Greeting with calendar available includes schedule summary
- Greeting without calendar falls back to standard response
- Greeting with empty calendar shows "Clear calendar" message
- Time-of-day greeting returns appropriate message
- Non-greeting actions are rejected (#1754: handler is greeting-only; the
  farewell/thanks/chitchat branches and the RESPONSES canned table were
  deleted — the action gate admits only pure-pleasantry greetings here)
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.shared_types import IntentCategory


class TestCalendarGreeting:
    """Issue #102: Tests for calendar-aware greeting responses."""

    @pytest.fixture
    def handler(self):
        """Create ConversationHandler instance for testing."""
        return ConversationHandler()

    @pytest.fixture
    def greeting_intent(self):
        """Create a greeting intent for testing."""
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=0.95,
            original_message="Good morning",
        )

    @pytest.mark.asyncio
    async def test_greeting_with_calendar_available(self, handler, greeting_intent):
        """Greeting includes calendar summary when available."""
        mock_summary = {
            "current_meeting": None,
            "next_meeting": {
                "summary": "Sprint Planning",
                "start_time": "2026-01-07T10:00:00-08:00",
            },
            "free_blocks": [
                {
                    "start_time": "2026-01-07T09:00:00-08:00",
                    "end_time": "2026-01-07T10:00:00-08:00",
                    "duration_minutes": 60,
                }
            ],
            "stats": {
                "total_meetings_today": 2,
                "total_meeting_minutes": 120,
                "total_free_minutes": 180,
            },
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            assert "Sprint Planning" in result["message"]
            assert "2 meetings today" in result["message"]

    @pytest.mark.asyncio
    async def test_greeting_without_calendar(self, handler, greeting_intent):
        """Greeting falls back gracefully when calendar unavailable."""
        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = None

            result = await handler.respond(greeting_intent)

            # Should use standard greeting response (may be time-aware via consciousness)
            assert "message" in result
            # #1754: RESPONSES canned table deleted — greetings are always
            # consciousness-formatted (format_greeting_conscious).
            msg = result["message"]
            is_time_aware = any(
                g in msg for g in ["Good morning", "Good afternoon", "Good evening", "Hello", "Hi"]
            )
            assert is_time_aware, f"Unexpected greeting: {msg}"

    @pytest.mark.asyncio
    async def test_greeting_with_calendar_error(self, handler, greeting_intent):
        """Greeting falls back gracefully when calendar returns error."""
        mock_summary = {
            "error": "Calendar unavailable",
            "fallback": "Static calendar patterns from configuration",
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            # Should use standard greeting response (not show error)
            assert "message" in result
            # #1754: RESPONSES canned table deleted — greetings are always
            # consciousness-formatted (format_greeting_conscious).
            msg = result["message"]
            is_time_aware = any(
                g in msg for g in ["Good morning", "Good afternoon", "Good evening", "Hello", "Hi"]
            )
            assert is_time_aware, f"Unexpected greeting: {msg}"

    @pytest.mark.asyncio
    async def test_greeting_with_empty_calendar(self, handler, greeting_intent):
        """Greeting handles an ESTABLISHED empty calendar gracefully.

        #1425: this fixture gained ``events_read_established``. Without it the
        summary is indistinguishable from a failed read that returned [], and
        the greeting must no longer call such a day clear — see
        ``test_greeting_does_not_claim_clear_day_on_unestablished_read`` below,
        which is the shape PM actually hit on 2026-08-10.
        """
        mock_summary = {
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
            "events_read_established": True,
            "stats": {
                "total_meetings_today": 0,
                "total_meeting_minutes": 0,
                "total_free_minutes": 480,
            },
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            # Consciousness-aware formatting may use different phrases (Issue #633-638)
            msg = result["message"].lower()
            assert "clear" in msg, f"Expected mention of clear calendar, got: {result['message']}"

    @pytest.mark.asyncio
    async def test_greeting_does_not_claim_clear_day_on_unestablished_read(
        self, handler, greeting_intent
    ):
        """#1425 / m-44: zero rows with nothing attesting the read happened.

        This is exactly what the deployed greeting was handed at 02:09Z on
        2026-08-10 — and it answered "a clear day ahead" over four real events.
        """
        mock_summary = {
            "current_meeting": None,
            "next_meeting": None,
            "free_blocks": [],
            "stats": {
                "total_meetings_today": 0,
                "total_meeting_minutes": 0,
                "total_free_minutes": 480,
            },
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            msg = result["message"].lower()
            assert "clear" not in msg, result["message"]
            assert "took a look at your calendar" not in msg, result["message"]

    @pytest.mark.asyncio
    async def test_greeting_with_current_meeting(self, handler, greeting_intent):
        """Greeting shows current meeting when in progress."""
        mock_summary = {
            "current_meeting": {
                "summary": "Team Standup",
                "start_time": "2026-01-07T09:00:00-08:00",
                "end_time": "2026-01-07T09:30:00-08:00",
            },
            "next_meeting": {
                "summary": "Sprint Planning",
                "start_time": "2026-01-07T10:00:00-08:00",
            },
            "free_blocks": [],
            "stats": {"total_meetings_today": 3},
        }

        with patch.object(handler, "_get_calendar_summary", new_callable=AsyncMock) as mock_cal:
            mock_cal.return_value = mock_summary

            result = await handler.respond(greeting_intent)

            # Should show current meeting, not next (Issue #633-638 grammar-conscious formatting)
            assert "Team Standup" in result["message"]
            # Accept either "Now" or "currently" for current meeting indication
            msg = result["message"]
            assert (
                "Now" in msg or "currently" in msg.lower()
            ), f"Expected current meeting indicator, got: {msg}"

    def test_time_of_day_greeting_morning(self, handler):
        """Time-of-day greeting returns 'Good morning' before noon."""
        assert handler._get_time_of_day_greeting(6) == "Good morning"
        assert handler._get_time_of_day_greeting(8) == "Good morning"
        assert handler._get_time_of_day_greeting(11) == "Good morning"

    def test_time_of_day_greeting_afternoon(self, handler):
        """Time-of-day greeting returns 'Good afternoon' from noon to 5pm."""
        assert handler._get_time_of_day_greeting(12) == "Good afternoon"
        assert handler._get_time_of_day_greeting(14) == "Good afternoon"
        assert handler._get_time_of_day_greeting(16) == "Good afternoon"

    def test_time_of_day_greeting_evening(self, handler):
        """Time-of-day greeting returns 'Good evening' after 5pm."""
        assert handler._get_time_of_day_greeting(17) == "Good evening"
        assert handler._get_time_of_day_greeting(19) == "Good evening"
        assert handler._get_time_of_day_greeting(22) == "Good evening"

    @pytest.mark.asyncio
    async def test_non_greeting_action_rejected(self, handler):
        """#1754: the handler is greeting-only — farewell/thanks/chitchat
        branches (and the RESPONSES canned table) were deleted; the action
        gate floor-routes every non-greeting CONVERSATION action. A
        non-greeting arriving here is a gate-contract violation and raises,
        which canonical_handlers.handle converts to its honest generic
        fallback."""
        for action, message in [
            ("farewell", "Goodbye"),
            ("thanks", "Thank you"),
            ("chitchat", "How are you?"),
        ]:
            intent = Intent(
                category=IntentCategory.CONVERSATION,
                action=action,
                confidence=0.95,
                original_message=message,
            )
            with pytest.raises(ValueError, match="non-greeting action"):
                await handler.respond(intent)
