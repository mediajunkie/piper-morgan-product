"""
Tests for ContextAssembler (#951 + #950 iteration).

Covers:
- _compute_deadline_proximity pure helper (Phase 1 of #951)
- _gather_calendar_context wiring + failure path (Phase 3 of #951)
- pending_todos due_date / deadline_proximity surfacing (Phase 2 of #951)
- _gather_identity_context user-anchoring data (#950 iteration)
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import (
    ContextAssembler,
    _compute_deadline_proximity,
)

# -------------------------------------------------------------------
# Phase 1: _compute_deadline_proximity helper
# -------------------------------------------------------------------


class TestComputeDeadlineProximity:
    """Pure function; covers all 5 buckets + None + edge cases."""

    def test_none_returns_none_bucket(self):
        assert _compute_deadline_proximity(None) == "none"

    def test_past_due_date_returns_overdue(self):
        past = datetime.now() - timedelta(hours=1)
        assert _compute_deadline_proximity(past) == "overdue"

    def test_past_days_returns_overdue(self):
        past = datetime.now() - timedelta(days=5)
        assert _compute_deadline_proximity(past) == "overdue"

    def test_today_returns_due_today(self):
        # Due later today (but not right now)
        today = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
        assert _compute_deadline_proximity(today) == "due_today"

    def test_exactly_now_is_due_today(self):
        # Boundary: due_date == now should be "due_today" (not overdue)
        # Allow a small slack since datetime.now() is called inside the function
        now = datetime.now() + timedelta(microseconds=500)
        assert _compute_deadline_proximity(now) == "due_today"

    def test_tomorrow_returns_due_this_week(self):
        tomorrow = datetime.now() + timedelta(days=1)
        assert _compute_deadline_proximity(tomorrow) == "due_this_week"

    def test_in_six_days_returns_due_this_week(self):
        in_six = datetime.now() + timedelta(days=6)
        assert _compute_deadline_proximity(in_six) == "due_this_week"

    def test_in_eight_days_returns_later(self):
        in_eight = datetime.now() + timedelta(days=8)
        assert _compute_deadline_proximity(in_eight) == "later"

    def test_in_one_month_returns_later(self):
        in_month = datetime.now() + timedelta(days=30)
        assert _compute_deadline_proximity(in_month) == "later"


# -------------------------------------------------------------------
# Phase 3: _gather_calendar_context — calendar wiring
# -------------------------------------------------------------------


class TestGatherCalendarContext:
    """Calendar assembly via CalendarIntegrationRouter."""

    @pytest.mark.asyncio
    async def test_calendar_available_returns_mapped_fields(self):
        """When router returns a temporal summary, assembler maps to formatter schema."""
        summary = {
            "next_meeting": {"title": "CXO 1:1", "start": "2026-04-16T14:00:00"},
            "free_blocks": [
                {"start": "2026-04-16T15:00:00", "duration_minutes": 90},
            ],
            "time_available_minutes": 30,
        }
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(return_value=summary)

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert "calendar" in result
        cal = result["calendar"]
        assert cal["next_meeting"]["title"] == "CXO 1:1"
        assert cal["next_meeting"]["start"] == "2026-04-16T14:00:00"
        assert cal["next_free_block"]["start"] == "2026-04-16T15:00:00"
        assert cal["next_free_block"]["duration_minutes"] == 90
        assert cal["time_available_minutes"] == 30

    @pytest.mark.asyncio
    async def test_calendar_unavailable_returns_empty(self):
        """When router raises, assembler returns empty dict — no exception, no calendar key."""
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(
            side_effect=RuntimeError("No calendar integration available")
        )

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert result == {}
        assert "calendar" not in result

    @pytest.mark.asyncio
    async def test_calendar_no_user_id_returns_empty(self):
        """Without user_id, can't do timezone-aware calendar query — skip gracefully."""
        assembler = ContextAssembler()
        result = await assembler._gather_calendar_context(user_id=None)
        assert result == {}

    @pytest.mark.asyncio
    async def test_calendar_partial_summary_handled(self):
        """If router returns summary without free_blocks, time_available_minutes absent."""
        summary = {
            "next_meeting": {"title": "Standup", "start": "2026-04-16T09:00:00"},
            "free_blocks": [],
            "time_available_minutes": None,
        }
        mock_router = MagicMock()
        mock_router.get_temporal_summary = AsyncMock(return_value=summary)

        assembler = ContextAssembler()
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=mock_router,
        ):
            result = await assembler._gather_calendar_context(user_id="test-user")

        assert "calendar" in result
        assert result["calendar"]["next_meeting"]["title"] == "Standup"
        assert "next_free_block" not in result["calendar"]  # empty list → no field


