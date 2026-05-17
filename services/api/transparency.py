"""
PM-087 User Transparency API Endpoints
User-accessible audit log endpoints with security redactions

Leverages existing infrastructure:
- services/ethics/audit_transparency.py
- services/infrastructure/logging/config.py
- services/api/errors.py patterns

#1095 (2026-05-16): Auth gates added. Two posture flavors:
- User-scoped endpoints (audit-log, audit-summary): require JWT user_id to
  own the session_id per ConversationDB. Admin override available via
  is_admin claim (SEC-RBAC pattern from files.py).
- Admin-scoped endpoints (stats, cleanup, health): require is_admin claim.
  Until SEC-RBAC global-admin lands, no production user has is_admin=True;
  these endpoints effectively 403 everyone in current deployment — by design.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import select

from services.api.errors import APIError
from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.models import ConversationDB
from services.database.session_factory import AsyncSessionFactory
from services.ethics.audit_transparency import audit_transparency
from services.infrastructure.logging.config import get_ethics_logger

# Configure structured logger
logger = get_ethics_logger(__name__)

# Create router
transparency_router = APIRouter(prefix="/api/v1/transparency", tags=["transparency"])


async def _require_session_owner_or_admin(
    session_id: str, current_user: JWTClaims
) -> None:
    """403 unless JWT user owns the session (per ConversationDB) or is admin.

    #1095: session_id-as-path-param surfaces a privilege-escalation risk
    (Pattern-071, Audit Logs as Attack Surface). This guard binds the
    requested session to the JWT-authenticated user. Uniform 403 message
    avoids leaking session existence to non-owners.
    """
    is_admin = getattr(current_user, "is_admin", False)
    if is_admin:
        return
    async with AsyncSessionFactory.session_scope_fresh() as db:
        result = await db.execute(
            select(ConversationDB).where(ConversationDB.id == session_id)
        )
        conv = result.scalar_one_or_none()
    if conv is None or str(conv.user_id) != str(current_user.sub):
        # Uniform 403 — don't differentiate "doesn't exist" from "not yours"
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this session's audit data",
        )


def _require_admin(current_user: JWTClaims) -> None:
    """403 unless JWT user has is_admin claim.

    Used for admin-shaped endpoints (stats, cleanup, health). Until
    SEC-RBAC global-admin lands (is_admin claim setter missing in current
    JWT issuance flow), this guard 403s every request — by design, since
    the endpoints were never meant to be user-reachable.
    """
    is_admin = getattr(current_user, "is_admin", False)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")


class AuditLogResponse(BaseModel):
    """Response model for audit log entries"""

    entries: List[Dict]
    total_entries: int
    session_id: str
    request_limit: int
    timestamp: str


class AuditSummaryResponse(BaseModel):
    """Response model for audit summary"""

    summary: Dict
    timestamp: str


class TransparencyStatsResponse(BaseModel):
    """Response model for transparency statistics"""

    stats: Dict
    timestamp: str


@transparency_router.get("/audit-log/{session_id}")
async def get_user_audit_log(
    session_id: str,
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of entries to return"),
    current_user: JWTClaims = Depends(get_current_user),
) -> AuditLogResponse:
    """Get user's audit log with security redactions"""
    await _require_session_owner_or_admin(session_id, current_user)
    try:
        # Get audit log entries
        entries = await audit_transparency.get_user_audit_log(session_id, limit)

        # Log transparency request
        logger.log_behavior_pattern(
            "transparency_api_request",
            {
                "session_id": session_id,
                "entries_returned": len(entries),
                "request_limit": limit,
                "endpoint": "get_user_audit_log",
            },
        )

        return AuditLogResponse(
            entries=entries,
            total_entries=len(entries),
            session_id=session_id,
            request_limit=limit,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    except Exception as e:
        logger.log_boundary_violation(
            "transparency_api_error",
            {"error": str(e), "session_id": session_id, "endpoint": "get_user_audit_log"},
        )

        from services.api.errors import ServiceUnavailableError

        raise ServiceUnavailableError(
            service="audit log retrieval",
            details={
                "session_id": session_id,
                "help": "Try again in a moment or contact support if this continues",
            },
        )


@transparency_router.get("/audit-summary/{session_id}")
async def get_user_audit_summary(
    session_id: str,
    current_user: JWTClaims = Depends(get_current_user),
) -> AuditSummaryResponse:
    """Get user's audit summary with privacy protection"""
    await _require_session_owner_or_admin(session_id, current_user)
    try:
        # Get user's audit log for summary
        entries = await audit_transparency.get_user_audit_log(session_id, limit=1000)

        # Calculate summary statistics
        total_entries = len(entries)
        violation_entries = [e for e in entries if e.get("event_type") == "boundary_violation"]
        decision_entries = [e for e in entries if e.get("event_type") == "ethics_decision"]

        # Calculate boundary type breakdown
        boundary_types = {}
        for entry in entries:
            details = entry.get("details", {})
            boundary_type = details.get("boundary_type", "unknown")
            boundary_types[boundary_type] = boundary_types.get(boundary_type, 0) + 1

        # Recent activity (last 24 hours)
        recent_cutoff = datetime.now(timezone.utc).timestamp() - 86400  # 24 hours
        recent_entries = [
            e
            for e in entries
            if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")).timestamp()
            > recent_cutoff
        ]

        # Issue #1101: dropped `audit_completeness: "100%"` and
        # `transparency_level: "Full transparency with privacy protection"`
        # fields — Pattern-073 (Documentation-Asserted-Behavior Drift)
        # instances 9 + 10. Both were unverifiable universal claims:
        # completeness is bounded by `limit=1000` on the upstream
        # get_user_audit_log call (line 158), and "Full transparency" is
        # a categorical claim the service can't actually verify. The UI
        # already applies the discipline by not rendering them (#1100
        # slice 2); this is the service-side cleanup.
        summary = {
            "total_entries": total_entries,
            "violation_entries": len(violation_entries),
            "decision_entries": len(decision_entries),
            "clean_interactions": total_entries - len(violation_entries),
            "boundary_types_checked": list(boundary_types.keys()),
            "boundary_type_breakdown": boundary_types,
            "recent_activity_24h": len(recent_entries),
            "entries_examined": len(entries),
            "entries_examined_limit": 1000,
            "session_id": session_id,
        }

        # Log summary request
        logger.log_behavior_pattern(
            "transparency_summary_request",
            {
                "session_id": session_id,
                "total_entries": total_entries,
                "violations": len(violation_entries),
                "endpoint": "get_user_audit_summary",
            },
        )

        return AuditSummaryResponse(
            summary=summary, timestamp=datetime.now(timezone.utc).isoformat()
        )

    except Exception as e:
        logger.log_boundary_violation(
            "transparency_summary_error",
            {"error": str(e), "session_id": session_id, "endpoint": "get_user_audit_summary"},
        )

        from services.api.errors import ServiceUnavailableError

        raise ServiceUnavailableError(
            service="audit summary generation",
            details={
                "session_id": session_id,
                "help": "Your audit data is safe - please try again in a moment",
            },
        )


@transparency_router.get("/stats")
async def get_transparency_stats(
    current_user: JWTClaims = Depends(get_current_user),
) -> TransparencyStatsResponse:
    """Get transparency system statistics (admin endpoint)"""
    _require_admin(current_user)
    try:
        # Get transparency statistics
        stats = await audit_transparency.get_transparency_stats()

        # Add additional system stats
        stats.update(
            {
                "system_status": "operational",
                "privacy_protection": "active",
                "user_access": "enabled",
                "audit_integrity": "validated",
            }
        )

        # Log stats request
        logger.log_behavior_pattern(
            "transparency_stats_request",
            {
                "total_entries": stats.get("total_audit_entries", 0),
                "transparency_requests": stats.get("transparency_requests", 0),
                "endpoint": "get_transparency_stats",
            },
        )

        return TransparencyStatsResponse(
            stats=stats, timestamp=datetime.now(timezone.utc).isoformat()
        )

    except Exception as e:
        logger.log_boundary_violation(
            "transparency_stats_error", {"error": str(e), "endpoint": "get_transparency_stats"}
        )

        from services.api.errors import ServiceUnavailableError

        raise ServiceUnavailableError(
            service="transparency statistics",
            details={"help": "Statistics are temporarily unavailable - please try again shortly"},
        )


@transparency_router.get("/health")
async def transparency_health_check(
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict:
    """Health check for transparency system (admin endpoint)"""
    _require_admin(current_user)
    try:
        # Basic health check
        stats = await audit_transparency.get_transparency_stats()

        health_status = {
            "status": "healthy",
            "transparency_system": "operational",
            "audit_log_entries": stats.get("total_audit_entries", 0),
            "transparency_requests": stats.get("transparency_requests", 0),
            "redaction_operations": stats.get("redaction_operations", 0),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Log health check
        logger.log_behavior_pattern(
            "transparency_health_check",
            {"status": "healthy", "endpoint": "transparency_health_check"},
        )

        return health_status

    except Exception as e:
        logger.log_boundary_violation(
            "transparency_health_error", {"error": str(e), "endpoint": "transparency_health_check"}
        )

        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


@transparency_router.post("/cleanup")
async def trigger_audit_cleanup(
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict:
    """Trigger audit log cleanup (admin endpoint)"""
    _require_admin(current_user)
    try:
        # Perform cleanup
        await audit_transparency.cleanup_old_entries()

        # Get updated stats
        stats = await audit_transparency.get_transparency_stats()

        cleanup_result = {
            "status": "cleanup_completed",
            "total_entries_remaining": stats.get("total_audit_entries", 0),
            "log_retention_days": stats.get("log_retention_days", 90),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Log cleanup
        logger.log_behavior_pattern(
            "transparency_cleanup_triggered",
            {
                "entries_remaining": stats.get("total_audit_entries", 0),
                "endpoint": "trigger_audit_cleanup",
            },
        )

        return cleanup_result

    except Exception as e:
        logger.log_boundary_violation(
            "transparency_cleanup_error", {"error": str(e), "endpoint": "trigger_audit_cleanup"}
        )

        from services.api.errors import ServiceUnavailableError

        raise ServiceUnavailableError(
            service="audit cleanup",
            details={"help": "Cleanup process temporarily unavailable - your data remains secure"},
        )
