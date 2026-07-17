"""
Integration Health Check API Routes
Issue #530: ALPHA-SETUP-VERIFY - Integration Health Check Dashboard

Provides API endpoints for checking and testing integration health status.
"""

import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.health.integration_health_monitor import ComponentStatus, IntegrationHealthMonitor

logger = structlog.get_logger()

# Router for integration health endpoints
router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


class IntegrationStatus(BaseModel):
    """Status information for a single integration"""

    name: str
    display_name: str
    status: str  # healthy, degraded, failed, unknown, not_configured
    status_message: str
    last_check: Optional[str] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None
    configure_url: Optional[str] = None
    can_test: bool = True


class IntegrationHealthResponse(BaseModel):
    """Response model for integration health check"""

    overall_status: str
    timestamp: str
    integrations: List[IntegrationStatus]
    healthy_count: int
    total_count: int


class ConnectionTestResponse(BaseModel):
    """Response model for testing a single connection"""

    integration: str
    success: bool
    message: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None


# Integration metadata and error guidance
INTEGRATION_REGISTRY = {
    "notion": {
        "display_name": "Notion",
        "icon": "📝",
        "configure_url": "/settings/integrations/notion",  # Issue #540: Dedicated settings page
        "errors": {
            "api_key_invalid": {
                "message": "Invalid Notion API key",
                "fix": "Check your Notion integration token in Settings → Integrations → Notion",
            },
            "connection_failed": {
                "message": "Cannot connect to Notion API",
                "fix": "Check your internet connection and Notion service status",
            },
            "permission_denied": {
                "message": "Integration lacks required permissions",
                "fix": "Ensure the integration has access to the required databases in Notion",
            },
        },
    },
    "slack": {
        "display_name": "Slack",
        "icon": "💬",
        "configure_url": "/settings/integrations/slack",  # Issue #528: Dedicated settings page
        "errors": {
            "token_expired": {
                "message": "Slack OAuth token has expired",
                "fix": "Re-authorize Slack in Settings → Integrations → Slack",
            },
            "token_invalid": {
                "message": "Invalid Slack token",
                "fix": "Re-connect your Slack workspace",
            },
            "scope_missing": {
                "message": "Missing required Slack permissions",
                "fix": "Re-authorize with updated permissions",
            },
        },
    },
    "github": {
        "display_name": "GitHub",
        "icon": "🐙",
        "configure_url": "/settings/integrations/github",
        "errors": {
            "token_invalid": {
                "message": "Invalid GitHub token",
                "fix": "Update your GitHub personal access token in Settings",
            },
            "rate_limited": {
                "message": "GitHub API rate limit exceeded",
                "fix": "Wait for rate limit reset or use authenticated requests",
            },
            "repo_not_found": {
                "message": "Repository not found or inaccessible",
                "fix": "Check repository permissions and token scope",
            },
        },
    },
    "calendar": {
        "display_name": "Google Calendar",
        "icon": "📅",
        "configure_url": "/settings/integrations/calendar",  # Issue #537: Dedicated settings page
        "errors": {
            "auth_failed": {
                "message": "Calendar authentication failed",
                "fix": "Re-authorize Google Calendar access",
            },
            "mcp_not_running": {
                "message": "Calendar MCP server not running",
                "fix": "Start the Google Calendar MCP server",
            },
        },
    },
}

# Module-level health monitor instance for tracking test results
_health_monitor: Optional[IntegrationHealthMonitor] = None


def _get_health_monitor() -> IntegrationHealthMonitor:
    """Get or create the health monitor singleton"""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = IntegrationHealthMonitor()
        # Register all integrations
        for integration_id in INTEGRATION_REGISTRY.keys():
            _health_monitor.register_component(integration_id, ComponentStatus.UNKNOWN)
    return _health_monitor


def _get_error_guidance(integration: str, error_type: str) -> tuple[str, Optional[str]]:
    """Get user-friendly error message and fix suggestion"""
    registry = INTEGRATION_REGISTRY.get(integration, {})
    errors = registry.get("errors", {})
    error_info = errors.get(error_type, {})

    message = error_info.get("message", f"Error: {error_type}")
    fix = error_info.get("fix")

    return message, fix