# -------------------------------------------------------------------
# Phase 2: pending_todos due_date / deadline_proximity surfacing
# -------------------------------------------------------------------


class TestPendingTodosDeadlineSurfacing:
    """pending_todos entries should include due_date and deadline_proximity."""

    @pytest.mark.asyncio
    async def test_temporal_gatherer_surfaces_due_date(self):
        """_gather_temporal_context pending_todos include due_date + deadline_proximity."""
        due_today = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
        due_next_week = datetime.now() + timedelta(days=10)

        mock_todos = [
            _make_mock_todo(text="M2c gameplan review", due_date=due_today, priority="high"),
            _make_mock_todo(text="Archive old logs", due_date=due_next_week, priority="low"),
            _make_mock_todo(text="No deadline task", due_date=None, priority="medium"),
        ]

        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=mock_todos)

        from uuid import uuid4

        user_id = str(uuid4())
        assembler = ContextAssembler()

        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            # Also patch the projects / session / history bits to avoid DB calls
            with patch("services.database.session_factory.AsyncSessionFactory"):
                with patch("services.intent_service.conversation_context.get_or_create_context"):
                    # Skip calendar for this test (Phase 2 focus)
                    with patch.object(
                        assembler, "_gather_calendar_context", AsyncMock(return_value={})
                    ):
                        result = await assembler._gather_temporal_context(
                            user_id=user_id, session_id="s1"
                        )

        assert "pending_todos" in result
        todos = result["pending_todos"]
        assert len(todos) == 3

        # First todo: due_today
        assert todos[0]["text"] == "M2c gameplan review"
        assert todos[0]["deadline_proximity"] == "due_today"
        assert todos[0]["due_date"] is not None
        # ISO-format string expected
        assert "T" in todos[0]["due_date"] or ":" in todos[0]["due_date"]

        # Second todo: due_this_week or later
        assert todos[1]["deadline_proximity"] in ("due_this_week", "later")

        # Third todo: no deadline
        assert todos[2]["deadline_proximity"] == "none"
        assert todos[2]["due_date"] is None


# -------------------------------------------------------------------
# #950 iteration: _gather_identity_context user-anchoring
# -------------------------------------------------------------------


class TestIdentityContextUserAnchoring:
    """Identity context should include user-anchoring data, not just capabilities."""

    @pytest.mark.asyncio
    async def test_identity_context_includes_user_projects_when_available(self):
        """When user_context_service returns projects, they appear in identity context."""
        mock_user_ctx = MagicMock()
        mock_user_ctx.projects = ["piper-morgan", "klatch"]
        mock_user_ctx.priorities = None
        mock_user_ctx.organization = None

        assembler = ContextAssembler()
        # Short-circuit the workflow dispatcher / plugin registry paths to keep
        # the test focused on user-anchoring
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch("services.user_context_service.user_context_service") as mock_svc:
                    mock_svc.get_user_context = AsyncMock(return_value=mock_user_ctx)
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        assert "user_projects" in result, f"Expected user_projects in {list(result.keys())}"
        assert result["user_projects"] == ["piper-morgan", "klatch"]

    @pytest.mark.asyncio
    async def test_identity_context_includes_recent_topics_when_available(self):
        """When conversation_context has recent turns, topics appear in identity context."""
        from services.intent_service.context_assembler import ContextAssembler

        mock_turn1 = MagicMock()
        mock_turn1.message = "I'm working on the floor prompt"
        mock_turn2 = MagicMock()
        mock_turn2.message = "Let's improve the canonical retest"

        mock_conv_ctx = MagicMock()
        mock_conv_ctx.turns = [mock_turn1, mock_turn2]

        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch(
                    "services.intent_service.conversation_context.get_or_create_context",
                    return_value=mock_conv_ctx,
                ):
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        assert "recent_topics" in result, f"Expected recent_topics in {list(result.keys())}"
        assert len(result["recent_topics"]) == 2
        assert "floor prompt" in result["recent_topics"][0]

    @pytest.mark.asyncio
    async def test_identity_context_no_user_id_skips_anchoring(self):
        """Without user_id, user-anchoring fields are absent (no exception)."""
        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                result = await assembler._gather_identity_context(user_id=None, session_id=None)

        # Capabilities + integrations still there; user-anchoring absent
        assert "capabilities" in result
        assert "user_projects" not in result
        assert "recent_topics" not in result

    @pytest.mark.asyncio
    async def test_identity_context_user_service_failure_is_graceful(self):
        """user_context_service raising doesn't break identity context assembly."""
        assembler = ContextAssembler()
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            with patch("services.plugins.get_plugin_registry") as mock_registry:
                mock_registry.return_value.get_status_all.return_value = {}
                with patch("services.user_context_service.user_context_service") as mock_svc:
                    mock_svc.get_user_context = AsyncMock(side_effect=RuntimeError("db down"))
                    # Should not raise
                    result = await assembler._gather_identity_context(
                        user_id="test-user", session_id="s1"
                    )

        # Capabilities still gathered; user-anchoring absent (not fabricated)
        assert "capabilities" in result
        assert "user_projects" not in result


