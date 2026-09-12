"""Session-lifecycle edge cases.

#1759: this file's clarification-flow tests (context switch, multi-turn
clarification, timeout/invalid/empty/long clarification responses) were
excised with the dead clarify-carrier machinery — ConversationHandler's
pending_clarification arm/consume pair was deleted per the #1730 Gap-2
ruling, so there is no handle_clarification_response to drive. The
surviving tests cover SessionManager lifecycle only and never touched the
carrier or the LLM (the former module-level `llm` mark rode with the
excised tests).
"""

import asyncio
import time
from datetime import datetime, timedelta, timezone

import pytest

from services.session.session_manager import SessionManager


class TestSessionLifecycleEdgeCases:
    """Session lifecycle edge cases (cleanup, performance, concurrency)."""

    @pytest.fixture
    def session_manager(self):
        """Create a fresh session manager for each test"""
        return SessionManager(ttl_minutes=30)

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
