"""#1809 — Slack inbound either binds the SENDER'S own LLM key or refuses honestly.

THE GAP (#1809, found while closing #1807): `SlackResponseHandler` constructs
`IntentService()` directly and dispatches inbound turns with NO key binding. Under the
old ContextVar default ("unbound → server key") every inbound Slack message ran on the
operator's key regardless of whose turn it was — the entry-point-scoped #1807 fix never
saw it, because Slack never calls the resolver. (#1481's inbound hold lowered the live
exposure, not the structural one.)

THE DESIGN (safe default, per the #1809 brief): the key an inbound Slack turn spends is
the SENDER'S — their Slack identity resolved to a Piper principal (#1466 mapping), then
that principal's stored Anthropic key. Nobody else's money. When that chain breaks —
unlinked sender, linked-but-keyless — nothing is bound, and the moment the turn actually
touches the LLM the inverted chokepoint raises; the handler converts that into an honest
in-channel reply (the #1466 link-deep-link decline, or CXO's "no key configured" copy)
instead of a silent spend or a silent None. Turns that never reach the LLM (template
responses: help, ping, status) still work for everyone — the refusal is lazy, at the
spend point, not a gate on the whole surface.

Driven through the REAL `handle_spatial_event` — the mocks stand only where external
systems stand (spatial adapter context lookup, Slack send, the classifier's answer, DB
session/key store), so the binding, propagation, refusal, and copy paths are all
production code.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.integrations.slack import link_copy
from services.integrations.slack.response_handler import SlackResponseHandler
from services.llm.request_key import (
    UnboundLLMKeyError,
    anthropic_client_for_request,
    get_request_api_key,
)
from services.shared_types import IntentCategory

STORED_SENDER_KEY = "sk-ant-api03-the-slack-senders-own-stored-key-1809"
SERVER_CLIENT = SimpleNamespace(name="THE-SERVERS-OWN-ANTHROPIC-CLIENT")


def _handler() -> SlackResponseHandler:
    handler = SlackResponseHandler(
        spatial_adapter=MagicMock(),
        intent_classifier=MagicMock(),
        slack_client=MagicMock(),
        intent_service=MagicMock(),
    )
    handler.slack_client.send_message = AsyncMock(return_value={"ok": True})
    return handler


def _spatial_event() -> SimpleNamespace:
    return SimpleNamespace(
        id=str(uuid.uuid4()),
        event_type="message_created",
        object_position=1,
        territory_position=1,
        room_position=1,
        path_position=1,
        actor_id="actor",
        significance_level="medium",
    )


def _slack_context(user_id: str, channel: str) -> dict:
    # Unique ts per call so the duplicate-event circuit breaker never trips across tests.
    return {
        "user_id": user_id,
        "workspace_id": f"T{uuid.uuid4().hex[:10].upper()}",
        "channel_id": channel,
        "content": "please summarize the current sprint",
        "ts": f"{uuid.uuid4().hex}.000100",
    }


def _query_intent(message: str = "please summarize the current sprint") -> Intent:
    # Non-EXECUTION → the emergency filter answers from a template, no LLM touch.
    return Intent(
        category=IntentCategory.QUERY,
        action="help",
        original_message=message,
        confidence=0.9,
    )


@contextlib.asynccontextmanager
async def _fake_session():
    yield object()


@contextlib.contextmanager
def _stored_key(value):
    """The sender's stored-key world, at the same seams the #1807 suites patch."""
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            lambda *a, **k: _fake_session(),
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            AsyncMock(return_value=value),
        ),
    ):
        yield


def _touch_the_llm(**kwargs):
    """A classifier stub that does what the real LLM leg does at the spend point:
    asks the REAL chokepoint for a client. Bound → returns (and we record the key);
    unbound → the production `UnboundLLMKeyError` — not a hand-raised stand-in."""
    client = anthropic_client_for_request(SERVER_CLIENT)
    _touch_the_llm.key_at_llm_time = get_request_api_key()
    _touch_the_llm.client = client
    return _query_intent()


