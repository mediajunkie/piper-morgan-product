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

import json
import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from urllib.parse import urlencode, urlparse

import httpx

from services.api.errors import SlackAuthFailedError
from services.cache.redis_factory import RedisFactory
from services.intent_service.canonical_handlers import CanonicalHandlers

from .config_service import SlackConfigService
from .spatial_mapper import SlackSpatialMapper

logger = logging.getLogger(__name__)

# Redis key prefix for OAuth nonce state (#1109 RECONNECT WS-7).
# Each in-flight OAuth nonce is stored at f"{OAUTH_STATE_KEY_PREFIX}{nonce}"
# with a Redis TTL set from the state's expiry — multi-process safe, and the
# TTL replaces the old manual expired-state cleanup sweep.
OAUTH_STATE_KEY_PREFIX = "slack:oauth:state:"


class SlackOAuthHandler:
    """
    Slack OAuth flow management following GitHub integration patterns.

    Handles OAuth 2.0 authorization flow for Slack app installation with
    spatial workspace initialization and secure token management.
    """

    # OAuth nonce store lives in Redis (#1109 RECONNECT WS-7) — multi-process
    # safe. Each nonce is a key f"{OAUTH_STATE_KEY_PREFIX}{nonce}" holding the
    # JSON state data, with a Redis TTL set from the state's expiry so entries
    # auto-expire (no manual cleanup needed). Replaces the prior class-level
    # dict, which only worked single-process (state stored during /connect by
    # one worker was invisible to a /callback handled by another).
    # History: in-process dict surfaced 2026-05-21 during PM's OAuth re-auth
    # (an instance-level dict had lost the nonce across the /connect→/callback
    # request boundary); the class-level dict fixed single-process but not the
    # multi-process case this issue addresses.

    @staticmethod
    def _state_key(nonce: str) -> str:
        """Redis key for a given OAuth nonce."""
        return f"{OAUTH_STATE_KEY_PREFIX}{nonce}"

    def __init__(self, config_service: Optional[SlackConfigService] = None):
        self.config_service = config_service or SlackConfigService()
        self.spatial_mapper = SlackSpatialMapper()

        # Slack OAuth endpoints
        self.auth_url = "https://slack.com/oauth/v2/authorize"
        self.token_url = "https://slack.com/api/oauth.v2.access"

        logger.info("SlackOAuthHandler initialized")

    async def generate_authorization_url(
        self,
        user_id: str,
        scopes: Optional[list] = None,
        user_scopes: Optional[list] = None,
        redirect_uri: Optional[str] = None,
        return_url: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Generate Slack OAuth authorization URL with user-scoped state.

        Issue #734: SEC-MULTITENANCY - Embed user_id in OAuth state.

        Args:
            user_id: The ID of the user initiating OAuth flow (required)
            scopes: Bot token scopes (optional, uses defaults)
            user_scopes: User token scopes (optional)
            redirect_uri: Custom redirect URI (optional, uses config)
            return_url: Optional URL to redirect to after OAuth completes

        Returns:
            Tuple of (authorization_url, state) for OAuth flow

        Raises:
            ValueError: If user_id is not provided
        """
        if not user_id:
            raise ValueError("user_id is required for OAuth state")

        try:
            import base64
            import json

            # Issue #734: Pass user_id for multi-tenancy isolation
            config = self.config_service.get_config(user_id=user_id)

            # Generate secure nonce
            nonce = secrets.token_urlsafe(16)

            # Create state with user_id, nonce, and optional return_url
            state_data = {
                "user_id": user_id,
                "nonce": nonce,
            }
            if return_url:
                state_data["return_url"] = return_url

            # Encode state as base64 JSON
            state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")

            # Store nonce with metadata for verification, in Redis with a TTL set
            # from the expiry window (#1109). datetimes are serialized as ISO
            # strings; the TTL (15 min) auto-expires the entry — no manual
            # cleanup. created_at/expires_at are retained for defensive
            # validation and parity with the prior in-process shape.
            created_at = datetime.utcnow()
            expires_at = created_at + timedelta(minutes=15)
            ttl_seconds = max(1, int((expires_at - created_at).total_seconds()))
            nonce_payload = {
                "created_at": created_at.isoformat(),
                "expires_at": expires_at.isoformat(),
                "scopes": scopes,
                "user_scopes": user_scopes,
                "redirect_uri": redirect_uri or config.redirect_uri,
                "user_id": user_id,  # Also store for verification
            }
            async with RedisFactory.redis_scope() as redis:
                await redis.setex(
                    self._state_key(nonce),
                    ttl_seconds,
                    json.dumps(nonce_payload),
                )

            # Default scopes for spatial metaphor capabilities (bot token)
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

            # Default user-token scopes (Issue #1085 slice 3 prep)
            # `search:read` is required for Slack's search.messages API,
            # which only works with user tokens (not bot tokens). Used by
            # the recent-activity aggregator's mentions-of-user lookup
            # path. Removable later via re-auth if scope-narrowing
            # becomes desirable.
            if not user_scopes:
                user_scopes = [
                    "search:read",
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

            logger.info(
                f"Generated OAuth authorization URL for user {user_id}, state {state[:8]}..."
            )
            return authorization_url, state

        except Exception as e:
            logger.error(f"Failed to generate authorization URL: {e}")
            raise SlackAuthFailedError(f"Authorization URL generation failed: {e}") from e

    async def handle_oauth_callback(
        self, code: str, state: str, received_redirect_uri: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle OAuth callback and complete token exchange.

        Issue #734: SEC-MULTITENANCY - Extract and return user_id from state.

        Args:
            code: Authorization code from Slack
            state: State parameter for security verification (includes user_id)
            received_redirect_uri: Redirect URI from callback (for verification)

        Returns:
            Dictionary containing workspace info, tokens, and user_id
        """
        import base64
        import json

        try:
            # Verify state parameter and extract user_id
            is_valid, user_id = await self._verify_oauth_state(state)
            if not is_valid:
                raise SlackAuthFailedError("Invalid or expired OAuth state")

            # Extract nonce from state to get stored data
            try:
                padded = state + "=" * (4 - len(state) % 4)
                decoded = base64.urlsafe_b64decode(padded)
                state_data = json.loads(decoded)
                nonce = state_data.get("nonce")
            except (ValueError, json.JSONDecodeError):
                raise SlackAuthFailedError("Could not decode state parameter")

            # Atomically fetch + remove stored state (single-use) from Redis
            # (#1109). GETDEL guarantees the nonce can't be replayed by a
            # concurrent callback even across processes.
            nonce_data = await self._pop_oauth_state(nonce)
            expected_redirect_uri = nonce_data.get("redirect_uri")

            # Verify redirect URI if provided
            if received_redirect_uri and expected_redirect_uri:
                if not self._verify_redirect_uri(received_redirect_uri, expected_redirect_uri):
                    raise SlackAuthFailedError("Redirect URI mismatch")

            # Exchange code for tokens
            # Issue #734: Pass user_id for multi-tenancy config access
            token_data = await self._exchange_code_for_tokens(
                code, expected_redirect_uri, user_id=user_id
            )

            # Initialize spatial workspace representation
            workspace_data = await self._initialize_spatial_workspace(token_data)

            # Store tokens using configuration patterns
            # Issue #734: Pass user_id for per-user storage
            await self._store_workspace_tokens(workspace_data, token_data, user_id=user_id)

            logger.info(
                f"OAuth callback completed for workspace {workspace_data.get('workspace_name')}, user_id={user_id}"
            )

            return {
                "success": True,
                "workspace": workspace_data,
                "spatial_mapping": workspace_data.get("spatial_context"),
                "tokens_stored": True,
                "installation_complete": True,
                "user_id": user_id,  # Issue #734: Return user_id for caller
            }

        except Exception as e:
            logger.error(f"OAuth callback handling failed: {e}")
            # Clean up state on failure - try to extract nonce (#1109: remove
            # from Redis so a failed attempt can't leave a replayable nonce).
            try:
                padded = state + "=" * (4 - len(state) % 4)
                decoded = base64.urlsafe_b64decode(padded)
                state_data = json.loads(decoded)
                nonce = state_data.get("nonce")
                if nonce:
                    await self._pop_oauth_state(nonce)
            except Exception:
                pass
            raise SlackAuthFailedError(f"OAuth callback failed: {e}") from e

    @staticmethod
    def _deserialize_nonce_data(raw: Optional[Any]) -> Optional[Dict[str, Any]]:
        """Decode a Redis-stored nonce payload (bytes or str JSON) to a dict.

        Returns None if the value is absent or not decodable.
        """
        if raw is None:
            return None
        if isinstance(raw, (bytes, bytearray)):
            raw = raw.decode()
        try:
            return json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            logger.warning("Corrupt OAuth nonce payload in Redis")
            return None

    async def _read_oauth_state(self, nonce: str) -> Optional[Dict[str, Any]]:
        """Read (non-destructive) the stored state for a nonce from Redis."""
        async with RedisFactory.redis_scope() as redis:
            raw = await redis.get(self._state_key(nonce))
        return self._deserialize_nonce_data(raw)

    async def _pop_oauth_state(self, nonce: str) -> Dict[str, Any]:
        """Atomically fetch + delete the stored state for a nonce (single-use).

        Uses Redis GETDEL so the read and delete are atomic — a concurrent
        callback (even in another process) cannot replay the same nonce.
        Returns {} if the nonce is absent.
        """
        async with RedisFactory.redis_scope() as redis:
            raw = await redis.getdel(self._state_key(nonce))
        return self._deserialize_nonce_data(raw) or {}

    async def _verify_oauth_state(self, state: str) -> Tuple[bool, Optional[str]]:
        """
        Verify OAuth state parameter and extract user_id.

        Issue #734: SEC-MULTITENANCY - Extract user_id from state.
        Issue #1109: Nonce store is Redis (multi-process safe). This read is
        non-destructive — the single-use pop happens in handle_oauth_callback
        via GETDEL.

        Args:
            state: The base64-encoded state parameter from callback

        Returns:
            Tuple of (is_valid, user_id). user_id is None if invalid.
        """
        import base64
        import json

        # Decode state to extract nonce and user_id
        try:
            padded = state + "=" * (4 - len(state) % 4)
            decoded = base64.urlsafe_b64decode(padded)
            state_data = json.loads(decoded)
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to decode OAuth state: {e}")
            return False, None

        nonce = state_data.get("nonce")
        user_id = state_data.get("user_id")

        if not nonce or not user_id:
            logger.warning(
                f"OAuth state missing required fields (nonce={bool(nonce)}, user_id={bool(user_id)})"
            )
            return False, None

        nonce_data = await self._read_oauth_state(nonce)
        if not nonce_data:
            # Missing key: never stored, already popped (single-use), or
            # TTL-expired in Redis — all rejected.
            logger.warning(f"Unknown OAuth nonce: {nonce[:8]}...")
            return False, None

        # Defensive expiration check (Redis TTL normally removes expired keys,
        # but the stored expires_at is the authoritative window). expires_at is
        # an ISO string (#1109).
        try:
            expires_at = datetime.fromisoformat(nonce_data["expires_at"])
        except (KeyError, ValueError):
            logger.warning(f"OAuth nonce missing/invalid expires_at: {nonce[:8]}...")
            return False, None

        if datetime.utcnow() > expires_at:
            logger.warning(f"Expired OAuth state for nonce: {nonce[:8]}...")
            await self._pop_oauth_state(nonce)
            return False, None

        # Verify user_id matches stored value (prevent tampering)
        stored_user_id = nonce_data.get("user_id")
        if stored_user_id and stored_user_id != user_id:
            logger.warning(
                f"OAuth state user_id mismatch: expected {stored_user_id}, got {user_id}"
            )
            return False, None

        return True, user_id

    async def verify_oauth_state(self, state: str) -> Tuple[bool, Optional[str]]:
        """
        Public method to verify OAuth state and extract user_id.

        Issue #734: SEC-MULTITENANCY - State verification for multi-tenant.
        Issue #1109: Now async (Redis-backed nonce store).

        Args:
            state: The base64-encoded state parameter from callback

        Returns:
            Tuple of (is_valid, user_id). user_id is None if invalid.
        """
        return await self._verify_oauth_state(state)

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

    async def _exchange_code_for_tokens(
        self, code: str, redirect_uri: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access tokens.

        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Redirect URI used in auth request
            user_id: User ID for config access (Issue #734)

        Returns:
            Token response data from Slack

        Issue #734: Added user_id parameter for multi-tenancy config access.
        Note: client_id and client_secret are app credentials (not user-scoped),
        but we need user_id for config access pattern consistency.
        """
        # Issue #734: Pass user_id for multi-tenancy config access
        # Note: client_id/secret are app credentials, but we use user config for timeout etc.
        config = self.config_service.get_config(user_id=user_id) if user_id else None

        # Use IntegrationConfigService for app credentials as fallback
        if not config or not config.client_id:
            from services.integrations.integration_config_service import IntegrationConfigService

            integration_config = IntegrationConfigService()
            client_id = integration_config.get_slack_client_id()
            client_secret = integration_config.get_slack_client_secret()
            timeout_seconds = 30  # Default timeout
        else:
            client_id = config.client_id
            client_secret = config.client_secret
            timeout_seconds = config.timeout_seconds

        token_params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.token_url,
                    data=token_params,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    timeout=timeout_seconds,
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

    def initialize_spatial_territory(self, oauth_response: dict):
        """
        Initialize spatial territory from OAuth response (TDD-compatible).

        Creates a territory representation that includes OAuth credentials.
        This is a simplified sync wrapper for TDD test compatibility.

        Args:
            oauth_response: OAuth response dict with team and token info

        Returns:
            Object with territory_id, name, type, and access_token attributes

        Raises:
            ValueError: If OAuth response indicates failure
        """
        from dataclasses import dataclass

        from services.integrations.slack.spatial_types import TerritoryType

        # Check for OAuth errors
        if "error" in oauth_response:
            raise ValueError(
                f"OAuth failed: {oauth_response.get('error_description', oauth_response['error'])}"
            )

        # Extract OAuth data
        access_token = oauth_response.get("access_token", "")
        team_info = oauth_response.get("team", {})
        territory_id = team_info.get("id", "")
        name = team_info.get("name", "Unknown Workspace")

        # Create territory via spatial mapper
        workspace_data = {
            "id": territory_id,
            "name": name,
            "domain": team_info.get("domain"),
            "enterprise_id": team_info.get("enterprise_id"),
        }

        territory = self.spatial_mapper.map_workspace(workspace_data)

        # Create TDD-compatible response object with access_token
        # For OAuth-initialized workspaces, default to WORKSPACE type
        @dataclass
        class SpatialTerritory:
            """OAuth + Spatial Territory wrapper"""

            territory_id: str
            name: str
            type: TerritoryType
            access_token: str

        return SpatialTerritory(
            territory_id=territory.id,
            name=territory.name,
            type=TerritoryType.WORKSPACE,  # OAuth workspaces default to WORKSPACE type
            access_token=access_token,
        )

    async def _store_workspace_tokens(
        self,
        workspace_data: Dict[str, Any],
        token_data: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> None:
        """Store workspace tokens using secure keychain storage.

        Issue #575: Now actually stores bot_token in keychain (like Calendar).
        Issue #734: SEC-MULTITENANCY - Accepts user_id for per-user storage.

        Args:
            workspace_data: Workspace metadata
            token_data: OAuth token response
            user_id: User ID for per-user token storage (Issue #734)
        """
        from services.infrastructure.keychain_service import KeychainService

        try:
            workspace_id = workspace_data["workspace_id"]

            # Extract tokens
            bot_token = token_data.get("access_token")
            user_token = token_data.get("authed_user", {}).get("access_token")

            # Issue #849: Use username param (not f-string) for consistent key naming with config service retrieval
            # Store bot token securely in keychain (Issue #575)
            if bot_token:
                keychain = KeychainService()
                keychain.store_api_key("slack_bot", bot_token, username=user_id)
                logger.info(
                    f"Bot token stored in keychain for workspace {workspace_id}, user_id={user_id}"
                )

                # Update configuration cache
                # Issue #734: Pass user_id for multi-tenancy isolation
                if user_id:
                    config = self.config_service.get_config(user_id=user_id)
                    if not config.bot_token:
                        config.bot_token = bot_token

            # Store user token if available (also in keychain)
            if user_token:
                keychain = KeychainService()
                keychain.store_api_key(
                    "slack_user", user_token, username=user_id
                )  # Issue #849: username param for consistent key naming
                logger.info(
                    f"User token stored in keychain for workspace {workspace_id}, user_id={user_id}"
                )

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
                "user_id": user_id,  # Issue #734: Track owning user
            }

            # This would typically go to database or secure storage
            logger.info(f"Workspace configuration stored: {workspace_config}")

        except Exception as e:
            logger.error(f"Failed to store workspace tokens: {e}")
            raise SlackAuthFailedError(f"Token storage failed: {e}") from e

    # Issue #1109: cleanup_expired_states() was removed. Redis TTL auto-expires
    # OAuth nonce keys, so no manual housekeeping sweep is needed.

    async def get_oauth_status(self) -> Dict[str, Any]:
        """Get OAuth handler status and metrics.

        Issue #1109: in-flight OAuth flows are counted via a Redis SCAN over the
        nonce key prefix. Every key present is live (TTL removes expired ones),
        so active == total. Degrades gracefully if Redis is unreachable.
        """
        active_states = 0
        try:
            async with RedisFactory.redis_scope() as redis:
                async for _ in redis.scan_iter(match=f"{OAUTH_STATE_KEY_PREFIX}*"):
                    active_states += 1
        except Exception as e:  # pragma: no cover - health endpoint resilience
            logger.warning(f"Could not count OAuth states from Redis: {e}")

        return {
            "handler_status": "operational",
            "active_oauth_flows": active_states,
            "total_state_entries": active_states,
            "spatial_mapper_status": self.spatial_mapper.get_spatial_analytics(),
            "auth_endpoints": {
                "authorization_url": self.auth_url,
                "token_exchange_url": self.token_url,
            },
        }

    async def revoke_workspace_access(self, user_id: str) -> bool:
        """Revoke this user's Slack OAuth tokens on Slack's side (#542).

        Renamed from a ``workspace_id`` parameter (2026-07-06): the prior version
        never made a real API call and took a workspace-level env var that had no
        relationship to which user was disconnecting. Slack's per-token model means
        the bot token and user token (if granted, #1338) are revoked independently;
        each call is best-effort so a missing/already-invalid token never blocks the
        disconnect from completing.
        """
        config = self.config_service.get_config(user_id=user_id)
        revoke_url = f"{config.api_base_url}/auth.revoke"
        any_revoked = False

        for token in (config.bot_token, config.user_token):
            if not token:
                continue
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        revoke_url,
                        headers={"Authorization": f"Bearer {token}"},
                        timeout=config.timeout_seconds,
                    )
                    data = response.json()
                    if data.get("ok"):
                        any_revoked = True
                    else:
                        logger.warning(
                            f"Slack auth.revoke returned not-ok for user {user_id}: "
                            f"{data.get('error', 'unknown error')}"
                        )
            except Exception as e:
                logger.warning(f"Slack auth.revoke request failed for user {user_id}: {e}")

        try:
            self.spatial_mapper.clear_spatial_cache()
        except Exception as e:
            logger.warning(f"Failed to clear spatial cache during revoke: {e}")

        logger.info(f"Revoke attempted for user {user_id} (any_revoked={any_revoked})")
        return any_revoked

    def get_spatial_capabilities(self, oauth_response: Dict[str, Any]) -> list:
        """
        Map OAuth scopes to spatial capabilities.

        Extracts granted scopes from OAuth response and returns them as a list
        of individual capability strings. These scopes determine what spatial
        operations the bot can perform in the workspace.

        Args:
            oauth_response: OAuth response dict containing authed_user.scope

        Returns:
            List of individual scope strings (e.g., ["chat:write", "channels:read"])

        Raises:
            KeyError: If authed_user.scope is missing from OAuth response

        Example:
            >>> oauth_response = {
            ...     "authed_user": {"scope": "chat:write,channels:read"}
            ... }
            >>> handler.get_spatial_capabilities(oauth_response)
            ['chat:write', 'channels:read']
        """
        try:
            # Extract scope string from authed_user
            authed_user = oauth_response.get("authed_user", {})
            scope_string = authed_user.get("scope", "")

            # Parse comma-separated scopes into list
            if not scope_string:
                logger.warning("No scopes found in OAuth response")
                return []

            capabilities = [scope.strip() for scope in scope_string.split(",") if scope.strip()]

            logger.info(f"Extracted {len(capabilities)} spatial capabilities from OAuth response")
            return capabilities

        except Exception as e:
            logger.error(f"Failed to extract spatial capabilities: {e}")
            raise

    def get_user_spatial_context(self, oauth_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get user's spatial context from OAuth data.

        Extracts user information and spatial permissions from OAuth response,
        providing a complete context of the user's spatial position and capabilities
        within the workspace.

        Args:
            oauth_response: OAuth response dict containing authed_user and team info

        Returns:
            Dict with user spatial context:
                - user_id: str - User's Slack ID
                - user_name: str - User's display name
                - territory_id: str - Workspace/team ID
                - capabilities: list - List of granted scopes

        Example:
            >>> oauth_response = {
            ...     "authed_user": {"id": "U123", "name": "Alice", "scope": "chat:write"},
            ...     "team": {"id": "T456", "name": "Workspace"}
            ... }
            >>> handler.get_user_spatial_context(oauth_response)
            {
                'user_id': 'U123',
                'user_name': 'Alice',
                'territory_id': 'T456',
                'capabilities': ['chat:write']
            }
        """
        try:
            # Extract user information
            authed_user = oauth_response.get("authed_user", {})
            user_id = authed_user.get("id", "")
            user_name = authed_user.get("name", "Unknown User")

            # Extract territory (workspace) information
            team_info = oauth_response.get("team", {})
            territory_id = team_info.get("id", "")

            # Get spatial capabilities (reuse existing method)
            capabilities = self.get_spatial_capabilities(oauth_response)

            user_context = {
                "user_id": user_id,
                "user_name": user_name,
                "territory_id": territory_id,
                "capabilities": capabilities,
            }

            logger.info(
                f"Extracted user spatial context for {user_name} ({user_id}) in territory {territory_id}"
            )
            return user_context

        except Exception as e:
            logger.error(f"Failed to extract user spatial context: {e}")
            raise

    def refresh_spatial_territory(self, refresh_response: Dict[str, Any]):
        """
        Refresh spatial territory after OAuth token refresh.

        Updates territory metadata when an OAuth token is refreshed, maintaining
        the same territory ID but updating the access token and other mutable fields.

        This method handles token refresh scenarios where the workspace/territory
        remains the same but credentials need to be updated.

        Args:
            refresh_response: OAuth token refresh response (same structure as initial OAuth response)

        Returns:
            Updated SpatialTerritory object with refreshed access token

        Raises:
            ValueError: If OAuth response indicates failure

        Example:
            >>> refresh_response = {
            ...     "access_token": "xoxb-new-token",
            ...     "team": {"id": "T123456", "name": "Test Workspace"}
            ... }
            >>> updated_territory = handler.refresh_spatial_territory(refresh_response)
            >>> updated_territory.access_token
            'xoxb-new-token'

        Note:
            This reuses initialize_spatial_territory() logic since the data structure
            is identical. The distinction is semantic - refresh vs initial setup.
        """
        try:
            # Extract territory info for logging
            team_info = refresh_response.get("team", {})
            territory_id = team_info.get("id", "")

            logger.info(f"Refreshing spatial territory for workspace {territory_id}")

            # Reuse initialization logic - structure is identical
            # The difference is semantic (refresh vs create), not structural
            territory = self.initialize_spatial_territory(refresh_response)

            logger.info(f"Spatial territory refreshed: {territory.name} ({territory.territory_id})")
            return territory

        except Exception as e:
            logger.error(f"Failed to refresh spatial territory: {e}")
            raise

    def validate_and_initialize_spatial_territory(
        self, oauth_response: Dict[str, Any], expected_state: str
    ):
        """
        Initialize spatial territory on OAuth success after state validation.

        Validates the OAuth state parameter for security, then initializes the
        spatial territory. This method combines security validation with territory
        creation to ensure OAuth callbacks are legitimate before creating workspace
        representations.

        Args:
            oauth_response: OAuth response dict containing state and workspace data
            expected_state: Expected state value for validation

        Returns:
            SpatialTerritory object for the authenticated workspace

        Raises:
            ValueError: If OAuth state is invalid or missing

        Example:
            >>> oauth_response = {
            ...     "access_token": "xoxb-token",
            ...     "state": "secure-state-123",
            ...     "team": {"id": "T123", "name": "Workspace"}
            ... }
            >>> territory = handler.validate_and_initialize_spatial_territory(
            ...     oauth_response, "secure-state-123"
            ... )
            >>> territory.territory_id
            'T123'

        Security:
            The state parameter prevents CSRF attacks in the OAuth flow.
            This method MUST be used for OAuth callbacks rather than calling
            initialize_spatial_territory() directly.
        """
        try:
            # Extract and validate state parameter
            received_state = oauth_response.get("state")

            # State validation
            if not received_state:
                raise ValueError("Invalid OAuth state: state parameter missing")

            if received_state != expected_state:
                logger.warning(
                    f"OAuth state mismatch: expected {expected_state[:8]}..., "
                    f"received {received_state[:8]}..."
                )
                raise ValueError("Invalid OAuth state: state mismatch")

            # State is valid - proceed with territory initialization
            logger.info("OAuth state validated successfully")

            # Initialize territory
            territory = self.initialize_spatial_territory(oauth_response)

            logger.info(f"Spatial territory initialized after state validation: {territory.name}")
            return territory

        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Failed to validate and initialize spatial territory: {e}")
            raise
