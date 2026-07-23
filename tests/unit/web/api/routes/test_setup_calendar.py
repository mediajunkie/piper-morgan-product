"""
Unit tests for Google Calendar OAuth in setup wizard
Issue #529: ALPHA-SETUP-CALENDAR

Tests Calendar OAuth flow initiation, callback handling,
and status checking in the setup wizard context.

Note: These tests mock the GoogleCalendarOAuthHandler at the import location
within the function (services.integrations.calendar.oauth_handler).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytestmark = pytest.mark.unit


class TestCalendarOAuthTrigger:
    """Tests for initiating Calendar OAuth from setup wizard"""

    @pytest.mark.asyncio
    async def test_get_calendar_oauth_url_returns_authorization_url(self):
        """Should return Google OAuth URL with state"""
        from web.api.routes.setup import start_calendar_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # When: Requesting OAuth start
        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_instance.client_id = "test_client_id"
            mock_instance.client_secret = "test_client_secret"
            mock_instance.generate_authorization_url.return_value = (
                "https://accounts.google.com/o/oauth2/v2/auth?client_id=test&scope=calendar.readonly",
                "state_abc123",
            )
            MockHandler.return_value = mock_instance

            response = await start_calendar_oauth(current_user=mock_user)

        # Then: Response contains auth URL and state
        assert "auth_url" in response
        assert "state" in response
        assert "accounts.google.com" in response["auth_url"]
        assert response["state"] == "state_abc123"
        # Verify user_id was passed to generate_authorization_url
        mock_instance.generate_authorization_url.assert_called_once_with(user_id="test-user-123")

    @pytest.mark.asyncio
    async def test_oauth_url_includes_calendar_scope(self):
        """OAuth URL should include calendar.readonly scope"""
        from web.api.routes.setup import start_calendar_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # When: Requesting OAuth start
        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_instance.client_id = "test_client_id"
            mock_instance.client_secret = "test_client_secret"
            mock_instance.generate_authorization_url.return_value = (
                "https://accounts.google.com/o/oauth2/v2/auth?scope=https://www.googleapis.com/auth/calendar.readonly",
                "state_xyz789",
            )
            MockHandler.return_value = mock_instance

            response = await start_calendar_oauth(current_user=mock_user)

        # Then: URL should contain calendar scope
        assert "calendar" in response["auth_url"].lower()

    @pytest.mark.asyncio
    async def test_oauth_url_requests_offline_access(self):
        """OAuth URL should request offline access for refresh token"""
        from web.api.routes.setup import start_calendar_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_instance.client_id = "test_client_id"
            mock_instance.client_secret = "test_client_secret"
            mock_instance.generate_authorization_url.return_value = (
                "https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent",
                "state_offline",
            )
            MockHandler.return_value = mock_instance

            response = await start_calendar_oauth(current_user=mock_user)

        # Then: URL should request offline access
        assert "offline" in response["auth_url"] or "consent" in response["auth_url"]

    @pytest.mark.asyncio
    async def test_start_oauth_fails_without_credentials(self):
        """Should return error when credentials not configured"""
        from fastapi import HTTPException

        from web.api.routes.setup import start_calendar_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_instance.client_id = ""  # Not configured
            mock_instance.client_secret = ""
            MockHandler.return_value = mock_instance

            with pytest.raises(HTTPException) as exc_info:
                await start_calendar_oauth(current_user=mock_user)

            assert exc_info.value.status_code == 503
            assert "not configured" in exc_info.value.detail.lower()


class TestCalendarOAuthCallback:
    """Tests for OAuth callback handling in setup context"""

    @pytest.mark.asyncio
    async def test_callback_success_redirects_with_email(self):
        """Successful callback should redirect with calendar email"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_calendar_oauth_callback

        # Mock the handler
        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_tokens = MagicMock()
            mock_tokens.refresh_token = "refresh_token_123"
            mock_instance.handle_oauth_callback = AsyncMock(
                return_value={
                    "tokens": mock_tokens,
                    "user": {"email": "test@gmail.com", "name": "Test User"},
                    "user_id": "test_user_456",  # Issue #917: user_id required
                }
            )
            MockHandler.return_value = mock_instance

            # Mock keychain
            with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
                mock_keychain = MagicMock()
                MockKeychain.return_value = mock_keychain

                response = await handle_calendar_oauth_callback(
                    code="test_code_123", state="valid_state_abc", error=None
                )

        # Then: Redirects to setup with success
        assert isinstance(response, RedirectResponse)
        assert response.status_code == 302
        location = str(response.headers.get("location", ""))
        assert "calendar_success=true" in location
        assert "test%40gmail.com" in location or "test@gmail.com" in location

    @pytest.mark.asyncio
    async def test_callback_error_redirects_with_error(self):
        """OAuth error should redirect with error message"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_calendar_oauth_callback

        # When: Callback has error parameter
        response = await handle_calendar_oauth_callback(
            code=None, state=None, error="access_denied"
        )

        # Then: Redirects with error
        assert isinstance(response, RedirectResponse)
        assert response.status_code == 302
        assert "calendar_error=access_denied" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_missing_params_returns_error(self):
        """Missing code/state should return error redirect"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_calendar_oauth_callback

        # When: Callback missing required params
        response = await handle_calendar_oauth_callback(code=None, state=None, error=None)

        # Then: Redirects with missing_params error
        assert isinstance(response, RedirectResponse)
        assert "calendar_error=missing_params" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_invalid_state_returns_error(self):
        """Invalid/expired state should return clear error"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_calendar_oauth_callback

        # When: Callback with invalid state
        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_instance.handle_oauth_callback = AsyncMock(
                side_effect=ValueError("Invalid or expired state")
            )
            MockHandler.return_value = mock_instance

            response = await handle_calendar_oauth_callback(
                code="test_code", state="expired_state", error=None
            )

        # Then: Redirects with callback_failed error
        assert isinstance(response, RedirectResponse)
        assert "calendar_error=callback_failed" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_stores_refresh_token_with_user_scope(self):
        """Callback should store refresh token in keychain with user-scoped key.

        Issue #917: Token must be stored under user-scoped key
        (google_calendar_{user_id}), never the global 'google_calendar' key.
        """
        from web.api.routes.setup import handle_calendar_oauth_callback

        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_tokens = MagicMock()
            mock_tokens.refresh_token = "refresh_token_to_store"
            mock_instance.handle_oauth_callback = AsyncMock(
                return_value={
                    "tokens": mock_tokens,
                    "user": {"email": "test@gmail.com"},
                    "user_id": "test_user_123",  # Issue #917: user_id required
                }
            )
            MockHandler.return_value = mock_instance

            with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
                mock_keychain = MagicMock()
                MockKeychain.return_value = mock_keychain

                await handle_calendar_oauth_callback(
                    code="test_code", state="valid_state", error=None
                )

                # Then: Keychain should have stored the token with user-scoped key
                mock_keychain.store_api_key.assert_called_once_with(
                    "google_calendar_test_user_123", "refresh_token_to_store"
                )

    @pytest.mark.asyncio
    async def test_callback_rejects_missing_user_id(self):
        """Callback must not store token when user_id is missing.

        Issue #917: Storing under global key causes cross-user credential leakage.
        """
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_calendar_oauth_callback

        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ) as MockHandler:
            mock_instance = MagicMock()
            mock_tokens = MagicMock()
            mock_tokens.refresh_token = "refresh_token_to_store"
            mock_instance.handle_oauth_callback = AsyncMock(
                return_value={
                    "tokens": mock_tokens,
                    "user": {"email": "test@gmail.com"},
                    # No user_id — this should be rejected
                }
            )
            MockHandler.return_value = mock_instance

            with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
                mock_keychain = MagicMock()
                MockKeychain.return_value = mock_keychain

                response = await handle_calendar_oauth_callback(
                    code="test_code", state="valid_state", error=None
                )

                # Token must NOT be stored
                mock_keychain.store_api_key.assert_not_called()
                # Should redirect with error
                assert isinstance(response, RedirectResponse)
                assert "missing_user_id" in str(response.headers.get("location", ""))


class TestCalendarSetupStatus:
    """Tests for Calendar status in setup wizard"""

    def _mock_request_with_jwt(self, user_id="test_user"):
        """Create a mock Request with auth cookie and mock JWTService."""
        mock_request = MagicMock()
        mock_request.cookies = {"auth_token": "fake_jwt"}
        mock_claims = MagicMock()
        mock_claims.sub = user_id
        mock_jwt_service = MagicMock()
        # #1434: validate_token is async — a sync MagicMock return makes the
        # route's await raise into its silent fallback (the exact bug #1434
        # fixed in the route; the mock had the same rot).
        mock_jwt_service.validate_token = AsyncMock(return_value=mock_claims)
        return mock_request, mock_jwt_service

    @pytest.mark.asyncio
    async def test_check_calendar_configured_with_token(self):
        """Should return configured=True when refresh token exists"""
        from web.api.routes.setup import get_calendar_status

        mock_request, mock_jwt = self._mock_request_with_jwt()

        with (
            patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain,
            patch("services.auth.jwt_service.JWTService", return_value=mock_jwt),
        ):
            mock_keychain = MagicMock()
            mock_keychain.get_api_key.return_value = "stored_refresh_token"
            MockKeychain.return_value = mock_keychain

            response = await get_calendar_status(mock_request)

        assert response["configured"] is True

    @pytest.mark.asyncio
    async def test_check_calendar_not_configured(self):
        """Should return configured=False when no token"""
        from web.api.routes.setup import get_calendar_status

        mock_request, mock_jwt = self._mock_request_with_jwt()

        with (
            patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain,
            patch("services.auth.jwt_service.JWTService", return_value=mock_jwt),
        ):
            mock_keychain = MagicMock()
            mock_keychain.get_api_key.return_value = None
            MockKeychain.return_value = mock_keychain

            response = await get_calendar_status(mock_request)

        assert response["configured"] is False

    @pytest.mark.asyncio
    async def test_status_check_handles_keychain_error(self):
        """Should handle keychain errors gracefully"""
        from web.api.routes.setup import get_calendar_status

        mock_request, mock_jwt = self._mock_request_with_jwt()

        with (
            patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain,
            patch("services.auth.jwt_service.JWTService", return_value=mock_jwt),
        ):
            mock_keychain = MagicMock()
            mock_keychain.get_api_key.side_effect = Exception("Keychain access denied")
            MockKeychain.return_value = mock_keychain

            response = await get_calendar_status(mock_request)

        assert response["configured"] is False
        assert "failed" in response["message"].lower()

    @pytest.mark.asyncio
    async def test_status_uses_user_scoped_key(self):
        """Issue #839: Should use user-scoped keychain key"""
        from web.api.routes.setup import get_calendar_status

        mock_request, mock_jwt = self._mock_request_with_jwt("alice_123")

        with (
            patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain,
            patch("services.auth.jwt_service.JWTService", return_value=mock_jwt),
        ):
            mock_keychain = MagicMock()
            mock_keychain.get_api_key.return_value = None
            MockKeychain.return_value = mock_keychain

            await get_calendar_status(mock_request)

            mock_keychain.get_api_key.assert_called_once_with("google_calendar_alice_123")
