"""Manager isolation tests for multi-tenancy security.

Issue #734: SEC-MULTITENANCY - Verify that singleton managers don't leak
state between users.

These tests ensure that:
1. User A's onboarding state is not visible to User B
2. User A's standup conversation is not visible to User B
3. Managers are keyed by user_id, not session_id
"""

from uuid import uuid4

import pytest

from services.onboarding.portfolio_manager import PortfolioOnboardingManager
from services.shared_types import PortfolioOnboardingState, StandupConversationState
from services.standup.conversation_manager import StandupConversationManager

# ADR-059: Mark onboarding-related classes for skip


@pytest.mark.skip(reason="ADR-059: onboarding on ice")
class TestPortfolioOnboardingManagerIsolation:
    """Verify PortfolioOnboardingManager isolates users."""

    def test_user_a_session_not_visible_to_user_b(self):
        """User A's onboarding session should not be visible to User B."""
        manager = PortfolioOnboardingManager()

        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        # User A creates onboarding session
        session_a = manager.create_session(
            session_id=str(uuid4()),
            user_id=user_a_id,
        )

        # Add a project so we can verify state
        manager.add_project(session_a.id, {"name": "User A's Project"})

        # User B queries for their session
        session_b = manager.get_session_by_user(user_b_id)

        # User B should have no session
        assert session_b is None

    def test_user_b_gets_own_session_not_user_a(self):
        """User B should get their own session, not User A's."""
        manager = PortfolioOnboardingManager()

        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        # User A creates session with project
        session_a = manager.create_session(
            session_id=str(uuid4()),
            user_id=user_a_id,
        )
        manager.add_project(session_a.id, {"name": "User A's Project"})

        # User B creates their own session
        session_b = manager.create_session(
            session_id=str(uuid4()),
            user_id=user_b_id,
        )
        manager.add_project(session_b.id, {"name": "User B's Project"})

        # User A queries - should get their own session
        retrieved_a = manager.get_session_by_user(user_a_id)
        assert retrieved_a is not None
        assert retrieved_a.user_id == user_a_id
        assert len(retrieved_a.captured_projects) == 1
        assert retrieved_a.captured_projects[0]["name"] == "User A's Project"

        # User B queries - should get their own session
        retrieved_b = manager.get_session_by_user(user_b_id)
        assert retrieved_b is not None
        assert retrieved_b.user_id == user_b_id
        assert len(retrieved_b.captured_projects) == 1
        assert retrieved_b.captured_projects[0]["name"] == "User B's Project"

    def test_manager_keyed_by_user_id(self):
        """Creating new session for same user should replace old session."""
        manager = PortfolioOnboardingManager()

        user_id = str(uuid4())

        # Create first session
        session_1 = manager.create_session(
            session_id=str(uuid4()),
            user_id=user_id,
        )
        manager.add_project(session_1.id, {"name": "First Project"})

        # Create second session for same user (e.g., new browser tab)
        session_2 = manager.create_session(
            session_id=str(uuid4()),
            user_id=user_id,
        )
        manager.add_project(session_2.id, {"name": "Second Project"})

        # Query should return the latest session
        retrieved = manager.get_session_by_user(user_id)
        assert retrieved is not None
        assert retrieved.id == session_2.id
        assert len(retrieved.captured_projects) == 1
        assert retrieved.captured_projects[0]["name"] == "Second Project"


class TestStandupConversationManagerIsolation:
    """Verify StandupConversationManager isolates users."""

    async def test_user_a_conversation_not_visible_to_user_b(self):
        """User A's standup conversation should not be visible to User B."""
        manager = StandupConversationManager()

        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        # User A creates standup conversation
        conv_a = await manager.create_conversation(
            session_id=str(uuid4()),
            user_id=user_a_id,
        )
        await manager.set_standup_content(conv_a.id, "User A's standup content")

        # User B queries for their conversation
        conv_b = await manager.get_conversation_by_user(user_b_id)

        # User B should have no conversation
        assert conv_b is None

    async def test_user_b_gets_own_conversation_not_user_a(self):
        """User B should get their own conversation, not User A's."""
        manager = StandupConversationManager()

        user_a_id = str(uuid4())
        user_b_id = str(uuid4())

        # User A creates conversation with content
        conv_a = await manager.create_conversation(
            session_id=str(uuid4()),
            user_id=user_a_id,
        )
        await manager.set_standup_content(conv_a.id, "User A's standup")

        # User B creates their own conversation
        conv_b = await manager.create_conversation(
            session_id=str(uuid4()),
            user_id=user_b_id,
        )
        await manager.set_standup_content(conv_b.id, "User B's standup")

        # User A queries - should get their own conversation
        retrieved_a = await manager.get_conversation_by_user(user_a_id)
        assert retrieved_a is not None
        assert retrieved_a.user_id == user_a_id
        assert retrieved_a.current_standup == "User A's standup"

        # User B queries - should get their own conversation
        retrieved_b = await manager.get_conversation_by_user(user_b_id)
        assert retrieved_b is not None
        assert retrieved_b.user_id == user_b_id
        assert retrieved_b.current_standup == "User B's standup"

    async def test_manager_keyed_by_user_id(self):
        """Creating new conversation for same user should replace old."""
        manager = StandupConversationManager()

        user_id = str(uuid4())

        # Create first conversation
        conv_1 = await manager.create_conversation(
            session_id=str(uuid4()),
            user_id=user_id,
        )
        await manager.set_standup_content(conv_1.id, "First standup")

        # Create second conversation for same user
        conv_2 = await manager.create_conversation(
            session_id=str(uuid4()),
            user_id=user_id,
        )
        await manager.set_standup_content(conv_2.id, "Second standup")

        # Query should return the latest conversation
        retrieved = await manager.get_conversation_by_user(user_id)
        assert retrieved is not None
        assert retrieved.id == conv_2.id
        assert retrieved.current_standup == "Second standup"


class TestManagerRequiresUserId:
    """Verify managers require user_id for session creation."""

    def test_portfolio_manager_requires_user_id(self):
        """PortfolioOnboardingManager must require user_id."""
        manager = PortfolioOnboardingManager()

        with pytest.raises((ValueError, TypeError)):
            manager.create_session(
                session_id=str(uuid4()),
                user_id=None,  # None should fail
            )

    def test_portfolio_manager_rejects_empty_user_id(self):
        """PortfolioOnboardingManager must reject empty user_id."""
        manager = PortfolioOnboardingManager()

        with pytest.raises(ValueError, match="user_id"):
            manager.create_session(
                session_id=str(uuid4()),
                user_id="",  # Empty should fail
            )

    async def test_standup_manager_requires_user_id(self):
        """StandupConversationManager must require user_id."""
        manager = StandupConversationManager()

        with pytest.raises((ValueError, TypeError)):
            await manager.create_conversation(
                session_id=str(uuid4()),
                user_id=None,  # None should fail
            )

    async def test_standup_manager_rejects_empty_user_id(self):
        """StandupConversationManager must reject empty user_id."""
        manager = StandupConversationManager()

        with pytest.raises(ValueError, match="user_id"):
            await manager.create_conversation(
                session_id=str(uuid4()),
                user_id="",  # Empty should fail
            )
