"""
Admin/Monitoring & Health Check API Routes

Provides endpoints for system health, monitoring, and cache management.
All endpoints intended for admin/monitoring purposes.

Routes:
- GET /health - Basic health check (UNGATED BY DESIGN — see route docstring)
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

from datetime import datetime, timezone

import structlog
from fastapi import APIRouter, Depends, Request

from services.auth.auth_middleware import JWTClaims, require_admin

logger = structlog.get_logger()

# Router configuration - split into multiple routers for clarity
router = APIRouter(tags=["admin", "monitoring", "health"])


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
      - docker-compose.staging.yml service healthcheck.
      - scripts/restart-server.sh waits on /health to declare a restart
        successful; scripts/start-piper.sh and scripts/phase-z-validation.sh
        probe it too.

    It is correspondingly cheap to leave open: the response is a fixed set of
    service-liveness strings (web / intent_enforcement / intent_service =
    healthy|degraded) plus a timestamp. No user data, no config values, no
    counts, no identifiers.

    Returns basic service status for monitoring and load balancers.

    #1116 Finding 3: also report key-service availability so silently-broken
    primary surfaces (e.g. intent_service=None from a silent startup failure)
    surface in /health rather than only appearing per-request as degradation
    responses.
    """
    # Report status of services that the primary surfaces depend on.
    # Each is checked against app.state for non-None presence.
    intent_service_present = getattr(request.app.state, "intent_service", None) is not None

    services_status = {
        "web": "healthy",
        "intent_enforcement": "active",
        "intent_service": "healthy" if intent_service_present else "degraded",
    }

    # Overall status degrades if any required service is missing.
    overall_status = "healthy" if intent_service_present else "degraded"

    return {
        "status": overall_status,
        "message": "Piper Morgan web service is running",
        "timestamp": datetime.now().isoformat(),
        "services": services_status,
    }


@router.get("/health/config")
async def health_config(admin: JWTClaims = Depends(require_admin)):
    """
    Configuration health check endpoint (admin only).

    Returns validation status for all service configurations.
    CORE-GREAT-2D: Configuration Validation

    #1598: admin-gated. This returns a per-service configuration-validity
    summary (which integrations are configured, which are misconfigured and
    why) — reconnaissance detail, not liveness. Unlike its `/health` sibling
    it has no infrastructure caller: fly.toml, the Dockerfile HEALTHCHECK,
    docker-compose.staging.yml and every script under scripts/ poll `/health`
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
