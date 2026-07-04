"""
Authentication Middleware - FastAPI Integration

FastAPI middleware for JWT-based authentication with OAuth 2.0 integration.
Provides secure authentication for API endpoints with flexible authorization.

Features:
- JWT token validation middleware
- OAuth 2.0 bearer token support
- Scope-based authorization
- MCP protocol compatibility
- Audit logging integration
"""

from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

import structlog
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from services.domain.models import RequestContext

from .jwt_service import JWTClaims, JWTService

logger = structlog.get_logger(__name__)


# ─── Default exempt-path categories for AuthMiddleware ──────────────────────
# Refactored from a flat 34-entry list to named categories per #1014 (Apr 29).
# Each category corresponds to one architectural reason for skipping auth.
# When adding a new exempt path, slot it into the right category — or create
# a new category if none fit. Concatenated into `DEFAULT_EXCLUDE_PATHS` below.

# OpenAPI / API documentation surfaces. No user data; safe public access.
EXEMPT_OPENAPI_PATHS: List[str] = [
    "/docs",
    "/redoc",
    "/openapi.json",
]

# Health-check endpoints. Used by load balancers + uptime monitoring; must be
# auth-free or we lose observability of the auth layer itself.
EXEMPT_HEALTH_PATHS: List[str] = [
    "/health",
    "/api/v1/health",  # Issue #906: versioned health path
]

# Auth endpoints themselves — login/logout/register can't require auth or you
# can't bootstrap a session. Setup-wizard endpoints similarly need to run
# pre-account-creation. /login and /setup are the template UI routes (not
# the API endpoints, which live under /api/v1/auth and /api/v1/setup
# respectively per #1013 Apr 28).
EXEMPT_AUTH_AND_SETUP_PATHS: List[str] = [
    "/login",  # Issue #393: login UI template
    "/setup",  # Issue #390: setup-wizard UI template
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/register",
    "/api/v1/auth/refresh",  # Issue #857: refresh endpoint hit with expired access token
    "/api/v1/setup",  # All /api/v1/setup/* sub-routes via startswith match
]

# Routes where auth is optional + handled inline. The route itself accepts
# both authenticated and unauthenticated requests; user_id is populated when
# present. Issue #490 established this pattern.
EXEMPT_OPTIONAL_AUTH_PATHS: List[str] = [
    "/api/v1/intent",
    "/api/v1/workflows",  # workflow status checks paired with intent
    "/api/v1/standup",
]

# OAuth callback URLs. Third-party OAuth providers POST here; the request
# carries an OAuth code, not a session token. Auth is established via the
# code exchange, not the middleware.
EXEMPT_OAUTH_CALLBACK_PATHS: List[str] = [
    "/slack/oauth/callback",
    "/github/oauth/callback",
    # Issue #528: Settings → Integrations OAuth flow
    "/api/v1/settings/integrations/slack/connect",
    "/api/v1/settings/integrations/slack/callback",
    "/api/v1/settings/integrations/calendar/connect",
    "/api/v1/settings/integrations/calendar/callback",
]

# Static assets. CSS/JS/images don't have user-bound responses.
EXEMPT_STATIC_ASSET_PATHS: List[str] = [
    "/static/",
    "/assets/",
]

# Localhost-only scaffolds. Not exposed externally; auth would be ceremony.
EXEMPT_LOCALHOST_SCAFFOLD_PATHS: List[str] = [
    "/api/v1/admin/trust",  # Issue #1148: dev trust-stage UI (router 404s in production)
]

# Read-only integration-status checks the setup wizard fires PRE-account-creation (#1320).
# The onboarding flow runs before login, so these GET "are app credentials configured?"
# checks 401'd and popped the browser's basic-auth dialog. They return ONLY booleans
# (configured / has_client_id / has_client_secret — never the secret values; see
# SlackAppCredentialsStatusResponse), so exempting them is safe. GET-only → no
# AUTH_EXEMPT_JUSTIFIED entry required (#1308: read-only exempt routes need none). The
# WRITE siblings (POST .../app-credentials) are intentionally NOT here — they still require auth.
EXEMPT_SETUP_READONLY_STATUS_PATHS: List[str] = [
    "/api/v1/settings/integrations/slack/app-credentials/status",
    "/api/v1/settings/integrations/calendar/app-credentials/status",
]

