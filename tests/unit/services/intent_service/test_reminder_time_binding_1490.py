"""Issue #1490 (reopened after PM verification 8/8): inverted-order time binding.

PM's verification phrasing — "remind me at 3pm tomorrow to review the PR" —
DROPPED the explicit 3pm and saved the reminder at the 09:00 morning default
(prod row: reminder_date 2026-08-09 09:00; reply copy said "tomorrow morning").

Root cause: parse_reminder_time's bare-"tomorrow" branch fired before any
branch that could see "at 3pm", so the explicit time was silently replaced by
the vague-time default. The prior #1490 fix covered [time-adjacent] "tomorrow
at 3pm" only.

Covers:
- The ordering matrix (parser + slot extraction): "at 3pm tomorrow",
  "tomorrow at 3pm" (must stay green), "at 9:41 today", "today at 9:41",
  "at noon tomorrow", and "tomorrow morning" (vague time — morning default
  IS correct there).
- THE INVARIANT (its own class): a message carrying an explicit clock time
  (am/pm form, HH:MM, noon/midnight) must yield a parsed reminder carrying
  that time — never a silent default. Unbindable explicit times ("at 25:99")
  return (None, honest-echo) and the handler ASKS instead of guessing 9am.
- #1493 companion: the inverted-order path returns an AWARE local datetime
  (same offset discipline as the rest of temporal_utils).

Related-but-out-of-scope: "remind me at 9:41 today to X" ALSO failed to
ROUTE on 8/8 (pre-classifier REMINDER_PATTERNS requires to|about directly
after "remind me") — that is #1517's routing half. These tests pin that the
slot layer (extraction + parsing) handles it once routed.
"""

import re
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.intent_service.temporal_utils import parse_reminder_time


def _now_local():
    return datetime.now().astimezone()


def _tomorrow_local():
    return _now_local() + timedelta(days=1)


# ---------------------------------------------------------------------------
# Parser: ordering matrix
# ---------------------------------------------------------------------------


class TestInvertedOrderTimeParsing1490:
    """parse_reminder_time must bind an explicit clock time to the date word
    regardless of which comes first in the message."""

    def test_pm_verbatim_at_3pm_tomorrow(self):
        """PM's exact failing phrasing (8/8 verification)."""
        dt, label = parse_reminder_time("remind me at 3pm tomorrow to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (15, 0), (
            f"explicit 3pm dropped — got {dt.hour:02d}:{dt.minute:02d} "
            f"(label {label!r}); 09:00 means the morning default swallowed it"
        )
        assert dt.date() == _tomorrow_local().date()
        assert "3pm" in label
        assert "morning" not in label

    def test_tomorrow_at_3pm_stays_green(self):
        """The already-fixed adjacent ordering must not regress."""
        dt, label = parse_reminder_time("remind me tomorrow at 3pm to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (15, 0)
        assert dt.date() == _tomorrow_local().date()
        assert label == "tomorrow at 3pm"

    def test_at_941_today(self):
        dt, label = parse_reminder_time("remind me at 9:41 today to check the deploy")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 41)
        # Existing next-occurrence semantics: today, or tomorrow if already past.
        assert dt.date() in (_now_local().date(), _tomorrow_local().date())
        assert "9:41" in label

    def test_today_at_941(self):
        dt, label = parse_reminder_time("remind me today at 9:41 to check the deploy")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 41)
        assert "9:41" in label

    def test_at_noon_tomorrow(self):
        dt, label = parse_reminder_time("remind me at noon tomorrow to review the PR")
        assert dt is not None
        assert (dt.hour, dt.minute) == (12, 0), (
            f"explicit noon dropped — got {dt.hour:02d}:{dt.minute:02d} (label {label!r})"
        )
        assert dt.date() == _tomorrow_local().date()
        assert "noon" in label

    def test_tomorrow_morning_vague_default_is_correct(self):
        """'tomorrow morning' carries NO explicit clock time — the 9am
        morning default is the CORRECT behavior there, not a bug."""
        dt, label = parse_reminder_time("remind me tomorrow morning to stretch")
        assert dt is not None
        assert (dt.hour, dt.minute) == (9, 0)
        assert dt.date() == _tomorrow_local().date()
        assert label == "tomorrow morning"


# ---------------------------------------------------------------------------
# Slot extraction: ordering matrix
# ---------------------------------------------------------------------------


class TestInvertedOrderTextExtraction1490:
    """_extract_reminder_text must consume time expressions in time-first
    position and strip them in trailing position, for the same matrix."""

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    @pytest.mark.parametrize(
        "message,expected",
        [
            # PM's verbatim failing phrasing
            ("remind me at 3pm tomorrow to review the PR", "review the pr"),
            # Adjacent ordering (must stay green)
            ("remind me tomorrow at 3pm to review the PR", "review the pr"),
            # HH:MM + today, both orderings (the #1517-adjacent slot half)
            ("remind me at 9:41 today to check the deploy", "check the deploy"),
            ("remind me today at 9:41 to check the deploy", "check the deploy"),
            # noon, time-first
            ("remind me at noon tomorrow to review the PR", "review the pr"),
            # vague time, time-first (must stay green)
            ("remind me tomorrow morning to stretch", "stretch"),
        ],
    )
    def test_time_first_orderings(self, message, expected):
        assert self.handlers._extract_reminder_text(message) == expected

    @pytest.mark.parametrize(
        "message,expected",
        [
            # Trailing time expressions stripped from the todo text
            ("remind me to review the PR at 3pm tomorrow", "review the pr"),
            ("remind me to check the deploy at 9:41 today", "check the deploy"),
            ("remind me to review the PR at noon tomorrow", "review the pr"),
        ],
    )
    def test_trailing_time_stripped(self, message, expected):
        assert self.handlers._extract_reminder_text(message) == expected


