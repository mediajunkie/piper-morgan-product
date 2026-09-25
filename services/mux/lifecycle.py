"""
Lifecycle State Machine with Composting.

This module implements the 8-stage lifecycle for objects in the MUX-VISION model:
EMERGENT → DERIVED → NOTICED → PROPOSED → RATIFIED → DEPRECATED → ARCHIVED → COMPOSTED

"Nothing disappears, it transforms."

The lifecycle represents how ideas, tasks, and decisions mature through a system:
- Objects begin as EMERGENT (first stirrings)
- Progress through recognition and formalization
- Eventually decompose into COMPOSTED nourishment for new ideas

References:
- ADR-055: Object Model Implementation
- MUX-399-P3: Lifecycle State Machine
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, runtime_checkable


class LifecycleState(Enum):
    """
    The 8 stages of an object's lifecycle.

    Each state represents a phase of consciousness:
    - EMERGENT: First stirrings, not yet formed
    - DERIVED: Pattern recognized from emergence
    - NOTICED: Brought to attention, considered
    - PROPOSED: Formally recommended for adoption
    - RATIFIED: Officially accepted and active
    - DEPRECATED: Marked for retirement
    - ARCHIVED: Preserved but inactive
    - COMPOSTED: Transformed into nourishment for new growth
    """

    EMERGENT = "emergent"
    DERIVED = "derived"
    NOTICED = "noticed"
    PROPOSED = "proposed"
    RATIFIED = "ratified"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"
    COMPOSTED = "composted"

    @property
    def meaning(self) -> str:
        """What this state means in the lifecycle journey."""
        meanings = {
            LifecycleState.EMERGENT: (
                "First stirrings of formation - an idea is forming in the collective consciousness"
            ),
            LifecycleState.DERIVED: (
                "Pattern derived from emergence - recognized as a distinct entity"
            ),
            LifecycleState.NOTICED: (
                "Brought to attention - someone or something has noticed this matters"
            ),
            LifecycleState.PROPOSED: (
                "Formally proposed for consideration - a recommendation has been made"
            ),
            LifecycleState.RATIFIED: (
                "Officially ratified and accepted - now part of the active system"
            ),
            LifecycleState.DEPRECATED: ("Marked as deprecated - scheduled for retirement"),
            LifecycleState.ARCHIVED: ("Preserved in the archive - inactive but not forgotten"),
            LifecycleState.COMPOSTED: (
                "Transformed into nourishment - wisdom extracted for future growth"
            ),
        }
        return meanings[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses experiencing objects in this state.

        These phrases are designed for conversational UI - short, actionable,
        and how Piper would naturally begin describing something in this state.
        """
        phrases = {
            LifecycleState.EMERGENT: "I just noticed...",
            LifecycleState.DERIVED: "I figured out from...",
            LifecycleState.NOTICED: "I'm aware of...",
            LifecycleState.PROPOSED: "I think we should...",
            LifecycleState.RATIFIED: "We're doing...",
            LifecycleState.DEPRECATED: "This used to be...",
            LifecycleState.ARCHIVED: "I remember when...",
            LifecycleState.COMPOSTED: "I learned that...",
        }
        return phrases[self]

    @property
    def typical_objects(self) -> List[str]:
        """Types of objects typically found in this state."""
        objects = {
            LifecycleState.EMERGENT: [
                "draft ideas",
                "fleeting thoughts",
                "unstructured notes",
                "initial signals",
            ],
            LifecycleState.DERIVED: [
                "recognized patterns",
                "extracted themes",
                "identified trends",
                "synthesized insights",
            ],
            LifecycleState.NOTICED: [
                "flagged items",
                "attention requests",
                "prioritized concerns",
                "acknowledged issues",
            ],
            LifecycleState.PROPOSED: [
                "feature requests",
                "RFC documents",
                "decision proposals",
                "change requests",
            ],
            LifecycleState.RATIFIED: [
                "active policies",
                "approved features",
                "accepted standards",
                "official decisions",
            ],
            LifecycleState.DEPRECATED: [
                "legacy features",
                "sunset APIs",
                "retiring processes",
                "phasing-out practices",
            ],
            LifecycleState.ARCHIVED: [
                "historical records",
                "past decisions",
                "completed projects",
                "reference documents",
            ],
            LifecycleState.COMPOSTED: [
                "lessons learned",
                "extracted wisdom",
                "pattern insights",
                "retrospective findings",
            ],
        }
        return objects[self]


# =============================================================================
# Transition Rules
# =============================================================================

