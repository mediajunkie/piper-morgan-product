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
from services.utils.datetime_utils import utc_now


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
        calendar_section = _build_calendar_narrative(calendar_summary, user_timezone)
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
    except Exception:  # silent-ok: invalid stored tz -> neutral greeting, no day-part claim; per-turn logging would be noise for a stored bad value (#1589 rationale)
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


def _build_calendar_narrative(
    summary: Dict[str, Any],
    user_timezone: Optional[str] = None,
) -> Optional[str]:
    """Build calendar narrative with source transparency.

    Two honesty rules, both paid for by a live greeting PM read on 2026-08-10
    that claimed a clear day over four real events and offered "focus time
    between 2:09 am and 6:00 pm":

    1. **The zero-claim needs an established read** (#1425 / m-44).
       ``total_meetings_today == 0`` is what a genuinely empty day, an open
       circuit breaker, a failed authenticate, and a swallowed exception all
       look like. Only ``events_read_established`` distinguishes them. Without
       it we say nothing about the day's shape — silence is recoverable, a
       false all-clear is not.
    2. **No unlabeled clock face** (time-handling audit F2). Free-block times
       are computed from the SERVER clock (UTC on Fly), so their bare
       ``%I:%M %p`` renders a UTC instant as if it were the reader's local
       time. Render them only in a zone we can name; otherwise omit.

    Returns None when nothing can be said honestly — the caller then omits the
    calendar section entirely, rather than leaving a stranded "I took a look at
    your calendar." with no observation behind it.
    """
    # Meeting load assessment
    stats = summary.get("stats", {})
    total_meetings = stats.get("total_meetings_today", 0)
    read_established = bool(summary.get("events_read_established"))

    load_assessment = None
    if total_meetings == 0:
        # Rule 1: only an established read may be reported as an empty day.
        if read_established:
            load_assessment = "and it looks like you have a clear day ahead - nice!"
    elif total_meetings >= 4:
        # A nonzero count is self-evidencing: rows came back, so they exist.
        load_assessment = f"and it looks like you have a packed day with {total_meetings} meetings"
    else:
        meeting_word = "meeting" if total_meetings == 1 else "meetings"
        load_assessment = f"and see you have {total_meetings} {meeting_word} today"

    observations = []

    # Current/next meeting. These times come from the calendar provider carrying
    # the event's OWN offset, so their clock face is already the user's local
    # one — a different layer from the server-computed free block below (m-43).
    if summary.get("current_meeting"):
        meeting = summary["current_meeting"]
        name = meeting.get("summary", "a meeting")
        observations.append(f"I see you're currently in {name}")
    elif summary.get("next_meeting"):
        meeting = summary["next_meeting"]
        name = meeting.get("summary", "a meeting")
        start_time = _format_time(meeting.get("start_time", ""))
        if start_time:
            observations.append(f"Your next one is {name} at {start_time}")
        else:
            observations.append(f"Your next one is {name}")

    # Free blocks — server-clock derived, so zone-labeled or not at all.
    free_block_phrase = _format_free_block(summary.get("free_blocks"), user_timezone)
    if free_block_phrase:
        observations.append(free_block_phrase)

    if not load_assessment and not observations:
        return None  # nothing honest to say; omit the calendar line entirely

    if load_assessment:
        narrative = "I took a look at your calendar " + load_assessment
    else:
        # No day-shape claim available, but a concrete observation stands on
        # its own — attribution first, then the thing actually observed.
        narrative = "I took a look at your calendar. " + observations.pop(0)

    for observation in observations:
        # "…clear day ahead - nice!. I noticed…" was the observed copy; don't
        # stack a period onto a sentence that already ended.
        separator = " " if narrative.endswith(("!", "?", ".")) else ". "
        narrative += separator + observation

    if not narrative.endswith((".", "!", "?")):
        narrative += "."
    return narrative


