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

        # #2043 (#1324 class): the setup-wizard callback derives from PIPER_BASE_URL and
        # carries the router's real path (/api/v1/setup/...); the old default had no
        # /api/v1 prefix and could not reach the route even on localhost.
        _base = os.getenv("PIPER_BASE_URL", "http://localhost:8001").rstrip("/")
        self.redirect_uri = (
            os.getenv("GOOGLE_CALENDAR_REDIRECT_URI")
            or f"{_base}/api/v1/setup/calendar/oauth/callback"
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
            # #2087/#2092 (Comms' read): the address itself stays out of the log.
            has_email=bool(user_info.get("email")),
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

        #2151 (route group 1): on None, ``last_refresh_error`` says why: ``"revoked"``
        when Google rejects the grant (``invalid_grant``), ``"unavailable"`` for anything
        else (a 5xx, an unexpected status). A Test that couldn't run is not a revoked token.
        """
        self.last_refresh_error: Optional[str] = None
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
                    self.last_refresh_error = (
                        "revoked"
                        if response.status in (400, 401) and "invalid_grant" in error_text
                        else "unavailable"
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


CALENDAR_READ_SCOPE = "https://www.googleapis.com/auth/calendar.readonly"

# #2148 (CXO 10-23): the connect moment's words when the grant lacks calendar access,
# and when the granted scopes can't be read from Google's token response.
CALENDAR_SCOPE_MISSING_LINE = (
    "Google is connected, but you didn't allow calendar access, so I can't read your "
    "calendar yet. Connect again and tick the calendar box on Google's consent page."
)
CALENDAR_SCOPE_UNCONFIRMED_LINE = (
    "I couldn't confirm what Google allowed. Open Settings and run the test."
)


def calendar_access_granted(scope: Optional[str]) -> Optional[bool]:
    """#2148: whether Google's token response granted calendar read access.

    Google returns the GRANTED scopes (space-separated) in the token response's
    ``scope``; with the unverified app's consent page the calendar box starts
    unticked, so a user can finish the flow without it. True/False when the
    list is readable; None when it is empty or absent (unconfirmed, never
    treated as granted).
    """
    if not isinstance(scope, str) or not scope.strip():
        return None
    granted = set(scope.split())
    return CALENDAR_READ_SCOPE in granted or "https://www.googleapis.com/auth/calendar" in granted


async def resolve_calendar_grant(tokens) -> str:
    """#2148 (Arch 10-23): "granted", "not_granted" or "unconfirmed", one derivation.

    The token response's ``scope`` decides when present; when it is empty or
    absent, the #2092 Test's own read (``probe_calendar_read``) decides: Google
    answering means granted, ``insufficient_scope`` means not granted, anything
    else (another refusal, a timeout) is unconfirmed. Never "granted" on an
    unknown.
    """
    granted = calendar_access_granted(getattr(tokens, "scope", None))
    if granted is True:
        return "granted"
    if granted is False:
        return "not_granted"
    access_token = getattr(tokens, "access_token", None)
    if not isinstance(access_token, str) or not access_token:
        return "unconfirmed"
    try:
        read_error = await probe_calendar_read(access_token)
    except (
        Exception
    ):  # silent-ok: an unreadable grant is "unconfirmed", never "granted" (#2148 fail-closed)
        return "unconfirmed"
    if read_error is None:
        return "granted"
    if read_error == "insufficient_scope":
        return "not_granted"
    return "unconfirmed"


async def probe_calendar_read(access_token: str) -> Optional[str]:
    """#2092: one real, minimal calendar read with a fresh access token.

    Returns None when Google answers, else the class from
    ``classify_calendar_read_error`` ("insufficient_scope" when the grant lacks
    calendar access, the 2026-10-19 alpha shape that a token refresh alone can
    never see). Used by the Settings Test so "Healthy" means readable.
    """
    import asyncio

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    from services.integrations.calendar.read_errors import classify_calendar_read_error

    def _read() -> None:
        service = build("calendar", "v3", credentials=Credentials(token=access_token))
        service.events().list(calendarId="primary", maxResults=1, singleEvents=True).execute()

    try:
        await asyncio.wait_for(asyncio.to_thread(_read), timeout=10.0)
    except Exception as exc:  # noqa: BLE001 — the class is the whole answer here
        error_class = classify_calendar_read_error(exc)
        # 2026-10-21 (Exec's ask: "the server log for that read"): there was none.
        # Log the class and the exception type, never the text (it can carry URLs
        # and ids) and never the token.
        logger.warning(
            "calendar_read_probe_failed",
            error_class=error_class,
            exception_type=type(exc).__name__,
        )
        return error_class
    return None
