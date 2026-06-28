"""Dev-only trust-stage affordance (Issue #1148 UAT-TEST-USER-STAGE).

Provides a small GUI + form-post to set a user's trust stage on demand so UAT
can exercise trust-gated surfaces (``/lists``, ``/documents``, Stage-3+ push
insights per #1032) WITHOUT organically climbing NEW -> TRUSTED across the
~50 successful interactions the ADR-053 thresholds require.

    GET  /api/v1/admin/trust            -> the dev GUI (user + stage picker)
    POST /api/v1/admin/trust/set-stage  -> apply a stage to a user, re-render

SECURITY (Issue #1148 AC#3, sibling of #1149 DEBUG-ROUTE-PROD-EXPOSURE):
This router is DEV-ONLY. Every route 404s when ``PIPER_ENVIRONMENT`` (or the
older ``ENVIRONMENT``) resolves to "production" — see ``require_dev_environment``.
There is no legitimate production use for arbitrarily setting a user's trust
level, so the gate fails toward 404 (the endpoint is invisible in prod, not
merely forbidden). Default environment is "development" (the #1087 pattern),
so the tool works locally with no extra config.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

import structlog
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import UserTrustProfile
from services.repositories.user_trust_profile_repository import (
    UserTrustProfileRepository,
)
from services.shared_types import TrustStage

logger = structlog.get_logger()


def _is_production() -> bool:
    """True only when the environment is explicitly production.

    Mirrors services/auth/jwt_service.py (#1087): PIPER_ENVIRONMENT is canonical,
    ENVIRONMENT is the older fallback, default is "development".
    """
    env = (os.getenv("PIPER_ENVIRONMENT") or os.getenv("ENVIRONMENT") or "development").lower()
    return env == "production"


def require_dev_environment() -> None:
    """Route dependency: hide this dev tool entirely in production.

    Raises 404 (not 403) so production does not even disclose the route exists.
    """
    if _is_production():
        raise HTTPException(status_code=404, detail="Not Found")


router = APIRouter(
    prefix="/api/v1/admin/trust",
    tags=["admin", "dev", "trust"],
    dependencies=[Depends(require_dev_environment)],
)

# Self-contained templates (web/templates/), isolated from the production UI
# tree (repo-root templates/) — the self-contained dev-router templates pattern.
_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))

_STAGE_REASON = "dev affordance (#1148): UAT trust-stage override"


async def _list_active_users(session) -> list[dict]:
    """Active users as [{username, user_id}], username-sorted, for the picker."""
    result = await session.execute(
        select(User.username, User.id).where(User.is_active.is_(True)).order_by(User.username)
    )
    return [{"username": row[0], "user_id": str(row[1])} for row in result.all()]


async def _current_stages(session, user_ids: list[str]) -> dict[str, dict]:
    """Map user_id(str) -> {"value": int, "name": str} for current trust stage.

    A user with no profile is implicitly NEW (matches the repository contract).
    """
    repo = UserTrustProfileRepository(session)
    out: dict[str, dict] = {}
    for uid in user_ids:
        profile = await repo.get_by_user_id(UUID(uid))
        stage = profile.current_stage if profile else TrustStage.NEW
        out[uid] = {"value": int(stage), "name": stage.name}
    return out


async def _force_set_stage(session, user_id: UUID, stage: TrustStage) -> TrustStage:
    """Get-or-create the user's trust profile, then force its stage.

    ``UserTrustProfileRepository.update_stage`` returns None when the user has no
    profile yet, so we first persist a NEW baseline profile, then set the target
    stage. update_stage records stage_history and invalidates the trust cache
    (#984) so the change takes effect on the very next floor query.
    """
    repo = UserTrustProfileRepository(session)
    profile = await repo.get_by_user_id(user_id)
    if profile is None:
        now = datetime.now(timezone.utc)
        await repo.create_or_update(
            UserTrustProfile(
                user_id=user_id,
                current_stage=TrustStage.NEW,
                highest_stage_achieved=TrustStage.NEW,
                successful_count=0,
                neutral_count=0,
                negative_count=0,
                consecutive_negative=0,
                recent_events=[],
                stage_history=[],
                last_interaction_at=now,
                last_stage_change_at=None,
            )
        )
    updated = await repo.update_stage(user_id, stage, reason=_STAGE_REASON)
    return updated.current_stage if updated else stage


def _stage_choices() -> list[dict]:
    """TrustStage options for the form, in ascending order (NEW..TRUSTED)."""
    return [{"value": int(s), "name": s.name} for s in TrustStage]


async def _render(
    request: Request, *, message: str | None = None, error: str | None = None
) -> HTMLResponse:
    """Render the picker with a fresh users/stages snapshot (read-only scope)."""
    async with AsyncSessionFactory.session_scope() as session:
        users = await _list_active_users(session)
        stages = await _current_stages(session, [u["user_id"] for u in users])
    return templates.TemplateResponse(
        "admin/trust_stage.html",
        {
            "request": request,
            "users": users,
            "stages": stages,
            "stage_choices": _stage_choices(),
            "message": message,
            "error": error,
        },
    )


@router.get("", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
async def trust_stage_form(request: Request) -> HTMLResponse:
    """Render the dev trust-stage picker."""
    return await _render(request)


@router.post("/set-stage", response_class=HTMLResponse)
async def set_trust_stage(
    request: Request,
    user_id: str = Form(...),
    stage: int = Form(...),
) -> HTMLResponse:
    """Apply a trust stage to a user, then re-render the picker with the result."""
    # Validate inputs before touching the DB.
    try:
        uid = UUID(user_id)
    except (ValueError, AttributeError):
        return await _render(request, error=f"Invalid user id: {user_id!r}")
    try:
        target = TrustStage(stage)
    except ValueError:
        return await _render(request, error=f"Invalid stage {stage!r} (must be 1-4)")

    # Writes must commit: transaction_scope() commits on success (session_scope
    # does NOT commit, despite its docstring).
    async with AsyncSessionFactory.transaction_scope() as session:
        username = (
            await session.execute(select(User.username).where(User.id == uid))
        ).scalar_one_or_none()
        if username is None:
            return await _render(request, error=f"No active user with id {user_id}")
        new_stage = await _force_set_stage(session, uid, target)

    logger.info(
        "dev_trust_stage_set",
        user_id=user_id,
        username=username,
        stage=int(new_stage),
        stage_name=new_stage.name,
    )
    return await _render(
        request,
        message=f"Set {username} → Stage {int(new_stage)} ({new_stage.name}). "
        f"Reload the trust-gated surface to see the effect.",
    )
