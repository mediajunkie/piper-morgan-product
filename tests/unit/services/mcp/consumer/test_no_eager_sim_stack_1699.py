"""#1699 regression: the calendar path must NOT construct the legacy MCP sim stack.

GoogleCalendarMCPAdapter.__init__ used to eagerly build ``MCPConsumerCore()``
(service discovery + connection pool) for a path that could never execute —
``_server_params_for`` raises NotImplementedError (#1220's open decision) before
any of it could be used. Real infrastructure on an unreachable path is carrying
cost plus a false liveness signal (it mis-led the 2026-08-29 census).

These tests spy at the DEFINITION site (``consumer_core.MCPConsumerCore.__init__``)
so ANY construction during adapter/router init is caught, regardless of import
shape. They pin construction-count zero; they do NOT touch #1220's transport
decision, ``_server_params_for``, or USE_SPATIAL_CALENDAR's default.
"""

from unittest.mock import patch

import services.mcp.consumer.consumer_core as consumer_core


def _count_constructions(fn):
    """Run ``fn`` with MCPConsumerCore.__init__ spied; return the call count."""
    calls = {"n": 0}
    orig = consumer_core.MCPConsumerCore.__init__

    def spy(self, *args, **kwargs):
        calls["n"] += 1
        return orig(self, *args, **kwargs)

    with patch.object(consumer_core.MCPConsumerCore, "__init__", spy):
        fn()
    return calls["n"]


class TestNoEagerSimStackConstruction:
    def test_adapter_init_does_not_construct_sim_stack(self):
        """Constructing the adapter builds NO MCPConsumerCore (#1699)."""
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        assert _count_constructions(lambda: GoogleCalendarMCPAdapter(user_id="u-1699")) == 0

    def test_router_init_does_not_construct_sim_stack(self):
        """The live entry (calendar_integration_router, USE_SPATIAL_CALENDAR
        default-true) builds the spatial leg with NO sim-stack construction —
        this is the path services/standup/assembler.py:214 exercises per standup."""
        from services.integrations.calendar.calendar_integration_router import (
            CalendarIntegrationRouter,
        )

        def build():
            router = CalendarIntegrationRouter(user_id="u-1699")
            # The spatial leg itself must still be live (the surgery removed the
            # sim stack's construction, not the working spatial adapter).
            assert router.spatial_calendar is not None
            assert type(router.spatial_calendar).__name__ == "GoogleCalendarMCPAdapter"

        assert _count_constructions(build) == 0
