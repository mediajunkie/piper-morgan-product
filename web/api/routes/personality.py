"""
Personality Configuration API Routes

Provides endpoints for managing personality preferences and response enhancement.
- GET  /api/v1/personality/profile - Retrieve personality configuration
- PUT  /api/v1/personality/profile - Update personality configuration (admin)
- POST /api/v1/personality/enhance - Enhance response with personality

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 799-889)
Now: Extracted to separate router module

#1751 (2026-09-13): THE PRINCIPAL COMES FROM THE SESSION, NEVER FROM THE CLIENT.
These routes used to take the principal from the caller — a `{user_id}` path
segment on GET/PUT (GET had no auth dependency at all) and a `user_id` key in
/enhance's request body — and the canonical template hardcoded `"default"` into
all three call sites. That is the multi-tenancy shape #1419/#1734 name: a
client-supplied principal on a write path. Both inputs are now REMOVED rather
than validated, so there is nowhere for a caller to write another principal
down; `Depends(get_current_user)` / `Depends(require_admin)` supply it.

⚠️ SCOPE, stated honestly (m-43): this closes the client-supplied-principal
hole. It does NOT create per-user data separation, because there is no per-user
store — `PiperConfigParser` ignores the user_id it is handed and reads/writes
one instance-wide file, `config/PIPER.user.md` (ADR-075 D4). Hence the literal
`"scope": "instance"` in the responses: the payload says what it is, so a
client cannot mistake the principal echo for evidence the data is private.
The session-derived id is still threaded into the parser calls to keep the
seam that a real per-user store (`users.preferences` JSONB, #1422) would need.
Pins: tests/unit/web/api/routes/test_personality_principal_from_session_1751.py
"""

import structlog
from fastapi import APIRouter, Depends, Request

from services.auth.auth_middleware import JWTClaims, get_current_user, require_admin
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


@router.get("/profile")
async def get_personality_profile(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Get the personality configuration for the authenticated session.

    #1751: was `GET /profile/{user_id}` with NO auth dependency — any caller
    could name any principal in the path and the response echoed it back as
    though it were that user's profile. The path segment is gone; the id comes
    from the session. The read stays open to any authenticated user (1734
    scoped its admin gate to the PUT, and the data is instance-wide anyway).
    """
    user_id = str(current_user.user_id)
    try:
        # Get config_parser from app state (initialized in WebComponentsInitializationPhase)
        if not hasattr(request.app.state, "config_parser"):
            return internal_error("Configuration parser not initialized in app state")

        config_parser = request.app.state.config_parser
        config = config_parser.load_personality_config(user_id)
        return {
            "status": "success",
            "data": config.to_dict(),
            "user_id": user_id,
            "scope": "instance",
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


@router.put("/profile")
async def update_personality_profile(
    request: Request,
    current_user: JWTClaims = Depends(require_admin),
):
    """Update the personality configuration for the authenticated session.

    1734: ADMIN-ONLY until the store is per-user.
    PiperConfigParser.save_personality_config ignores user_id entirely and
    rewrites the GLOBAL config/PIPER.user.md — so on the hosted beta, any
    authenticated user's save would clobber every user's overlay (including
    PM's ADR-075 D4 personal overlay, if present). require_admin is the #1508/
    #1598 idiom: global-blast-radius write → admin authority, live DB check,
    fail-closed, no payload in the refusal. The GET above and /enhance below
    require authentication but no admin authority — they only read. When the
    store is scoped per-user (users.preferences JSONB is the natural home, per
    the 1734 filing), this gate can come off in the same change that makes
    user_id real.

    1751: the `{user_id}` path segment is REMOVED. It was the last place a
    caller could aim this write at someone else — and an admin aiming it at
    another principal got a 200 plus a global rewrite, which is exactly the
    cross-user-write shape 1734's gate was holding back rather than closing.
    """
    user_id = str(current_user.user_id)
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
                "scope": "instance",
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
async def enhance_response(
    request: Request,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Enhance a response with personality.

    #1751: the request body's `user_id` key is no longer read. It used to
    select whose personality config the enhancement ran against
    (`data.get("user_id", "default")`), which is a client-supplied principal on
    an endpoint that takes free-form content — the same defect as the profile
    routes, just carried in the body instead of the path. The principal is the
    session's; the derived id is echoed in the response so the property is
    observable from outside (a silently-ignored key is indistinguishable from
    an honored one at the wire).
    """
    user_id = str(current_user.user_id)
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
        confidence = data.get("confidence", 0.5)
        # NB: data.get("user_id") is deliberately NOT read — see the docstring.

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
                "user_id": user_id,
                "scope": "instance",
            },
        }
    except (ValueError, TypeError) as e:
        # Validation errors - return 422
        return validation_error(f"Invalid enhancement request: {str(e)}", {"error": str(e)})
    except Exception as e:
        # Processing errors - return 500
        logger.error(f"Error enhancing response: {e}", exc_info=True)
        return internal_error("Failed to enhance response")
