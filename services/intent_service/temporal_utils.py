"""
Temporal extraction utilities for calendar queries and reminders.

Issue #588: Pragmatic approach to parsing relative date modifiers
(today, tomorrow, this week, next week) without over-engineering.

Issue #903: Added parse_reminder_time() for natural language reminder dates.

Future: MUX LLM integration will handle complex natural language dates.
"""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple


def parse_relative_date(
    message: str, user_timezone: Optional[str] = None
) -> Tuple[datetime, datetime, str]:
    """
    Extract date range from message with temporal modifiers.

    Supports: today, tomorrow, this week, next week
    Default: today (if no modifier found)

    Args:
        message: User message to parse
        user_timezone: Optional timezone string (e.g., "America/Los_Angeles")
                      If not provided, uses local system time

    Returns:
        Tuple of (start_date, end_date, label)
        - start_date: Beginning of date range (midnight local time, converted to UTC)
        - end_date: End of date range (midnight next day, converted to UTC)
        - label: Human-readable label ("today", "tomorrow", etc.)
    """
    message_lower = message.lower()

    # Get current time in user's timezone (or local if not specified)
    # Issue #588: Use local time for "today" calculation, then convert to UTC for API
    # #1493: AWARE local time — the naive value stored to timestamptz drifted
    # by the server's UTC offset (asyncpg interprets naive as UTC). Local
    # wall-clock semantics are unchanged; the value now carries its offset so
    # storage is UTC-normalized. Per-user timezones are the #747/#750 family.
    now = datetime.now().astimezone()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Check for "tomorrow" first (more specific than "today")
    if "tomorrow" in message_lower:
        start = today_start + timedelta(days=1)
        end = start + timedelta(days=1)
        return (start, end, "tomorrow")

    # "next week" - Monday to Sunday of next week
    if "next week" in message_lower:
        days_until_monday = (7 - today_start.weekday()) % 7 or 7
        start = today_start + timedelta(days=days_until_monday)
        end = start + timedelta(days=7)
        return (start, end, "next week")

    # "this week" - Monday to Sunday of current week
    if "this week" in message_lower:
        start = today_start - timedelta(days=today_start.weekday())
        end = start + timedelta(days=7)
        return (start, end, "this week")

    # Default: today
    return (today_start, today_start + timedelta(days=1), "today")


