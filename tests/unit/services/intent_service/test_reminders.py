"""
Tests for Issue #903: Basic Reminder System

Covers:
- Pre-classifier reminder patterns
- Reminder time parsing (natural language → datetime)
- Reminder text extraction (strip command phrases)
- Reminder handler creates time-annotated todo
- Context assembler surfaces due reminders
"""

import re
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.temporal_utils import parse_reminder_time

# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestReminderPreClassifierPatterns:
    """Issue #903: Verify reminder patterns classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "remind me to review PRs tomorrow",
            "remind me about the standup meeting",
            "set a reminder to check deployment",
            "set reminder for team sync",
            "create a reminder to update the docs",
            "don't let me forget to submit the report",
            "I need to remember to call the vendor",
        ],
    )
    def test_reminder_patterns_match(self, message):
        result = PreClassifier._matches_patterns(message.lower(), PreClassifier.REMINDER_PATTERNS)
        assert result is True, f"Pattern should match: {message}"

    @pytest.mark.parametrize(
        "message",
        [
            "show my todos",
            "what's the weather tomorrow",
            "add todo: review PRs",
            "close issue #123",
        ],
    )
    def test_non_reminder_messages_do_not_match(self, message):
        result = PreClassifier._matches_patterns(message.lower(), PreClassifier.REMINDER_PATTERNS)
        assert result is False, f"Pattern should NOT match: {message}"


# ---------------------------------------------------------------------------
# Time parsing tests
# ---------------------------------------------------------------------------


class TestParseReminderTime:
    """Issue #903: Natural language time parsing for reminders."""

    def test_in_minutes(self):
        dt, label = parse_reminder_time("remind me in 30 minutes")
        assert dt is not None
        assert "30 minute" in label
        # Should be roughly 30 minutes from now
        # #1493: dt is now AWARE local; compare aware-to-aware
        expected = datetime.now().astimezone() + timedelta(minutes=30)
        assert abs((dt - expected).total_seconds()) < 5

    def test_in_hours(self):
        dt, label = parse_reminder_time("remind me in 2 hours")
        assert dt is not None
        assert "2 hour" in label
        expected = datetime.now().astimezone() + timedelta(hours=2)
        assert abs((dt - expected).total_seconds()) < 5

    def test_in_days(self):
        dt, label = parse_reminder_time("remind me in 3 days")
        assert dt is not None
        assert "3 day" in label
        expected = datetime.now().astimezone() + timedelta(days=3)
        assert abs((dt - expected).total_seconds()) < 5

    def test_tomorrow_default_morning(self):
        dt, label = parse_reminder_time("remind me tomorrow")
        assert dt is not None
        assert "tomorrow" in label
        tomorrow = datetime.now() + timedelta(days=1)
        assert dt.day == tomorrow.day
        assert dt.hour == 9  # Default morning

    def test_tomorrow_afternoon(self):
        dt, label = parse_reminder_time("remind me tomorrow afternoon")
        assert dt is not None
        assert "afternoon" in label
        assert dt.hour == 14

    def test_tomorrow_at_specific_time(self):
        dt, label = parse_reminder_time("remind me tomorrow at 3pm")
        assert dt is not None
        tomorrow = datetime.now() + timedelta(days=1)
        assert dt.day == tomorrow.day
        assert dt.hour == 15

    def test_next_week(self):
        dt, label = parse_reminder_time("remind me next week")
        assert dt is not None
        assert "next week" in label
        assert dt.hour == 9  # Default morning
        # Should be at least 1 day ahead (next Monday), at most 8
        diff = dt - datetime.now().astimezone()  # #1493: aware-to-aware
        hours_ahead = diff.total_seconds() / 3600
        assert hours_ahead > 0  # Must be in the future

    def test_day_name(self):
        dt, label = parse_reminder_time("remind me next Monday")
        assert dt is not None
        assert "Monday" in label
        assert dt.weekday() == 0  # Monday

    def test_fallback_to_tomorrow(self):
        """When no time is detected, default to tomorrow morning."""
        dt, label = parse_reminder_time("remind me to do something")
        assert dt is not None
        assert "tomorrow" in label
        assert dt.hour == 9