# Free blocks come in three shapes, and they are NOT the same layer (m-43):
#
#   "between_meetings" — both boundaries are real event timestamps carrying the
#       calendar's own offset. The clock face is already the reader's. Safe.
#   "before_meeting"   — starts at the SERVER's wall clock, ends at a real event.
#       Half server-derived, so the start face is unattributable without a zone.
#   "free_block"       — the synthetic "no meetings came back, so treat the rest
#       of the server's day as free" block. Not an observation about the user's
#       day at all: it is the absence of one, wearing an interval's clothes, and
#       both of its boundaries are server-clock artifacts (``now`` and
#       ``now.replace(hour=18)``). This is the one that told PM he had "focus
#       time between 2:09 am and 6:00 pm" — 02:09 being the UTC instant of his
#       own request. Never rendered as user copy.
_EVENT_DERIVED_BLOCK_TYPES = {"between_meetings"}
_SYNTHETIC_BLOCK_TYPES = {"free_block"}


def _format_free_block(
    free_blocks: Optional[List[Dict[str, Any]]],
    user_timezone: Optional[str],
) -> Optional[str]:
    """Render the first free block that can be stated honestly, or None.

    Rule: a clock face is printable only if the reader can tell which clock it
    is on. Event-derived boundaries already carry the calendar's offset;
    server-derived ones need a timezone we can NAME, and are otherwise omitted.
    The general per-user timezone answer is #1572, not this.

    Tense rule (#1615): a window that has already finished is never cited in
    present tense — PM's 12:42 retest greeting said "you have some focus time
    between 9:30 am and 10:00 am", a real block honestly read but long over.
    Unlike the day-part question, this is NOT #1572-gated: every block that
    reaches rendering passed ``_parse_iso`` (naive values rejected), so
    "finished?" is an absolute-instant comparison against ``utc_now()`` — no
    user clock face involved (m-43: elapsed-ness and clock-face rendering are
    different layers). A still-open block is preferred over an elapsed one;
    with only elapsed blocks on offer, the first renders in past tense.
    """
    if not free_blocks:
        return None
    now = utc_now()
    elapsed_fallback: Optional[str] = None

    tz = None
    if user_timezone:
        try:
            from zoneinfo import ZoneInfo

            tz = ZoneInfo(user_timezone)
        except Exception:  # silent-ok: invalid/unknown tz string -> tz=None -> no local clock face is rendered (never a wrong one, #1589); per-turn logging would be noise for a stored bad value
            tz = None

    for block in free_blocks[:2]:
        block_type = block.get("type")
        if block_type in _SYNTHETIC_BLOCK_TYPES:
            continue

        start_dt = _parse_iso(block.get("start_time", ""))
        end_dt = _parse_iso(block.get("end_time", ""))
        if not start_dt or not end_dt:
            continue
        if end_dt <= start_dt:
            # `now.replace(hour=18)` runs backwards past 18:00 server time.
            continue

        if block_type in _EVENT_DERIVED_BLOCK_TYPES:
            start, end = (
                _format_time(block.get("start_time", "")),
                _format_time(block.get("end_time", "")),
            )
        elif tz is not None:
            # Unknown/server-derived, but we can name a zone → convert + label.
            start, end = _format_time_labeled(start_dt, tz), _format_time_labeled(end_dt, tz)
        else:
            continue

        if start and end:
            if end_dt > now:
                return f"I noticed you have some focus time between {start} and {end}"
            if elapsed_fallback is None:
                # Window already finished at render time: past tense, and keep
                # looking — a later still-open block is worth more than this.
                elapsed_fallback = f"I noticed you had some focus time between {start} and {end}"
    return elapsed_fallback


def _parse_iso(time_str: str) -> Optional[datetime]:
    """Parse an ISO timestamp, or None. Naive values are rejected: without an
    offset there is no way to say which clock they belong to, and guessing is
    exactly the failure this module is fixing."""
    if not time_str or "T" not in str(time_str):
        return None
    try:
        parsed = datetime.fromisoformat(str(time_str).replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return parsed if parsed.tzinfo is not None else None


def _format_time_labeled(dt: datetime, tz) -> str:
    """Clock face in ``tz``, WITH the zone abbreviation attached."""
    local = dt.astimezone(tz)
    label = local.strftime("%Z") or str(tz)
    return f"{local.strftime('%I:%M %p').lstrip('0').lower()} {label}"


def _format_time(time_str: str) -> str:
    """Format time string to readable format.

    Only for provider-supplied event times, which carry the event's own offset
    (so the clock face is already the reader's). Never use this on a
    server-clock-derived instant — see ``_format_free_block``.
    """
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
