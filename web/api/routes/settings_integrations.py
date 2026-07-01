"""
Settings Integrations API Routes

Provides OAuth connection management for the Settings page.
Allows users to connect/disconnect OAuth-based integrations
(Slack, Calendar) after initial setup is complete.

Issue #529: ALPHA-SETUP-CALENDAR (Settings integration)
Issue #570: Slack Channel Selection Settings
"""

import json
import os
from typing import List, Optional
from urllib.parse import quote

import structlog
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims

# #1327 gap 3: the Settings repo-config dropdown reads repos over the per-user OAuth connector
# (mirroring the #1322 chat-read cutover). Imported at module level so the connector-first rail
# in get_github_repositories is patchable in tests.
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/settings/integrations", tags=["settings-integrations"])


# ============================================================================
# Pydantic Models for Slack Preferences (Issue #570)
# ============================================================================


class SlackChannel(BaseModel):
    """Slack channel representation."""

    id: str
    name: str
    is_private: bool = False


class SlackChannelsResponse(BaseModel):
    """Response containing list of Slack channels."""

    channels: List[SlackChannel]


class SlackPreferencesRequest(BaseModel):
    """Request body for saving Slack preferences."""

    notification_channel: Optional[str] = None
    monitored_channels: List[str] = []
    default_response_channel: Optional[str] = None


class SlackPreferencesResponse(BaseModel):
    """Response containing Slack preferences."""

    notification_channel: Optional[str] = None
    monitored_channels: List[str] = []
    default_response_channel: Optional[str] = None


# ============================================================================
# Pydantic Models for Slack App Credentials (Issue #576)
# ============================================================================


class SlackAppCredentialsRequest(BaseModel):
    """Request body for saving Slack app credentials."""

    client_id: str
    client_secret: str


class SlackAppCredentialsStatusResponse(BaseModel):
    """Response for credential status check (never exposes actual values)."""

    configured: bool
    has_client_id: bool
    has_client_secret: bool


class SlackAppTokenRequest(BaseModel):
    """Request body for saving the Slack app-level token (#1201 inbound)."""

    app_token: str


class SlackInboundStatusResponse(BaseModel):
    """Inbound (Socket Mode) status for the settings surface (#1201).

    state: 'listening' (connected), 'connecting' (token set, not yet connected /
    connect failed), or 'not_enabled' (no app token stored).
    """

    connected: bool
    state: str


# ============================================================================
# Pydantic Models for Calendar App Credentials (Issue #577)
# ============================================================================


class CalendarAppCredentialsRequest(BaseModel):
    """Request body for saving Google Calendar app credentials."""

    client_id: str
    client_secret: str


class CalendarAppCredentialsStatusResponse(BaseModel):
    """Response for credential status check (never exposes actual values)."""

    configured: bool
    has_client_id: bool
    has_client_secret: bool


# ============================================================================
# Pydantic Models for Calendar Sync Preferences (Issue #571)
# ============================================================================


class CalendarInfo(BaseModel):
    """Google Calendar representation."""

    id: str
    name: str
    description: str = ""
    primary: bool = False
    selected: bool = False


class CalendarListResponse(BaseModel):
    """Response containing list of Google calendars."""

    calendars: List[CalendarInfo]


class CalendarPreferencesRequest(BaseModel):
    """Request body for saving calendar preferences."""

    selected_calendars: List[str]
    primary_calendar: str


class CalendarPreferencesResponse(BaseModel):
    """Response containing calendar preferences."""

    selected_calendars: List[str] = []
    primary_calendar: Optional[str] = None


# ============================================================================
# Pydantic Models for Notion Workspace Preferences (Issue #572)
# ============================================================================


class NotionDatabaseInfo(BaseModel):
    """Notion database representation."""

    id: str
    name: str
    description: str = ""
    selected: bool = False


class NotionDatabaseListResponse(BaseModel):
    """Response containing list of Notion databases."""

    databases: List[NotionDatabaseInfo]


class NotionPreferencesRequest(BaseModel):
    """Request body for saving Notion preferences."""

    selected_databases: List[str]
    default_database: str


class NotionPreferencesResponse(BaseModel):
    """Response containing Notion preferences."""

    selected_databases: List[str] = []
    default_database: Optional[str] = None


# ============================================================================
# Pydantic Models for GitHub Repository Preferences (Issue #573)
# ============================================================================


class GitHubRepositoryInfo(BaseModel):
    """GitHub repository representation."""

    id: int
    name: str
    full_name: str
    description: str = ""
    selected: bool = False


class GitHubRepositoryListResponse(BaseModel):
    """Response containing list of GitHub repositories."""

    repositories: List[GitHubRepositoryInfo]


class GitHubPreferencesRequest(BaseModel):
    """Request body for saving GitHub preferences."""

    selected_repositories: List[str]  # full_name format
    default_repository: str


class GitHubPreferencesResponse(BaseModel):
    """Response containing GitHub preferences."""

    selected_repositories: List[str] = []
    default_repository: Optional[str] = None


# Simple file-based storage for Slack preferences (Issue #570)
# This is a minimal implementation - could be moved to DB later
SLACK_PREFERENCES_FILE = "data/slack_preferences.json"