VALID_TRANSITIONS: Dict[LifecycleState, Set[LifecycleState]] = {
    LifecycleState.EMERGENT: {LifecycleState.DERIVED, LifecycleState.NOTICED},
    LifecycleState.DERIVED: {LifecycleState.NOTICED, LifecycleState.DEPRECATED},
    LifecycleState.NOTICED: {LifecycleState.PROPOSED, LifecycleState.DEPRECATED},
    LifecycleState.PROPOSED: {LifecycleState.RATIFIED, LifecycleState.DEPRECATED},
    LifecycleState.RATIFIED: {LifecycleState.DEPRECATED},
    LifecycleState.DEPRECATED: {LifecycleState.ARCHIVED},
    LifecycleState.ARCHIVED: {LifecycleState.COMPOSTED},
    LifecycleState.COMPOSTED: set(),  # Terminal state - nothing beyond compost
}

# Transition explanation templates - how Piper explains why something moved between states
TRANSITION_EXPLANATIONS: Dict[tuple, str] = {
    (LifecycleState.EMERGENT, LifecycleState.DERIVED): "I recognized a pattern in {object}",
    (LifecycleState.EMERGENT, LifecycleState.NOTICED): "I noticed {object} needed attention",
    (LifecycleState.DERIVED, LifecycleState.NOTICED): "{object} caught my attention",
    (LifecycleState.DERIVED, LifecycleState.DEPRECATED): "{object} is no longer relevant",
    (LifecycleState.NOTICED, LifecycleState.PROPOSED): "I think we should act on {object}",
    (LifecycleState.NOTICED, LifecycleState.DEPRECATED): "{object} is no longer a priority",
    (LifecycleState.PROPOSED, LifecycleState.RATIFIED): "We agreed to proceed with {object}",
    (LifecycleState.PROPOSED, LifecycleState.DEPRECATED): "We decided not to pursue {object}",
    (LifecycleState.RATIFIED, LifecycleState.DEPRECATED): "{object} has served its purpose",
    (LifecycleState.DEPRECATED, LifecycleState.ARCHIVED): "I'm preserving {object} for reference",
    (LifecycleState.ARCHIVED, LifecycleState.COMPOSTED): "{object} has taught me something",
}


def transition_explanation(
    from_state: LifecycleState,
    to_state: LifecycleState,
    object_name: str = "this",
    reason: Optional[str] = None,
) -> str:
    """
    Generate a user-friendly explanation for a lifecycle transition.

    Args:
        from_state: The state the object is transitioning from
        to_state: The state the object is transitioning to
        object_name: Name/description of the object being transitioned
        reason: Optional additional context for why the transition happened

    Returns:
        A friendly explanation string, or a generic message if transition unknown
    """
    key = (from_state, to_state)
    template = TRANSITION_EXPLANATIONS.get(key)

    if template:
        explanation = template.format(object=object_name)
        if reason:
            explanation = f"{explanation} - {reason}"
        return explanation

    # Fallback for unknown transitions (shouldn't happen with valid transitions)
    return f"{object_name} moved from {from_state.value} to {to_state.value}"


class InvalidTransitionError(Exception):
    """
    Raised when an invalid lifecycle transition is attempted.

    Objects follow a forward-only lifecycle. You cannot:
    - Go backward (e.g., RATIFIED → PROPOSED)
    - Skip stages without valid paths
    - Resurrect from COMPOSTED
    """

    def __init__(self, from_state: LifecycleState, to_state: LifecycleState):
        self.from_state = from_state
        self.to_state = to_state
        super().__init__(
            f"Invalid transition: {from_state.value} → {to_state.value}. "
            f"Valid transitions from {from_state.value}: "
            f"{[s.value for s in VALID_TRANSITIONS[from_state]]}"
        )

    @property
    def user_message(self) -> str:
        """
        A user-friendly message explaining why this transition isn't possible.

        No technical jargon, no state names - just friendly language.
        """
        # Get the state ordinals for comparison
        states = list(LifecycleState)
        from_idx = states.index(self.from_state)
        to_idx = states.index(self.to_state)

        # From COMPOSTED - terminal state
        if self.from_state == LifecycleState.COMPOSTED:
            return "Once something becomes a learning, it stays that way"

        # Going backward
        if to_idx < from_idx:
            return "I can't go back to that state - things only move forward"

        # Skipping states (forward but not a valid transition)
        if self.to_state not in VALID_TRANSITIONS[self.from_state]:
            return "That's too big a jump - let's take it one step at a time"

        # Generic fallback
        return "That transition isn't possible right now"