class TestLinkedSenderWithKeyRunsOnTheirOwnKey:
    @pytest.mark.asyncio
    async def test_senders_stored_key_is_bound_for_the_whole_pipeline(self):
        """A linked sender (Piper-UUID passthrough, #1466) with a stored key: the
        pipeline runs with THEIR key bound — the LLM leg gets a fresh client keyed
        to it, never the server's client."""
        handler = _handler()
        piper_id = str(uuid.uuid4())
        context = _slack_context(piper_id, "C-1809-bound")
        handler._get_slack_context_from_spatial_event = AsyncMock(return_value=context)

        _touch_the_llm.key_at_llm_time = None
        _touch_the_llm.client = None
        handler.intent_classifier.classify = AsyncMock(side_effect=_touch_the_llm)

        with _stored_key(STORED_SENDER_KEY):
            result = await handler.handle_spatial_event(_spatial_event())

        assert _touch_the_llm.key_at_llm_time == STORED_SENDER_KEY
        assert _touch_the_llm.client is not SERVER_CLIENT
        assert getattr(_touch_the_llm.client, "api_key", None) == STORED_SENDER_KEY
        assert result is not None, "the turn completed and a reply went back to Slack"
        handler.slack_client.send_message.assert_awaited()

    @pytest.mark.asyncio
    async def test_the_binding_does_not_outlive_the_event(self):
        """No residue: after the event, the context is back to UNBOUND (refuse) —
        the next turn cannot ride this sender's key."""
        handler = _handler()
        context = _slack_context(str(uuid.uuid4()), "C-1809-residue")
        handler._get_slack_context_from_spatial_event = AsyncMock(return_value=context)
        handler.intent_classifier.classify = AsyncMock(return_value=_query_intent())

        with _stored_key(STORED_SENDER_KEY):
            await handler.handle_spatial_event(_spatial_event())

        assert get_request_api_key() is None
        with pytest.raises(UnboundLLMKeyError):
            anthropic_client_for_request(SERVER_CLIENT)


class TestKeylessTurnsRefuseHonestly:
    @pytest.mark.asyncio
    async def test_linked_but_keyless_sender_gets_the_no_key_copy_not_a_spend(self):
        """Linked sender, no stored key: nothing is bound, the LLM touch raises the
        production refusal, and the handler answers in-channel with CXO's honest
        "bring your own key" copy — the server's client is never handed out."""
        handler = _handler()
        piper_id = str(uuid.uuid4())
        context = _slack_context(piper_id, "C-1809-keyless")
        handler._get_slack_context_from_spatial_event = AsyncMock(return_value=context)
        handler.intent_classifier.classify = AsyncMock(side_effect=_touch_the_llm)

        with _stored_key(None):
            result = await handler.handle_spatial_event(_spatial_event())

        assert result is not None, "the refusal is a REPLY, not a silent None"
        sent_text = handler.slack_client.send_message.await_args.kwargs["text"]
        assert "key of your own" in sent_text
        assert "Settings" in sent_text  # actionable remediation, not just blame

    @pytest.mark.asyncio
    async def test_unlinked_sender_gets_the_link_decline_with_deep_link(self):
        """Unlinked sender (raw Slack id, no mapping): the honest answer is the
        #1466 link-your-account decline — their key may exist; Piper can't know
        whose turn this is until they link."""
        handler = _handler()
        su = f"U{uuid.uuid4().hex[:10].upper()}"
        context = _slack_context(su, "C-1809-unlinked")
        handler._get_slack_context_from_spatial_event = AsyncMock(return_value=context)
        handler.intent_classifier.classify = AsyncMock(side_effect=_touch_the_llm)

        with (
            _stored_key(None),
            patch(
                "services.auth.slack_link_service.resolve_slack_principal",
                AsyncMock(return_value=None),
            ),
        ):
            result = await handler.handle_spatial_event(_spatial_event())

        assert result is not None
        sent_text = handler.slack_client.send_message.await_args.kwargs["text"]
        assert link_copy.UNLINKED_DECLINE_PROSE in sent_text
        assert f"slack_user_id={su}" in sent_text  # the CXO deep link, not just prose

    @pytest.mark.asyncio
    async def test_a_template_turn_still_works_for_a_keyless_sender(self):
        """The refusal is LAZY — at the spend point, not the door. A turn the
        pipeline answers from templates (non-EXECUTION emergency filter) completes
        for an unlinked, keyless sender exactly as before #1809."""
        handler = _handler()
        su = f"U{uuid.uuid4().hex[:10].upper()}"
        context = _slack_context(su, "C-1809-template")
        handler._get_slack_context_from_spatial_event = AsyncMock(return_value=context)
        handler.intent_classifier.classify = AsyncMock(return_value=_query_intent())

        with (
            _stored_key(None),
            patch(
                "services.auth.slack_link_service.resolve_slack_principal",
                AsyncMock(return_value=None),
            ),
        ):
            result = await handler.handle_spatial_event(_spatial_event())

        assert result is not None
        sent_text = handler.slack_client.send_message.await_args.kwargs["text"]
        assert link_copy.UNLINKED_DECLINE_PROSE not in sent_text
        assert "key of your own" not in sent_text
