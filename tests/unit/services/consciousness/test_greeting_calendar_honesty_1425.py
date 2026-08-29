"""Greeting-copy honesty for the calendar narrative (m-44 / #1425 family).

Two defects PM observed live on v48 (2026-08-10 19:08 PT / 02:08Z), both in
``_build_calendar_narrative``:

1. **The unestablished "clear day" claim.** ``get_todays_events`` returns ``[]``
   identically for circuit-open, auth failure, and any swallowed exception, so
   ``stats.total_meetings_today == 0`` does NOT mean "no meetings" — it means
   "zero rows came back, for reasons unknown". The greeting asserted "a clear
   day ahead" from it while PM's calendar held four events. An emptiness claim
   requires the read to have *established* emptiness; absent that, say nothing
   about the day's shape.

2. **The unlabeled UTC clock face.** Free blocks are computed from
   ``datetime.now().astimezone()`` — the SERVER clock (UTC on Fly) — and were
   rendered with a bare ``%I:%M %p``. PM read "focus time between 2:09 am and
   6:00 pm"; 02:09 was the UTC instant of his own request. A clock face with no
   zone the reader can attribute is worse than no clock face. Render it only
   when we can name the zone (time-handling audit F2, 2026-08-10); the general
   per-user timezone fix is #1572 and deliberately NOT attempted here.
"""

import pytest

from services.consciousness.conversation_consciousness import format_greeting_conscious

# A UTC-instant free block of the exact shape that produced PM's copy: the
# server's "now" through a server-clock 18:00, no zone the reader can see.
_SERVER_CLOCK_BLOCK = {
    "start_time": "2026-08-11T02:09:00+00:00",
    "end_time": "2026-08-11T18:00:00+00:00",
    "duration_minutes": 951,
    "type": "free_block",
}


def _summary(**overrides):
    base = {
        "success": True,
        "calendar_connected": True,
        "current_meeting": None,
        "next_meeting": None,
        "free_blocks": [],
        "stats": {
            "total_meetings_today": 0,
            "total_meeting_minutes": 0,
            "total_free_minutes": 480,
        },
    }
    base.update(overrides)
    return base


