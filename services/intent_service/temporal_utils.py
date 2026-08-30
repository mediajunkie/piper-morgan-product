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


def _anchor_now(user_timezone: Optional[str] = None) -> datetime:
    """#1572: the ONE parse anchor. With a valid IANA tz, "now" is the
    USER'S wall clock — so "4pm today" typed at 1:49 PM Pacific is 2+ hours
    in the future, not 4 hours in the past on the server's UTC clock (audit
    F1/F4). Without one (or with an invalid one), the pre-#1572 aware
    server-local anchor is kept unchanged (fail-safe: unknown tz → existing
    behavior; see #1493 for why the anchor is aware either way)."""
    if user_timezone:
        try:
            from zoneinfo import ZoneInfo

            return datetime.now(ZoneInfo(user_timezone))
        except Exception:  # silent-ok: fail-safe direction (#1572) — an unresolvable tz degrades to the server anchor, never crashes a parse
            pass
    return datetime.now().astimezone()


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
    # storage is UTC-normalized.
    # #1572: user_timezone is LIVE (the 2026-08-10 audit found it dead —
    # body never read it). When supplied, "today" is the user's calendar
    # day; when absent, the server anchor is unchanged.
    now = _anchor_now(user_timezone)
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


# --- Issue #1542 (#1490 invariant deepening): explicit-duration finder ---
# "remind me to stretch in two hours" saved for TOMORROW 9AM: the "in N
# units" branch matched digits only, so word-form numbers fell through to
# the vague-time default — a silent replacement of an explicit duration,
# the same class #1490 bans for clock times. Mirrors the
# find_explicit_clock_time architecture: one shared pattern, one finder,
# consumed by both the parser (below) and the slot layer
# (todo_handlers._TIME_EXPR imports DURATION_NUMBER_SRC so the two can't
# drift).
_NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}

# NON-capturing, longest-first (so "seven" can't pre-empt "seventeen"):
# todo_handlers embeds this inside slot patterns that rely on group(1)
# indexing, so introducing a capturing group here would silently break them.
DURATION_NUMBER_SRC = r"(?:\d+|" + "|".join(sorted(_NUMBER_WORDS, key=len, reverse=True)) + r")"

_DURATION_RE = re.compile(
    rf"\bin\s+(?P<amount>{DURATION_NUMBER_SRC})\s+"
    r"(?P<unit>minute|minutes|min|mins|hour|hours|hr|hrs|day|days)\b"
)


def find_explicit_duration(message_lower: str) -> Optional[Tuple[timedelta, str]]:
    """Issue #1542: locate an explicit relative duration anywhere in the
    message — "in 2 hours", "in two hours", "in an hour", "in ten minutes",
    "in three days".

    Digit and word-form numbers (a/an, one through twenty) bind identically,
    so a word-form duration is never silently replaced by the vague-time
    default (the #1490 invariant, deepened to durations). Returns None when
    the message carries no explicit duration; otherwise (timedelta, label).
    """
    match = _DURATION_RE.search(message_lower)
    if not match:
        return None
    token = match.group("amount")
    amount = int(token) if token.isdigit() else _NUMBER_WORDS[token]
    unit = match.group("unit")
    if unit.startswith("min"):
        delta = timedelta(minutes=amount)
        label = f"in {amount} minute{'s' if amount != 1 else ''}"
    elif unit.startswith("hr") or unit.startswith("hour"):
        delta = timedelta(hours=amount)
        label = f"in {amount} hour{'s' if amount != 1 else ''}"
    else:
        delta = timedelta(days=amount)
        label = f"in {amount} day{'s' if amount != 1 else ''}"
    return (delta, label)


# --- Issue #1562: "today" is an explicit DAY WORD ---
# Sentinel prefix for the honest-ask label when an explicit "today" + clock
# time has already passed on the server clock. parse_reminder_time returns
# (None, PAST_TODAY_PREFIX + time_label); todo_handlers recognizes the prefix
# and asks "did you mean tomorrow?" instead of silently rolling the date.
PAST_TODAY_PREFIX = "past-today:"

# "today" as a day word — excludes the possessive ("send today's report" is
# task text, not a time expression).
_TODAY_WORD_RE = re.compile(r"\btoday\b(?!['’]s)")


