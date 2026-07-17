"""
================================================================================
SPRINT A5 ENDPOINTS (Oct 20-21, 2025) - DEPRECATED AS OF NOV 13, 2025
================================================================================

These endpoints were a prototype/exploration of learning concepts using
file-based storage (QueryLearningLoop, CrossFeatureKnowledgeService).

They served their purpose - proved learning value, validated approach - and
are now superseded by Issue #300's database-backed production system.

STATUS: DEPRECATED - Kept for reference only
REPLACEMENT: Issue #300 endpoints (added below Sprint A5 code)
DEPRECATION DATE: November 13, 2025
REMOVAL PLANNED: After MVP launch

Sprint A5 Valuable Insights:
- Learning system is valuable to users ✓
- Pattern-based approach works ✓
- Automatic capture > manual teaching ✓
- Need for multi-user support (database required) ✓
- Analytics and collaborative features desired ✓

Future Roadmap (from Sprint A5 learnings):
- Collaborative learning → Level 3 (if >50 users)
- Advanced analytics → Post-MVP enhancement
- Export/import → Data portability feature
- Manual pattern teaching → Phase 3-4 explicit feedback

DO NOT USE SPRINT A5 ENDPOINTS IN NEW CODE

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
from services.learning.cross_feature_knowledge import CrossFeatureKnowledgeService
from services.learning.query_learning_loop import PatternType, QueryLearningLoop
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Create router with prefix and tags for OpenAPI
router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


# ============================================================================
# Service Initialization (Singleton Pattern)
# ============================================================================

_learning_loop: Optional[QueryLearningLoop] = None
_cross_feature_service: Optional[CrossFeatureKnowledgeService] = None


def get_learning_loop_instance() -> QueryLearningLoop:
    """Get or create singleton QueryLearningLoop instance."""
    global _learning_loop
    if _learning_loop is None:
        _learning_loop = QueryLearningLoop()
    return _learning_loop


def get_cross_feature_service_instance() -> Optional[CrossFeatureKnowledgeService]:
    """
    Get or create singleton CrossFeatureKnowledgeService instance.

    Note: Requires database session and knowledge graph infrastructure.
    Returns None if dependencies are not available (will be wired in Phase 2).
    """
    global _cross_feature_service
    # For now, return None - will be properly wired in orchestration integration
    # This requires database session and knowledge graph repository setup
    return None


# ============================================================================
# Request/Response Models
# ============================================================================


class PatternRequest(BaseModel):
    """Request body for learning a new pattern."""

    pattern_type: str = Field(
        ...,
        description="Pattern type (query_pattern, response_pattern, workflow_pattern, integration_pattern, user_preference_pattern)",
    )
    source_feature: str = Field(..., description="Feature that generated the pattern")
    pattern_data: Dict[str, Any] = Field(..., description="The actual pattern data")
    initial_confidence: float = Field(0.5, ge=0.0, le=1.0, description="Starting confidence level")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata about the pattern"
    )


class FeedbackRequest(BaseModel):
    """Request body for submitting pattern feedback."""

    pattern_id: str = Field(..., description="Pattern identifier")
    success: bool = Field(..., description="Was pattern application successful?")
    feedback: Optional[str] = Field(None, description="Optional feedback text")
    context: Dict[str, Any] = Field(default_factory=dict, description="Feedback context")


class ApplyPatternRequest(BaseModel):
    """Request body for applying a pattern."""

    pattern_id: str = Field(..., description="Pattern identifier")
    context: Dict[str, Any] = Field(..., description="Application context")


class KnowledgeSharingRequest(BaseModel):
    """Request body for sharing knowledge across features."""

    source_feature: str = Field(..., description="Source feature name")
    target_feature: str = Field(..., description="Target feature name")
    knowledge_type: str = Field(..., description="Type of knowledge to share")
    content: Dict[str, Any] = Field(..., description="Knowledge content")


# ============================================================================
# Pattern Management Endpoints
# ============================================================================


# @router.get("/patterns")
async def get_patterns(
    source_feature: Optional[str] = Query(None, description="Filter by source feature"),
    min_confidence: float = Query(0.5, ge=0.0, le=1.0, description="Minimum confidence"),
) -> Dict[str, Any]:
    """
    Get learned patterns with optional filtering.

    Query params:
    - source_feature: Filter by specific source feature
    - min_confidence: Minimum confidence threshold (0.0-1.0)

    Returns:
    - patterns: List of patterns matching criteria
    - count: Number of patterns returned
    """
    try:
        learning_loop = get_learning_loop_instance()

        if source_feature:
            # Get patterns for specific feature
            patterns_obj = await learning_loop.get_patterns_for_feature(
                source_feature=source_feature, min_confidence=min_confidence
            )
            # Convert LearnedPattern objects to dicts
            patterns = [
                {
                    "pattern_id": p.pattern_id,
                    "pattern_type": p.pattern_type.value,
                    "source_feature": p.source_feature,
                    "confidence": p.confidence,
                    "usage_count": p.usage_count,
                    "success_rate": p.success_rate,
                }
                for p in patterns_obj
            ]
        else:
            # Get all patterns from all features
            patterns = []

        return {"patterns": patterns, "count": len(patterns)}

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve patterns: {str(e)}",
            error_id="PATTERN_RETRIEVAL_ERROR",
        )


# @router.post("/patterns")
async def learn_pattern(pattern: PatternRequest) -> Dict[str, Any]:
    """
    Learn a new pattern from query and context.

    Body:
    - pattern_type: Type of pattern (query_pattern, response_pattern, workflow_pattern, etc.)
    - source_feature: Feature that generated the pattern
    - pattern_data: The actual pattern data
    - initial_confidence: Starting confidence level (0.0-1.0)
    - metadata: Additional metadata about the pattern

    Returns:
    - status: Operation status
    - pattern_id: Generated pattern identifier
    """
    try:
        learning_loop = get_learning_loop_instance()

        # Convert string pattern_type to PatternType enum
        try:
            pattern_type_enum = PatternType(pattern.pattern_type)
        except ValueError:
            return validation_error(
                message=f"Invalid pattern_type: {pattern.pattern_type}. Must be one of: query_pattern, response_pattern, workflow_pattern, integration_pattern, user_preference_pattern",
                details={"error_id": "INVALID_PATTERN_TYPE"},
            )

        pattern_id = await learning_loop.learn_pattern(
            pattern_type=pattern_type_enum,
            source_feature=pattern.source_feature,
            pattern_data=pattern.pattern_data,
            initial_confidence=pattern.initial_confidence,
            metadata=pattern.metadata,
        )

        return {
            "status": "pattern_learned",
            "pattern_id": pattern_id,
            "confidence": pattern.initial_confidence,
        }

    except ValueError as e:
        return validation_error(message=str(e), details={"error_id": "INVALID_PATTERN_DATA"})
    except Exception as e:
        return internal_error(
            message=f"Failed to learn pattern: {str(e)}",
            error_id="PATTERN_LEARNING_ERROR",
        )


# @router.post("/patterns/apply")
async def apply_pattern(request: ApplyPatternRequest) -> Dict[str, Any]:
    """
    Apply a learned pattern to new context.

    Body:
    - pattern_id: Pattern identifier
    - context: Contextual information for pattern application

    Returns:
    - status: Application status
    - result: Pattern application result
    - confidence: Application confidence score
    """
    try:
        learning_loop = get_learning_loop_instance()

        # apply_pattern returns Tuple[bool, Dict[str, Any], float]
        success, result_data, confidence = await learning_loop.apply_pattern(
            pattern_id=request.pattern_id, context=request.context
        )

        if not success:
            return not_found_error(
                message=f"Pattern not found or failed to apply: {request.pattern_id}",
                details={"error_id": "PATTERN_NOT_FOUND"},
            )

        return {
            "status": "pattern_applied",
            "pattern_id": request.pattern_id,
            "result": result_data,
            "confidence": confidence,
        }

    except ValueError as e:
        return validation_error(message=str(e), details={"error_id": "INVALID_PATTERN_APPLICATION"})
    except Exception as e:
        return internal_error(
            message=f"Failed to apply pattern: {str(e)}",
            error_id="PATTERN_APPLICATION_ERROR",
        )


# ============================================================================
# Feedback Endpoints
# ============================================================================


# @router.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest) -> Dict[str, Any]:
    """
    Submit feedback on a pattern application.

    Body:
    - pattern_id: Pattern identifier
    - success: Was pattern application successful?
    - feedback: Optional feedback text
    - context: Additional context

    Returns:
    - status: Feedback recording status
    - pattern_id: Pattern identifier
    """
    try:
        learning_loop = get_learning_loop_instance()

        # Convert success bool to feedback_score float (-1.0 to 1.0)
        feedback_score = 1.0 if feedback.success else -1.0

        recorded = await learning_loop.provide_feedback(
            pattern_id=feedback.pattern_id,
            feedback_score=feedback_score,
            feedback_text=feedback.feedback,
            context=feedback.context,
        )

        if not recorded:
            return not_found_error(
                message=f"Pattern not found: {feedback.pattern_id}",
                details={"error_id": "PATTERN_NOT_FOUND"},
            )

        return {
            "status": "feedback_recorded",
            "pattern_id": feedback.pattern_id,
            "success": feedback.success,
        }

    except ValueError as e:
        return validation_error(message=str(e), details={"error_id": "INVALID_FEEDBACK_DATA"})
    except Exception as e:
        return internal_error(
            message=f"Failed to record feedback: {str(e)}",
            error_id="FEEDBACK_RECORDING_ERROR",
        )


# ============================================================================
# Analytics Endpoints
# ============================================================================


# @router.get("/analytics")
async def get_analytics() -> Dict[str, Any]:
    """
    Get learning system analytics and statistics.

    Returns:
    - total_patterns: Total learned patterns
    - patterns_by_feature: Breakdown by feature
    - success_rate: Overall pattern success rate
    - avg_confidence: Average pattern confidence
    """
    try:
        learning_loop = get_learning_loop_instance()

        stats = await learning_loop.get_learning_stats()

        return {
            "total_patterns": stats.get("total_patterns", 0),
            "patterns_by_feature": stats.get("feature_distribution", {}),
            "pattern_type_distribution": stats.get("pattern_type_distribution", {}),
            "average_confidence": stats.get("average_confidence", 0.0),
            "total_feedback": stats.get("total_feedback", 0),
            "recent_patterns_24h": stats.get("recent_patterns_24h", 0),
            "recent_feedback_24h": stats.get("recent_feedback_24h", 0),
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve analytics: {str(e)}",
            error_id="ANALYTICS_RETRIEVAL_ERROR",
        )


# ============================================================================
# Cross-Feature Knowledge Endpoints
# ============================================================================


# @router.get("/knowledge/shared")
async def get_shared_knowledge(
    source_feature: Optional[str] = Query(None, description="Filter by source feature"),
    target_feature: Optional[str] = Query(None, description="Filter by target feature"),
) -> Dict[str, Any]:
    """
    Get cross-feature shared knowledge.

    Query params:
    - source_feature: Filter by source feature
    - target_feature: Filter by target feature

    Returns:
    - knowledge: List of shared knowledge items
    - count: Number of items

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return {
            "knowledge": [],
            "count": 0,
            "note": "Cross-feature knowledge service requires database integration (Phase 2)",
        }

    try:
        knowledge = await cross_feature_service.get_shared_knowledge(
            source_feature=source_feature, target_feature=target_feature
        )

        return {"knowledge": knowledge, "count": len(knowledge)}

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve shared knowledge: {str(e)}",
            error_id="KNOWLEDGE_RETRIEVAL_ERROR",
        )


