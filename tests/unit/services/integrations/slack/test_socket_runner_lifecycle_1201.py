"""#1201 — Socket Mode runner connection-state + runtime (re)start lifecycle.

The inbound-status surface needs (a) the runner to report whether its websocket is
actually open, and (b) a way to start the runner at RUNTIME after a user pastes the
app-level token (boot starts it once; a token entered later must take effect without
an app restart). These are the backend foundation for the status endpoint + the
start-on-save flow.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack import socket_mode_runner as smr
from services.integrations.slack.socket_mode_runner import (
    SlackSocketModeRunner,
    restart_socket_runner,
)

pytestmark = pytest.mark.asyncio


def _runner():
    return SlackSocketModeRunner(
        intent_service=MagicMock(), app_token="xapp-1-x", bot_token="xoxb-b", bound_user_id="u1"
    )


async def test_is_connected_false_on_init():
    assert _runner().is_connected is False


async def test_start_sets_connected_then_stop_clears():
    r = _runner()
    fake_client = MagicMock()
    fake_client.socket_mode_request_listeners = []
    fake_client.connect = AsyncMock()
    fake_client.disconnect = AsyncMock()
    fake_client.close = AsyncMock()
    with (
        patch("slack_sdk.socket_mode.aiohttp.SocketModeClient", return_value=fake_client),
        patch("slack_sdk.web.async_client.AsyncWebClient", return_value=MagicMock()),
    ):
        await r.start()
        assert r.is_connected is True
        fake_client.connect.assert_awaited_once()
        await r.stop()
        assert r.is_connected is False


# ---- restart_socket_runner (runtime lifecycle on app.state) ----

def _app(intent_service=object(), existing=None):
    return SimpleNamespace(state=SimpleNamespace(intent_service=intent_service, slack_socket_runner=existing))


async def test_restart_builds_starts_and_stores():
    app = _app()
    new_runner = MagicMock()
    new_runner.start = AsyncMock()
    with patch.object(smr, "build_runner", AsyncMock(return_value=new_runner)):
        got = await restart_socket_runner(app)
    assert got is new_runner
    assert app.state.slack_socket_runner is new_runner
    new_runner.start.assert_awaited_once()


async def test_restart_stops_existing_first():
    existing = MagicMock(); existing.stop = AsyncMock()
    app = _app(existing=existing)
    new_runner = MagicMock(); new_runner.start = AsyncMock()
    with patch.object(smr, "build_runner", AsyncMock(return_value=new_runner)):
        await restart_socket_runner(app)
    existing.stop.assert_awaited_once()
    assert app.state.slack_socket_runner is new_runner


async def test_restart_none_when_not_configured_clears_runner():
    existing = MagicMock(); existing.stop = AsyncMock()
    app = _app(existing=existing)
    with patch.object(smr, "build_runner", AsyncMock(return_value=None)):
        got = await restart_socket_runner(app)
    assert got is None
    assert app.state.slack_socket_runner is None  # cleared


async def test_restart_none_when_no_intent_service():
    app = _app(intent_service=None)
    with patch.object(smr, "build_runner", AsyncMock()) as bld:
        got = await restart_socket_runner(app)
    assert got is None
    bld.assert_not_awaited()  # doesn't even try to build without intent_service


async def test_restart_keeps_runner_on_start_failure_for_connecting_state():
    app = _app()
    flaky = MagicMock(); flaky.start = AsyncMock(side_effect=RuntimeError("connect boom"))
    with patch.object(smr, "build_runner", AsyncMock(return_value=flaky)):
        got = await restart_socket_runner(app)
    # runner is kept (not connected) so status can show 'connecting/unavailable'
    assert got is flaky
    assert app.state.slack_socket_runner is flaky
