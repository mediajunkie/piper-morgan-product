"""
Intent Processing & Workflow Management API Routes

Provides endpoints for intent processing (Phase 2B: Thin HTTP adapter)
and workflow status tracking (Bug #166 fix).

Routes:
- POST /api/v1/intent - Process user intent message
- GET /api/v1/workflows/{workflow_id} - Get workflow status

Pattern-007: Implements graceful degradation (async error handling)
- Returns 200 OK with structured response even when services unavailable
- Provides user-friendly degradation messages
- Maintains consistent IntentResponse structure

Design decision (Issue #875): This endpoint returns 200 OK for ALL responses from
IntentService, including business-logic errors. Errors are conversational responses
(displayed in the chat window), not HTTP error codes. Pattern-007 degradation handles
infrastructure failures the same way. Only use validation_error()/HTTP 4xx for
actual malformed HTTP requests (missing body, bad JSON, etc).

Issue #878: workflow_id is stripped from responses unless the handler sets
async_work_started=True on IntentProcessingResult. Currently only _handle_generic_query
uses the orchestration engine for real async work. All other handlers are synchronous —
passing workflow_id through caused the frontend to poll for 60s then show timeout.
Future async handlers: set async_work_started=True to preserve workflow_id.

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 419-658)
Now: Extracted to separate router module
"""

from datetime import datetime
from typing import Optional

import structlog
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth.jwt_service import JWTClaims, JWTService
from services.domain.models import RequestContext
from services.llm.request_key import (
    AnonymousLLMKeyRequiredError,
    request_api_key,
    resolve_request_api_key,
)
from web.utils.error_responses import internal_error, validation_error

logger = structlog.get_logger()

# Router configuration
router = APIRouter(prefix="/api/v1", tags=["intent", "workflows"])

# Security - optional bearer token for authentication
security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[JWTClaims]:
    """
    Issue #490: Get current user from JWT if present, otherwise return None.

    This allows the /intent endpoint to work both authenticated and unauthenticated,
    but when authenticated, we get the user_id for features like portfolio onboarding.

    Issue #455: Checks both Authorization header AND auth_token cookie
    to support web UI authentication with credentials: 'include'.

    Issue #840: Sets request.state.auth_expired = True when a token was present
    but expired, so the route can signal the frontend to re-authenticate.
    """
    from services.auth.jwt_service import TokenExpired

    # Extract token from Authorization header or cookie (Issue #455)
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Try auth_token cookie (for web UI)
        token = request.cookies.get("auth_token")

    if not token:
        return None

    try:
        jwt_service = getattr(request.app.state, "jwt_service", None)
        if jwt_service is None:
            jwt_service = JWTService()

        # Issue #490: Use validate_token (async) not verify_token (doesn't exist)
        claims = await jwt_service.validate_token(token)
        return claims
    except TokenExpired:
        # Issue #840: Token was present but expired — flag for route to signal frontend
        request.state.auth_expired = True
        logger.warning(
            "auth_token_expired", detail="Token present but expired, flagging for frontend redirect"
        )
        return None
    except Exception as e:
        logger.debug(f"JWT verification failed (continuing as unauthenticated): {e}")
        return None


# Helper functions for graceful degradation (Pattern-007)
def _extract_degradation_message(error: Exception) -> str:
    """Extract a user-friendly message from an exception.

    Converts technical exceptions into user-understandable messages
    for graceful degradation (Pattern-007).

    Args:
        error: The exception to extract message from

    Returns:
        User-friendly degradation message string
    """
    error_str = str(error).lower()

    # Database/Connection errors
    if "database" in error_str or "connection" in error_str or "timeout" in error_str:
        return "Database service is temporarily unavailable. Please ensure Docker containers are running and try again."

    # LLM/API errors
    if "llm" in error_str or "api" in error_str or "openai" in error_str:
        return "AI service is temporarily unavailable. Please try again in a few moments."

    # File system errors
    if "file" in error_str or "path" in error_str:
        return "File system error. Please check your configuration and try again."

    # Config errors
    if "config" in error_str:
        return "Configuration error. Please verify your setup and try again."

    # Default message for unknown errors
    return "An unexpected error occurred. Please try again later."


def _create_degradation_response(original_message: str, degradation_msg: str) -> dict:
    """Create a structured IntentResponse with degradation message.

    Returns a properly formatted response even when services fail,
    following Pattern-007 (graceful degradation).

    Args:
        original_message: Original user message that failed to process (for context)
        degradation_msg: User-friendly error message

    Returns:
        Structured IntentResponse dict with degradation values

    Issue #560: Fixed echo bug - response.message should be the degradation
    message (what Piper says), not the original user message.
    """
    return {
        "message": degradation_msg,
        "intent": {
            "type": "unknown",
            "confidence": 0,
            "action": "clarify",
        },
        "workflow_id": None,
        "requires_clarification": True,
        "clarification_type": "service_unavailable",
        "suggestions": [
            f"Unable to process your request right now ({degradation_msg})",
            "Please try again in a moment",
        ],
        "preferences": {},
        "error": degradation_msg,
        "error_type": "service_unavailable",
    }