@dataclass(frozen=True)
class LifecycleTransition:
    """
    Represents a transition between lifecycle states.

    Captures:
    - from_state: The state being left
    - to_state: The state being entered
    - reason: Why the transition occurred (optional)
    - timestamp: When the transition occurred (auto-set)

    Example:
        transition = LifecycleTransition(
            from_state=LifecycleState.PROPOSED,
            to_state=LifecycleState.RATIFIED,
            reason="Approved by architecture review"
        )
    """

    from_state: LifecycleState
    to_state: LifecycleState
    reason: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    def is_valid(self) -> bool:
        """Check if this transition follows valid lifecycle rules."""
        # Same state is not a valid transition
        if self.from_state == self.to_state:
            return False

        # Check against valid transitions
        return self.to_state in VALID_TRANSITIONS[self.from_state]


# =============================================================================
# HasLifecycle Protocol
# =============================================================================


@runtime_checkable
class HasLifecycle(Protocol):
    """
    Protocol for objects with lifecycle awareness.

    Any object can satisfy this protocol by providing:
    - lifecycle_state: Current state in the lifecycle
    - lifecycle_history: Record of past transitions

    Example:
        class MyTask:
            @property
            def lifecycle_state(self) -> LifecycleState:
                return self._state

            @property
            def lifecycle_history(self) -> List[LifecycleTransition]:
                return self._history

        task = MyTask()
        assert isinstance(task, HasLifecycle)  # True
    """

    @property
    def lifecycle_state(self) -> LifecycleState:
        """The current lifecycle state of this object."""
        ...

    @property
    def lifecycle_history(self) -> List[LifecycleTransition]:
        """The history of lifecycle transitions for this object."""
        ...


# =============================================================================
# LifecycleManager
# =============================================================================


class LifecycleManager:
    """
    Manages lifecycle transitions for objects.

    The manager:
    - Validates transitions against rules
    - Updates object state on valid transitions
    - Records transition history
    - Optionally calls event callbacks

    Example:
        manager = LifecycleManager()
        obj = MyLifecycleObject(state=LifecycleState.EMERGENT)

        manager.transition(obj, LifecycleState.DERIVED)
        assert obj.lifecycle_state == LifecycleState.DERIVED
    """

    def transition(
        self,
        obj: Any,
        to_state: LifecycleState,
        reason: Optional[str] = None,
        on_transition: Optional[Callable[[LifecycleTransition], None]] = None,
    ) -> bool:
        """
        Transition an object to a new lifecycle state.

        Args:
            obj: Object implementing HasLifecycle-like interface
            to_state: The target state
            reason: Why the transition is happening (optional)
            on_transition: Callback after successful transition (optional)

        Returns:
            True if transition succeeded

        Raises:
            InvalidTransitionError: If the transition is not valid
        """
        from_state = obj.lifecycle_state

        # Create transition record
        transition = LifecycleTransition(
            from_state=from_state,
            to_state=to_state,
            reason=reason,
        )

        # Validate
        if not transition.is_valid():
            raise InvalidTransitionError(from_state, to_state)

        # Execute transition
        obj.lifecycle_state = to_state

        # Record history
        if hasattr(obj, "add_history"):
            obj.add_history(transition)
        elif hasattr(obj, "lifecycle_history"):
            obj.lifecycle_history.append(transition)
        elif hasattr(obj, "_history"):
            obj._history.append(transition)

        # Call callback if provided
        if on_transition:
            on_transition(transition)

        return True


# =============================================================================
# Composting Integration
# =============================================================================


@dataclass
class CompostResult:
    """
    The result of composting an object.

    "Nothing disappears, it transforms."

    Contains:
    - object_summary: Key attributes preserved from the original
    - journey: The lifecycle states traversed
    - lessons: Wisdom extracted from the object's existence
    - composted_at: When the composting occurred
    """

    object_summary: Dict[str, Any]
    journey: List[LifecycleState]
    lessons: List[str]
    composted_at: datetime


