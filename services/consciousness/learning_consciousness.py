"""
Consciousness Wrapper for Learning and Preferences

Transforms learning feedback into conscious narrative expression.
Issue: #636 CONSCIOUSNESS-TRANSFORM: Learning Patterns
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import Any, Dict, List


def format_patterns_learned_conscious(patterns: List[Dict[str, Any]], total_analyzed: int) -> str:
    """Format learning patterns feedback with consciousness.

    Transforms the data-driven pattern list into a first-person narrative
    that expresses identity, explains what was learned, and invites dialogue.

    Args:
        patterns: List of identified patterns, each with description, occurrences, confidence
        total_analyzed: Total number of items analyzed

    Returns:
        Formatted message string with consciousness
    """
    if not patterns:
        return (
            f"I looked through {total_analyzed} items but didn't spot any clear patterns yet. "
            "As we work together more, I'll get better at understanding your preferences. "
            "Is there something specific you'd like me to learn?"
        )

    sections = []

    # Opening with identity
    count = len(patterns)
    sections.append(
        f"I've been paying attention to how you work, and I noticed "
        f"{count} {'pattern' if count == 1 else 'patterns'} from our {total_analyzed} interactions."
    )

    # Describe top patterns conversationally
    sections.append("\nHere's what I've learned:")
    for pattern in patterns[:3]:
        desc = pattern.get("description", "a preference")
        confidence = pattern.get("confidence", 0)

        if confidence > 0.8:
            certainty = "I'm pretty confident"
        elif confidence > 0.6:
            certainty = "It seems like"
        else:
            certainty = "I think"

        sections.append(f"- {certainty} you {desc.lower()}")

    # Issue #1096 slice 3 (Pattern-073 discipline): the intent_service
    # _learn_*_patterns methods compute patterns inline and return them in
    # intent_data["patterns_found"] but do NOT persist to a store that
    # future inferences read. The previous copy "I'll keep these in mind
    # going forward" promised persistent learning the system doesn't
    # currently deliver. Honest copy describes the bounded scope.
    sections.append(
        "\nThese are the patterns from the data I just looked at. "
        "Persisting them across sessions is a separate feature; "
        "you can ask me to look again anytime."
    )

    # Dialogue invitation
    sections.append("Does this match what you see, or should I look at the data differently?")

    return "\n".join(sections)


def format_preference_saved_conscious(preference_name: str, value: Any) -> str:
    """Format preference saved feedback with consciousness.

    Transforms preference save confirmation into a first-person narrative
    that acknowledges the change and states future behavior.

    Args:
        preference_name: Name of the preference (may use underscores)
        value: The value being saved

    Returns:
        Formatted message string with consciousness
    """
    # Make preference name human-readable
    readable_name = preference_name.replace("_", " ").lower()

    # #1198: claim only the save itself — "I'll remember / I'll use this in
    # future interactions" is a durable-recall promise the caller may not be
    # able to back (the in-memory preference store doesn't survive restarts;
    # see #1199). If/when this is wired to a persistent store, the caller can
    # add future-tense language deliberately.
    return (
        f"Got it - I've set {readable_name} to '{value}'. " f"Anything else you'd like to adjust?"
    )


def format_learning_event_conscious(what_learned: str, context: str = "") -> str:
    """Format a single learning event with consciousness.

    Transforms a learning event into a first-person narrative
    that explains what was noticed and invites feedback.

    Args:
        what_learned: Description of what was learned (e.g., "you prefer morning standups")
        context: Optional context for the learning (e.g., "your last three requests")

    Returns:
        Formatted message string with consciousness
    """
    base = f"I noticed {what_learned}"
    if context:
        base += f" based on {context}"

    # #1198: offer, don't promise — "I'll remember this for next time" asserts
    # durable recall this function can't guarantee. The OFFER invites consent
    # and matches whatever the caller actually persists.
    return f"{base}. Want me to keep that in mind going forward?"