def _create_anonymous_key_required_response(original_message: str) -> dict:
    """#1320: the honest response when an anonymous (no login, no X-User-Api-Key)
    request is refused. NOT `_create_degradation_response` — that message ("service
    unavailable... try again") is misleading here: retrying changes nothing, the
    remediation is signing in or bringing a key. Same IntentResponse shape, honest
    case-specific copy (mirrors the #1231/#1333 honest-degrade discipline).
    """
    msg = (
        "I can't process this without you being signed in or supplying your own "
        "Anthropic API key — sign in, or connect your own key."
    )
    return {
        "message": msg,
        "intent": {"type": "unknown", "confidence": 0, "action": "clarify"},
        "workflow_id": None,
        "requires_clarification": True,
        "clarification_type": "auth_or_key_required",
        "suggestions": ["Sign in to continue", "Or connect your own Anthropic API key"],
        "preferences": {},
        "error": msg,
        "error_type": "anonymous_key_required",
    }


@router.get("/workflows/{workflow_id}")
async def get_workflow_status(workflow_id: str, request: Request):
    """Get workflow status to prevent UI polling hang (Bug #166 fix)"""
    try:
        # Validate workflow_id
        if not workflow_id or not workflow_id.strip():
            return validation_error(
                "Workflow ID required",
                {"field": "workflow_id", "issue": "Cannot be empty"},
            )

        # Get OrchestrationEngine from app state
        orchestration_engine = getattr(request.app.state, "orchestration_engine", None)

        if orchestration_engine is None:
            # Service unavailable - return 500
            logger.error("OrchestrationEngine not available for workflow status check")
            return internal_error("OrchestrationEngine not available")

        # For GREAT-1B, return a simple status response
        # This prevents the infinite polling that causes UI hangs
        # Bug #xpv: Changed message to not claim completion when status unknown
        return {
            "workflow_id": workflow_id,
            "status": "processing",  # Neutral status (not "completed" - may need clarification)
            "message": "",  # No message - avoids misleading "completed" claim
            "tasks": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

    except ValueError as e:
        # Known validation errors
        return validation_error(str(e))
    except Exception as e:
        # Unexpected errors - log and return 500
        logger.error(f"Error getting workflow {workflow_id}: {e}", exc_info=True)
        return internal_error()


@router.post("/intent")
async def process_intent(
    request: Request,
    current_user: Optional[JWTClaims] = Depends(get_current_user_optional),
):
    """
    Phase 2B: Thin HTTP adapter for intent processing

    Delegates all business logic to IntentService.
    Route only handles HTTP concerns (request parsing, response formatting, status codes).

    Issue #490: Now accepts optional authentication to pass user_id for features
    like portfolio onboarding that require user context.

    Implements Pattern-007 (Async Error Handling) graceful degradation:
    - Returns 200 OK with structured response even when services unavailable
    - Provides user-friendly degradation messages
    - Maintains consistent IntentResponse structure

    Business logic: services/intent/intent_service.py
    """
    try:
        # Parse HTTP request
        request_data = await request.json()
        message = request_data.get("message", "")
        session_id = request_data.get("session_id", "default_session")

        # Issue #490: Extract user_id from authenticated user if available
        user_id = current_user.sub if current_user else None

        # ADR-051 Phase 2: Create RequestContext at boundary (when authenticated)
        # session_id semantically IS conversation_id (ADR-051 resolution)
        # ctx is None for unauthenticated requests - services handle gracefully
        ctx: Optional[RequestContext] = None
        if current_user:
            try:
                ctx = RequestContext.from_jwt_and_request(
                    claims=current_user,
                    conversation_id=session_id,
                )
                logger.debug(
                    "request_context_created",
                    context=str(ctx),
                )
            except ValueError as e:
                # Malformed JWT claims - log but continue without context
                logger.warning(
                    "request_context_creation_failed",
                    error=str(e),
                    has_sub=bool(current_user.sub),
                )

        logger.info(
            "intent_route_auth_trace",
            has_current_user=current_user is not None,
            user_id=user_id,
            session_id=session_id,
            has_request_context=ctx is not None,
            message_preview=message[:50] if message else None,
            has_auth_cookie="auth_token" in request.cookies,
        )

        # Get IntentService from app state (dependency injection)
        intent_service = getattr(request.app.state, "intent_service", None)

        if intent_service is None:
            # Pattern-007: Graceful degradation - return 200 with user-friendly message.
            # #1116 Finding 1 fix: previous message claimed Docker was the cause, which
            # was misleading — the actual cause is app.state.intent_service is None
            # (silent init failure during server startup, see Finding 2 + the Phase 1.5
            # fix in web/startup.py). The honest remediation is server restart + log
            # inspection, not Docker.
            logger.error(
                "intent_service_unavailable_returning_degradation_response - "
                "app.state.intent_service is None; check startup logs for IntentService init errors"
            )
            return _create_degradation_response(
                message,
                "Intent service is currently unavailable. The server may need a restart — "
                "check startup logs for IntentService initialization errors.",
            )

        # Issue #731: Auto-create conversation if none exists for this session
        # This ensures conversations are persisted even when user types directly
        # in the chat input without clicking "+ New Chat" button
        # Issue #787: Track if conversation was created to signal frontend sidebar refresh
        conversation_created = False
        if user_id and session_id and session_id != "default_session":
            try:
                from services.database.models import ConversationDB
                from services.database.session_factory import AsyncSessionFactory

                async with AsyncSessionFactory.session_scope_fresh() as db_session:
                    # Check if conversation exists
                    existing = await db_session.get(ConversationDB, session_id)
                    if not existing:
                        # Create new conversation with the session_id as its ID
                        # This ensures the frontend's localStorage session_id matches the DB
                        conversation = ConversationDB(
                            id=session_id,
                            user_id=user_id,
                            session_id=session_id,
                            title="New conversation",
                            context={},
                            is_active=True,
                        )
                        db_session.add(conversation)
                        await db_session.commit()
                        conversation_created = True
                        logger.info(
                            "Auto-created conversation for session",
                            session_id=session_id,
                            user_id=user_id,
                        )
            except Exception as e:
                # Don't fail the intent if conversation creation fails
                logger.warning(f"Failed to auto-create conversation: {e}")

        # Issue #490: Pass user_id to service for user-specific features
        # ADR-051 Phase 3: Pass RequestContext alongside old params (dual pattern)
        # ctx is None for unauthenticated requests - service handles gracefully
        # #1162/#1185 BYOC: resolve this request's Anthropic key — the X-User-Api-Key
        # header (Claude Desktop BYOC) wins; else the authenticated user's STORED key
        # (hosted web, #1185), resolved by user_id from user_api_keys; else the server
        # key. Bound to the request-scoped ContextVar (reset in finally; never logged).
        async def _fetch_stored_anthropic_key(uid: str):
            from services.database.session_factory import AsyncSessionFactory
            from services.security.user_api_key_service import UserAPIKeyService

            async with AsyncSessionFactory.session_scope_fresh() as _s:
                return await UserAPIKeyService().retrieve_user_key(_s, uid, "anthropic")

        try:
            resolved_key = await resolve_request_api_key(
                request.headers.get("X-User-Api-Key"), user_id, _fetch_stored_anthropic_key
            )
        except AnonymousLLMKeyRequiredError:
            # #1320: refuse BEFORE touching intent_service/the LLM at all — never
            # silently bill the server's own key to a fully anonymous caller.
            logger.warning("intent_anonymous_key_required_1320", session_id=session_id)
            return _create_anonymous_key_required_response(message)
        with request_api_key(resolved_key):
            result = await intent_service.process_intent(
                message=message, session_id=session_id, user_id=user_id, ctx=ctx
            )

        # Format HTTP response from service result
        response = {
            "message": result.message,
            "intent": result.intent_data,
            "workflow_id": result.workflow_id,
            "requires_clarification": result.requires_clarification,
            "clarification_type": result.clarification_type,
            "suggestions": result.suggestions,  # Phase 3: Pattern suggestions
            "preferences": result.preferences,  # Issue #248: Preference detection results
            "session_id": session_id,  # Issue #787: Return session_id for frontend sync
            "conversation_created": conversation_created,  # Issue #787: Signal sidebar refresh
            # Issue #840: Signal frontend when auth has expired so it can redirect to login
            "auth_expired": getattr(request.state, "auth_expired", False),
        }

        # Issue #878/#883: Strip workflow_id unless the handler started async work.
        # Issue #883: Workflows are no longer pre-created. workflow_id is None by
        # default. This guard remains for future handlers that create workflows
        # on demand and set async_work_started=True.
        if not result.async_work_started:
            response["workflow_id"] = None

        # Issue #875: Business-logic errors from IntentService are conversational
        # responses, not HTTP errors. Return 200 OK with error data in body so
        # frontend displays the message in the chat window (not as a red error box).
        # This restores the pre-refactor (#385) behavior accidentally changed Nov 2025.
        if result.error:
            response["error"] = result.error
            if result.error_type:
                response["error_type"] = result.error_type

        return response

    except Exception as e:
        # Pattern-007: Graceful degradation - return 200 with user-friendly message
        logger.error(f"Intent route error: {str(e)}", exc_info=True)

        # Extract user-friendly degradation message from exception
        degradation_msg = _extract_degradation_message(e)

        # Return structured IntentResponse instead of 500 error
        return _create_degradation_response(
            request_data.get("message", "") if "request_data" in locals() else "",
            degradation_msg,
        )
