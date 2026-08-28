"""#1513: Integration Health showed GitHub "Not configured" while the user's
PAT sat verifiably in the keychain — the github branch of
_get_integration_config_status was env-only, unlike its notion/slack/calendar
siblings. With #1507 removing the restart-volatile env write, the user-scoped
keychain check is the ONLY correct source for PAT-connected users.
"""

from unittest.mock import MagicMock, patch

import pytest

from web.api.routes.integrations import _get_integration_config_status


def _keychain_with(token):
    kc = MagicMock()
    kc.get_api_key.return_value = token
    return kc


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
        kc_cls.return_value.get_api_key.assert_called_once_with("github_token", username="user-1")

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
        with patch("services.infrastructure.keychain_service.KeychainService") as kc_cls:
            status = await _get_integration_config_status("github", user_id=None)
        assert status == "not_configured"
        kc_cls.assert_not_called()

    @pytest.mark.asyncio
    async def test_env_still_wins_when_present(self, monkeypatch):
        """System-floor deployments configured via env stay recognized."""
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_env")
        status = await _get_integration_config_status("github", user_id="user-1")
        assert status == "configured"
