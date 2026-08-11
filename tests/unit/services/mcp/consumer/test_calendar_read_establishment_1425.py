"""The temporal summary must say whether the day's events were actually read.

``GoogleCalendarMCPAdapter.get_todays_events`` returns ``[]`` for a genuinely
empty day, for an open circuit breaker, for a failed authenticate, and for any
exception inside the Google call — four states, one indistinguishable value.
``get_temporal_summary`` then published ``total_meetings_today: 0`` with
``success: True``, and the greeting narrated that as "a clear day ahead" while
PM's calendar held four events (observed on v48, 2026-08-10 02:09Z).

The fix is not to guess better downstream: it is for the layer that KNOWS
whether the read happened to say so. ``events_read_established`` is that flag —
True only when the events query completed, whatever it returned.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter


async def _passthrough_wrap(_name, coro, **_kw):
    """Stand-in for TokenCounter.wrap_mcp_call: awaits and returns the inner coroutine."""
    return await coro


def _adapter() -> GoogleCalendarMCPAdapter:
    adapter = GoogleCalendarMCPAdapter(MagicMock())
    adapter._service = MagicMock()  # already "authenticated"
    adapter.token_counter = MagicMock()
    adapter.token_counter.wrap_mcp_call = AsyncMock(side_effect=_passthrough_wrap)
    return adapter


class TestEventsReadEstablishment:
    @pytest.mark.asyncio
    async def test_established_true_when_events_query_completes_empty(self):
        """A genuinely empty day: the read HAPPENED and returned nothing."""
        adapter = _adapter()
        with patch.object(adapter, "_fetch_todays_events", AsyncMock(return_value=([], True))):
            summary = await adapter.get_temporal_summary()
        assert summary["success"] is True
        assert summary["stats"]["total_meetings_today"] == 0
        assert summary["events_read_established"] is True

    @pytest.mark.asyncio
    async def test_established_false_when_events_query_failed(self):
        """The failure shape that produced PM's copy: [] with no read behind it."""
        adapter = _adapter()
        with patch.object(adapter, "_fetch_todays_events", AsyncMock(return_value=([], False))):
            summary = await adapter.get_temporal_summary()
        assert summary["stats"]["total_meetings_today"] == 0
        assert summary["events_read_established"] is False

    @pytest.mark.asyncio
    async def test_swallowed_exception_reports_not_established(self):
        """Exercise the real ``get_todays_events`` failure path end to end."""
        adapter = _adapter()
        adapter._service.events.side_effect = RuntimeError("google exploded")
        events, established = await adapter._fetch_todays_events(None)
        assert events == []
        assert established is False

    @pytest.mark.asyncio
    async def test_circuit_open_reports_not_established(self):
        adapter = _adapter()
        adapter._circuit_open = True
        events, established = await adapter._fetch_todays_events(None)
        assert events == []
        assert established is False

    @pytest.mark.asyncio
    async def test_get_todays_events_still_returns_a_plain_list(self):
        """Backward compatibility: the public method's contract is unchanged."""
        adapter = _adapter()
        with patch.object(
            adapter, "_fetch_todays_events", AsyncMock(return_value=([{"a": 1}], True))
        ):
            assert await adapter.get_todays_events() == [{"a": 1}]


class TestFreeBlockNonPositive:
    """``now.replace(hour=18)`` runs BACKWARDS once the server clock passes
    18:00, producing a block that ends before it starts. ``_now_server_local``
    is the explicit seam for that server-clock dependency (the per-user
    timezone answer is #1572, not this)."""

    @pytest.mark.asyncio
    async def test_no_free_block_when_workday_end_already_passed(self):
        import datetime as _dt

        adapter = _adapter()
        with patch.object(
            adapter, "_fetch_todays_events", AsyncMock(return_value=([], True))
        ), patch.object(
            adapter,
            "_now_server_local",
            return_value=_dt.datetime(2026, 8, 10, 19, 9, tzinfo=_dt.timezone.utc),
        ):
            blocks = await adapter.get_free_time_blocks()
        assert blocks == []

    @pytest.mark.asyncio
    async def test_free_block_emitted_when_workday_end_is_ahead(self):
        """The shape PM actually got (02:09Z now, 18:00Z end) is still emitted
        here — the adapter's job is the interval; naming its zone is the
        renderer's (see test_greeting_calendar_honesty_1425)."""
        import datetime as _dt

        adapter = _adapter()
        with patch.object(
            adapter, "_fetch_todays_events", AsyncMock(return_value=([], True))
        ), patch.object(
            adapter,
            "_now_server_local",
            return_value=_dt.datetime(2026, 8, 11, 2, 9, tzinfo=_dt.timezone.utc),
        ):
            blocks = await adapter.get_free_time_blocks()
        assert len(blocks) == 1
        assert blocks[0]["duration_minutes"] == 951
