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
"""

from datetime import datetime, timezone
from typing import Optional, overload


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
