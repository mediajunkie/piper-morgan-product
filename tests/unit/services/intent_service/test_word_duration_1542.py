"""Issue #1542 — word-form durations in reminders (#1490 invariant deepening).

PM live 2026-08-09, two verbatim phrasings:

1. "remind me to stretch in two hours" — saved for TOMORROW 9AM with
   "in two hours" swallowed into the task text: word-form durations escape
   _TIME_EXPR's digit-only ``in \\d+ hours`` (so the trailing strip leaves the
   phrase in the todo text) AND parse_reminder_time's digit-only "in N units"
   branch (so the parser falls to the tomorrow-morning default).
2. "remind me in two hours to stretch" — task extraction fails entirely:
   the time-first pattern requires _TIME_EXPR to match directly after
   "remind me", and the digit-only duration form can't see "in two hours".

This is #1490 invariant-DEEPENING (slot layer only, not routing): an explicit
duration — digit or word form — must parse as an explicit duration, never be
silently defaulted, and duration-first orderings must extract the task.

Architecture note: word numbers bind through the same up-front finder shape as
find_explicit_clock_time (a `find_explicit_duration` sibling in
temporal_utils), and _TIME_EXPR imports the shared number-token source so slot
extraction and parsing cannot drift apart.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.intent_service.temporal_utils import parse_reminder_time


def _bounded_parse(message: str):
    """Run parse_reminder_time bracketed by aware-local now() readings so
    relative-duration results can be asserted without clock flake."""
    before = datetime.now().astimezone()
    dt, label = parse_reminder_time(message)
    after = datetime.now().astimezone()
    return before, dt, label, after


# ---------------------------------------------------------------------------
# Parser: word-duration matrix
# ---------------------------------------------------------------------------


class TestWordDurationParsing1542:
    """parse_reminder_time must treat word-form durations exactly like their
    digit forms — an offset from now, never the tomorrow-9am default."""

    def test_pm_verbatim_task_first(self):
        """PM's exact failing phrasing #1: parser half — 'in two hours' must
        not fall to the tomorrow-morning default."""
        before, dt, label, after = _bounded_parse("remind me to stretch in two hours")
        assert dt is not None
        assert before + timedelta(hours=2) <= dt <= after + timedelta(hours=2), (
            f"'in two hours' not parsed as a 2h offset — got {dt} (label "
            f"{label!r}); tomorrow 09:00 means the default swallowed it"
        )
        assert "hour" in label
        assert "morning" not in label

    def test_pm_verbatim_duration_first(self):
        """PM's exact failing phrasing #2, parser half."""
        before, dt, label, after = _bounded_parse("remind me in two hours to stretch")
        assert dt is not None
        assert before + timedelta(hours=2) <= dt <= after + timedelta(hours=2)
        assert "hour" in label

    @pytest.mark.parametrize(
        "message,delta,unit_word",
        [
            ("remind me to check the oven in ten minutes", timedelta(minutes=10), "minute"),
            ("remind me in ten minutes to check the oven", timedelta(minutes=10), "minute"),
            ("remind me to follow up in three days", timedelta(days=3), "day"),
            ("remind me in three days to follow up", timedelta(days=3), "day"),
            ("remind me in one hour to stand up", timedelta(hours=1), "hour"),
            ("remind me in twelve hours to take the medication", timedelta(hours=12), "hour"),
            ("remind me in an hour to stand up", timedelta(hours=1), "hour"),
            # Digit forms must stay green (regression guard)
            ("remind me in 2 hours to stretch", timedelta(hours=2), "hour"),
            ("remind me to stretch in 45 minutes", timedelta(minutes=45), "minute"),
        ],
    )
    def test_word_duration_matrix(self, message, delta, unit_word):
        before, dt, label, after = _bounded_parse(message)
        assert dt is not None, f"{message!r} parsed to None (label {label!r})"
        assert (
            before + delta <= dt <= after + delta
        ), f"{message!r}: expected now+{delta}, got {dt} (label {label!r})"
        assert unit_word in label

    def test_singular_label_for_one(self):
        _, dt, label, _ = _bounded_parse("remind me in one hour to stand up")
        assert dt is not None
        assert label == "in 1 hour"