# ---------------------------------------------------------------------------
# THE INVARIANT
# ---------------------------------------------------------------------------


class TestExplicitClockTimeInvariant1490:
    """If the user's message contains an explicit clock time (am/pm form,
    HH:MM, or noon/midnight), the parsed reminder MUST carry that time —
    never a silent default. If the time can't be bound, the parser returns
    (None, honest-echo) and the handler asks instead of guessing 9am."""

    @pytest.mark.parametrize(
        "message,hour,minute",
        [
            ("remind me at 3pm tomorrow to review the PR", 15, 0),
            ("remind me to review the PR at 3pm tomorrow", 15, 0),
            ("remind me tomorrow at 3pm to review the PR", 15, 0),
            ("remind me at 9:41 today to check the deploy", 9, 41),
            ("remind me today at 9:41 to check the deploy", 9, 41),
            ("remind me at noon tomorrow to submit the report", 12, 0),
            ("remind me at midnight tomorrow to run the deploy", 0, 0),
            ("remind me tomorrow at 7:15am to go for a run", 7, 15),
            ("remind me next Monday at 4pm to send the invoice", 16, 0),
            ("remind me next week at 4pm to send the invoice", 16, 0),
            ("remind me at 5pm to send the update", 17, 0),
        ],
    )
    def test_explicit_time_is_always_carried(self, message, hour, minute):
        dt, label = parse_reminder_time(message)
        assert dt is not None, (
            f"explicit clock time in {message!r} parsed to None (label {label!r})"
        )
        assert (dt.hour, dt.minute) == (hour, minute), (
            f"explicit clock time in {message!r} not carried: expected "
            f"{hour:02d}:{minute:02d}, got {dt.hour:02d}:{dt.minute:02d} "
            f"(label {label!r}) — a silent default violates the #1490 invariant"
        )

    @pytest.mark.parametrize(
        "message,echo",
        [
            # Explicit-but-unbindable times: minute > 59, am/pm hour out of
            # 1-12. Pre-fix these either crashed (ValueError from
            # .replace(hour=25)) or silently fell to a default.
            ("remind me at 25:99 tomorrow to review the PR", "25:99"),
            ("remind me at 13pm tomorrow to review the PR", "13pm"),
        ],
    )
    def test_unbindable_explicit_time_returns_none_with_honest_echo(self, message, echo):
        dt, label = parse_reminder_time(message)
        assert dt is None, (
            f"unbindable explicit time in {message!r} was guessed as {dt!r} — "
            "must return None so the handler can ask"
        )
        assert echo in label, f"label {label!r} must echo the unparsed time"

    @pytest.mark.asyncio
    async def test_handler_asks_on_unbindable_time_never_saves_default(self):
        """Handler honest path: explicit-but-unbindable time -> no todo is
        created, no 'scheduled' claim, the copy echoes the time and asks."""
        from services.domain.models import Intent
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me at 25:99 tomorrow to review the PR"},
        )
        with patch.object(
            handlers.todo_service, "create_todo", new_callable=AsyncMock
        ) as mock_create:
            result = await handlers.handle_create_reminder(intent, "session-1", uuid4())

        assert not mock_create.called, (
            "handler saved a reminder despite an unbindable explicit time — "
            "the silent-default path the #1490 invariant forbids"
        )
        assert "25:99" in result, "honest path must echo the time it couldn't parse"
        assert "scheduled" not in result.lower()
        assert "?" in result, "honest path should ask for the time"

    @pytest.mark.asyncio
    async def test_handler_saves_pm_phrasing_at_15_00_not_morning(self):
        """End-to-end for PM's verbatim phrasing: reminder_date carries 15:00
        and the confirmation copy does NOT claim 'tomorrow morning'."""
        from services.domain.models import Intent, Todo
        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.shared_types import IntentCategory

        handlers = TodoIntentHandlers()
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me at 3pm tomorrow to review the PR"},
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
        saved = mock_create.call_args.kwargs.get("reminder_date")
        assert saved is not None
        assert (saved.hour, saved.minute) == (15, 0), (
            f"saved reminder_date {saved} dropped the explicit 3pm — this is "
            "the exact prod failure (row saved at 09:00)"
        )
        assert mock_create.call_args.kwargs.get("text") == "review the pr"
        assert "morning" not in result.lower(), (
            f"confirmation copy claims a morning default: {result!r}"
        )
        assert "3:00 pm" in result.lower() or "3pm" in result.lower()
        assert not re.search(r"\b(\w+)\s+\1\b", result.lower())


# ---------------------------------------------------------------------------
# #1493 companion: inverted-order path is timezone-aware local
# ---------------------------------------------------------------------------


class TestInvertedOrderTZAware1493:
    """The new inverted-order binding must honor #1493's aware-local rule:
    the returned datetime CARRIES the server-local offset (so timestamptz
    storage is UTC-normalized instead of drifting by the UTC offset)."""

    def test_inverted_order_reminder_is_aware_local(self):
        dt, label = parse_reminder_time("remind me at 3pm tomorrow to review the PR")
        assert dt is not None
        assert dt.tzinfo is not None, (
            "inverted-order path returned a NAIVE datetime — stored to "
            "timestamptz it drifts by the server's UTC offset (#1493)"
        )
        assert dt.utcoffset() == datetime.now().astimezone().utcoffset()
        assert dt.hour == 15  # 3pm server-LOCAL wall clock, per #1493 semantics
