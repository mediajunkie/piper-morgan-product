"""#2172 (Arch 2026-10-25, ADR-080 / #2151): Disconnect says "disconnected" only when
every saved copy is verifiably gone.

Each clear is attempted; each copy is then read back with provenance. A copy still
there, or a read-back that failed, is ``remaining`` and the route answers with the
incomplete line (503), never ``success: true``. A provider-side revoke failure alone is
not remaining: Piper holds no copy once the local clears verify.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.connectors.disconnect import DisconnectResult, disconnect_connector
from services.infrastructure.keychain_service import SecretProvenance, SecretRead
from services.mcp.consumer.connector import DegradationReason

pytestmark = pytest.mark.asyncio

_U = "user-2172"
_ABSENT = SecretRead(SecretProvenance.VERIFIED_ABSENT)
_PRESENT = SecretRead(SecretProvenance.PRESENT, value="fake-token-2172")
_FAILED = SecretRead(SecretProvenance.STORE_FAILED, error="store down")


def _keychain(reads=None):
    """A keychain double: async delete/read, read-backs absent unless ``reads`` says."""
    reads = reads or {}
    kc = MagicMock()
    kc.adelete_api_key = AsyncMock(return_value=True)
    kc.aget_api_key = AsyncMock(return_value=None)
    kc.aread_secret = AsyncMock(
        side_effect=lambda provider, username=None: reads.get(provider, _ABSENT)
    )
    return kc


class _Scope:
    def __init__(self, session):
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, *exc):
        return False


async def _github(keychain, *, resolved, pat_at_rest=None, binding_raises=False):
    binding_repo = MagicMock()
    binding_repo.set_status = AsyncMock(side_effect=RuntimeError("db") if binding_raises else None)
    grant_store = MagicMock()
    grant_store.delete = AsyncMock()
    factory = MagicMock()
    factory.session_scope = MagicMock(side_effect=lambda: _Scope(MagicMock()))
    resolver = (
        AsyncMock(side_effect=resolved)
        if isinstance(resolved, Exception)
        else AsyncMock(return_value=resolved)
    )
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch("services.integrations.github.config_service.GitHubConfigService"),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
        patch(
            "services.connectors.binding_repository.ConnectorBindingRepository",
            return_value=binding_repo,
        ),
        patch(
            "services.mcp.consumer.connector_grant_store.ConnectorGrantStore",
            return_value=grant_store,
        ),
        patch(
            "services.connectors.github_pat_store.delete_user_pat_at_rest",
            pat_at_rest or AsyncMock(),
        ),
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            resolver,
        ),
    ):
        result = await disconnect_connector(_U, "github")
    return result, resolver


_GONE = SimpleNamespace(reason=DegradationReason.CONNECT_REQUIRED)


class TestGitHub:
    async def test_every_copy_gone_is_cleared(self):
        result, resolver = await _github(_keychain(), resolved=_GONE)
        assert isinstance(result, DisconnectResult)
        assert result.cleared and result.remaining == ()
        resolver.assert_awaited_once_with(_U)

    async def test_failed_at_rest_delete_is_remaining_and_the_rest_still_run(self):
        kc = _keychain()
        result, _ = await _github(
            kc, resolved=_GONE, pat_at_rest=AsyncMock(side_effect=RuntimeError("db down"))
        )
        assert not result.cleared
        assert "pat_at_rest" in result.remaining
        kc.adelete_api_key.assert_any_await("github_token", _U)
        kc.adelete_api_key.assert_any_await("github", _U)

    async def test_failed_binding_clear_is_remaining(self):
        result, _ = await _github(_keychain(), resolved=_GONE, binding_raises=True)
        assert "oauth_binding_and_grant" in result.remaining

    async def test_keychain_copy_still_present_is_remaining(self):
        result, _ = await _github(_keychain({"github_token": _PRESENT}), resolved=_GONE)
        assert result.remaining == ("keychain_pat",)

    async def test_keychain_read_back_that_failed_is_not_gone(self):
        result, _ = await _github(_keychain({"github": _FAILED}), resolved=_GONE)
        assert result.remaining == ("keychain_pat_key_service",)

    async def test_the_grants_keychain_copy_is_read_back(self):
        kc = _keychain({"github_mcp_oauth": _PRESENT})
        result, _ = await _github(kc, resolved=_GONE)
        assert result.remaining == ("oauth_grant_keychain",)
        kc.adelete_api_key.assert_any_await("github_mcp_oauth", _U)
        kc.aread_secret.assert_any_await("github_mcp_oauth", _U)

    async def test_the_grants_keychain_read_back_that_failed_is_not_gone(self):
        result, _ = await _github(_keychain({"github_mcp_oauth": _FAILED}), resolved=_GONE)
        assert result.remaining == ("oauth_grant_keychain",)

    async def test_resolver_still_serving_a_leg_is_remaining(self):
        still = SimpleNamespace(leg="pat", token="fake-token-2172")
        result, _ = await _github(_keychain(), resolved=still)
        assert result.remaining == ("credential_still_resolves:pat",)

    async def test_resolver_store_failure_is_unverified_not_gone(self):
        unreachable = SimpleNamespace(reason=DegradationReason.UNREACHABLE)
        result, _ = await _github(_keychain(), resolved=unreachable)
        assert result.remaining == ("credential_unverified",)

    async def test_resolver_raising_is_unverified_not_gone(self):
        result, _ = await _github(_keychain(), resolved=RuntimeError("binding read failed"))
        assert result.remaining == ("credential_unverified",)


class TestSlackCalendarNotion:
    async def _slack(self, keychain, revoke=None):
        oauth = MagicMock()
        oauth.revoke_workspace_access = revoke or AsyncMock(return_value=True)
        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService", return_value=keychain
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler", return_value=oauth
            ),
        ):
            return await disconnect_connector(_U, "slack")

    async def test_slack_both_tokens_gone_is_cleared(self):
        kc = _keychain()
        assert (await self._slack(kc)).cleared
        kc.adelete_api_key.assert_any_await("slack_bot", _U)
        kc.adelete_api_key.assert_any_await("slack_user", _U)

    async def test_slack_a_token_still_present_is_remaining(self):
        result = await self._slack(_keychain({"slack_user": _PRESENT}))
        assert result.remaining == ("slack_user",)

    async def test_slack_failed_read_back_is_remaining(self):
        result = await self._slack(_keychain({"slack_bot": _FAILED}))
        assert result.remaining == ("slack_bot",)

    async def test_slack_revoke_raising_alone_is_not_remaining_but_is_reported(self):
        result = await self._slack(
            _keychain(), revoke=AsyncMock(side_effect=RuntimeError("slack api down"))
        )
        assert result.cleared
        assert result.provider_revoke_failed

    async def test_slack_revoke_returning_false_is_reported(self):
        result = await self._slack(_keychain(), revoke=AsyncMock(return_value=False))
        assert result.cleared and result.provider_revoke_failed

    async def test_slack_revoked_is_not_reported(self):
        result = await self._slack(_keychain())
        assert not result.provider_revoke_failed

    async def test_calendar_revoke_false_is_reported_not_remaining(self):
        kc = _keychain()
        kc.aget_api_key = AsyncMock(return_value="fake-token-refresh")
        handler = MagicMock()
        handler.revoke_token = AsyncMock(return_value=False)
        with (
            patch("services.infrastructure.keychain_service.KeychainService", return_value=kc),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=handler,
            ),
        ):
            result = await disconnect_connector(_U, "calendar")
        assert result.cleared and result.provider_revoke_failed

    async def test_calendar_with_no_stored_token_attempts_no_revoke_and_reports_none(self):
        kc = _keychain()
        with patch("services.infrastructure.keychain_service.KeychainService", return_value=kc):
            result = await disconnect_connector(_U, "calendar")
        assert result.cleared and not result.provider_revoke_failed

    async def test_calendar_failed_read_back_is_remaining(self):
        kc = _keychain({f"google_calendar_{_U}": _FAILED})
        with patch("services.infrastructure.keychain_service.KeychainService", return_value=kc):
            result = await disconnect_connector(_U, "calendar")
        assert result.remaining == ("calendar_refresh_token",)
        kc.adelete_api_key.assert_awaited_once_with(f"google_calendar_{_U}", None)

    async def test_calendar_gone_is_cleared(self):
        kc = _keychain()
        with patch("services.infrastructure.keychain_service.KeychainService", return_value=kc):
            assert (await disconnect_connector(_U, "calendar")).cleared

    async def _notion(self, keychain, delete):
        svc = MagicMock()
        svc.delete_user_key = delete
        factory = MagicMock()
        factory.session_scope_fresh = MagicMock(side_effect=lambda: _Scope(MagicMock()))
        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService", return_value=keychain
            ),
            patch("services.database.session_factory.AsyncSessionFactory", factory),
            patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
        ):
            return await disconnect_connector(_U, "notion")

    async def test_notion_failed_store_delete_is_remaining(self):
        result = await self._notion(_keychain(), AsyncMock(side_effect=RuntimeError("db")))
        assert result.remaining == ("notion_user_key",)

    async def test_notion_keychain_copy_still_present_is_remaining(self):
        result = await self._notion(_keychain({"notion": _PRESENT}), AsyncMock(return_value=True))
        assert result.remaining == ("notion_keychain",)

    async def test_notion_gone_is_cleared(self):
        result = await self._notion(_keychain(), AsyncMock(return_value=False))
        assert result.cleared


class TestRoutesNeverClaimSuccessOnAPartialClear:
    @pytest.mark.parametrize(
        "route_name,connector,service",
        [
            ("disconnect_github", "github", "GitHub"),
            ("disconnect_slack", "slack", "Slack"),
            ("disconnect_calendar", "calendar", "Google Calendar"),
            ("disconnect_notion", "notion", "Notion"),
        ],
    )
    async def test_partial_clear_answers_503_with_the_line(self, route_name, connector, service):
        import json

        from web.api.routes import settings_integrations as routes

        partial = DisconnectResult(connector, ("some_copy",))
        user = SimpleNamespace(sub=_U)
        with patch(
            "services.connectors.disconnect.disconnect_connector", AsyncMock(return_value=partial)
        ):
            route = getattr(routes, route_name)
            resp = await route(current_user=user)
        assert resp.status_code == 503
        body = json.loads(resp.body)
        assert body["success"] is False
        assert body["detail"] == routes.DISCONNECT_INCOMPLETE_LINE.format(service=service)

    @pytest.mark.parametrize(
        "route_name,connector,service",
        [
            ("disconnect_github", "github", "GitHub"),
            ("disconnect_slack", "slack", "Slack"),
            ("disconnect_calendar", "calendar", "Google Calendar"),
            ("disconnect_notion", "notion", "Notion"),
        ],
    )
    async def test_full_clear_still_says_disconnected(self, route_name, connector, service):
        from web.api.routes import settings_integrations as routes

        with patch(
            "services.connectors.disconnect.disconnect_connector",
            AsyncMock(return_value=DisconnectResult(connector)),
        ):
            resp = await getattr(routes, route_name)(current_user=SimpleNamespace(sub=_U))
        assert resp["success"] is True
        assert resp["message"] == f"{service} disconnected"

    @pytest.mark.parametrize(
        "route_name,connector,service",
        [
            ("disconnect_slack", "slack", "Slack"),
            ("disconnect_calendar", "calendar", "Google Calendar"),
        ],
    )
    async def test_revoke_failed_is_success_with_cxos_sentence(
        self, route_name, connector, service
    ):
        from web.api.routes import settings_integrations as routes

        result = DisconnectResult(connector, (), provider_revoke_failed=True)
        with patch(
            "services.connectors.disconnect.disconnect_connector", AsyncMock(return_value=result)
        ):
            resp = await getattr(routes, route_name)(current_user=SimpleNamespace(sub=_U))
        assert resp["success"] is True
        assert resp["message"] == (
            f"{service} disconnected. Piper no longer holds your access. I couldn't revoke it "
            f"at {service}, so it stays valid there until you remove Piper in {service}'s "
            "settings."
        )


def test_the_partial_clear_line_is_cxos_words():
    """CXO 10-25 16:00, verbatim with the service filled in."""
    from web.api.routes.settings_integrations import DISCONNECT_INCOMPLETE_LINE

    assert DISCONNECT_INCOMPLETE_LINE.format(service="GitHub") == (
        "I couldn't fully disconnect GitHub: a saved copy of your access may still be "
        "stored, so Piper may still be able to use it. Try Disconnect again; if it keeps "
        "failing, tell us."
    )


@pytest.mark.parametrize("template", ["settings_slack.html", "settings_calendar.html"])
def test_the_success_toast_shows_the_servers_message(template):
    """The revoke sentence rides in ``message``; a hardcoded toast would drop it."""
    from pathlib import Path

    src = (Path(__file__).resolve().parents[4] / "templates" / template).read_text()
    assert "Toast.show('success', 'Disconnected', data.message ||" in src


class TestSlackRevokeReportsAPartialFailure:
    """``revoke_workspace_access`` is True only when every held token was revoked."""

    async def _run(self, outcomes):
        import httpx

        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        config = SimpleNamespace(
            api_base_url="https://slack.example",
            bot_token="fake-token-bot",
            user_token="fake-token-user",
            timeout_seconds=1,
        )
        cfg = MagicMock()
        cfg.get_config.return_value = config
        handler = SlackOAuthHandler.__new__(SlackOAuthHandler)
        handler.config_service = cfg
        handler.spatial_mapper = MagicMock()
        it = iter(outcomes)

        async def post(*a, **k):
            ok = next(it)
            if isinstance(ok, Exception):
                raise ok
            return SimpleNamespace(json=lambda: {"ok": ok})

        client = MagicMock()
        client.post = post
        client.__aenter__ = AsyncMock(return_value=client)
        client.__aexit__ = AsyncMock(return_value=False)
        with patch.object(httpx, "AsyncClient", return_value=client):
            return await handler.revoke_workspace_access(_U)

    async def test_both_revoked(self):
        assert await self._run([True, True]) is True

    async def test_one_refused_is_false(self):
        assert await self._run([True, False]) is False

    async def test_one_raising_is_false(self):
        assert await self._run([True, RuntimeError("connect timeout")]) is False
