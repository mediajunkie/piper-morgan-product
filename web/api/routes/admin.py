"""
Admin/Monitoring & Health Check API Routes

Provides endpoints for system health, monitoring, and cache management.
All endpoints intended for admin/monitoring purposes.

Routes:
- GET /health - Basic health check (exempt from intent enforcement)
- GET /health/config - Configuration health validation (GREAT-2D)
- GET /api/admin/intent-monitoring - Intent enforcement monitoring (GREAT-4B)
- GET /api/admin/intent-cache-metrics - Intent cache performance metrics
- POST /api/admin/intent-cache-clear - Clear intent cache (admin only)
- GET /api/admin/piper-config-cache-metrics - PIPER.md cache metrics
- POST /api/admin/piper-config-cache-clear - Clear PIPER.md cache (admin only)
- GET /api/admin/user-context-cache-metrics - User context cache metrics
- POST /api/admin/user-context-cache-clear - Clear user context cache (admin only)
- POST /api/admin/user-context-cache-invalidate/{session_id} - Invalidate user session cache

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 877-1036)
Now: Extracted to separate router module
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
async def health_config():
    """
    Configuration health check endpoint.

    Returns validation status for all service configurations.
    CORE-GREAT-2D: Configuration Validation
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
async def intent_monitoring():
    """
    Intent enforcement monitoring endpoint.

    Returns current middleware configuration and monitoring status.
    CORE-GREAT-4B: Intent Enforcement
    """
    from web.middleware.intent_enforcement import IntentEnforcementMiddleware

    return IntentEnforcementMiddleware.get_monitoring_status()


@router.get("/api/admin/intent-cache-metrics")
async def intent_cache_metrics(request: Request):
    """
    Intent cache performance metrics endpoint.

    Returns cache hit rate, size, and performance statistics.
    CORE-GREAT-4B Phase 3: Intent Caching
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
async def piper_config_cache_metrics():
    """
    PIPER.md config cache performance metrics endpoint.

    Returns cache hit rate, age, and performance statistics for PIPER configuration caching.
    GREAT-4C Phase 3: PIPER Config Caching
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
async def user_context_cache_metrics():
    """
    User context cache performance metrics endpoint.

    Returns cache hit rate and session-level cache statistics.
    GREAT-4C Phase 3: PIPER Config Caching
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
