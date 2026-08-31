"""
================================================================================
SPRINT A5 REMNANT (deprecated Nov 13, 2025; pooling surface REMOVED per 1613)
================================================================================

Sprint A5 (Oct 20-21, 2025) prototyped learning endpoints on the file-based
cross-user pooled stores (QueryLearningLoop, CrossFeatureKnowledgeService).
It proved learning value and was superseded by Issue #300's database-backed,
per-user production system.

1613 (PM ruling 2026-08-31): the pooled stores and every A5 endpoint that
touched them were DELETED — patterns keyed by source_feature (not by user)
implemented exactly the cross-user pooling our published privacy claims
disclaim. What remains of A5 below is only the never-mounted (decorators
commented) User Controls section, which uses the user-scoped
UserPreferenceManager only. DO NOT re-wire it without checking the privacy
claims first.

Sprint A5 Valuable Insights (kept for the record):
- Learning system is valuable to users ✓
- Pattern-based approach works ✓
- Automatic capture > manual teaching ✓
- Need for multi-user support (database required) ✓
- Analytics and collaborative features desired ✓

================================================================================
ISSUE #300 ENDPOINTS (Nov 12-13, 2025) - PRODUCTION IMPLEMENTATION
================================================================================

Database-backed learning system with automatic real-time capture.

Architecture:
- Backend: LearningHandler (services/learning/learning_handler.py)
- Models: LearnedPattern, LearningSettings (services/database/models.py)
- Integration: IntentService (automatic capture + outcome recording)

See: gameplan-300-learning-basic-revised.md for complete architecture
See: dev/active/sprint-a5-vs-phase2-analysis.md for supersession rationale

Phase 2 Endpoints (added after Sprint A5 code below):
- GET /patterns - List user's learned patterns
- GET /patterns/{id} - Get pattern details
- DELETE /patterns/{id} - Delete pattern
- POST /patterns/{id}/enable - Enable pattern
- POST /patterns/{id}/disable - Disable pattern
- GET /settings - Get learning settings
- PUT /settings - Update learning settings
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.database.models import LearnedPattern, LearningSettings
from services.database.session_factory import AsyncSessionFactory
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Create router with prefix and tags for OpenAPI
router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


# ============================================================================
# User Controls (CORE-LEARN-F)
# ============================================================================


# @router.post("/controls/learning/enable")
async def enable_learning(user_id: str) -> Dict[str, Any]:
    """
    Enable learning for a user.

    Allows the learning system to collect patterns and preferences
    for this user.

    Args:
        user_id: User ID to enable learning for

    Returns:
        Confirmation with learning status
    """
    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        preference_manager = UserPreferenceManager()
        await preference_manager.set_preference(user_id, "learning_enabled", True)

        return {
            "status": "success",
            "learning_enabled": True,
            "user_id": user_id,
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to enable learning: {str(e)}",
            error_id="ENABLE_LEARNING_ERROR",
        )


# @router.post("/controls/learning/disable")
async def disable_learning(user_id: str) -> Dict[str, Any]:
    """
    Disable learning for a user.

    Stops the learning system from collecting new patterns
    and preferences. Existing data is preserved.

    Args:
        user_id: User ID to disable learning for

    Returns:
        Confirmation with learning status
    """
    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        preference_manager = UserPreferenceManager()
        await preference_manager.set_preference(user_id, "learning_enabled", False)

        return {
            "status": "success",
            "learning_enabled": False,
            "user_id": user_id,
            "note": "Existing learned data preserved",
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to disable learning: {str(e)}",
            error_id="DISABLE_LEARNING_ERROR",
        )


# @router.get("/controls/learning/status")
async def get_learning_status(user_id: str) -> Dict[str, Any]:
    """
    Get current learning status for a user.

    Args:
        user_id: User ID to check status for

    Returns:
        Current learning status (enabled/disabled)
    """
    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        preference_manager = UserPreferenceManager()
        enabled = await preference_manager.get_preference(user_id, "learning_enabled")

        # Default to enabled if not set
        if enabled is None:
            enabled = True

        return {"user_id": user_id, "learning_enabled": enabled}

    except Exception as e:
        return internal_error(
            message=f"Failed to get learning status: {str(e)}",
            error_id="GET_STATUS_ERROR",
        )


# @router.delete("/controls/data/clear")
async def clear_learned_data(
    user_id: str,
    data_type: str = Query(
        "all", description="Type of data to clear: all, patterns, preferences, automation"
    ),
) -> Dict[str, Any]:
    """
    Clear learned data for a user.

    Args:
        user_id: User ID
        data_type: Type of data to clear (all, patterns, preferences, automation)

    Returns:
        Confirmation of data cleared
    """
    from datetime import datetime, timezone

    from services.automation.audit_trail import get_audit_trail

    try:
        results = {}

        if data_type in ["all", "patterns"]:
            # 1613: the pooled pattern store (QueryLearningLoop) was removed per
            # PM ruling 2026-08-31 — there is no pooled store left to clear.
            # User-scoped patterns live in the #300 system (see clear_learning_data).
            results["patterns_cleared"] = True
            results["note"] = "Pooled pattern store removed (1613); nothing to clear"

        if data_type in ["all", "preferences"]:
            # Clear user preferences
            from services.domain.user_preference_manager import UserPreferenceManager

            preference_manager = UserPreferenceManager()
            # Note: Would need to add clear_all_preferences method
            results["preferences_cleared"] = True
            results["note"] = "Preference clearing requires clear_all method (future enhancement)"

        if data_type in ["all", "automation"]:
            # Clear automation audit trail for user
            audit_trail = get_audit_trail()
            # Note: AuditTrail has global clear, not user-specific
            results["automation_cleared"] = True
            results["note"] = (
                "Automation data clearing requires user filtering (future enhancement)"
            )

        return {
            "status": "success",
            "user_id": user_id,
            "data_type": data_type,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to clear data: {str(e)}", error_id="CLEAR_DATA_ERROR"
        )


# @router.get("/controls/export")
async def export_preferences(
    user_id: str, format: str = Query("json", description="Export format: json or csv")
) -> Dict[str, Any]:
    """
    Export user's learned preferences and patterns.

    Args:
        user_id: User ID
        format: Export format (json or csv)

    Returns:
        Exported data in requested format
    """
    from datetime import datetime, timezone

    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        preference_manager = UserPreferenceManager()

        # Gather all user data
        export_data = {
            "user_id": user_id,
            "export_timestamp": datetime.now(timezone.utc).isoformat(),
            "preferences": {},
            "patterns": [],
            "automation_settings": {},
        }

        # Get learning preferences
        learning_enabled = await preference_manager.get_preference(user_id, "learning_enabled")
        automation_enabled = await preference_manager.get_preference(user_id, "automation_enabled")
        privacy_settings = await preference_manager.get_preference(user_id, "privacy_settings")

        export_data["preferences"] = {
            "learning_enabled": learning_enabled if learning_enabled is not None else True,
            "automation_enabled": automation_enabled if automation_enabled is not None else False,
            "privacy_settings": privacy_settings or {},
        }

        # 1613: the pooled pattern store was removed (PM ruling 2026-08-31);
        # user-scoped patterns are exportable via the #300 export_learning_data
        # route below. This deprecated A5 export carries none.
        export_data["patterns"] = []
        export_data["note"] = "Pooled pattern store removed (1613); see /controls/export (#300)"

        if format == "json":
            return export_data
        elif format == "csv":
            return {
                "status": "success",
                "format": "csv",
                "note": "CSV export not yet implemented, returning JSON",
                "data": export_data,
            }
        else:
            return validation_error(
                message=f"Unsupported format: {format}",
                details={"format": format, "supported": ["json", "csv"]},
            )

    except Exception as e:
        return internal_error(message=f"Failed to export data: {str(e)}", error_id="EXPORT_ERROR")


# @router.post("/controls/privacy/settings")
async def set_privacy_settings(user_id: str, settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set privacy settings for user.

    Privacy settings:
    - share_patterns: Allow pattern sharing across features
    - share_across_users: Allow anonymized pattern sharing
    - data_retention_days: Days to retain learned data (0 = forever)
    - allow_automation: Allow intelligent automation
    - allow_predictive: Allow predictive assistance

    Args:
        user_id: User ID
        settings: Privacy settings dictionary

    Returns:
        Confirmation with settings
    """
    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        # Validate settings
        valid_keys = {
            "share_patterns",
            "share_across_users",
            "data_retention_days",
            "allow_automation",
            "allow_predictive",
        }

        for key in settings:
            if key not in valid_keys:
                return validation_error(
                    message=f"Invalid setting: {key}",
                    details={"invalid_key": key, "valid_keys": list(valid_keys)},
                )

        # Store privacy settings
        preference_manager = UserPreferenceManager()
        await preference_manager.set_preference(user_id, "privacy_settings", settings)

        return {"status": "success", "user_id": user_id, "privacy_settings": settings}

    except Exception as e:
        return internal_error(
            message=f"Failed to set privacy settings: {str(e)}",
            error_id="SET_PRIVACY_ERROR",
        )