class TestReminderTimeLabelNoDoubledTokens:
    """Issue #1490: confirmation copy printed 'tomorrow at at 3pm' (doubled 'at').

    The label f-strings prepended 'at ' to a match fragment that already
    contained 'at'. Pin the exact labels and assert no doubled tokens.
    """

    def test_tomorrow_at_label_no_double_at(self):
        dt, label = parse_reminder_time("remind me tomorrow at 3pm to review the PR")
        assert dt is not None
        assert label == "tomorrow at 3pm"

    def test_tomorrow_at_label_without_at_keyword(self):
        """'tomorrow 3pm' (no 'at' in message) still labels as 'tomorrow at 3pm'."""
        dt, label = parse_reminder_time("remind me tomorrow 3pm to review the PR")
        assert dt is not None
        assert label == "tomorrow at 3pm"

    def test_at_time_label_no_double_at(self):
        dt, label = parse_reminder_time("remind me at 5pm to send the update")
        assert dt is not None
        assert label == "at 5pm"

    def test_today_at_time_label_no_double_at(self, monkeypatch):
        # #1562: "today" now has its own branch and label ("today at 4pm").
        # Frozen before 4pm so the binding is deterministic (an explicit
        # "today" + past time returns the honest-ask shape, not a roll).
        import services.intent_service.temporal_utils as tu

        class _Frozen(datetime):
            @classmethod
            def now(cls, tz=None):
                frozen = datetime(2026, 8, 10, 10, 0)
                return frozen if tz is None else frozen.astimezone(tz)

        monkeypatch.setattr(tu, "datetime", _Frozen)
        dt, label = parse_reminder_time("remind me today at 4pm to file the report")
        assert dt is not None
        assert dt.date() == datetime(2026, 8, 10).date()
        assert label == "today at 4pm"

    @pytest.mark.parametrize(
        "message",
        [
            "remind me tomorrow at 3pm to review the PR",
            "remind me to review PRs tomorrow at 3pm",
            "remind me at 5pm to send the update",
            "remind me today at 4pm to file the report",
            "remind me tomorrow morning",
            "remind me in 2 hours",
        ],
    )
    def test_no_doubled_tokens_in_any_label(self, message):
        """No label may contain the same word twice in a row (e.g. 'at at')."""
        _, label = parse_reminder_time(message)
        assert not re.search(r"\b(\w+)\s+\1\b", label), f"Doubled token in label: {label!r}"


# ---------------------------------------------------------------------------
# Text extraction tests
# ---------------------------------------------------------------------------


class TestReminderTextExtraction:
    """Issue #903: Extract actionable text from reminder messages."""

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    def test_remind_me_to(self):
        text = self.handlers._extract_reminder_text("remind me to review PRs")
        assert text == "review prs"

    def test_remind_me_about(self):
        text = self.handlers._extract_reminder_text("remind me about the team meeting")
        assert text == "the team meeting"

    def test_set_reminder_to(self):
        text = self.handlers._extract_reminder_text("set a reminder to deploy the fix")
        assert text == "deploy the fix"

    def test_dont_forget(self):
        text = self.handlers._extract_reminder_text("don't let me forget to submit the report")
        assert text == "submit the report"

    def test_strips_time_suffix(self):
        """Time expressions should be stripped from the todo text."""
        text = self.handlers._extract_reminder_text("remind me to review PRs tomorrow")
        assert text == "review prs"
        assert "tomorrow" not in (text or "")

    def test_strips_in_n_hours(self):
        text = self.handlers._extract_reminder_text("remind me to check the deploy in 2 hours")
        assert text == "check the deploy"

    def test_empty_after_strip(self):
        text = self.handlers._extract_reminder_text("remind me to")
        assert text is None

    def test_no_match(self):
        text = self.handlers._extract_reminder_text("show my todos")
        assert text is None


