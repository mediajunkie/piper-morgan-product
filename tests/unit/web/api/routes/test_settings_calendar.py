"""
Unit tests for Google Calendar Settings API
Issue #537: ALPHA-SETUP-MANAGE - Integration Management Post-Setup

Tests the Google Calendar OAuth management endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    CalendarAppCredentialsRequest,
    disconnect_calendar,
    get_calendar_app_credentials_status,
    get_calendar_settings,
    save_calendar_app_credentials,
)


def _mock_current_user(user_id="test_user"):
    """Create a mock JWTClaims object for testing."""
    mock_user = MagicMock()
    mock_user.sub = user_id
    return mock_user


class TestGetCalendarSettings:
    """Tests for GET /api/v1/settings/integrations/calendar.

    #2151 (route group 1): the card answers from the Test button's own check
    (``_test_calendar``): a provenance keychain read, the refresh's recorded reason, and
    the real-read probe. A check that couldn't run is ``check_failed``, never "expired or
    revoked", and ``valid`` needs a calendar read that worked."""

    @staticmethod
    def _patches(read, *, tokens=None, refresh_error=None, refresh_raises=None, probe=None):
        from services.infrastructure.keychain_service import SecretProvenance, SecretRead

        keychain = MagicMock()
        if read is None:
            keychain.aread_secret = AsyncMock(
                return_value=SecretRead(SecretProvenance.VERIFIED_ABSENT)
            )
        elif read == "STORE_FAILED":
            keychain.aread_secret = AsyncMock(
                return_value=SecretRead(SecretProvenance.STORE_FAILED, error="timeout")
            )
        else:
            keychain.aread_secret = AsyncMock(
                return_value=SecretRead(SecretProvenance.PRESENT, value=read)
            )
        handler = MagicMock()
        handler.refresh_access_token = (
            AsyncMock(side_effect=refresh_raises, return_value=tokens)
            if refresh_raises
            else AsyncMock(return_value=tokens)
        )
        handler.last_refresh_error = refresh_error
        return keychain, [
            patch(
                "services.infrastructure.keychain_service.KeychainService", return_value=keychain
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=handler,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.probe_calendar_read",
                new=AsyncMock(return_value=probe),
            ),
        ]

    async def _get(self, patches, user="test-user"):
        for p in patches:
            p.start()
        try:
            return await get_calendar_settings(current_user=_mock_current_user(user))
        finally:
            for p in patches:
                p.stop()

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_token(self):
        _kc, patches = self._patches(None)
        result = await self._get(patches)
        assert result == {"configured": False, "valid": False, "email": None, "error": None}

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_a_calendar_read_works(self):
        _kc, patches = self._patches("valid_refresh_token", tokens=MagicMock(access_token="t"))
        result = await self._get(patches)
        assert result["configured"] is True and result["valid"] is True
        assert result["error"] is None

    @pytest.mark.asyncio
    async def test_a_revoked_grant_is_configured_but_invalid(self):
        _kc, patches = self._patches("expired_refresh_token", refresh_error="revoked")
        result = await self._get(patches)
        assert result["configured"] is True and result["valid"] is False
        assert "expired or revoked" in result["error"]

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"refresh_error": "unavailable"},
            {"refresh_raises": Exception("API error")},
        ],
    )
    async def test_a_check_that_couldnt_run_is_check_failed_not_revoked(self, kwargs):
        from web.api.routes.settings_integrations import CALENDAR_STATUS_CHECK_FAILED_LINE

        _kc, patches = self._patches("a_refresh_token", **kwargs)
        result = await self._get(patches)
        assert result["check_failed"] is True
        assert result["error"] == CALENDAR_STATUS_CHECK_FAILED_LINE
        assert "revoked" not in result["error"] and "API error" not in result["error"]

    @pytest.mark.asyncio
    async def test_a_store_that_failed_is_check_failed(self):
        _kc, patches = self._patches("STORE_FAILED")
        result = await self._get(patches)
        assert result["check_failed"] is True

    @pytest.mark.asyncio
    async def test_a_refresh_without_calendar_access_is_not_valid(self):
        """#2148/#2092 shape: a refresh works with any scope; the card needs a real read."""
        _kc, patches = self._patches(
            "a_refresh_token", tokens=MagicMock(access_token="t"), probe="insufficient_scope"
        )
        result = await self._get(patches)
        assert result["configured"] is True and result["valid"] is False
        assert "calendar access" in result["error"]

    @pytest.mark.asyncio
    async def test_uses_user_scoped_keychain_key(self):
        """Issue #839: Should use user-scoped keychain key for isolation"""
        kc, patches = self._patches(None)
        await self._get(patches, user="user_abc")
        kc.aread_secret.assert_awaited_once_with("google_calendar_user_abc")


