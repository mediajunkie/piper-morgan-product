"""
Unit tests for agenda query functionality in canonical_handlers.py

Tests for Issue #499 - Query #8 Agenda detection and handling.
Tests the implementation of:
- _detect_agenda_request() - Detects agenda-related queries
- _handle_agenda_query() - Handles agenda requests
- _get_todays_todos() - Gets today's todos
- _format_agenda_embedded() - Formats embedded output
- _format_agenda_standard() - Formats standard output
- _format_agenda_granular() - Formats granular output
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers


@pytest.fixture
def canonical_handlers():
    """Fixture to create CanonicalHandlers instance"""
    return CanonicalHandlers()


class TestAgendaQuery:
    """Test suite for agenda query detection and handling (Issue #499)"""

    def test_detect_agenda_request_today_agenda(self, canonical_handlers):
        """Test detection of 'agenda today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda for today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_schedule_today(self, canonical_handlers):
        """Test detection of 'schedule today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's my schedule today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_schedule",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_have_today(self, canonical_handlers):
        """Test detection of 'what do I have today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What do I have today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_todays_plan(self, canonical_handlers):
        """Test detection of 'today's plan' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="Show me today's plan",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_plan",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_planned_for_today(self, canonical_handlers):
        """Test detection of 'planned for today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's planned for today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_lined_up_today(self, canonical_handlers):
        """Test detection of 'lined up for today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's lined up for today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_coming_up_today(self, canonical_handlers):
        """Test detection of 'coming up today' pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's coming up today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is True

    def test_detect_agenda_request_returns_false_for_non_agenda(self, canonical_handlers):
        """Test that non-agenda queries return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What day is it?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_date",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is False

    def test_detect_agenda_request_returns_false_for_empty_message(self, canonical_handlers):
        """Test that empty messages return False."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="",
            category=IntentCategoryEnum.TEMPORAL,
            action="query",
            confidence=0.9,
        )

        result = canonical_handlers._detect_agenda_request(intent)
        assert result is False

    def test_detect_agenda_request_returns_false_for_none_intent(self, canonical_handlers):
        """Test that None intent returns False."""
        result = canonical_handlers._detect_agenda_request(None)
        assert result is False

    def test_format_agenda_embedded_with_meeting_and_tasks(self, canonical_handlers):
        """Test EMBEDDED format with current meeting and tasks."""
        calendar_context = {
            "current_meeting": {"title": "Team Standup", "duration": "30 min"},
        }
        todos = [
            {"title": "Review PR #123", "priority": "high", "due_date": None},
            {"title": "Update docs", "priority": "medium", "due_date": None},
        ]
        priorities = ["Complete authentication feature"]

        result = canonical_handlers._format_agenda_embedded(calendar_context, todos, priorities)

        assert "In meeting: Team Standup" in result
        assert "2 tasks" in result
        assert "Focus: Complete authentication" in result

    def test_format_agenda_embedded_with_next_meeting(self, canonical_handlers):
        """Test EMBEDDED format with next meeting."""
        calendar_context = {
            "next_meeting": {"title": "Client Review", "start_time": "2:00 PM"},
        }
        todos = []
        priorities = []

        result = canonical_handlers._format_agenda_embedded(calendar_context, todos, priorities)

        assert "Next: 2:00 PM" in result

    def test_format_agenda_embedded_no_items(self, canonical_handlers):
        """Test EMBEDDED format with no agenda items."""
        result = canonical_handlers._format_agenda_embedded(None, [], [])
        assert result == "No agenda items"

    def test_format_agenda_standard_with_full_context(self, canonical_handlers):
        """Test STANDARD format with calendar, todos, and priorities."""
        calendar_context = {
            "current_meeting": {"title": "Sprint Planning"},
            "next_meeting": {"title": "Design Review", "start_time": "3:00 PM"},
            "meeting_count": 4,
        }
        todos = [
            {"title": "Fix bug #456", "priority": "high", "due_date": None},
            {"title": "Write tests", "priority": "medium", "due_date": None},
            {"title": "Code review", "priority": "low", "due_date": None},
        ]
        priorities = ["Ship v2.0 by Friday"]

        result = canonical_handlers._format_agenda_standard(calendar_context, todos, priorities)

        assert "Here's your agenda for today:" in result
        assert "Now**: Sprint Planning" in result
        assert "Next Meeting**: Design Review at 3:00 PM" in result
        assert "Total Meetings**: 4 today" in result
        assert "Fix bug #456" in result
        assert "🔴" in result  # high priority icon
        assert "🟡" in result  # medium priority icon
        assert "Focus Priority**: Ship v2.0 by Friday" in result

    def test_format_agenda_standard_no_tasks(self, canonical_handlers):
        """Test STANDARD format with no tasks."""
        calendar_context = {"meeting_count": 2}
        todos = []
        priorities = []

        result = canonical_handlers._format_agenda_standard(calendar_context, todos, priorities)

        assert "Tasks**: No pending tasks" in result

    def test_format_agenda_standard_many_tasks(self, canonical_handlers):
        """STANDARD format lists EVERY gathered task — inverted by #1762.

        This test previously asserted ``"... and 3 more" in result``, pinning
        the very cap #1762 removes. The rendered string is the only per-turn
        record reaching next-turn context (``build_recent_history``, #1122),
        so the 6th-8th tasks were ones the assistant believed it had never
        been given — asked "what else is on my list?", it could only describe
        its own render (#1738's live failure). GatherOutcome §5b: a render cap
        may shorten what the user sees; it must never change what the system
        believes it has. Full pinning in
        ``test_render_truncation_sweep_1762.py``.
        """
        todos = [{"title": f"Task {i}", "priority": "medium", "due_date": None} for i in range(8)]

        result = canonical_handlers._format_agenda_standard(None, todos, [])

        for i in range(8):
            assert f"Task {i}" in result
        assert "more" not in result

    def test_format_agenda_granular_with_all_details(self, canonical_handlers):
        """Test GRANULAR format with full calendar and task details."""
        calendar_context = {
            "current_meeting": {"title": "Team Sync", "duration": "45 min"},
            "next_meeting": {"title": "1:1 Meeting", "start_time": "4:00 PM"},
            "free_blocks": [
                {"duration_minutes": 90, "start": "10:00 AM"},
                {"duration_minutes": 60, "start": "2:00 PM"},
            ],
            "meeting_count": 5,
            "meeting_hours": 3.5,
        }
        todos = [
            {"title": "Deploy to staging", "priority": "high", "due_date": None},
            {"title": "Review analytics", "priority": "medium", "due_date": None},
            {"title": "Update roadmap", "priority": "low", "due_date": None},
        ]
        priorities = ["Launch feature X", "Fix critical bugs"]

        result = canonical_handlers._format_agenda_granular(calendar_context, todos, priorities)

        assert "# Today's Full Agenda" in result
        assert "## 📅 Calendar" in result
        assert "Currently In**: Team Sync" in result
        assert "Duration: 45 min" in result
        assert "Next Up**: 1:1 Meeting" in result
        assert "Time: 4:00 PM" in result
        assert "Focus Time Available**:" in result
        assert "90 min at 10:00 AM" in result
        assert "Meeting Load**: 5 meetings (3.5 hours)" in result
        assert "## ✅ Tasks" in result
        assert "High Priority**:" in result
        assert "Deploy to staging" in result
        assert "Total**: 3 pending tasks" in result
        assert "## 🎯 Priorities" in result
        assert "Launch feature X" in result
        assert "Fix critical bugs" in result

    def test_format_agenda_granular_no_tasks(self, canonical_handlers):
        """Test GRANULAR format with no tasks."""
        result = canonical_handlers._format_agenda_granular(None, [], [])

        assert "No pending tasks - great day for deep work!" in result

    def test_format_agenda_granular_no_priorities(self, canonical_handlers):
        """Test GRANULAR format with no priorities."""
        result = canonical_handlers._format_agenda_granular(None, [], [])

        assert "No priorities configured" in result

    @pytest.mark.asyncio
    async def test_handle_agenda_query_returns_correct_structure(self, canonical_handlers):
        """Test handler returns expected response structure."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        with patch(
            "services.intent_service.canonical_handlers.CanonicalHandlers._get_calendar_context",
            return_value=None,
        ):
            with patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                # #1776: the gather returns (todos, total_pending) — the
                # pre-LIMIT row count rides beside the capped page so no
                # formatter counts its own input and calls it a total.
                return_value=([], 0),
            ):
                result = await canonical_handlers._handle_agenda_query(intent, "test_session")

        # Assert structure
        assert "message" in result
        assert "intent" in result
        assert result["intent"]["category"] == "temporal"
        assert result["intent"]["action"] == "provide_agenda"
        assert result["intent"]["confidence"] == 1.0
        assert "context" in result["intent"]
        assert "todo_count" in result["intent"]["context"]
        assert "has_calendar" in result["intent"]["context"]
        assert "has_priorities" in result["intent"]["context"]
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_handle_agenda_query_respects_spatial_pattern_embedded(self, canonical_handlers):
        """Test handler uses EMBEDDED format for embedded spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "EMBEDDED"}

        with patch(
            "services.intent_service.canonical_handlers.CanonicalHandlers._get_calendar_context",
            return_value=None,
        ):
            with patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                # #1776: the gather returns (todos, total_pending) — the
                # pre-LIMIT row count rides beside the capped page so no
                # formatter counts its own input and calls it a total.
                return_value=([], 0),
            ):
                result = await canonical_handlers._handle_agenda_query(intent, "test_session")

        # Should use brief embedded format
        assert result["spatial_pattern"] == "EMBEDDED"
        assert result["message"] == "No agenda items" or len(result["message"]) < 100

    @pytest.mark.asyncio
    async def test_handle_agenda_query_respects_spatial_pattern_granular(self, canonical_handlers):
        """Test handler uses GRANULAR format for granular spatial pattern."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        with patch(
            "services.intent_service.canonical_handlers.CanonicalHandlers._get_calendar_context",
            return_value=None,
        ):
            with patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                # #1776: the gather returns (todos, total_pending) — the
                # pre-LIMIT row count rides beside the capped page so no
                # formatter counts its own input and calls it a total.
                return_value=([], 0),
            ):
                result = await canonical_handlers._handle_agenda_query(intent, "test_session")

        # Should use detailed granular format
        assert result["spatial_pattern"] == "GRANULAR"
        assert "# Today's Full Agenda" in result["message"]

    @pytest.mark.asyncio
    async def test_handle_agenda_query_uses_standard_format_by_default(self, canonical_handlers):
        """Test handler uses STANDARD format when no spatial pattern is set."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="What's on the agenda today?",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_agenda",
            confidence=0.9,
        )

        with patch(
            "services.intent_service.canonical_handlers.CanonicalHandlers._get_calendar_context",
            return_value=None,
        ):
            with patch(
                "services.intent_service.canonical_handlers.CanonicalHandlers._get_todays_todos",
                # #1776: the gather returns (todos, total_pending) — the
                # pre-LIMIT row count rides beside the capped page so no
                # formatter counts its own input and calls it a total.
                return_value=([], 0),
            ):
                result = await canonical_handlers._handle_agenda_query(intent, "test_session")

        # Should use standard format
        assert "Here's your agenda for today:" in result["message"]
        assert result["spatial_pattern"] is None
