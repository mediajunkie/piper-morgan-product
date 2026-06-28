"""
Tests for Issue #1032 INSIGHT-PUSH floor integration.

Step 3 + Step 4 of #1030+#1032 implementation:
- _maybe_append_push: skip for pull-mode, denial-mode, missing IDs, mute state,
  no payload; augment when payload returned; update cooldown state; fail-graceful
- respond() NL-detected session-mute trigger flips per-session state and
  short-circuits push for the rest of that session

PM dispositions (2026-05-31):
- R2 session-mute storage: per-session dict for MVP (process-local)
- R5 confidence cuts already covered in test_context_assembler_insight_pull_1030
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
)
from services.mux.push_mode import FramedPushPayload


def _floor():
    """Floor with stub LLM (we don't want real LLM calls in tests)."""
    f = ConversationalFloor(llm_client=MagicMock())
    # Reset class-level dict between tests
    f._push_session_state = {}
    return f


def _ctx(**overrides):
    """FloorContext factory with sensible defaults."""
    base = {
        "user_message": "How's the project going?",
        "session_id": "s-test",
        "user_id": "u-test",
        "intent_category": "STATUS",
        "intent_action": "get_project_status",
    }
    base.update(overrides)
    return FloorContext(**base)


class TestMaybeAppendPushGuards:
    """Eligibility guards before maybe_push is even called."""

    @pytest.mark.asyncio
    async def test_skip_when_no_user_id(self):
        floor = _floor()
        ctx = _ctx(user_id=None)
        result = await floor._maybe_append_push("primary response", ctx)
        assert result == "primary response"

    @pytest.mark.asyncio
    async def test_skip_when_no_session_id(self):
        floor = _floor()
        ctx = _ctx(session_id=None)
        result = await floor._maybe_append_push("primary response", ctx)
        assert result == "primary response"

    @pytest.mark.asyncio
    async def test_skip_when_intent_is_pull_insights(self):
        """Pull-mode (#1030) already surfaced insights; push would double-surface."""
        floor = _floor()
        ctx = _ctx(intent_category="MEMORY", intent_action="pull_insights")
        with patch("services.mux.push_mode.maybe_push", new=AsyncMock()) as mp:
            result = await floor._maybe_append_push("primary response", ctx)
            assert result == "primary response"
            mp.assert_not_called()

    @pytest.mark.asyncio
    async def test_skip_when_denial_mode(self):
        """Ethics boundary decline (#992) shouldn't carry push appendage."""
        floor = _floor()
        ctx = _ctx(denial_mode=True)
        with patch("services.mux.push_mode.maybe_push", new=AsyncMock()) as mp:
            result = await floor._maybe_append_push("primary response", ctx)
            assert result == "primary response"
            mp.assert_not_called()


class TestMaybeAppendPushBehavior:
    """maybe_push interaction + augmentation + state update."""

    @pytest.mark.asyncio
    async def test_no_payload_returns_unchanged_message(self):
        floor = _floor()
        ctx = _ctx()
        with patch("services.mux.push_mode.maybe_push", new=AsyncMock(return_value=None)):
            result = await floor._maybe_append_push("primary response", ctx)
            assert result == "primary response"
            # last_push_at NOT updated when no payload
            assert floor._push_session_state.get("s-test", {}).get("last_push_at") is None

    @pytest.mark.asyncio
    async def test_payload_appends_framed_text_and_affordances(self):
        floor = _floor()
        ctx = _ctx()
        payload = FramedPushPayload(
            insight_id="ins-1",
            framed_text="By the way, I've noticed you tend to work in focused mornings.",
        )
        with patch("services.mux.push_mode.maybe_push", new=AsyncMock(return_value=payload)):
            result = await floor._maybe_append_push("primary response", ctx)
        assert "primary response" in result
        assert payload.framed_text in result
        # Affordances present
        assert "Not now" in result or "quiet insights" in result
        assert "Tell me more" in result
        # Cooldown updated
        assert floor._push_session_state.get("s-test", {}).get("last_push_at") is not None

    @pytest.mark.asyncio
    async def test_push_error_is_fail_graceful(self):
        floor = _floor()
        ctx = _ctx()
        with patch(
            "services.mux.push_mode.maybe_push",
            new=AsyncMock(side_effect=RuntimeError("simulated push failure")),
        ):
            result = await floor._maybe_append_push("primary response", ctx)
        # Error swallowed; primary response returned unchanged
        assert result == "primary response"

    @pytest.mark.asyncio
    async def test_mute_active_state_skips_push(self):
        """When session's mute_active is True, _maybe_append_push must pass
        session_mute_active=True to maybe_push. Push_mode's Gate 1 then
        returns None.
        """
        floor = _floor()
        floor._push_session_state["s-test"] = {"mute_active": True}
        ctx = _ctx()

        captured_push_ctx = {}

        async def fake_maybe_push(push_ctx, **_kwargs):
            captured_push_ctx["ctx"] = push_ctx
            return None  # Simulate mute gate firing

        with patch("services.mux.push_mode.maybe_push", new=fake_maybe_push):
            result = await floor._maybe_append_push("primary response", ctx)

        assert result == "primary response"
        assert captured_push_ctx["ctx"].session_mute_active is True


class TestRespondSessionMuteFlow:
    """respond() NL-detected session-mute trigger persists state."""

    @pytest.mark.asyncio
    async def test_mute_utterance_flips_state(self):
        """User says 'don't surface insights' → session state flipped to mute_active."""
        floor = _floor()
        # Stub LLM to skip the network call
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(return_value="OK, noted.")

        ctx = _ctx(user_message="Don't surface insights right now please")
        # Stub push integration since we're testing mute-flip not the push call
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctx)

        assert floor._push_session_state.get("s-test", {}).get("mute_active") is True

    @pytest.mark.asyncio
    async def test_non_mute_utterance_does_not_flip_state(self):
        floor = _floor()
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(return_value="Sure, here's the status.")

        ctx = _ctx(user_message="What's the project status?")
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctx)

        # Either no entry or mute_active False
        sess = floor._push_session_state.get("s-test", {})
        assert sess.get("mute_active", False) is False

    @pytest.mark.asyncio
    async def test_mute_state_persists_across_turns_in_session(self):
        """Once muted in turn N, turn N+1 in same session still muted."""
        floor = _floor()
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(return_value="OK.")

        # Turn 1: mute trigger
        ctx1 = _ctx(user_message="Mute insights")
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctx1)
        assert floor._push_session_state.get("s-test", {}).get("mute_active") is True

        # Turn 2: ordinary query — state should persist
        ctx2 = _ctx(user_message="What's my next task?")
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctx2)
        assert floor._push_session_state.get("s-test", {}).get("mute_active") is True

    @pytest.mark.asyncio
    async def test_new_session_id_resets_state(self):
        """AC: 'Session-mute resets on next session.' New session_id → no mute."""
        floor = _floor()
        floor.llm_client = MagicMock()
        floor.llm_client.complete = AsyncMock(return_value="OK.")

        # Session A: mute (use phrasing the SESSION_MUTE_PATTERNS regex matches:
        # mute-verb directly followed by insights-noun).
        ctxA = _ctx(session_id="session-A", user_message="Don't surface insights")
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctxA)
        assert floor._push_session_state.get("session-A", {}).get("mute_active") is True

        # Session B: brand new session_id; should NOT be muted (state is per-session)
        ctxB = _ctx(session_id="session-B", user_message="What's up?")
        with patch.object(floor, "_maybe_append_push", new=AsyncMock(side_effect=lambda m, c: m)):
            await floor.respond(ctxB)
        sessB = floor._push_session_state.get("session-B", {})
        assert sessB.get("mute_active", False) is False