class TestUnestablishedEmptinessClaim:
    """A zero row-count is not an established empty day."""

    def test_no_clear_day_claim_when_read_not_established(self):
        """PM's exact case: zero meetings reported, nothing attesting the read
        actually enumerated the day → the greeting must not call it clear."""
        message = format_greeting_conscious(calendar_summary=_summary())
        lowered = message.lower()
        assert "clear day" not in lowered, message
        assert "clear calendar" not in lowered, message

    def test_no_dangling_calendar_attribution_when_nothing_to_say(self):
        """Suppressing the day-shape claim must not leave a stranded
        'I took a look at your calendar.' with no content behind it."""
        message = format_greeting_conscious(calendar_summary=_summary())
        assert "took a look at your calendar" not in message.lower(), message

    def test_clear_day_claim_allowed_when_read_established(self):
        """When the adapter attests the day was actually enumerated, the
        emptiness claim is honest and should still be made."""
        message = format_greeting_conscious(calendar_summary=_summary(events_read_established=True))
        assert "clear day" in message.lower(), message

    def test_meeting_count_claim_unaffected_when_nonzero(self):
        """A nonzero count is self-evidencing — rows exist. No gate needed."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                stats={
                    "total_meetings_today": 2,
                    "total_meeting_minutes": 120,
                    "total_free_minutes": 180,
                }
            )
        )
        assert "2 meetings today" in message, message


class TestUnlabeledClockFace:
    """Never present a server-clock instant as if it were the reader's."""

    def test_synthetic_whole_day_block_is_never_rendered(self):
        """PM's exact block. ``type: free_block`` is what the adapter emits when
        NO meetings came back — the absence of an observation wearing an
        interval's clothes, with both boundaries server-clock artifacts."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True, free_blocks=[_SERVER_CLOCK_BLOCK]
            )
        )
        lowered = message.lower()
        assert "2:09 am" not in lowered, message
        assert "6:00 pm" not in lowered, message
        assert "focus time" not in lowered, message

    def test_synthetic_block_suppressed_even_with_a_known_timezone(self):
        """Labeling doesn't rescue it — the interval itself isn't an observation."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True, free_blocks=[_SERVER_CLOCK_BLOCK]
            ),
            user_timezone="America/Los_Angeles",
        )
        assert "focus time" not in message.lower(), message

    def test_server_derived_block_suppressed_when_timezone_unknown(self):
        """``before_meeting`` starts at the server's wall clock. No zone we can
        name → no clock face."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True,
                free_blocks=[
                    {
                        "start_time": "2026-08-11T02:09:00+00:00",
                        "end_time": "2026-08-11T17:00:00+00:00",
                        "duration_minutes": 891,
                        "type": "before_meeting",
                    }
                ],
            )
        )
        lowered = message.lower()
        assert "2:09 am" not in lowered, message
        assert "focus time" not in lowered, message

    def test_server_derived_block_labeled_when_timezone_known(self):
        """With a known zone we convert AND name it — the reader can check it."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True,
                free_blocks=[
                    {
                        "start_time": "2026-08-11T02:09:00+00:00",
                        "end_time": "2026-08-11T17:00:00+00:00",
                        "duration_minutes": 891,
                        "type": "before_meeting",
                    }
                ],
            ),
            user_timezone="America/Los_Angeles",
        )
        assert "focus time" in message.lower(), message
        # 02:09Z -> 7:09 pm PDT; 17:00Z -> 10:00 am PDT, both zone-labeled.
        assert "7:09 pm PDT" in message, message
        assert "10:00 am PDT" in message, message

    def test_event_derived_gap_renders_without_a_timezone(self):
        """m-43: a gap BETWEEN two real meetings has provider-supplied offsets,
        so its clock face is already the reader's — same layer as the next
        meeting's time, and not what broke."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True,
                free_blocks=[
                    {
                        "start_time": "2026-08-10T09:00:00-07:00",
                        "end_time": "2026-08-10T11:30:00-07:00",
                        "duration_minutes": 150,
                        "type": "between_meetings",
                    }
                ],
                stats={
                    "total_meetings_today": 2,
                    "total_meeting_minutes": 120,
                    "total_free_minutes": 150,
                },
            )
        )
        assert "focus time between 9:00 am and 11:30 am" in message.lower(), message

    def test_no_focus_time_for_non_positive_block(self):
        """``now.replace(hour=18)`` goes backwards once the server clock passes
        18:00, yielding an 'ends before it starts' block. Never render it."""
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True,
                free_blocks=[
                    {
                        "start_time": "2026-08-10T19:09:00-07:00",
                        "end_time": "2026-08-10T18:00:00-07:00",
                        "duration_minutes": -69,
                        "type": "before_meeting",
                    }
                ],
            ),
            user_timezone="America/Los_Angeles",
        )
        assert "focus time" not in message.lower(), message


class TestNextMeetingTimeUnchanged:
    """m-43, naming the layer: event times arrive from Google carrying the
    calendar's OWN offset, so their clock face is already the user's local one.
    That is a different layer from the server-computed free block and is NOT
    what broke — this test pins that it stays working."""

    def test_next_meeting_time_still_rendered(self):
        message = format_greeting_conscious(
            calendar_summary=_summary(
                events_read_established=True,
                next_meeting={
                    "summary": "Sprint Planning",
                    "start_time": "2026-08-11T10:00:00-07:00",
                },
                stats={
                    "total_meetings_today": 1,
                    "total_meeting_minutes": 60,
                    "total_free_minutes": 180,
                },
            )
        )
        assert "Sprint Planning" in message, message
        assert "10:00 am" in message, message
