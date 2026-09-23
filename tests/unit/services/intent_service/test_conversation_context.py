"""
Tests for Conversation Context Manager (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Verifies:
- Turn-by-turn memory
- Context window + session management

(#1768, 2026-09-12: the follow-up detection/resolution/extraction test classes
were deleted with detect_follow_up/resolve_follow_up/extract_temporal_reference/
extract_topic — sole caller was classify_conscious.)

(#1863, 2026-09-23, Rule-0 rip, Arch GO: the writer-less lens surface tests
(TestLensFieldsExist, TestLensStackPruning — ConversationTurn.lens,
ConversationContext.current_lens/lens_stack, the ConversationalLens enum) and
the small-fry temporal_reference/topic/entity_references tests were deleted
here along with the fields and enum they exercised. No writer for any of
these existed anywhere in production post-#1768; see
services/intent_service/conversation_context.py's module docstring and
docs/internal/architecture/design-records/
design-record-lens-surface-rip-1863-2026-09-23.md.)
"""

from datetime import datetime
from uuid import uuid4

from services.domain.models import Intent
from services.intent_service.conversation_context import (
    ConversationContext,
    ConversationTurn,
    clear_context,
    get_or_create_context,
)
from services.shared_types import IntentCategory


class TestConversationTurn:
    """Tests for ConversationTurn dataclass."""

    def test_turn_has_unique_id(self):
        """Each turn should have a unique ID."""
        turn1 = ConversationTurn(message="Hello")
        turn2 = ConversationTurn(message="Hello")
        assert turn1.id != turn2.id

    def test_turn_has_timestamp(self):
        """Turn should have a timestamp."""
        turn = ConversationTurn(message="Hello")
        assert turn.timestamp is not None
        assert isinstance(turn.timestamp, datetime)

    def test_turn_age_seconds(self):
        """Turn should track age in seconds."""
        turn = ConversationTurn(message="Hello")
        assert turn.age_seconds >= 0
        assert turn.age_seconds < 1  # Should be very recent

    def test_turn_stores_intent(self):
        """Turn should store the classified intent."""
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        turn = ConversationTurn(message="What's on my calendar?", intent=intent)
        assert turn.intent == intent


class TestConversationContext:
    """Tests for ConversationContext."""

    def test_context_starts_empty(self):
        """Context should start with no turns."""
        context = ConversationContext()
        assert len(context.turns) == 0

    def test_add_turn(self):
        """Should be able to add turns."""
        context = ConversationContext()
        turn = context.add_turn("Hello Piper!")
        assert len(context.turns) == 1
        assert turn.message == "Hello Piper!"

    def test_last_turn(self):
        """Should return the most recent turn."""
        context = ConversationContext()
        context.add_turn("First")
        context.add_turn("Second")
        context.add_turn("Third")
        assert context.last_turn.message == "Third"

    def test_last_intent(self):
        """Should return intent from last turn."""
        context = ConversationContext()
        intent = Intent(category=IntentCategory.QUERY, action="meeting_time")
        context.add_turn("What's tomorrow?", intent=intent)
        assert context.last_intent == intent

    def test_prunes_old_turns_by_count(self):
        """Should prune turns beyond max_turns."""
        context = ConversationContext(max_turns=3)
        for i in range(5):
            context.add_turn(f"Message {i}")
        assert len(context.turns) == 3
        assert context.turns[0].message == "Message 2"  # Oldest kept

    def test_is_active_when_recent(self):
        """Context should be active when turns are recent."""
        context = ConversationContext()
        context.add_turn("Hello")
        assert context.is_active is True

    def test_not_active_when_empty(self):
        """Context should not be active when empty."""
        context = ConversationContext()
        assert context.is_active is False


class TestSessionManagement:
    """Tests for session context management."""

    def test_get_or_create_new(self):
        """Should create new context for new session."""
        session_id = str(uuid4())
        context = get_or_create_context(session_id)
        assert context is not None
        assert len(context.turns) == 0

    def test_get_or_create_existing(self):
        """Should return existing context."""
        session_id = str(uuid4())
        context1 = get_or_create_context(session_id)
        context1.add_turn("Hello")
        context2 = get_or_create_context(session_id)
        assert len(context2.turns) == 1

    def test_clear_context(self):
        """Should clear context for session."""
        session_id = str(uuid4())
        context = get_or_create_context(session_id)
        context.add_turn("Hello")
        clear_context(session_id)
        new_context = get_or_create_context(session_id)
        assert len(new_context.turns) == 0


class TestContextWindowBehavior:
    """Tests for the 10-turn context window (PM-034)."""

    def test_default_max_turns_is_10(self):
        """Default max turns should be 10 per PM-034."""
        context = ConversationContext()
        assert context.max_turns == 10

    def test_maintains_10_turn_window(self):
        """Should maintain exactly 10 turns when more are added."""
        context = ConversationContext()
        for i in range(15):
            context.add_turn(f"Message {i}")
        assert len(context.turns) == 10
        # Should have messages 5-14 (the last 10)
        assert context.turns[0].message == "Message 5"
        assert context.turns[-1].message == "Message 14"

    def test_30_minute_max_age(self):
        """Default max age should be 30 minutes."""
        context = ConversationContext()
        assert context.max_age_minutes == 30


class TestContextCompositeKeys:
    """Test user-scoped composite keys for context storage (#817)."""

    def test_different_users_get_separate_contexts(self):
        """Two users on the same session_id get separate contexts."""
        from services.intent_service.conversation_context import (
            _conversation_contexts,
        )

        # Clear store for test isolation
        _conversation_contexts.clear()

        sess = "00000000-0000-0000-0000-000000000001"
        alice = "00000000-0000-0000-0000-00000000000a"
        bob = "00000000-0000-0000-0000-00000000000b"

        ctx_alice = get_or_create_context(sess, user_id=alice)
        ctx_bob = get_or_create_context(sess, user_id=bob)

        assert ctx_alice is not ctx_bob
        assert len(_conversation_contexts) == 2
        _conversation_contexts.clear()  # Cleanup

    def test_anonymous_fallback_key(self):
        """No user_id uses 'anonymous' prefix."""
        from services.intent_service.conversation_context import _context_key

        assert _context_key("sess1") == "anonymous:sess1"
        assert _context_key("sess1", "alice") == "alice:sess1"
