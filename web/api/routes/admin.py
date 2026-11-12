"""
Admin/Monitoring & Health Check API Routes

Provides endpoints for system health, monitoring, and cache management.
All endpoints intended for admin/monitoring purposes.

Routes:
- GET /health - Basic health check (UNGATED BY DESIGN — see route docstring)
- GET /api/v1/version - Deploy identity for the UI footer (#1499)
- GET /health/config - Configuration health validation (GREAT-2D) (admin only)
- GET /api/admin/intent-monitoring - Intent enforcement monitoring (GREAT-4B) (admin only)
- GET /api/admin/intent-cache-metrics - Intent cache performance metrics (admin only)
- POST /api/admin/intent-cache-clear - Clear intent cache (admin only)
- GET /api/admin/piper-config-cache-metrics - PIPER.md cache metrics (admin only)
- POST /api/admin/piper-config-cache-clear - Clear PIPER.md cache (admin only)
- GET /api/admin/user-context-cache-metrics - User context cache metrics (admin only)
- POST /api/admin/user-context-cache-clear - Clear user context cache (admin only)
- POST /api/admin/user-context-cache-invalidate/{session_id} - Invalidate user session cache

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 877-1036)
Now: Extracted to separate router module

Authorization (#1508 → 1598)
----------------------------
#1508 gated the four cache-MUTATION routes behind `require_admin`. The
read-only metrics/health reads on the same router were left ungated, which
made `/api/admin/` a prefix that only half-honored its own name — any merely
authenticated user could read cache metrics and config-validation detail.
PM ruled 2026-08-25: gate them admin-only.

Nine of the ten routes on this router now depend on
`services.auth.auth_middleware.require_admin` (the SAME dependency #1508 used
— there is deliberately no second authorization path here). `require_admin`
reads `users.is_admin` LIVE from the DB (#357 SEC-RBAC): non-admin → 403,
admin-check failure → 503 fail-closed, unauthenticated → 401 from its own
`get_current_user` sub-dependency.

The single exception is `GET /health`, which stays open — it is polled by
deployment infrastructure that cannot authenticate. See its docstring.
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import create_async_engine

from services.auth.auth_middleware import JWTClaims, require_admin

logger = structlog.get_logger()

# Router configuration - split into multiple routers for clarity
router = APIRouter(tags=["admin", "monitoring", "health"])


# #2083: the database half of the health verdict. Bounded so the route stays fast
# under Fly's 5 s check timeout; any exception or a timeout reads "unreachable".
DATABASE_PROBE_SECONDS = 2.0


async def _database_probe() -> str:
    """Return "healthy" when `SELECT 1` answers on the database, else "unreachable".

    #2083: on 2026-10-19 alpha's Postgres stopped answering for hours while
    /health kept saying "healthy" (it had no DB check), so sign-in returned 500
    for everyone while the deploy gate, the promotion grant and the test card
    all read the page as fine.

    The probe opens its OWN one-connection engine and disposes it in `finally`;
    it never touches the global singleton (`services.database.connection.db`).
    The first landing (13716892ee) used the singleton and turned Tests red:
    `asyncio.wait_for` cancelling an asyncpg operation mid-flight left a POOLED
    connection in "another operation is in progress", and a health call under
    a TestClient loop bound the singleton to that loop, so later DB tests in
    the same process failed (3 new failures, 2026-10-19 10:01). A throwaway
    engine has no pool to poison and no loop to keep. Cost: one connection
    setup per check (every 30 s on Fly), which session_scope_fresh() already
    pays per request on the setup endpoints.

    The body never carries the DSN, the host or the exception text: the class
    name goes to the log only.
    """
    from sqlalchemy import text

    from services.database.session_factory import _get_database_url

    engine = create_async_engine(
        _get_database_url(), pool_pre_ping=False, pool_size=1, max_overflow=0
    )

    async def _ping() -> None:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

    try:
        await asyncio.wait_for(_ping(), timeout=DATABASE_PROBE_SECONDS)
    except Exception as exc:  # noqa: BLE001 — every failure class reads the same from outside
        logger.warning("health_database_probe_failed", error_class=type(exc).__name__)
        return "unreachable"
    finally:
        try:
            await asyncio.wait_for(engine.dispose(), timeout=DATABASE_PROBE_SECONDS)
        except Exception as exc:  # noqa: BLE001
            logger.warning("health_database_probe_dispose_failed", error_class=type(exc).__name__)
    return "healthy"


def _credential_store_status() -> str:
    """#2125: healthy | unavailable | not_configured, from the startup probe (cached);
    never raises."""
    try:
        from services.security.field_encryption import probe_credential_store

        return str(probe_credential_store().get("status") or "unavailable")
    except Exception:
        return "unavailable"


def _redis_status() -> str:
    """#2348 (Arch's shape): ok | unavailable, from the pool's RECORDED health ping.
    Never pings (/health is hit too often, #2336) and never raises. No address."""
    try:
        from services.cache.redis_factory import RedisFactory

        return RedisFactory.recorded_health()
    except Exception:
        return "unavailable"


#: A recorded "unavailable" degrades the body status only while it is this fresh (Arch,
#: 2026-11-12). The record refreshes when a request takes a Redis client, never from
#: /health, so on a host with no traffic an old failure must not hold promotions or keep
#: alerting after Redis has come back.
REDIS_FRESH_SECONDS = 120


def _redis_checked_s() -> Optional[int]:
    """#2348: seconds since the recorded ping, or None when there has been none."""
    try:
        from services.cache.redis_factory import RedisFactory

        return RedisFactory.recorded_health_age_s()
    except Exception:
        return None


def _revocation_source() -> str:
    """#2348: redis | database, the store this process checks revoked tokens in. A process
    that started with Redis down stays on the database (the record) until it restarts."""
    try:
        from services.auth.container import AuthContainer

        return str(AuthContainer.get_token_blacklist().revocation_source)
    except Exception:
        return "database"


def _uptime_seconds() -> int:
    """Seconds since this process started (the quiet count zeroes on a restart)."""
    try:
        from services.infrastructure.turn_activity import PROCESS_STARTED_AT

        return max(0, int(time.time() - PROCESS_STARTED_AT))
    except Exception:  # silent-ok: never let a counter fail /health
        return 0


def _quiet_count() -> Dict[str, Any]:
    """The quiet verdict for the promote gate, from the intent service's recorder.

    CIO (2026-10-21): /health is public, so it serves only ``quiet`` (no account
    sent a chat turn in the last 30 minutes) plus the failure marker; the counts
    go to the server log. A failure serves ``{"error": "unavailable"}`` and a
    record failure inside the window serves ``quiet: false`` with the flag, so
    a counter that cannot count never reads as quiet (Arch). /health stays 200.
    """
    try:
        from services.infrastructure.turn_activity import TURN_ACTIVITY

        snap = TURN_ACTIVITY.snapshot()
        failed = bool(snap.get("record_failed_in_window"))
        logger.info(
            "quiet_count_computed",
            accounts=snap.get("accounts"),
            turns=snap.get("turns"),
            record_failed_in_window=failed,
        )
        return {
            "quiet": (snap.get("accounts") == 0) and not failed,
            "record_failed_in_window": failed,
        }
    except Exception:  # silent-ok: /health is polled by Fly; never let a counter fail it
        return {"error": "unavailable"}


@router.get("/health")
async def health(request: Request):
    """
    Health check endpoint - exempt from intent enforcement.

    ⚠️ DELIBERATELY UNGATED — DO NOT ADD `require_admin` HERE. ⚠️

    #1598 gated the other nine routes on this router admin-only. This one is
    the named exception, because it is polled by deployment infrastructure
    that has no credentials and no way to acquire any. Gating it does not
    "tighten security" — it takes the app down:

      - fly.toml `[[http_service.checks]] path = "/health"` (every 30s). A
        non-200 marks the machine unhealthy; Fly stops routing to it and
        restarts it. On a single-machine app that is a full outage, and a
        deploy would never pass its health gate.
      - Dockerfile HEALTHCHECK (`GET localhost:8001/health`) — same effect at
        the container layer.
      - scripts/restart-server.sh waits on /health to declare a restart
        successful; scripts/start-piper.sh and scripts/phase-z-validation.sh
        probe it too.

    It is correspondingly cheap to leave open: the response is a fixed set of
    service-liveness strings (web / intent_enforcement / intent_service =
    healthy|degraded) plus a timestamp and the #1839 deploy identity
    (environment / version / git SHA — deliberately unauthenticated, per the
    issue: "what is actually deployed" must be a curl, not an inference; these
    are release facts, not user data or secrets).

    Returns basic service status for monitoring and load balancers.

    #1116 Finding 3: also report key-service availability so silently-broken
    primary surfaces (e.g. intent_service=None from a silent startup failure)
    surface in /health rather than only appearing per-request as degradation
    responses.

    #2083 (Arch, 2026-10-19): `services.database` reports healthy|unreachable
    from a bounded `SELECT 1`, and top-level `status` reads "degraded" when it
    fails. The HTTP status STAYS 200 either way: Fly restarts the machine on a
    non-200, and restarting the only machine every 30 s cannot fix a database
    outage; it would also take down the pages that need no database. Readers
    that want the verdict read the body's `status`, never the HTTP code.
    """
    # Report status of services that the primary surfaces depend on.
    # Each is checked against app.state for non-None presence.
    intent_service_present = getattr(request.app.state, "intent_service", None) is not None

    database_status = await _database_probe()

    # #2101: the event-loop watchdog's presence, readable with one curl before a run.
    # "running" = the checker thread is alive; "absent" = never started or stopped.
    # Informational: it never changes the overall status.
    _watchdog = getattr(request.app.state, "loop_watchdog", None)
    watchdog_status = (
        "running" if _watchdog is not None and getattr(_watchdog, "is_running", False) else "absent"
    )

    redis_status: str = _redis_status()
    redis_age: Optional[int] = _redis_checked_s()

    services_status = {
        "web": "healthy",
        "intent_enforcement": "active",
        "intent_service": "healthy" if intent_service_present else "degraded",
        "database": database_status,
        "loop_watchdog": watchdog_status,
        # The quiet count (grant condition 3): accounts with a chat turn in the
        # last 30 minutes, name-free; the promote gate reads `.accounts` and
        # refuses while it is above zero. Informational for the status line.
        "chat_turns_last_30m": _quiet_count(),
        # Seconds since the process started: a promotion restarts alpha and zeroes the
        # count, so the dispatcher reads this beside it (grant condition 3, CIO 10-21).
        "uptime_seconds": _uptime_seconds(),
        # #2125: a box that cannot store keys reads degraded before anyone presses Validate,
        # and the promote step's health refusal holds a promotion onto it.
        "credential_store": _credential_store_status(),
        # #2348: Redis is on the path of every request (the usage cap refuses without
        # it) and nothing served showed it. `redis_checked_s` is the record's age.
        # `revocation_source` is informational: the database is safe and a restart fixes it.
        "redis": redis_status,
        "redis_checked_s": redis_age,
        "revocation_source": _revocation_source(),
    }
    # Arch, 2026-11-12: without Redis the usage cap answers every page 503, so the host
    # is down for users and `status` says so, but only on a FRESH record.
    redis_down_now = (
        redis_status == "unavailable" and redis_age is not None and redis_age < REDIS_FRESH_SECONDS
    )

    # Overall status degrades if any required service is missing, the DB is unreachable,
    # the credential store cannot encrypt, or a fresh record says Redis is not answering.
    overall_status = (
        "healthy"
        if intent_service_present
        and database_status == "healthy"
        and services_status["credential_store"] != "unavailable"
        and not redis_down_now
        else "degraded"
    )

    # #1839: deploy identity on the surface infrastructure actually polls.
    # The first landing put these fields only on staging_health's router,
    # which no app mounted — this route is the served /health (2026-09-21).
    # staging_health.py itself was deleted 2026-09-23 (#1499 Class 2, dead
    # router disposal); deploy_identity() moved to its own module first.
    from services.api.health.deploy_identity import deploy_identity

    return {
        "status": overall_status,
        "message": "Piper Morgan web service is running",
        "timestamp": datetime.now().isoformat(),
        **deploy_identity(),
        "services": services_status,
    }


@router.get("/api/v1/version")
async def version():
    """
    Deploy identity for the UI footer — version / git SHA / environment.

    #1499: `templates/settings-index.html` and `templates/account.html` have both
    fetched `/api/v1/version` on load since they shipped, and NO router defined the
    path. Each page silently 404'd, fell into its `.catch`, rendered "unknown" in the
    footer and raised a `version_check_failed` toast — which reads as a broken
    version lookup rather than a missing route. The 2026-08-07 route audit found it.

    The payload is `deploy_identity()` — the same helper the SERVED `/health` above
    uses. That is deliberate and is the #1839 lesson applied a second time: when the
    same three facts are rendered on two surfaces, they get ONE source, or they drift
    and the drift is invisible until someone curls production. `version` and
    `environment` are exactly the two field names both pages read.

    Placed on this router (prefix-less, mounted at `web/app.py:308`) rather than
    `web/api/routes/health.py`, whose `/api/v1/health` prefix cannot produce this
    path. It carries the explicit `/api/v1/` prefix per the API convention.

    Not auth-exempt: both callers are authenticated pages fetching with
    `credentials: 'include'`, so the default gate costs them nothing, and #1308 makes
    the exempt list a security boundary that should not grow without a reason.
    """
    from services.api.health.deploy_identity import deploy_identity

    return deploy_identity()


@router.get("/health/config")
async def health_config(admin: JWTClaims = Depends(require_admin)):
    """
    Configuration health check endpoint (admin only).

    Returns validation status for all service configurations.
    CORE-GREAT-2D: Configuration Validation

    #1598: admin-gated. This returns a per-service configuration-validity
    summary (which integrations are configured, which are misconfigured and
    why) — reconnaissance detail, not liveness. Unlike its `/health` sibling
    it has no infrastructure caller: fly.toml, the Dockerfile HEALTHCHECK and
    every script under scripts/ poll `/health`
    (and the staging Prometheus job scrapes /health/metrics, /health/system,
    /health/mcp, /health/comprehensive — never this path).

    ⚠️ BEHAVIOR CHANGE, called out because it is the one place #1598 moves
    the UNAUTHENTICATED response: AuthMiddleware's exempt matching is a
    `startswith` (services/auth/auth_middleware.py `_should_exclude_path`),
    so EXEMPT_HEALTH_PATHS' "/health" entry was silently exempting
    "/health/config" as well — it was world-readable, no token required.
    It now returns 401 unauthenticated / 403 for a non-admin. That is the
    intent of the ruling, but it is a real change, not a no-op.
    """
    from services.infrastructure.config.config_validator import ConfigValidator

    validator = ConfigValidator()
    summary = validator.get_summary()

    # Return 200 with summary (even if some services invalid)
    # This is a health check endpoint, not a gate
    return {
        "status": "healthy" if summary["all_valid"] else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "validation": summary,
    }


@router.get("/api/admin/intent-monitoring")
async def intent_monitoring(admin: JWTClaims = Depends(require_admin)):
    """
    Intent enforcement monitoring endpoint (admin only).

    Returns current middleware configuration and monitoring status.
    CORE-GREAT-4B: Intent Enforcement

    #1598: admin-gated. The payload is the enforcement middleware's own
    configuration — including the full exempt-path list, i.e. a map of which
    routes skip intent enforcement. That is exactly the shape an attacker
    would enumerate first; it should not be readable by any authenticated user.
    """
    from web.middleware.intent_enforcement import IntentEnforcementMiddleware

    return IntentEnforcementMiddleware.get_monitoring_status()


@router.get("/api/admin/intent-cache-metrics")
async def intent_cache_metrics(request: Request, admin: JWTClaims = Depends(require_admin)):
    """
    Intent cache performance metrics endpoint (admin only).

    Returns cache hit rate, size, and performance statistics.
    CORE-GREAT-4B Phase 3: Intent Caching

    #1598: admin-gated. Its mutating sibling (/api/admin/intent-cache-clear)
    has required admin since #1508; the read of the same cache's contents-level
    statistics is now held to the same bar.
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        metrics = intent_service.intent_classifier.cache.get_metrics()
        return {"cache_enabled": True, "metrics": metrics, "status": "operational"}
    else:
        return {"cache_enabled": False, "status": "not_configured"}


@router.post("/api/admin/intent-cache-clear")
async def clear_intent_cache(request: Request, admin: JWTClaims = Depends(require_admin)):
    """
    Clear the intent cache (admin only).

    Removes all cached intent classifications and resets metrics.
    CORE-GREAT-4B Phase 3: Intent Caching
    """
    # Get IntentService from app state
    intent_service = getattr(request.app.state, "intent_service", None)

    # GREAT-5 Phase 1.5: Fix attribute name (intent_classifier not classifier)
    if intent_service and hasattr(intent_service.intent_classifier, "cache"):
        intent_service.intent_classifier.cache.clear()
        return {
            "status": "cache_cleared",
            "message": "Intent cache cleared successfully",
        }
    else:
        return {"status": "cache_not_configured", "message": "Intent cache not available"}


@router.get("/api/admin/piper-config-cache-metrics")
async def piper_config_cache_metrics(admin: JWTClaims = Depends(require_admin)):
    """
    PIPER.md config cache performance metrics endpoint (admin only).

    Returns cache hit rate, age, and performance statistics for PIPER configuration caching.
    GREAT-4C Phase 3: PIPER Config Caching

    #1598: admin-gated, matching its /api/admin/piper-config-cache-clear
    sibling (#1508).
    """
    from services.configuration.piper_config_loader import piper_config_loader

    metrics = piper_config_loader.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@router.post("/api/admin/piper-config-cache-clear")
async def clear_piper_config_cache(admin: JWTClaims = Depends(require_admin)):
    """
    Clear the PIPER.md config cache (admin only).

    Forces next PIPER.md load to read from disk.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.configuration.piper_config_loader import piper_config_loader

    piper_config_loader.clear_cache()
    return {
        "status": "cache_cleared",
        "message": "PIPER config cache cleared successfully",
    }


@router.get("/api/admin/user-context-cache-metrics")
async def user_context_cache_metrics(admin: JWTClaims = Depends(require_admin)):
    """
    User context cache performance metrics endpoint (admin only).

    Returns cache hit rate and session-level cache statistics.
    GREAT-4C Phase 3: PIPER Config Caching

    #1598: admin-gated. These are OTHER users' session-level cache statistics;
    the mutating siblings (user-context-cache-clear / -invalidate) have
    required admin since #1508.
    """
    from services.user_context_service import user_context_service

    metrics = user_context_service.get_cache_metrics()
    return {"cache_enabled": True, "metrics": metrics, "status": "operational"}


@router.post("/api/admin/user-context-cache-clear")
async def clear_user_context_cache(admin: JWTClaims = Depends(require_admin)):
    """
    Clear the user context cache (admin only).

    Removes all cached user contexts. Next request will reload from PIPER.md.
    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache()  # No session_id = clear all
    return {
        "status": "cache_cleared",
        "message": "User context cache cleared successfully",
    }


@router.post("/api/admin/user-context-cache-invalidate/{session_id}")
async def invalidate_user_context(session_id: str, admin: JWTClaims = Depends(require_admin)):
    """
    Invalidate specific user's cached context (admin only).

    Args:
        session_id: Session identifier to invalidate

    GREAT-4C Phase 3: PIPER Config Caching
    """
    from services.user_context_service import user_context_service

    user_context_service.invalidate_cache(session_id)
    return {
        "status": "invalidated",
        "session_id": session_id,
        "message": f"User context for session {session_id} invalidated",
    }