def parse_reminder_time(
    message: str, user_timezone: Optional[str] = None
) -> Tuple[Optional[datetime], str]:
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
        user_timezone: #1572 — optional IANA tz name. When valid, every
            wall-clock expression ("4pm today", "tomorrow at 9am") and every
            past-check binds on the USER'S clock; the returned datetime is
            aware in that tz (same UTC instant on storage). When absent or
            invalid: the pre-#1572 server anchor, unchanged.

    Returns:
        Tuple of (reminder_datetime, human_label)
        - reminder_datetime: When the reminder should fire (None if unparseable)
        - human_label: Human-readable description of the time
    """
    message_lower = message.lower()
    # #1493: AWARE anchor (see parse_relative_date) — the stored timestamptz
    # instant is unambiguous. #1572: anchored on the user's clock when known.
    now = _anchor_now(user_timezone)

    # Issue #1490 invariant: find any explicit clock time up front so every
    # date-word branch below can bind it, whichever side of the date it sits
    # on ("tomorrow at 3pm" AND "at 3pm tomorrow"). If the mention is
    # explicit but unbindable, return (None, raw-echo) — the handler asks
    # instead of guessing a default.
    raw_clock = find_explicit_clock_time(message_lower)
    # #1436: rebind with the unbindable case structurally excluded, so every
    # branch below gets (int, int, str) — the guard here already enforced
    # this at runtime; the locals make the invariant visible to type checkers.
    clock: Optional[Tuple[int, int, str]] = None
    if raw_clock is not None:
        clock_hour, clock_minute = raw_clock[0], raw_clock[1]
        if clock_hour is None or clock_minute is None:
            return (None, raw_clock[2])
        clock = (clock_hour, clock_minute, raw_clock[2])

    # --- "in N minutes/hours/days" — digit or word-form N (#1542) ---
    duration = find_explicit_duration(message_lower)
    if duration is not None:
        delta, label = duration
        return (now + delta, label)

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
            dt = tomorrow.replace(hour=clock[0], minute=clock[1], second=0, microsecond=0)
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

    # --- "today" + explicit clock: "remind me at 9:41am today ..." (#1562) ---
    # PM live 8/10 (07:16 PT): this stored TOMORROW 9:41 — the branch below
    # claimed "today at 9:41" as its case but had no today handling, so its
    # past-roll silently overrode the explicit day word. And the past-check
    # runs on the ANCHOR clock. Never-default (#1490 family): an explicit
    # "today" binds TODAY; if the time HAS passed on the anchor clock,
    # return the honest-ask shape (None, PAST_TODAY_PREFIX + label) so the
    # handler asks "did you mean tomorrow?" — NEVER a silent roll.
    # #1572: with a stored user tz the anchor IS the user's clock, so the
    # false "already passed" refusal (PM refused '4 PM today' at 1:49 PM
    # Pacific because 16:00 < 20:49 UTC) is gone; without one, the
    # server-clock limitation remains, unchanged.
    has_today = _TODAY_WORD_RE.search(message_lower) is not None
    if has_today and clock is not None:
        dt = now.replace(hour=clock[0], minute=clock[1], second=0, microsecond=0)
        if dt <= now:
            return (None, f"{PAST_TODAY_PREFIX}{clock[2]}")
        return (dt, f"today at {clock[2]}")

    # --- explicit clock time with no date word: "at 5pm", "at noon"
    # (Issue #1490: was an "at"-adjacent regex; now the shared finder, so
    # noon/midnight and bare "3pm" forms bind too). No day word, so the
    # next-occurrence roll-forward is legitimate here (#1562 keeps it). ---
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

    # --- bare "today" with no bindable clock (#1562) ---
    # "remind me today to X" used to fall through to the tomorrow-morning
    # default below — the same silent day-word override in vague form. Ask
    # instead (the handler's None-branch echoes "today" and asks for a time).
    if has_today:
        return (None, "today")

    # --- Fallback: tomorrow morning at 9 AM ---
    tomorrow = now + timedelta(days=1)
    dt = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    return (dt, "tomorrow morning")
