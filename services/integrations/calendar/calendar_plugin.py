"""
Calendar Integration Plugin

Wraps Calendar integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata

from .calendar_integration_router import CalendarIntegrationRouter
from .config_service import CalendarConfigService


class CalendarPlugin(PiperPlugin):
    """
    Google Calendar integration plugin.

    Provides Calendar integration routes and spatial intelligence
    through the plugin system.
    """

    def __init__(self):
        """Initialize Calendar plugin with config service"""
        self.config_service = CalendarConfigService()
        # Issue #849: CalendarPlugin is a singleton initialized without user context.
        # This router is used for feature flags and status only, not authenticated data access.
        # User-scoped calendar operations use ad-hoc CalendarIntegrationRouter(user_id=...) instances.
        self.integration_router = CalendarIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Calendar plugin metadata"""
        return PluginMetadata(
            name="calendar",
            version="1.0.0",
            description="Google Calendar integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "spatial"],  # Calendar has spatial
            dependencies=[],
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Calendar routes.

        Creates APIRouter wrapper around CalendarIntegrationRouter.
        """
        if self._api_router is None:
            self._api_router = APIRouter(prefix="/api/v1/integrations/calendar", tags=["calendar"])
            # #1547 (audit F5): the GET /status sub-route is DELETED — it served
            # `configured: false` forever, for everyone (is_configured() is
            # hardcoded False without user context, #784). Truthful status lives
            # at /api/v1/integrations/health and the calendar settings routes.

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Calendar is properly configured.

        Note: At plugin startup, there's no user context available.
        This returns False until a user context is established.
        Issue #784: Fixed crash from calling is_configured() without user_id.
        """
        # Without user context, we can't determine configuration
        # The config_service.is_configured() requires user_id (Issue #734)
        return False

    async def initialize(self) -> None:
        """Initialize Calendar plugin"""
        if self.is_configured():
            print(
                f"  ✅ Calendar plugin initialized (spatial: {self.integration_router.use_spatial})"
            )
        else:
            print(f"  ⚠️  Calendar plugin initialized but not configured")

    async def shutdown(self) -> None:
        """Cleanup Calendar plugin resources"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get Calendar plugin status.

        #1547: `configured` is None, not False — configuration is user-scoped
        and unknowable at plugin level (#784). Callers needing real status use
        services/integrations/integration_status_service.py.
        """
        return {
            "configured": None,
            "configured_note": (
                "user-scoped — use IntegrationStatusService.get_status(user_id, ...)"
            ),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.integration_router.use_spatial,
            "legacy_allowed": self.integration_router.allow_legacy,
            "integration_router": "active",
        }


# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_calendar_plugin = CalendarPlugin()
get_plugin_registry().register(_calendar_plugin)
