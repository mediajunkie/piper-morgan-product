"""#1576 — agenda / temporal meeting-time and free-block FACES (audit F2).

The audit named three sites (``canonical_handlers.py`` 2439 / 2467 / 2511 at the
2026-08-10 tree, ``0b82edd02``): the EMBEDDED / STANDARD / GRANULAR agenda
formatters, each rendering ``next_meeting["start_time"]`` straight into prose.
Two things are wrong on those lines and only one of them is the audit's:

1. **The face** — what the formatters print is whatever the producer put there,
   with no zone and no formatting. On the live ``_handle_temporal_query`` path
   the producer hands over the adapter's raw ``start_time``, so the user reads
   ``Next Meeting: Design Review at 2026-09-23T15:00:00-07:00``.

2. **The key** — ``_get_calendar_context`` builds its ``next_meeting`` dict with
   ``title`` / ``start`` / ``end``, and reads ``start``/``end`` off a processed
   event that the adapter emits as ``start_time``/``end_time``. Two mismatches in
   series, so ``start`` is always ``None`` and every agenda formatter prints the
   literal ``"TBD"``. Same for ``free_blocks`` and ``meeting_count``, which
   ``_get_calendar_context`` never sets at all — the GRANULAR "Focus Time
   Available" block is unreachable code behind a key that is never written.

The face fix is not verifiable without the key fix: a correctly-labeled render
of a value that never arrives still prints "TBD". So both are pinned here.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers

PT = "America/Los_Angeles"
USER = "11111111-2222-3333-4444-555555555555"

# What the Google adapter actually emits for a processed event (see
# google_calendar_adapter._process_event) — the shape the producer must read.
PROCESSED_MEETING = {
    "id": "evt-1",
    "title": "Design Review",
    "summary": "Design Review",
    "start_time": "2026-09-23T15:00:00-07:00",
    "end_time": "2026-09-23T16:00:00-07:00",
    "start_time_formatted": "3:00 PM",
    "status": "upcoming",
    "duration_minutes": 60,
    "is_all_day": False,
}

# What get_free_time_blocks actually emits (start_time/end_time, not "start").
PROCESSED_FREE_BLOCK = {
    "start_time": "2026-09-23T10:00:00-07:00",
    "end_time": "2026-09-23T11:30:00-07:00",
    "duration_minutes": 90,
    "type": "before_meeting",
}


@pytest.fixture
def handlers():
    return CanonicalHandlers()


def _stored_timezone(tz_name: str):
    """Patch the #1574 STORE, not an import of the getter.

    Patching ``datetime_utils.user_timezone_name`` would miss every module that
    did ``from ... import user_timezone_name`` — and would have passed here for
    the wrong reason, since the preference layer's default is already PT. The
    store is the one place all import styles converge on.
    """
    return patch(
        "services.domain.user_preference_manager.UserPreferenceManager.get_reminder_timezone",
        AsyncMock(return_value=tz_name),
    )


def _patched_calendar():
    """Patch the two collaborators ``_get_calendar_context`` reaches for."""
    config = patch("services.integrations.calendar.config_service.CalendarConfigService")
    router = patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
    )
    return config, router


class TestCalendarContextCarriesAnInstantAndAFace:
    """``_get_calendar_context`` is the producer for all three agenda formatters."""

    @pytest.mark.asyncio
    async def test_next_meeting_time_reaches_the_context_at_all(self, handlers):
        """The key-mismatch defect: ``start``/``end`` read off keys the adapter
        does not emit, so the agenda's meeting time was structurally ``None``
        for every user with a calendar — rendered as the literal "TBD"."""
        config, router = _patched_calendar()
        with config as MockConfig, router as MockRouter:
            MockConfig.return_value.is_configured.return_value = True
            mock_router = MagicMock()
            mock_router.get_next_meeting = AsyncMock(return_value=PROCESSED_MEETING)
            mock_router.get_free_time_blocks = AsyncMock(return_value=[PROCESSED_FREE_BLOCK])
            MockRouter.return_value = mock_router

            with _stored_timezone(PT):
                ctx = await handlers._get_calendar_context(user_id=USER)

        assert ctx is not None
        nm = ctx["next_meeting"]
        # The machine-facing instant survives, aware, for the time-until math
        # in _synthesize_focus_recommendation.
        assert datetime.fromisoformat(nm["start"]).tzinfo is not None
        # And a separate, labeled FACE exists for anything that prints.
        assert nm["start_display"] == "3:00 PM PDT"

    @pytest.mark.asyncio
    async def test_face_follows_the_stored_preference_not_a_default(self, handlers):
        """PT is the preference layer's own default, so a PT assertion cannot
        distinguish "reads the store" from "reads nothing". A non-default zone
        can (m-43: assert at the layer that can actually fail)."""
        config, router = _patched_calendar()
        with config as MockConfig, router as MockRouter:
            MockConfig.return_value.is_configured.return_value = True
            mock_router = MagicMock()
            mock_router.get_next_meeting = AsyncMock(return_value=PROCESSED_MEETING)
            mock_router.get_free_time_blocks = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            with _stored_timezone("America/New_York"):
                ctx = await handlers._get_calendar_context(user_id=USER)

        assert ctx["next_meeting"]["start_display"] == "6:00 PM EDT"

    @pytest.mark.asyncio
    async def test_free_blocks_reach_the_context_with_labeled_faces(self, handlers):
        """``calendar_context["free_blocks"]`` was never written, so GRANULAR's
        Focus-Time section could not render even when free blocks existed."""
        config, router = _patched_calendar()
        with config as MockConfig, router as MockRouter:
            MockConfig.return_value.is_configured.return_value = True
            mock_router = MagicMock()
            mock_router.get_next_meeting = AsyncMock(return_value=None)
            mock_router.get_free_time_blocks = AsyncMock(return_value=[PROCESSED_FREE_BLOCK])
            MockRouter.return_value = mock_router

            with _stored_timezone(PT):
                ctx = await handlers._get_calendar_context(user_id=USER)

        assert ctx["free_blocks"], "free_blocks never reached the render layer"
        block = ctx["free_blocks"][0]
        assert block["start_display"] == "10:00 AM PDT"
        assert block["end_display"] == "11:30 AM PDT"


class TestAgendaFormattersPrintALabeledFace:
    """The three sites the audit named, driven with producer-shaped input."""

    def _ctx(self):
        return {
            "next_meeting": {
                "title": "Design Review",
                "start": "2026-09-23T15:00:00-07:00",
                "start_display": "3:00 PM PDT",
            },
            "free_blocks": [
                {"duration_minutes": 90, "start_display": "10:00 AM PDT"},
            ],
            "meeting_count": 4,
        }

    def test_embedded(self, handlers):
        out = handlers._format_agenda_embedded(self._ctx(), [], [])
        assert "Next: 3:00 PM PDT" in out
        assert "TBD" not in out
        assert "T15:00" not in out, "raw ISO leaked into the EMBEDDED agenda"

    def test_standard(self, handlers):
        out = handlers._format_agenda_standard(self._ctx(), [], [])
        assert "Design Review at 3:00 PM PDT" in out
        assert "TBD" not in out
        assert "T15:00" not in out

    def test_granular(self, handlers):
        out = handlers._format_agenda_granular(self._ctx(), [], [])
        assert "3:00 PM PDT" in out
        assert "90 min at 10:00 AM PDT" in out
        assert "TBD" not in out
        assert "T15:00" not in out

    def test_missing_time_says_so_rather_than_printing_tbd_over_a_real_meeting(self, handlers):
        """When the producer genuinely has no time, the render says the time is
        unknown — it does not silently drop the meeting, and it does not print
        an ISO string or a bare face it does not have."""
        ctx = {"next_meeting": {"title": "Design Review"}}
        out = handlers._format_agenda_standard(ctx, [], [])
        assert "Design Review" in out
        assert "time unknown" in out.lower()


class TestTemporalQueryMeetingFaces:
    """``_handle_temporal_query`` is where the raw ISO is LIVE today: the
    temporal-summary dicts come straight off the adapter, so ``start_time`` is
    the unformatted ISO string and goes directly into the message."""

    def _summary(self):
        return {
            "success": True,
            "calendar_connected": True,
            "next_meeting": dict(PROCESSED_MEETING),
            "free_blocks": [dict(PROCESSED_FREE_BLOCK)],
            "stats": {"total_meetings_today": 2, "total_meeting_time_minutes": 90},
        }

    @pytest.mark.asyncio
    @pytest.mark.parametrize("pattern", ["EMBEDDED", "GRANULAR", None])
    async def test_no_raw_iso_in_the_rendered_message(self, handlers, pattern):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="what's my day look like",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )
        if pattern:
            intent.spatial_context = {"pattern": pattern}

        router = MagicMock()
        router.get_temporal_summary = AsyncMock(return_value=self._summary())

        with (
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=router,
            ),
            _stored_timezone(PT),
        ):
            result = await handlers._handle_temporal_query(intent, "session-1", user_id=USER)

        message = result["message"]
        assert "T15:00" not in message, f"raw ISO meeting time in prose: {message!r}"
        assert "2026-09-23T" not in message, f"raw ISO in prose: {message!r}"
        assert "3:00 PM PDT" in message, f"no labeled meeting face: {message!r}"

    @pytest.mark.asyncio
    async def test_free_block_face_is_not_the_literal_tbd(self, handlers):
        """GRANULAR reads ``block.get("start")`` from blocks the adapter emits
        with ``start_time`` — so "Focus Time Available" listed every block as
        ``0 min at TBD``. A render that is structurally incapable of being
        right is worse than absent: it looks like an answer."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="what's my day look like",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )
        intent.spatial_context = {"pattern": "GRANULAR"}

        router = MagicMock()
        router.get_temporal_summary = AsyncMock(return_value=self._summary())

        with (
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=router,
            ),
            _stored_timezone(PT),
        ):
            result = await handlers._handle_temporal_query(intent, "session-1", user_id=USER)

        message = result["message"]
        assert "90 min at 10:00 AM PDT" in message, message
        assert "TBD" not in message

    @pytest.mark.asyncio
    async def test_the_headline_clock_is_the_users_not_the_config_files(self, handlers):
        """The audit's third face category: 3 sites label the zone honestly and
        then read the CONFIG file's timezone, which is the same value for every
        user. Labeled-but-wrong is the hardest kind to notice, because the
        string looks careful."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory as IntentCategoryEnum

        intent = Intent(
            original_message="what time is it",
            category=IntentCategoryEnum.TEMPORAL,
            action="query_time",
            confidence=0.9,
        )

        router = MagicMock()
        router.get_temporal_summary = AsyncMock(
            return_value={"success": True, "calendar_connected": False}
        )

        with (
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=router,
            ),
            _stored_timezone("America/New_York"),
        ):
            result = await handlers._handle_temporal_query(intent, "session-1", user_id=USER)

        assert "EDT" in result["message"] or "EST" in result["message"], result["message"]
        assert result["intent"]["context"]["timezone"] in ("EDT", "EST")


class TestCalendarAdapterAndAssemblerFaces:
    """The two remaining bare faces on this surface."""

    def test_processed_event_face_is_zone_labeled(self):
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
        processed = GoogleCalendarMCPAdapter._process_event(
            adapter,
            {
                "id": "e1",
                "summary": "Design Review",
                "start": {"dateTime": "2026-09-23T15:00:00-07:00"},
                "end": {"dateTime": "2026-09-23T16:00:00-07:00"},
            },
            tz_name=PT,
        )

        assert processed["start_time_formatted"] == "3:00 PM PDT"
        assert processed["end_time_formatted"] == "4:00 PM PDT"

    def test_all_day_event_face_is_not_a_bare_midnight_on_the_wrong_clock(self):
        """An all-day event has a naive date. It used to be stamped UTC and
        rendered as a bare '12:00 AM' — a clock face for something that has no
        clock time, on a zone the user never sees named."""
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
        processed = GoogleCalendarMCPAdapter._process_event(
            adapter,
            {
                "id": "e2",
                "summary": "Company Holiday",
                "start": {"date": "2026-09-23"},
                "end": {"date": "2026-09-24"},
            },
            tz_name=PT,
        )

        # CXO amended the original "no face" (2026-09-23): an empty face reads as
        # a broken render, so the all-day event SAYS so instead.
        assert (
            processed["start_time_formatted"] == "All day"
        ), "all-day event rendered a clock face it does not have"

    @pytest.mark.asyncio
    async def test_standup_calendar_provider_face_is_labeled(self):
        """The standup page's only time render (``StandupItem.meta``) is a
        server-rendered string dropped into HTML — no browser localization
        downstream, so it carries its zone."""
        from services.standup.assembler import StandupCalendarProvider

        router = MagicMock()
        router.get_todays_events = AsyncMock(return_value=[dict(PROCESSED_MEETING)])
        provider = StandupCalendarProvider(router_factory=lambda user_id: router)

        with _stored_timezone(PT):
            events = await provider.events_today(USER)

        assert events[0]["time"] == "3:00 PM PDT"


class TestSharedFaceHelper:
    """The one formatter everything above routes through."""

    def test_face_is_on_the_users_clock_and_says_which(self):
        from services.utils.datetime_utils import format_user_time

        instant = datetime(2026, 9, 23, 22, 0, tzinfo=timezone.utc)
        assert format_user_time(instant, PT) == "3:00 PM PDT"
        assert format_user_time(instant, "America/New_York") == "6:00 PM EDT"

    def test_unknown_zone_degrades_to_labeled_utc_never_a_bare_face(self):
        from services.utils.datetime_utils import format_user_time

        instant = datetime(2026, 9, 23, 22, 0, tzinfo=timezone.utc)
        assert format_user_time(instant, None) == "10:00 PM UTC"
        assert format_user_time(instant, "Not/AZone") == "10:00 PM UTC"

    def test_unparseable_iso_returns_none_so_callers_cannot_fall_back_to_raw(self):
        from services.utils.datetime_utils import format_iso_as_user_time

        assert format_iso_as_user_time("not a date", PT) is None
        assert format_iso_as_user_time(None, PT) is None


class TestAllDayFace:
    """CXO ruling 2026-09-23 (copy decision 3): all-day events render 'All day', not an empty face."""

    def test_all_day_item_says_all_day_not_a_midnight_clock(self):
        from services.intent_service.canonical_handlers import CanonicalHandlers

        item = {"start_time": "2026-09-24T00:00:00+00:00", "is_all_day": True}
        assert CanonicalHandlers._meeting_face(item, "America/Los_Angeles") == "All day"

    def test_timed_item_is_unchanged(self):
        from services.intent_service.canonical_handlers import CanonicalHandlers

        item = {"start_time": "2026-09-24T22:00:00+00:00", "is_all_day": False}
        assert CanonicalHandlers._meeting_face(item, "America/Los_Angeles") == "3:00 PM PDT"


class TestDefaultZoneIsNamedNotAssumed:
    """#1876: while a user is on the DEFAULT zone the time reply says so and points at
    the one place to change it — this is the chat pointer for /settings/preferences."""

    async def _time_reply(self, handlers, tz_name):
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.TEMPORAL,
            action="get_current_time",
            confidence=1.0,
            original_message="what time is it for me?",
        )
        router = MagicMock()
        router.get_temporal_summary = AsyncMock(return_value={"events": [], "free_blocks": []})
        with (
            patch(
                "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
                return_value=router,
            ),
            _stored_timezone(tz_name),
        ):
            return (await handlers._handle_temporal_query(intent, "session-1", user_id=USER))[
                "message"
            ]

    @pytest.mark.asyncio
    async def test_default_zone_reply_points_at_preferences(self, handlers):
        message = await self._time_reply(handlers, PT)
        assert "default zone (America/Los_Angeles)" in message
        assert "Settings → Preferences" in message

    @pytest.mark.asyncio
    async def test_chosen_zone_reply_has_no_hint(self, handlers):
        message = await self._time_reply(handlers, "Europe/Helsinki")
        assert "default zone" not in message
        assert "EEST" in message or "EET" in message
