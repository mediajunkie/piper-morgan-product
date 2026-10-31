"""#2233: a due reminder reaches the user unasked only via code, after the answer, on a
declared op set, once per todo id per principal's session."""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.intent_service import conversation_context as cc
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.due_reminder_line import (
    _when,
    due_reminder_line,
    render_due_reminder_line,
)
from services.intent_service.workflow_dispatcher import (
    DUE_REMINDER_LINE_OPS,
    DUE_REMINDER_SELF_RENDERING_OPS,
)

TZ = "America/Los_Angeles"
U1, U2 = str(uuid4()), str(uuid4())


def _row(text="file the report", when=None):
    return SimpleNamespace(
        id=uuid4(),
        text=text,
        reminder_date=when or datetime(2026, 10, 29, 20, 0, tzinfo=timezone.utc),
    )


def _ok():
    return SimpleNamespace(success=True, requires_clarification=False, error=None, error_type=None)


@pytest.fixture(autouse=True)
def _clean():
    cc._conversation_contexts.clear()
    yield
    cc._conversation_contexts.clear()


def _patch(rows):
    return (
        patch(
            "services.intent_service.todo_handlers.TodoIntentHandlers.get_due_reminder_rows",
            AsyncMock(return_value=rows),
        ),
        patch("services.utils.datetime_utils.user_timezone_name", AsyncMock(return_value=TZ)),
    )


async def _line(action, rows, user=U1, session="s1", result=None):
    a, b = _patch(rows)
    with a, b:
        return await due_reminder_line(
            action=action, result=result or _ok(), user_id=user, session_id=session
        )


def test_declared_set_is_pinned():
    assert DUE_REMINDER_LINE_OPS == {
        "get_standup",
        "list_todos_query",
        "list_reminders_query",
        "greeting",
    }
    assert DUE_REMINDER_SELF_RENDERING_OPS <= DUE_REMINDER_LINE_OPS
    for banned in ("get_identity", "get_capabilities"):
        assert banned not in DUE_REMINDER_LINE_OPS


class TestEligibility:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "op", ["get_identity", "get_capabilities", "get_weather", "explain_trust"]
    )
    async def test_op_outside_the_set_gets_no_line(self, op):
        assert await _line(op, [_row()]) is None

    @pytest.mark.asyncio
    async def test_q1_name_question_answers_and_stops(self):
        assert await _line("get_identity", [_row()]) is None

    @pytest.mark.asyncio
    async def test_op_in_the_set_renders_the_line(self):
        out = await _line("list_todos_query", [_row()])
        assert out.startswith('Reminder: "file the report" came due ')

    @pytest.mark.asyncio
    async def test_greeting_is_in_the_set(self):
        assert await _line("greeting", [_row()])

    @pytest.mark.asyncio
    async def test_anonymous_turn_gets_no_line(self):
        assert await _line("greeting", [_row()], user=None) is None

    @pytest.mark.asyncio
    async def test_declines_errors_and_clarifications_get_none(self):
        for r in (
            SimpleNamespace(
                success=False, requires_clarification=False, error=None, error_type=None
            ),
            SimpleNamespace(success=True, requires_clarification=True, error=None, error_type=None),
            SimpleNamespace(success=True, requires_clarification=False, error="x", error_type=None),
            SimpleNamespace(success=True, requires_clarification=False, error=None, error_type="e"),
        ):
            assert await _line("greeting", [_row()], result=r) is None


class TestOncePerTodoPerPrincipalSession:
    @pytest.mark.asyncio
    async def test_second_eligible_turn_does_not_repeat_the_id(self):
        rows = [_row()]
        assert await _line("greeting", rows)
        assert await _line("list_todos_query", rows) is None
        new = _row("call the vendor")
        out = await _line("greeting", rows + [new])
        assert "call the vendor" in out and "file the report" not in out

    @pytest.mark.asyncio
    async def test_different_principal_same_session_starts_empty(self):
        rows = [_row()]
        assert await _line("greeting", rows, user=U1, session="shared")
        assert await _line("greeting", rows, user=U2, session="shared")

    @pytest.mark.asyncio
    async def test_failed_read_gives_no_line_and_logs(self):
        with patch("services.intent_service.due_reminder_line.logger") as log:
            assert await _line("greeting", None) is None
        log.warning.assert_called()

    @pytest.mark.asyncio
    async def test_standup_marks_surfaced_and_adds_no_line(self):
        rows = [_row()]
        assert await _line("get_standup", rows) is None
        assert await _line("greeting", rows) is None  # no duplicate later either

    @pytest.mark.asyncio
    async def test_reminder_list_turn_adds_no_second_mention(self):
        assert await _line("list_reminders_query", [_row()]) is None


