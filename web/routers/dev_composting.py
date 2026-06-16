"""Dev-only composting trigger (Issue #1143 COMPOSTING-DEV-TRIGGER).

Lets UAT kick a composting cycle on demand instead of waiting for the hourly
scheduler tick (which is additionally quiet-hours gated). This makes the
#1033 (MUX-COMPOSTED-EXPERIENCE) and #1035 (MUX-COMPOSTING-ACTIVATION) surfaces
exercisable in a UAT-style smoke test.

    GET  /api/v1/admin/composting          -> status (bin pending, job running)
    POST /api/v1/admin/composting/trigger  -> force a composting cycle, return counts

Reuses the *running* subsystem wired in web/startup.py:
``app.state.composting_scheduler_job`` (holds the domain ``CompostingScheduler``)
and ``app.state.compost_bin``. The trigger calls ``scheduler.run(force=True)``,
which bypasses the quiet-hours/min-pending gates that ``maybe_run`` enforces.

SECURITY (sibling of #1148/#1149): DEV-ONLY. Every route 404s in production via
``require_dev_environment`` (imported from dev_trust — single source of the gate).

SCOPE (slice 1): this triggers a cycle over whatever is in the compost bin. The
bin is in-memory and its contributor surface is not yet formalized (see
web/startup.py note), so on a fresh process it is typically empty and a trigger
returns ``processed_count: 0`` — the response says so honestly. A seed affordance
(adding a synthetic lifecycle-bearing object so the full extract→journal write
path can be exercised) is the natural companion slice; tracked on #1143.
"""

from __future__ import annotations

from datetime import datetime

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from services.mux.composting_models import CompostingTrigger
from services.mux.seed_compostable import make_seed_compostable
from web.routers.dev_trust import require_dev_environment

logger = structlog.get_logger()

router = APIRouter(
    prefix="/api/v1/admin/composting",
    tags=["admin", "dev", "composting"],
    dependencies=[Depends(require_dev_environment)],
)


def _job_and_bin(request: Request):
    """Return (job, bin) from app.state, or (None, None) if not wired."""
    job = getattr(request.app.state, "composting_scheduler_job", None)
    bin_ = getattr(request.app.state, "compost_bin", None)
    return job, bin_


@router.get("")
@router.get("/")
async def composting_status(request: Request):
    """Report whether the composting subsystem is running + how full the bin is."""
    job, bin_ = _job_and_bin(request)
    if job is None:
        return JSONResponse(
            {"available": False, "reason": "composting scheduler not running on this instance"},
            status_code=503,
        )
    return {
        "available": True,
        "is_running": job.is_running(),
        "bin_pending": len(bin_.pending) if bin_ is not None else None,
    }


@router.post("/trigger")
async def trigger_composting(request: Request, user_id: str = ""):
    """Force a composting cycle now (bypasses quiet-hours/min-pending gates).

    Returns the run counts. ``processed_count: 0`` with ``bin_pending_before: 0``
    means the cycle fired correctly but there was nothing to compost.
    """
    job, bin_ = _job_and_bin(request)
    if job is None:
        raise HTTPException(
            status_code=503,
            detail="composting scheduler not running on this instance",
        )

    pending_before = len(bin_.pending) if bin_ is not None else None
    result = await job.scheduler.run(force=True, user_id=user_id)

    processed = result.processed_count
    if processed == 0 and (pending_before or 0) == 0:
        message = (
            "Cycle fired, but the compost bin was empty — nothing to process. "
            "The bin is in-memory and its contributor surface is not yet "
            "formalized (#1143 slice 2 / web/startup.py note); seed objects to "
            "exercise #1033/#1035 end-to-end."
        )
    else:
        message = f"Composted {processed} object(s); {result.learnings_extracted} learning(s) written."

    logger.info(
        "dev_composting_triggered",
        user_id=user_id or None,
        bin_pending_before=pending_before,
        processed_count=processed,
        learnings_extracted=result.learnings_extracted,
    )

    return {
        "triggered": True,
        "user_id": user_id or None,
        "bin_pending_before": pending_before,
        "processed_count": processed,
        "learnings_extracted": result.learnings_extracted,
        "object_ids": result.object_ids,
        "errors": result.errors,
        "message": message,
    }