class TestReminderTextExtractionTimeFirst1490:
    """Issue #1490: 'remind me tomorrow at 3pm to review the PR' lost the WHAT slot.

    Slot extraction must handle [time-first, task-after-'to'] ordering, the
    already-working [task-first, time-after] ordering, and punctuation variants
    of both. PM's verbatim failing phrasing is the first case.
    """

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    @pytest.mark.parametrize(
        "message,expected",
        [
            # PM's verbatim failing phrasing (8/7 walkthrough)
            ("remind me tomorrow at 3pm to review the PR", "review the pr"),
            # The bot's own suggested-adjacent phrasing that worked
            ("remind me to review PRs tomorrow at 3pm", "review prs"),
            # Punctuation variants of both orderings
            ("Remind me tomorrow at 3pm to review the PR.", "review the pr"),
            ("remind me to review PRs tomorrow at 3pm.", "review prs"),
        ],
    )
    def test_both_orderings_and_punctuation_variants(self, message, expected):
        text = self.handlers._extract_reminder_text(message)
        assert text == expected

    @pytest.mark.parametrize(
        "message,expected",
        [
            # Other time expressions in time-first position
            ("remind me in 2 hours to check the deploy", "check the deploy"),
            ("remind me tomorrow to stretch", "stretch"),
            ("remind me tonight to lock the door", "lock the door"),
            ("remind me next Monday to send the invoice", "send the invoice"),
            # 'set/create a reminder' command variants, time-first
            ("set a reminder tomorrow at 9am to submit the timesheet", "submit the timesheet"),
            ("create a reminder for tomorrow to water the plants", "water the plants"),
        ],
    )
    def test_time_first_across_command_variants(self, message, expected):
        text = self.handlers._extract_reminder_text(message)
        assert text == expected

    def test_time_first_still_none_when_no_task(self):
        """Time-only messages still return None (help copy path)."""
        assert self.handlers._extract_reminder_text("remind me tomorrow at 3pm") is None

    @pytest.mark.asyncio
    async def test_handler_saves_time_first_phrasing_no_doubled_at(self):
        """PM's failing phrasing end-to-end: saves the reminder, confirmation
        copy names the task and contains no doubled 'at'."""
        from unittest.mock import AsyncMock, patch
        from uuid import uuid4

        from services.domain.models import Intent, Todo
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me tomorrow at 3pm to review the PR"},
        )
        mock_todo = Todo(
            id=str(uuid4()),
            text="review the pr",
            priority="medium",
            status="pending",
            completed=False,
        )
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert mock_create.called
        assert mock_create.call_args.kwargs.get("text") == "review the pr"
        assert mock_create.call_args.kwargs.get("reminder_date") is not None
        assert "didn't catch" not in result.lower()
        assert "review the pr" in result.lower()
        assert not re.search(
            r"\b(\w+)\s+\1\b", result.lower()
        ), f"Doubled token in confirmation copy: {result!r}"


# ---------------------------------------------------------------------------
# Handler integration test
# ---------------------------------------------------------------------------


