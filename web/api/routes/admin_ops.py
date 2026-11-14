"""Operations reads and the narrow-flag control (#2327).

Two gates, on purpose:

- ``GET /api/v1/admin/floored-actions`` is behind ``require_ops_reader`` (an admin,
  or an account holding the narrow ``users.ops_reader`` flag). It is the ONLY route
  that uses that gate (pinned). It returns read-only aggregate counts and nothing
  about any person.
- ``/api/v1/admin/account-flags`` (read and set) is behind ``require_admin``. It is
  how an admin gives one named account a narrow flag, with no SQL at anyone's hand.
  The set of flags is a closed list in ``services/auth/narrow_flags.py``; ``is_admin``
  is not in it and cannot be set here.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select

from services.auth import narrow_flags
from services.auth.auth_middleware import require_admin, require_ops_reader
from services.auth.jwt_service import JWTClaims
from services.database.models import FlooredActionCountDB
from services.database.session_factory import AsyncSessionFactory

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["admin-ops"])

FLOORED_ACTIONS_MAX_DAYS = 90
# HOST's content bar: a counter row is exactly these, never a user or a message.
FLOORED_ACTION_ROW_KEYS = ("name", "site", "day", "count")

ACCOUNT_NOT_FOUND_DETAIL = "No account has exactly that username. Nothing was changed."
UNKNOWN_FLAG_DETAIL = "That is not a flag this page can set. Nothing was changed."


@router.get("/floored-actions")
async def floored_actions(
    days: int = 30, reader: JWTClaims = Depends(require_ops_reader)
) -> Dict[str, Any]:
    """#2327: the out-of-vocabulary floored action counter.

    Each row is a name (or ``(withheld)``), the floor site, a UTC day and a count.
    ``window`` is the day range asked for, and ``first_day``/``last_day`` are the
    days that actually hold rows, so "no names" is never read without its window
    (absence must not read as clear: #2335, #2337). Read by
    ``scripts/floored_action_tally.py``.
    """
    span = max(1, min(int(days), FLOORED_ACTIONS_MAX_DAYS))
    today = datetime.now(timezone.utc).date()
    since = today - timedelta(days=span - 1)
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(FlooredActionCountDB)
            .where(FlooredActionCountDB.day >= since)
            .order_by(
                FlooredActionCountDB.day, FlooredActionCountDB.name, FlooredActionCountDB.site
            )
        )
        rows = [
            {"name": r.name, "site": r.site, "day": str(r.day), "count": int(r.count or 0)}
            for r in result.scalars().all()
        ]
    return {
        "window": {"days": span, "since": since.isoformat(), "through": today.isoformat()},
        "first_day": rows[0]["day"] if rows else None,
        "last_day": rows[-1]["day"] if rows else None,
        "row_count": len(rows),
        "rows": rows,
    }


def _not_found() -> Dict[str, Any]:
    """No account has exactly that username. A plain answer, not a 404: the app's
    error handler replaces every 404's words with "It may have been moved or
    deleted", which would be untrue here. Nothing was changed."""
    return {"found": False, "message": ACCOUNT_NOT_FOUND_DETAIL}


class SetFlagRequest(BaseModel):
    username: str
    flag: str
    on: bool


@router.get("/account-flags")
async def read_account_flags(
    username: str, admin: JWTClaims = Depends(require_admin)
) -> Dict[str, Any]:
    """The named account's current narrow flags (admin only), so the admin sees
    what is set before changing anything. The username is matched exactly."""
    found = await narrow_flags.read_flags(username)
    if found is None:
        return _not_found()
    return {"found": True, **found, "settable": list(narrow_flags.NARROW_FLAGS)}


@router.post("/account-flags")
async def set_account_flag(
    req: SetFlagRequest, admin: JWTClaims = Depends(require_admin)
) -> Dict[str, Any]:
    """Turn one narrow flag on or off for one named account (admin only). A flag
    outside the closed list (``is_admin`` included) is refused; a username that
    matches no account changes nothing and says so."""
    try:
        result = await narrow_flags.set_flag(req.username, req.flag, req.on, admin.user_id)
    except narrow_flags.UnknownFlag:
        logger.warning("account_flag_refused_unknown", flag=req.flag, admin_id=str(admin.user_id))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=UNKNOWN_FLAG_DETAIL)
    if result is None:
        return _not_found()
    return {"found": True, **result, "settable": list(narrow_flags.NARROW_FLAGS)}