@router.post("/seed")
async def seed_composting(
    request: Request,
    count: int = 1,
    user_id: str = "",
    trigger: bool = True,
):
    """Seed synthetic lifecycle-bearing object(s) into the compost bin (#1143 slice 2).

    Slice 1's ``/trigger`` fires a cycle over *whatever is in the bin* — which on a
    fresh process is empty, so #1033 / #1035 stay unobservable. This route drops in
    synthetic objects that each walk a full lifecycle (EMERGENT → … → RATIFIED → …
    → ARCHIVED), so a cycle extracts real lessons and writes ``SurfaceableInsight``
    rows.

    With ``trigger=true`` (default) the cycle is fired immediately and the run
    counts + the just-written insights are returned, so a single POST exercises
    extraction → journal-write end-to-end. With ``trigger=false`` the objects are
    only staged; call ``/trigger`` separately.

    DEV-ONLY (router-level ``require_dev_environment`` gate; 404s in production).
    """
    job, bin_ = _job_and_bin(request)
    if job is None or bin_ is None:
        raise HTTPException(
            status_code=503,
            detail="composting scheduler not running on this instance",
        )

    # Clamp: this is a smoke-test affordance, not a bulk loader.
    count = max(1, min(count, 10))
    base = f"seed-{user_id or 'anon'}-{int(datetime.now().timestamp())}"
    seeded_ids: list[str] = []
    for i in range(count):
        obj = make_seed_compostable(object_id=f"{base}-{i}")
        bin_.add(
            obj,
            CompostingTrigger.MANUAL,
            object_type="seed_demo_object",
            priority=5,
        )
        seeded_ids.append(obj.id)

    response = {
        "seeded": True,
        "user_id": user_id or None,
        "seeded_object_ids": seeded_ids,
        "bin_pending_after_seed": len(bin_.pending),
    }

    if not trigger:
        response["message"] = (
            f"Seeded {count} object(s). POST /api/v1/admin/composting/trigger"
            "?user_id=… to compost them."
        )
        logger.info(
            "dev_composting_seeded",
            count=count,
            user_id=user_id or None,
            triggered=False,
        )
        return response

    result = await job.scheduler.run(force=True, user_id=user_id)

    # Best-effort read-back of what landed in the journal (evidence for #1035).
    # Read-back failure must not fail the trigger — it is reporting, not core.
    stored_insights: list[dict] = []
    journal = getattr(getattr(job.scheduler, "pipeline", None), "journal", None)
    if journal is not None and hasattr(journal, "get_for_object"):
        for oid in seeded_ids:
            try:
                # #1252 (a,3): thread the seeding principal so the read-back is
                # owner-scoped (objects were seeded + composted under this user_id).
                for ins in await journal.get_for_object(oid, user_id=user_id or None):
                    learning = getattr(ins, "learning", None)
                    stored_insights.append(
                        {
                            "object_id": oid,
                            "insight_id": getattr(ins, "id", None),
                            "text": getattr(learning, "expression", None),
                            "confidence": getattr(learning, "confidence", None),
                            "min_trust_stage": getattr(ins, "min_trust_stage", None),
                        }
                    )
            except Exception as e:  # fail-graceful: read-back is evidence, not core
                logger.warning(
                    "dev_composting_readback_failed", object_id=oid, error=str(e)
                )

    response.update(
        {
            "triggered": True,
            "processed_count": result.processed_count,
            "learnings_extracted": result.learnings_extracted,
            "object_ids": result.object_ids,
            "errors": result.errors,
            "stored_insights": stored_insights,
            "message": (
                f"Seeded {count} object(s) and composted {result.processed_count}; "
                f"{result.learnings_extracted} learning(s) written. Persistence "
                "survives restart (#1035); framed reflective surfacing is observable "
                "via the next-morning surfacing path (#1033)."
            ),
        }
    )
    logger.info(
        "dev_composting_seeded",
        count=count,
        user_id=user_id or None,
        triggered=True,
        processed_count=result.processed_count,
        learnings_extracted=result.learnings_extracted,
    )
    return response
