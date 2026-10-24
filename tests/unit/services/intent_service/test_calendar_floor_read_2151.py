"""#2151 FLOOR-ABSENT, calendar (Arch 10-23 21:28 shape, gathers 4b and 6 of 7).

The calendar gather mapped every failure to {} (cached for its TTL, since {} is not
None), the same as a free day; the recent-activity calendar leg returned [] on any
error. These pins run the real CalendarIntegrationRouter and GoogleCalendarMCPAdapter
paths and inject the failure at the adapter:

- an error summary, or a connected summary whose events read never happened, arms
  ``calendar_source_failed``; not connected and no integration are not performed;
- ``get_events_in_range`` now sets ``last_read_error`` on its circuit-open and
  not-authenticated returns, so the activity leg arms
  ``calendar_activity_source_failed`` on a real failure and stays silent when the
  user simply has no calendar.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter
from services.intent_service.context_assembler import ContextAssembler
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

UID = "00000000-0000-0000-0000-000000002151"


class _NoOpCache:
    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


def _adapter() -> GoogleCalendarMCPAdapter:
    adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
    adapter.last_read_error = None
    adapter._circuit_open = False
    adapter._service = object()
    counter = MagicMock()

    async def _passthrough(_name, coro, input_data=""):
        return await coro

    counter.wrap_mcp_call = _passthrough
    adapter.token_counter = counter
    return adapter


def _signin(adapter, *, stored_token, refreshed=True, keychain_error=None):
    """Run the REAL ``authenticate`` (Arch 10-24: pins at the failure point). The
    keychain read and the token refresh are the patched seams; the file fallback
    finds no client secrets (the hosted shape)."""
    adapter._service = None
    adapter._credentials = None
    adapter._user_id = UID
    adapter._token_file = "/nonexistent/fake-token.json"
    adapter._client_secrets_file = "/nonexistent/fake-secrets.json"
    adapter._scopes = []
    adapter._error_count = 0
    keychain = MagicMock()
    if keychain_error is not None:
        keychain.aget_api_key = AsyncMock(side_effect=keychain_error)
    else:
        keychain.aget_api_key = AsyncMock(return_value=stored_token)
    handler = MagicMock()
    handler.refresh_access_token = AsyncMock(
        return_value=MagicMock(access_token="fake-access") if refreshed else None
    )
    return [
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
            return_value=handler,
        ),
        patch.object(GoogleCalendarMCPAdapter, "_is_user_scoped", new=True, create=True),
    ]


async def _with(patches, coro_fn):
    for p in patches:
        p.start()
    try:
        return await coro_fn()
    finally:
        for p in patches:
            p.stop()


def _router(adapter) -> CalendarIntegrationRouter:
    router = CalendarIntegrationRouter.__new__(CalendarIntegrationRouter)
    router.use_spatial = True
    router.allow_legacy = False
    router.spatial_calendar = adapter
    router.legacy_calendar = None
    router._user_id = UID
    return router


async def _gather_calendar(router):
    with patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
        return_value=router,
    ):
        return await ContextAssembler()._gather_calendar_context(UID)


# ── The calendar gather ──


@pytest.mark.asyncio
async def test_an_error_inside_the_summary_arms_the_flag():
    adapter = _adapter()
    adapter.get_current_meeting = AsyncMock(side_effect=TimeoutError("fake"))
    assert await _gather_calendar(_router(adapter)) == {"calendar_source_failed": True}


@pytest.mark.asyncio
async def test_an_events_read_never_established_arms_the_flag():
    adapter = _adapter()
    adapter.get_current_meeting = AsyncMock(return_value=None)
    adapter.get_next_meeting = AsyncMock(return_value=None)
    adapter.get_free_time_blocks = AsyncMock(return_value=[])
    adapter._fetch_todays_events = AsyncMock(return_value=([], False))
    assert await _gather_calendar(_router(adapter)) == {"calendar_source_failed": True}


@pytest.mark.asyncio
async def test_never_connected_is_not_performed():
    adapter = _adapter()
    patches = _signin(adapter, stored_token=None)
    out = await _with(patches, lambda: _gather_calendar(_router(adapter)))
    assert out == {}
    assert adapter.last_read_error == "no_credential"


@pytest.mark.asyncio
async def test_a_stored_credential_that_will_not_refresh_is_a_failed_read():
    """Arch 10-24 07:55: the false free day — connected, the refresh fails, and the
    summary says calendar_connected False."""
    adapter = _adapter()
    patches = _signin(adapter, stored_token="fake-refresh-token", refreshed=False)
    out = await _with(patches, lambda: _gather_calendar(_router(adapter)))
    assert out == {"calendar_source_failed": True}
    assert adapter.last_read_error == "unauthorized"


@pytest.mark.asyncio
async def test_a_keychain_error_is_a_failed_read():
    adapter = _adapter()
    patches = _signin(adapter, stored_token=None, keychain_error=TimeoutError("fake"))
    out = await _with(patches, lambda: _gather_calendar(_router(adapter)))
    assert out == {"calendar_source_failed": True}
    assert adapter.last_read_error not in (None, "no_credential")


@pytest.mark.asyncio
async def test_no_calendar_integration_is_not_performed():
    router = _router(None)
    router.use_spatial = False
    assert await _gather_calendar(router) == {}


@pytest.mark.asyncio
async def test_a_read_day_maps_as_before():
    adapter = _adapter()
    adapter.get_current_meeting = AsyncMock(return_value=None)
    adapter.get_next_meeting = AsyncMock(
        return_value={"title": "Fake 1:1", "start": "2026-10-24T14:00:00"}
    )
    adapter.get_free_time_blocks = AsyncMock(
        return_value=[{"start": "2026-10-24T15:00:00", "duration_minutes": 60}]
    )
    adapter._fetch_todays_events = AsyncMock(return_value=([], True))
    adapter._generate_recommendations = MagicMock(return_value=[])
    out = await _gather_calendar(_router(adapter))
    assert out["calendar"]["next_meeting"]["title"] == "Fake 1:1"
    assert "calendar_source_failed" not in out


# ── The recent-activity calendar leg ──


async def _gather_activity(router):
    assembler = ContextAssembler()
    with (
        patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
            return_value=router,
        ),
        patch.object(
            assembler, "_fetch_github_activity_items", new=AsyncMock(return_value=([], False))
        ),
        patch.object(assembler, "_fetch_slack_activity_items", new=AsyncMock(return_value=[])),
        patch.object(assembler, "_fetch_slack_mentions_items", new=AsyncMock(return_value=[])),
    ):
        return await assembler._gather_recent_activity_context(UID)


@pytest.mark.asyncio
async def test_activity_circuit_open_arms_the_leg_flag():
    adapter = _adapter()
    adapter._circuit_open = True
    assert await _gather_activity(_router(adapter)) == {"calendar_activity_source_failed": True}


@pytest.mark.asyncio
async def test_activity_read_error_arms_the_leg_flag():
    adapter = _adapter()
    adapter._get_user_timezone = AsyncMock(side_effect=TimeoutError("fake"))
    adapter._handle_error = MagicMock()
    assert await _gather_activity(_router(adapter)) == {"calendar_activity_source_failed": True}


@pytest.mark.asyncio
async def test_activity_no_calendar_is_not_performed():
    adapter = _adapter()
    patches = _signin(adapter, stored_token=None)
    assert await _with(patches, lambda: _gather_activity(_router(adapter))) == {}


@pytest.mark.asyncio
async def test_activity_a_failed_refresh_arms_the_leg_flag():
    adapter = _adapter()
    patches = _signin(adapter, stored_token="fake-refresh-token", refreshed=False)
    out = await _with(patches, lambda: _gather_activity(_router(adapter)))
    assert out == {"calendar_activity_source_failed": True}


@pytest.mark.asyncio
async def test_a_stale_error_class_is_reset_by_the_next_read():
    """The real get_events_in_range resets last_read_error first: a leftover
    "unauthorized" from an earlier read must not turn a never-connected read into a
    failure."""
    adapter = _adapter()
    adapter.last_read_error = "unauthorized"  # left over from an earlier read
    patches = _signin(adapter, stored_token=None)
    assert await _with(patches, lambda: _gather_activity(_router(adapter))) == {}
    assert adapter.last_read_error == "no_credential"
