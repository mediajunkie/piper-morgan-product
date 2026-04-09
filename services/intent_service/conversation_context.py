"""
Conversation Context Manager (#427 MUX-IMPLEMENT-CONVERSE-MODEL)

Tracks conversational state to enable:
- Conversational follow-ups ("How about today?" after asking about tomorrow)
- Context-dependent phrase resolution
- Turn-by-turn memory within a session

Design principle: "Intent inherits from context when ambiguous"

The 10-turn context window (per PM-034) enables natural conversation
without surveillance-level tracking.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from services.intent_service.intent_types import Intent, IntentCategory


class FollowUpType(str, Enum):
    """Types of conversational follow-ups."""

    TEMPORAL_SHIFT = "temporal_shift"  # "How about today?" after "tomorrow"
    ENTITY_REFERENCE = "entity_reference"  # "What about that one?"
    CONFIRMATION = "confirmation"  # "Yes", "No", "Okay"
    REFINEMENT = "refinement"  # "Just the morning ones"
    CONTINUATION = "continuation"  # "And?" "What else?"
    NEGATION = "negation"  # "Not that one" "Something else"


@dataclass
class LastOffer:
    """Tracks the most recent contextual offer for continuation detection (#852).

    When Piper makes a contextual offer ("Would you like me to explain more?"),
    this stores the continuation hint so the next turn's classifier knows what
    "yes" refers to. One-turn memory — cleared on every new turn regardless.

    Bright-line rule (Chief Architect): If "yes" invokes a named workflow,
    use action_required. If "yes" means "continue/elaborate," use this.
    """

    offer_type: str  # "contextual" (for now; "actionable" reserved for future use)
    continuation_hint: str  # What to continue with, e.g. "explain how project context works"
    offer_text: str = ""  # Original offer text for logging/debugging


@dataclass
class ConversationTurn:
    """
    A single turn in the conversation.

    Captures the message, intent, and key entities for reference resolution.
    """

    id: UUID = field(default_factory=uuid4)
    timestamp: datetime = field(default_factory=datetime.now)
    message: str = ""
    response: Optional[str] = None  # #922: Piper's response, added after processing
    intent: Optional[Intent] = None

    # Extracted entities for reference resolution
    temporal_reference: Optional[str] = None  # "tomorrow", "today", "this week"
    entity_references: list[str] = field(
        default_factory=list
    )  # stored, not yet consumed (audit #827)
    topic: Optional[str] = None  # Inferred topic

    # Conversational lens (#763 GLUE-FOLLOWUP)
    lens: Optional[str] = None  # ConversationalLens value or None

    @property
    def age_seconds(self) -> float:
        """How old this turn is in seconds."""
        return (datetime.now() - self.timestamp).total_seconds()


@dataclass
class ConversationContext:
    """
    Tracks the conversational context for a session.

    Maintains a sliding window of recent turns to enable:
    - Follow-up detection
    - Reference resolution
    - Intent inheritance
    - Lens tracking (#763 GLUE-FOLLOWUP)
    """

    session_id: UUID = field(default_factory=uuid4)
    user_id: Optional[UUID] = None
    turns: list[ConversationTurn] = field(default_factory=list)
    max_turns: int = 10  # PM-034: 10-turn context window
    max_age_minutes: int = 30  # Conversations older than 30 min are stale

    # Lens stack for topic digression/restoration (#763 GLUE-FOLLOWUP)
    lens_stack: list[str] = field(default_factory=list)

    # Issue #852: Track last contextual offer for continuation detection
    last_offer: Optional[LastOffer] = None

    # Issue #913: Track whether last response was a floor hit (continuation rate)
    last_response_was_floor: bool = False
    last_floor_category: Optional[str] = None

    def add_turn(
        self,
        message: str,
        intent: Optional[Intent] = None,
        temporal_reference: Optional[str] = None,
        entity_references: Optional[list[str]] = None,
        topic: Optional[str] = None,
        lens: Optional[str] = None,
    ) -> ConversationTurn:
        """
        Add a new turn to the conversation.

        Automatically prunes old turns to maintain the context window.
        """
        turn = ConversationTurn(
            message=message,
            intent=intent,
            temporal_reference=temporal_reference,
            entity_references=entity_references or [],
            topic=topic,
            lens=lens,
        )
        self.turns.append(turn)
        self._prune_old_turns()
        return turn

    def _prune_old_turns(self) -> None:
        """Remove turns outside the context window."""
        # Remove by age
        cutoff = datetime.now() - timedelta(minutes=self.max_age_minutes)
        self.turns = [t for t in self.turns if t.timestamp > cutoff]

        # Remove by count (keep most recent)
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns :]

        # #763: Clear lens stack when all turns are pruned
        if not self.turns:
            self.lens_stack.clear()

    # ---- Lens stack operations (#763 Phase 4) ----

    def push_lens(self, lens: str) -> None:
        """Push the current lens onto the stack before a sub-topic digression."""
        current = self.current_lens
        if current and current != lens:
            self.lens_stack.append(current)

    def pop_lens(self) -> Optional[str]:
        """Pop the most recent lens from the stack (returning from a digression)."""
        return self.lens_stack.pop() if self.lens_stack else None

    def reset_lens(self) -> None:
        """Clear the lens stack entirely (explicit topic change)."""
        self.lens_stack.clear()

    @property
    def last_turn(self) -> Optional[ConversationTurn]:
        """Get the most recent turn."""
        return self.turns[-1] if self.turns else None

    @property
    def last_intent(self) -> Optional[Intent]:
        """Get the intent from the most recent turn."""
        return self.last_turn.intent if self.last_turn else None

    @property
    def last_temporal_reference(self) -> Optional[str]:
        """Get the most recent temporal reference.

        NOTE: Not yet called in production. Reserved for future temporal
        reference resolution in follow-up handling. (Audit: #827, 2026-02-18)
        """
        for turn in reversed(self.turns):
            if turn.temporal_reference:
                return turn.temporal_reference
        return None

    @property
    def last_topic(self) -> Optional[str]:
        """Get the most recent topic."""
        for turn in reversed(self.turns):
            if turn.topic:
                return turn.topic
        return None

    @property
    def current_lens(self) -> Optional[str]:
        """Get the current conversational lens from the most recent turn with one."""
        for turn in reversed(self.turns):
            if turn.lens:
                return turn.lens
        return None

    @property
    def is_active(self) -> bool:
        """Check if there's an active conversation."""
        if not self.turns:
            return False
        return self.last_turn.age_seconds < (self.max_age_minutes * 60)


# Follow-up phrase patterns
FOLLOW_UP_PATTERNS: dict[FollowUpType, list[str]] = {
    FollowUpType.TEMPORAL_SHIFT: [
        r"^how about (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^what about (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^and (today|tomorrow|yesterday|this week|next week|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",
        r"^(today|tomorrow|yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\??$",  # Single word temporal
    ],
    FollowUpType.CONFIRMATION: [
        r"^(yes|yeah|yep|yup|sure|ok|okay|alright|sounds good|perfect|great)\.?$",
        r"^(no|nope|nah|not really|never mind|cancel)\.?$",
    ],
    FollowUpType.ENTITY_REFERENCE: [
        r"^(that one|the first one|the second one|the last one)\.?$",
        r"^what about (that|this|it|them)\??$",
        r"^tell me more( about (that|it|this))?\??$",
    ],
    FollowUpType.REFINEMENT: [
        r"^just (the|my) (morning|afternoon|evening|work|personal) (ones?|meetings?|tasks?)\.?$",
        r"^only (the|my) (urgent|important|priority) (ones?|items?)\.?$",
        r"^(filter|show) (only|just) .+$",
    ],
    FollowUpType.CONTINUATION: [
        r"^(and|what else|anything else|more|continue)\??$",
        r"^go on\.?$",
        r"^keep going\.?$",
    ],
    FollowUpType.NEGATION: [
        r"^not (that|those|this|it)\.?$",
        r"^something else\.?$",
        r"^different (one|ones)\.?$",
    ],
}


def detect_follow_up(
    message: str,
    context: ConversationContext,
) -> Optional[tuple[FollowUpType, dict[str, Any]]]:
    """
    Detect if a message is a conversational follow-up.

    Args:
        message: The user's message
        context: The conversation context

    Returns:
        Tuple of (follow_up_type, extracted_data) or None if not a follow-up
    """
    import re

    if not context.is_active:
        return None

    clean_msg = message.strip().lower()

    # Check each follow-up type
    for follow_up_type, patterns in FOLLOW_UP_PATTERNS.items():
        for pattern in patterns:
            match = re.match(pattern, clean_msg, re.IGNORECASE)
            if match:
                extracted = {"groups": match.groups() if match.groups() else []}

                # Extract specific data based on type
                if follow_up_type == FollowUpType.TEMPORAL_SHIFT:
                    # Extract the new temporal reference
                    if match.groups():
                        extracted["new_temporal"] = match.group(1)

                return (follow_up_type, extracted)

    return None


def resolve_follow_up(
    follow_up_type: FollowUpType,
    extracted_data: dict[str, Any],
    context: ConversationContext,
) -> Optional[Intent]:
    """
    Resolve a follow-up into a concrete intent by inheriting from context.

    Args:
        follow_up_type: The type of follow-up detected
        extracted_data: Data extracted from the follow-up message
        context: The conversation context

    Returns:
        A resolved Intent that inherits from context, or None if unresolvable
    """
    last_intent = context.last_intent
    if not last_intent:
        return None

    # #763: Inherit lens from context for all follow-up types
    current_lens = context.current_lens

    if follow_up_type == FollowUpType.TEMPORAL_SHIFT:
        # Inherit the intent category and action, but update temporal context
        new_temporal = extracted_data.get("new_temporal")
        if new_temporal and last_intent:
            # Create a new intent with updated temporal reference
            return Intent(
                category=last_intent.category,
                action=last_intent.action,
                confidence=0.9,  # Slightly lower confidence for inferred intent
                context={
                    **(last_intent.context or {}),
                    "temporal_reference": new_temporal,
                    "inherited_from": str(context.last_turn.id) if context.last_turn else None,
                    "follow_up_type": follow_up_type.value,
                    "inherited_lens": current_lens,
                },
            )

    elif follow_up_type == FollowUpType.CONFIRMATION:
        # Return a confirmation intent with the original context
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="confirmation",
            confidence=1.0,
            context={
                "confirmed_intent": last_intent.action if last_intent else None,
                "original_message": context.last_turn.message if context.last_turn else None,
                "inherited_lens": current_lens,
            },
        )

    elif follow_up_type == FollowUpType.CONTINUATION:
        # Return a continuation intent
        return Intent(
            category=last_intent.category if last_intent else IntentCategory.CONVERSATION,
            action="continue_previous",
            confidence=0.9,
            context={
                "previous_intent": last_intent.action if last_intent else None,
                "previous_topic": context.last_topic,
                "inherited_lens": current_lens,
            },
        )

    elif follow_up_type == FollowUpType.NEGATION:
        # Return a negation/change intent
        return Intent(
            category=IntentCategory.CONVERSATION,
            action="change_selection",
            confidence=0.9,
            context={
                "rejected_intent": last_intent.action if last_intent else None,
                "inherited_lens": current_lens,
            },
        )

    return None


def extract_temporal_reference(message: str) -> Optional[str]:
    """
    Extract temporal references from a message.

    Args:
        message: The user's message

    Returns:
        The temporal reference (e.g., "today", "tomorrow") or None
    """
    import re

    temporal_patterns = [
        (r"\b(today)\b", "today"),
        (r"\b(tomorrow)\b", "tomorrow"),
        (r"\b(yesterday)\b", "yesterday"),
        (r"\b(this week)\b", "this_week"),
        (r"\b(next week)\b", "next_week"),
        (r"\b(last week)\b", "last_week"),
        (r"\b(this month)\b", "this_month"),
        (r"\b(next month)\b", "next_month"),
        (r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", None),  # Day name
    ]

    clean_msg = message.lower()
    for pattern, replacement in temporal_patterns:
        match = re.search(pattern, clean_msg, re.IGNORECASE)
        if match:
            return replacement or match.group(1).lower()

    return None


def extract_topic(message: str, intent: Optional[Intent] = None) -> Optional[str]:
    """
    Extract the topic from a message.

    Args:
        message: The user's message
        intent: The classified intent (if available)

    Returns:
        The topic or None
    """
    # Topic inference based on intent category
    topic_by_category = {
        IntentCategory.QUERY: "information",
        IntentCategory.TEMPORAL: "time",
        IntentCategory.STATUS: "status",
        IntentCategory.PRIORITY: "priorities",
        IntentCategory.EXECUTION: "action",
    }

    if intent:
        # Use action as topic if specific
        if intent.action and intent.action not in ["get", "list", "query"]:
            return intent.action

        # Fall back to category-based topic
        return topic_by_category.get(intent.category)

    return None


# Session storage (in-memory for now, can be backed by Redis/DB later)
_conversation_contexts: dict[str, ConversationContext] = {}


def _context_key(session_id: str, user_id: Optional[str] = None) -> str:
    """Build composite key for user-scoped context storage (#817)."""
    return f"{user_id or 'anonymous'}:{session_id}"


def get_or_create_context(
    session_id: str,
    user_id: Optional[str] = None,
) -> ConversationContext:
    """
    Get or create a conversation context for a session.

    Args:
        session_id: The session identifier
        user_id: Optional user identifier (#817: used for scoped storage key)

    Returns:
        The conversation context
    """
    key = _context_key(session_id, user_id)
    if key not in _conversation_contexts:
        # Defensive UUID parsing — session_id may not be a valid UUID
        # (e.g., "default_session" for unauthenticated users)
        try:
            parsed_session = UUID(session_id) if session_id else uuid4()
        except (ValueError, AttributeError):
            parsed_session = uuid4()

        try:
            parsed_user = UUID(user_id) if user_id else None
        except (ValueError, AttributeError):
            parsed_user = None

        _conversation_contexts[key] = ConversationContext(
            session_id=parsed_session,
            user_id=parsed_user,
        )
    return _conversation_contexts[key]


def clear_context(session_id: str, user_id: Optional[str] = None) -> None:
    """Clear the conversation context for a session.

    NOTE: Not yet called in production. Reserved for explicit session cleanup
    (e.g., logout, session timeout). (Audit: #827, 2026-02-18)
    """
    key = _context_key(session_id, user_id)
    if key in _conversation_contexts:
        del _conversation_contexts[key]