# -------------------------------------------------------------------
# Issue #1057: UNKNOWN-fallback + context_contract_empty_data warning
#
# Backfills coverage for the f2408df6 commit (#960/#961 context contract).
# Architect's soundness review 2026-05-04 flagged that commit as item 4 of
# 5 cleanup items (no-tests on a contract path). This block adds the 4
# tests called out in the issue body:
#   1. UNKNOWN with user_id → falls through to status_priority context
#   2. UNKNOWN without user_id → returns empty cleanly (no exception)
#   3. TEMPORAL/STATUS/PRIORITY with no data → emits warning
#   4. TEMPORAL/STATUS/PRIORITY with data → does NOT emit warning
# -------------------------------------------------------------------


class TestUnknownCategoryFallback:
    """#1057 / #960: UNKNOWN routes through status_priority gatherer."""

    @pytest.mark.asyncio
    async def test_unknown_with_user_id_falls_through_to_status_priority(self):
        """UNKNOWN category + user_id → context populated with status_priority data."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(return_value={
                "pending_todos": [{"text": "ship the thing"}],
                "completed_todos": [],
                "projects": ["alpha"],
                "priorities": [],
            }),
        ) as mock_gather:
            result = await assembler.gather_context(
                intent_category="UNKNOWN",
                user_id="test-user",
                session_id="s1",
            )
            mock_gather.assert_called_once_with("test-user")
            assert "pending_todos" in result
            assert result["pending_todos"] == [{"text": "ship the thing"}]
            assert "projects" in result
            assert result["projects"] == ["alpha"]

    @pytest.mark.asyncio
    async def test_unknown_without_user_id_returns_minimal_context(self):
        """UNKNOWN + user_id=None → no fallback gather, returns only current_time."""
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(),
        ) as mock_gather:
            result = await assembler.gather_context(
                intent_category="UNKNOWN",
                user_id=None,
                session_id="s1",
            )
            mock_gather.assert_not_called()
            # current_time is always set; nothing else for a userless UNKNOWN
            assert "current_time" in result
            assert "pending_todos" not in result
            assert "projects" not in result


class TestContextContractEmptyDataWarning:
    """#1057 / #960: empty-data warning for TEMPORAL/STATUS/PRIORITY.

    structlog doesn't route through stdlib logging cleanly in this codebase,
    so we patch the module-level `logger.warning` directly to capture calls.
    """

    @pytest.mark.asyncio
    async def test_empty_data_warning_emitted_when_no_keys(self):
        """STATUS reaches floor with no data keys → context_contract_empty_data fires."""
        from services.intent_service import context_assembler as ca_module
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(return_value={}),  # gather returns empty
        ), patch.object(ca_module.logger, "warning") as mock_warn:
            await assembler.gather_context(
                intent_category="STATUS",
                user_id="test-user",
                session_id="s1",
            )
        # First positional arg of structlog .warning() is the event name
        events = [call.args[0] for call in mock_warn.call_args_list if call.args]
        assert "context_contract_empty_data" in events, (
            f"Expected context_contract_empty_data warning; got: {events}"
        )

    @pytest.mark.asyncio
    async def test_empty_data_warning_NOT_emitted_when_data_present(self):
        """STATUS reaches floor WITH data keys → no warning."""
        from services.intent_service import context_assembler as ca_module
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            new=AsyncMock(return_value={
                "pending_todos": [{"text": "x"}],
                "projects": ["alpha"],
            }),
        ), patch.object(ca_module.logger, "warning") as mock_warn:
            await assembler.gather_context(
                intent_category="STATUS",
                user_id="test-user",
                session_id="s1",
            )
        events = [call.args[0] for call in mock_warn.call_args_list if call.args]
        assert "context_contract_empty_data" not in events, (
            f"Did not expect empty-data warning; got: {events}"
        )


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------


def _make_mock_todo(text, due_date=None, priority="medium", completed=False):
    """Construct a mock Todo-like object for tests."""
    t = MagicMock()
    t.text = text
    t.due_date = due_date
    t.priority = priority
    t.completed = completed
    t.completed_at = None
    return t
