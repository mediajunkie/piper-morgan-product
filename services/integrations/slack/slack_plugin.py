"""
Slack Integration Plugin

Wraps Slack integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.plugins import PiperPlugin, PluginMetadata

from .config_service import SlackConfigService
from .slack_integration_router import SlackIntegrationRouter


class SlackPlugin(PiperPlugin):
    """
    Slack workspace integration plugin.

    Provides Slack integration routes, webhooks, and spatial intelligence
    capabilities through the plugin system.
    """

    def __init__(self):
        """Initialize Slack plugin with config service"""
        self.config_service = SlackConfigService()
        self.integration_router = SlackIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return Slack plugin metadata"""
        return PluginMetadata(
            name="slack",
            version="1.0.0",
            description="Slack workspace integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "webhooks", "spatial"],
            dependencies=[],
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with Slack routes.

        Creates APIRouter wrapper around SlackIntegrationRouter
        for plugin system compatibility.
        """
        if self._api_router is None:
            self._api_router = APIRouter(prefix="/api/v1/integrations/slack", tags=["slack"])

            # Delegate to existing router methods
            @self._api_router.get("/status")
            async def slack_status():
                """Get Slack integration status"""
                return {
                    "configured": self.is_configured(),
                    "spatial_enabled": self.integration_router.use_spatial,
                    "legacy_allowed": self.integration_router.allow_legacy,
                }

        return self._api_router

    def is_configured(self) -> bool:
        """Check if Slack is properly configured"""
        return self.config_service.is_configured()

    async def initialize(self) -> None:
        """
        Initialize Slack plugin.

        Performs any startup initialization needed for Slack integration.
        """
        # Log initialization
        if self.is_configured():
            print(f"  ✅ Slack plugin initialized (spatial: {self.integration_router.use_spatial})")
        else:
            print(f"  ⚠️  Slack plugin initialized but not configured")

    async def shutdown(self) -> None:
        """
        Cleanup Slack plugin resources.

        Performs any cleanup needed when shutting down.
        """
        # Any cleanup needed
        pass

    def get_status(self) -> Dict[str, Any]:
        """
        Get Slack plugin status.

        Returns detailed status information for monitoring.
        """
        return {
            "configured": self.is_configured(),
            "config_service": "active",
            "router": "active" if self._api_router else "inactive",
            "spatial_enabled": self.integration_router.use_spatial,
            "legacy_allowed": self.integration_router.allow_legacy,
            "integration_router": "active",
        }


# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_slack_plugin = SlackPlugin()
get_plugin_registry().register(_slack_plugin)