def _load_slack_preferences() -> dict:
    """Load all Slack preferences from file."""
    try:
        if os.path.exists(SLACK_PREFERENCES_FILE):
            with open(SLACK_PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("slack_preferences_load_failed", error=str(e))
    return {}


def _save_slack_preferences(prefs: dict) -> None:
    """Save all Slack preferences to file."""
    try:
        os.makedirs(os.path.dirname(SLACK_PREFERENCES_FILE), exist_ok=True)
        with open(SLACK_PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        logger.error("slack_preferences_save_failed", error=str(e))


# Simple file-based storage for Calendar preferences (Issue #571)
# Same pattern as Slack - could be moved to DB later
CALENDAR_PREFERENCES_FILE = "data/calendar_preferences.json"


def _load_calendar_preferences() -> dict:
    """Load all calendar preferences from file."""
    try:
        if os.path.exists(CALENDAR_PREFERENCES_FILE):
            with open(CALENDAR_PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("calendar_preferences_load_failed", error=str(e))
    return {}


def _save_calendar_preferences(prefs: dict) -> None:
    """Save all calendar preferences to file."""
    try:
        os.makedirs(os.path.dirname(CALENDAR_PREFERENCES_FILE), exist_ok=True)
        with open(CALENDAR_PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        logger.error("calendar_preferences_save_failed", error=str(e))


# Simple file-based storage for Notion preferences (Issue #572)
# Same pattern as Slack and Calendar - could be moved to DB later
NOTION_PREFERENCES_FILE = "data/notion_preferences.json"


def _load_notion_preferences() -> dict:
    """Load all Notion preferences from file."""
    try:
        if os.path.exists(NOTION_PREFERENCES_FILE):
            with open(NOTION_PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("notion_preferences_load_failed", error=str(e))
    return {}


def _save_notion_preferences(prefs: dict) -> None:
    """Save all Notion preferences to file."""
    try:
        os.makedirs(os.path.dirname(NOTION_PREFERENCES_FILE), exist_ok=True)
        with open(NOTION_PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        logger.error("notion_preferences_save_failed", error=str(e))


# WS-1 (#1226 / #1199): GitHub connector prefs live in the DB-backed connector_configs store
# (ADR-070 D4). The flat-file store (data/github_preferences.json) + the in-memory
# UserPreferenceManager were RETIRED 2026-06-21 — there is now ONE canonical store. These two
# helpers are the single read/write path for the github config blob
# ({selected_repositories, default_repository, github_username}).
async def _load_github_prefs_db(owner_sub: str) -> dict:
    """The user's github connector config from the DB store. Returns {} on miss OR DB error
    (best-effort read — a settings page should still render if the DB hiccups)."""
    try:
        from services.connectors.config_service import ConnectorConfigService
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope_fresh() as session:
            return await ConnectorConfigService(session).get_config(owner_sub, "github")
    except Exception as e:
        logger.warning("github_prefs_db_load_failed", error=str(e))
        return {}


async def _save_github_prefs_db(owner_sub: str, prefs: dict) -> None:
    """MERGE the given keys into the user's github connector config in the DB store (preserves
    untouched keys like github_username). RAISES on failure — the DB is the only store now, so a
    write error must surface (silent failure would be data loss). Fresh-engine session
    (event-loop-safe #442) + explicit commit (session_scope_fresh doesn't auto-commit)."""
    from services.connectors.config_service import ConnectorConfigService
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as session:
        svc = ConnectorConfigService(session)
        merged = await svc.get_config(owner_sub, "github")
        merged.update(prefs)
        await svc.set_config(owner_sub, "github", merged)
        await session.commit()


# ============================================================================
# Slack OAuth for Settings
# ============================================================================


@router.get("/slack/connect")
async def connect_slack(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Start Slack OAuth flow from Settings page.

    Issue #734: SEC-MULTITENANCY - Requires authentication, embeds user_id in state.

    Returns authorization URL for OAuth. After completion,
    redirects back to /settings/integrations with status.
    """
    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()

        # Use settings-specific redirect URI
        redirect_uri = os.getenv(
            "SLACK_SETTINGS_REDIRECT_URI",
            os.getenv(
                "SLACK_REDIRECT_URI",
                "http://localhost:8001/api/v1/settings/integrations/slack/callback",
            ),
        )

        # Issue #734: Pass user_id for multi-tenant state
        # Issue #1109: generate_authorization_url is async (Redis-backed state)
        auth_url, state = await handler.generate_authorization_url(
            user_id=current_user.sub, redirect_uri=redirect_uri if redirect_uri else None
        )

        logger.info(
            "slack_settings_oauth_started", user_id=current_user.sub, state=state[:8] + "..."
        )

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except Exception as e:
        logger.error("slack_settings_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Slack OAuth: {str(e)}",
        )


@router.get("/slack/callback")
async def handle_slack_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Slack OAuth callback for Settings page.

    Issue #734: SEC-MULTITENANCY - user_id extracted from state and used
    for per-user token storage in SlackOAuthHandler.

    Redirects back to /settings/integrations with status.
    """
    # Handle OAuth error
    if error:
        logger.warning("slack_settings_oauth_denied", error=error)
        return RedirectResponse(url=f"/settings/integrations?slack_error={error}", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning(
            "slack_settings_oauth_missing_params", has_code=bool(code), has_state=bool(state)
        )
        return RedirectResponse(
            url="/settings/integrations?slack_error=missing_params", status_code=302
        )

    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Issue #734: user_id is already extracted and used for storage in handler
        user_id = result.get("user_id")

        workspace_name = result.get("workspace", {}).get("workspace_name", "Workspace")
        workspace_name_encoded = quote(workspace_name)

        logger.info("slack_settings_oauth_success", user_id=user_id, workspace=workspace_name)

        return RedirectResponse(
            url=f"/settings/integrations?slack_success=true&slack_workspace={workspace_name_encoded}",
            status_code=302,
        )

    except ValueError as e:
        logger.warning("slack_settings_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/settings/integrations?slack_error=callback_failed", status_code=302
        )
    except Exception as e:
        logger.error("slack_settings_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/settings/integrations?slack_error=callback_failed", status_code=302
        )


@router.post("/slack/disconnect")
async def disconnect_slack(current_user: JWTClaims = Depends(get_current_user)):
    """
    Disconnect Slack integration.

    Removes the user-scoped stored tokens (keychain, #849), revokes OAuth access on
    Slack's side, and clears the Slack env vars. #1334 P1 consolidated the duplicate
    route; #1334-P2 delegates the clearing to the uniform `disconnect_connector` helper.
    """
    try:
        from services.connectors.disconnect import disconnect_connector

        await disconnect_connector(current_user.sub, "slack")
        logger.info("slack_disconnected")

        return {
            "success": True,
            "message": "Slack disconnected",
        }

    except Exception as e:
        logger.error("slack_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Slack: {str(e)}",
        )


# ============================================================================
# Slack Channel Preferences (Issue #570)
# ============================================================================


@router.get("/slack/channels", response_model=SlackChannelsResponse)
async def get_slack_channels(current_user: JWTClaims = Depends(get_current_user)):
    """
    Fetch available Slack channels for the user.

    Returns list of channels the Slack bot has access to.
    Issue #570: Slack Channel Selection Settings
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.slack_client import SlackClient

        # #1110: SlackClient requires a config_service AND a user_id (ADR-058
        # multi-tenancy). This route has the authenticated user in scope.
        client = SlackClient(config_service=SlackConfigService(), user_id=current_user.sub)
        response = await client.list_channels()

        if not response.success:
            logger.warning(
                "slack_channels_fetch_failed",
                error=response.error.message if response.error else "Unknown error",
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to fetch Slack channels: {response.error.message if response.error else 'Unknown error'}",
            )

        # Parse channels from Slack API response
        channels_data = response.data.get("channels", [])
        channels = [
            SlackChannel(
                id=ch.get("id", ""),
                name=ch.get("name", ""),
                is_private=ch.get("is_private", False),
            )
            for ch in channels_data
            if ch.get("id") and ch.get("name")
        ]

        logger.info("slack_channels_fetched", count=len(channels))

        return SlackChannelsResponse(channels=channels)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("slack_channels_fetch_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch Slack channels: {str(e)}",
        )


@router.get("/slack/preferences", response_model=SlackPreferencesResponse)
async def get_slack_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved Slack preferences for the current user.

    Returns notification channel, monitored channels, and default response channel.
    Issue #570: Slack Channel Selection Settings
    """
    try:
        all_prefs = _load_slack_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})

        logger.info("slack_preferences_loaded", user_id=str(current_user.sub))

        return SlackPreferencesResponse(
            notification_channel=user_prefs.get("notification_channel"),
            monitored_channels=user_prefs.get("monitored_channels", []),
            default_response_channel=user_prefs.get("default_response_channel"),
        )

    except Exception as e:
        logger.error("slack_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load Slack preferences: {str(e)}",
        )


@router.post("/slack/preferences", response_model=SlackPreferencesResponse)
async def save_slack_preferences(
    preferences: SlackPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save Slack preferences for the current user.

    Stores notification channel, monitored channels, and default response channel.
    Issue #570: Slack Channel Selection Settings
    """
    try:
        all_prefs = _load_slack_preferences()

        # Store preferences for this user
        user_prefs = {
            "notification_channel": preferences.notification_channel,
            "monitored_channels": preferences.monitored_channels,
            "default_response_channel": preferences.default_response_channel,
        }

        all_prefs[str(current_user.sub)] = user_prefs
        _save_slack_preferences(all_prefs)

        logger.info(
            "slack_preferences_saved",
            user_id=str(current_user.sub),
            notification_channel=preferences.notification_channel,
            monitored_count=len(preferences.monitored_channels),
        )

        return SlackPreferencesResponse(
            notification_channel=preferences.notification_channel,
            monitored_channels=preferences.monitored_channels,
            default_response_channel=preferences.default_response_channel,
        )

    except Exception as e:
        logger.error("slack_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Slack preferences: {str(e)}",
        )


# ============================================================================
# Slack App Credentials Management (Issue #576)
# ============================================================================


@router.post("/slack/app-credentials")
async def save_slack_app_credentials(
    credentials: SlackAppCredentialsRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save Slack app credentials to secure keychain storage.

    Stores client_id and client_secret for OAuth flow.
    Issue #576: OAuth App Credential Configuration in UI
    Issue #734: Uses IntegrationConfigService for app credentials

    Security: Credentials are stored in OS keychain, never logged or exposed.
    """
    from services.integrations.integration_config_service import IntegrationConfigService

    try:
        # Validate both fields are non-empty
        if not credentials.client_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="client_id is required and cannot be empty",
            )
        if not credentials.client_secret.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="client_secret is required and cannot be empty",
            )

        # Store via IntegrationConfigService (Issue #734)
        config_service = IntegrationConfigService()
        config_service.store_slack_credentials(
            credentials.client_id.strip(), credentials.client_secret.strip()
        )

        logger.info(
            "slack_app_credentials_saved",
            user_id=str(current_user.sub),
        )

        return {"success": True, "message": "Slack app credentials saved securely"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("slack_app_credentials_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Slack app credentials: {str(e)}",
        )


@router.post("/slack/app-token")
async def save_slack_app_token(
    body: SlackAppTokenRequest,
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
) -> SlackInboundStatusResponse:
    """Save the Slack app-level token (xapp-) + start inbound Socket Mode (#1201).

    Enables inbound replies (DM the bot / @mention → Piper responds). The app-level
    token is a single per-app credential (global keychain `slack_app_token`), independent
    of the per-user OAuth bot/user tokens — additive, doesn't touch the OAuth flow. On
    save we (re)start the Socket Mode runner at runtime (no app restart) and return the
    resulting inbound state so the UI can flip the badge.

    Security: stored via KeychainService (the `_api_key`-suffix contract), never logged.
    """
    from services.infrastructure.keychain_service import KeychainService
    from services.integrations.slack.socket_mode_runner import restart_socket_runner

    token = (body.app_token or "").strip()
    # Slack app-level tokens are `xapp-…`; reject anything else with a clear message.
    if not token.startswith("xapp-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "That doesn't look like an app-level token — they start with 'xapp-'. "
                "Check you copied the right one from Basic Information → App-Level Tokens."
            ),
        )

    try:
        # Global (per-app) key — the Socket Mode runner reads `slack_app_token` unscoped.
        KeychainService().store_api_key("slack_app_token", token)
        logger.info("slack_app_token_saved", user_id=str(current_user.sub))

        # Start-on-save: (re)build + connect the runner at runtime.
        runner = await restart_socket_runner(request.app)
        connected = bool(runner and runner.is_connected)
        state = "listening" if connected else "connecting"
        return SlackInboundStatusResponse(connected=connected, state=state)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("slack_app_token_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Slack app token: {str(e)}",
        )


@router.get("/slack/inbound/status", response_model=SlackInboundStatusResponse)
async def get_slack_inbound_status(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
) -> SlackInboundStatusResponse:
    """Inbound (Socket Mode) status for the Settings→Slack surface (#1201).

    Composes the 3-state view from app-token presence + the runner's live connection:
    - no app token → 'not_enabled' (gray)
    - token present + runner connected → 'listening' (green)
    - token present + runner absent/not-connected → 'connecting' (yellow)
    """
    from services.infrastructure.keychain_service import KeychainService

    has_token = bool(
        os.getenv("SLACK_APP_TOKEN") or KeychainService().get_api_key("slack_app_token")
    )
    if not has_token:
        return SlackInboundStatusResponse(connected=False, state="not_enabled")

    runner = getattr(request.app.state, "slack_socket_runner", None)
    connected = bool(runner and getattr(runner, "is_connected", False))
    return SlackInboundStatusResponse(
        connected=connected, state="listening" if connected else "connecting"
    )


@router.get("/slack/app-credentials/status", response_model=SlackAppCredentialsStatusResponse)
async def get_slack_app_credentials_status(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Check if Slack app credentials are configured.

    Returns boolean status only - NEVER returns actual credential values.
    Issue #576: OAuth App Credential Configuration in UI
    """
    from services.integrations.slack.config_service import SlackConfigService

    try:
        config_service = SlackConfigService()
        # #1120: get_config requires user_id (refactor-miss recovery)
        config = config_service.get_config(user_id=current_user.sub)

        has_client_id = bool(config.client_id)
        has_client_secret = bool(config.client_secret)
        configured = has_client_id and has_client_secret

        return SlackAppCredentialsStatusResponse(
            configured=configured,
            has_client_id=has_client_id,
            has_client_secret=has_client_secret,
        )

    except Exception as e:
        logger.error("slack_app_credentials_status_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check Slack app credentials status: {str(e)}",
        )


# ============================================================================
# Google Calendar App Credentials Management (Issue #577)
# ============================================================================


@router.post("/calendar/app-credentials")
async def save_calendar_app_credentials(
    credentials: CalendarAppCredentialsRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save Google Calendar app credentials to secure keychain storage.

    Stores client_id and client_secret for OAuth flow.
    Issue #577: Google Calendar OAuth Credential Configuration in UI
    Issue #734: Uses IntegrationConfigService for app credentials

    Security: Credentials are stored in OS keychain, never logged or exposed.
    """
    from services.integrations.integration_config_service import IntegrationConfigService

    try:
        # Validate both fields are non-empty
        if not credentials.client_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="client_id is required and cannot be empty",
            )
        if not credentials.client_secret.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="client_secret is required and cannot be empty",
            )

        # Store via IntegrationConfigService (Issue #734)
        config_service = IntegrationConfigService()
        config_service.store_google_credentials(
            credentials.client_id.strip(), credentials.client_secret.strip()
        )

        logger.info(
            "calendar_app_credentials_saved",
            user_id=str(current_user.sub),
        )

        return {"success": True, "message": "Google Calendar app credentials saved securely"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_app_credentials_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Calendar app credentials: {str(e)}",
        )


@router.get("/calendar/app-credentials/status", response_model=CalendarAppCredentialsStatusResponse)
async def get_calendar_app_credentials_status(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Check if Google Calendar app credentials are configured.

    Returns boolean status only - NEVER returns actual credential values.
    Issue #577: Google Calendar OAuth Credential Configuration in UI
    Issue #734: Uses IntegrationConfigService for app credentials
    """
    from services.integrations.integration_config_service import IntegrationConfigService

    try:
        config_service = IntegrationConfigService()

        # Check via IntegrationConfigService (Issue #734)
        client_id = config_service.get_google_client_id() or ""
        client_secret = config_service.get_google_client_secret() or ""

        # Also check environment variables as fallback
        if not client_id:
            client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        if not client_secret:
            client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")

        has_client_id = bool(client_id)
        has_client_secret = bool(client_secret)
        configured = has_client_id and has_client_secret

        return CalendarAppCredentialsStatusResponse(
            configured=configured,
            has_client_id=has_client_id,
            has_client_secret=has_client_secret,
        )

    except Exception as e:
        logger.error("calendar_app_credentials_status_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check Calendar app credentials status: {str(e)}",
        )


# ============================================================================
# Google Calendar OAuth for Settings (Issue #537)
# ============================================================================


@router.get("/calendar")
async def get_calendar_settings(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get Google Calendar integration status.

    Returns whether Calendar is configured and validates connection if token present.
    Issue #537: ALPHA-SETUP-MANAGE - Integration Management Post-Setup
    Issue #839: Use user-scoped keychain key
    """
    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        keychain = KeychainService()
        # Issue #839: Use user-scoped key to prevent cross-user leakage
        key_name = f"google_calendar_{current_user.sub}"
        refresh_token = keychain.get_api_key(key_name)

        if refresh_token:
            # Validate the token by attempting to refresh it
            handler = GoogleCalendarOAuthHandler()
            try:
                tokens = await handler.refresh_access_token(refresh_token)

                if tokens:
                    # Token is valid - try to get user info if possible
                    return {
                        "configured": True,
                        "valid": True,
                        "email": None,  # Would need additional API call to get email
                        "error": None,
                    }
                else:
                    return {
                        "configured": True,
                        "valid": False,
                        "email": None,
                        "error": "Token expired or revoked",
                    }
            except Exception as token_error:
                logger.warning("calendar_token_validation_failed", error=str(token_error))
                return {
                    "configured": True,
                    "valid": False,
                    "email": None,
                    "error": str(token_error),
                }
        else:
            return {
                "configured": False,
                "valid": False,
                "email": None,
                "error": None,
            }

    except Exception as e:
        logger.error("calendar_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "email": None,
            "error": str(e),
        }


@router.get("/calendar/connect")
async def connect_calendar(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Start Google Calendar OAuth flow from Settings page.

    Issue #734: SEC-MULTITENANCY - Requires authentication, embeds user_id in state.

    Returns authorization URL for OAuth. After completion,
    redirects back to /settings/integrations with status.
    """
    try:
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Verify credentials are configured
        if not handler.client_id or not handler.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Calendar OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            )

        # Override redirect URI for settings flow
        original_redirect = handler.redirect_uri
        handler.redirect_uri = os.getenv(
            "GOOGLE_SETTINGS_REDIRECT_URI",
            "http://localhost:8001/api/v1/settings/integrations/calendar/callback",
        )

        # Issue #734: Pass user_id for multi-tenant state
        auth_url, state = handler.generate_authorization_url(user_id=current_user.sub)

        # Restore original
        handler.redirect_uri = original_redirect

        logger.info(
            "calendar_settings_oauth_started", user_id=current_user.sub, state=state[:8] + "..."
        )

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_settings_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start Calendar OAuth: {str(e)}",
        )


@router.get("/calendar/callback")
async def handle_calendar_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Google Calendar OAuth callback for Settings page.

    Issue #734: SEC-MULTITENANCY - Extracts user_id from state for per-user storage.

    Redirects back to /settings/integrations with status.
    """
    # Handle OAuth error
    if error:
        logger.warning("calendar_settings_oauth_denied", error=error)
        return RedirectResponse(
            url=f"/settings/integrations?calendar_error={error}", status_code=302
        )

    # Handle missing parameters
    if not code or not state:
        logger.warning(
            "calendar_settings_oauth_missing_params", has_code=bool(code), has_state=bool(state)
        )
        return RedirectResponse(
            url="/settings/integrations?calendar_error=missing_params", status_code=302
        )

    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Override redirect URI to match what was used in authorization
        handler.redirect_uri = os.getenv(
            "GOOGLE_SETTINGS_REDIRECT_URI",
            "http://localhost:8001/api/v1/settings/integrations/calendar/callback",
        )

        result = await handler.handle_oauth_callback(code, state)

        # Issue #734: Extract user_id from callback result
        user_id = result.get("user_id")

        # Store refresh token securely with user-scoped key
        tokens = result["tokens"]
        if tokens.refresh_token:
            keychain = KeychainService()
            # Issue #734: Use user-scoped key for per-user storage
            key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
            keychain.store_api_key(key_name, tokens.refresh_token)
            logger.info("calendar_refresh_token_stored_settings", user_id=user_id)

        user_email = result["user"].get("email", "Calendar")
        email_encoded = quote(user_email)

        logger.info("calendar_settings_oauth_success", user_id=user_id, email=user_email)

        return RedirectResponse(
            url=f"/settings/integrations?calendar_success=true&calendar_email={email_encoded}",
            status_code=302,
        )

    except ValueError as e:
        logger.warning("calendar_settings_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/settings/integrations?calendar_error=callback_failed", status_code=302
        )
    except Exception as e:
        logger.error("calendar_settings_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/settings/integrations?calendar_error=callback_failed", status_code=302
        )


# ── GitHub connector OAuth (#1317 inc.2 / ADR-070 option C) ──
# Mirrors the calendar flow: connect → GitHub OAuth App authorize → callback stores the
# user's grant (encrypted #358 store) + marks the #1229 binding BOUND. The grant is
# forwarded (Authorization header) to our self-hosted github-mcp-server at resolve-time.
@router.get("/github/connect")
async def connect_github(
    current_user: JWTClaims = Depends(get_current_user),
):
    """Start the GitHub OAuth flow from Settings. Returns the authorization URL + state."""
    try:
        from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

        handler = GitHubOAuthHandler()
        if not handler.client_id or not handler.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="GitHub OAuth not configured (missing OAuth App client_id/secret).",
            )
        auth_url, state = handler.generate_authorization_url(user_id=current_user.sub)
        logger.info(
            "github_settings_oauth_started", user_id=current_user.sub, state=state[:8] + "..."
        )
        return {"auth_url": auth_url, "state": state}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("github_settings_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start GitHub OAuth: {str(e)}",
        )


@router.get("/github/callback")
async def handle_github_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """Handle the GitHub OAuth callback: verify state → exchange code → store the grant +
    mark the binding BOUND (#1317 inc.2). Redirects back to /settings/integrations."""
    if error:
        logger.warning("github_settings_oauth_denied", error=error)
        return RedirectResponse(url=f"/settings/integrations?github_error={error}", status_code=302)
    if not code or not state:
        logger.warning(
            "github_settings_oauth_missing_params", has_code=bool(code), has_state=bool(state)
        )
        return RedirectResponse(
            url="/settings/integrations?github_error=missing_params", status_code=302
        )
    try:
        from services.database.session_factory import AsyncSessionFactory
        from services.mcp.consumer.github_oauth_handler import (
            GitHubOAuthHandler,
            persist_github_connection,
        )

        result = await GitHubOAuthHandler().handle_oauth_callback(code, state)
        user_id = result.get("user_id")
        access_token = result["tokens"].access_token

        async with AsyncSessionFactory.session_scope() as session:
            await persist_github_connection(session, user_id, access_token)
            await session.commit()

        login = quote(result.get("login", "github"))
        logger.info("github_settings_oauth_success", user_id=user_id, login=result.get("login"))
        return RedirectResponse(
            url=f"/settings/integrations?github_success=true&github_login={login}",
            status_code=302,
        )
    except ValueError as e:
        logger.warning("github_settings_oauth_validation_error", error=str(e))
        return RedirectResponse(
            url="/settings/integrations?github_error=callback_failed", status_code=302
        )
    except Exception as e:
        logger.error("github_settings_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(
            url="/settings/integrations?github_error=callback_failed", status_code=302
        )


@router.get("/github/oauth-status")
async def github_oauth_status(current_user: JWTClaims = Depends(get_current_user)):
    """Per-user GitHub OAuth-connector binding status (#1317 / ADR-070 C).

    Distinct from the legacy native-PAT status (`GET /github`, system-scoped) — this
    reflects the user's `connector_binding`, so the Settings page can show the OAuth
    connection as connected. No token is read or returned (D3).
    """
    from services.connectors.binding_repository import ConnectorBindingRepository
    from services.database.session_factory import AsyncSessionFactory
    from services.mcp.consumer.connector import ConnectorStatusState

    async with AsyncSessionFactory.session_scope() as session:
        binding = await ConnectorBindingRepository(session).get(current_user.sub, "github")
    connected = binding is not None and binding.status == ConnectorStatusState.BOUND.value
    return {"connected": connected, "status": (binding.status if binding else None)}


@router.post("/calendar/disconnect")
async def disconnect_calendar(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Disconnect Google Calendar integration.

    Removes stored refresh token from keychain.
    Note: Does not revoke tokens on Google's side.
    Issue #839: Use user-scoped keychain key
    #1334-P2: clearing delegated to the uniform `disconnect_connector` helper.
    """
    try:
        from services.connectors.disconnect import disconnect_connector

        await disconnect_connector(current_user.sub, "calendar")
        logger.info("calendar_disconnected", user_id=current_user.sub)

        return {
            "success": True,
            "message": "Calendar disconnected",
        }

    except Exception as e:
        logger.error("calendar_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Calendar: {str(e)}",
        )


# ============================================================================
# Calendar Sync Preferences (Issue #571)
# ============================================================================


@router.get("/calendar/calendars", response_model=CalendarListResponse)
async def get_calendar_list(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get list of available Google calendars for the user.

    Returns calendar IDs, names, and current selection status.
    Requires a connected Google Calendar account.
    Issue #571: Calendar sync preferences
    """
    import aiohttp

    from services.infrastructure.keychain_service import KeychainService
    from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

    try:
        keychain = KeychainService()
        # Issue #839: Use user-scoped key
        key_name = f"google_calendar_{current_user.sub}"
        refresh_token = keychain.get_api_key(key_name)

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Calendar not connected. Please connect Google Calendar first.",
            )

        # Get fresh access token
        handler = GoogleCalendarOAuthHandler()
        tokens = await handler.refresh_access_token(refresh_token)

        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Failed to refresh calendar token. Please reconnect Google Calendar.",
            )

        # Fetch calendar list from Google API
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://www.googleapis.com/calendar/v3/users/me/calendarList",
                headers={"Authorization": f"Bearer {tokens.access_token}"},
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "calendar_list_fetch_failed",
                        status=response.status,
                        error=error_text,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch calendars from Google: {response.status}",
                    )

                data = await response.json()

        # Load user's saved preferences
        all_prefs = _load_calendar_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})
        selected_calendars = user_prefs.get("selected_calendars", [])

        # Build calendar list with selection status
        calendars = []
        for cal in data.get("items", []):
            cal_id = cal.get("id", "")
            calendars.append(
                CalendarInfo(
                    id=cal_id,
                    name=cal.get("summary", "Unnamed Calendar"),
                    description=cal.get("description", ""),
                    primary=cal.get("primary", False),
                    selected=(
                        cal_id in selected_calendars
                        if selected_calendars
                        else cal.get("primary", False)
                    ),
                )
            )

        logger.info("calendar_list_fetched", count=len(calendars), user_id=str(current_user.sub))

        return CalendarListResponse(calendars=calendars)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_list_fetch_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch calendar list: {str(e)}",
        )