class CompostingExtractor:
    """
    Extracts wisdom from objects entering the COMPOSTED state.

    The extractor:
    - Captures key object attributes as summary
    - Records the lifecycle journey taken
    - Generates lessons learned from the object's existence
    - Timestamps the transformation

    This enables:
    - Learning from completed/failed work
    - Pattern recognition across composted objects
    - Feeding insights back into new emergent ideas

    Example:
        extractor = CompostingExtractor()
        result = extractor.extract(old_feature)
        for lesson in result.lessons:
            print(f"Learned: {lesson}")
    """

    # Attributes to look for when summarizing objects
    SUMMARY_ATTRIBUTES = [
        "id",
        "title",
        "name",
        "description",
        "type",
        "category",
        "created_at",
        "updated_at",
        "owner",
        "status",
    ]

    def extract(self, obj: Any) -> CompostResult:
        """
        Extract wisdom from an object for composting.

        Args:
            obj: Object to compost (should implement HasLifecycle)

        Returns:
            CompostResult containing preserved wisdom
        """
        object_summary = self._extract_summary(obj)
        journey = self._extract_journey(obj)
        lessons = self._generate_lessons(obj, journey)

        return CompostResult(
            object_summary=object_summary,
            journey=journey,
            lessons=lessons,
            composted_at=datetime.now(),
        )

    def _extract_summary(self, obj: Any) -> Dict[str, Any]:
        """Extract key attributes from the object."""
        summary = {}

        for attr in self.SUMMARY_ATTRIBUTES:
            if hasattr(obj, attr):
                value = getattr(obj, attr)
                # Convert datetime to string for serialization
                if isinstance(value, datetime):
                    value = value.isoformat()
                summary[attr] = value

        return summary

    def _extract_journey(self, obj: Any) -> List[LifecycleState]:
        """Extract the lifecycle journey from history."""
        if not hasattr(obj, "lifecycle_history"):
            return [obj.lifecycle_state] if hasattr(obj, "lifecycle_state") else []

        history = obj.lifecycle_history
        if not history:
            return [obj.lifecycle_state] if hasattr(obj, "lifecycle_state") else []

        # Build journey from history
        journey = [history[0].from_state]
        for transition in history:
            journey.append(transition.to_state)

        return journey

    def _generate_lessons(self, obj: Any, journey: List[LifecycleState]) -> List[str]:
        """Generate lessons learned from the object's lifecycle."""
        lessons = []

        # Lesson from journey length
        if len(journey) >= 7:
            lessons.append("This object completed a full lifecycle - patterns are worth studying")
        elif len(journey) <= 2:
            lessons.append("Short lifecycle - consider what caused early deprecation")

        # Lesson from reaching ratified
        if LifecycleState.RATIFIED in journey:
            lessons.append("Successfully ratified - this approach was validated")

        # Lesson from skipping states
        if (
            LifecycleState.EMERGENT in journey
            and LifecycleState.NOTICED in journey
            and LifecycleState.DERIVED not in journey
        ):
            lessons.append("Skipped derivation - sometimes direct noticing is efficient")

        # Ensure at least one lesson
        if not lessons:
            lessons.append("Every object teaches something through its existence")

        return lessons


def get_composting_narrative(compost_result: CompostResult) -> str:
    """
    Generate a user-facing narrative for a composting event.

    This creates a reflective, learning-focused story of what was gained
    from the object's journey - using the "filing dreams" metaphor rather
    than "deletion" language.

    Args:
        compost_result: The result from CompostingExtractor.extract()

    Returns:
        A narrative string suitable for user display
    """
    journey = compost_result.journey
    lessons = compost_result.lessons
    summary = compost_result.object_summary

    # Get object name from summary, with fallback
    object_name = summary.get("title") or summary.get("name") or "this"

    # Determine journey type for narrative selection
    journey_length = len(journey)
    reached_ratified = LifecycleState.RATIFIED in journey

    # Format lessons for display
    if lessons:
        lessons_text = "; ".join(lessons[:3])  # Limit to 3 for readability
    else:
        lessons_text = "every experience teaches something"

    # Select narrative template based on journey characteristics
    if journey_length >= 6 and reached_ratified:
        # Full lifecycle with ratification - complete journey
        narrative = f"Having had time to reflect on {object_name}, " f"I learned: {lessons_text}."
    elif journey_length >= 6:
        # Full lifecycle but never ratified
        narrative = (
            f"{object_name} went through many stages but never quite landed. "
            f"Still, I noticed: {lessons_text}."
        )
    elif journey_length <= 3 and not reached_ratified:
        # Short lifecycle - quick deprecation
        narrative = f"{object_name} was brief, but I noticed: {lessons_text}."
    elif reached_ratified:
        # Ratified then deprecated - something worked for a while
        narrative = f"{object_name} worked for a while. " f"Looking back: {lessons_text}."
    else:
        # Default reflective narrative
        narrative = f"Reflecting on {object_name}: {lessons_text}."

    return narrative
