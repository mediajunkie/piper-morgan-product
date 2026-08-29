"""Issue #1572: per-user timezone — parse and render reminders on the USER'S
clock (the deferred half of #747; time audit F1/F6 root).

All clock math here runs against a FIXED instant injected by patching the
``datetime`` name inside temporal_utils — never the real wall clock, so
nothing in this file is flaky by time-of-day (fallback-path tests
additionally pin TZ=UTC so the server anchor is deterministic).

The fixed instant is PM's live failure moment: **2026-08-29 20:49 UTC ==
1:49 PM Pacific**, when 'remind me ... 4 PM today' was refused as already
past (16:00 < 20:49 on the server's UTC clock) while being 2+ hours in the
user's future.

Fail-safe pins: with NO stored tz (or an invalid one), parse and render
behavior is byte-identical to pre-#1572 — server anchor, UTC-labeled faces.
"""

import os
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

import services.intent_service.temporal_utils as temporal_utils
from services.intent_service.temporal_utils import (
    PAST_TODAY_PREFIX,
    parse_relative_date,
    parse_reminder_time,
)
from services.intent_service.todo_handlers import (
    _format_reminder_when,
    _reminder_saved_message,
)
from services.utils.user_timezone import is_valid_iana_timezone, resolve_zone

# PM's live failure moment: 1:49 PM PDT, 2026-08-29 (a Saturday).
FIXED_UTC = datetime(2026, 8, 29, 20, 49, tzinfo=timezone.utc)

LA = "America/Los_Angeles"


class _FixedDatetime(datetime):
    """datetime whose now() is pinned to FIXED_UTC (tz-converting like the
    real one). Patched over temporal_utils.datetime so _anchor_now reads the
    fixed instant on every clock."""

    @classmethod
    def now(cls, tz=None):
        if tz is not None:
            return FIXED_UTC.astimezone(tz)
        return FIXED_UTC  # aware; .astimezone() keeps the instant


@pytest.fixture
def frozen_clock(monkeypatch):
    monkeypatch.setattr(temporal_utils, "datetime", _FixedDatetime)
    yield FIXED_UTC


@pytest.fixture
def utc_server():
    """Pin the server-local zone to UTC (what fly runs) so no-tz fallback
    assertions are deterministic on any dev machine."""
    old = os.environ.get("TZ")
    os.environ["TZ"] = "UTC"
    time.tzset()
    yield
    if old is None:
        os.environ.pop("TZ", None)
    else:
        os.environ["TZ"] = old
    time.tzset()


class TestParseOnUserClock1572:
    def test_pm_case_4pm_today_pacific_saves_instead_of_refusing(self, frozen_clock):
        """THE seed failure: '4 PM today' at 1:49 PM Pacific must bind
        today 16:00 PDT (= 23:00 UTC), not the past-today refusal."""
        dt, label = parse_reminder_time(
            "remind me to review the beta notes at 4pm today", user_timezone=LA
        )
        assert dt is not None, f"refused with label {label!r}"
        assert label == "today at 4pm"
        assert dt.astimezone(timezone.utc) == datetime(2026, 8, 29, 23, 0, tzinfo=timezone.utc)

    def test_no_stored_tz_same_message_keeps_utc_refusal(self, frozen_clock, utc_server):
        """Fail-safe pin: WITHOUT a tz, the same message at the same instant
        keeps the pre-#1572 behavior — 16:00 has passed on the server's UTC
        clock, so the honest past-today ask fires."""
        dt, label = parse_reminder_time("remind me to review the beta notes at 4pm today")
        assert dt is None
        assert label.startswith(PAST_TODAY_PREFIX)

    def test_invalid_tz_behaves_exactly_like_no_tz(self, frozen_clock, utc_server):
        with_bad = parse_reminder_time(
            "remind me to review the beta notes at 4pm today", user_timezone="Not/AZone"
        )
        with_none = parse_reminder_time("remind me to review the beta notes at 4pm today")
        assert with_bad == with_none

    def test_tomorrow_9am_binds_in_user_tz_tokyo(self, frozen_clock):
        """20:49 UTC Aug 29 is already Aug 30 05:49 in Tokyo — 'tomorrow at
        9am' must mean Aug 31 09:00 JST (= Aug 31 00:00 UTC), not the
        server's Aug 30."""
        dt, label = parse_reminder_time(
            "remind me to call the team tomorrow at 9am", user_timezone="Asia/Tokyo"
        )
        assert dt is not None
        assert dt.astimezone(timezone.utc) == datetime(2026, 8, 31, 0, 0, tzinfo=timezone.utc)
        assert label == "tomorrow at 9am"

    def test_bare_clock_next_occurrence_rolls_on_user_clock(self, frozen_clock):
        """'at 5pm' with no day word at 1:49 PM PDT is later TODAY on the
        user's clock (17:00 PDT = 00:00 UTC Aug 30) — no roll to tomorrow."""
        dt, label = parse_reminder_time("remind me to stretch at 5pm", user_timezone=LA)
        assert dt is not None
        assert dt.astimezone(timezone.utc) == datetime(2026, 8, 30, 0, 0, tzinfo=timezone.utc)

    def test_parse_relative_date_today_is_users_calendar_day(self, frozen_clock):
        """The revived user_timezone param (dead 0/2 callers per the audit):
        'today' anchored in LA starts at Aug 29 00:00 PDT = 07:00 UTC."""
        start, end, label = parse_relative_date("what's on today", user_timezone=LA)
        assert label == "today"
        assert start.astimezone(timezone.utc) == datetime(2026, 8, 29, 7, 0, tzinfo=timezone.utc)
        assert end.astimezone(timezone.utc) == datetime(2026, 8, 30, 7, 0, tzinfo=timezone.utc)

    def test_parse_relative_date_without_tz_unchanged(self, frozen_clock, utc_server):
        """Fail-safe pin for the revived param's default: no tz → server
        (UTC) day bounds, the pre-#1572 behavior."""
        start, end, label = parse_relative_date("what's on today")
        assert label == "today"
        assert start.astimezone(timezone.utc) == datetime(2026, 8, 29, 0, 0, tzinfo=timezone.utc)


