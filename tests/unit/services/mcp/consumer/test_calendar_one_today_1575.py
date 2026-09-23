"""#1575 — the calendar adapter computes ONE 'today', on the user's clock (audit F3c).

Before: get_todays_events used the user's timezone while get_free_time_blocks and the
naive-range conversion used the SERVER's (UTC on Fly) — two 'today's in one file, so after
5pm PT a PT user's free blocks were computed for tomorrow and ended at 18:00 UTC. After: every
day-boundary derivation starts at ``_now_user_local(user_id)``; #1574 made the stored timezone
preference it reads a real value.

LAYER (m-43): the adapter's own methods with the network + preference reads patched at their
seams — the day-boundary arithmetic is what's under test. DENOMINATOR: the free-blocks path and
the naive-range path (the two server-clock sites the audit named); get_todays_events was already
user-clock and is not re-pinned here.
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

pytestmark = pytest.mark.asyncio

TOKYO = ZoneInfo("Asia/Tokyo")
# 10:00 in Tokyo = 01:00 UTC. A server-clock 'end of day 18:00' would land at 18:00 UTC
# (= 03:00 NEXT DAY Tokyo); the user's is 18:00 Tokyo, 8 hours away.
NOW_TOKYO = datetime(2026, 9, 24, 10, 0, tzinfo=TOKYO)


class TestFreeBlocksUseTheUsersClock:
    async def test_end_of_day_is_the_users_18_00(self):
        """THE #1575 pin: with no meetings, the free block ends at 18:00 in the USER's zone."""
        adapter = GoogleCalendarMCPAdapter()
        with (
            patch.object(adapter, "_fetch_todays_events", AsyncMock(return_value=([], True))),
            patch.object(adapter, "_now_user_local", AsyncMock(return_value=NOW_TOKYO)),
        ):
            blocks = await adapter.get_free_time_blocks(user_id="u-1575")

        assert len(blocks) == 1
        end = datetime.fromisoformat(blocks[0]["end_time"])
        assert end.tzinfo is not None
        assert end.utcoffset() == NOW_TOKYO.utcoffset()  # the user's zone, not the server's
        assert (end.hour, end.minute) == (18, 0)
        assert blocks[0]["duration_minutes"] == 8 * 60

    async def test_user_clock_is_built_from_the_stored_timezone(self):
        """The seam reads the preference layer — the value #1574 made persistent."""
        adapter = GoogleCalendarMCPAdapter()
        with patch.object(adapter, "_get_user_timezone", AsyncMock(return_value="Asia/Tokyo")):
            now = await adapter._now_user_local("u-1575")
        assert now.tzinfo is not None and now.utcoffset() == NOW_TOKYO.utcoffset()


class TestNaiveRangeAssumesTheUsersClock:
    async def test_naive_dates_consult_the_users_clock_before_any_network(self):
        """Naive range bounds are interpreted on the USER's clock (was: the server's)."""
        adapter = GoogleCalendarMCPAdapter()
        # Past the auth/circuit guards with a stub service; the conversion under test runs
        # before the (stubbed) API call — the seam being consulted with the user's id is the
        # observable contract at this layer.
        from unittest.mock import MagicMock

        adapter._service = MagicMock()
        adapter._service.events.return_value.list.return_value.execute.return_value = {"items": []}
        with patch.object(adapter, "_now_user_local", AsyncMock(return_value=NOW_TOKYO)) as seam:
            await adapter.get_events_in_range(
                datetime(2026, 9, 24, 9, 0), datetime(2026, 9, 24, 10, 0), user_id="u-1575"
            )
        seam.assert_awaited_with("u-1575")
