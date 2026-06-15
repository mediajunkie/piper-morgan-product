"""#1228 — Slack "thinking" placeholder on the inbound reply seam.

The runner posts a "…thinking…" placeholder before processing so the user can
tell normal LLM latency from a frozen connection, then updates it in place with
the real reply (or an honest error). These tests pin that behavior at the
``_handle_event`` seam with a mocked Slack web client.
"""
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from services.integrations.slack.socket_mode_runner import SlackSocketModeRunner

THINKING = "_…thinking…_"
DM_EVENT = {"type": "message", "channel_type": "im", "channel": "D1", "text": "hi", "ts": "100.0"}


def _runner(process_return=None, process_raises=None):
    intent = MagicMock()
    if process_raises is not None:
        intent.process_intent = AsyncMock(side_effect=process_raises)
    else:
        intent.process_intent = AsyncMock(return_value=process_return)
    r = SlackSocketModeRunner(
        intent_service=intent, app_token="xapp", bot_token="xoxb", bound_user_id="u1"
    )
    r._web = AsyncMock()
    return r


async def test_thinking_placeholder_then_update_happy_path():
    r = _runner(process_return=SimpleNamespace(message="Hello there"))
    r._web.chat_postMessage = AsyncMock(return_value={"ts": "999.0"})
    r._web.chat_update = AsyncMock()

    await r._handle_event(dict(DM_EVENT))

    # placeholder posted first…
    r._web.chat_postMessage.assert_awaited_once()
    assert r._web.chat_postMessage.call_args.kwargs["text"] == THINKING
    # …then replaced in place with the real reply (no second post)
    r._web.chat_update.assert_awaited_once()
    assert r._web.chat_update.call_args.kwargs["ts"] == "999.0"
    assert r._web.chat_update.call_args.kwargs["text"] == "Hello there"


async def test_processing_error_updates_placeholder_not_stuck():
    r = _runner(process_raises=RuntimeError("boom"))
    r._web.chat_postMessage = AsyncMock(return_value={"ts": "999.0"})
    r._web.chat_update = AsyncMock()

    await r._handle_event(dict(DM_EVENT))

    # placeholder is replaced with an honest error — never left at "…thinking…"
    r._web.chat_update.assert_awaited_once()
    assert "went wrong" in r._web.chat_update.call_args.kwargs["text"].lower()


async def test_update_failure_falls_back_to_fresh_post():
    r = _runner(process_return=SimpleNamespace(message="Hi"))
    r._web.chat_postMessage = AsyncMock(return_value={"ts": "999.0"})
    r._web.chat_update = AsyncMock(side_effect=Exception("cant update"))

    await r._handle_event(dict(DM_EVENT))

    # placeholder + fallback = 2 posts; the fallback carries the reply
    assert r._web.chat_postMessage.await_count == 2
    assert r._web.chat_postMessage.call_args.kwargs["text"] == "Hi"


async def test_placeholder_post_failure_still_replies():
    r = _runner(process_return=SimpleNamespace(message="Hi"))
    # first postMessage (placeholder) fails; second (fallback reply) succeeds
    r._web.chat_postMessage = AsyncMock(side_effect=[Exception("no placeholder"), {"ts": "x"}])
    r._web.chat_update = AsyncMock()

    await r._handle_event(dict(DM_EVENT))

    # no placeholder ts → no update attempted; reply still posts fresh
    r._web.chat_update.assert_not_awaited()
    assert r._web.chat_postMessage.await_count == 2
    assert r._web.chat_postMessage.call_args.kwargs["text"] == "Hi"
