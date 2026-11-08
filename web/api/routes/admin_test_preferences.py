"""#2325: reset one stored preference on one named TEST account, so a served check of a
one-shot preference (the clear verb's first-time question) doesn't burn an account.

Arch's mechanism (decisions.log 2026-11-07 18:03, #955/#2325): one deletion path,
``verified_inference.forget_verified_inference``, with this route as its admin caller.
#955's person-facing forget is the other caller, with its own gate. Gates here, all
checked before anything is written:

* ``require_admin`` (users.is_admin, live DB read, fail closed; #1485's dependency).
* The account must be on ``TEST_ACCOUNT_USERNAMES``, a list held in code so adding an
  account is a reviewed commit. A real person's account can never be reset here.
* The key must be one this route is allowed to forget (``FORGETTABLE_KEY_PREFIXES``).
* One audit row per call, with the outcome, the account and the key (never the value).

Never user-facing: no page links to it.
"""

from __future__ import annotations

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.auth.auth_middleware import require_admin
from services.auth.jwt_service import JWTClaims
from services.intent_service.verified_inference import ForgetOutcome, forget_verified_inference

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/admin/test-preferences", tags=["admin"])

# The cohort's alpha test accounts (Web's and PA's served-check accounts). An account
# not named here is refused, whatever the admin asks.
TEST_ACCOUNT_USERNAMES = frozenset(
    {
        "web-seed-1386",
        "web-fresh-test",
        "web-pat-test",
        "web-oauth-test",
        "web-agent",
    }
)

# The one-shot verb preferences (reminder_clear.inference_key). Other stored inferences
# are refused until someone needs them reset and says so.
FORGETTABLE_KEY_PREFIXES = ("reminder_clear_verb:",)

AUDIT_ACTION = "test_preference_forgotten"


class ForgetRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=255)
    key: str = Field(..., min_length=1, max_length=255)


class ForgetResponse(BaseModel):
    username: str
    key: str
    outcome: str


async def _user_id_for(username: str) -> Optional[str]:
    from sqlalchemy import select

    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        row = await session.execute(select(User.id).where(User.username == username))
        found = row.scalar_one_or_none()
    return str(found) if found is not None else None


async def _write_audit(*, actor_user_id, username: str, key: str, outcome: str) -> None:
    """One audit row through the shared ``AuditLogger``. Best effort, like the invites
    route: a failed audit write is logged and doesn't undo the reset."""
    from services.database.session_factory import AsyncSessionFactory
    from services.security.audit_logger import audit_logger

    try:
        async with AsyncSessionFactory.session_scope() as session:
            await audit_logger.log_event(
                event_type="admin",
                action=AUDIT_ACTION,
                status="success" if outcome != ForgetOutcome.FAILED.value else "failed",
                severity="info",
                message=f"test preference reset: {username} {key} -> {outcome}",
                session=session,
                user_id=actor_user_id,
                resource_type="user_preference",
                resource_id=key,
                details={"username": username, "key": key, "outcome": outcome},
            )
    except Exception as exc:  # silent-ok: logged; the audit row must not undo the admin's act
        logger.error(
            "test_preference_audit_write_failed", username=username, key=key, error=str(exc)
        )


@router.post("/forget", response_model=ForgetResponse)
async def forget_test_preference(
    body: ForgetRequest, admin: JWTClaims = Depends(require_admin)
) -> ForgetResponse:
    if body.username not in TEST_ACCOUNT_USERNAMES:
        raise HTTPException(status_code=403, detail="Only a listed test account can be reset.")
    if not body.key.startswith(FORGETTABLE_KEY_PREFIXES):
        raise HTTPException(status_code=422, detail="That preference can't be reset here.")
    user_id = await _user_id_for(body.username)
    if user_id is None:
        raise HTTPException(status_code=404, detail="No account with that username.")
    result = await forget_verified_inference(user_id, body.key)
    await _write_audit(
        actor_user_id=admin.user_id,
        username=body.username,
        key=body.key,
        outcome=result.outcome.value,
    )
    if result.outcome is ForgetOutcome.FAILED:
        raise HTTPException(
            status_code=503, detail="The preference could not be read or written; nothing changed."
        )
    return ForgetResponse(username=body.username, key=body.key, outcome=result.outcome.value)