@router.get("/calendar/preferences", response_model=CalendarPreferencesResponse)
async def get_calendar_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved calendar sync preferences for the current user.

    Returns selected calendars and primary calendar designation.
    Issue #571: Calendar sync preferences
    """
    try:
        all_prefs = _load_calendar_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})

        logger.info("calendar_preferences_loaded", user_id=str(current_user.sub))

        return CalendarPreferencesResponse(
            selected_calendars=user_prefs.get("selected_calendars", []),
            primary_calendar=user_prefs.get("primary_calendar"),
        )

    except Exception as e:
        logger.error("calendar_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load calendar preferences: {str(e)}",
        )


@router.post("/calendar/preferences", response_model=CalendarPreferencesResponse)
async def save_calendar_preferences(
    preferences: CalendarPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save calendar sync preferences for the current user.

    Stores selected calendars and primary calendar designation.
    Issue #571: Calendar sync preferences
    """
    try:
        all_prefs = _load_calendar_preferences()

        # Store preferences for this user
        user_prefs = {
            "selected_calendars": preferences.selected_calendars,
            "primary_calendar": preferences.primary_calendar,
        }

        all_prefs[str(current_user.sub)] = user_prefs
        _save_calendar_preferences(all_prefs)

        logger.info(
            "calendar_preferences_saved",
            user_id=str(current_user.sub),
            selected_count=len(preferences.selected_calendars),
            primary_calendar=preferences.primary_calendar,
        )

        return CalendarPreferencesResponse(
            selected_calendars=preferences.selected_calendars,
            primary_calendar=preferences.primary_calendar,
        )

    except Exception as e:
        logger.error("calendar_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save calendar preferences: {str(e)}",
        )


