import asyncio
import time
from datetime import datetime, timedelta, timezone

import pytest

from services.conversation.conversation_handler import ConversationHandler
from services.intent_service import classifier
from services.session.session_manager import SessionManager
from services.shared_types import IntentCategory

# #1452 wave 21: every test here drives the module-level classifier through
# real classify() calls that reach llm.complete ("create a ticket" → asserts
# on live classification) — keyed llm lane, not the keyless CI sweep.
pytestmark = pytest.mark.llm

# Note: We'll use direct component testing rather than FastAPI TestClient
# since we need more control over session state and async operations


class TestClarificationEdgeCases:
    """Test edge cases for the clarification flow"""

    @pytest.fixture
    def session_manager(self):
        """Create a fresh session manager for each test"""
        return SessionManager(ttl_minutes=30)

    @pytest.fixture
    def conversation_handler(self, session_manager):
        """Create conversation handler with session manager"""
        return ConversationHandler(session_manager=session_manager)

    @pytest.mark.asyncio
    async def test_context_switch_during_clarification(self, session_manager, conversation_handler):
        """Test that Piper handles context switches cleanly without maintaining
        unnecessary clarification state when intents are clear."""
        session_id = "test_context_switch"

        # Start clarification with vague request
        vague_intent = await classifier.classify("create a ticket")
        # System now directly recognizes action intent without clarification
        assert vague_intent.action == "create_ticket"

        # Generate clarification questions and set up session
        response1 = await conversation_handler.respond(vague_intent, session_id)
        # Piper now recognizes intent confidently, so no clarification is needed

        # Check that clarification is NOT pending (Piper is confident)
        session = session_manager.get_or_create_session(session_id)
        assert session.get_pending_clarification() is None  # Piper now confident

        # User switches context with clear intent
        clear_intent = await classifier.classify("actually, list all projects")
        assert clear_intent.category == IntentCategory.QUERY
        assert clear_intent.action == "list_projects"

        # Process the clear intent (should override pending clarification)
        response2 = await conversation_handler.respond(clear_intent, session_id)

        # Should process the new intent, not treat as clarification
        assert response2.get("intent", {}).get("action") == "list_projects"

        # Piper now cleans up unnecessary clarification state after context switch
        session = session_manager.get_or_create_session(session_id)
        assert session.get_pending_clarification() is None  # Clean context switch

    @pytest.mark.asyncio
    async def test_multiple_clarifications_needed(self, session_manager, conversation_handler):
        """Test multiple rounds of clarification"""
        session_id = "test_multi_turn"

        # Very vague request
        vague_intent = await classifier.classify("fix it")
        assert vague_intent.category == IntentCategory.CONVERSATION
        assert vague_intent.action == "clarification_needed"

        # Set up clarification session first
        response0 = await conversation_handler.respond(vague_intent, session_id)
        assert (
            "what" in response0.get("message", "").lower()
            or "details" in response0.get("message", "").lower()
        )

        # First clarification response (still vague)
        response1 = await conversation_handler.handle_clarification_response(
            "the mobile app", session_id
        )

        # Should still need more info - check for clarification indicators
        message = response1.get("message", "").lower()
        assert any(word in message for word in ["what", "details", "detail", "more", "need"])

        # Check that clarification is still pending
        session = session_manager.get_or_create_session(session_id)
        assert session.get_pending_clarification() is not None

        # Second clarification response (more specific)
        response2 = await conversation_handler.handle_clarification_response(
            "the login button crashes on iOS devices", session_id
        )

        # Should now have enough info or still need clarification
        if response2.get("clarification_resolved"):
            assert "understand" in response2.get("message", "").lower()

            # Session should be cleared
            session = session_manager.get_or_create_session(session_id)
            assert session.get_pending_clarification() is None
        else:
            # Still needs more info, which is also valid
            message = response2.get("message", "").lower()
            assert any(word in message for word in ["what", "details", "detail", "more", "need"])

    @pytest.mark.asyncio
    async def test_session_timeout_during_clarification(
        self, session_manager, conversation_handler
    ):
        """Test that expired sessions handle gracefully and Piper does not maintain unnecessary clarification state if intent is clear."""
        session_id = "test_timeout"

        # Create vague request and start clarification
        vague_intent = await classifier.classify("create a ticket")
        response1 = await conversation_handler.respond(vague_intent, session_id)

        # Piper now recognizes intent confidently, so no clarification is needed
        session = session_manager.get_or_create_session(session_id)
        assert session.get_pending_clarification() is None  # Piper now confident

        # Manually expire the session
        session.last_activity = datetime.now(timezone.utc) - timedelta(hours=1)

        # Try to respond to clarification with expired session
        response2 = await conversation_handler.handle_clarification_response(
            "for the login bug", session_id
        )

        # Should handle gracefully (either treat as new intent or give helpful error)
        assert response2 is not None
        assert "message" in response2
        # Test updated to match improved behavior: Timeouts clear pending clarifications
        assert session.get_pending_clarification() is None

    @pytest.mark.asyncio
    async def test_invalid_clarification_response(self, session_manager, conversation_handler):
        """Test handling of unhelpful clarification responses"""
        session_id = "test_invalid"

        # Start clarification
        vague_intent = await classifier.classify("create a ticket")
        response1 = await conversation_handler.respond(vague_intent, session_id)

        # Unhelpful responses
        unhelpful_responses = ["I don't know", "whatever", "???", "skip"]

        for unhelpful in unhelpful_responses:
            response = await conversation_handler.handle_clarification_response(
                unhelpful, session_id
            )

            # Should ask for clarification again or provide helpful guidance
            assert response is not None
            message = response.get("message", "").lower()

            # Should either still need clarification or provide helpful guidance
            # The actual response might be a new clarification question
            assert len(message) > 0  # Should have some response

    def test_session_cleanup(self):
        """Test that old sessions are cleaned up"""
        session_manager = SessionManager(ttl_minutes=1)  # 1 minute TTL

        # Create sessions
        old_session = session_manager.get_or_create_session("old_session")
        old_session.last_activity = datetime.now(timezone.utc) - timedelta(minutes=2)

        active_session = session_manager.get_or_create_session("active_session")

        initial_count = len(session_manager._sessions)

        # Run cleanup
        session_manager.cleanup_expired_sessions()

        # Check results
        assert len(session_manager._sessions) < initial_count
        assert "old_session" not in session_manager._sessions
        assert "active_session" in session_manager._sessions

    def test_session_performance(self):
        """Test that session operations are fast"""
        session_manager = SessionManager()

        # Create many sessions
        start_time = time.time()
        sessions = []
        for i in range(100):
            session = session_manager.get_or_create_session(f"session_{i}")
            sessions.append(session)
        create_time = time.time() - start_time

        # Access sessions
        start_time = time.time()
        for session in sessions:
            retrieved = session_manager._sessions.get(session.session_id)
            assert retrieved is not None
        access_time = time.time() - start_time

        # Cleanup
        start_time = time.time()
        session_manager.cleanup_expired_sessions()
        cleanup_time = time.time() - start_time

        # Assert performance targets (relaxed for CI environments)
        assert create_time < 1.0  # 1 second for 100 sessions
        assert access_time < 0.5  # 500ms for 100 lookups
        assert cleanup_time < 0.1  # 100ms for cleanup

    @pytest.mark.asyncio
    async def test_concurrent_session_access(self, session_manager):
        """Test concurrent access to sessions"""
        session_id = "concurrent_test"

        # Create session
        session = session_manager.get_or_create_session(session_id)

        # Simulate concurrent access
        async def access_session():
            return session_manager.get_or_create_session(session_id)

        # Run multiple concurrent accesses
        tasks = [access_session() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # All should return the same session
        for result in results:
            assert result.session_id == session_id
            assert result is session  # Same object reference

    @pytest.mark.asyncio
    async def test_clarification_with_empty_response(self, session_manager, conversation_handler):
        """Test handling of empty or whitespace-only clarification responses"""
        session_id = "test_empty"

        # Start clarification
        vague_intent = await classifier.classify("create a ticket")
        response1 = await conversation_handler.respond(vague_intent, session_id)

        # Empty responses
        empty_responses = ["", "   ", "\n", "\t"]

        for empty in empty_responses:
            response = await conversation_handler.handle_clarification_response(empty, session_id)

            # Should handle gracefully
            assert response is not None
            assert "message" in response

    @pytest.mark.asyncio
    async def test_clarification_with_very_long_response(
        self, session_manager, conversation_handler
    ):
        """Test that Piper handles very long clarification responses gracefully and does not maintain unnecessary clarification state if intent is clear."""
        session_id = "test_long"

        # Start clarification
        vague_intent = await classifier.classify("create a ticket")
        response1 = await conversation_handler.respond(vague_intent, session_id)

        # Very long response
        long_response = (
            "This is a very detailed explanation of the bug that occurs when users try to log in to the mobile application on iOS devices running version 15.0 or later. The issue manifests as a 500 Internal Server Error that appears after the user enters their credentials and taps the login button. The error message is displayed in a modal dialog that cannot be dismissed, forcing the user to restart the application. This affects approximately 25% of our iOS user base and has been reported by multiple users across different device models including iPhone 12, iPhone 13, and iPhone 14. The bug appears to be related to the authentication service timeout configuration and the way the mobile app handles session tokens. We have received customer complaints about this issue and it is impacting our user satisfaction scores."
            * 3
        )

        response2 = await conversation_handler.handle_clarification_response(
            long_response, session_id
        )

        # Piper now recognizes intent confidently, so no clarification is needed
        session = session_manager.get_or_create_session(session_id)
        assert (
            session.get_pending_clarification() is None
        )  # Piper now confident after long response
