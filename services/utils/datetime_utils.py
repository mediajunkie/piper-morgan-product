"""
Timezone-aware datetime utilities.

Issue #750 (child of #747 - Timezone Support)

This module provides timezone-aware datetime functions to replace deprecated
datetime.now(timezone.utc) throughout the codebase. All functions return UTC timezone-aware
datetimes to ensure consistent behavior.

Usage:
    from services.utils.datetime_utils import utc_now, ensure_utc, is_timezone_aware

    # Get current UTC time (replaces datetime.now(timezone.utc))
    now = utc_now()

    # Convert naive datetime to UTC-aware
    aware_dt = ensure_utc(naive_dt)

    # Check if datetime is timezone-aware
    if is_timezone_aware(dt):
        ...

For SQLAlchemy column defaults:
    from services.utils.datetime_utils import utc_now

    created_at = Column(DateTime(timezone=True), default=utc_now)

#1576 (time-handling audit F2) adds the *render* half: one shared way to turn an
instant into a user-facing clock FACE. See the "User-facing clock faces" section
at the bottom of this module.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Optional, overload

logger = logging.getLogger(__name__)


def utc_now() -> datetime:
    """
    Return the current UTC time as a timezone-aware datetime.

    This is the recommended replacement for datetime.now(timezone.utc), which is
    deprecated and scheduled for removal in Python 3.14.

    Returns:
        datetime: Current time with UTC timezone info.

    Example:
        >>> now = utc_now()
        >>> now.tzinfo == timezone.utc
        True
    """
    return datetime.now(timezone.utc)


def utc_now_naive() -> datetime:
    """
    Return the current UTC time as a naive datetime (no timezone info).

    Use this when comparing with database timestamps that are returned as naive
    datetimes but represent UTC values. This is common with PostgreSQL
    TIMESTAMP WITH TIME ZONE columns when using SQLAlchemy/asyncpg.

    Issue #768: Fixes timezone mismatch where datetime.now() (local time) was
    compared with database values (UTC), causing negative age calculations.

    Returns:
        datetime: Current UTC time without timezone info.

    Example:
        >>> now = utc_now_naive()
        >>> now.tzinfo is None
        True
        >>> # Safe to compare with database values
        >>> age = now - record.upload_time  # Both are naive UTC
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


# #1797 rider (2026-09-22): overloads so a non-Optional datetime stays
# non-Optional through the call — the Optional-in/Optional-out signature was
# manufacturing [operator] noise (`x - now` on a value that provably can't be
# None) at call sites that never pass None. Zero runtime change.
@overload
def ensure_utc(dt: datetime) -> datetime: ...
@overload
def ensure_utc(dt: None) -> None: ...
def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Ensure a datetime is timezone-aware in UTC.

    - If dt is None, returns None
    - If dt is naive (no timezone), assumes it's UTC and adds timezone info
    - If dt is already UTC-aware, returns unchanged
    - If dt has a different timezone, converts to UTC

    Args:
        dt: A datetime object (naive or aware) or None.

    Returns:
        datetime or None: The datetime in UTC, or None if input was None.

    Example:
        >>> naive = datetime(2026, 1, 15, 12, 0, 0)
        >>> aware = ensure_utc(naive)
        >>> aware.tzinfo == timezone.utc
        True
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # Naive datetime - assume it's UTC and add timezone info
        return dt.replace(tzinfo=timezone.utc)

    if dt.tzinfo == timezone.utc:
        # Already UTC - return as-is
        return dt

    # Has a different timezone - convert to UTC
    return dt.astimezone(timezone.utc)


def ensure_utc_naive(dt: Optional[datetime]) -> Optional[datetime]:
    """
    Ensure a datetime is naive and represents UTC.

    Use this when you need to compare a datetime (that may or may not have
    timezone info) with other naive UTC datetimes, such as those from
    utc_now_naive() or database queries.

    - If dt is None, returns None
    - If dt is naive, assumes it's already UTC (as from database) and returns as-is
    - If dt is timezone-aware, converts to UTC and strips timezone info

    Issue #768: Use this with database timestamps to ensure consistent comparison.

    Args:
        dt: A datetime object (naive or aware) or None.

    Returns:
        datetime or None: Naive datetime in UTC, or None if input was None.

    Example:
        >>> from services.utils.datetime_utils import utc_now_naive, ensure_utc_naive
        >>> age = utc_now_naive() - ensure_utc_naive(record.upload_time)
    """
    if dt is None:
        return None

    if dt.tzinfo is None:
        # Naive datetime - assume it's already UTC (from database)
        return dt

    # Has timezone info - convert to UTC and strip tzinfo
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


def is_timezone_aware(dt: Optional[datetime]) -> bool:
    """
    Check if a datetime object is timezone-aware.

    Args:
        dt: A datetime object or None.

    Returns:
        bool: True if dt has timezone info, False if naive or None.

    Example:
        >>> naive = datetime(2026, 1, 15, 12, 0, 0)
        >>> is_timezone_aware(naive)
        False
        >>> aware = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
        >>> is_timezone_aware(aware)
        True
    """
    if dt is None:
        return False
    return dt.tzinfo is not None


