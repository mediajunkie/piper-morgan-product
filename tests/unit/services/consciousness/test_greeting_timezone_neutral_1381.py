"""Greetings don't assume the user's timezone (PM 2026-07-14, #1381 family).

The bug: `format_greeting_conscious` computed the day-part from `datetime.now()`
— the SERVER's clock, which is UTC on the hosted deploys. A Pacific-time user at
11:44am got "Good evening!" because the server was at 18:44 UTC. The greeting was
correct for the server and wrong for the user, presented as if it were the user's
day-part.

PM's rule: when we don't know the user's timezone, speak neutrally — no day-part
assumption. When we DO know it (a real tz name), the day-part is honest and kept.
"""

from services.consciousness.conversation_consciousness import (
    _current_time_of_day,
    format_greeting_conscious,
)

_DAY_PARTS = {"morning", "late_morning", "afternoon", "evening"}


class TestUnknownTimezoneIsNeutral:
    def test_none_timezone_is_unknown(self):
        assert _current_time_of_day(None) == "unknown"

    def test_invalid_timezone_degrades_to_unknown(self):
        """A garbage tz name must degrade to neutral, never raise or guess."""
        assert _current_time_of_day("Not/AZone") == "unknown"

    def test_greeting_without_timezone_has_no_day_part(self):
        opening = format_greeting_conscious().split("\n")[0]
        assert "Hello" in opening
        for banned in ("Good morning", "Good afternoon", "Good evening"):
            assert banned not in opening


class TestKnownTimezoneKeepsDayPart:
    def test_valid_timezone_resolves_a_day_part(self):
        """When we actually know the tz, the day-part is honest and preserved
        (forward-compatible for when per-user tz lands)."""
        assert _current_time_of_day("America/Los_Angeles") in _DAY_PARTS

    def test_greeting_with_timezone_uses_day_part(self):
        """Freeze the day-part: the original wall-clock version assumed every
        day-part template LEADS with "Good ..." — the evening family opens
        differently ("I'm here and ready. Good evening!"), so the test failed
        only during evening-hour runs (#1452 gate caught it as an oscillator)."""
        from unittest.mock import patch

        with patch(
            "services.consciousness.conversation_consciousness._current_time_of_day",
            return_value="morning",
        ):
            opening = format_greeting_conscious(
                user_timezone="America/Los_Angeles"
            ).split("\n")[0]
        assert "Good morning" in opening