# @router.get("/controls/privacy/settings")
async def get_privacy_settings(user_id: str) -> Dict[str, Any]:
    """
    Get current privacy settings for user.

    Args:
        user_id: User ID

    Returns:
        Privacy settings
    """
    from services.domain.user_preference_manager import UserPreferenceManager

    try:
        preference_manager = UserPreferenceManager()
        settings = await preference_manager.get_preference(user_id, "privacy_settings")

        # Default privacy settings
        if settings is None:
            settings = {
                "share_patterns": True,
                "share_across_users": False,  # Conservative default
                "data_retention_days": 0,  # Keep forever by default
                "allow_automation": True,
                "allow_predictive": True,
            }

        return {"user_id": user_id, "privacy_settings": settings}

    except Exception as e:
        return internal_error(
            message=f"Failed to get privacy settings: {str(e)}",
            error_id="GET_PRIVACY_ERROR",
        )


# ============================================================================
# Issue #300 Phase 2 - Database-backed Pattern Management (PRODUCTION)
# ============================================================================

# #1252 (ADR-071 D4): the hardcoded TEST_USER_ID stand-in was removed — every
# pattern route now anchors to the authenticated principal (current_user.user_id
# = users.id) via Depends(get_current_user), closing the cross-user read+write
# leak where any authenticated user operated on one shared test principal's
# patterns.