class TestModelNeverSeesDueReminders:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "cat,action",
        [("IDENTITY", "get_identity"), ("QUERY", "list_todos_query"), ("CONVERSATION", "greeting")],
    )
    async def test_outside_reminder_list_no_due_reminders_in_context(self, cat, action):
        asm = ContextAssembler()
        asm._gather_reminder_context = AsyncMock(
            return_value={"due_reminders": ["x"], "reminder_count": 1}
        )
        ctx = await asm.gather_context(cat, user_id=U1, session_id="s", intent_action=action)
        assert "due_reminders" not in ctx and "source_failed" not in ctx
        asm._gather_reminder_context.assert_not_called()

    @pytest.mark.asyncio
    async def test_reminder_list_op_still_gets_them(self):
        asm = ContextAssembler()
        asm._gather_reminder_context = AsyncMock(
            return_value={"due_reminders": ["x"], "reminder_count": 1}
        )
        ctx = await asm.gather_context(
            "QUERY", user_id=U1, session_id="s", intent_action="list_reminders_query"
        )
        assert ctx.get("due_reminders") == ["x"]


class TestWording:
    def test_three_forms(self):
        d = datetime(2026, 10, 1, 20, 0, tzinfo=timezone.utc)
        one = render_due_reminder_line([_row("A", d)], TZ)
        assert one == 'Reminder: "A" came due Oct 1.'
        two = render_due_reminder_line([_row("A", d), _row("B", d)], TZ)
        assert two == 'Reminders that came due: "A" (Oct 1), "B" (Oct 1).'
        five = render_due_reminder_line([_row(c, d) for c in "ABCDE"], TZ)
        assert five == 'Reminders that came due: "A" (Oct 1), "B" (Oct 1), "C" (Oct 1), and 2 more.'
        for text in (one, two, five):
            assert "overdue" not in text.lower()

    def test_time_is_in_the_users_zone_not_utc(self):
        fixed = datetime(2026, 10, 30, 18, 0, tzinfo=timezone.utc)  # 11:00 AM PDT, Oct 30
        with patch(
            "services.utils.datetime_utils.now_in_zone",
            lambda tz: fixed.astimezone(__import__("zoneinfo").ZoneInfo(tz)),
        ):
            # yesterday in UTC (Oct 29 23:30Z is 4:30 PM PDT Oct 29): date, not "today"
            assert _when(datetime(2026, 10, 29, 23, 30, tzinfo=timezone.utc), TZ) == "Oct 29"
            # 2026-10-30 02:00Z is 7:00 PM PDT Oct 29 -> date although UTC-today
            assert _when(datetime(2026, 10, 30, 2, 0, tzinfo=timezone.utc), TZ) == "Oct 29"
            # 2026-10-30 16:00Z is 9:00 AM PDT Oct 30 -> today
            assert (
                _when(datetime(2026, 10, 30, 16, 0, tzinfo=timezone.utc), TZ)
                == "today at 9:00 AM PDT"
            )
        # yesterday UTC but today in the user's zone (Auckland): 2026-10-29 20:00Z = Oct 30 9:00 AM NZDT
        akl = "Pacific/Auckland"
        fixed2 = datetime(2026, 10, 30, 1, 0, tzinfo=timezone.utc)
        with patch(
            "services.utils.datetime_utils.now_in_zone",
            lambda tz: fixed2.astimezone(__import__("zoneinfo").ZoneInfo(tz)),
        ):
            assert (
                _when(datetime(2026, 10, 29, 20, 0, tzinfo=timezone.utc), akl)
                == "today at 9:00 AM NZDT"
            )
