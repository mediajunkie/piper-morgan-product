"""
Grammar-conscious intent classification types.

These dataclasses support the MUX grammar transformation of intent
classification from data processing to experiential understanding.

The core insight: transform "classification result" into "what Piper
understood and how she's expressing that understanding."

Issue #619: GRAMMAR-TRANSFORM: Intent Classification
Pattern: Pattern-050 (Context Dataclass Pair)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from services.domain.models import Intent
from services.shared_types import IntentCategory, InteractionSpace, PerceptionMode

if TYPE_CHECKING:
    from services.intent_service.conversation_context import ConversationContext
    from services.mux.orientation import OrientationState


@dataclass
class IntentClassificationContext:
    """
    Rich context for intent classification - the Situation.

    This captures everything Piper knows when trying to understand
    what someone wants. It's not just the message, but the full
    context of who, where, when, and what came before.

    In MUX grammar: this is the Situation - the convergence of
    Entity (user), Place (where), and Moment (when/what's happening).
    """

    message: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    place: InteractionSpace = InteractionSpace.UNKNOWN
    spatial_context: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[str]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)

    # Issue #410: Piper's orientation state (perception through lenses)
    # Set after PlaceDetector, before IntentClassifier per Arch decision
    orientation: Optional["OrientationState"] = None

    # Issue #427: Conversation context for follow-up detection
    # Tracks recent turns for context-dependent phrase resolution
    conversation_context: Optional["ConversationContext"] = None

    @classmethod
    def from_classify_args(
        cls,
        message: str,
        context: Optional[Dict] = None,
        spatial_context: Optional[Dict] = None,
        place: InteractionSpace = InteractionSpace.UNKNOWN,
    ) -> "IntentClassificationContext":
        """
        Build context from existing classify() arguments.

        This factory method enables gradual migration - existing code
        passes the same arguments, and we build rich context from them.
        """
        return cls(
            message=message,
            user_id=(context or {}).get("user_id"),
            session_id=context.get("session_id") if context else None,
            place=place,
            spatial_context=spatial_context,
            conversation_history=context.get("conversation_history") if context else None,
            user_preferences=context.get("user_preferences") if context else None,
        )


@dataclass
class IntentUnderstanding:
    """
    Grammar-conscious classification result - Piper's understanding.

    This wraps the raw Intent with experiential framing. Instead of
    "classification result", this represents "what Piper understood
    and how she's expressing that understanding."

    The `intent` field preserves backward compatibility - existing
    code can access the raw Intent via understanding.intent.

    Experience Test: The narrative should sound like Piper *understood*
    something, not that a system *processed* a query.
    """

    intent: Intent
    understanding_narrative: str  # "I understand you want to..."
    confidence_expression: str  # "I'm fairly certain" / "I think"
    place_awareness: str  # "Since we're in Slack..." (often empty)
    perception_mode: PerceptionMode
    follow_up_suggestion: Optional[str] = None  # What Piper might ask next
    metadata: Optional[Dict[str, Any]] = None  # Additional data (e.g., recognition state)

    @property
    def category(self) -> IntentCategory:
        """Proxy to intent.category for compatibility."""
        return self.intent.category

    @property
    def action(self) -> str:
        """Proxy to intent.action for compatibility."""
        return self.intent.action

    @property
    def confidence(self) -> float:
        """Proxy to intent.confidence for compatibility."""
        return self.intent.confidence

    @property
    def id(self) -> str:
        """Proxy to intent.id for compatibility."""
        return self.intent.id

    @property
    def context(self) -> Dict[str, Any]:
        """Proxy to intent.context for compatibility."""
        return self.intent.context