# ============================================================================
# Connection Status Endpoints
# ============================================================================


@router.get("/status")
async def get_all_oauth_status(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get connection status for all OAuth-based integrations.

    Returns connection status for Slack and Calendar.
    Issue #839: Use user-scoped keychain key for calendar
    """
    from services.infrastructure.keychain_service import KeychainService

    status_result = {
        "slack": {"connected": False, "info": None},
        "calendar": {"connected": False, "info": None},
    }

    try:
        keychain = KeychainService()

        # Check Slack
        try:
            from services.integrations.slack.config_service import SlackConfigService

            config_service = SlackConfigService()
            # #1120: get_config requires user_id (refactor-miss recovery)
            slack_config = config_service.get_config(user_id=current_user.sub)
            if slack_config.bot_token:
                status_result["slack"]["connected"] = True
        except Exception:
            pass

        # Check Calendar (Issue #839: user-scoped key)
        try:
            key_name = f"google_calendar_{current_user.sub}"
            refresh_token = keychain.get_api_key(key_name)
            if refresh_token:
                status_result["calendar"]["connected"] = True
        except Exception:
            pass

    except Exception as e:
        logger.error("oauth_status_check_failed", error=str(e))

    return status_result


# ============================================================================
# Notion API Key Management (Issue #540)
# ============================================================================


@router.get("/notion")
async def get_notion_settings(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get Notion integration status.

    Returns whether Notion is configured and any workspace info.
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()
        api_key = keychain.get_api_key(
            "notion", username=current_user.sub
        )  # Issue #849: User-scoped key for multi-tenancy isolation

        if api_key:
            # Validate the key and get workspace info
            from services.security.user_api_key_service import UserAPIKeyService
            from web.api.routes.setup import validate_notion_key_and_get_workspace

            is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(
                api_key
            )

            return {
                "configured": True,
                "valid": is_valid,
                "workspace": workspace_name if is_valid else None,
                "error": error_msg if not is_valid else None,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "workspace": None,
                "error": None,
            }

    except Exception as e:
        logger.error("notion_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "workspace": None,
            "error": str(e),
        }


@router.post("/notion/save")
async def save_notion_key(
    api_key: str = Form(...),
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save or update Notion API key.

    Validates the key first, then stores in keychain.
    Note 2026-05-25: `api_key` is form-urlencoded body parameter (matches
    `templates/settings_notion.html::saveNotionKey()` Content-Type
    `application/x-www-form-urlencoded`). Without the `Form(...)` annotation
    FastAPI treats `api_key: str` as a query parameter → 422 on every save.
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    """
    from services.database.session_factory import AsyncSessionFactory
    from services.security.user_api_key_service import UserAPIKeyService
    from web.api.routes.setup import validate_notion_key_and_get_workspace

    # Validate the key first
    is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(api_key)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg or "Invalid Notion API key",
        )

    # Store in keychain using UserAPIKeyService
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            service = UserAPIKeyService()

            # Use authenticated user from JWT context
            await service.store_user_key(
                session=session,
                user_id=str(current_user.user_id),
                provider="notion",
                api_key=api_key,
                validate=False,  # Already validated above
            )

        logger.info("notion_key_saved", workspace=workspace_name)

        return {
            "success": True,
            "workspace": workspace_name,
            "message": f"Connected to {workspace_name}",
        }

    except Exception as e:
        logger.error("notion_key_save_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Notion key: {str(e)}",
        )


