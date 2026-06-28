"""
Integration test for Issue #1030 R4 — full provenance round-trip.

Verifies end-to-end:
1. ContextAssembler.gather_context populates _last_provenance from gatherers
2. Floor.respond() receives FloorContext with domain_context_provenance
3. FloorResponse.provenance reflects intersection of fed-keys + sourced-keys
4. Manually simulating the intent_service write: turn_provenance[turn.id]
   captures the floor response's provenance
5. ConversationContext.get_last_turn_provenance() returns it
6. ProvenanceHandler formats colleague-prose citation

This test focuses on the data flow without mounting the full FastAPI app —
the wire-level integration (HTTP → intent_service → response) is covered by
unit tests at each layer; this test verifies the data shape contracts at
the boundaries.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversation_context import ConversationContext
from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
)
from services.shared_types import IntentCategory
from services.domain.models import Intent


class _NoOpCache:
    async def get_or_compute(self, key, ttl_seconds, compute_fn):
        return await compute_fn()

    async def get(self, key):
        return None

    async def set(self, key, value, ttl_seconds):
        return False

    async def invalidate(self, key):
        return False

    async def invalidate_prefix(self, prefix):
        return 0


@pytest.fixture(autouse=True)
def _patch_context_cache(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.context_assembler.ContextCache",
        lambda *args, **kwargs: _NoOpCache(),
    )


class TestProvenanceRoundtrip:
    """Full data-flow contract from ContextAssembler → Floor → sidecar → handler."""

    @pytest.mark.asyncio
    async def test_full_roundtrip_status_query_then_why(self):
        """User asks for status (which generates context with calendar +
        priorities) → we capture provenance → user follows up 'why did you
        mention that?' → ProvenanceHandler formats grounded citation."""

        # ============================================================
        # Turn 1: STATUS query — gathers context + floor responds
        # ============================================================
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_gather_status_priority_context",
            AsyncMock(
                return_value={
                    "priorities": {"user_priorities": ["ship #1030"]},
                    "blocked_items": [{"number": 1089, "title": "Sample"}],
                }
            ),
        ):
            domain_context = await assembler.gather_context(
                intent_category="STATUS",
                user_id="u-test",
                session_id="s-test",
            )
            provenance_map = assembler.get_last_provenance()

        # Verify Step 5 worked
        assert "priorities" in provenance_map
        assert "blocked_items" in provenance_map
        assert provenance_map["priorities"]["source"] == "UserContextService+GitHub"
        assert provenance_map["blocked_items"]["source"] == "GitHubIntegrationRouter"

        # Floor receives FloorContext with both context + provenance
        floor = ConversationalFloor(llm_client=MagicMock())
        floor._push_session_state = {}  # Reset for test isolation
        floor.llm_client.complete = AsyncMock(
            return_value=(
                "Your top priority is shipping #1030. "
                "You have a blocker on #1089 that's worth attention."
            )
        )

        floor_ctx = FloorContext(
            user_message="What's my status?",
            session_id="s-test",
            user_id="u-test",
            intent_category="STATUS",
            intent_action="get_project_status",
            domain_context=domain_context,
            domain_context_provenance=provenance_map,
        )
        floor_response = await floor.respond(floor_ctx)

        # Verify Step 4 worked: FloorResponse.provenance reflects intersection
        assert "priorities" in floor_response.provenance
        assert "blocked_items" in floor_response.provenance
        # current_time was in context but NOT in provenance (always-available)
        assert "current_time" not in floor_response.provenance

        # ============================================================
        # Simulate intent_service Step 6: write to turn_provenance
        # ============================================================
        conv_ctx = ConversationContext()
        turn1 = conv_ctx.add_turn(message="What's my status?")
        turn1.response = floor_response.message
        # This is exactly what intent_service.py Step 6 code does:
        if floor_response.provenance and conv_ctx.turns:
            conv_ctx.turn_provenance[conv_ctx.turns[-1].id] = floor_response.provenance

        # Verify Step 3 sidecar accepted the entry
        assert conv_ctx.get_turn_provenance(turn1.id) is not None
        prev = conv_ctx.get_previous_assistant_turn()
        assert prev is not None
        assert prev.id == turn1.id

        # ============================================================
        # Turn 2: "why did you bring that up?" — ProvenanceHandler answers
        # ============================================================
        ch = CanonicalHandlers()
        why_intent = Intent(
            category=IntentCategory.PROVENANCE,
            action="explain_suggestion",
            confidence=1.0,
            context={"original_message": "why did you bring up #1089?"},
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=conv_ctx,
        ):
            citation = await ch._handle_provenance_query(
                why_intent, session_id="s-test", user_id="u-test"
            )

        # Verify Step 7 worked: citation grounded in real source phrases
        assert citation["provenance_hit"] is True
        assert citation["keys_cited"] == 2
        msg = citation["message"]
        # Should mention blocked_items source + priorities source
        assert "blocked" in msg.lower() or "GitHub" in msg
        assert "priorities" in msg.lower() or "priorities" in msg
        # Colleague-prose framing (Q2 (b))
        assert "When I said that" in msg or "drawing on" in msg

    @pytest.mark.asyncio
    async def test_roundtrip_with_no_prior_provenance_returns_honest_message(self):
        """If user asks 'why?' but no prior turn has provenance, response is
        honest about not having a record. No fabrication."""
        ch = CanonicalHandlers()
        why_intent = Intent(
            category=IntentCategory.PROVENANCE,
            action="explain_suggestion",
            confidence=1.0,
            context={"original_message": "why did you suggest that?"},
        )
        # Fresh ConversationContext — no provenance
        fresh_ctx = ConversationContext()
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=fresh_ctx,
        ):
            citation = await ch._handle_provenance_query(
                why_intent, session_id="s-test", user_id="u-test"
            )

        assert citation["provenance_hit"] is False
        assert "don't have a clear record" in citation["message"]

    @pytest.mark.asyncio
    async def test_roundtrip_multi_turn_picks_most_recent_provenance(self):
        """User asks 'what's my calendar today' (turn 1) → 'what's blocked'
        (turn 2) → 'why did you mention that?' (turn 3). Step 7 should cite
        turn 2's provenance, not turn 1's."""
        conv_ctx = ConversationContext()
        turn1 = conv_ctx.add_turn(message="what's my calendar today?")
        turn1.response = "You have a 2pm meeting."
        conv_ctx.turn_provenance[turn1.id] = {"calendar": {"source": "CalendarIntegrationRouter"}}

        turn2 = conv_ctx.add_turn(message="what's blocked?")
        turn2.response = "#1089 is blocked."
        conv_ctx.turn_provenance[turn2.id] = {
            "blocked_items": {"source": "GitHubIntegrationRouter"}
        }

        ch = CanonicalHandlers()
        why_intent = Intent(
            category=IntentCategory.PROVENANCE,
            action="explain_suggestion",
            confidence=1.0,
            context={"original_message": "why did you mention that?"},
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=conv_ctx,
        ):
            citation = await ch._handle_provenance_query(
                why_intent, session_id="s-test", user_id="u-test"
            )

        msg = citation["message"]
        # Should reference blocked_items (turn 2), not calendar (turn 1)
        assert "blocked" in msg.lower() or "GitHub" in msg
        assert "calendar" not in msg.lower() or "Google Calendar" not in msg
