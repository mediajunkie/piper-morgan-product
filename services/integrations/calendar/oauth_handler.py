"""
Google Calendar OAuth Handler for Web Flow

Issue #529: ALPHA-SETUP-CALENDAR
Implements standard OAuth 2.0 web server flow for Google Calendar.
"""

import os
import secrets
import time
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode

import aiohttp
import structlog

logger = structlog.get_logger(__name__)

# Module-level state storage (singleton pattern)
# This ensures state persists across handler instances within the same process.
# Production should use Redis/DB - this works for single-server alpha.
_PENDING_STATES: Dict[str, float] = {}


@dataclass
class CalendarTokens:
    """OAuth tokens for Google Calendar"""

    access_token: str
    refresh_token: Optional[str]
    expires_at: int  # Unix timestamp
    token_type: str = "Bearer"
    scope: str = ""


class GoogleCalendarOAuthHandler:
    """
    OAuth 2.0 web flow handler for Google Calendar.

    Implements standard authorization code flow:
    1. Generate authorization URL with state
    2. User authorizes at Google
    3. Handle callback with code exchange
    4. Return tokens and user info

    Issue #529: ALPHA-SETUP-CALENDAR
    """

    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
    REVOKE_URL = "https://oauth2.googleapis.com/revoke"

    # State tokens expire after 15 minutes
    STATE_EXPIRATION = 900

    def __init__(self):
        # Issue #577: Load credentials with keychain fallback
        # Issue #734: Uses IntegrationConfigService for app credentials
        # Priority: env vars > IntegrationConfigService
        self.client_id = os.getenv("GOOGLE_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")

        # Fallback to IntegrationConfigService if env vars not set
        if not self.client_id or not self.client_secret:
            try:
                from services.integrations.integration_config_service import (
                    IntegrationConfigService,
                )

                config_service = IntegrationConfigService()
                if not self.client_id:
                    self.client_id = config_service.get_google_client_id() or ""
                if not self.client_secret:
                    self.client_secret = config_service.get_google_client_secret() or ""
            except Exception:
                pass  # Config service not available, continue with empty values

        self.redirect_uri = os.getenv(
            "GOOGLE_CALENDAR_REDIRECT_URI", "http://localhost:8001/setup/calendar/oauth/callback"
        )
        self.scopes = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/userinfo.email",
        ]
        # State storage is now module-level (_PENDING_STATES) to persist across instances

    def generate_authorization_url(
        self, user_id: str, return_url: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Generate Google OAuth authorization URL with user-scoped state.

        Issue #734: SEC-MULTITENANCY - Embed user_id in OAuth state for
        multi-tenant isolation.

        Args:
            user_id: The ID of the user initiating OAuth flow (required)
            return_url: Optional URL to redirect to after OAuth completes

        Returns:
            Tuple of (authorization_url, state_token)

        Raises:
            ValueError: If user_id is not provided
        """
        if not user_id:
            raise ValueError("user_id is required for OAuth state")

        # Create state with user_id, nonce, and optional return_url
        nonce = secrets.token_urlsafe(16)
        state_data = {
            "user_id": user_id,
            "nonce": nonce,
        }
        if return_url:
            state_data["return_url"] = return_url

        # Encode state as base64 JSON (safe for URL parameter)
        import base64
        import json

        state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")

        # Store nonce with timestamp and user_id for verification
        # Issue #734: Store user_id to detect tampering
        _PENDING_STATES[nonce] = {
            "created_at": time.time(),
            "user_id": user_id,
        }

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "access_type": "offline",  # Request refresh token
            "state": state,
            "prompt": "consent",  # Force consent to get refresh token
        }

        auth_url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"

        logger.info(
            "calendar_oauth_url_generated",
            user_id=user_id,
            state_prefix=state[:8],
            redirect_uri=self.redirect_uri,
        )

        return auth_url, state

    def _verify_state(self, state: str) -> Tuple[bool, Optional[str]]:
        """
        Verify state token is valid and not expired.

        Issue #734: SEC-MULTITENANCY - Extract user_id from state and verify
        against stored value to detect tampering.

        Args:
            state: The base64-encoded state parameter from callback

        Returns:
            Tuple of (is_valid, user_id). user_id is None if invalid.
        """
        import base64
        import json

        # Decode state to extract nonce and user_id
        try:
            # Add padding if needed for base64 decode
            padded = state + "=" * (4 - len(state) % 4)
            decoded = base64.urlsafe_b64decode(padded)
            state_data = json.loads(decoded)
        except (ValueError, json.JSONDecodeError) as e:
            logger.warning(
                "calendar_oauth_state_decode_failed",
                state_prefix=state[:8] if state else "none",
                error=str(e),
            )
            return False, None

        nonce = state_data.get("nonce")
        user_id = state_data.get("user_id")

        if not nonce or not user_id:
            logger.warning(
                "calendar_oauth_state_missing_fields",
                has_nonce=bool(nonce),
                has_user_id=bool(user_id),
            )
            return False, None

        if nonce not in _PENDING_STATES:
            logger.warning(
                "calendar_oauth_state_not_found", nonce_prefix=nonce[:8] if nonce else "none"
            )
            return False, None

        nonce_data = _PENDING_STATES[nonce]
        created_at = nonce_data["created_at"]

        if time.time() - created_at > self.STATE_EXPIRATION:
            del _PENDING_STATES[nonce]
            logger.warning("calendar_oauth_state_expired", nonce_prefix=nonce[:8])
            return False, None

        # Issue #734: Verify user_id matches stored value (detect tampering)
        stored_user_id = nonce_data.get("user_id")
        if stored_user_id and stored_user_id != user_id:
            logger.warning(
                "calendar_oauth_state_user_id_mismatch",
                expected=stored_user_id,
                received=user_id,
            )
            del _PENDING_STATES[nonce]
            return False, None

        # Remove state after successful verification (single-use)
        del _PENDING_STATES[nonce]
        return True, user_id

    def verify_state(self, state: str) -> Tuple[bool, Optional[str]]:
        """
        Public method to verify OAuth state and extract user_id.

        Issue #734: SEC-MULTITENANCY - State verification for multi-tenant.

        Args:
            state: The base64-encoded state parameter from callback

        Returns:
            Tuple of (is_valid, user_id). user_id is None if invalid.
        """
        return self._verify_state(state)

    async def handle_oauth_callback(self, code: str, state: str) -> Dict:
        """
        Handle OAuth callback: verify state, exchange code, get user info.

        Issue #734: SEC-MULTITENANCY - Extract and return user_id from state.

        Args:
            code: Authorization code from Google
            state: State token for CSRF verification (includes user_id)

        Returns:
            Dict with tokens, user info, and user_id from state

        Raises:
            ValueError: If state is invalid or expired
        """
        is_valid, user_id = self._verify_state(state)
        if not is_valid:
            raise ValueError("Invalid or expired state token")

        # Exchange code for tokens
        tokens = await self._exchange_code_for_tokens(code)

        # Get user info (email)
        user_info = await self._get_user_info(tokens.access_token)

        logger.info(
            "calendar_oauth_callback_success",
            user_id=user_id,
            email=user_info.get("email", "unknown"),
            has_refresh_token=bool(tokens.refresh_token),
        )

        return {
            "tokens": tokens,
            "user": user_info,
            "user_id": user_id,  # Issue #734: Return user_id for per-user storage
        }

    async def _exchange_code_for_tokens(self, code: str) -> CalendarTokens:
        """Exchange authorization code for access/refresh tokens."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": self.redirect_uri,
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "calendar_token_exchange_failed",
                        status=response.status,
                        error=error_text,
                    )
                    raise ValueError(f"Token exchange failed: {error_text}")

                data = await response.json()

                return CalendarTokens(
                    access_token=data["access_token"],
                    refresh_token=data.get("refresh_token"),
                    expires_at=int(time.time()) + data.get("expires_in", 3600),
                    token_type=data.get("token_type", "Bearer"),
                    scope=data.get("scope", ""),
                )

    async def revoke_token(self, token: str) -> bool:
        """Revoke a Google OAuth token (#542: actual server-side revocation on disconnect).

        Revoking a refresh token also invalidates any access token derived from it, so
        callers only need to pass the stored refresh token. Best-effort: a failure here
        must never block clearing the local credential (Google's own guidance -- an
        already-invalid/expired token still returns 200; other failures are logged, not
        raised).
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.REVOKE_URL,
                    data={"token": token},
                ) as response:
                    if response.status == 200:
                        logger.info("calendar_token_revoked")
                        return True
                    logger.warning(
                        "calendar_token_revoke_failed",
                        status=response.status,
                    )
                    return False
        except Exception as e:
            logger.warning("calendar_token_revoke_error", error=str(e))
            return False

    async def _get_user_info(self, access_token: str) -> Dict:
        """Get user email from Google."""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            ) as response:
                if response.status != 200:
                    logger.warning(
                        "calendar_userinfo_failed",
                        status=response.status,
                    )
                    return {"email": "Unknown"}

                data = await response.json()
                return {
                    "email": data.get("email", "Unknown"),
                    "name": data.get("name", ""),
                }

    async def refresh_access_token(self, refresh_token: str) -> Optional[CalendarTokens]:
        """
        Refresh an expired access token using refresh token.

        Args:
            refresh_token: The stored refresh token

        Returns:
            New CalendarTokens or None if refresh failed
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.TOKEN_URL,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token",
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(
                        "calendar_token_refresh_failed",
                        status=response.status,
                        error=error_text,
                    )
                    return None

                data = await response.json()

                return CalendarTokens(
                    access_token=data["access_token"],
                    refresh_token=refresh_token,  # Keep the original refresh token
                    expires_at=int(time.time()) + data.get("expires_in", 3600),
                    token_type=data.get("token_type", "Bearer"),
                    scope=data.get("scope", ""),
                )