# ---------------------------------------------------------------------------
# Slot extraction: word durations in both orderings
# ---------------------------------------------------------------------------


class TestWordDurationTextExtraction1542:
    """_extract_reminder_text must consume word-form durations in time-first
    position and strip them in trailing position — same contract the digit
    forms already have."""

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    @pytest.mark.parametrize(
        "message,expected",
        [
            # PM's verbatim phrasing #1: trailing word duration must be
            # stripped from the saved task text, not swallowed into it.
            ("remind me to stretch in two hours", "stretch"),
            # PM's verbatim phrasing #2: duration-first must extract at all.
            ("remind me in two hours to stretch", "stretch"),
            ("remind me in ten minutes to check the oven", "check the oven"),
            ("remind me to check the oven in ten minutes", "check the oven"),
            ("remind me in three days to follow up", "follow up"),
            ("remind me to follow up in three days", "follow up"),
            ("remind me in an hour to stand up", "stand up"),
            # Digit forms must stay green
            ("remind me in 2 hours to stretch", "stretch"),
            ("remind me to stretch in 2 hours", "stretch"),
        ],
    )
    def test_word_duration_orderings(self, message, expected):
        assert self.handlers._extract_reminder_text(message) == expected


# ---------------------------------------------------------------------------
# Handler end-to-end: PM's two verbatim phrasings
# ---------------------------------------------------------------------------


class TestWordDurationHandler1542:
    def _intent(self, message: str):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        return Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": message},
        )

    def _mock_todo(self, text: str):
        from services.domain.models import Todo

        return Todo(
            id=str(uuid4()),
            text=text,
            priority="medium",
            status="pending",
            completed=False,
        )

    async def test_task_first_saves_two_hour_offset_clean_text(self):
        """PM phrasing #1 end-to-end: reminder_date ≈ now+2h (NOT tomorrow
        09:00) and the saved text is 'stretch' (duration not swallowed)."""
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handlers = TodoIntentHandlers()
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=self._mock_todo("stretch"),
        ) as mock_create:
            before = datetime.now().astimezone()
            result = await handlers.handle_create_reminder(
                self._intent("remind me to stretch in two hours"), "s-1", uuid4()
            )
            after = datetime.now().astimezone()

        assert mock_create.called
        assert mock_create.call_args.kwargs.get("text") == "stretch", (
            "duration phrase swallowed into the task text — the exact prod "
            "failure (todo saved as 'stretch in two hours')"
        )
        saved = mock_create.call_args.kwargs.get("reminder_date")
        assert saved is not None
        assert before + timedelta(hours=2) <= saved <= after + timedelta(hours=2), (
            f"saved reminder_date {saved} is not now+2h — tomorrow 09:00 "
            "means the morning default swallowed the explicit duration"
        )
        assert "morning" not in result.lower()

    async def test_duration_first_extracts_task_and_saves(self):
        """PM phrasing #2 end-to-end: pre-fix the handler replied 'I didn't
        catch what you'd like to be reminded about' and saved nothing."""
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handlers = TodoIntentHandlers()
        with patch.object(
            handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=self._mock_todo("stretch"),
        ) as mock_create:
            before = datetime.now().astimezone()
            result = await handlers.handle_create_reminder(
                self._intent("remind me in two hours to stretch"), "s-1", uuid4()
            )
            after = datetime.now().astimezone()

        assert (
            "didn't catch" not in result
        ), "duration-first ordering still fails task extraction entirely"
        assert mock_create.called
        assert mock_create.call_args.kwargs.get("text") == "stretch"
        saved = mock_create.call_args.kwargs.get("reminder_date")
        assert before + timedelta(hours=2) <= saved <= after + timedelta(hours=2)
