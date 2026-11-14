"""Narrow account flags an admin may set on one named account (#2327, #2361).

Arch's ruling (2026-11-14): ONE admin-only control for the narrow flags, a closed
list in code. A narrow flag opens exactly one thing and never anything more:

- ``ops_reader``: the read-only operations counters (``require_ops_reader``).

``is_admin`` is not a narrow flag and can never be set from here (pinned). #2361
adds ``can_pause_admission`` to this list when it is built; nothing else changes.

HOST's custody: a flag is set on a named account by an admin, and every change is
written as one evidence line (the flag, the account id, on or off, the acting
admin's id; no usernames), which is the served source of HOST's record.

The account is named by USERNAME, matched exactly as sign-in matches a username
(``User.username == value``; never an email fallback, never a near match). A name
that matches no account changes nothing.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import structlog
from sqlalchemy import select

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.logging.evidence import evidence

logger = structlog.get_logger(__name__)

# The closed list. Order is the order the page shows them.
NARROW_FLAGS: Tuple[str, ...] = ("ops_reader",)


class UnknownFlag(ValueError):
    """The flag is not in the closed list (``is_admin`` included)."""


def _flags_of(user: Any) -> Dict[str, bool]:
    return {flag: bool(getattr(user, flag)) for flag in NARROW_FLAGS}


async def _find(session: Any, username: str) -> Optional[Any]:
    name = (username or "").strip()
    if not name:
        return None
    result = await session.execute(select(User).where(User.username == name).limit(2))
    matches = result.scalars().all()
    return matches[0] if len(matches) == 1 else None


async def read_flags(username: str) -> Optional[Dict[str, Any]]:
    """The account's current narrow flags, or ``None`` when no account has exactly
    that username."""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        user = await _find(session, username)
        if user is None:
            return None
        return {"username": user.username, "flags": _flags_of(user)}


async def set_flag(username: str, flag: str, on: bool, admin_id: Any) -> Optional[Dict[str, Any]]:
    """Turn one narrow flag on or off for the account with exactly this username.
    ``None`` when no such account (nothing is changed). Raises ``UnknownFlag`` for
    anything outside the closed list. Writes one evidence line per real change."""
    if flag not in NARROW_FLAGS:
        raise UnknownFlag(flag)
    async with AsyncSessionFactory.session_scope_fresh() as session:
        user = await _find(session, username)
        if user is None:
            return None
        before = bool(getattr(user, flag))
        changed = before != bool(on)
        if changed:
            setattr(user, flag, bool(on))
            await session.commit()
            # A literal name: the evidence pin reads call sites for listed literals.
            evidence(
                "account_narrow_flag_changed",
                flag=flag,
                account_id=str(user.id),
                on=bool(on),
                admin_id=str(admin_id),
            )
        return {"username": user.username, "flags": _flags_of(user), "changed": changed}