@router.post("/notion/disconnect")
async def disconnect_notion(current_user: JWTClaims = Depends(get_current_user)):
    """
    Disconnect Notion integration.

    Removes API key from keychain AND the user-scoped #358 store where save_notion_key
    actually writes (#1337 — clearing only keychain left the real token behind).
    Issue #540: ALPHA-SETUP-NOTION stuck state recovery
    #1334-P2: clearing delegated to the uniform `disconnect_connector` helper.
    """
    try:
        from services.connectors.disconnect import disconnect_connector

        await disconnect_connector(current_user.sub, "notion")
        logger.info("notion_disconnected")

        return {
            "success": True,
            "message": "Notion disconnected",
        }

    except Exception as e:
        logger.error("notion_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect Notion: {str(e)}",
        )


# ============================================================================
# Notion Workspace Preferences (Issue #572)
# ============================================================================


@router.get("/notion/databases", response_model=NotionDatabaseListResponse)
async def get_notion_databases(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get list of available Notion databases for the user.

    Returns database IDs, names, and current selection status.
    Requires a connected Notion account.
    Issue #572: Notion workspace preferences
    """
    import aiohttp

    from services.integrations.notion.config_service import NotionConfigService

    try:
        config_service = NotionConfigService()
        # #1120: get_config requires user_id (refactor-miss recovery)
        config = config_service.get_config(user_id=current_user.sub)
        api_key = config.api_key

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Notion not connected. Please add your API key first.",
            )

        # Fetch databases from Notion API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/search",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={"filter": {"property": "object", "value": "database"}},
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "notion_database_list_failed",
                        status=response.status,
                        error=error_text,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch databases from Notion: {response.status}",
                    )

                data = await response.json()

        # Load user's saved preferences
        all_prefs = _load_notion_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})
        selected_databases = user_prefs.get("selected_databases", [])

        # Build database list with selection status
        databases = []
        for db in data.get("results", []):
            db_id = db.get("id", "")
            # Get title from title property
            title_prop = db.get("title", [])
            name = (
                title_prop[0].get("plain_text", "Unnamed Database")
                if title_prop
                else "Unnamed Database"
            )
            # Get description if available
            description = db.get("description", [])
            desc_text = description[0].get("plain_text", "") if description else ""

            databases.append(
                NotionDatabaseInfo(
                    id=db_id,
                    name=name,
                    description=desc_text,
                    selected=db_id in selected_databases if selected_databases else False,
                )
            )

        logger.info("notion_databases_fetched", count=len(databases), user_id=str(current_user.sub))

        return NotionDatabaseListResponse(databases=databases)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("notion_database_list_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch database list: {str(e)}",
        )


@router.get("/notion/preferences", response_model=NotionPreferencesResponse)
async def get_notion_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved Notion preferences for the current user.

    Returns selected databases and default database designation.
    Issue #572: Notion workspace preferences
    """
    try:
        all_prefs = _load_notion_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})

        logger.info("notion_preferences_loaded", user_id=str(current_user.sub))

        return NotionPreferencesResponse(
            selected_databases=user_prefs.get("selected_databases", []),
            default_database=user_prefs.get("default_database"),
        )

    except Exception as e:
        logger.error("notion_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load Notion preferences: {str(e)}",
        )