class TestReminderHandler:
    """Issue #903: Test reminder creation handler."""

    @pytest.fixture
    def todo_handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handlers = TodoIntentHandlers()
        return handlers

    @pytest.mark.asyncio
    async def test_creates_reminder_with_time(self, todo_handlers):
        """Reminder handler should create a todo with reminder_date."""
        from services.domain.models import Intent, Todo
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me to review PRs tomorrow"},
        )

        mock_todo = Todo(
            id=str(uuid4()),
            text="review prs",
            priority="medium",
            status="pending",
            completed=False,
        )

        with patch.object(
            todo_handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await todo_handlers.handle_create_reminder(intent, "session-1", uuid4())

            assert mock_create.called
            call_kwargs = mock_create.call_args
            # Should have reminder_date set
            assert call_kwargs.kwargs.get("reminder_date") is not None
            # Response should confirm the reminder
            assert "remind you" in result.lower() or "review prs" in result.lower()

    @pytest.mark.asyncio
    async def test_reminder_with_no_text_returns_help(self, todo_handlers):
        """Missing reminder text should return helpful message."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me to"},
        )

        result = await todo_handlers.handle_create_reminder(intent, "session-1", uuid4())
        assert "didn't catch" in result.lower() or "try" in result.lower()


# ---------------------------------------------------------------------------
# Context assembler reminder surfacing
# ---------------------------------------------------------------------------


class TestReminderContextSurfacing:
    """Issue #903: Due reminders appear in conversation context."""

    @pytest.mark.asyncio
    async def test_due_reminders_in_context(self):
        """When user has due reminders, they should appear in CONVERSATION context."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()

        with patch("services.intent_service.todo_handlers.TodoIntentHandlers") as MockHandlers:
            mock_instance = MagicMock()
            mock_instance.get_due_reminders = AsyncMock(
                return_value=["review PRs", "check deployment"]
            )
            MockHandlers.return_value = mock_instance

            context = await assembler.gather_context("CONVERSATION", user_id=str(uuid4()))

            assert "due_reminders" in context
            assert len(context["due_reminders"]) == 2
            assert context["reminder_count"] == 2

    @pytest.mark.asyncio
    async def test_no_reminders_no_context(self):
        """When no reminders are due, context should be clean."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()

        with patch("services.intent_service.todo_handlers.TodoIntentHandlers") as MockHandlers:
            mock_instance = MagicMock()
            mock_instance.get_due_reminders = AsyncMock(return_value=[])
            MockHandlers.return_value = mock_instance

            context = await assembler.gather_context("CONVERSATION", user_id=str(uuid4()))

            assert "due_reminders" not in context


# ---------------------------------------------------------------------------
# Issue #1491: naive-vs-aware datetime guard in get_due_reminders
# ---------------------------------------------------------------------------


class TestDueReminderTZGuard1491:
    """Issue #1491: due-reminder fetch crashed on naive-vs-aware comparison.

    Live on v30 (2026-08-07T15:32:10Z): `datetime.now()` (naive) compared
    against `reminder_date` rows that come back tz-aware from Postgres
    timestamptz -> TypeError -> warning-swallow -> None sentinel -> saved
    reminders NEVER surface. Guard shape mirrors the #1429 standup fix:
    both sides normalized to aware-UTC at the comparison boundary.
    """

    def _handler_with_todos(self, todos):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handler = TodoIntentHandlers()
        handler.todo_service = MagicMock()
        handler.todo_service.list_todos = AsyncMock(return_value=todos)
        return handler

    @staticmethod
    def _todo(text, reminder_date, completed=False):
        from services.domain.models import Todo

        return Todo(text=text, reminder_date=reminder_date, completed=completed)

    @pytest.mark.asyncio
    async def test_naive_and_aware_rows_both_fetch_without_crash(self):
        """Regression (#1491): one AWARE row + one NAIVE row -> both fetch,
        no TypeError, due-ness computed correctly for each."""
        from datetime import timezone

        aware_past = datetime.now(timezone.utc) - timedelta(hours=1)
        naive_past = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=2)

        handler = self._handler_with_todos(
            [
                self._todo("aware reminder", aware_past),
                self._todo("naive reminder", naive_past),
            ]
        )

        due = await handler.get_due_reminders(uuid4())

        # Pre-fix: TypeError swallowed -> None sentinel. Post-fix: both due.
        assert due is not None, "fetch must not crash into the None sentinel"
        assert "aware reminder" in due
        assert "naive reminder" in due

    @pytest.mark.asyncio
    async def test_due_ness_correct_future_rows_not_due(self):
        """Future reminders (aware AND naive-UTC) are not due; past ones are."""
        from datetime import timezone

        now_utc = datetime.now(timezone.utc)
        handler = self._handler_with_todos(
            [
                self._todo("due aware", now_utc - timedelta(minutes=5)),
                self._todo("future aware", now_utc + timedelta(hours=3)),
                self._todo("future naive", now_utc.replace(tzinfo=None) + timedelta(hours=3)),
                self._todo("no reminder", None),
                self._todo("completed", now_utc - timedelta(hours=1), completed=True),
            ]
        )

        due = await handler.get_due_reminders(uuid4())

        assert due == ["due aware"]

    @pytest.mark.asyncio
    async def test_due_reminder_surfaces_end_to_end_with_aware_row(self):
        """#1491 AC: the 'I'll surface this next time you check in' promise
        works end-to-end at the handler level — a REAL TodoIntentHandlers
        (real comparison code, only the DB-backed service mocked) feeds the
        context assembler, and an aware-stored due reminder surfaces."""
        from datetime import timezone

        from services.intent_service.context_assembler import ContextAssembler

        aware_past = datetime.now(timezone.utc) - timedelta(minutes=10)
        naive_past = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=20)
        todos = [
            self._todo("submit the report", aware_past),
            self._todo("call the vendor", naive_past),
        ]

        mock_service = MagicMock()
        mock_service.list_todos = AsyncMock(return_value=todos)

        assembler = ContextAssembler()
        with patch(
            "services.intent_service.todo_handlers.TodoManagementService",
            return_value=mock_service,
        ):
            context = await assembler.gather_context("CONVERSATION", user_id=str(uuid4()))

        assert context.get("source_failed") is not True
        assert (
            "due_reminders" in context
        ), "due reminder must surface in conversation context (the #903 promise)"
        assert "submit the report" in context["due_reminders"]
        assert "call the vendor" in context["due_reminders"]
        assert context["reminder_count"] == 2

    @pytest.mark.asyncio
    async def test_fetch_failure_logs_error_with_count_context(self):
        """#1491 AC: the None sentinel stays (#1425 — assembler flags
        source_failed, never a false "no reminders due"), but the failure must
        log at ERROR level with exc_info and reminder-count context — not a
        warning-swallow (the #1423 silent-death shape). Mirrors the
        handle_list_reminders error-logging discipline."""
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handler = TodoIntentHandlers()
        handler.todo_service = MagicMock()
        handler.todo_service.list_todos = AsyncMock(side_effect=RuntimeError("db down"))

        with patch("services.intent_service.todo_handlers.logger") as mock_logger:
            result = await handler.get_due_reminders(uuid4())

        assert result is None  # sentinel preserved (#1425)
        assert (
            not mock_logger.warning.called
        ), "failure must not be warning-swallowed (#1491/#1423) — log at error level"
        assert mock_logger.error.called, "fetch failure must log at ERROR level (#1491)"
        _, kwargs = mock_logger.error.call_args
        assert "error" in kwargs
        assert kwargs.get("exc_info") is True, "error log must carry exc_info (#1423 shape)"
        assert "todo_count" in kwargs, "error must carry count context (#1491)"
        assert "reminders_considered" in kwargs, "error must carry count context (#1491)"