# ===========================================================================
# User-facing clock faces (#1576 — time-handling audit F2, 2026-08-10)
# ===========================================================================
#
# The audit found 27 of 50 user-visible datetime renders wrong or unreadable:
# 13 showed the SERVER's clock with no zone label (UTC on Fly, so a PT user
# read a face seven hours off and had no way to know), 10 printed raw ISO
# ("2026-08-08T15:00:00+00:00") straight into prose.
#
# The pattern that already works on 23 of the 50 — and the one everything
# converges on — is: **the server emits an AWARE ISO instant, the browser
# renders it with `toLocale*`.** The browser knows the viewer's zone; the
# server does not have to guess.
#
# Where no browser exists — Slack text, chat prose, a plain-text export — the
# face has to be rendered here, and then it carries an explicit zone label
# built from the user's stored timezone (#1574). Two rules, from #1381's
# `_current_time_for_user`, generalized:
#
#   1. Never a BARE clock face. "4:27 PM" is unfalsifiable; "4:27 PM PDT" is
#      checkable by the person reading it.
#   2. When the user's zone is unknown, fall back to UTC and SAY "UTC" —
#      an honest wrong-for-you face beats a silent wrong-for-you face.

DEFAULT_USER_TIMEZONE = "America/Los_Angeles"

# The face an all-day event shows where a clock time would go. Not empty: an
# empty face reads as a broken render, not a choice (CXO ruling 2026-09-23).
ALL_DAY_FACE = "All day"


def _zone(tz_name: Optional[str]):
    """Resolve an IANA name to a tzinfo, degrading to UTC on anything unusable.

    Deliberately total: a render must not raise because a preference row holds
    a typo. The label follows the zone actually used, so a degrade is visible
    in the face itself rather than silent.
    """
    from zoneinfo import ZoneInfo

    if not tz_name:
        return timezone.utc
    try:
        return ZoneInfo(tz_name)
    except Exception:
        logger.warning("unusable_timezone_name_falling_back_to_utc name=%s", tz_name)
        return timezone.utc


async def user_timezone_name(user_id: Optional[Any]) -> str:
    """The IANA zone a user-facing face must be rendered in.

    THE getter — the same #1574 store the calendar adapter reads
    (`UserPreferenceManager.get_reminder_timezone`), so a face and the
    day-boundary math behind it can never disagree about which clock the user
    is on. Anonymous / unknown / lookup failure → the preference layer's own
    default (that default is #1572's open question, not this function's).
    """
    if user_id:
        try:
            from uuid import UUID

            from services.domain.user_preference_manager import UserPreferenceManager

            return await UserPreferenceManager().get_reminder_timezone(UUID(str(user_id)))
        except (
            Exception
        ) as e:  # silent-ok: a face still renders, labeled with the zone it actually used
            logger.warning("user_timezone_lookup_failed user_id=%s error=%s", user_id, e)
    return DEFAULT_USER_TIMEZONE


def now_in_zone(tz_name: Optional[str]) -> datetime:
    """The current instant, expressed on the named clock (UTC if unusable).

    For surfaces that render "what time is it for *you* right now" rather than
    formatting a stored instant.
    """
    return datetime.now(_zone(tz_name))


def to_user_tz(dt: datetime, tz_name: Optional[str]) -> datetime:
    """Same instant, expressed on the user's clock. Naive input is read as UTC."""
    return ensure_utc(dt).astimezone(_zone(tz_name))


def zone_label(dt: datetime) -> str:
    """The zone abbreviation for an aware datetime — 'PDT', 'PST', 'UTC'.

    `%Z` rather than a static IANA→abbreviation table because the table cannot
    know about DST: a table saying "PT" is correct year-round and precise
    never, and the whole point of the label is that the reader can check it.
    """
    return dt.strftime("%Z") or "UTC"


def format_user_time(dt: datetime, tz_name: Optional[str]) -> str:
    """A labeled clock face on the user's clock — ``'9:41 AM PDT'``."""
    local = to_user_tz(dt, tz_name)
    return f"{local.strftime('%I:%M %p').lstrip('0')} {zone_label(local)}"


def format_user_datetime(dt: datetime, tz_name: Optional[str]) -> str:
    """A labeled date+time face on the user's clock — ``'2026-09-23 9:41 AM PDT'``."""
    local = to_user_tz(dt, tz_name)
    return f"{local.strftime('%Y-%m-%d')} {format_user_time(local, tz_name)}"


def _parse_iso(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def format_iso_as_user_time(value: Any, tz_name: Optional[str]) -> Optional[str]:
    """Parse an ISO-8601 instant and return its labeled face, or None.

    Returns None — never the input string — when the value is missing or
    unparseable. A caller that falls back to printing `value` would put the
    raw ISO back on the screen, which is the defect this exists to remove;
    None forces the caller to choose an honest alternative instead.
    """
    parsed = _parse_iso(value)
    return format_user_time(parsed, tz_name) if parsed else None


def format_iso_as_user_datetime(value: Any, tz_name: Optional[str]) -> Optional[str]:
    """Date+time twin of `format_iso_as_user_time` — ``'2026-09-23 9:41 AM PDT'`` or None."""
    parsed = _parse_iso(value)
    return format_user_datetime(parsed, tz_name) if parsed else None
