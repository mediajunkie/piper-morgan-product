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


# --- Issue #1490 (inverted-order reopen, 8/8): explicit clock-time finder ---
# "remind me at 3pm tomorrow ..." dropped the 3pm: the bare-"tomorrow" branch
# fired before any branch that could see "at 3pm" and silently defaulted to
# 9am. The fix: detect an explicit clock time ANYWHERE in the message up
# front, so every date-word branch can bind it regardless of ordering.
#
# Alternation order matters: noon/midnight first; then "at N(:MM)(am|pm)?"
# ("at" required so durations like "30 minutes" can't match); then bare
# "N(:MM)am/pm" (am/pm required, same reason).
_CLOCK_TIME_RE = re.compile(
    r"\b(?:at\s+)?(?P<word>noon|midnight)\b"
    r"|\bat\s+(?P<h1>\d{1,2})(?::(?P<m1>\d{2}))?\s*(?P<ap1>am|pm)?\b"
    r"|\b(?P<h2>\d{1,2})(?::(?P<m2>\d{2}))?\s*(?P<ap2>am|pm)\b"
)


def _to_24h(hour: int, minute: int, ampm: Optional[str]) -> Optional[Tuple[int, int]]:
    """Convert a matched clock time to 24h, or None when unbindable (#1490).

    Preserves the pre-existing heuristics: 12-hour wrap for am/pm; without
    am/pm, small hours (<8) are assumed PM ("at 3" -> 15:00). Out-of-range
    values (minute > 59, am/pm hour outside 1-12, bare hour > 23) return
    None instead of crashing .replace() or guessing.
    """
    if minute > 59:
        return None
    if ampm:
        if not 1 <= hour <= 12:
            return None
        if ampm == "pm" and hour < 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0
    else:
        if hour > 23:
            return None
        if hour < 8:
            hour += 12
    return (hour, minute)


def find_explicit_clock_time(
    message_lower: str,
) -> Optional[Tuple[Optional[int], Optional[int], str]]:
    """Issue #1490: locate an explicit clock time anywhere in the message.

    Returns None when the message carries no explicit clock time; otherwise
    (hour24, minute, raw_label). hour24/minute are None when the mention is
    explicit but unbindable (e.g. "at 25:99") — the caller must then refuse
    to guess (the #1490 invariant: an explicit time is never silently
    replaced by a default), returning the raw text for an honest echo.
    """
    match = _CLOCK_TIME_RE.search(message_lower)
    if not match:
        return None
    if match.group("word"):
        word = match.group("word")
        return (12 if word == "noon" else 0, 0, word)
    hour = int(match.group("h1") or match.group("h2"))
    minute = int(match.group("m1") or match.group("m2") or 0)
    ampm = match.group("ap1") or match.group("ap2")
    converted = _to_24h(hour, minute, ampm)
    if converted is None:
        return (None, None, match.group(0).strip())
    raw = re.sub(r"^at\s+", "", match.group(0).strip())
    return (converted[0], converted[1], raw)


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

    # Issue #1490 invariant: find any explicit clock time up front so every
    # date-word branch below can bind it, whichever side of the date it sits
    # on ("tomorrow at 3pm" AND "at 3pm tomorrow"). If the mention is
    # explicit but unbindable, return (None, raw-echo) — the handler asks
    # instead of guessing a default.
    clock = find_explicit_clock_time(message_lower)
    if clock is not None and clock[0] is None:
        return (None, clock[2])

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
        converted = _to_24h(
            int(tomorrow_at.group(1)),
            int(tomorrow_at.group(2) or 0),
            tomorrow_at.group(3),
        )
        if converted is None:
            # #1490 invariant: explicit but unbindable ("tomorrow at 25:99")
            # — refuse to guess; pre-fix this crashed .replace(hour=25).
            return (None, tomorrow_at.group(0).strip())
        hour, minute = converted
        tomorrow = now + timedelta(days=1)
        dt = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        # Issue #1490: the matched fragment may already contain "at" ("tomorrow
        # at 3pm"), so strip it before the f-string re-adds it — otherwise the
        # confirmation copy reads "tomorrow at at 3pm".
        time_part = tomorrow_at.group(0).split("tomorrow", 1)[1].strip()
        time_part = re.sub(r"^at\s+", "", time_part)
        return (dt, f"tomorrow at {time_part}")

    # --- "tomorrow" with the time elsewhere, or vague morning/afternoon ---
    if "tomorrow" in message_lower:
        tomorrow = now + timedelta(days=1)
        if clock is not None:
            # Issue #1490 (PM's 8/8 verification): "remind me at 3pm tomorrow"
            # — explicit clock time on the OTHER side of "tomorrow". Pre-fix
            # this fell through to the 9am morning default (prod row saved at
            # 09:00 with copy "tomorrow morning").
            dt = tomorrow.replace(
                hour=clock[0], minute=clock[1], second=0, microsecond=0
            )
            return (dt, f"tomorrow at {clock[2]}")
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

    # --- "next week" (Issue #1490: now clock-aware, checked BEFORE the
    # generic clock branch so "next week at 4pm" binds next week, not today) ---
    if "next week" in message_lower:
        hour, minute = (clock[0], clock[1]) if clock is not None else (9, 0)
        days_until_monday = (7 - now.weekday()) % 7 or 7
        dt = (now + timedelta(days=days_until_monday)).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )
        label = "next week" if clock is None else f"next week at {clock[2]}"
        return (dt, label)

    # --- Day names: "next Monday", "on Tuesday", etc. (Issue #1490: now
    # clock-aware and checked BEFORE the generic clock branch, so "next
    # Monday at 4pm" binds Monday 16:00 instead of today's date) ---
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
        hour, minute = (clock[0], clock[1]) if clock is not None else (9, 0)
        dt = (now + timedelta(days=days_ahead)).replace(
            hour=hour, minute=minute, second=0, microsecond=0
        )
        label = f"next {day_match.group(1).capitalize()}"
        if clock is not None:
            label = f"{label} at {clock[2]}"
        return (dt, label)

    # --- explicit clock time with no date word: "today at 9:41", "at 5pm",
    # "at noon" (Issue #1490: was an "at"-adjacent regex; now the shared
    # finder, so noon/midnight and bare "3pm" forms bind too) ---
    if clock is not None:
        dt = now.replace(hour=clock[0], minute=clock[1], second=0, microsecond=0)
        # If the time is already past, push to tomorrow (next occurrence)
        if dt <= now:
            dt += timedelta(days=1)
        return (dt, f"at {clock[2]}")

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

    # --- Fallback: tomorrow morning at 9 AM ---
    tomorrow = now + timedelta(days=1)
    dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    return (dt, "tomorrow morning")
