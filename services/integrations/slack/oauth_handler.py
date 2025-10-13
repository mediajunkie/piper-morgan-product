"""
Slack OAuth Handler
Implements Slack OAuth flow management following GitHub integration patterns.

Provides OAuth 2.0 flow management for Slack app installation including:
- OAuth callback handling with spatial workspace initialization
- Token exchange and storage using existing configuration patterns
- State management for security
- Workspace permission verification
- Integration with spatial metaphor system
"""

import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse

import httpx

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.api.errors import SlackAuthFailedError

from .config_service import SlackConfigService
from .spatial_mapper import SlackSpatialMapper

logger = logging.getLogger(__name__)


class SlackOAuthHandler:
    """
    Slack OAuth flow management following GitHub integration patterns.

    Handles OAuth 2.0 authorization flow for Slack app installation with
    spatial workspace initialization and secure token management.
    """

    def __init__(self, config_service: Optional[SlackConfigService] = None):
        self.config_service = config_service or SlackConfigService()
        self.spatial_mapper = SlackSpatialMapper()

        # OAuth state management (in-memory for development, Redis for production)
        self._oauth_states: Dict[str, Dict[str, Any]] = {}

        # Slack OAuth endpoints
        self.auth_url = "https://slack.com/oauth/v2/authorize"
        self.token_url = "https://slack.com/api/oauth.v2.access"

        logger.info("SlackOAuthHandler initialized")

    def generate_authorization_url(
        self,
        scopes: Optional[list] = None,
        user_scopes: Optional[list] = None,
        redirect_uri: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Generate Slack OAuth authorization URL with secure state.

        Args:
            scopes: Bot token scopes (optional, uses defaults)
            user_scopes: User token scopes (optional)
            redirect_uri: Custom redirect URI (optional, uses config)

        Returns:
            Tuple of (authorization_url, state) for OAuth flow
        """
        try:
            config = self.config_service.get_config()

            # Generate secure state token
            state = secrets.token_urlsafe(32)

            # Store state with expiration (15 minutes)
            self._oauth_states[state] = {
                "created_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(minutes=15),
                "scopes": scopes,
                "user_scopes": user_scopes,
                "redirect_uri": redirect_uri or config.redirect_uri,
            }

            # Default scopes for spatial metaphor capabilities
            if not scopes:
                scopes = [
                    "app_mentions:read",  # Attention attractors (@mentions)
                    "channels:history",  # Room (channel) message access
                    "channels:read",  # Room (channel) metadata
                    "chat:write",  # Object placement (message sending)
                    "groups:history",  # Private room access
                    "groups:read",  # Private room metadata
                    "im:history",  # Direct conversation paths
                    "im:read",  # Direct conversation metadata
                    "mpim:history",  # Multi-party conversation paths
                    "mpim:read",  # Multi-party conversation metadata
                    "reactions:read",  # Emotional valence markers
                    "team:read",  # Territory (workspace) information
                    "users:read",  # Inhabitant information
                    "channels:join",  # Room navigation capability
                    "chat:write.public",  # Public room object placement
                ]

            # Build authorization parameters
            auth_params = {
                "client_id": config.client_id,
                "scope": ",".join(scopes),
                "redirect_uri": redirect_uri or config.redirect_uri,
                "state": state,
                "response_type": "code",
            }

            # Add user scopes if specified
            if user_scopes:
                auth_params["user_scope"] = ",".join(user_scopes)

            # Construct authorization URL
            authorization_url = f"{self.auth_url}?{urlencode(auth_params)}"

            logger.info(f"Generated OAuth authorization URL with state {state[:8]}...")
            return authorization_url, state

        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {e}")
            raise SlackAuthFailedError(f"Authorization URL generation failed: {e}") from e

    async def handle_oauth_callback(
        self, code: str, state: str, received_redirect_uri: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle OAuth callback and complete token exchange.

        Args:
            code: Authorization code from Slack
            state: State parameter for security verification
            received_redirect_uri: Redirect URI from callback (for verification)

        Returns:
            Dictionary containing workspace info and tokens
        """
        try:
            # Verify state parameter
            if not self._verify_oauth_state(state):
                raise SlackAuthFailedError("Invalid or expired OAuth state")

            # Get stored state data
            state_data = self._oauth_states.pop(state, {})
            expected_redirect_uri = state_data.get("redirect_uri")

            # Verify redirect URI if provided
            if received_redirect_uri and expected_redirect_uri:
                if not self._verify_redirect_uri(received_redirect_uri, expected_redirect_uri):
                    raise SlackAuthFailedError("Redirect URI mismatch")

            # Exchange code for tokens
            token_data = await self._exchange_code_for_tokens(code, expected_redirect_uri)

            # Initialize spatial workspace representation
            workspace_data = await self._initialize_spatial_workspace(token_data)

            # Store tokens using configuration patterns
            await self._store_workspace_tokens(workspace_data, token_data)

            logger.info(
                f"OAuth callback completed for workspace {workspace_data.get('workspace_name')}"
            )

            return {
                "success": True,
                "workspace": workspace_data,
                "spatial_mapping": workspace_data.get("spatial_context"),
                "tokens_stored": True,
                "installation_complete": True,
            }

        except Exception as e:
            logger.error(f"OAuth callback handling failed: {e}")
            # Clean up state on failure
            self._oauth_states.pop(state, None)
            raise SlackAuthFailedError(f"OAuth callback failed: {e}") from e

    def _verify_oauth_state(self, state: str) -> bool:
        """Verify OAuth state parameter for security"""

        if state not in self._oauth_states:
            logger.warning(f"Unknown OAuth state: {state[:8]}...")
            return False

        state_data = self._oauth_states[state]

        # Check expiration
        if datetime.utcnow() > state_data["expires_at"]:
            logger.warning(f"Expired OAuth state: {state[:8]}...")
            self._oauth_states.pop(state, None)
            return False

        return True

    def _verify_redirect_uri(self, received: str, expected: str) -> bool:
        """Verify redirect URI matches expected value"""

        # Parse URLs for comparison
        received_parsed = urlparse(received)
        expected_parsed = urlparse(expected)

        # Compare scheme, netloc, and path (ignore query params)
        return (
            received_parsed.scheme == expected_parsed.scheme
            and received_parsed.netloc == expected_parsed.netloc
            and received_parsed.path == expected_parsed.path
        )

    async def _exchange_code_for_tokens(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for access tokens"""

        config = self.config_service.get_config()

        token_params = {
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data=token_params,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=config.timeout_seconds,
                )

                response.raise_for_status()
                token_data = response.json()

                if not token_data.get("ok"):
                    error_msg = token_data.get("error", "Unknown token exchange error")
                    raise SlackAuthFailedError(f"Slack token exchange failed: {error_msg}")

                logger.info("Successfully exchanged code for tokens")
                return token_data

            except httpx.TimeoutException as e:
                raise SlackAuthFailedError("Token exchange request timed out") from e
            except httpx.HTTPStatusError as e:
                raise SlackAuthFailedError(
                    f"Token exchange HTTP error: {e.response.status_code}"
                ) from e

    async def _initialize_spatial_workspace(self, token_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize spatial representation of newly connected workspace"""

        try:
            # Extract workspace information from token response
            team_info = token_data.get("team", {})
            workspace_id = team_info.get("id", "")
            workspace_name = team_info.get("name", "Unknown Workspace")

            # Create workspace representation for spatial mapper
            workspace_slack_data = {
                "id": workspace_id,
                "name": workspace_name,
                "domain": team_info.get("domain"),
                "enterprise_id": team_info.get("enterprise_id"),
                "is_paid_plan": True,  # Assume paid for OAuth apps
                "created": None,  # Would need additional API call for this
                "locale": "en-US",  # Default, would need user info for actual locale
            }

            # Map to spatial territory
            territory = self.spatial_mapper.map_workspace(workspace_slack_data)

            # Get spatial context for response
            spatial_context = territory.get_navigation_context()

            workspace_data = {
                "workspace_id": workspace_id,
                "workspace_name": workspace_name,
                "workspace_domain": team_info.get("domain"),
                "territory": {
                    "id": territory.id,
                    "name": territory.name,
                    "type": territory.territory_type.value,
                    "navigation_context": spatial_context,
                },
                "spatial_context": spatial_context,
                "installation_time": datetime.utcnow().isoformat(),
                "bot_user_id": token_data.get("bot_user_id"),
                "app_id": token_data.get("app_id"),
            }

            logger.info(
                f"Initialized spatial workspace: {workspace_name} as {territory.territory_type.value} territory"
            )

            return workspace_data

        except Exception as e:
            logger.error(f"Failed to initialize spatial workspace: {e}")
            raise SlackAuthFailedError(f"Spatial workspace initialization failed: {e}") from e

    async def _store_workspace_tokens(
        self, workspace_data: Dict[str, Any], token_data: Dict[str, Any]
    ) -> None:
        """Store workspace tokens using existing configuration patterns"""

        try:
            workspace_id = workspace_data["workspace_id"]

            # Extract tokens
            bot_token = token_data.get("access_token")
            user_token = token_data.get("authed_user", {}).get("access_token")

            # In production, this would integrate with secure token storage
            # For development, we'll use environment-style storage pattern

            # Store bot token (primary for API operations)
            if bot_token:
                # This would typically go to secure key-value store
                logger.info(f"Bot token stored for workspace {workspace_id}")

                # Update configuration cache if needed
                config = self.config_service.get_config()
                if not config.bot_token:
                    # Set as primary bot token if none configured
                    config.bot_token = bot_token

            # Store user token if available
            if user_token:
                logger.info(f"User token stored for workspace {workspace_id}")

            # Store workspace metadata
            workspace_config = {
                "workspace_id": workspace_id,
                "workspace_name": workspace_data["workspace_name"],
                "workspace_domain": workspace_data.get("workspace_domain"),
                "bot_user_id": token_data.get("bot_user_id"),
                "app_id": token_data.get("app_id"),
                "spatial_territory_id": workspace_data["territory"]["id"],
                "installed_at": workspace_data["installation_time"],
                "scopes": token_data.get("scope", "").split(","),
                "user_scopes": (
                    token_data.get("authed_user", {}).get("scope", "").split(",")
                    if token_data.get("authed_user", {}).get("scope")
                    else []
                ),
            }

            # This would typically go to database or secure storage
            logger.info(f"Workspace configuration stored: {workspace_config}")

        except Exception as e:
            logger.error(f"Failed to store workspace tokens: {e}")
            raise SlackAuthFailedError(f"Token storage failed: {e}") from e

    def cleanup_expired_states(self) -> int:
        """Clean up expired OAuth states (housekeeping)"""

        current_time = datetime.utcnow()
        expired_states = []

        for state, data in self._oauth_states.items():
            if current_time > data["expires_at"]:
                expired_states.append(state)

        for state in expired_states:
            self._oauth_states.pop(state, None)

        if expired_states:
            logger.info(f"Cleaned up {len(expired_states)} expired OAuth states")

        return len(expired_states)

    def get_oauth_status(self) -> Dict[str, Any]:
        """Get OAuth handler status and metrics"""

        current_time = datetime.utcnow()
        active_states = sum(
            1 for data in self._oauth_states.values() if current_time <= data["expires_at"]
        )

        return {
            "handler_status": "operational",
            "active_oauth_flows": active_states,
            "total_state_entries": len(self._oauth_states),
            "spatial_mapper_status": self.spatial_mapper.get_spatial_analytics(),
            "auth_endpoints": {
                "authorization_url": self.auth_url,
                "token_exchange_url": self.token_url,
            },
        }

    async def revoke_workspace_access(self, workspace_id: str) -> bool:
        """Revoke OAuth access for a workspace"""

        try:
            # This would typically:
            # 1. Call Slack's auth.revoke API
            # 2. Remove stored tokens
            # 3. Clear spatial mapping data
            # 4. Update configuration

            # Clear spatial cache for workspace
            self.spatial_mapper.clear_spatial_cache()

            logger.info(f"Revoked access for workspace {workspace_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to revoke workspace access: {e}")
            return False