@router.post("/notion/preferences", response_model=NotionPreferencesResponse)
async def save_notion_preferences(
    preferences: NotionPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save Notion preferences for the current user.

    Stores selected databases and default database designation.
    Issue #572: Notion workspace preferences
    """
    try:
        all_prefs = _load_notion_preferences()

        # Store preferences for this user
        user_prefs = {
            "selected_databases": preferences.selected_databases,
            "default_database": preferences.default_database,
        }

        all_prefs[str(current_user.sub)] = user_prefs
        _save_notion_preferences(all_prefs)

        logger.info(
            "notion_preferences_saved",
            user_id=str(current_user.sub),
            selected_count=len(preferences.selected_databases),
            default_database=preferences.default_database,
        )

        return NotionPreferencesResponse(
            selected_databases=preferences.selected_databases,
            default_database=preferences.default_database,
        )

    except Exception as e:
        logger.error("notion_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Notion preferences: {str(e)}",
        )


# ============================================================================
# GitHub Token Management (Issue #541)
# ============================================================================


@router.get("/github")
async def get_github_settings():
    """
    Get GitHub integration status.

    Returns whether GitHub is configured and validates token if present.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    """
    try:
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()
        # Issue #891: get_authentication_token requires user_id since #734.
        # This is an unauthenticated status-check endpoint, so use "system"
        # to check env var tokens without user-scoped keychain lookup.
        token = config_service.get_authentication_token(user_id="system")

        if token:
            # Validate via GitHub's GET /user API (#1192 slice c — see save endpoint:
            # router.test_connection() is an unimplemented migration orphan).
            from services.integrations.github.token_validator import verify_github_token

            test_result = await verify_github_token(token)
            is_valid = test_result.get("authenticated", False)

            return {
                "configured": True,
                "valid": is_valid,
                "username": test_result.get("username") if is_valid else None,
                "error": test_result.get("error") if not is_valid else None,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "username": None,
                "error": None,
            }

    except Exception as e:
        logger.error("github_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "username": None,
            "error": str(e),
        }


@router.post("/github/save")
async def save_github_token(
    token: str = Form(...),
    current_user: JWTClaims = Depends(get_current_user),
):
    # Note 2026-05-25: same Form(...) shape as save_notion_key — see comment there.
    """
    Save or update GitHub personal access token.

    Validates the token first, then stores in keychain and environment.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    """
    from services.infrastructure.keychain_service import KeychainService
    from services.integrations.github.config_service import GitHubConfigService
    from services.integrations.github.token_validator import verify_github_token

    # Validate the submitted PAT directly via GitHub's GET /user API.
    # #1192 slice (c): the old `router.test_connection()` path was a migration
    # orphan (#198) — neither the MCP adapter nor the spatial fallback implements
    # test_connection, so it raised AttributeError and 500'd *every* PAT, valid or
    # not (the #541 "stuck state"). verify_github_token checks the exact token
    # submitted, no env juggling, no router/adapter dependency.
    test_result = await verify_github_token(token)
    if not test_result.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=test_result.get("error", "Invalid GitHub token"),
        )

    try:
        # Valid → persist (user-scoped keychain, #849) + make it live for this
        # process immediately (env) + clear the config cache so the next lookup
        # picks it up.
        keychain = KeychainService()
        keychain.store_api_key("github_token", token, username=current_user.sub)
        os.environ["GITHUB_TOKEN"] = token
        GitHubConfigService().clear_cache()

        username = test_result.get("username") or "GitHub User"
        logger.info("github_token_saved", username=username)
        return {
            "success": True,
            "username": username,
            "message": f"Connected as {username}",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("github_token_save_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save GitHub token: {str(e)}",
        )


@router.post("/github/disconnect")
async def disconnect_github(current_user: JWTClaims = Depends(get_current_user)):
    """
    Disconnect GitHub integration.

    Removes token from keychain and environment.
    Issue #541: ALPHA-SETUP-GITHUB stuck state recovery
    #1334-P2: clearing (keychain PAT + env + config-cache + OAuth binding + #358 grant,
    #1330) is delegated to the uniform `disconnect_connector` helper.
    """
    from services.connectors.disconnect import disconnect_connector

    try:
        await disconnect_connector(current_user.sub, "github")
        logger.info("github_disconnected")

        return {
            "success": True,
            "message": "GitHub disconnected",
        }

    except Exception as e:
        logger.error("github_disconnect_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to disconnect GitHub: {str(e)}",
        )


# ============================================================================
# GitHub Repository Preferences (Issue #573)
# ============================================================================


@router.get("/github/repositories", response_model=GitHubRepositoryListResponse)
async def get_github_repositories(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get list of accessible GitHub repositories for the user.

    Returns repository IDs, names, and current selection status.

    #1327 gap 3 cutover: prefer the per-user OAuth connector (binding + grant →
    ``search_repositories`` user:@me), mirroring the #1322 chat-read cutover. Fall back to the
    native shared PAT ONLY when the user is not OAuth-connected (``CONNECT_REQUIRED``) — the
    layer-then-migrate transition (D6 retires the PAT path). If they ARE connected but the
    connector is degraded (server unreachable / re-auth), surface an honest error rather than
    masking the real connection state with a silent PAT fallback or a silent empty (#1231).

    Issue #573: GitHub repository preferences
    """
    try:
        # --- Connector-first (#1327 gap 3): the user's own repos over the OAuth connector. ---
        connector_result = await GitHubMCPSpatialAdapter().search_user_repositories(
            current_user.sub, limit=100
        )
        if connector_result.repositories is not None:
            repo_dicts = connector_result.repositories  # normalized {id,name,full_name,description}
            source = "connector"
        elif (
            connector_result.degradation
            and connector_result.degradation.reason is DegradationReason.CONNECT_REQUIRED
        ):
            # Not OAuth-connected → transitional native-PAT fallback (#1042 path).
            repo_dicts = await _list_repos_native_pat(current_user.sub)
            source = "native_pat"
        else:
            # Connected but degraded (unreachable / stale) → honest error, never a silent PAT
            # fallback or silent empty (#1231).
            logger.warning(
                "github_repositories_degraded",
                user_id=str(current_user.sub),
                reason=connector_result.degradation.reason.value,
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=connector_result.degradation.user_message,
            )

        # Load user's saved preferences (WS-1: DB store) + merge selection status.
        user_prefs = await _load_github_prefs_db(str(current_user.sub))
        selected_repos = user_prefs.get("selected_repositories", [])

        repositories = []
        for repo in repo_dicts:
            full_name = repo.get("full_name", "")
            repositories.append(
                GitHubRepositoryInfo(
                    id=repo.get("id", 0),
                    name=repo.get("name", ""),
                    full_name=full_name,
                    description=repo.get("description") or "",
                    selected=full_name in selected_repos if selected_repos else False,
                )
            )

        logger.info(
            "github_repositories_fetched",
            count=len(repositories),
            user_id=str(current_user.sub),
            source=source,
        )

        return GitHubRepositoryListResponse(repositories=repositories)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("github_repository_list_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch repository list: {str(e)}",
        )


async def _list_repos_native_pat(user_sub: str) -> list:
    """Transitional native-PAT repo list (the #1042 fallback when not OAuth-connected).

    Returns raw GitHub-API repo dicts (``id/name/full_name/description`` among the fields). Raises
    HTTP 401 when no PAT is configured (keychain user-scoped key #849, then env fallback), and HTTP
    502 when the GitHub API call fails — the same surfaces the handler used pre-cutover. Retired by
    ADR-070 D6 once the OAuth connector is the sole path."""
    import aiohttp

    from services.infrastructure.keychain_service import KeychainService

    keychain = KeychainService()
    token = keychain.get_api_key("github_token", username=user_sub)  # #849 user-scoped
    if not token:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="GitHub not connected. Please add your token first.",
        )

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            params={"per_page": 100, "sort": "updated"},
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(
                    "github_repository_list_failed",
                    status=response.status,
                    error=error_text,
                )
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Failed to fetch repositories from GitHub: {response.status}",
                )
            return await response.json()