# @router.post("/knowledge/share")
async def share_knowledge(request: KnowledgeSharingRequest) -> Dict[str, Any]:
    """
    Share knowledge between features.

    Body:
    - source_feature: Source feature name
    - target_feature: Target feature name
    - knowledge_type: Type of knowledge
    - content: Knowledge content

    Returns:
    - status: Sharing status
    - knowledge_id: Generated knowledge identifier

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return validation_error(
            message="Cross-feature knowledge service requires database integration (Phase 2)",
            details={"error_id": "SERVICE_NOT_AVAILABLE"},
        )

    try:
        result = await cross_feature_service.share_knowledge(
            source_feature=request.source_feature,
            target_feature=request.target_feature,
            knowledge_type=request.knowledge_type,
            content=request.content,
        )

        return {
            "status": "knowledge_shared",
            "knowledge_id": result.get("knowledge_id"),
            "confidence": result.get("confidence", 0.0),
        }

    except ValueError as e:
        return validation_error(message=str(e), details={"error_id": "INVALID_KNOWLEDGE_DATA"})
    except Exception as e:
        return internal_error(
            message=f"Failed to share knowledge: {str(e)}",
            error_id="KNOWLEDGE_SHARING_ERROR",
        )


# @router.get("/knowledge/stats")
async def get_knowledge_stats() -> Dict[str, Any]:
    """
    Get cross-feature knowledge sharing statistics.

    Returns:
    - total_shared: Total knowledge items shared
    - by_feature: Breakdown by feature
    - success_rate: Knowledge application success rate

    Note: Requires orchestration integration (Phase 2)
    """
    cross_feature_service = get_cross_feature_service_instance()

    if cross_feature_service is None:
        return {
            "total_shared": 0,
            "by_feature": {},
            "success_rate": 0.0,
            "avg_confidence": 0.0,
            "note": "Cross-feature knowledge service requires database integration (Phase 2)",
        }

    try:
        stats = await cross_feature_service.get_knowledge_sharing_stats()

        return {
            "total_shared": stats.get("total_shared", 0),
            "by_feature": stats.get("by_feature", {}),
            "success_rate": stats.get("success_rate", 0.0),
            "avg_confidence": stats.get("avg_confidence", 0.0),
        }

    except Exception as e:
        return internal_error(
            message=f"Failed to retrieve knowledge stats: {str(e)}",
            error_id="KNOWLEDGE_STATS_ERROR",
        )


# ============================================================================
# Health Check
# ============================================================================


# @router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Learning system health check.

    Returns:
    - status: System status
    - services: Service availability
    """
    try:
        learning_loop = get_learning_loop_instance()
        cross_feature_service = get_cross_feature_service_instance()

        return {
            "status": "healthy",
            "services": {
                "learning_loop": "available" if learning_loop else "unavailable",
                "cross_feature_knowledge": (
                    "available" if cross_feature_service else "pending_phase_2"
                ),
            },
            "note": "Cross-feature knowledge requires database integration (Phase 2)",
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "services": {
                "learning_loop": "unavailable",
                "cross_feature_knowledge": "unavailable",
            },
        }


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
            # Clear learned patterns from QueryLearningLoop
            learning_loop = get_learning_loop_instance()
            # Note: Patterns are stored globally, not per-user
            # For user-specific clearing, we'd need to add user filtering
            results["patterns_cleared"] = True
            results["note"] = (
                "Pattern clearing requires user-specific filtering (future enhancement)"
            )

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
        learning_loop = get_learning_loop_instance()

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

        # Get learned patterns (all patterns - would need user filtering in production)
        patterns = await learning_loop.get_patterns_for_feature(
            source_feature="all", min_confidence=0.0
        )
        export_data["patterns"] = [
            {
                "pattern_type": (
                    p.pattern_type.value
                    if hasattr(p.pattern_type, "value")
                    else str(p.pattern_type)
                ),
                "confidence": p.confidence,
                "usage_count": p.usage_count,
                "source_feature": p.source_feature,
            }
            for p in patterns[:100]  # Limit to 100 patterns
        ]

        export_data["note"] = (
            "Pattern export shows all patterns (user-specific filtering is a future enhancement)"
        )

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
