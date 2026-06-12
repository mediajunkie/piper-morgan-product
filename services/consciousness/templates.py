"""
Consciousness Expression Templates

Concrete templates for transforming data into conscious narrative.
Templates are organized by pattern category.

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

import random
from typing import Dict, List

# =============================================================================
# OPENING TEMPLATES
# =============================================================================

TEMPORAL_GREETINGS: Dict[str, List[str]] = {
    "morning": [
        "Good morning! I've been looking through your work context...",
        "Morning! Let me share what I found looking at your day...",
        "Good morning! Here's what I see as we start the day...",
    ],
    "late_morning": [
        "Starting a bit later? No worries - let me catch you up...",
        "Good morning! Here's what I found looking through your context...",
        "Late morning check-in - here's what I see...",
    ],
    "afternoon": [
        "Afternoon check-in! Here's where things stand...",
        "Quick afternoon summary - here's what I see...",
        "Checking in this afternoon - here's the picture...",
    ],
    "evening": [
        "End of day? Let's look at what you accomplished...",
        "Wrapping up? Here's how the day went from what I can see...",
        "Evening reflection - here's what I noticed today...",
    ],
}

CONTEXT_ACKNOWLEDGMENTS: Dict[str, List[str]] = {
    "in_meeting": [
        "I see you're in a meeting - I'll keep this brief...",
        "Looks like you're busy right now. Quick summary...",
    ],
    "heavy_meeting_day": [
        "You've got a packed day ahead - {meeting_hours:.1f} hours of meetings. Here's what matters most...",
        "Heavy meeting day! Let me highlight what's most important given your {meeting_count} meetings...",
    ],
    "focus_time": [
        "You've got some focus time coming up - let me help you make the most of it...",
        "I see a focus block ahead. Here's what might be worth tackling...",
    ],
    "general": [
        "Here's what I found looking through your context...",
        "Let me share what I see for today...",
    ],
}

# =============================================================================
# NAVIGATION TEMPLATES
# =============================================================================

SPATIAL_JOURNEY: Dict[str, List[str]] = {
    "single_source": [
        "I checked {source}...",
        "Looking at {source}...",
    ],
    "two_sources": [
        "I started by checking {source1}, then looked at {source2}...",
        "I checked {source1} first, and also looked through {source2}...",
    ],
    "three_plus_sources": [
        "I've been looking through {sources_list}, and {final_source}...",
        "I checked {sources_list}. Also pulled up {final_source}...",
    ],
}

SOURCE_NAMES: Dict[str, str] = {
    "github": "GitHub",
    "calendar": "your calendar",
    "documents": "some relevant documents",
    "session": "your recent session context",
    "issues": "your open issues",
}

SOURCE_ATTRIBUTION: Dict[str, List[str]] = {
    "github": [
        "In GitHub, I see {finding}...",
        "Your GitHub activity shows {finding}...",
        "Looking at GitHub, {finding}...",
    ],
    "calendar": [
        "Your calendar shows {finding}...",
        "Looking at your schedule, {finding}...",
    ],
    "inference": [
        "Based on what I'm seeing, {finding}...",
        "Putting this together, it looks like {finding}...",
    ],
}

# =============================================================================
# DISCOVERY TEMPLATES
# =============================================================================

ACCOMPLISHMENT_RECOGNITION: Dict[str, List[str]] = {
    "single_major": [
        "Nice work on {accomplishment}! That looked like a big one.",
        "I see you finished {accomplishment} - great progress!",
        "You completed {accomplishment} - that's been on the list a while!",
    ],
    "single_minor": [
        "You worked on {accomplishment}...",
        "I see {accomplishment} got done...",
    ],
    "multiple": [
        "Looks like you made good progress - {main}, plus {count} other {items}.",
        "Productive day! You finished {main}, along with {count} other {items}.",
        "Nice momentum - {main} done, and {count} more {items} checked off.",
    ],
    "none": [
        "I didn't find much recorded activity yesterday. You might have been in meetings or doing work I can't see. What were you focused on?",
        "Quiet day on the tools I can see - probably means heads-down work or meetings. What were you working on?",
    ],
}

PRIORITY_FRAMING: Dict[str, List[str]] = {
    "single_clear": [
        "The main thing today looks like {priority}...",
        "I'd focus on {priority} - it seems like the critical path.",
        "Today's priority looks like {priority}...",
    ],
    "multiple_ranked": [
        "A few things competing for attention today. I'd suggest: {priority1} first, then {priority2}.",
        "You've got {priority1} and {priority2} on deck. {priority1} seems more urgent.",
    ],
    "multiple_equal": [
        "You've got {count} priorities today: {priorities}. Which feels most important to you?",
        "Several things to tackle: {priorities}. What's your instinct on where to start?",
    ],
    "with_calendar_context": [
        "Given your {meeting_count} meetings, maybe focus on {priority} during your focus time?",
        "With {meeting_hours:.1f} hours of meetings, your best window for deep work is limited.",
    ],
}

# =============================================================================
# CONCERN TEMPLATES
# =============================================================================

GENTLE_FLAGGING: Dict[str, List[str]] = {
    "blocker": [
        "One thing I wanted to flag - {blocker}. This might need attention.",
        "I noticed {blocker} - something to keep an eye on.",
        "One thing that could use attention: {blocker}.",  # #1198: no first-person monitoring claim
    ],
    "potential_issue": [
        "I'm not sure if this is a problem, but {concern}...",
        "This might be nothing, but I noticed {concern}...",
        "I could be wrong about this, but it looks like {concern}...",
    ],
    "workload": [
        "You've got a lot on your plate today - {count} items. Let me know if you want help prioritizing.",
        "That's a full agenda. If something needs to slip, what would it be?",
    ],
}

MISSING_DATA_EXPLANATION: Dict[str, List[str]] = {
    "no_github": [
        "I didn't see much GitHub activity yesterday - you might have been in meetings or doing work I can't see. What were you focused on?",
        "Quiet day on GitHub. That usually means meetings or deep work elsewhere. What's the context?",
    ],
    "no_calendar": [
        "Your calendar looks open today. That could mean focus time, or maybe meetings aren't synced?",
        "I don't see any calendar events. Is your calendar connected, or is today really that open?",
    ],
    "no_context": [
        "I don't have much context from yesterday. Want to fill me in so I can track it going forward?",
        "Starting fresh today - I don't have history from yesterday. What should I know?",
    ],
}

# =============================================================================
# CLOSING TEMPLATES
# =============================================================================

SUMMARY_SYNTHESIS: Dict[str, List[str]] = {
    "positive": [
        "Overall, good momentum from yesterday carrying into today.",
        "Looks like a productive day ahead with clear priorities.",
        "Nice progress yesterday, and today's plan looks solid.",
    ],
    "neutral": [
        "That's the picture from what I can see.",
        "Here's where things stand heading into today.",
    ],
    "cautious": [
        "It's a busy day, but manageable if you protect your focus time.",
        "A lot on the plate today - staying focused will be key.",
    ],
    "with_concern": [
        "Good direction overall, though {concern} is worth watching.",
        "Solid plan, with one thing to keep an eye on: {concern}.",
    ],
}

DIALOGUE_INVITATION: List[str] = [
    "How does that sound? Anything you'd like me to adjust?",
    "Does this capture your priorities? Let me know what to change.",
    "What do you think? I can update this if something's off.",
    "Anything I missed or got wrong?",
    "Let me know if you want to adjust anything.",
]


# =============================================================================
# TEMPLATE SELECTION HELPERS
# =============================================================================


def get_temporal_greeting(time_of_day: str) -> str:
    """Get a random temporal greeting for the time of day."""
    templates = TEMPORAL_GREETINGS.get(time_of_day, TEMPORAL_GREETINGS["morning"])
    return random.choice(templates)


def get_context_acknowledgment(context_type: str, **kwargs) -> str:
    """Get a context acknowledgment, formatted with kwargs."""
    templates = CONTEXT_ACKNOWLEDGMENTS.get(context_type, CONTEXT_ACKNOWLEDGMENTS["general"])
    template = random.choice(templates)
    return template.format(**kwargs) if kwargs else template


def get_spatial_journey(sources: List[str]) -> str:
    """Get spatial journey narrative for given sources."""
    if not sources:
        return ""

    source_names = [SOURCE_NAMES.get(s, s) for s in sources]

    if len(sources) == 1:
        template = random.choice(SPATIAL_JOURNEY["single_source"])
        return template.format(source=source_names[0])
    elif len(sources) == 2:
        template = random.choice(SPATIAL_JOURNEY["two_sources"])
        return template.format(source1=source_names[0], source2=source_names[1])
    else:
        template = random.choice(SPATIAL_JOURNEY["three_plus_sources"])
        return template.format(
            sources_list=", ".join(source_names[:-1]),
            final_source=source_names[-1],
        )


def get_accomplishment_recognition(accomplishments: List[str]) -> str:
    """Get accomplishment recognition narrative."""
    if not accomplishments:
        return random.choice(ACCOMPLISHMENT_RECOGNITION["none"])

    if len(accomplishments) == 1:
        template = random.choice(ACCOMPLISHMENT_RECOGNITION["single_major"])
        return template.format(accomplishment=accomplishments[0])
    else:
        template = random.choice(ACCOMPLISHMENT_RECOGNITION["multiple"])
        items = "item" if len(accomplishments) - 1 == 1 else "items"
        return template.format(
            main=accomplishments[0],
            count=len(accomplishments) - 1,
            items=items,
        )


def get_priority_framing(priorities: List[str], context: dict = None) -> str:
    """Get priority framing narrative."""
    if not priorities:
        return ""

    context = context or {}

    if len(priorities) == 1:
        template = random.choice(PRIORITY_FRAMING["single_clear"])
        return template.format(priority=priorities[0])
    elif context.get("meeting_load") == "heavy":
        template = random.choice(PRIORITY_FRAMING["with_calendar_context"])
        return template.format(
            priority=priorities[0],
            meeting_count=context.get("meeting_count", 0),
            meeting_hours=context.get("meeting_hours", 0),
        )
    else:
        template = random.choice(PRIORITY_FRAMING["multiple_ranked"])
        return template.format(
            priority1=priorities[0],
            priority2=priorities[1] if len(priorities) > 1 else "other items",
        )


def get_gentle_flagging(blockers: List[str]) -> str:
    """Get gentle flagging for blockers."""
    if not blockers:
        return ""

    template = random.choice(GENTLE_FLAGGING["blocker"])
    return template.format(blocker=blockers[0])


def get_summary_synthesis(context: dict) -> str:
    """Get summary synthesis based on context."""
    if context.get("has_blockers"):
        template = random.choice(SUMMARY_SYNTHESIS["with_concern"])
        return template.format(concern="the blocker mentioned above")
    elif context.get("meeting_load") == "heavy":
        return random.choice(SUMMARY_SYNTHESIS["cautious"])
    elif context.get("has_accomplishments"):
        return random.choice(SUMMARY_SYNTHESIS["positive"])
    else:
        return random.choice(SUMMARY_SYNTHESIS["neutral"])


def get_dialogue_invitation() -> str:
    """Get a random dialogue invitation."""
    return random.choice(DIALOGUE_INVITATION)
