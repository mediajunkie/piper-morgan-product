"""#1680 Dashboard Criterion E: the admin JSON read of consequential actions.

``GET /api/v1/admin/consequential-actions`` serves HOST's headline ("N of M sites
instrumented", sites, never a bare percentage), the census drill-in (each site,
instrumented or not, with its registry flags), the action counts for a window, and the
failed-write count with the window it covers (since this process started; it resets on
every restart, so it is never a durable "no failed writes").

The counts come from ONE SQL query over ``audit_logs`` (``event_type='consequential'``,
``created_at`` inside the window), aggregated in the database with ``GROUPING SETS``:
the empty set gives the totals row and ``(action)`` gives one row per site. No row is
counted in Python.

Admin only: ``require_admin`` is the same live, fail-closed gate every admin read uses
(#2096's pattern in ``feedback.py``).
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends, Query
from sqlalchemy import text

from services.auth.auth_middleware import require_admin
from services.auth.jwt_service import JWTClaims
from services.security.audit_logger import EventType, consequential_write_failures_window
from services.security.consequential_sites import (
    CONSEQUENTIAL_SITES,
    coverage,
    coverage_headline,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

DEFAULT_WINDOW_DAYS = 7
MAX_WINDOW_DAYS = 90

# One statement: GROUPING SETS ((), (action)) yields the totals row (grouped = 1) and
# one row per site key (grouped = 0). The empty grouping set returns a row even when no
# action falls in the window, so the totals are always present (as zeros).
_COUNTS_SQL = text(
    """
    SELECT
        action,
        GROUPING(action) AS grouped,
        (now() - make_interval(days => :days)) AS since,
        count(*) AS rows_all,
        count(*) FILTER (WHERE details->>'nested_in' IS NOT NULL) AS nested,
        count(*) FILTER (WHERE details->>'nested_in' IS NULL) AS total,
        count(*) FILTER (WHERE status = 'success' AND details->>'nested_in' IS NULL) AS success,
        count(*) FILTER (WHERE status = 'failed' AND details->>'nested_in' IS NULL) AS failed,
        count(*) FILTER (WHERE status = 'unconfirmed' AND details->>'nested_in' IS NULL) AS unconfirmed,
        count(*) FILTER (WHERE proactive AND details->>'nested_in' IS NULL) AS proactive,
        count(*) FILTER (WHERE credits_spent AND details->>'nested_in' IS NULL) AS credits_spent,
        count(*) FILTER (WHERE external_message AND details->>'nested_in' IS NULL) AS external_message,
        count(*) FILTER (WHERE hard_to_reverse AND details->>'nested_in' IS NULL) AS hard_to_reverse
    FROM audit_logs
    WHERE event_type = :event_type
      AND created_at >= now() - make_interval(days => :days)
    GROUP BY GROUPING SETS ((), (action))
    """
)


def _site_entries() -> Dict[str, Any]:
    instrumented, censused = coverage()
    return {
        "instrumented": instrumented,
        "censused": censused,
        "complete": instrumented == censused,
        "entries": [
            {
                "key": s.key,
                "family": s.family,
                "module": s.module,
                "function": s.function,
                "instrumented": s.instrumented,
                "proactive": s.proactive,
                "external_message": s.external_message,
                "hard_to_reverse": s.hard_to_reverse,
            }
            for s in CONSEQUENTIAL_SITES.values()
        ],
    }


async def _action_counts(days: int) -> Dict[str, Any]:
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as session:
        rows = (
            (
                await session.execute(
                    _COUNTS_SQL, {"days": days, "event_type": EventType.CONSEQUENTIAL}
                )
            )
            .mappings()
            .all()
        )
    totals = next(r for r in rows if r["grouped"] == 1)
    since = totals["since"]
    return {
        "window_days": days,
        "since": since.isoformat() if hasattr(since, "isoformat") else str(since),
        "total": int(totals["total"]),
        # Landing C: rows written inside another site's call (details.nested_in) are
        # the same action seen twice; they are excluded from total/by_status/by_flag
        # and shown here and in by_site.
        "nested": int(totals["nested"]),
        "by_status": {
            "success": int(totals["success"]),
            "failed": int(totals["failed"]),
            "unconfirmed": int(totals["unconfirmed"]),
        },
        "by_flag": {
            "proactive": int(totals["proactive"]),
            "credits_spent": int(totals["credits_spent"]),
            "external_message": int(totals["external_message"]),
            "hard_to_reverse": int(totals["hard_to_reverse"]),
        },
        "by_site": {r["action"]: int(r["rows_all"]) for r in rows if r["grouped"] == 0},
    }


@router.get("/consequential-actions")
async def consequential_actions(
    admin: JWTClaims = Depends(require_admin),
    days: int = Query(DEFAULT_WINDOW_DAYS, ge=1, le=MAX_WINDOW_DAYS),
) -> Dict[str, Any]:
    """Headline, census drill-in, window counts and the failed-write window."""
    return {
        "headline": coverage_headline(),
        "sites": _site_entries(),
        "actions": await _action_counts(days),
        "failed_writes": consequential_write_failures_window(),
    }
