"""Per-user timezone supply — Issue #1572 (the deferred half of #747).

The 2026-08-10 time-handling audit found user-tz SUPPLY at 0% (no capture,
no writer, no storage) while the consumption scaffolding was ~80% built.
This module is the supply side, deliberately small:

- **Storage**: one key (``timezone``) in the existing ``users.preferences``
  JSONB column (#1422) — no migration needed, and the collaboration-gate
  (#1510) already established this column as the per-user pref store.
- **Capture**: the login flow (web/api/routes/auth.py) posts the browser's
  ``Intl.DateTimeFormat().resolvedOptions().timeZone`` and writes it here.
- **Consumption**: reminder parse (temporal_utils.parse_reminder_time) and
  reminder/save rendering (todo_handlers) read it via
  :func:`get_user_timezone`.

**Fail-safe direction is load-bearing**: every path here degrades to
``None`` — meaning "no user tz known" — and every consumer treats ``None``
as "keep the pre-#1572 server-clock/UTC-labeled behavior". A storage error
or a bogus tz string must never crash a reminder turn or silently shift an
instant.
"""

from typing import Optional
from zoneinfo import ZoneInfo

import structlog

logger = structlog.get_logger(__name__)

# The users.preferences JSONB key holding the IANA timezone name.
TIMEZONE_PREF_KEY = "timezone"


def is_valid_iana_timezone(tz_name) -> bool:
    """True only for a string naming a real IANA zone ("America/Los_Angeles")."""
    if not tz_name or not isinstance(tz_name, str):
        return False
    try:
        ZoneInfo(tz_name)
        return True
    except Exception:  # silent-ok: validation predicate — any failure (KeyError, ValueError, ZoneInfoNotFoundError) IS the False answer
        return False


def resolve_zone(tz_name) -> Optional[ZoneInfo]:
    """A ZoneInfo for a valid IANA name, else None (never raises)."""
    if not tz_name or not isinstance(tz_name, str):
        return None
    try:
        return ZoneInfo(tz_name)
    except Exception:  # silent-ok: fail-safe direction — an unresolvable tz means "unknown", consumers keep UTC behavior
        return None


async def get_user_timezone(user_id) -> Optional[str]:
    """The user's stored IANA timezone, or None when unknown.

    Reads ``users.preferences[TIMEZONE_PREF_KEY]``. Returns None on any
    failure — absent user, absent key, invalid stored value, DB
    unavailable — so consumers keep the pre-#1572 behavior.
    """
    if not user_id:
        return None
    try:
        from sqlalchemy import select

        from services.database.connection import db
        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory

        if not db._initialized:
            await db.initialize()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            row = await session.execute(
                select(User.preferences).where(User.id == str(user_id))
            )
            prefs = row.scalar_one_or_none() or {}
        tz_name = prefs.get(TIMEZONE_PREF_KEY)
        if is_valid_iana_timezone(tz_name):
            return tz_name
        return None
    except Exception as e:  # silent-ok: fail-safe direction is the point (#1572) — a storage error degrades to server-clock behavior, never crashes a reminder turn; logged WARNING
        logger.warning("user_timezone_read_failed", user_id=str(user_id), error=str(e))
        return None


async def save_user_timezone(user_id, tz_name) -> bool:
    """Validated write of the user's IANA timezone into users.preferences.

    False (never an exception) when the tz is invalid, the user row is
    absent, or storage fails — callers (the login flow) must never block on
    this.
    """
    if not user_id or not is_valid_iana_timezone(tz_name):
        return False
    try:
        from sqlalchemy import select

        from services.database.connection import db
        from services.database.models import User
        from services.database.session_factory import AsyncSessionFactory

        if not db._initialized:
            await db.initialize()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(select(User).where(User.id == str(user_id)))
            user = result.scalar_one_or_none()
            if user is None:
                return False
            # New dict on purpose: reassignment is what marks the JSONB
            # column dirty; in-place mutation can silently not persist
            # (same rationale as collaboration_gate._save_preference).
            prefs = dict(user.preferences or {})
            if prefs.get(TIMEZONE_PREF_KEY) == tz_name:
                return True  # already current — skip the write
            prefs[TIMEZONE_PREF_KEY] = tz_name
            user.preferences = prefs
            await session.commit()
            return True
    except Exception as e:  # silent-ok: capture is best-effort (#1572) — login must succeed with or without a tz write; logged WARNING
        logger.warning("user_timezone_write_failed", user_id=str(user_id), error=str(e))
        return False
