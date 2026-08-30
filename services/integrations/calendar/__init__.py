"""
Calendar Integration Module

Provides router-based access to calendar integrations with feature flag control.
"""

from .calendar_integration_router import CalendarIntegrationRouter, create_calendar_integration

# The Issue-624 grammar-conscious triplet (narrative_bridge / narrative_helpers /
# response_context) was disposed 2026-08-30 in the Batch-2 census-dead-family
# disposal — loaded-only, zero call sites. Retrievable by commit hash via the
# disposal record in decisions.log.

__all__ = [
    # Router
    "CalendarIntegrationRouter",
    "create_calendar_integration",
]
