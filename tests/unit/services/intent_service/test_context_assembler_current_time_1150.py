"""Tests for #1150: context_assembler's current_time is timezone-aware.

Bug: a bare datetime.now() is the server process's local time, unlabeled. On a
non-local-tz instance (UTC container / dedicated skunkworks instance) it fed the
wrong time-of-day to the conversational floor ("late evening" at 11:30 AM). The
fix converts to the configured timezone (DST-aware %Z label) and is fail-safe.
"""

import re
from datetime import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

from services.intent_service.context_assembler import _current_time_in_configured_tz


class TestCurrentTimeTimezoneAware:
    def test_returns_labeled_time_in_configured_tz(self):
        """Result is 'HH:MM AM/PM TZ' (carries a timezone label, not naive)."""
        result = _current_time_in_configured_tz()
        assert re.match(r"^\d{2}:\d{2} (AM|PM) [A-Z]{2,5}$", result), result

    def test_converts_to_configured_tz_not_server_tz(self):
        """The clock + label reflect the CONFIGURED timezone, regardless of the
        server's local tz — this is the core #1150 fix. Mock a known tz and
        assert the output matches that tz's wall-clock + label."""
        with patch(
            "services.configuration.piper_config_loader.piper_config_loader.load_standup_config",
            return_value={"timing": {"timezone": "America/New_York"}},
        ):
            result = _current_time_in_configured_tz()

        expected = datetime.now(ZoneInfo("America/New_York")).strftime("%I:%M %p %Z")
        # Compare on the tz label + AM/PM (deterministic); allow the minute to
        # differ if the clock ticked between the two now() calls.
        assert result.endswith(expected.split()[-1]), (result, expected)  # tz label (EST/EDT)
        assert result.split()[1] == expected.split()[1], (result, expected)  # AM/PM

    def test_fallback_on_config_error_is_naive_and_does_not_raise(self):
        """A config/zoneinfo failure must NOT break context assembly — it falls
        back to the previous naive (unlabeled) behavior."""
        with patch(
            "services.configuration.piper_config_loader.piper_config_loader.load_standup_config",
            side_effect=RuntimeError("config unavailable"),
        ):
            result = _current_time_in_configured_tz()

        # Naive fallback: 'HH:MM AM/PM' with no tz label.
        assert re.match(r"^\d{2}:\d{2} (AM|PM)$", result), result