@router.get("/github/preferences", response_model=GitHubPreferencesResponse)
async def get_github_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved GitHub preferences for the current user.

    Returns selected repositories and default repository designation.
    Issue #573: GitHub repository preferences
    """
    try:
        user_prefs = await _load_github_prefs_db(str(current_user.sub))

        logger.info("github_preferences_loaded", user_id=str(current_user.sub))

        return GitHubPreferencesResponse(
            selected_repositories=user_prefs.get("selected_repositories", []),
            default_repository=user_prefs.get("default_repository"),
        )

    except Exception as e:
        logger.error("github_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load GitHub preferences: {str(e)}",
        )


@router.post("/github/preferences", response_model=GitHubPreferencesResponse)
async def save_github_preferences(
    preferences: GitHubPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save GitHub preferences for the current user.

    Stores selected repositories and default repository designation.
    Issue #573: GitHub repository preferences
    """
    try:
        # Store preferences for this user (WS-1: DB store is the single home)
        user_prefs = {
            "selected_repositories": preferences.selected_repositories,
            "default_repository": preferences.default_repository,
        }
        await _save_github_prefs_db(str(current_user.sub), user_prefs)

        logger.info(
            "github_preferences_saved",
            user_id=str(current_user.sub),
            selected_count=len(preferences.selected_repositories),
            default_repository=preferences.default_repository,
        )

        return GitHubPreferencesResponse(
            selected_repositories=preferences.selected_repositories,
            default_repository=preferences.default_repository,
        )

    except Exception as e:
        logger.error("github_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save GitHub preferences: {str(e)}",
        )


