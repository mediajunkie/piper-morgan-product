"""
Piper Morgan Web Interface
Simple FastAPI app for interacting with the main Piper Morgan Platform API
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import structlog
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Add project root to path for imports (same as CLI)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Standup API moved to backend - only config loader needed for legacy compatibility
from services.configuration.piper_config_loader import piper_config_loader

# Configuration service import - eliminates hardcoded values
from services.configuration.port_configuration_service import get_port_configuration

# Startup phase management (Phase 2 of Issue #385 - INFR-MAINT-REFACTOR)
from web.startup import lifespan

# Import error response utilities (Pattern 034: Error Handling Standards)
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Personality components are now initialized during startup (Phase 4 - WebComponentsInitializationPhase)


# Server Configuration - now accessed via app.state during startup (Phase 4 - WebComponentsInitializationPhase)

# Initialize logger
logger = structlog.get_logger()


# Create FastAPI app with lifespan
app = FastAPI(
    title="Piper Morgan UI",
    description="Web Interface for the Piper Morgan Platform",
    lifespan=lifespan,
)

# ADR-076: usage-cap enforcement (rate limit + concurrency cap), Redis-backed.
# Starlette's add_middleware() inserts at position 0 of the internal stack, so
# LATER add_middleware() calls become MORE OUTER (execute first on a request).
# This middleware reads request.state.user_id, which AuthMiddleware sets — so
# it must be registered BEFORE AuthMiddleware's own add_middleware() call
# below, not after, or it would run before Auth and never see the resolved
# principal (verified empirically, not assumed — see usage_cap_middleware.py).
try:
    from web.middleware.usage_cap_middleware import UsageCapMiddleware

    app.add_middleware(UsageCapMiddleware)
    logger.info("✅ UsageCapMiddleware registered (ADR-076 - usage-cap enforcement)")
except Exception as e:
    logger.error(f"⚠️ Failed to register UsageCapMiddleware: {e}")

# Issue #393: Register AuthMiddleware to enable cookie-based authentication
# Must be registered before other middleware so it sets request.state.user_id early
try:
    from services.auth.auth_middleware import AuthMiddleware
    from services.auth.container import AuthContainer

    # Issue #723: Use AuthContainer to get JWTService with blacklist support
    # Plain JWTService() has no blacklist, so revoked tokens aren't rejected
    jwt_service = AuthContainer.get_jwt_service()

    # #936: UserService removed (dead code; never populated in production).
    # AuthMiddleware now takes only jwt_service; user identity is set on
    # request.state.user_id from JWT claims directly.
    app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
    logger.info("✅ AuthMiddleware registered (Issue #393 - cookie-based authentication)")
except Exception as e:
    logger.error(f"⚠️ Failed to register AuthMiddleware: {e}")

# Issue #283: Enhanced error handling with user-friendly messages
# Mount BEFORE other middleware so it catches exceptions from all handlers
try:
    from web.middleware.enhanced_error_middleware import EnhancedErrorMiddleware

    app.add_middleware(EnhancedErrorMiddleware)
    logger.info("✅ EnhancedErrorMiddleware registered (Issue #283 - CORE-ALPHA-ERROR-MESSAGES)")
except Exception as e:
    logger.error(f"⚠️ Failed to mount EnhancedErrorMiddleware: {e}")

# Issue #283: Custom HTTPException handler for friendly error messages
# This catches FastAPI's built-in HTTPException errors (401, 404, etc) which bypass middleware
try:
    from fastapi import HTTPException, Request
    from fastapi.responses import JSONResponse

    from services.ui_messages.user_friendly_errors import UserFriendlyErrorService

    error_service = UserFriendlyErrorService()

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """
        Convert FastAPI HTTPException to user-friendly messages.

        This handler intercepts FastAPI's built-in error responses (401, 404, etc)
        that bypass normal middleware exception handling, and converts them using
        UserFriendlyErrorService for consistent user-friendly messaging.
        """
        # Get friendly message based on status code and exception detail
        friendly_message = None

        if exc.status_code == 401:
            # Authentication errors
            friendly_message = "Let's try logging in again. Your session may have expired."
        elif exc.status_code == 403:
            # Permission errors
            friendly_message = "You don't have permission to access that. Please contact your administrator if you think this is incorrect."
        elif exc.status_code == 404:
            # Not found errors
            friendly_message = "I couldn't find that. It may have been moved or deleted."
        elif exc.status_code == 422:
            # Validation errors
            friendly_message = f"I couldn't process that request: {str(exc.detail)}"
        elif exc.status_code >= 500:
            # Server errors
            friendly_message = (
                "Something went wrong on my end. I've logged the details for debugging."
            )
        else:
            # Fallback to original detail
            friendly_message = str(exc.detail)

        # CRITICAL: Log technical details server-side for debugging
        logger.error(
            "http_exception",
            status_code=exc.status_code,
            detail=str(exc.detail),
            path=request.url.path,
            method=request.method,
        )

        # Return friendly message to user. Build the response first so we
        # can apply cookie-clearing (Issue #1078) if the raiser asked for it.
        response = JSONResponse(status_code=exc.status_code, content={"message": friendly_message})

        # #1078: HTTPExceptionWithCookieClear signals that auth cookies must
        # be cleared as part of this 4xx — apply to the rebuilt response so
        # the Set-Cookie headers actually reach the client. The rebuild in
        # this handler drops Set-Cookie headers from the dependency-injected
        # Response, so the raiser communicates intent via the exception.
        try:
            from web.api.exceptions import HTTPExceptionWithCookieClear

            if isinstance(exc, HTTPExceptionWithCookieClear) and exc.clear_cookies:
                for cookie_name in exc.clear_cookies:
                    response.delete_cookie(cookie_name)
        except ImportError:
            # Custom exception module not available — fall through with the
            # default JSONResponse (preserves pre-#1078 behavior).
            pass

        return response

    logger.info(
        "✅ HTTPException handler registered (Issue #283 - catches 401, 404, 403, 422 errors)"
    )
except Exception as e:
    logger.error(f"⚠️ Failed to register HTTPException handler: {e}")

# Issue #283: APIError exception handler for dependency-level errors
# Dependencies execute BEFORE middleware, so exceptions raised in Depends() need
# this handler to be caught and converted to friendly messages
try:
    from services.api.errors import APIError

    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """
        Handle APIError exceptions with user-friendly messages.

        This catches APIError raised anywhere in the application,
        including from FastAPI dependencies like get_current_user.

        Since dependencies execute before middleware, this exception
        handler is the appropriate layer to convert APIError to
        friendly messages for users.
        """
        # Get friendly message based on error code and status code
        friendly_message = None

        if exc.status_code == 401:
            # Authentication errors
            friendly_message = "Let's try logging in again. Your session may have expired."
        elif exc.status_code == 403:
            # Permission errors
            friendly_message = (
                "You don't have permission to access that. Please contact your administrator."
            )
        elif exc.status_code == 404:
            # Not found errors
            friendly_message = "I couldn't find that. It may have been moved or deleted."
        elif exc.status_code == 422:
            # Validation errors
            friendly_message = (
                "I couldn't process that request. Please check your input and try again."
            )
        elif exc.status_code >= 500:
            # Server errors
            friendly_message = (
                "Something went wrong on my end. I've logged the details for debugging."
            )
        else:
            # Fallback
            friendly_message = "An error occurred. Please try again."

        # CRITICAL: Log technical details for debugging
        logger.error(
            "api_error",
            error_code=exc.error_code,
            status_code=exc.status_code,
            details=exc.details,
            path=request.url.path,
            method=request.method,
        )

        # Return friendly message to user
        return JSONResponse(status_code=exc.status_code, content={"message": friendly_message})

    logger.info(
        "✅ APIError exception handler registered (Issue #283 - catches dependency-level errors)"
    )
except Exception as e:
    logger.error(f"⚠️ Failed to register APIError handler: {e}")

# GREAT-4B: Intent Enforcement Middleware
from web.middleware.intent_enforcement import IntentEnforcementMiddleware

app.add_middleware(IntentEnforcementMiddleware)
logger.info("✅ IntentEnforcementMiddleware registered (GREAT-4B)")

# Phase 1: Mount remaining API routers using factory pattern (Issue #385 - INFR-MAINT-REFACTOR)
# Previously: ~90 lines of duplicate try/catch boilerplate
# Now: Consolidated calls to RouterInitializer factory for consistency
from web.router_initializer import RouterInitializer

RouterInitializer.mount_router(app, "web.api.routes.auth", "router", "Auth API")
RouterInitializer.mount_router(
    app, "web.api.routes.setup", "router", "Setup Wizard API"
)  # Issue #390
RouterInitializer.mount_router(app, "web.api.routes.files", "router", "Files API")
RouterInitializer.mount_router(app, "web.api.routes.artifacts", "router", "Artifacts API")
RouterInitializer.mount_router(app, "web.api.routes.documents", "router", "Documents API")
RouterInitializer.mount_router(
    app, "services.api.todo_management", "todo_management_router", "Todos API"
)
RouterInitializer.mount_router(app, "web.api.routes.lists", "router", "Lists API")
RouterInitializer.mount_router(
    app, "web.api.routes.insights", "router", "Insights API"
)  # Issue #1031 MUX-INSIGHT-PASSIVE
RouterInitializer.mount_router(
    app, "web.api.routes.places", "router", "Places API"
)  # Issue #684/#1192(d)/#1195 — "What I'm seeing" panel backend
RouterInitializer.mount_router(app, "web.api.routes.todos", "router", "Todos SEC-RBAC API")
RouterInitializer.mount_router(app, "web.api.routes.projects", "router", "Projects API")
RouterInitializer.mount_router(
    app,
    "web.api.routes.repositories",
    "router",
    "Repositories API",  # Issue #866
)
RouterInitializer.mount_router(app, "web.api.routes.feedback", "router", "Feedback API")
RouterInitializer.mount_router(
    app, "web.api.routes.knowledge_graph", "router", "Knowledge Graph API"
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.integrations",
    "router",
    "Integrations API",  # Issue #530
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.settings_integrations",
    "router",
    "Settings Integrations API",  # Issue #529
)

# Phase 3: Mount extracted route modules (Issue #385 - INFR-MAINT-REFACTOR)
# Previously: Inline routes scattered throughout web/app.py
# Now: Organized into logical router modules for maintainability
RouterInitializer.mount_router(app, "web.api.routes.personality", "router", "Personality Routes")
RouterInitializer.mount_router(app, "web.api.routes.intent", "router", "Intent Routes")
RouterInitializer.mount_router(app, "web.api.routes.admin", "router", "Admin Routes")
RouterInitializer.mount_router(app, "web.api.routes.ui", "router", "UI Routes")
RouterInitializer.mount_router(app, "web.api.routes.debug", "router", "Debug Routes")
RouterInitializer.mount_router(
    app,
    "web.api.routes.conversations",
    "router",
    "Conversations API",  # Issue #563
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.user_history",
    "router",
    "User History API",  # Issue #1021
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.radar",
    "router",
    "Radar API",  # Issue #1236 / #1090 (Layer-2 entities surface)
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.work_items",
    "router",
    "Work Items API",  # Issue #710
)
RouterInitializer.mount_router(
    app,
    "web.api.routes.preferences",
    "router",
    "Preferences API",  # Issue #248 rewired
)

# Issue #1148: Dev-only trust-stage GUI — lets UAT reach trust-gated surfaces.
# Every route 404s in production (PIPER_ENVIRONMENT gate); see web/routers/dev_trust.py.
RouterInitializer.mount_router(
    app,
    "web.routers.dev_trust",
    "router",
    "Dev Trust-Stage UI (Issue #1148, dev-only)",
)

# Issue #1143: Dev-only composting trigger — force a cycle for #1033/#1035 UAT.
# Every route 404s in production (PIPER_ENVIRONMENT gate); see web/routers/dev_composting.py.
RouterInitializer.mount_router(
    app,
    "web.routers.dev_composting",
    "router",
    "Dev Composting Trigger (Issue #1143, dev-only)",
)

# Issue #1018 + #1075: User Transparency API endpoints (PM-087 surface)
RouterInitializer.mount_router(
    app,
    "services.api.transparency",
    "transparency_router",
    "Transparency API (Issue #1018 audit-log surface)",
)

# Web components (Jinja2 templates, config_parser, personality_enhancer) are now initialized
# in WebComponentsInitializationPhase during startup and stored in app.state (Phase 4)


# Mount static files (MUST be last - after all routes)
# FastAPI/Starlette routing: routes are checked first, mounts last
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "assets")),
    name="assets",
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)


if __name__ == "__main__":
    import uvicorn

    # Get port configuration locally for __main__ (Phase 4)
    local_port_config = get_port_configuration()

    print(f"🚀 Starting Piper Morgan Web Interface on {local_port_config.get_web_url()}")
    print(f"📊 Standup API: {local_port_config.get_web_url()}/api/standup")
    print(f"🌅 Standup UI: {local_port_config.get_web_url()}/standup")
    print(f"📖 API Docs: {local_port_config.get_web_url()}/docs")
    print(f"🔗 Backend API: {local_port_config.get_backend_url()}")
    print(
        f"\n🔧 Server Command: PYTHONPATH=. python -m uvicorn web.app:app --host {local_port_config.web_host} --port {local_port_config.web_port}"
    )
    uvicorn.run(app, host=local_port_config.web_host, port=local_port_config.web_port)
