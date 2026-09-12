import time
from dataclasses import dataclass

import pytest

from services.domain.models import Intent
from services.session.session_manager import ConversationSession, SessionManager
from services.shared_types import IntentCategory


@dataclass
class DummyIntent:
    action: str
    category: IntentCategory
    confidence: float
    context: dict

    def to_dict(self):
        return {
            "action": self.action,
            "category": self.category.value,
            "confidence": self.confidence,
        }


def test_conversation_session_interaction():
    session = ConversationSession("test-session")
    intent = DummyIntent(
        action="greeting", category=IntentCategory.CONVERSATION, confidence=1.0, context={}
    )
    session.add_interaction(intent, "Hello!")
    assert len(session.history) == 1
    assert session.history[0]["intent"]["action"] == "greeting"
    assert session.history[0]["response"] == "Hello!"
    # #1759: the pending_clarification assertions were excised with the
    # deleted carrier trio (set/get/clear_pending_clarification).


def test_session_manager_get_or_create():
    manager = SessionManager(ttl_minutes=0.001)  # Short TTL for test
    session1 = manager.get_or_create_session()
    session2 = manager.get_or_create_session(session1.session_id)
    assert session1 is session2
    session3 = manager.get_or_create_session()
    assert session3.session_id != session1.session_id
    # Test cleanup
    session1.last_activity = session1.last_activity.replace(year=2000)  # Simulate old session
    manager.cleanup_expired_sessions()
    assert session1.session_id not in manager._sessions
