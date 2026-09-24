"""
Preference Management API Routes

Endpoints for:
- Accepting/dismissing preference suggestions
- Viewing user preferences
- Managing personality profile settings

Issue #248: CONV-LEARN-PREF - Conversational Preference Gathering
"""

import logging
from typing import Any, Dict, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from services.auth.auth_middleware import get_current_user
from services.database.session_factory import AsyncSessionFactory
from services.domain.user_preference_manager import UserPreferenceManager
from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.personality.personality_profile import PersonalityProfile
from services.utils.datetime_utils import DEFAULT_USER_TIMEZONE

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/preferences", tags=["preferences"])

# Service instances
preference_manager = UserPreferenceManager()
preference_handler = PreferenceDetectionHandler()


# ============================================================================
# Request/Response Models
# ============================================================================


class AcceptPreferenceRequest(BaseModel):
    """Request to accept a preference suggestion"""

    hint_id: str = Field(..., description="ID of the preference hint to accept")
    session_id: Optional[str] = Field(None, description="Current session ID")


class PreferenceResponse(BaseModel):
    """Standard response for preference operations"""

    success: bool
    message: str
    dimension: Optional[str] = None
    previous_value: Optional[Any] = None
    new_value: Optional[Any] = None


class TimezoneResponse(BaseModel):
    """#1876 — the caller's reminder-timezone preference."""

    timezone: str = Field(..., description="IANA timezone name, e.g. 'Europe/Helsinki'")
    is_default: bool = Field(
        ...,
        description=(
            "True when this value is DEFAULT_USER_TIMEZONE because nothing has ever "
            "been set for this user (not a real preference the user chose) — the "
            "settings page reads this to decide whether to show the browser-zone nudge."
        ),
    )


class SetTimezoneRequest(BaseModel):
    """#1876 — PUT body for setting the reminder timezone."""

    timezone: str = Field(..., description="IANA timezone name, e.g. 'Europe/Helsinki'")


# ============================================================================
# Endpoints
# ============================================================================