# The flat list AuthMiddleware compares against, assembled from category
# constants above. This keeps the constructor signature unchanged.
DEFAULT_EXCLUDE_PATHS: List[str] = [
    *EXEMPT_OPENAPI_PATHS,
    *EXEMPT_HEALTH_PATHS,
    *EXEMPT_AUTH_AND_SETUP_PATHS,
    *EXEMPT_OPTIONAL_AUTH_PATHS,
    *EXEMPT_OAUTH_CALLBACK_PATHS,
    *EXEMPT_STATIC_ASSET_PATHS,
    *EXEMPT_LOCALHOST_SCAFFOLD_PATHS,
    *EXEMPT_SETUP_READONLY_STATUS_PATHS,
]


# ─── #1308: auth-exempt WRITABLE routes must be JUSTIFIED (the exempt list is a
#     security boundary) ────────────────────────────────────────────────────────
# Once the perimeter (Caddy) gate is removed (#1162), this exempt list IS the entire
# attack surface. Every exempt route with a WRITE method (POST/PUT/PATCH/DELETE) must
# appear here with a reason, or the `TestAuthExemptListIsASecurityBoundary` lint
# (tests/test_exempt_list_boundary_1308.py) fails the build — making the #1307 class
# (exempt + writable + prod-reachable) impossible by omission. A key is an exact path
# OR a trailing-"/" prefix. Read-only exempt routes need no entry. Env-gated dev routes
# are listed here with reason "env-gated" (they 404 in prod via require_dev_environment).
AUTH_EXEMPT_JUSTIFIED: Dict[str, str] = {
    # Auth bootstrap — can't require auth to authenticate.
    "/api/v1/auth/login": "auth bootstrap (login)",
    "/api/v1/auth/logout": "auth bootstrap (logout)",
    "/api/v1/auth/refresh": "auth bootstrap (token refresh, #857)",
    # Setup wizard — runs pre-account-creation.
    "/api/v1/setup/": "setup wizard, pre-account-creation",
    # #1344 (Gap-A closure): create-user's justification is NOT "runs pre-account-creation"
    # alone (that was the pre-#1344 gap — true, but not a real gate once the Caddy perimeter
    # that used to restrict wizard access was removed Jun 29). It now requires a valid,
    # unused, atomically-consumed invite token enforced IN THE HANDLER — a real app-layer
    # gate independent of any perimeter. Specific entry (not just the blanket prefix above)
    # so this route's true protection is legible on its own, not implied by the group.
    "/api/v1/setup/create-user": "requires a valid invite token (#1344), atomically consumed "
    "in create_user — see services/auth/invite_token_service.py",
    # Optional-auth — handles auth inline; the LLM call is gated by BYO-key (#490 / #1185).
    "/api/v1/intent": "optional-auth (inline user resolution); LLM gated by BYO-key",
    # Env-gated dev tooling — 404s in production via dev_trust's require_dev_environment.
    "/api/v1/admin/trust/set-stage": "env-gated dev-only (dev_trust); 404s in prod",
}


