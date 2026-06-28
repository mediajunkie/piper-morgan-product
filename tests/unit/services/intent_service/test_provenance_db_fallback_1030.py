"""
Tests for Issue #1030 R4 Step 11: cross-session DB-backed provenance fallback.

PM Q1 disposition: cross-session GUARANTEED. When the in-memory sidecar
misses (turn aged out of 30-min/10-turn window, OR process restart), the
ProvenanceHandler falls back to ConversationTurnDB.turn_metadata['provenance']
via ConversationRepository.get_most_recent_turn_provenance().

Plus:
- ConversationManager.save_conversation_turn accepts + persists provenance
- IntentService._save_conversation_turn passes through to ConversationManager
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import ConversationContext
from services.shared_types import IntentCategory
from services.domain.models import Intent


def _mk_intent():
    return Intent(
        category=IntentCategory.PROVENANCE,
        action="explain_suggestion",
        confidence=1.0,
        context={"original_message": "why did you mention that?"},
    )


class TestProvenanceHandlerDBFallback:
    """When in-memory sidecar misses, ProvenanceHandler queries DB."""

    @pytest.mark.asyncio
    async def test_db_fallback_hit_when_sidecar_empty(self):
        """Empty sidecar + DB has provenance → DB-source citation."""
        ch = CanonicalHandlers()
        intent = _mk_intent()

        # Fresh ConversationContext — no in-memory sidecar
        fresh_ctx = ConversationContext()

        # Mock the DB lookup to return a provenance dict
        db_provenance = {"calendar": {"source": "CalendarIntegrationRouter"}}

        async def fake_get_most_recent_turn_provenance(conv_id):
            return db_provenance

        mock_repo = MagicMock()
        mock_repo.get_most_recent_turn_provenance = fake_get_most_recent_turn_provenance

        mock_session_factory = MagicMock()
        # session_scope() returns an async context manager
        mock_session_factory.session_scope.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock()
        )
        mock_session_factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "services.intent_service.conversation_context.get_or_create_context",
                return_value=fresh_ctx,
            ),
            patch(
                "services.database.repositories.ConversationRepository",
                return_value=mock_repo,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        assert result["provenance_hit"] is True
        assert result["fallback_source"] == "db"  # Came from DB, not sidecar
        assert "Google Calendar" in result["message"]

    @pytest.mark.asyncio
    async def test_db_fallback_miss_returns_honest_no_record(self):
        """Empty sidecar AND DB returns None → honest no-record."""
        ch = CanonicalHandlers()
        intent = _mk_intent()
        fresh_ctx = ConversationContext()

        async def fake_get_most_recent_turn_provenance(conv_id):
            return None  # DB has nothing either

        mock_repo = MagicMock()
        mock_repo.get_most_recent_turn_provenance = fake_get_most_recent_turn_provenance

        mock_session_factory = MagicMock()
        mock_session_factory.session_scope.return_value.__aenter__ = AsyncMock(
            return_value=MagicMock()
        )
        mock_session_factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "services.intent_service.conversation_context.get_or_create_context",
                return_value=fresh_ctx,
            ),
            patch(
                "services.database.repositories.ConversationRepository",
                return_value=mock_repo,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        assert result["provenance_hit"] is False
        assert "don't have a clear record" in result["message"]

    @pytest.mark.asyncio
    async def test_db_fallback_error_is_fail_graceful(self):
        """DB query raises → caught + handler still returns honest no-record."""
        ch = CanonicalHandlers()
        intent = _mk_intent()
        fresh_ctx = ConversationContext()

        mock_session_factory = MagicMock()
        mock_session_factory.session_scope.side_effect = RuntimeError("simulated DB outage")

        with (
            patch(
                "services.intent_service.conversation_context.get_or_create_context",
                return_value=fresh_ctx,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        # DB error swallowed; honest no-record response
        assert result["provenance_hit"] is False
        assert "don't have a clear record" in result["message"]

    @pytest.mark.asyncio
    async def test_sidecar_hit_short_circuits_no_db_call(self):
        """When sidecar has provenance, DB should NOT be queried."""
        ch = CanonicalHandlers()
        intent = _mk_intent()

        ctx = ConversationContext()
        turn = ctx.add_turn(message="what's blocked?")
        turn.response = "#1089 is blocked."
        ctx.turn_provenance[turn.id] = {"blocked_items": {"source": "GitHubIntegrationRouter"}}

        mock_session_factory = MagicMock()
        # If session_scope is called, this will be True
        mock_session_factory.session_scope = MagicMock()

        with (
            patch(
                "services.intent_service.conversation_context.get_or_create_context",
                return_value=ctx,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory",
                mock_session_factory,
            ),
        ):
            result = await ch._handle_provenance_query(
                intent, session_id="s-test", user_id="u-test"
            )

        assert result["provenance_hit"] is True
        assert result["fallback_source"] == "sidecar"
        # DB session was NEVER opened
        mock_session_factory.session_scope.assert_not_called()