class TestRenderOnUserClock1572:
    WHEN = datetime(2026, 8, 29, 23, 0, tzinfo=timezone.utc)  # 4:00 PM PDT

    def test_format_when_in_user_tz_labeled(self):
        assert _format_reminder_when(self.WHEN, LA) == "Saturday, August 29 at 4:00 PM PDT"

    def test_format_when_without_tz_keeps_labeled_utc(self):
        """Fail-safe pin: the pre-#1572 face, byte-identical."""
        assert _format_reminder_when(self.WHEN, None) == "Saturday, August 29 at 11:00 PM UTC"

    def test_format_when_invalid_tz_keeps_labeled_utc(self):
        assert _format_reminder_when(self.WHEN, "Not/AZone") == (
            "Saturday, August 29 at 11:00 PM UTC"
        )

    def test_saved_message_renders_user_clock(self):
        msg = _reminder_saved_message("water the plants", self.WHEN, "today at 4pm", user_tz=LA)
        assert "4:00 PM PDT" in msg
        assert "UTC" not in msg
        assert "water the plants" in msg

    def test_saved_message_without_tz_keeps_utc_label(self):
        msg = _reminder_saved_message("water the plants", self.WHEN, "today at 4pm")
        assert "11:00 PM UTC" in msg


class TestValidatorAndZones1572:
    def test_valid_iana_names(self):
        assert is_valid_iana_timezone("America/Los_Angeles")
        assert is_valid_iana_timezone("UTC")
        assert is_valid_iana_timezone("Asia/Tokyo")

    def test_invalid_values(self):
        assert not is_valid_iana_timezone("Not/AZone")
        assert not is_valid_iana_timezone("")
        assert not is_valid_iana_timezone(None)
        assert not is_valid_iana_timezone(123)

    def test_resolve_zone(self):
        assert isinstance(resolve_zone(LA), ZoneInfo)
        assert resolve_zone("Not/AZone") is None
        assert resolve_zone(None) is None


class TestSupplyRoundTrip1572:
    """users.preferences['timezone'] storage — real DB, fail-safe reads."""

    @pytest.fixture
    async def tz_user(self):
        import uuid as _uuid

        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory
        from tests.conftest import delete_test_user_fully

        uid = str(_uuid.uuid4())
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(
                User(
                    id=uid,
                    username=f"tz-test-{uid[:8]}",
                    email=f"tz-test-{uid[:8]}@example.com",
                    password_hash="x",
                    is_active=True,
                    is_verified=True,
                )
            )
            await session.commit()
        yield uid
        async with AsyncSessionFactory.session_scope_fresh() as session:
            await delete_test_user_fully(session, uid)
            await session.commit()

    @pytest.mark.asyncio
    async def test_save_then_get_round_trip(self, tz_user):
        from services.utils.user_timezone import get_user_timezone, save_user_timezone

        assert await get_user_timezone(tz_user) is None  # nothing stored yet
        assert await save_user_timezone(tz_user, LA) is True
        assert await get_user_timezone(tz_user) == LA

    @pytest.mark.asyncio
    async def test_invalid_tz_never_writes(self, tz_user):
        from services.utils.user_timezone import get_user_timezone, save_user_timezone

        assert await save_user_timezone(tz_user, "Not/AZone") is False
        assert await get_user_timezone(tz_user) is None

    @pytest.mark.asyncio
    async def test_absent_user_reads_none(self):
        import uuid as _uuid

        from services.utils.user_timezone import get_user_timezone

        assert await get_user_timezone(str(_uuid.uuid4())) is None

    @pytest.mark.asyncio
    async def test_invalid_stored_value_reads_none(self, tz_user):
        """A corrupt stored value degrades to 'unknown', never propagates."""
        from sqlalchemy import select

        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory
        from services.utils.user_timezone import get_user_timezone

        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(select(User).where(User.id == tz_user))
            user = result.scalar_one()
            user.preferences = {"timezone": "garbage"}
            await session.commit()

        assert await get_user_timezone(tz_user) is None

    @pytest.mark.asyncio
    async def test_none_user_id_reads_none(self):
        from services.utils.user_timezone import get_user_timezone

        assert await get_user_timezone(None) is None