# Pattern Management Endpoints


@router.get("/patterns")
async def list_patterns(
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    List the authenticated user's learned patterns.

    Returns patterns ordered by most recently used first.

    #1252 (ADR-071 D4): anchored to current_user.user_id (= users.id), not a
    hardcoded TEST_USER_ID — the latter leaked every user's view onto one
    shared principal.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearnedPattern)
                .where(LearnedPattern.user_id == current_user.user_id)
                .order_by(LearnedPattern.last_used_at.desc())
            )
            patterns = result.scalars().all()

            return {
                "patterns": [
                    {
                        "id": str(pattern.id),
                        "pattern_type": pattern.pattern_type.value,
                        "pattern_data": pattern.pattern_data,
                        "confidence": pattern.confidence,
                        "usage_count": pattern.usage_count,
                        "success_count": pattern.success_count,
                        "failure_count": pattern.failure_count,
                        "enabled": pattern.enabled,
                        "last_used_at": (
                            pattern.last_used_at.isoformat() if pattern.last_used_at else None
                        ),
                        "created_at": pattern.created_at.isoformat(),
                        "updated_at": pattern.updated_at.isoformat(),
                    }
                    for pattern in patterns
                ],
                "count": len(patterns),
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to list patterns: {str(e)}",
            error_id="LIST_PATTERNS_ERROR",
        )