class AuthMiddleware(BaseHTTPMiddleware):
    """
    JWT Authentication middleware for FastAPI.

    Validates JWT tokens and sets user context for authenticated requests.
    Integrates with existing OAuth flows and provides audit logging.
    """

    def __init__(
        self,
        app,
        jwt_service: JWTService,
        exclude_paths: Optional[List[str]] = None,
    ):
        """
        Initialize authentication middleware.

        Args:
            app: FastAPI application instance
            jwt_service: JWT service for token validation
            exclude_paths: Paths to exclude from authentication

        #936 (May 9 2026): user_service param removed. The previous UserService
        was wired in but never populated in production — `get_session()` always
        returned None. Real auth flow uses `users` PostgreSQL table + AuthService
        + JWT claims; user identity is set on `request.state.user_id` from JWT
        claims directly (line 172). The dead `request.state.session` write below
        also removed.
        """
        super().__init__(app)
        self.jwt_service = jwt_service
        # Default exempt list assembled from category constants above.
        # See module-level EXEMPT_* lists for the categorical breakdown.
        self.exclude_paths = exclude_paths or list(DEFAULT_EXCLUDE_PATHS)

        logger.info("AuthMiddleware initialized", exclude_paths=len(self.exclude_paths))

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request through authentication middleware.

        Args:
            request: Incoming HTTP request
            call_next: Next middleware/handler in chain

        Returns:
            HTTP response
        """
        # Skip authentication for excluded paths
        if self._should_exclude_path(request.url.path):
            return await call_next(request)

        # Extract and validate JWT token
        try:
            token = self._extract_token(request)
            if token:
                # Import exceptions for specific handling
                from services.auth.jwt_service import TokenExpired, TokenInvalid, TokenRevoked

                try:
                    claims = await self.jwt_service.validate_token(token)
                    if claims:
                        # Set user context in request state
                        request.state.user_claims = claims
                        request.state.user_id = claims.user_id
                        request.state.scopes = claims.scopes

                        # #936 (May 9 2026): removed dead UserService.get_session()
                        # call here. UserService was wired in but never populated;
                        # request.state.session never fired in production.

                        logger.debug(
                            "Request authenticated",
                            user_id=claims.user_id,
                            scopes=claims.scopes,
                            path=request.url.path,
                        )
                    else:
                        logger.warning(
                            "Invalid token provided",
                            path=request.url.path,
                            client_ip=self._get_client_ip(request),
                        )
                        return self._unauthorized_response("Invalid or expired token", request)

                except TokenRevoked:
                    logger.warning(
                        "Revoked token rejected",
                        path=request.url.path,
                        client_ip=self._get_client_ip(request),
                    )
                    return self._unauthorized_response("Token has been revoked", request)
                except TokenExpired:
                    logger.warning(
                        "Expired token rejected",
                        path=request.url.path,
                        client_ip=self._get_client_ip(request),
                    )
                    return self._unauthorized_response("Token has expired", request)
                except TokenInvalid as e:
                    logger.warning(
                        "Invalid token rejected",
                        path=request.url.path,
                        client_ip=self._get_client_ip(request),
                        error=str(e),
                    )
                    return self._unauthorized_response("Invalid token", request)
            else:
                logger.warning("No authentication token provided", path=request.url.path)
                return self._unauthorized_response("Authentication required", request)

        except Exception as e:
            logger.error("Authentication middleware error", error=str(e), path=request.url.path)
            return self._unauthorized_response("Authentication error", request)

        # Process request with authentication context
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response

    def _should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded from authentication"""
        return any(path.startswith(exclude) for exclude in self.exclude_paths)

    def _extract_token(self, request: Request) -> Optional[str]:
        """
        Extract JWT token from request.

        Supports Authorization header, query parameter, and auth_token cookie.
        Issue #390: Added cookie support for web UI authentication.
        """
        # Try Authorization header first (standard OAuth 2.0)
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header[7:]  # Remove "Bearer " prefix

        # Try query parameter (for WebSocket or special cases)
        token_param = request.query_params.get("token")
        if token_param:
            return token_param

        # Try auth_token cookie (for web UI, Issue #390)
        auth_cookie = request.cookies.get("auth_token")
        if auth_cookie:
            return auth_cookie

        return None

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request"""
        # Check X-Forwarded-For header first (for proxied requests)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"

    def _unauthorized_response(self, message: str, request: Request = None) -> Response:
        """
        Create unauthorized response.

        For browser requests to UI routes (non-API), redirect to /login.
        For API requests, return JSON 401.
        """
        from fastapi.responses import JSONResponse, RedirectResponse

        # Check if this is a browser request to a UI route (should redirect to login)
        if request:
            path = request.url.path
            accept_header = request.headers.get("accept", "")

            # If it's not an API route and browser accepts HTML, redirect to login
            is_api_route = path.startswith("/api/")
            accepts_html = "text/html" in accept_header

            if not is_api_route and accepts_html:
                # Redirect to login with return URL
                return_url = str(request.url.path)
                if request.url.query:
                    return_url += f"?{request.url.query}"
                return RedirectResponse(url=f"/login?next={return_url}", status_code=302)

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": "authentication_required",
                "message": message,
                "type": "authentication_error",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )


# FastAPI dependency for route-level authentication
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> JWTClaims:
    """
    FastAPI dependency to get current authenticated user.

    Usage:
        @app.get("/protected")
        async def protected_route(current_user: JWTClaims = Depends(get_current_user)):
            return {"user_id": current_user.user_id}

    Args:
        request: FastAPI request object (for cookie access)
        credentials: HTTP bearer credentials

    Returns:
        JWT claims for authenticated user

    Raises:
        APIError: If authentication fails (Issue #283 - for friendly error messages)

    Note:
        Issue #455: Now checks both Authorization header AND auth_token cookie
        to support web UI authentication with credentials: 'include'.
    """
    from services.api.errors import APIError
    from services.auth.container import AuthContainer
    from services.auth.jwt_service import TokenExpired, TokenInvalid, TokenRevoked

    # Extract token from Authorization header or cookie (Issue #455)
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Try auth_token cookie (for web UI)
        token = request.cookies.get("auth_token")

    if not token:
        # Issue #283: Use APIError so exception handler can convert to friendly message
        raise APIError(
            status_code=401,
            error_code="AUTHENTICATION_REQUIRED",
            details={"detail": "Authentication required"},
        )

    # Get JWT service singleton with blacklist support
    jwt_service = AuthContainer.get_jwt_service()

    try:
        claims = await jwt_service.validate_token(token)
        if not claims:
            raise APIError(
                status_code=401,
                error_code="INVALID_TOKEN",
                details={"detail": "Invalid or expired token"},
            )

        return claims

    except TokenRevoked:
        raise APIError(
            status_code=401,
            error_code="TOKEN_REVOKED",
            details={"detail": "Token has been revoked"},
        )
    except TokenExpired:
        raise APIError(
            status_code=401,
            error_code="TOKEN_EXPIRED",
            details={"detail": "Token has expired"},
        )
    except TokenInvalid:
        raise APIError(
            status_code=401,
            error_code="INVALID_TOKEN",
            details={"detail": "Invalid token"},
        )


# Note: `require_request_context` removed 2026-05-16 per #1015 Phase 2 + Pattern-073
# instance disposition. The function was defined for a Phase 2 RequestContext-everywhere
# migration that has been descoped via ADR-051 amendment (RequestContext is now
# intent-path-specific; see services/domain/models.py RequestContext docstring + ADR-051
# amendment section). The dependency had zero production callers; keeping it around was
# itself the doc-drift shape Pattern-073 names ("documentation/code asserting a contract
# the system doesn't honor"). If the Pattern-072 second-coordination-surface trigger
# fires later, re-introducing the dependency is a ~10-line edit.


def require_scopes(required_scopes: List[str]):
    """
    FastAPI dependency to require specific scopes.

    Usage:
        @app.get("/admin")
        async def admin_route(
            current_user: JWTClaims = Depends(get_current_user),
            _: None = Depends(require_scopes(["admin", "write"]))
        ):
            return {"message": "Admin access granted"}

    Args:
        required_scopes: List of required scopes

    Returns:
        Dependency function
    """

    def scope_checker(current_user: JWTClaims = Depends(get_current_user)):
        user_scopes = set(current_user.scopes)
        required_scope_set = set(required_scopes)

        if not required_scope_set.issubset(user_scopes):
            missing_scopes = required_scope_set - user_scopes
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Missing scopes: {', '.join(missing_scopes)}",
            )

        return current_user

    return scope_checker


class MCPAuthAdapter:
    """
    MCP Protocol Authentication Adapter.

    Provides authentication compatibility for MCP (Model Context Protocol)
    integration with standardized token validation.
    """

    def __init__(self, jwt_service: JWTService):
        """Initialize MCP auth adapter"""
        self.jwt_service = jwt_service
        logger.info("MCP authentication adapter initialized")

    async def validate_mcp_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Validate token for MCP protocol compatibility.

        Args:
            token: JWT token to validate

        Returns:
            MCP-compatible authentication info or None
        """
        from services.auth.jwt_service import TokenExpired, TokenInvalid, TokenRevoked

        try:
            claims = await self.jwt_service.validate_token(token)
            if not claims or not claims.mcp_compatible:
                return None

            return {
                "user_id": claims.user_id,
                "scopes": claims.scopes,
                "session_id": claims.session_id,
                "workspace_id": claims.workspace_id,
                "valid": True,
            }
        except (TokenRevoked, TokenExpired, TokenInvalid):
            return None

    def create_mcp_context(self, claims: JWTClaims) -> Dict[str, Any]:
        """
        Create MCP execution context from JWT claims.

        Args:
            claims: Validated JWT claims

        Returns:
            MCP execution context
        """
        return {
            "user": {"id": claims.user_id, "email": claims.user_email, "scopes": claims.scopes},
            "session": {"id": claims.session_id, "workspace_id": claims.workspace_id},
            "auth": {
                "method": "jwt",
                "token_id": claims.jti,
                "issued_at": claims.iat,
                "expires_at": claims.exp,
            },
        }
