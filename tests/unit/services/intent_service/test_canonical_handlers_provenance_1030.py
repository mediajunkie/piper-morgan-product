"""
Tests for Issue #1030 R4 Step 7: ProvenanceHandler in canonical_handlers.

Covers:
- can_handle includes PROVENANCE category
- handle() routes PROVENANCE to _handle_provenance_query
- _handle_provenance_query with no prior turn provenance → honest no-record response
- _handle_provenance_query with prior turn provenance → colleague-prose citation
- Multi-key (3+) formats with Oxford comma
- Exception fail-graceful (no raised exception, returns honest error message)
"""

from unittest.mock import patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import (
    ConversationContext,
    ConversationTurn,
)
from services.shared_types import IntentCategory as IntentCategoryEnum


def _mk_intent(message="Why did you suggest that?"):
    """Construct an Intent in PROVENANCE category."""
    intent = Intent(
        category=IntentCategoryEnum.PROVENANCE,
        action="explain_suggestion",
        confidence=1.0,
        context={"original_message": message},
    )
    return intent


def _mk_context_with_turn_provenance(session_id, prov_dict):
    """Build a ConversationContext with a turn that has a response + provenance."""
    ctx = ConversationContext()
    turn = ctx.add_turn(message="What's my next priority?")
    turn.response = "Your next priority is shipping #1030."
    ctx.turn_provenance[turn.id] = prov_dict
    return ctx


class TestCanHandleProvenance:
    def test_can_handle_provenance_returns_true(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        assert ch.can_handle(intent) is True


class TestProvenanceHandlerNoRecord:
    @pytest.mark.asyncio
    async def test_no_record_response_when_no_provenance(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        # Fresh ConversationContext, no provenance entries
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=ConversationContext(),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        assert "don't have a clear record" in result["message"]
        assert result["provenance_hit"] is False
        assert result["keys_cited"] == 0


class TestProvenanceHandlerWithRecord:
    @pytest.mark.asyncio
    async def test_single_key_citation(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        ctx = _mk_context_with_turn_provenance(
            "s-test", {"calendar": {"source": "CalendarIntegrationRouter"}}
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=ctx,
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        assert "Google Calendar" in result["message"]
        assert result["provenance_hit"] is True
        assert result["keys_cited"] == 1

    @pytest.mark.asyncio
    async def test_two_key_citation(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        ctx = _mk_context_with_turn_provenance(
            "s-test",
            {
                "calendar": {"source": "CalendarIntegrationRouter"},
                "pending_todos": {"source": "TodoManagementService"},
            },
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=ctx,
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        assert "Google Calendar" in result["message"]
        assert "open todos" in result["message"]
        assert " and " in result["message"]
        assert result["keys_cited"] == 2

    @pytest.mark.asyncio
    async def test_three_plus_key_citation_uses_oxford_comma(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        ctx = _mk_context_with_turn_provenance(
            "s-test",
            {
                "calendar": {"source": "CalendarIntegrationRouter"},
                "pending_todos": {"source": "TodoManagementService"},
                "blocked_items": {"source": "GitHubIntegrationRouter"},
            },
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=ctx,
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        # Three phrases joined with commas + final "and" → Oxford comma usage
        # via the ", " + ", and " pattern
        assert ", and " in result["message"]
        assert result["keys_cited"] == 3

    @pytest.mark.asyncio
    async def test_unknown_provenance_key_named_plainly(self):
        """Keys not in _PROVENANCE_PHRASES still get named (not skipped)."""
        ch = CanonicalHandlers()
        intent = _mk_intent()
        ctx = _mk_context_with_turn_provenance(
            "s-test", {"future_custom_source": {"source": "Whatever"}}
        )
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            return_value=ctx,
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        # Unknown key gets named with underscores stripped
        assert "future custom source" in result["message"]
        assert result["keys_cited"] == 1


class TestProvenanceHandlerErrorPath:
    @pytest.mark.asyncio
    async def test_exception_is_fail_graceful(self):
        """RuntimeError in lookup → honest error message, no raise."""
        ch = CanonicalHandlers()
        intent = _mk_intent()
        with patch(
            "services.intent_service.conversation_context.get_or_create_context",
            side_effect=RuntimeError("simulated failure"),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )
        assert "ran into a snag" in result["message"]
        assert result["provenance_hit"] is False
        assert "error" in result


class TestHandleRoutesPROVENANCEcorrectly:
    @pytest.mark.asyncio
    async def test_handle_dispatches_provenance_to_handler(self):
        ch = CanonicalHandlers()
        intent = _mk_intent()
        with patch.object(
            ch,
            "_handle_provenance_query",
            return_value={"message": "stub", "intent": {}, "requires_clarification": False},
        ) as mock:
            await ch.handle(intent, session_id="s-test", user_id="u-test")
            mock.assert_called_once()
