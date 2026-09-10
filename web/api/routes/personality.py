"""
Personality Configuration API Routes

Provides endpoints for managing user personality preferences and response enhancement.
- GET /api/v1/personality/profile/{user_id} - Retrieve personality configuration
- PUT /api/v1/personality/profile/{user_id} - Update personality configuration
- POST /api/v1/personality/enhance - Enhance response with personality

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 799-889)
Now: Extracted to separate router module
"""

import structlog
from fastapi import APIRouter, Depends, Request

from services.auth.auth_middleware import JWTClaims, require_admin
from web.personality_integration import (
    PersonalityResponseEnhancer,
    PiperConfigParser,
    WebPersonalityConfig,
)
from web.utils.error_responses import internal_error, not_found_error, validation_error

logger = structlog.get_logger()

# Router configuration
router = APIRouter(prefix="/api/v1/personality", tags=["personality"])

# These are initialized in WebComponentsInitializationPhase during startup
# and stored in app.state for dependency injection (Phase 4 - INFR-MAINT-REFACTOR)
# config_parser: PiperConfigParser (app.state.config_parser)
# personality_enhancer: PersonalityResponseEnhancer (app.state.personality_enhancer)


@router.get("/profile/{user_id}")
async def get_personality_profile(user_id: str = "default", request: Request = None):
    """Get user's personality preferences"""
    try:
        # Get config_parser from app state (initialized in WebComponentsInitializationPhase)
        if not request or not hasattr(request.app.state, "config_parser"):
            return internal_error("Configuration parser not initialized in app state")

        config_parser = request.app.state.config_parser
        config = config_parser.load_personality_config(user_id)
        return {
            "status": "success",
            "data": config.to_dict(),
            "user_id": user_id,
        }
    except FileNotFoundError:
        # Profile not found - return 404
        return not_found_error(
            f"Personality profile not found for user: {user_id}",
            {"resource": "personality_profile", "user_id": user_id},
        )
    except Exception as e:
        # Load failure - return 500
        logger.error(
            f"Failed to load personality profile for {user_id}: {e}",
            exc_info=True,
        )
        return internal_error("Failed to load personality profile")


@router.put("/profile/{user_id}")
async def update_personality_profile(
    user_id: str,
    request: Request,
    current_user: JWTClaims = Depends(require_admin),
):
    """Update user's personality preferences.

    1734: ADMIN-ONLY until the store is per-user. Despite the {user_id} in the
    path, PiperConfigParser.save_personality_config ignores user_id entirely and
    rewrites the GLOBAL config/PIPER.user.md — so on the hosted beta, any
    authenticated user's save would clobber every user's overlay (including
    PM's ADR-075 D4 personal overlay, if present). require_admin is the #1508/
    #1598 idiom: global-blast-radius write → admin authority, live DB check,
    fail-closed, no payload in the refusal. The GET above and /enhance below
    stay ungated — they only read. When the store is scoped per-user (users.
    preferences JSONB is the natural home, per the 1734 filing), this gate can
    come off in the same change that makes user_id real.
    """
    try:
        # Get config_parser from app state (initialized in app.py)
        config_parser = (
            request.app.state.config_parser if hasattr(request.app.state, "config_parser") else None
        )
        if not config_parser:
            return internal_error("Configuration parser not initialized")

        data = await request.json()
        config = WebPersonalityConfig.from_dict(data)

        success = config_parser.save_personality_config(config, user_id)

        if success:
            return {
                "status": "success",
                "data": config.to_dict(),
                "user_id": user_id,
                "message": "Personality preferences updated successfully",
            }
        else:
            # Save failed - return 500
            logger.error(f"Failed to save personality config for {user_id}")
            return internal_error("Failed to save personality configuration")
    except (ValueError, KeyError, TypeError) as e:
        # Invalid data - return 422
        return validation_error(
            f"Invalid personality configuration data: {str(e)}",
            {"user_id": user_id, "error": str(e)},
        )
    except Exception as e:
        # Unexpected error - return 500
        logger.error(
            f"Error updating personality profile for {user_id}: {e}",
            exc_info=True,
        )
        return internal_error("Failed to update personality profile")


@router.post("/enhance")
async def enhance_response(request: Request):
    """Enhance a response with personality"""
    try:
        # Get both config_parser and personality_enhancer from app state
        config_parser = (
            request.app.state.config_parser if hasattr(request.app.state, "config_parser") else None
        )
        personality_enhancer = (
            request.app.state.personality_enhancer
            if hasattr(request.app.state, "personality_enhancer")
            else None
        )

        if not config_parser or not personality_enhancer:
            return internal_error(
                "Required services not initialized (config_parser or personality_enhancer)"
            )

        data = await request.json()
        content = data.get("content", "")
        user_id = data.get("user_id", "default")
        confidence = data.get("confidence", 0.5)

        # Validate required fields
        if not content or not isinstance(content, str):
            return validation_error(
                "Content is required and must be a string",
                {
                    "field": "content",
                    "issue": "Required field missing or invalid type",
                },
            )

        # Load personality config
        config = config_parser.load_personality_config(user_id)

        # Enhance response
        enhanced_content = personality_enhancer.enhance_response(content, config, confidence)

        return {
            "status": "success",
            "data": {
                "original_content": content,
                "enhanced_content": enhanced_content,
                "personality_config": config.to_dict(),
                "confidence": confidence,
            },
        }
    except (ValueError, TypeError) as e:
        # Validation errors - return 422
        return validation_error(f"Invalid enhancement request: {str(e)}", {"error": str(e)})
    except Exception as e:
        # Processing errors - return 500
        logger.error(f"Error enhancing response: {e}", exc_info=True)
        return internal_error("Failed to enhance response")