def parse_reminder_time(message: str) -> Tuple[Optional[datetime], str]:
    """
    Issue #903: Extract a reminder datetime from natural language.

    Parses time expressions commonly used with "remind me to X" messages.
    Returns the parsed datetime and a human-readable label.

    Supported formats:
    - "tomorrow" / "tomorrow morning" / "tomorrow at 3pm"
    - "in N minutes/hours/days"
    - "this afternoon" / "this evening" / "tonight"
    - "next week" / "next Monday" / "next Tuesday" etc.
    - "today at 3pm" / "at 5pm"
    - Falls back to "tomorrow morning" (9 AM) if no time detected

    Args:
        message: The user's full message

    Returns:
        Tuple of (reminder_datetime, human_label)
        - reminder_datetime: When the reminder should fire (None if unparseable)
        - human_label: Human-readable description of the time
    """
    message_lower = message.lower()
    # #1493: AWARE local time (see parse_relative_date) — "tomorrow at 3pm"
    # still means 3pm server-local, but the stored timestamptz instant is now
    # unambiguous instead of drifting by the UTC offset.
    now = datetime.now().astimezone()

    # --- "in N minutes/hours/days" ---
    in_match = re.search(
        r"\bin\s+(\d+)\s+(minute|minutes|min|mins|hour|hours|hr|hrs|day|days)\b",
        message_lower,
    )
    if in_match:
        amount = int(in_match.group(1))
        unit = in_match.group(2)
        if unit.startswith("min"):
            dt = now + timedelta(minutes=amount)
            label = f"in {amount} minute{'s' if amount != 1 else ''}"
        elif unit.startswith("hr") or unit.startswith("hour"):
            dt = now + timedelta(hours=amount)
            label = f"in {amount} hour{'s' if amount != 1 else ''}"
        else:
            dt = now + timedelta(days=amount)
            label = f"in {amount} day{'s' if amount != 1 else ''}"
        return (dt, label)

    # --- "tomorrow at Xpm/am" ---
    tomorrow_at = re.search(
        r"\btomorrow\s+(?:at\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b",
        message_lower,
    )
    if tomorrow_at:
        hour = int(tomorrow_at.group(1))
        minute = int(tomorrow_at.group(2) or 0)
        ampm = tomorrow_at.group(3)
        if ampm == "pm" and hour < 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        elif not ampm and hour < 8:
            # Assume PM for small numbers without AM/PM ("tomorrow at 3")
            hour += 12
        tomorrow = now + timedelta(days=1)
        dt = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        # Issue #1490: the matched fragment may already contain "at" ("tomorrow
        # at 3pm"), so strip it before the f-string re-adds it — otherwise the
        # confirmation copy reads "tomorrow at at 3pm".
        time_part = tomorrow_at.group(0).split("tomorrow", 1)[1].strip()
        time_part = re.sub(r"^at\s+", "", time_part)
        return (dt, f"tomorrow at {time_part}")

    # --- "tomorrow morning/afternoon/evening" ---
    if "tomorrow" in message_lower:
        tomorrow = now + timedelta(days=1)
        if "afternoon" in message_lower:
            dt = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
            return (dt, "tomorrow afternoon")
        elif "evening" in message_lower:
            dt = tomorrow.replace(hour=18, minute=0, second=0, microsecond=0)
            return (dt, "tomorrow evening")
        else:
            # Default: tomorrow morning at 9 AM
            dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
            return (dt, "tomorrow morning")

    # --- "today at Xpm/am" or "at Xpm" ---
    at_time = re.search(
        r"\b(?:today\s+)?at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b",
        message_lower,
    )
    if at_time:
        hour = int(at_time.group(1))
        minute = int(at_time.group(2) or 0)
        ampm = at_time.group(3)
        if ampm == "pm" and hour < 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
        elif not ampm and hour < 8:
            hour += 12
        dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        # If the time is already past, push to tomorrow
        if dt <= now:
            dt += timedelta(days=1)
        # Issue #1490: group(0) already contains "at" (and possibly "today"),
        # so strip both before the f-string re-adds "at " — avoids "at at 5pm".
        time_part = re.sub(r"^(?:today\s+)?at\s+", "", at_time.group(0).strip())
        return (dt, f"at {time_part}")

    # --- "this afternoon/evening/tonight" ---
    if "this afternoon" in message_lower:
        dt = now.replace(hour=14, minute=0, second=0, microsecond=0)
        if dt <= now:
            dt += timedelta(days=1)
        return (dt, "this afternoon")
    if "this evening" in message_lower or "tonight" in message_lower:
        dt = now.replace(hour=18, minute=0, second=0, microsecond=0)
        if dt <= now:
            dt += timedelta(days=1)
        return (dt, "this evening")

    # --- "next week" ---
    if "next week" in message_lower:
        days_until_monday = (7 - now.weekday()) % 7 or 7
        dt = (now + timedelta(days=days_until_monday)).replace(
            hour=9, minute=0, second=0, microsecond=0
        )
        return (dt, "next week")

    # --- Day names: "next Monday", "on Tuesday", etc. ---
    day_names = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    day_match = re.search(
        r"\b(?:next|on)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        message_lower,
    )
    if day_match:
        target_day = day_names[day_match.group(1)]
        days_ahead = (target_day - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7  # "next Monday" when it's Monday → next week
        dt = (now + timedelta(days=days_ahead)).replace(hour=9, minute=0, second=0, microsecond=0)
        return (dt, f"next {day_match.group(1).capitalize()}")

    # --- Fallback: tomorrow morning at 9 AM ---
    tomorrow = now + timedelta(days=1)
    dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    return (dt, "tomorrow morning")