@router.get("/patterns/{pattern_id}")
async def get_pattern(
    pattern_id: str, current_user: JWTClaims = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get details of a specific learned pattern.

    Args:
        pattern_id: UUID of the pattern

    Returns:
        Pattern details with full metadata
    """
    try:
        pattern_uuid = UUID(pattern_id)
    except ValueError:
        return validation_error(
            message=f"Invalid pattern ID format: {pattern_id}",
            details={"error_id": "INVALID_PATTERN_ID", "pattern_id": pattern_id},
        )

    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearnedPattern).where(
                    and_(
                        LearnedPattern.id == pattern_uuid,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={"error_id": "PATTERN_NOT_FOUND", "pattern_id": pattern_id},
                )

            return {
                "pattern": {
                    "id": str(pattern.id),
                    "pattern_type": pattern.pattern_type.value,
                    "pattern_data": pattern.pattern_data,
                    "confidence": pattern.confidence,
                    "usage_count": pattern.usage_count,
                    "success_count": pattern.success_count,
                    "failure_count": pattern.failure_count,
                    "enabled": pattern.enabled,
                    "last_used_at": (
                        pattern.last_used_at.isoformat() if pattern.last_used_at else None
                    ),
                    "created_at": pattern.created_at.isoformat(),
                    "updated_at": pattern.updated_at.isoformat(),
                }
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to get pattern: {str(e)}",
            error_id="GET_PATTERN_ERROR",
        )


@router.delete("/patterns/{pattern_id}")
async def delete_pattern(
    pattern_id: str, current_user: JWTClaims = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Delete a learned pattern.

    Args:
        pattern_id: UUID of the pattern to delete

    Returns:
        Success confirmation
    """
    try:
        pattern_uuid = UUID(pattern_id)
    except ValueError:
        return validation_error(
            message=f"Invalid pattern ID format: {pattern_id}",
            details={"error_id": "INVALID_PATTERN_ID", "pattern_id": pattern_id},
        )

    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearnedPattern).where(
                    and_(
                        LearnedPattern.id == pattern_uuid,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={"error_id": "PATTERN_NOT_FOUND", "pattern_id": pattern_id},
                )

            await session.delete(pattern)
            await session.commit()

            return {
                "success": True,
                "message": f"Pattern {pattern_id} deleted successfully",
                "pattern_id": pattern_id,
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to delete pattern: {str(e)}",
            error_id="DELETE_PATTERN_ERROR",
        )


@router.post("/patterns/{pattern_id}/enable")
async def enable_pattern(
    pattern_id: str, current_user: JWTClaims = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Enable a learned pattern.

    Args:
        pattern_id: UUID of the pattern to enable

    Returns:
        Updated pattern with enabled=True
    """
    try:
        pattern_uuid = UUID(pattern_id)
    except ValueError:
        return validation_error(
            message=f"Invalid pattern ID format: {pattern_id}",
            details={"error_id": "INVALID_PATTERN_ID", "pattern_id": pattern_id},
        )

    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.id == pattern_uuid,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
                .with_for_update()
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={"error_id": "PATTERN_NOT_FOUND", "pattern_id": pattern_id},
                )

            pattern.enabled = True
            await session.commit()

            return {
                "success": True,
                "message": f"Pattern {pattern_id} enabled",
                "pattern": {
                    "id": str(pattern.id),
                    "enabled": pattern.enabled,
                },
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to enable pattern: {str(e)}",
            error_id="ENABLE_PATTERN_ERROR",
        )


@router.post("/patterns/{pattern_id}/disable")
async def disable_pattern(
    pattern_id: str, current_user: JWTClaims = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Disable a learned pattern.

    Args:
        pattern_id: UUID of the pattern to disable

    Returns:
        Updated pattern with enabled=False
    """
    try:
        pattern_uuid = UUID(pattern_id)
    except ValueError:
        return validation_error(
            message=f"Invalid pattern ID format: {pattern_id}",
            details={"error_id": "INVALID_PATTERN_ID", "pattern_id": pattern_id},
        )

    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.id == pattern_uuid,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
                .with_for_update()
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={"error_id": "PATTERN_NOT_FOUND", "pattern_id": pattern_id},
                )

            pattern.enabled = False
            await session.commit()

            return {
                "success": True,
                "message": f"Pattern {pattern_id} disabled",
                "pattern": {
                    "id": str(pattern.id),
                    "enabled": pattern.enabled,
                },
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to disable pattern: {str(e)}",
            error_id="DISABLE_PATTERN_ERROR",
        )


@router.post("/patterns/{pattern_id}/execute")
async def execute_pattern(
    pattern_id: str, current_user: JWTClaims = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Execute a pattern action (Phase 4 - proactive execution).

    Called when user clicks "Execute Now" on a proactive suggestion.

    Args:
        pattern_id: UUID of the pattern to execute

    Returns:
        Execution result from ActionRegistry
    """
    # #1465: function-local per file idiom; without this the success path's
    # datetime.now() NameError'd into the failure branch, recording every
    # successful execution as a failure (failure_count += 1, confidence *= 0.9).
    from datetime import datetime, timezone

    try:
        pattern_uuid = UUID(pattern_id)
    except ValueError:
        return validation_error(
            message=f"Invalid pattern ID format: {pattern_id}",
            details={"error_id": "INVALID_PATTERN_ID", "pattern_id": pattern_id},
        )

    try:
        from services.actions.action_registry import ActionRegistry

        async with AsyncSessionFactory.session_scope() as session:
            # Get pattern
            result = await session.execute(
                select(LearnedPattern).where(
                    and_(
                        LearnedPattern.id == pattern_uuid,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={
                        "error_id": "PATTERN_NOT_FOUND",
                        "pattern_id": pattern_id,
                    },
                )

            # Extract action from pattern
            pattern_data = pattern.pattern_data
            action_type = pattern_data.get("action_type")
            action_params = pattern_data.get("action_params", {})

            if not action_type:
                return validation_error(
                    message="Pattern has no action_type defined",
                    details={
                        "error_id": "MISSING_ACTION_TYPE",
                        "pattern_id": pattern_id,
                    },
                )

            # Execute via Action Registry
            try:
                context = {"user_id": pattern.user_id, "pattern_id": pattern.id}

                execution_result = await ActionRegistry.execute(action_type, action_params, context)

                # Record as success
                pattern.success_count += 1
                pattern.confidence = min(pattern.confidence * 1.05, 1.0)
                pattern.updated_at = datetime.now(timezone.utc)
                await session.commit()

                return {
                    "success": True,
                    "message": execution_result.get("message", "Action executed successfully"),
                    "result": execution_result,
                    "pattern": {
                        "id": str(pattern.id),
                        "confidence": round(pattern.confidence, 2),
                        "success_count": pattern.success_count,
                    },
                }

            except Exception as exec_error:
                # Record as failure
                pattern.failure_count += 1
                pattern.confidence *= 0.9
                await session.commit()

                return internal_error(
                    message=f"Execution failed: {str(exec_error)}",
                    error_id="PATTERN_EXECUTION_ERROR",
                )

    except Exception as e:
        return internal_error(
            message=f"Failed to execute pattern: {str(e)}",
            error_id="EXECUTE_PATTERN_ERROR",
        )


# Dashboard Data Controls (Export / Clear)

# #1430 (F19): the Sprint A5 /controls/* handlers above are deprecated and
# unregistered (decorators commented in the #300 supersession) — but the live
# dashboard's Export and Clear buttons still pointed at them with a
# client-supplied user_id (the phantom 'current_user'), so both buttons 404'd.
# These production replacements derive the principal from the authenticated
# session (current_user.user_id = users.id), same as every pattern/settings
# route; a client-supplied user_id is not declared and therefore ignored.


@router.get("/controls/export")
async def export_learning_data(
    format: str = Query("json", description="Export format: json"),
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Export the authenticated user's learning data (settings + patterns).

    Returns:
        JSON payload with the user's learning settings and learned patterns
    """
    from datetime import datetime, timezone

    if format != "json":
        return validation_error(
            message=f"Unsupported format: {format}",
            details={"format": format, "supported": ["json"]},
        )

    try:
        async with AsyncSessionFactory.session_scope() as session:
            settings_result = await session.execute(
                select(LearningSettings).where(LearningSettings.user_id == current_user.user_id)
            )
            settings = settings_result.scalar_one_or_none()

            patterns_result = await session.execute(
                select(LearnedPattern)
                .where(LearnedPattern.user_id == current_user.user_id)
                .order_by(LearnedPattern.created_at.desc())
            )
            patterns = patterns_result.scalars().all()

            return {
                "user_id": str(current_user.user_id),
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "settings": (
                    {
                        "learning_enabled": settings.learning_enabled,
                        "suggestion_threshold": settings.suggestion_threshold,
                        "automation_threshold": settings.automation_threshold,
                        "auto_apply_enabled": settings.auto_apply_enabled,
                        "notification_enabled": settings.notification_enabled,
                    }
                    if settings
                    else {"learning_enabled": True, "configured": False}
                ),
                "patterns": [
                    {
                        "id": str(pattern.id),
                        "pattern_type": pattern.pattern_type.value,
                        "pattern_data": pattern.pattern_data,
                        "confidence": pattern.confidence,
                        "usage_count": pattern.usage_count,
                        "success_count": pattern.success_count,
                        "failure_count": pattern.failure_count,
                        "enabled": pattern.enabled,
                        "created_at": pattern.created_at.isoformat(),
                    }
                    for pattern in patterns
                ],
                "pattern_count": len(patterns),
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to export data: {str(e)}",
            error_id="EXPORT_ERROR",
        )


@router.delete("/controls/data/clear")
async def clear_learning_data(
    data_type: str = Query("all", description="Type of data to clear: all, patterns, settings"),
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Clear the authenticated user's learned data.

    Args:
        data_type: all (patterns + settings), patterns, or settings

    Returns:
        Confirmation with per-type counts of what was cleared
    """
    from datetime import datetime, timezone

    from sqlalchemy import delete as sql_delete

    valid_types = {"all", "patterns", "settings"}
    if data_type not in valid_types:
        return validation_error(
            message=f"Invalid data_type: {data_type}",
            details={"data_type": data_type, "valid_types": sorted(valid_types)},
        )

    try:
        results: Dict[str, Any] = {}
        async with AsyncSessionFactory.session_scope() as session:
            if data_type in ("all", "patterns"):
                deleted = await session.execute(
                    sql_delete(LearnedPattern).where(LearnedPattern.user_id == current_user.user_id)
                )
                results["patterns_cleared"] = deleted.rowcount

            if data_type in ("all", "settings"):
                deleted = await session.execute(
                    sql_delete(LearningSettings).where(
                        LearningSettings.user_id == current_user.user_id
                    )
                )
                results["settings_cleared"] = deleted.rowcount

            await session.commit()

        return {
            "status": "success",
            "user_id": str(current_user.user_id),
            "data_type": data_type,
            "results": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        return internal_error(
            message=f"Failed to clear data: {str(e)}", error_id="CLEAR_DATA_ERROR"
        )


# Learning Settings Endpoints


@router.get("/settings")
async def get_settings(current_user: JWTClaims = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get learning settings for the authenticated user.

    Returns settings or default values if not yet configured.

    #1250 (ADR-071 D4): anchored to the real principal (current_user.user_id =
    users.id), not a hardcoded TEST_USER_ID.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearningSettings).where(LearningSettings.user_id == current_user.user_id)
            )
            settings = result.scalar_one_or_none()

            if not settings:
                # Return defaults if no settings exist yet
                return {
                    "settings": {
                        "learning_enabled": True,
                        "suggestion_threshold": 0.7,
                        "automation_threshold": 0.9,
                        "auto_apply_enabled": False,
                        "notification_enabled": True,
                    },
                    "configured": False,
                }

            return {
                "settings": {
                    "learning_enabled": settings.learning_enabled,
                    "suggestion_threshold": settings.suggestion_threshold,
                    "automation_threshold": settings.automation_threshold,
                    "auto_apply_enabled": settings.auto_apply_enabled,
                    "notification_enabled": settings.notification_enabled,
                    "created_at": settings.created_at.isoformat() if settings.created_at else None,
                    "updated_at": settings.updated_at.isoformat() if settings.updated_at else None,
                },
                "configured": True,
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to get settings: {str(e)}",
            error_id="GET_SETTINGS_ERROR",
        )


class SettingsUpdate(BaseModel):
    """Request model for updating learning settings"""

    learning_enabled: Optional[bool] = None
    suggestion_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    automation_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    auto_apply_enabled: Optional[bool] = None
    notification_enabled: Optional[bool] = None


class PatternFeedback(BaseModel):
    """Request model for pattern suggestion feedback (Phase 3)"""

    action: str = Field(..., description="Feedback action: 'accept', 'reject', or 'dismiss'")
    feedback_text: Optional[str] = Field(None, description="Optional user feedback text")


@router.put("/settings")
async def update_settings(
    settings_update: SettingsUpdate,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Update learning settings for the authenticated user.

    Creates settings if they don't exist, updates if they do.

    #1250 (ADR-071 D4): anchored to the real principal (current_user.user_id =
    users.id FK), not a hardcoded TEST_USER_ID — the latter violated the
    learning_settings→users FK, so the toggle had never worked.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            result = await session.execute(
                select(LearningSettings)
                .where(LearningSettings.user_id == current_user.user_id)
                .with_for_update()
            )
            settings = result.scalar_one_or_none()

            if not settings:
                # Create new settings
                settings = LearningSettings(
                    user_id=current_user.user_id,
                    learning_enabled=(
                        settings_update.learning_enabled
                        if settings_update.learning_enabled is not None
                        else True
                    ),
                    suggestion_threshold=settings_update.suggestion_threshold or 0.7,
                    automation_threshold=settings_update.automation_threshold or 0.9,
                    auto_apply_enabled=settings_update.auto_apply_enabled or False,
                    notification_enabled=(
                        settings_update.notification_enabled
                        if settings_update.notification_enabled is not None
                        else True
                    ),
                )
                session.add(settings)
            else:
                # Update existing settings
                if settings_update.learning_enabled is not None:
                    settings.learning_enabled = settings_update.learning_enabled
                if settings_update.suggestion_threshold is not None:
                    settings.suggestion_threshold = settings_update.suggestion_threshold
                if settings_update.automation_threshold is not None:
                    settings.automation_threshold = settings_update.automation_threshold
                if settings_update.auto_apply_enabled is not None:
                    settings.auto_apply_enabled = settings_update.auto_apply_enabled
                if settings_update.notification_enabled is not None:
                    settings.notification_enabled = settings_update.notification_enabled

            await session.commit()

            return {
                "success": True,
                "message": "Settings updated successfully",
                "settings": {
                    "learning_enabled": settings.learning_enabled,
                    "suggestion_threshold": settings.suggestion_threshold,
                    "automation_threshold": settings.automation_threshold,
                    "auto_apply_enabled": settings.auto_apply_enabled,
                    "notification_enabled": settings.notification_enabled,
                },
            }
    except Exception as e:
        return internal_error(
            message=f"Failed to update settings: {str(e)}",
            error_id="UPDATE_SETTINGS_ERROR",
        )


# ============================================================================
# Phase 3: Pattern Feedback Endpoint
# ============================================================================


@router.post("/patterns/{pattern_id}/feedback")
async def provide_pattern_feedback(
    pattern_id: UUID,
    feedback: PatternFeedback,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Submit feedback on a pattern suggestion (Phase 3).

    Actions:
    - 'accept': Increase confidence (* 1.1, cap at 1.0), success_count += 2
    - 'reject': Decrease confidence (* 0.5), failure_count += 2
    - 'dismiss': No confidence change, just track dismissal

    This endpoint is called by the frontend suggestion UI when users
    interact with pattern suggestion cards.
    """
    try:
        async with AsyncSessionFactory.session_scope() as session:
            # Get pattern with row lock
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.id == pattern_id,
                        LearnedPattern.user_id == current_user.user_id,
                    )
                )
                .with_for_update()
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                return not_found_error(
                    message=f"Pattern {pattern_id} not found",
                    details={"error_id": "PATTERN_NOT_FOUND"},
                )

            # Apply feedback based on action
            action = feedback.action.lower()

            if action == "accept":
                # Increase confidence
                pattern.confidence = min(1.0, pattern.confidence * 1.1)
                pattern.success_count += 2
                message = "Pattern accepted - confidence increased"

            elif action == "reject":
                # Decrease confidence
                pattern.confidence = pattern.confidence * 0.5
                pattern.failure_count += 2

                # Auto-disable if confidence falls below threshold
                if pattern.confidence < 0.3:
                    pattern.enabled = False
                    message = "Pattern rejected - confidence decreased and pattern disabled"
                else:
                    message = "Pattern rejected - confidence decreased"

            elif action == "dismiss":
                # No confidence change, just track
                message = "Pattern dismissed"

            else:
                return validation_error(
                    message=f"Invalid action: {action}. Must be 'accept', 'reject', or 'dismiss'",
                    details={"error_id": "INVALID_FEEDBACK_ACTION"},
                )

            await session.commit()

            return {
                "success": True,
                "message": message,
                "pattern": {
                    "id": str(pattern.id),
                    "confidence": round(pattern.confidence, 2),
                    "success_count": pattern.success_count,
                    "failure_count": pattern.failure_count,
                    "enabled": pattern.enabled,
                },
            }

    except Exception as e:
        return internal_error(
            message=f"Failed to submit feedback: {str(e)}",
            error_id="FEEDBACK_SUBMISSION_ERROR",
        )
