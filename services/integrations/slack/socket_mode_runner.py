"""Slack Socket Mode runner (#1129 — inbound rebuild, PM path C).

History: inbound (Slack → Piper) worked Jul–Sep 2025 via an HTTP webhook; the
mount was removed in the Oct 2025 CORE-GREAT-2D refactor and inbound has been
broken since. Rebuilt here on Socket Mode (no public URL needed): the app-level
token (`xapp-…`, keychain `slack_app_token`) opens a websocket; `message.im` +
`app_mention` events route into the intent service; replies post via the
existing user-scoped bot token (`slack_bot`, ADR-058).

MVP user-binding: single-tenant — events are processed AS the Piper user who
holds the stored `slack_bot` token (resolved at startup by probing active
users). Real Slack-user→Piper-user mapping is follow-on work (#1110-adjacent);
the setup UX for all of this is #1201.
"""

from __future__ import annotations

import asyncio
import re
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)

_MENTION_RE = re.compile(r"<@[A-Z0-9]+>")


async def _resolve_bound_user() -> Optional[str]:
    """Find the Piper user whose keychain holds the Slack bot token (MVP single-tenant)."""
    try:
        from sqlalchemy import text

        from services.database.session_factory import AsyncSessionFactory
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            rows = await session.execute(text("SELECT id FROM users ORDER BY created_at"))
            for (uid,) in rows.fetchall():
                if keychain.get_api_key("slack_bot", username=str(uid)):
                    return str(uid)
    except Exception as e:
        logger.warning("slack_socket_bound_user_resolution_failed", error=str(e))
    return None


class SlackSocketModeRunner:
    """Owns the Socket Mode connection + event→intent→reply loop."""

    def __init__(self, intent_service: Any, app_token: str, bot_token: str, bound_user_id: str):
        self.intent_service = intent_service
        self.app_token = app_token
        self.bot_token = bot_token
        self.bound_user_id = bound_user_id
        self._client = None
        self._web = None

    async def start(self) -> None:
        from slack_sdk.socket_mode.aiohttp import SocketModeClient
        from slack_sdk.socket_mode.request import SocketModeRequest
        from slack_sdk.socket_mode.response import SocketModeResponse
        from slack_sdk.web.async_client import AsyncWebClient

        self._web = AsyncWebClient(token=self.bot_token)
        self._client = SocketModeClient(app_token=self.app_token, web_client=self._web)

        async def _listener(client, req: "SocketModeRequest") -> None:
            # Always ack fast — Slack retries unacked envelopes.
            await client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id)
            )
            if req.type != "events_api":
                return
            event = (req.payload or {}).get("event") or {}
            # Fire-and-forget so slow LLM turns don't block the socket.
            asyncio.create_task(self._handle_event(event))

        self._client.socket_mode_request_listeners.append(_listener)
        await self._client.connect()
        logger.info("slack_socket_mode_connected", bound_user=self.bound_user_id)

    async def _handle_event(self, event: dict) -> None:
        try:
            etype = event.get("type")
            # Ignore our own / other bots' messages and message edits etc.
            if event.get("bot_id") or event.get("subtype"):
                return
            is_dm = etype == "message" and event.get("channel_type") == "im"
            is_mention = etype == "app_mention"
            if not (is_dm or is_mention):
                return
            text = (event.get("text") or "").strip()
            if is_mention:
                text = _MENTION_RE.sub("", text).strip()
            if not text:
                return
            channel = event.get("channel")
            logger.info(
                "slack_inbound_event", etype=etype, channel=channel, chars=len(text)
            )
            # #1228: post a "thinking" placeholder first so the user can tell
            # normal LLM latency from a frozen connection, then update it in
            # place with the real reply (or an honest error) when done.
            thread_ts = event.get("thread_ts")
            placeholder_ts = None
            try:
                placeholder = await self._web.chat_postMessage(
                    channel=channel,
                    text="_…thinking…_",
                    thread_ts=thread_ts,
                )
                placeholder_ts = placeholder.get("ts") if placeholder else None
            except Exception as e:
                logger.warning("slack_thinking_placeholder_failed", error=str(e))

            try:
                result = await self.intent_service.process_intent(
                    message=text,
                    session_id=f"slack-{channel}",
                    user_id=self.bound_user_id,
                )
                reply = getattr(result, "message", None) or (
                    result.get("message") if isinstance(result, dict) else None
                )
                if not reply:
                    reply = "I heard you, but couldn't form a response — try me again?"
            except Exception:
                logger.error("slack_intent_processing_failed", channel=channel, exc_info=True)
                reply = "Something went wrong on my end handling that — try me again?"

            await self._post_or_update(channel, placeholder_ts, reply[:4000], thread_ts)
        except Exception as e:
            logger.error("slack_inbound_handling_failed", error=str(e), exc_info=True)

    async def _post_or_update(
        self, channel: str, ts: Optional[str], text: str, thread_ts: Optional[str]
    ) -> None:
        """Replace the #1228 thinking placeholder with the final text in place;
        fall back to a fresh post if there's no placeholder or the update fails."""
        if ts:
            try:
                await self._web.chat_update(channel=channel, ts=ts, text=text)
                return
            except Exception as e:
                logger.warning("slack_chat_update_failed", error=str(e))
        await self._web.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)

    async def stop(self) -> None:
        try:
            if self._client:
                await self._client.disconnect()
                await self._client.close()
        except Exception:
            pass


async def build_runner(intent_service: Any) -> Optional[SlackSocketModeRunner]:
    """Construct the runner if (and only if) inbound is fully configured.

    Honest absence: missing app token / bot token / bound user → None (the
    server runs without inbound; status surfacing is #1201's lane).
    """
    import os

    from services.infrastructure.keychain_service import KeychainService

    app_token = os.getenv("SLACK_APP_TOKEN") or KeychainService().get_api_key("slack_app_token")
    if not app_token:
        logger.info("slack_socket_mode_skipped", reason="no app-level token")
        return None
    bound_user = await _resolve_bound_user()
    if not bound_user:
        logger.info("slack_socket_mode_skipped", reason="no user with stored slack_bot token")
        return None
    bot_token = KeychainService().get_api_key("slack_bot", username=bound_user)
    if not bot_token:
        logger.info("slack_socket_mode_skipped", reason="bot token unreadable")
        return None
    return SlackSocketModeRunner(
        intent_service=intent_service,
        app_token=app_token,
        bot_token=bot_token,
        bound_user_id=bound_user,
    )