# ---------------------------------------------------------------------------
# Issue #1493: parsed reminder/date-range times must be timezone-aware
# ---------------------------------------------------------------------------


class TestParsedTimesAreTimezoneAware1493:
    """#1493: temporal_utils built NAIVE local datetimes that were stored to
    timestamptz `reminder_date` — internally consistent, but the stored
    instant depended on the server's tz interpretation (asyncpg treats naive
    as UTC), drifting every reminder by the UTC offset. This was the upstream
    source of the ambiguity #1491's ensure_utc guard had to absorb.

    Local-time UX semantics stay ("tomorrow at 3pm" = 3pm server-local; user
    timezones are the #747/#750 family) — but the value now CARRIES its
    offset, so storage is UTC-normalized. No wall-clock equality assertions
    here: awareness and offset only (plus delta-vs-aware-now with wide
    tolerance where the semantics are relative)."""

    def _local_offset(self):
        return datetime.now().astimezone().utcoffset()

    def test_relative_reminder_is_aware_local(self):
        dt, label = parse_reminder_time("remind me in 2 hours")
        assert dt.tzinfo is not None, (
            "parse_reminder_time returned a NAIVE datetime — stored to "
            "timestamptz it drifts by the server's UTC offset (#1493)"
        )
        assert dt.utcoffset() == self._local_offset()
        # Relative semantics: ~2h from now, compared aware-to-aware.
        delta = dt - datetime.now().astimezone()
        assert timedelta(hours=1, minutes=55) < delta <= timedelta(hours=2)

    def test_wall_clock_reminder_keeps_local_semantics_and_offset(self):
        dt, label = parse_reminder_time("remind me tomorrow at 3pm")
        assert dt.tzinfo is not None
        assert dt.utcoffset() == self._local_offset()
        assert dt.hour == 15  # 3pm LOCAL — the UX semantics are unchanged

    def test_fallback_reminder_is_aware(self):
        dt, label = parse_reminder_time("remind me to do something")
        assert dt.tzinfo is not None
        assert dt.hour == 9

    def test_parse_relative_date_range_is_aware(self):
        from services.intent_service.temporal_utils import parse_relative_date

        start, end, label = parse_relative_date("what's on today")
        for value, name in ((start, "start"), (end, "end")):
            assert value.tzinfo is not None, f"parse_relative_date {name} is naive (#1493)"
            assert value.utcoffset() == self._local_offset()
        assert end - start == timedelta(days=1)
