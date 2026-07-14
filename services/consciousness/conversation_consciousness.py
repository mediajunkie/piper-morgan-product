"""
Consciousness Wrapper for Conversation Responses

Transforms conversation responses into conscious narrative expression.
Part of Phase 3: Proof of Concept Transforms (#407)

Uses the consciousness injection framework to apply standup patterns
to conversational responses (greetings, chitchat, farewells).

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from services.consciousness.validation import validate_mvc


def format_greeting_conscious(
    calendar_summary: Optional[Dict[str, Any]] = None,
    user_name: Optional[str] = None,
    user_timezone: Optional[str] = None,
) -> str:
    """
    Format greeting with consciousness.

    Transforms from:
        "Good morning! Here's your day at a glance:
         📅 **Next**: Team standup at 10:00 AM
         📋 3 meetings today
         What would you like to focus on?"

    To:
        "Good morning! I took a look at your calendar - looks like you have
         a packed day with 3 meetings ahead. Your first one is the team
         standup at 10:00 AM.

         I noticed you have some focus time between 2 and 4 PM if you need
         deep work time. What's on your mind this morning?"

    Args:
        calendar_summary: Calendar data if available
        user_name: User's name for personalization

    Returns:
        Conscious narrative greeting
    """
    time_of_day = _current_time_of_day(user_timezone)

    sections = []

    # Opening with identity and temporal awareness
    opening = _build_greeting_opening(time_of_day, user_name)
    sections.append(opening)

    # Calendar context with source attribution
    if calendar_summary and not calendar_summary.get("error"):
        calendar_section = _build_calendar_narrative(calendar_summary)
        if calendar_section:
            sections.append(calendar_section)

    # Dialogue invitation
    sections.append(_build_greeting_invitation(time_of_day, calendar_summary))

    narrative = "\n\n".join(sections)

    # Validate MVC
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = _fix_mvc_gaps(narrative, mvc_result)

    return narrative


def format_farewell_conscious() -> str:
    """
    Format farewell with consciousness.

    Transforms from:
        "Goodbye! Feel free to return if you need PM assistance."

    To (honest, #1198 - no false monitoring promise):
        "Take care! I'll be here whenever you want to pick things back up."
    """
    # #1198: no false monitoring promise ("I'll keep an eye on things") — Piper
    # has no background watch on the user's behalf, and the phrasing is also
    # surveillance-shaped (anti_surveillance class). Honest version:
    return "Take care! I'll be here whenever you want to pick things back up."


def format_thanks_conscious() -> str:
    """
    Format thanks response with consciousness.

    Transforms from:
        "You're welcome! Is there anything else I can help with?"

    To:
        "Happy to help! Is there anything else on your mind,
         or should I check on something for you?"
    """
    return (
        "Happy to help! Is there anything else on your mind, "
        "or should I check on something for you?"
    )


def format_chitchat_conscious(topic: Optional[str] = None) -> str:
    """
    Format chitchat with consciousness.

    Transforms from:
        "I'm doing well, thanks! Ready to help with any PM tasks you have."

    To (honest, #1198 - no false background-activity claim):
        "I'm doing well, thanks for asking! What's on your mind?"
    """
    # #1198: "I've been keeping an eye on your projects" was a false claim
    # (no such background activity) and surveillance-shaped. Honest version:
    return "I'm doing well, thanks for asking! What's on your mind?"


def format_clarification_conscious(
    analysis_questions: List[Dict[str, Any]],
    original_message: str,
) -> str:
    """
    Format clarification request with consciousness.

    Transforms from:
        "I need a bit more information to help you:
         1. What is the specific goal?
         2. Are there any constraints?"

    To:
        "I want to make sure I understand what you're looking for.
         Based on what you said, I have a couple of questions:

         [questions]

         Once I understand these better, I can help more effectively."
    """
    sections = []

    # Opening with epistemic humility
    sections.append(
        "I want to make sure I understand what you're looking for. "
        "Based on what you said, I have a couple of questions:"
    )

    # Questions
    question_lines = []
    for i, q in enumerate(analysis_questions[:3], 1):
        question_text = q.get("question", "")
        example = q.get("example_answer", "")
        line = f"{i}. {question_text}"
        if example:
            line += f" (for example: {example})"
        question_lines.append(line)

    sections.append("\n".join(question_lines))

    # Closing with invitation
    sections.append("Once I understand these better, I can help more effectively.")

    return "\n\n".join(sections)


def _current_time_of_day(user_timezone: Optional[str]) -> str:
    """Day-part for greetings, honoring the honest-timezone rule.

    We only claim a day-part when we actually know the user's timezone. With
    no tz (a fresh account, no personalization yet), the server clock is UTC —
    and presenting *its* day-part as the user's is a wrong assumption: a
    Pacific user at 11am got "Good evening" from an 18:00-UTC server
    (PM-flagged 2026-07-14, #1381 family). Unknown tz → "unknown" → the
    greeting builders fall back to a neutral "Hello" with no day-part claim.
    """
    if not user_timezone:
        return "unknown"
    try:
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo(user_timezone))
    except Exception:
        # Unknown/invalid tz name — degrade to neutral rather than guess.
        return "unknown"
    return _get_time_of_day(now.hour)


def _get_time_of_day(hour: int) -> str:
    """Get time of day category."""
    if 6 <= hour < 9:
        return "morning"
    elif 9 <= hour < 12:
        return "late_morning"
    elif 12 <= hour < 17:
        return "afternoon"
    else:
        return "evening"


def _build_greeting_opening(time_of_day: str, user_name: Optional[str] = None) -> str:
    """Build greeting opening with identity voice."""
    greetings = {
        "morning": "Good morning",
        "late_morning": "Good morning",
        "afternoon": "Good afternoon",
        "evening": "Good evening",
    }
    greeting = greetings.get(time_of_day, "Hello")

    if user_name:
        return f"{greeting}, {user_name}!"
    return f"{greeting}!"


def _build_calendar_narrative(summary: Dict[str, Any]) -> Optional[str]:
    """Build calendar narrative with source transparency."""
    parts = []

    # Source attribution
    parts.append("I took a look at your calendar ")

    # Meeting load assessment
    stats = summary.get("stats", {})
    total_meetings = stats.get("total_meetings_today", 0)

    if total_meetings == 0:
        parts.append("and it looks like you have a clear day ahead - nice!")
    elif total_meetings >= 4:
        parts.append(f"and it looks like you have a packed day with {total_meetings} meetings")
    else:
        meeting_word = "meeting" if total_meetings == 1 else "meetings"
        parts.append(f"and see you have {total_meetings} {meeting_word} today")

    # Current/next meeting
    if summary.get("current_meeting"):
        meeting = summary["current_meeting"]
        name = meeting.get("summary", "a meeting")
        parts.append(f". I see you're currently in {name}")
    elif summary.get("next_meeting"):
        meeting = summary["next_meeting"]
        name = meeting.get("summary", "a meeting")
        start_time = _format_time(meeting.get("start_time", ""))
        if start_time:
            parts.append(f". Your next one is {name} at {start_time}")
        else:
            parts.append(f". Your next one is {name}")

    # Free blocks (if any)
    if summary.get("free_blocks"):
        blocks = summary["free_blocks"][:2]
        if blocks:
            block = blocks[0]
            start = _format_time(block.get("start_time", ""))
            end = _format_time(block.get("end_time", ""))
            if start and end:
                parts.append(f". I noticed you have some focus time between {start} and {end}")

    return "".join(parts) + "."


def _format_time(time_str: str) -> str:
    """Format time string to readable format."""
    if not time_str or "T" not in str(time_str):
        return ""
    try:
        dt = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
        return dt.strftime("%I:%M %p").lstrip("0").lower()
    except (ValueError, AttributeError):
        return ""


def _build_greeting_invitation(
    time_of_day: str,
    calendar_summary: Optional[Dict[str, Any]],
) -> str:
    """Build dialogue invitation."""
    if time_of_day == "morning" or time_of_day == "late_morning":
        return "What's on your mind this morning?"
    elif time_of_day == "afternoon":
        return "What can I help you with this afternoon?"
    else:
        return "What's on your mind?"


def _fix_mvc_gaps(narrative: str, mvc_result) -> str:
    """Fix any missing MVC requirements."""
    fixed = narrative

    if "identity" in mvc_result.missing:
        fixed = "I'm here and ready. " + fixed

    if "uncertainty" in mvc_result.missing:
        # Add "looks like" somewhere
        fixed = fixed.replace("you have", "it looks like you have", 1)

    if "invitation" in mvc_result.missing:
        fixed = fixed.rstrip(".") + ". What can I help you with?"

    if "attribution" in mvc_result.missing:
        # #1196: only inject attribution if none present — blind replace on text
        # that already says "I took a look at your calendar" produced
        # "I took a look at looking at your calendar," (the PM-observed garble).
        if "took a look" not in fixed and "looking at" not in fixed:
            fixed = fixed.replace("your calendar", "looking at your calendar,", 1)

    return fixed