def _async_keychain(get_value=None):
    """KeychainService double for the async disconnect path (#2172): deletes succeed and
    the provenance read-back answers VERIFIED_ABSENT unless a test says otherwise."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    kc = MagicMock()
    kc.adelete_api_key = AsyncMock(return_value=True)
    kc.aget_api_key = AsyncMock(return_value=get_value)
    kc.aread_secret = AsyncMock(return_value=SecretRead(SecretProvenance.VERIFIED_ABSENT))
    return kc


def _github_credential_gone():
    """The GitHub read-back (#2172) finds no credential: CONNECT_REQUIRED, no leg."""
    from types import SimpleNamespace

    from services.mcp.consumer.connector import DegradationReason

    return patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
        AsyncMock(return_value=SimpleNamespace(reason=DegradationReason.CONNECT_REQUIRED)),
    )


class TestDisconnectCalendar:
    """Tests for POST /api/v1/settings/integrations/calendar/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should remove token from keychain and return success"""
        mock_keychain = _async_keychain()

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await disconnect_calendar(current_user=_mock_current_user("test_user"))

            assert result["success"] is True
            assert result["message"] == "Google Calendar disconnected"  # #2172: CXO display name
            # Issue #839: Should use user-scoped key
            mock_keychain.adelete_api_key.assert_awaited_once_with(
                "google_calendar_test_user", None
            )

    @pytest.mark.asyncio
    async def test_succeeds_even_when_no_token_exists(self):
        """Should still succeed even if no token exists to clear"""
        mock_keychain = _async_keychain()
        mock_keychain.adelete_api_key.side_effect = Exception("Key not found")

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await disconnect_calendar(current_user=_mock_current_user())

            assert result["success"] is True
            assert result["message"] == "Google Calendar disconnected"  # #2172: CXO display name


