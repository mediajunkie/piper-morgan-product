"""#1425 (F2) — status/agenda handlers must not assert emptiness when the source FAILED.

The false-claim family: a swallowed source error rendered as "there is nothing"
(about the user's own work) instead of "I couldn't check." The fix distinguishes
source-FAILED from source-EMPTY and degrades honestly (ADR-060 / #1331 / #1414 model).

This file grows one class per handler as #1425 is fixed. Handler 1
(_get_priority_metadata → _format_detailed_priorities) landed first; handlers
2-5 (agenda todos, retrospective, status-report count, reminders double-swallow)
use the None sentinel: fetch helpers return None on failure — [] / 0 stays
reserved for genuinely-empty — and every formatter renders honest "couldn't
check" copy for None while keeping its existing empty-state copy.
"""

from datetime import datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from services.intent_service.canonical_handlers import CanonicalHandlers

TARGET_DATE = datetime(2026, 7, 15, 12, 0, 0)


class TestPriorityMetadataSourceFailed:
    """_get_priority_metadata swallow → _format_detailed_priorities render."""

    def _render(self, priority_metadata):
        return CanonicalHandlers()._format_detailed_priorities(
            priorities=["Ship the beta"],  # non-empty so we reach the metadata branch
            user_context=type("U", (), {"organization": None})(),
            priority_metadata=priority_metadata,
        )

    def test_source_failed_renders_honest_not_false_empty(self):
        """The load-bearing assertion: on source failure, be honest — never claim
        'no high-priority issues found' (which would be false while P0/P1s exist)."""
        out = self._render({"has_github": True, "high_priority_issues": [], "source_failed": True})
        assert "couldn't check" in out.lower()
        assert "No high-priority" not in out  # the false-claim must NOT appear

    def test_genuine_empty_still_says_none_found(self):
        """A real empty (source OK, no P0/P1s) keeps the honest 'none found' claim."""
        out = self._render({"has_github": True, "high_priority_issues": []})
        assert "No high-priority" in out
        assert "couldn't check" not in out.lower()

    def test_populated_still_lists_issues(self):
        """The happy path is unchanged — real issues still render."""
        out = self._render({
            "has_github": True,
            "high_priority_issues": [{"number": 107, "title": "Fix login", "labels": ["P0"]}],
        })
        assert "#107" in out
        assert "couldn't check" not in out.lower()
        assert "No high-priority" not in out


class TestAgendaTodosSourceFailed:
    """Handler 2: _get_todays_todos (None sentinel) → agenda formatters."""

    def test_standard_failure_never_claims_no_pending(self):
        msg = CanonicalHandlers()._format_agenda_standard(None, None, [])
        assert "No pending tasks" not in msg
        assert "couldn't check" in msg.lower()

    def test_standard_genuine_empty_keeps_copy(self):
        msg = CanonicalHandlers()._format_agenda_standard(None, [], [])
        assert "No pending tasks" in msg

    def test_embedded_failure_vs_empty(self):
        failed = CanonicalHandlers()._format_agenda_embedded(None, None, [])
        assert "tasks unavailable" in failed
        empty = CanonicalHandlers()._format_agenda_embedded(None, [], [])
        assert "unavailable" not in empty

    def test_granular_failure_never_claims_deep_work_day(self):
        msg = CanonicalHandlers()._format_agenda_granular(None, None, [])
        assert "great day for deep work" not in msg
        assert "couldn't check" in msg.lower()
        # genuine empty keeps the upbeat copy
        empty = CanonicalHandlers()._format_agenda_granular(None, [], [])
        assert "great day for deep work" in empty


class TestRetrospectiveSourceFailed:
    """Handler 3: _get_completed_todos_for_date (None sentinel) → retrospective formatters."""

    def test_standard_failure_never_claims_momentum(self):
        msg = CanonicalHandlers()._format_retrospective_standard(None, TARGET_DATE)
        assert "No completed tasks" not in msg
        assert "Keep up the momentum" not in msg
        assert "couldn't check" in msg.lower()

    def test_standard_genuine_empty_keeps_copy(self):
        msg = CanonicalHandlers()._format_retrospective_standard([], TARGET_DATE)
        assert "No completed tasks found for yesterday" in msg

    def test_embedded_and_granular_failure(self):
        h = CanonicalHandlers()
        assert "couldn't check" in h._format_retrospective_embedded(None, TARGET_DATE).lower()
        assert "couldn't check" in h._format_retrospective_granular(None, TARGET_DATE).lower()
        assert "No completed tasks" in h._format_retrospective_embedded([], TARGET_DATE)


class TestStatusReportCountSourceFailed:
    """Handler 4: _handle_status_report todo count (None sentinel) → status formatters."""

    _HEALTH = {"healthy": 0, "at-risk": 0, "stalled": 0, "unknown": 0}

    def _report(self, todos):
        return {"total_projects": 0, "health_summary": dict(self._HEALTH), "open_todos": todos}

    def test_failure_never_claims_zero(self):
        h = CanonicalHandlers()
        for fmt in (
            h._format_status_report_embedded,
            h._format_status_report_standard,
            h._format_status_report_granular,
        ):
            msg = fmt(self._report(None))
            assert "0 open todos" not in msg and "**Open Todos**: 0" not in msg, fmt.__name__
            assert "unavailable" in msg or "couldn't check" in msg.lower(), fmt.__name__

    def test_genuine_zero_still_renders_zero(self):
        msg = CanonicalHandlers()._format_status_report_standard(self._report(0))
        assert "**Open Todos**: 0" in msg


class TestRemindersDoubleSwallow:
    """Handler 5: get_due_reminders (None sentinel) + assembler flag — the pair
    whose combined swallows silently broke the 'I'll surface this next time'
    promise."""

    async def test_get_due_reminders_failure_returns_none_not_empty(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos.side_effect = RuntimeError("db down")
        assert await h.get_due_reminders(uuid4()) is None

    async def test_reminder_context_flags_failure(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler.__new__(ContextAssembler)  # method is self-contained
        with patch(
            "services.intent_service.todo_handlers.TodoIntentHandlers.get_due_reminders",
            new=AsyncMock(return_value=None),
        ):
            ctx = await assembler._compute_reminder_context(str(uuid4()))
        assert ctx == {"source_failed": True}
