"""#1513: Integration Health showed GitHub "Not configured" while the user's
PAT sat verifiably in the keychain — the github branch of
_get_integration_config_status was env-only, unlike its notion/slack/calendar
siblings. With #1507 removing the restart-volatile env write, the user-scoped
keychain check is the ONLY correct source for PAT-connected users.

ADR-081 D1 (Arch 10-24 18:45): a user's GitHub status derives from the connector
resolver's own PAT legs, never from the deployment's env; the env (through the one
local-only "system" helper) counts only for a principal-less local call.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.integrations import _get_integration_config_status


def _keychain_with(token):
    kc = MagicMock()
    kc.get_api_key.return_value = token
    kc.aget_api_key = AsyncMock(side_effect=kc.get_api_key)  # #2101: the coroutine path
    # #2151 ISS-STATUS: config status reads with provenance (absent vs store failed).
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    def _read(provider, username=None):
        value = kc.get_api_key(provider, username)
        if value:
            return SecretRead(SecretProvenance.PRESENT, value=value)
        return SecretRead(SecretProvenance.VERIFIED_ABSENT)

    kc.aread_secret = AsyncMock(side_effect=_read)
    # ADR-081 D1: the resolver's keychain leg (read_user_token) is the sync read.
    kc.read_secret = MagicMock(side_effect=_read)
    return kc


def _no_system_token():
    """The local-only "system" helper reads the env and the host's "system" keychain row;
    pin it, so the result doesn't depend on the machine running the test."""
    from services.integrations.github.config_service import GitHubConfigService

    return patch.object(GitHubConfigService, "get_authentication_token", return_value=None)


class TestGitHubConfigStatusReadsKeychain:
    @pytest.mark.asyncio
    async def test_keychain_pat_reports_configured_without_env(self, monkeypatch):
        """The exact live failure: env wiped by restart, token in keychain →
        must be 'configured'. (Pre-fix this returned 'not_configured'.)"""
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_ACCESS_TOKEN", raising=False)
        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain_with("ghp_stored"),
        ) as kc_cls:
            status = await _get_integration_config_status("github", user_id="user-1")
        assert status == "configured"
        # and it asked for the USER-SCOPED key, the one the save route writes
        kc_cls.return_value.read_secret.assert_called_once_with("github_token", username="user-1")

    @pytest.mark.asyncio
    async def test_no_env_no_keychain_is_not_configured(self, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_ACCESS_TOKEN", raising=False)
        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain_with(None),
        ):
            status = await _get_integration_config_status("github", user_id="user-1")
        assert status == "not_configured"

    @pytest.mark.asyncio
    async def test_anonymous_caller_skips_keychain(self, monkeypatch):
        """No user_id → no user-scoped lookup to make (env-only path preserved)."""
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        monkeypatch.delenv("GITHUB_ACCESS_TOKEN", raising=False)
        with (
            patch("services.infrastructure.keychain_service.KeychainService") as kc_cls,
            _no_system_token(),
        ):
            status = await _get_integration_config_status("github", user_id=None)
        assert status == "not_configured"
        kc_cls.assert_not_called()

    @pytest.mark.asyncio
    async def test_the_env_token_does_not_connect_a_user(self, monkeypatch):
        """ADR-081 D1 (was "env still wins"): the deployment's token is not the user's
        connection, so a user with no PAT of their own is not configured."""
        monkeypatch.setenv("GITHUB_TOKEN", "fake-token-deployment")
        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain_with(None),
        ):
            status = await _get_integration_config_status("github", user_id="user-1")
        assert status == "not_configured"

    @pytest.mark.asyncio
    async def test_a_principal_less_local_call_reads_the_system_helper(self):
        """The env counts only through the one local-only helper, for no principal."""
        from services.integrations.github.config_service import GitHubConfigService

        with patch.object(
            GitHubConfigService, "get_authentication_token", return_value="fake-token-local"
        ) as helper:
            status = await _get_integration_config_status("github", user_id=None)
        assert status == "configured"
        helper.assert_called_once_with("system")