# ============================================================================
# Slack OAuth Management (Issue #528)
# ============================================================================


@router.get("/slack")
async def get_slack_settings():
    """
    Get Slack integration status.

    Returns whether Slack is configured and validates connection if token present.
    Issue #528: ALPHA-SETUP-SLACK - Add Slack OAuth to setup wizard
    """
    try:
        # Check if bot token is configured
        bot_token = os.environ.get("SLACK_BOT_TOKEN")

        if bot_token:
            # Validate the token by testing connection
            from services.integrations.slack.config_service import SlackConfigService
            from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

            # #1110: This endpoint has no authenticated user (no Depends), but a
            # Slack API call requires a user_id (ADR-058 multi-tenancy). The
            # workspace-level status check uses the connector-owner user id
            # (SLACK_CONNECTOR_USER_ID, the #759 alpha pattern). Per the #1110
            # guardrail we do NOT fall back to None — if no connector user is
            # configured we report that honestly instead of recreating the bug.
            connector_user_id = os.environ.get("SLACK_CONNECTOR_USER_ID")
            if not connector_user_id:
                return {
                    "configured": True,
                    "valid": False,
                    "workspace": None,
                    "bot_id": None,
                    "error": (
                        "SLACK_CONNECTOR_USER_ID not configured; cannot validate "
                        "workspace connection (multi-tenancy requires a user id)."
                    ),
                }

            router_instance = SlackIntegrationRouter(config_service=SlackConfigService())
            test_response = await router_instance.test_auth(user_id=connector_user_id)

            # test_auth returns a SlackResponse dataclass, not a dict.
            is_valid = bool(getattr(test_response, "success", False))
            data = getattr(test_response, "data", {}) or {}
            team_name = data.get("team")
            bot_id = data.get("bot_id")
            error = None
            if not is_valid:
                err_obj = getattr(test_response, "error", None)
                error = getattr(err_obj, "message", None) if err_obj else "Slack auth failed"

            return {
                "configured": True,
                "valid": is_valid,
                "workspace": team_name if is_valid else None,
                "bot_id": bot_id if is_valid else None,
                "error": error,
            }
        else:
            return {
                "configured": False,
                "valid": False,
                "workspace": None,
                "bot_id": None,
                "error": None,
            }

    except Exception as e:
        logger.error("slack_settings_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "valid": False,
            "workspace": None,
            "bot_id": None,
            "error": str(e),
        }


@router.get("/slack/authorize")
async def get_slack_oauth_url(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get Slack OAuth authorization URL.

    Issue #528: ALPHA-SETUP-SLACK
    Issue #734: SEC-MULTITENANCY - Requires authentication, embeds user_id in state.

    Generates a secure OAuth URL to initiate Slack workspace connection.
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        config_service = SlackConfigService()
        oauth_handler = SlackOAuthHandler(config_service)

        # Issue #734: Pass user_id for multi-tenant state
        # Issue #1109: generate_authorization_url is async (Redis-backed state)
        auth_url, state = await oauth_handler.generate_authorization_url(user_id=current_user.sub)

        return {
            "success": True,
            "authorization_url": auth_url,
            "state": state,
        }

    except Exception as e:
        logger.error("slack_oauth_url_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate Slack OAuth URL: {str(e)}",
        )


# NOTE: the second `/slack/disconnect` definition (Issue #528) was removed here in
# #1334 — it was a shadowed duplicate (FastAPI used the first-registered route above).
# Its Slack-side OAuth-revoke behavior was merged into the canonical def above; this
# def also leaked the user-scoped keychain creds (it cleared only env), so it was the
# worse of the two to keep live.
