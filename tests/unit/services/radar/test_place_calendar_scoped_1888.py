"""1888 — the Place feature's calendar candidate is built WITH the user's scope.

`PlaceProvider.list_for_user` and `/api/v1/places` constructed
`CalendarIntegrationRouter()` with no user_id although both had it in hand —
an unscoped router never takes the per-user keychain path, so a connected
user's calendar Places were silently absent (after #1592, an INFO line was the
only trace). Pinned at the construction call: the router is built with
`user_id=<the caller's user>`, at both sites.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _router_factory(seen: list):
    def factory(*args, **kwargs):
        seen.append(kwargs.get("user_id"))
        inst = MagicMock()
        inst.authenticate = AsyncMock(return_value=False)  # not connected — stop early
        return inst

    return factory


@pytest.mark.asyncio
async def test_place_provider_scopes_the_calendar_router_to_the_user():
    from services.radar.feed_factory import PlaceProvider

    seen: list = []
    with patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
        side_effect=_router_factory(seen),
    ):
        provider = PlaceProvider()
        try:
            await provider.list_for_user("user-1888")
        except Exception:
            pass  # everything after the calendar candidate is out of scope here
    assert seen == ["user-1888"], f"router built with user_id={seen}"


@pytest.mark.asyncio
async def test_places_route_scopes_the_calendar_router_to_the_user():
    from web.api.routes import places as places_route

    seen: list = []
    with patch(
        "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter",
        side_effect=_router_factory(seen),
    ):
        src = open(places_route.__file__, encoding="utf-8").read()
        # The route builds the candidate the same way; pin the construction text
        # so a regression to the bare constructor is caught even if the route's
        # auth/DB scaffolding makes a full drive impractical here.
        assert "CalendarIntegrationRouter(user_id=user_id)" in src
        assert "CalendarIntegrationRouter()" not in src
