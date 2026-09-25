"""
Personality Configuration API Routes

Provides endpoints for managing personality preferences and response enhancement.
- GET  /api/v1/personality/profile - Retrieve personality configuration
- PUT  /api/v1/personality/profile - Update personality configuration (own row; #1791)
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
down; `Depends(get_current_user)` supplies it (see #1791 below for why the PUT
no longer needs `require_admin` too).

#1791 (2026-09-24): PER-USER DATA SEPARATION NOW EXISTS. `PiperConfigParser`
reads/writes each user's own row in `users.preferences["upm"]` (#1574's store)
and falls back to the instance-wide file (`config/PIPER.user.md`, ADR-075 D4)
ONLY for a user who has never saved a profile — `"scope"` in the responses now
reflects which one actually served the request (`"user"` or `"instance"`)
rather than a hardcoded literal. Because a save now lands in the CALLER'S OWN
row and can no longer clobber every user's overlay, #1734's `require_admin`
gate — which existed only to hold back that global blast radius — comes off
the PUT in this same change; it is `Depends(get_current_user)` like the other
two routes. Existing answers in the pre-#1791 instance file were NOT migrated
into any user's row (unknowable ownership — see `PiperConfigParser`'s
docstring); every user's first save under the new store starts from that
shared default.
Pins: tests/unit/web/api/routes/test_personality_principal_from_session_1751.py
      tests/unit/web/api/routes/test_personality_put_admin_gated_1734.py
"""

import structlog
from fastapi import APIRouter, Depends, Request

from services.auth.auth_middleware import JWTClaims, get_current_user
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
    from the session. The read stays open to any authenticated user.

    #1791: `scope` in the response is now honest — `"user"` when this reads the
    caller's own saved row, `"instance"` when they have never saved one and the
    shared default file served the read.
    """
    user_id = str(current_user.user_id)
    try:
        # Get config_parser from app state (initialized in WebComponentsInitializationPhase)
        if not hasattr(request.app.state, "config_parser"):
            return internal_error("Configuration parser not initialized in app state")

        config_parser = request.app.state.config_parser
        config, scope = await config_parser.load_personality_config_scoped(user_id)
        return {
            "status": "success",
            "data": config.to_dict(),
            "user_id": user_id,
            "scope": scope,
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
    current_user: JWTClaims = Depends(get_current_user),
):
    """Update the personality configuration for the authenticated session.

    1734 (historical): ADMIN-ONLY until the store was per-user.
    PiperConfigParser.save_personality_config used to ignore user_id entirely
    and rewrite the GLOBAL config/PIPER.user.md — so on the hosted beta, any
    authenticated user's save would clobber every user's overlay (including
    PM's ADR-075 D4 personal overlay, if present). require_admin was the
    #1508/#1598 idiom for exactly that shape: global-blast-radius write →
    admin authority, live DB check, fail-closed, no payload in the refusal.

    #1791: the store is now per-user (`users.preferences["upm"]`, #1574) — a
    save lands in the CALLER'S OWN row, never the shared file, so it no longer
    has a global blast radius. `require_admin` is REMOVED in this same change
    (1734's own stated exit condition); the PUT now takes `get_current_user`
    like the GET and /enhance below — authenticated, not admin-gated.

    1751: the `{user_id}` path segment is REMOVED. It was the last place a
    caller could aim this write at someone else.
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

        scope = config_parser.write_scope_for(user_id)
        success = await config_parser.save_personality_config(config, user_id)

        if success:
            return {
                "status": "success",
                "data": config.to_dict(),
                "user_id": user_id,
                "scope": scope,
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

        # Load personality config (the caller's own saved profile, or the
        # instance-wide default if they have never saved one — #1791)
        config, scope = await config_parser.load_personality_config_scoped(user_id)

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
                "scope": scope,
            },
        }
    except (ValueError, TypeError) as e:
        # Validation errors - return 422
        return validation_error(f"Invalid enhancement request: {str(e)}", {"error": str(e)})
    except Exception as e:
        # Processing errors - return 500
        logger.error(f"Error enhancing response: {e}", exc_info=True)
        return internal_error("Failed to enhance response")
