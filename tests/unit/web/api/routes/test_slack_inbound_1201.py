"""#1201 — Slack inbound app-token save route + inbound-status endpoint.

save_slack_app_token: validate xapp- → store global keychain slack_app_token →
start-on-save (restart the Socket Mode runner at runtime) → return inbound state.
get_slack_inbound_status: compose the 3-state view (not_enabled / connecting / listening).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from web.api.routes.settings_integrations import (
    SlackAppTokenRequest,
    get_slack_inbound_status,
    save_slack_app_token,
)

pytestmark = pytest.mark.asyncio

_USER = MagicMock(sub="owner-1")



@pytest.fixture(autouse=True)
def _inbound_enabled(monkeypatch):
    """#1484 (2026-08-04): these tests exercise the ENABLED pathway — the
    deployment gate (default OFF) now fronts it; the gate's own contract is
    pinned in test_inbound_deployment_gate_1484.py."""
    monkeypatch.setenv("PIPER_SLACK_INBOUND_ENABLED", "true")


def _request(runner=None):
    return SimpleNamespace(app=SimpleNamespace(state=SimpleNamespace(slack_socket_runner=runner)))


# ---- save_slack_app_token ----

async def test_rejects_non_xapp_token():
    with pytest.raises(HTTPException) as exc:
        await save_slack_app_token(
            SlackAppTokenRequest(app_token="xoxb-not-an-app-token"), _request(), current_user=_USER
        )
    assert exc.value.status_code == 400
    assert "xapp-" in exc.value.detail


async def test_saves_global_key_and_starts_runner():
    keychain = MagicMock()
    connected_runner = MagicMock(is_connected=True)
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch(
            "services.integrations.slack.socket_mode_runner.restart_socket_runner",
            AsyncMock(return_value=connected_runner),
        ),
    ):
        resp = await save_slack_app_token(
            SlackAppTokenRequest(app_token="xapp-1-ABC"), _request(), current_user=_USER
        )
    # stored GLOBAL (no username kwarg) under slack_app_token — matches the runner's read
    keychain.store_api_key.assert_called_once_with("slack_app_token", "xapp-1-ABC")
    assert resp.connected is True
    assert resp.state == "listening"


async def test_save_reports_connecting_when_runner_not_yet_connected():
    keychain = MagicMock()
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch(
            "services.integrations.slack.socket_mode_runner.restart_socket_runner",
            AsyncMock(return_value=MagicMock(is_connected=False)),
        ),
    ):
        resp = await save_slack_app_token(
            SlackAppTokenRequest(app_token="xapp-1-ABC"), _request(), current_user=_USER
        )
    assert resp.connected is False
    assert resp.state == "connecting"


# ---- get_slack_inbound_status: 3-state ----

async def test_status_not_enabled_without_token():
    keychain = MagicMock()
    keychain.get_api_key.return_value = None
    with (
        patch.dict("os.environ", {"PIPER_SLACK_INBOUND_ENABLED": "true"}, clear=True),  # 1484 gate open; these test the enabled pathway
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
    ):
        resp = await get_slack_inbound_status(_request(), current_user=_USER)
    assert resp.connected is False
    assert resp.state == "not_enabled"


async def test_status_listening_when_token_and_runner_connected():
    keychain = MagicMock()
    keychain.get_api_key.return_value = "xapp-1-ABC"
    with (
        patch.dict("os.environ", {"PIPER_SLACK_INBOUND_ENABLED": "true"}, clear=True),  # 1484 gate open; these test the enabled pathway
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
    ):
        resp = await get_slack_inbound_status(
            _request(runner=MagicMock(is_connected=True)), current_user=_USER
        )
    assert resp.connected is True
    assert resp.state == "listening"


async def test_status_connecting_when_token_but_runner_absent_or_down():
    keychain = MagicMock()
    keychain.get_api_key.return_value = "xapp-1-ABC"
    with (
        patch.dict("os.environ", {"PIPER_SLACK_INBOUND_ENABLED": "true"}, clear=True),  # 1484 gate open; these test the enabled pathway
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
    ):
        # runner absent
        r1 = await get_slack_inbound_status(_request(runner=None), current_user=_USER)
        # runner present but not connected
        r2 = await get_slack_inbound_status(
            _request(runner=MagicMock(is_connected=False)), current_user=_USER
        )
    assert (r1.connected, r1.state) == (False, "connecting")
    assert (r2.connected, r2.state) == (False, "connecting")