@router.post("/hints/{hint_id}/accept", response_model=PreferenceResponse)
async def accept_preference(
    hint_id: str,
    request: AcceptPreferenceRequest,
    current_user: Any = Depends(get_current_user),
) -> PreferenceResponse:
    """
    Accept a preference suggestion from the system.

    When a user clicks "Apply" on a preference suggestion, this endpoint:
    1. Confirms the preference in UserPreferenceManager
    2. Updates PersonalityProfile
    3. Logs to learning system
    4. Triggers preference application

    Args:
        hint_id: ID of the preference hint
        request: Request containing session_id
        current_user: Authenticated user

    Returns:
        PreferenceResponse with status and updated values
    """
    try:
        user_id = str(current_user.user_id)
        session_id = request.session_id

        logger.info(f"User {user_id} accepted preference hint {hint_id}")

        # Confirm the preference through the handler
        result = await preference_handler.confirm_preference(
            user_id=user_id,
            session_id=session_id,
            hint_id=hint_id,
            accepted=True,
        )

        if not result.get("success"):
            logger.warning(f"Failed to confirm preference for {user_id}: {result}")
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Failed to apply preference"),
            )

        return PreferenceResponse(
            success=True,
            message="Preference updated successfully!",
            dimension=result.get("dimension"),
            new_value=result.get("new_value"),
            previous_value=result.get("previous_value"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accepting preference: {e}")
        raise HTTPException(status_code=500, detail="Error applying preference")


@router.post("/hints/{hint_id}/dismiss", response_model=PreferenceResponse)
async def dismiss_preference(
    hint_id: str,
    request: AcceptPreferenceRequest,
    current_user: Any = Depends(get_current_user),
) -> PreferenceResponse:
    """
    Dismiss a preference suggestion.

    When a user clicks "Dismiss" on a preference suggestion:
    1. Log the dismissal for learning system
    2. Remove suggestion from UI
    3. Optionally track for preference refinement

    Args:
        hint_id: ID of the preference hint
        request: Request containing session_id
        current_user: Authenticated user

    Returns:
        PreferenceResponse with dismiss status
    """
    try:
        user_id = str(current_user.user_id)
        session_id = request.session_id

        logger.info(f"User {user_id} dismissed preference hint {hint_id}")

        # Log dismissal (for future learning system refinement)
        result = await preference_handler.confirm_preference(
            user_id=user_id,
            session_id=session_id,
            hint_id=hint_id,
            accepted=False,  # Dismissed, not accepted
        )

        return PreferenceResponse(
            success=True,
            message="Suggestion dismissed",
        )

    except Exception as e:
        logger.error(f"Error dismissing preference: {e}")
        # Dismissal failures are not critical, still return success
        return PreferenceResponse(
            success=True,
            message="Suggestion dismissed",
        )


@router.get("/profile", response_model=Dict[str, Any])
async def get_preference_profile(
    current_user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get user's current personality preference profile.

    Returns:
        Dict with all 4 personality dimensions:
        - warmth_level: 0.0-1.0
        - confidence_style: enum
        - action_orientation: enum
        - technical_depth: enum
    """
    try:
        user_id = str(current_user.user_id)
        profile = await PersonalityProfile.load_with_preferences(user_id)

        return {
            "user_id": user_id,
            "warmth_level": profile.warmth_level,
            "confidence_style": profile.confidence_style.value,
            "action_orientation": profile.action_orientation.value,
            "technical_depth": profile.technical_depth.value,
            "created_at": profile.created_at.isoformat(),
            "updated_at": profile.updated_at.isoformat(),
        }

    except Exception as e:
        logger.error(f"Error loading preference profile: {e}")
        raise HTTPException(status_code=500, detail="Error loading preferences")


@router.get("/stats", response_model=Dict[str, Any])
async def get_preference_stats(
    current_user: Any = Depends(get_current_user),
) -> Dict[str, Any]:
    """
    Get statistics about user's preference changes over time.

    Returns:
        Dict with stats:
        - total_hints_detected: count
        - total_hints_accepted: count
        - total_hints_dismissed: count
        - acceptance_rate: percentage
        - dimensions_changed: list of dimensions user has customized
    """
    try:
        user_id = str(current_user.user_id)

        # Get stored preferences to track changes
        # This is a placeholder for more sophisticated tracking
        preferences = await preference_manager.get_preference(
            user_id=user_id, key="personality_stats"
        )

        if preferences:
            # get_preference returns the VALUE (a dict here), not a PreferenceItem —
            # the old `.value` access could never have worked (nothing ever set
            # this key, so nothing ever reached it).
            return preferences
        else:
            # Return default stats
            return {
                "total_hints_detected": 0,
                "total_hints_accepted": 0,
                "total_hints_dismissed": 0,
                "acceptance_rate": 0.0,
                "dimensions_changed": [],
                "user_id": user_id,
            }

    except Exception as e:
        logger.error(f"Error getting preference stats: {e}")
        raise HTTPException(status_code=500, detail="Error loading statistics")


# ============================================================================
# Timezone (#1876 — UserPreferenceManager.set_reminder_timezone had zero callers)
# ============================================================================


@router.get("/timezone", response_model=TimezoneResponse)
async def get_timezone(
    current_user: Any = Depends(get_current_user),
) -> TimezoneResponse:
    """The caller's reminder timezone (#1574's store). Principal comes from the
    session (#1252 P6) — never a client-supplied id."""
    tz = await preference_manager.get_reminder_timezone(current_user.user_id)
    return TimezoneResponse(timezone=tz, is_default=(tz == DEFAULT_USER_TIMEZONE))


@router.put("/timezone", response_model=TimezoneResponse)
async def set_timezone(
    request: SetTimezoneRequest,
    current_user: Any = Depends(get_current_user),
) -> TimezoneResponse:
    """Set the caller's reminder timezone.

    Validation is `set_reminder_timezone`'s own (`_validate_timezone`, checked
    against `zoneinfo.available_timezones()` + a `ZoneInfo()` construction) —
    no duplicate check here, so there is exactly one place that decides what
    counts as a valid zone. An unknown name raises `ValueError`; that becomes
    an honest 400 naming the bad value, never a silent fallback to the default.
    """
    try:
        await preference_manager.set_reminder_timezone(current_user.user_id, request.timezone)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    return TimezoneResponse(
        timezone=request.timezone, is_default=(request.timezone == DEFAULT_USER_TIMEZONE)
    )


# ============================================================================
# Health Check
# ============================================================================


@router.get("/health")
async def preferences_health() -> Dict[str, str]:
    """
    Health check endpoint for preferences service.

    Returns:
        Dict with service status
    """
    try:
        # Verify handler is initialized
        _ = preference_handler.analyzer
        return {"status": "healthy", "service": "preferences"}
    except Exception as e:
        logger.error(f"Preferences service health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
