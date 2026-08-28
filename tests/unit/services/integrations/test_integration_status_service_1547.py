"""#1547: the canonical IntegrationStatusService — ONE status source for
"is integration X connected for user U?".

Root cause (status-truth audit 2026-08-09): all four real plugins hardcode
``is_configured() -> False`` (#784), so every registry-fed surface reported real
integrations never-connected while the Demo plugin (env-fed) was the only one that
could ever appear connected. The fix hoists the already-correct ``/health``
composition (web/api/routes/integrations.py — #1513 keychain reads, #1329
binding-first github, #1337 notion user-secret-store, #839 user-scoped calendar)
into ``services/integrations/integration_status_service.py`` so chat / floor /
standup / Radar read the same truth the Integration Health page reports.

Contract pinned here:
- ``get_status(user_id, integration_id)`` -> {configured, via, healthy, last_check}
- ``get_all(user_id)`` -> the known user-facing set ONLY (github/slack/calendar/
  notion) — demo is structurally excluded, not filtered downstream.
- github is binding-FIRST: a BOUND OAuth connector reports configured via
  "oauth_binding" regardless of PAT/env state.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations import integration_status_service as iss_mod
from services.integrations.integration_status_service import (
    KNOWN_INTEGRATIONS,
    IntegrationStatusService,
)


def _clear_integration_env(monkeypatch):
    for var in (
        "GITHUB_TOKEN",
        "GITHUB_ACCESS_TOKEN",
        "NOTION_API_TOKEN",
        "NOTION_API_KEY",
        "SLACK_BOT_TOKEN",
        "GOOGLE_CALENDAR_CREDENTIALS",
        "MCP_ENABLED",
    ):
        monkeypatch.delenv(var, raising=False)


def _keychain_with(token):
    kc = MagicMock()
    kc.get_api_key.return_value = token
    return kc


@pytest.fixture
def service():
    return IntegrationStatusService()


class TestKnownSet:
    def test_known_set_is_the_four_user_facing_integrations(self):
        assert set(KNOWN_INTEGRATIONS) == {"github", "slack", "calendar", "notion"}

    @pytest.mark.asyncio
    async def test_demo_is_structurally_excluded(self, service):
        """Demo is not a user-facing integration — asking for it is an error,
        and get_all never enumerates it (the #1534 Demo leak, fixed at the source)."""
        with pytest.raises(ValueError):
            await service.get_status("u1", "demo")

    @pytest.mark.asyncio
    async def test_get_all_covers_exactly_the_known_set(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        with (
            patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=False)),
            patch.object(
                iss_mod,
                "get_config_status",
                new=AsyncMock(return_value=("not_configured", None)),
            ),
        ):
            statuses = await service.get_all("u1")
        assert set(statuses.keys()) == set(KNOWN_INTEGRATIONS)
        assert "demo" not in statuses


class TestGitHubBindingFirst:
    @pytest.mark.asyncio
    async def test_bound_oauth_connector_is_configured_via_oauth_binding(
        self, service, monkeypatch
    ):
        """#1329 hoisted: BOUND connector → configured+healthy, no PAT needed."""
        _clear_integration_env(monkeypatch)
        with patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=True)):
            status = await service.get_status("u1", "github")
        assert status["configured"] is True
        assert status["via"] == "oauth_binding"
        assert status["healthy"] is True

    @pytest.mark.asyncio
    async def test_keychain_pat_is_configured_via_keychain(self, service, monkeypatch):
        """#1513 hoisted: user-scoped keychain PAT, no env, no binding."""
        _clear_integration_env(monkeypatch)
        with (
            patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=False)),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=_keychain_with("ghp_stored"),
            ) as kc_cls,
        ):
            status = await service.get_status("u1", "github")
        assert status["configured"] is True
        assert status["via"] == "keychain"
        kc_cls.return_value.get_api_key.assert_called_once_with("github_token", username="u1")

    @pytest.mark.asyncio
    async def test_env_token_is_configured_via_env(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_env")
        with patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=False)):
            status = await service.get_status("u1", "github")
        assert status["configured"] is True
        assert status["via"] == "env"

    @pytest.mark.asyncio
    async def test_nothing_anywhere_is_not_configured(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        with (
            patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=False)),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=_keychain_with(None),
            ),
        ):
            status = await service.get_status("u1", "github")
        assert status == {
            "configured": False,
            "via": None,
            "healthy": None,
            "last_check": None,
        }


class TestNonGitHubVias:
    @pytest.mark.asyncio
    async def test_notion_env_via(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        monkeypatch.setenv("NOTION_API_TOKEN", "secret_x")
        status = await service.get_status("u1", "notion")
        assert status["configured"] is True
        assert status["via"] == "env"

    @pytest.mark.asyncio
    async def test_slack_keychain_via(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain_with("xoxb-1"),
        ) as kc_cls:
            status = await service.get_status("u1", "slack")
        assert status["configured"] is True
        assert status["via"] == "keychain"
        kc_cls.return_value.get_api_key.assert_called_once_with("slack_bot", username="u1")

    @pytest.mark.asyncio
    async def test_calendar_user_scoped_keychain_via(self, service, monkeypatch):
        """#839 hoisted: calendar reads the user-scoped keychain key."""
        _clear_integration_env(monkeypatch)
        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=_keychain_with("refresh-tok"),
        ) as kc_cls:
            status = await service.get_status("u1", "calendar")
        assert status["configured"] is True
        assert status["via"] == "keychain"
        kc_cls.return_value.get_api_key.assert_called_once_with("google_calendar_u1")


class TestHealthComposition:
    @pytest.mark.asyncio
    async def test_configured_with_cached_healthy_check(self, service, monkeypatch):
        """IntegrationHealthMonitor cached results ride along (hoisted from /health)."""
        _clear_integration_env(monkeypatch)
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-env")

        from services.health.integration_health_monitor import (
            ComponentStatus,
            IntegrationHealthMonitor,
        )

        monitor = IntegrationHealthMonitor()
        monitor.register_component("slack", ComponentStatus.UNKNOWN)
        monitor.record_success("slack", 12.0)

        with patch.object(iss_mod, "get_health_monitor", return_value=monitor):
            status = await service.get_status("u1", "slack")
        assert status["configured"] is True
        assert status["healthy"] is True
        assert status["last_check"] is not None

    @pytest.mark.asyncio
    async def test_configured_never_tested_has_unknown_health(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-env")

        from services.health.integration_health_monitor import (
            ComponentStatus,
            IntegrationHealthMonitor,
        )

        monitor = IntegrationHealthMonitor()
        monitor.register_component("slack", ComponentStatus.UNKNOWN)

        with patch.object(iss_mod, "get_health_monitor", return_value=monitor):
            status = await service.get_status("u1", "slack")
        assert status["configured"] is True
        assert status["healthy"] is None
        assert status["last_check"] is None

    @pytest.mark.asyncio
    async def test_is_configured_convenience(self, service, monkeypatch):
        _clear_integration_env(monkeypatch)
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_env")
        with patch.object(iss_mod, "github_oauth_bound", new=AsyncMock(return_value=False)):
            assert await service.is_configured("u1", "github") is True
