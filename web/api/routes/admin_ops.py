"""Operations reads and the narrow-flag control (#2327).

Two gates, on purpose:

- The routes in ``OPS_READER_ROUTES`` are behind ``require_ops_reader`` (an admin, or
  an account holding the narrow ``users.ops_reader`` flag). They are the ONLY routes
  that use that gate: the list is closed and pinned by a test, and a new route is a
  diff HOST reads before it ships (ADR-084 D4 rule 5, issue 2390). Each returns
  read-only aggregate counts and nothing about any person, and each read writes one
  evidence line with the route and the reader and never the response.
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
from sqlalchemy import func, select

from services.auth import narrow_flags
from services.auth.auth_middleware import require_admin, require_ops_reader
from services.auth.jwt_service import JWTClaims
from services.database.models import FlooredActionCountDB, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.logging.evidence import evidence
from services.llm.config import LLMProvider

logger = structlog.get_logger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["admin-ops"])

FLOORED_ACTIONS_MAX_DAYS = 90
# HOST's content bar: a counter row is exactly these, never a user or a message.
FLOORED_ACTION_ROW_KEYS = ("name", "site", "day", "count")

# ADR-084 D4 rule 5 (issue 2390): every route behind ``require_ops_reader``. Closed;
# ``tests/unit/web/api/routes/test_ops_reader_routes_2390.py`` fails if a route joins
# or leaves the gate without this list changing. A change here is a diff HOST reads.
OPS_READER_ROUTES = ("/api/v1/admin/active-keys", "/api/v1/admin/floored-actions")

# The active-keys read names providers from this fixed list only (D4 rule 2). A stored
# row for any other provider is counted under OTHER_PROVIDERS, never by its own name.
KEY_PROVIDERS = tuple(sorted(p.value for p in LLMProvider))
OTHER_PROVIDERS = "other"
ACTIVE_KEYS_ROW_KEYS = ("provider", "active_keys")


def _note_read(route: str, reader: JWTClaims) -> None:
    """D4 rule 4: one line per read, with the route and the reader and nothing the
    route returned. On the evidence logger, so the hosts keep it."""
    evidence("ops_read", route=route, reader=str(reader.user_id))


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
    _note_read("/api/v1/admin/floored-actions", reader)
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


@router.get("/active-keys")
async def active_keys(reader: JWTClaims = Depends(require_ops_reader)) -> Dict[str, Any]:
    """Issue 2390 (ADR-084 D4): how many active provider keys are stored, by provider.

    A fixed query with no parameter. Each row is a provider name from ``KEY_PROVIDERS``
    (or ``other``) and a count; every listed provider has a row, so a zero is said and
    not left out. No id, account, key prefix or time is read or returned.
    """
    _note_read("/api/v1/admin/active-keys", reader)
    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(UserAPIKey.provider, func.count())
            .where(UserAPIKey.is_active.is_(True))
            .group_by(UserAPIKey.provider)
        )
        found = [(str(provider), int(count or 0)) for provider, count in result.all()]
    counts = {name: 0 for name in (*KEY_PROVIDERS, OTHER_PROVIDERS)}
    for provider, count in found:
        counts[provider if provider in KEY_PROVIDERS else OTHER_PROVIDERS] += count
    return {"rows": [{"provider": name, "active_keys": counts[name]} for name in counts]}


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