class TestIntegrationRegistryCalendarUrl:
    """Tests for Calendar configure_url in INTEGRATION_REGISTRY (Issue #537)"""

    def test_calendar_configure_url_points_to_settings_page(self):
        """Calendar configure_url should point to dedicated settings page"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        calendar_config = INTEGRATION_REGISTRY.get("calendar")
        assert calendar_config is not None
        assert calendar_config["configure_url"] == "/settings/integrations/calendar"
        # Should NOT be None anymore
        assert calendar_config["configure_url"] is not None


class TestCalendarAppCredentials:
    """Tests for Calendar app credentials endpoints (Issue #577)"""

    @pytest.mark.asyncio
    async def test_save_credentials_stores_in_keychain(self):
        """Should store client_id and client_secret via IntegrationConfigService (Issue #734)"""
        mock_config_service = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = CalendarAppCredentialsRequest(
            client_id="123456789.apps.googleusercontent.com",
            client_secret="GOCSPX-test_secret_value",
        )

        with patch(
            "services.integrations.integration_config_service.IntegrationConfigService",
            return_value=mock_config_service,
        ):
            result = await save_calendar_app_credentials(credentials, mock_user)

            assert result["success"] is True
            assert "saved" in result["message"].lower()
            # Verify IntegrationConfigService was called with correct credentials
            mock_config_service.store_google_credentials.assert_called_once_with(
                "123456789.apps.googleusercontent.com", "GOCSPX-test_secret_value"
            )

    @pytest.mark.asyncio
    async def test_save_credentials_strips_whitespace(self):
        """Should strip whitespace from credentials before storing (Issue #734)"""
        mock_config_service = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = CalendarAppCredentialsRequest(
            client_id="  123456789.apps.googleusercontent.com  ",
            client_secret="  GOCSPX-secret_with_spaces  ",
        )

        with patch(
            "services.integrations.integration_config_service.IntegrationConfigService",
            return_value=mock_config_service,
        ):
            await save_calendar_app_credentials(credentials, mock_user)

            # Verify whitespace was stripped
            mock_config_service.store_google_credentials.assert_called_once_with(
                "123456789.apps.googleusercontent.com", "GOCSPX-secret_with_spaces"
            )

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_when_both_present(self):
        """Should return configured=True when both client_id and client_secret exist (Issue #734)"""
        mock_config_service = MagicMock()
        mock_config_service.get_google_client_id.return_value = (
            "123456789.apps.googleusercontent.com"
        )
        mock_config_service.get_google_client_secret.return_value = "GOCSPX-secret_value"
        mock_user = MagicMock()

        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=mock_config_service,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is True
            assert result.has_client_id is True
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_id(self):
        """Should return configured=False when client_id is missing (Issue #734)"""
        mock_config_service = MagicMock()
        mock_config_service.get_google_client_id.return_value = ""  # Empty
        mock_config_service.get_google_client_secret.return_value = "GOCSPX-secret_value"
        mock_user = MagicMock()

        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=mock_config_service,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is False
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_secret(self):
        """Should return configured=False when client_secret is missing (Issue #734)"""
        mock_config_service = MagicMock()
        mock_config_service.get_google_client_id.return_value = (
            "123456789.apps.googleusercontent.com"
        )
        mock_config_service.get_google_client_secret.return_value = ""  # Empty
        mock_user = MagicMock()

        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=mock_config_service,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is True
            assert result.has_client_secret is False

    @pytest.mark.asyncio
    async def test_get_status_falls_back_to_env_vars(self):
        """Should check environment variables as fallback when service returns empty (Issue #734)"""
        mock_config_service = MagicMock()
        mock_config_service.get_google_client_id.return_value = ""  # Service returns nothing
        mock_config_service.get_google_client_secret.return_value = ""
        mock_user = MagicMock()

        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=mock_config_service,
            ),
            patch.dict(
                "os.environ",
                {
                    "GOOGLE_CLIENT_ID": "env_client_id",
                    "GOOGLE_CLIENT_SECRET": "env_client_secret",
                },
            ),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            assert result.configured is True
            assert result.has_client_id is True
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_never_exposes_credentials(self):
        """Status response should never contain actual credential values (Issue #734)"""
        mock_config_service = MagicMock()
        mock_config_service.get_google_client_id.return_value = "secret_client_id_value"
        mock_config_service.get_google_client_secret.return_value = "super_secret_value"
        mock_user = MagicMock()

        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=mock_config_service,
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(mock_user)

            # Convert to dict to check all fields
            result_dict = result.model_dump()

            # Should not contain actual credential values
            for value in result_dict.values():
                if isinstance(value, str):
                    assert "secret_client_id_value" not in value
                    assert "super_secret_value" not in value


class TestAppCredentialsCardIsAdminOnly:
    """PM's ruling 2026-10-01 (test card, Test 5): the Google OAuth APP is
    deployment plumbing. A non-admin user must never be shown the
    app-credential form — the page hides it unless ``can_configure``. The
    write path keeps its own fail-closed admin gate (#357); this is the
    read side that stops testers from hitting a Save that refuses."""

    def _configured_service(self):
        svc = MagicMock()
        svc.get_google_client_id.return_value = "123.apps.googleusercontent.com"
        svc.get_google_client_secret.return_value = "GOCSPX-x"
        return svc

    @pytest.mark.asyncio
    async def test_non_admin_cannot_configure(self):
        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=self._configured_service(),
            ),
            patch("services.auth.auth_middleware._user_is_admin", AsyncMock(return_value=False)),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(MagicMock(user_id="u1"))
        assert result.configured is True
        assert result.can_configure is False

    @pytest.mark.asyncio
    async def test_admin_can_configure(self):
        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=self._configured_service(),
            ),
            patch("services.auth.auth_middleware._user_is_admin", AsyncMock(return_value=True)),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(MagicMock(user_id="u1"))
        assert result.can_configure is True

    @pytest.mark.asyncio
    async def test_admin_check_failure_hides_the_card(self):
        with (
            patch(
                "services.integrations.integration_config_service.IntegrationConfigService",
                return_value=self._configured_service(),
            ),
            patch(
                "services.auth.auth_middleware._user_is_admin",
                AsyncMock(side_effect=RuntimeError("db down")),
            ),
            patch.dict("os.environ", {}, clear=True),
        ):
            result = await get_calendar_app_credentials_status(MagicMock(user_id="u1"))
        assert result.can_configure is False

    def test_template_hides_the_card_by_default_and_carries_the_honest_note(self):
        html = open("templates/settings_calendar.html").read()
        assert 'id="app-config-card" hidden' in html
        assert 'id="app-not-configured-note"' in html
        assert "card.hidden = !data.can_configure" in html