@router.get("/health", response_model=IntegrationHealthResponse)
async def get_integrations_health(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get health status of all configured integrations.

    Returns status information for Notion, Slack, GitHub, Calendar, etc.
    Issue #530: ALPHA-SETUP-VERIFY

    2026-05-21: Added auth dependency to thread user_id down to per-integration
    config-status checks. Without it, user-scoped credentials in keychain
    (like Slack tokens stored under user_id per ADR-058) are invisible to the
    config-status check and integrations forever appear "Not configured" after
    successful OAuth.
    """
    try:
        integrations = []
        healthy_count = 0

        # Check each integration
        for integration_id, metadata in INTEGRATION_REGISTRY.items():
            integration_status = await _check_integration_health(
                integration_id, metadata, user_id=current_user.sub
            )
            integrations.append(integration_status)
            if integration_status.status == "healthy":
                healthy_count += 1

        # Determine overall status
        total = len(integrations)
        if healthy_count == total:
            overall = "healthy"
        elif healthy_count > 0:
            overall = "degraded"
        else:
            overall = "unhealthy"

        return IntegrationHealthResponse(
            overall_status=overall,
            timestamp=datetime.now(timezone.utc).isoformat(),
            integrations=integrations,
            healthy_count=healthy_count,
            total_count=total,
        )

    except Exception as e:
        logger.error("Failed to check integrations health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/test/{integration_name}", response_model=ConnectionTestResponse)
async def check_integration_connection(
    integration_name: str, current_user: JWTClaims = Depends(get_current_user)
):
    """
    Test connection to a specific integration.

    Performs an active health check and returns detailed results.
    Issue #530: ALPHA-SETUP-VERIFY
    """
    if integration_name not in INTEGRATION_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown integration: {integration_name}",
        )

    metadata = INTEGRATION_REGISTRY[integration_name]
    start_time = time.time()
    health_monitor = _get_health_monitor()

    try:
        result = await _test_integration(integration_name, user_id=current_user.sub)
        latency_ms = (time.time() - start_time) * 1000

        if result["success"]:
            # Record success in health monitor
            health_monitor.record_success(integration_name, latency_ms)
            return ConnectionTestResponse(
                integration=integration_name,
                success=True,
                message=f"{metadata['display_name']} connection successful",
                latency_ms=round(latency_ms, 2),
            )
        else:
            # Record failure in health monitor
            error_msg = result.get("error", result.get("error_type", "Unknown error"))
            health_monitor.record_failure(integration_name, error_msg)
            message, fix = _get_error_guidance(
                integration_name, result.get("error_type", "unknown")
            )
            return ConnectionTestResponse(
                integration=integration_name,
                success=False,
                message=message,
                latency_ms=round(latency_ms, 2),
                error=result.get("error"),
                fix_suggestion=fix,
            )

    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        # Record failure in health monitor
        health_monitor.record_failure(integration_name, str(e))
        logger.error(f"Integration test failed: {integration_name}", error=str(e))
        return ConnectionTestResponse(
            integration=integration_name,
            success=False,
            message=f"Test failed: {str(e)}",
            latency_ms=round(latency_ms, 2),
            error=str(e),
            fix_suggestion="Check logs for details or contact support",
        )


@router.post("/test-all", response_model=List[ConnectionTestResponse])
async def check_all_connections(current_user: JWTClaims = Depends(get_current_user)):
    """
    Test all configured integrations.

    Issue #530: ALPHA-SETUP-VERIFY
    """
    results = []
    for integration_name in INTEGRATION_REGISTRY.keys():
        try:
            result = await check_integration_connection(integration_name, current_user=current_user)
            results.append(result)
        except Exception as e:
            results.append(
                ConnectionTestResponse(
                    integration=integration_name,
                    success=False,
                    message=f"Test failed: {str(e)}",
                    error=str(e),
                )
            )
    return results


async def _github_oauth_bound(user_id: Optional[str]) -> bool:
    """True if the user has a BOUND github OAuth-connector binding (#1329 / ADR-070 C).

    GitHub health follows the OAuth connector after the #1322 cutover, not the legacy
    native PAT — so a dead/expired PAT must NOT make GitHub read as unhealthy when the
    connector is bound and the chat reads work through it. Mirrors the binding check in
    ``GET /github/oauth-status``.
    """
    if not user_id:
        return False
    try:
        from services.connectors.binding_repository import ConnectorBindingRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.mcp.consumer.connector import ConnectorStatusState

        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, "github")
        return binding is not None and binding.status == ConnectorStatusState.BOUND.value
    except Exception as e:
        logger.warning("github oauth-binding health check failed", error=str(e))
        return False


async def _check_integration_health(
    integration_id: str, metadata: Dict[str, Any], user_id: Optional[str] = None
) -> IntegrationStatus:
    """Check health of a specific integration without active testing.

    Args:
        integration_id: integration name (e.g. "slack", "calendar")
        metadata: registry entry from INTEGRATION_REGISTRY
        user_id: authenticated user id (used to look up user-scoped keychain
            credentials per ADR-058; if None, only env-var configuration is
            visible — fine for non-user-scoped integrations).
    """
    try:
        # RECONNECT (#1329): GitHub health follows the OAuth connector binding, not the
        # legacy native PAT. A BOUND connector → healthy (the chat reads go through it),
        # even if the old PAT is expired. Takes precedence over the native config/health.
        if integration_id == "github" and await _github_oauth_bound(user_id):
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status="healthy",
                status_message="Connected via OAuth (MCP connector)",
                configure_url=metadata.get("configure_url"),
                can_test=True,
            )

        # Try to get cached health status or check configuration
        config_status = await _get_integration_config_status(integration_id, user_id=user_id)

        if config_status == "not_configured":
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status="not_configured",
                status_message="Not configured",
                configure_url=metadata.get("configure_url"),
                can_test=False,
            )

        # Get cached health status from IntegrationHealthMonitor
        health_monitor = _get_health_monitor()
        component_health = health_monitor.get_component_health(integration_id)

        if component_health and component_health.last_check > 0:
            # Map ComponentStatus to our status strings
            status_map = {
                ComponentStatus.HEALTHY: "healthy",
                ComponentStatus.DEGRADED: "degraded",
                ComponentStatus.FAILED: "failed",
                ComponentStatus.UNKNOWN: "unknown",
            }
            status_str = status_map.get(component_health.status, "unknown")

            # Convert timestamp to ISO string
            last_check_dt = datetime.fromtimestamp(component_health.last_check, tz=timezone.utc)
            last_check_str = last_check_dt.isoformat()

            # Build status message based on last check
            if status_str == "healthy":
                status_message = f"Healthy (last checked: {last_check_str[:16]})"
            elif status_str == "failed":
                status_message = component_health.last_error or "Connection failed"
            else:
                status_message = f"Status: {status_str}"

            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status=status_str,
                status_message=status_message,
                last_check=last_check_str,
                error=component_health.last_error,
                configure_url=metadata.get("configure_url"),
                can_test=True,
            )

        # Fallback for configured but never-tested integrations
        return IntegrationStatus(
            name=integration_id,
            display_name=metadata["display_name"],
            status="unknown",
            status_message="Click 'Test' to check connection",
            configure_url=metadata.get("configure_url"),
            can_test=True,
        )

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} health", error=str(e))
        return IntegrationStatus(
            name=integration_id,
            display_name=metadata["display_name"],
            status="unknown",
            status_message="Status unknown",
            error=str(e),
            configure_url=metadata.get("configure_url"),
            can_test=True,
        )


async def _get_integration_config_status(integration_id: str, user_id: Optional[str] = None) -> str:
    """Check if an integration is configured by checking environment variables"""
    import os

    try:
        # Check integration-specific environment variables
        if integration_id == "notion":
            if os.environ.get("NOTION_API_TOKEN") or os.environ.get("NOTION_API_KEY"):
                return "configured"
            # #1337: user-scoped path. save_notion_key stores the key in the #358
            # user-secret store (UserAPIKeyService, provider "notion") — NOT the keychain
            # that slack/calendar use. Health was env-only and missed this, so a
            # UI-configured Notion read "not configured." Mirror the user-scoped intent.
            if user_id:
                try:
                    from services.database.session_factory import AsyncSessionFactory
                    from services.security.user_api_key_service import UserAPIKeyService

                    async with AsyncSessionFactory.session_scope_fresh() as session:
                        if await UserAPIKeyService().retrieve_user_key(
                            session, user_id, "notion"
                        ):
                            return "configured"
                except Exception:
                    pass
        elif integration_id == "slack":
            # Env-var path (production / explicit-config deployment)
            if os.environ.get("SLACK_BOT_TOKEN"):
                return "configured"
            # Keychain path (OAuth-completed deployment per ADR-058 — bot token
            # stored under user-scoped keychain key after a successful OAuth
            # callback). Mirrors the calendar branch below.
            if user_id:
                try:
                    from services.infrastructure.keychain_service import KeychainService

                    keychain = KeychainService()
                    if keychain.get_api_key("slack_bot", username=user_id):
                        return "configured"
                except Exception:
                    pass
        elif integration_id == "github":
            if os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_ACCESS_TOKEN"):
                return "configured"
        elif integration_id == "calendar":
            # Calendar uses keychain token (Issue #529) or legacy MCP/credentials
            # Issue #839: Use user-scoped key when user_id available
            try:
                from services.infrastructure.keychain_service import KeychainService

                keychain = KeychainService()
                key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
                if keychain.get_api_key(key_name):
                    return "configured"
            except Exception:
                pass
            # Fallback to legacy check
            if os.environ.get("GOOGLE_CALENDAR_CREDENTIALS") or os.environ.get("MCP_ENABLED"):
                return "configured"

        return "not_configured"

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} config", error=str(e))
        return "unknown"


async def _test_integration(integration_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Perform active connection test for an integration"""
    try:
        if integration_id == "notion":
            return await _test_notion(user_id=user_id)
        elif integration_id == "slack":
            return await _test_slack(user_id=user_id)
        elif integration_id == "github":
            return await _test_github(user_id=user_id)
        elif integration_id == "calendar":
            return await _test_calendar(user_id=user_id)
        else:
            return {"success": False, "error": f"Unknown integration: {integration_id}"}

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_notion(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Notion API connection using stored API key (Issue #562).

    #1436 B16: get_config requires a principal — the acting user's key when
    present, the "system" marker otherwise (the router:157 convention), same
    as the sibling _test_slack/_test_github helpers.
    """
    try:
        import aiohttp

        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()
        config = config_service.get_config(user_id or "system")
        api_key = config.api_key

        if not api_key:
            return {
                "success": False,
                "error": "Notion not connected. Please add your API key.",
                "error_type": "not_configured",
            }

        # Test with users/me endpoint using stored API key
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.notion.com/v1/users/me",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28",
                },
            ) as response:
                if response.status == 200:
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": "API key invalid or expired",
                        "error_type": "api_key_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_slack(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Slack API connection using stored OAuth token (Issue #562)"""
    try:
        import aiohttp

        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        token = (
            keychain.get_api_key("slack_bot", username=user_id)
            if user_id
            else keychain.get_api_key("slack_bot")
        )  # Issue #849: Correct key name + user-scoped

        if not token:
            return {
                "success": False,
                "error": "Slack not connected. Click Connect to authorize.",
                "error_type": "not_configured",
            }

        # Test with auth.test endpoint using stored OAuth token
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://slack.com/api/auth.test",
                headers={"Authorization": f"Bearer {token}"},
            ) as response:
                data = await response.json()

                if data.get("ok"):
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Token invalid or expired"),
                        "error_type": "token_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_github(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test GitHub connection (Issue #562).

    #1329: the OAuth connector is the live read path post-#1322 cutover, so a BOUND
    connector means "connected" regardless of the legacy native PAT — report success
    and skip the native-PAT probe. Falls back to the native PAT test only when there is
    no OAuth binding.
    """
    try:
        # #1329: OAuth connector takes precedence — a bound connector is connected.
        if await _github_oauth_bound(user_id):
            return {"success": True, "message": "Connected via OAuth (MCP connector)"}

        import aiohttp

        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        token = (
            keychain.get_api_key("github_token", username=user_id)
            if user_id
            else keychain.get_api_key("github_token")
        )  # Issue #849: Correct key name + user-scoped

        if not token:
            return {
                "success": False,
                "error": "GitHub not connected. Please add your token.",
                "error_type": "not_configured",
            }

        # Test with user endpoint using stored PAT
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            ) as response:
                if response.status == 200:
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": "Token invalid or expired",
                        "error_type": "token_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_calendar(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Google Calendar OAuth connection (Issue #539)"""
    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        keychain = KeychainService()
        # Issue #839: Use user-scoped key when user_id available
        key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
        refresh_token = keychain.get_api_key(key_name)

        if not refresh_token:
            return {
                "success": False,
                "error": "Calendar not connected. Click Connect to authorize.",
                "error_type": "not_configured",
            }

        # Validate by attempting to refresh the token (Issue #539)
        handler = GoogleCalendarOAuthHandler()
        tokens = await handler.refresh_access_token(refresh_token)

        if tokens:
            return {"success": True}
        else:
            return {
                "success": False,
                "error": "Token expired or revoked. Please reconnect.",
                "error_type": "token_invalid",
            }

    except ImportError:
        return {"success": False, "error": "Calendar integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
