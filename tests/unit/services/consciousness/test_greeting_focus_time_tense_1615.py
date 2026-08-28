"""#1615 (tense half): the greeting never cites finished focus time in
present tense.

PM's 2026-08-13 12:42 retest: the greeting said "I noticed you have some
focus time between 9:30 am and 10:00 am" — a real block, honestly read
(no fabrication), but fully elapsed at render time and cited as though
upcoming. Stale-but-true present tense, cousin of
feedback_present_tense_note_goes_stale.

Root cause, layer named: ``_format_free_block``
(services/consciousness/conversation_consciousness.py) rendered the first
honest block with no elapsed check. The fix is NOT #1572-gated the way the
day-part question is: every block that reaches rendering passed
``_parse_iso``, which rejects naive timestamps, so "has this window
finished?" is an absolute-instant comparison (``end_dt <= utc_now()``) —
no user clock face involved (m-43: elapsed-ness and clock-face rendering
are different layers).

Behavior pinned here:
- a block whose end is already past renders in PAST tense ("you had"),
  never "you have";
- a still-open block (upcoming OR ongoing — not finished) keeps the
  present tense;
- when an elapsed block sits ahead of a still-open one in the list, the
  still-open one wins (mention remaining time in preference to spent time).

Clock control: module-level ``utc_now`` monkeypatch — the established
idiom (see test_context_assembler.py's #1573 pins). No sleeps.
"""

from datetime import datetime, timezone

import pytest

import services.consciousness.conversation_consciousness as cc
from services.consciousness.conversation_consciousness import format_greeting_conscious

# PM's retest moment: 2026-08-13 12:42 PT == 19:42 UTC.
_RETEST_NOW = datetime(2026, 8, 13, 19, 42, 0, tzinfo=timezone.utc)

# The block PM saw cited in present tense: 9:30-10:00 am PT, long finished
# by 12:42. Event-derived (provider offsets), so it renders without a tz.
_ELAPSED_BLOCK = {
    "start_time": "2026-08-13T09:30:00-07:00",
    "end_time": "2026-08-13T10:00:00-07:00",
    "duration_minutes": 30,
    "type": "between_meetings",
}

_UPCOMING_BLOCK = {
    "start_time": "2026-08-13T14:00:00-07:00",
    "end_time": "2026-08-13T16:00:00-07:00",
    "duration_minutes": 120,
    "type": "between_meetings",
}

# Straddles the frozen now (12:00-13:30 PT at 12:42): started, not finished.
_ONGOING_BLOCK = {
    "start_time": "2026-08-13T12:00:00-07:00",
    "end_time": "2026-08-13T13:30:00-07:00",
    "duration_minutes": 90,
    "type": "between_meetings",
}


@pytest.fixture(autouse=True)
def _frozen_now(monkeypatch):
    """Freeze the module's clock at PM's retest instant (#1573 idiom)."""
    monkeypatch.setattr(cc, "utc_now", lambda: _RETEST_NOW)


def _summary(free_blocks):
    return {
        "success": True,
        "calendar_connected": True,
        "events_read_established": True,
        "current_meeting": None,
        "next_meeting": None,
        "free_blocks": free_blocks,
        "stats": {
            "total_meetings_today": 2,
            "total_meeting_minutes": 120,
            "total_free_minutes": 150,
        },
    }


class TestElapsedBlockPastTense:
    """Finished time is never cited as though upcoming."""

    def test_elapsed_block_renders_in_past_tense(self):
        """PM's exact case: at 12:42, the 9:30-10:00 am block is over —
        'you had', with the same times, never 'you have'."""
        message = format_greeting_conscious(calendar_summary=_summary([_ELAPSED_BLOCK]))
        lowered = message.lower()
        assert "you had some focus time between 9:30 am and 10:00 am" in lowered, message
        assert "you have some focus time" not in lowered, message

    def test_elapsed_server_derived_block_past_tense_with_zone_label(self):
        """The labeled (tz-known, server-derived) render path gets the same
        tense discipline as the event-derived one."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                [
                    {
                        # 16:30-17:00 UTC == 9:30-10:00 am PDT, elapsed at 19:42Z.
                        "start_time": "2026-08-13T16:30:00+00:00",
                        "end_time": "2026-08-13T17:00:00+00:00",
                        "duration_minutes": 30,
                        "type": "before_meeting",
                    }
                ]
            ),
            user_timezone="America/Los_Angeles",
        )
        lowered = message.lower()
        assert "you had some focus time between 9:30 am pdt and 10:00 am pdt" in lowered, message
        assert "you have some focus time" not in lowered, message


class TestStillOpenBlockPresentTense:
    """A window that hasn't finished keeps the present tense."""

    def test_upcoming_block_stays_present_tense(self):
        message = format_greeting_conscious(calendar_summary=_summary([_UPCOMING_BLOCK]))
        lowered = message.lower()
        assert "you have some focus time between 2:00 pm and 4:00 pm" in lowered, message
        assert "you had some focus time" not in lowered, message

    def test_ongoing_block_stays_present_tense(self):
        """Started but not finished is not finished — no past-tense claim
        about a window with remaining time."""
        message = format_greeting_conscious(calendar_summary=_summary([_ONGOING_BLOCK]))
        lowered = message.lower()
        assert "you have some focus time between 12:00 pm and 1:30 pm" in lowered, message
        assert "you had some focus time" not in lowered, message


class TestStillOpenBlockPreferred:
    """Remaining time beats spent time when both are on offer."""

    def test_upcoming_block_wins_over_earlier_elapsed_block(self):
        """Elapsed block first in the list, upcoming second: the greeting
        mentions the one the user can still use."""
        message = format_greeting_conscious(
            calendar_summary=_summary([_ELAPSED_BLOCK, _UPCOMING_BLOCK])
        )
        lowered = message.lower()
        assert "you have some focus time between 2:00 pm and 4:00 pm" in lowered, message
        assert "9:30 am" not in lowered, message

    def test_only_elapsed_blocks_fall_back_to_past_tense_not_silence(self):
        """Two elapsed blocks: the first still gets an honest past-tense
        mention (PM asked for 'past ones in past tense', not omission)."""
        earlier = {
            "start_time": "2026-08-13T08:00:00-07:00",
            "end_time": "2026-08-13T08:45:00-07:00",
            "duration_minutes": 45,
            "type": "between_meetings",
        }
        message = format_greeting_conscious(calendar_summary=_summary([earlier, _ELAPSED_BLOCK]))
        lowered = message.lower()
        assert "you had some focus time between 8:00 am and 8:45 am" in lowered, message
        assert "you have some focus time" not in lowered, message
