"""
GitHub Integration Plugin

Wraps GitHub integration as a PiperPlugin for auto-registration
with the plugin system.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata

from .config_service import GitHubConfigService
from .github_integration_router import GitHubIntegrationRouter


class GitHubPlugin(PiperPlugin):
    """
    GitHub repository integration plugin.

    Provides GitHub integration routes and capabilities through
    the plugin system.
    """

    def __init__(self):
        """Initialize GitHub plugin with config service"""
        self.config_service = GitHubConfigService()
        self.integration_router = GitHubIntegrationRouter(self.config_service)
        self._api_router: Optional[APIRouter] = None

    def get_metadata(self) -> PluginMetadata:
        """Return GitHub plugin metadata"""
        return PluginMetadata(
            name="github",
            version="1.0.0",
            description="GitHub repository integration with spatial intelligence",
            author="Piper Morgan Team",
            capabilities=["routes", "spatial"],
            dependencies=[],
        )

    def get_router(self) -> Optional[APIRouter]:
        """
        Return FastAPI router with GitHub routes.

        Creates APIRouter wrapper around GitHubIntegrationRouter.
        """
        if self._api_router is None:
            self._api_router = APIRouter(prefix="/api/v1/integrations/github", tags=["github"])
            # #1547 (audit F5): the GET /status sub-route is DELETED — it served
            # `configured: false` forever, for everyone (is_configured() is
            # hardcoded False without user context, #784). Truthful status lives
            # at /api/v1/integrations/health (user-scoped, binding-first).

        return self._api_router

    def is_configured(self) -> bool:
        """Check if GitHub is properly configured.

        Note: At plugin startup, there's no user context available.
        This returns False until a user context is established.
        Issue #784: Fixed crash from calling is_configured() without user_id.
        """
        # Without user context, we can't determine configuration
        # The config_service.is_configured() requires user_id (Issue #734)
        return False

    async def initialize(self) -> None:
        """Initialize GitHub plugin"""
        if self.is_configured():
            print(
                f"  ✅ GitHub plugin initialized (spatial: {self.integration_router.use_spatial})"
            )
        else:
            print(f"  ⚠️  GitHub plugin initialized but not configured")

    async def shutdown(self) -> None:
        """Cleanup GitHub plugin resources"""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get GitHub plugin status.

        #1547: `configured` is None, not False — configuration is user-scoped
        and unknowable at plugin level (#784), so a boolean here was a
        structural lie every registry consumer inherited. Callers needing real
        status use services/integrations/integration_status_service.py.
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

_github_plugin = GitHubPlugin()
get_plugin_registry().register(_github_plugin)
