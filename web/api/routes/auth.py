"""
Authentication API Routes

Provides JWT authentication endpoints including login, logout, and token management.
Integrates with TokenBlacklist for secure token revocation.

Issue #281: CORE-ALPHA-WEB-AUTH
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog
from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims, JWTService
from services.auth.models import (
    LoginRequest,
    LoginResponse,
    PasswordChangeRequest,
    PasswordChangeResponse,
)
from services.auth.password_service import PasswordService
from services.auth.password_validator import PasswordValidator
from services.database.connection import db
from services.database.models import User
from services.database.session_factory import AsyncSessionFactory

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])
# piper-morgan-fb9: auto_error=False allows logout to handle missing/invalid tokens gracefully
security = HTTPBearer(auto_error=False)
logger = structlog.get_logger(__name__)


from services.consciousness.auth_consciousness import (
    format_logout_success_conscious,
    format_password_changed_conscious,
)


def build_audit_context(request: Request) -> Dict[str, Any]:
    """
    Extract audit context from FastAPI request.

    Args:
        request: FastAPI Request object

    Returns:
        Dict with ip_address, user_agent, request_id, request_path

    Issue #249: Audit logging context helper
    """
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "request_id": request.headers.get("x-request-id"),
        "request_path": str(request.url.path),
    }


async def get_jwt_service(request: Request) -> JWTService:
    """
    Dependency injection for JWTService.

    Uses AuthContainer for singleton JWT service with proper DI.
    Fixed: Issue #258 CORE-AUTH-CONTAINER
    """
    # Get from AuthContainer (singleton pattern)
    from services.auth.container import AuthContainer

    return AuthContainer.get_jwt_service()


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    username: str = Form(..., min_length=1),
    password: str = Form(..., min_length=1),
    # #1572: the browser's IANA timezone, posted by auth.js from
    # Intl.DateTimeFormat().resolvedOptions().timeZone. Optional — every
    # existing client that doesn't send it logs in unchanged. Named
    # browser_timezone on the wire (and here) so it can't shadow the
    # datetime.timezone import this module uses.
    browser_timezone: Optional[str] = Form(None, max_length=64),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Authenticate user with username/password and return JWT token.

    Security Features:
    - Bcrypt password verification (timing-safe)
    - Generic error messages (prevent user enumeration)
    - JWT token generation with user claims
    - Cookie-based auth for web clients
    - Bearer token for API clients

    Args:
        request: FastAPI Request object for audit context
        response: FastAPI Response object for setting cookies
        username: Username from form data
        password: Password from form data
        jwt_service: JWT service for token generation

    Returns:
        LoginResponse with token, user_id, username

    Raises:
        HTTPException 401: Invalid credentials or user not active
        HTTPException 500: Server error during authentication

    Issue #281: CORE-ALPHA-WEB-AUTH
    Issue #393: Auth UI Phase 1 - Form data support
    """
    try:
        # Validate credentials are not empty
        username = username.strip()
        if not username or not password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
            )

        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user and update last_login in single session
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # #1261: accept username OR email as the login identifier (PM hit
            # this wall in UAT — tried email, field wanted username, dead end).
            # Username takes precedence, then email (both columns are unique;
            # sequential lookups keep the edge case "one user's username equals
            # another's email" deterministic instead of MultipleResultsFound).
            # The form field stays named `username` — existing clients depend
            # on that contract; only the accepted VALUES widened.
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalar_one_or_none()
            if user is None and "@" in username:
                result = await session.execute(select(User).where(User.email == username))
                user = result.scalar_one_or_none()

            # User not found - generic error message for security
            if not user:
                logger.warning(
                    "login_failed_user_not_found",
                    username=username,
                    ip_address=request.client.host if request.client else None,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                )

            # Check if user is active
            if not user.is_active:
                logger.warning(
                    "login_failed_user_inactive",
                    user_id=str(user.id),
                    username=user.username,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is inactive. Please contact administrator.",
                )

            # Check if password is set
            if not user.password_hash:
                logger.warning(
                    "login_failed_no_password",
                    user_id=str(user.id),
                    username=user.username,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Password not set for this account. Please contact administrator.",
                )

            # Verify password
            password_service = PasswordService()
            is_valid = password_service.verify_password(password, user.password_hash)

            if not is_valid:
                logger.warning(
                    "login_failed_invalid_password",
                    user_id=str(user.id),
                    username=user.username,
                    ip_address=request.client.host if request.client else None,
                )
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                )

            # Update last_login_at (in same session)
            user.last_login_at = datetime.now(timezone.utc)

            # #1572: per-user timezone capture — the supply half the
            # 2026-08-10 time audit found at 0%. Validated IANA name into
            # users.preferences["timezone"], riding the same commit as
            # last_login_at. Best-effort: a missing or invalid value never
            # affects login (fail-safe direction — consumers then keep the
            # server-clock/UTC-labeled behavior).
            if browser_timezone:
                from services.utils.user_timezone import (
                    TIMEZONE_PREF_KEY,
                    is_valid_iana_timezone,
                )

                if is_valid_iana_timezone(browser_timezone):
                    # New dict on purpose: reassignment marks the JSONB
                    # column dirty; in-place mutation can silently not
                    # persist (collaboration_gate._save_preference rationale).
                    prefs = dict(user.preferences or {})
                    if prefs.get(TIMEZONE_PREF_KEY) != browser_timezone:
                        prefs[TIMEZONE_PREF_KEY] = browser_timezone
                        user.preferences = prefs
                else:
                    logger.warning(
                        "login_browser_timezone_invalid",
                        user_id=str(user.id),
                        browser_timezone=browser_timezone[:64],
                    )

            await session.commit()

            # Store user details for response (before session closes)
            user_id = str(user.id)
            username = user.username
            user_email = user.email

        # Generate JWT token (after session closed)
        audit_context = build_audit_context(request)
        token = jwt_service.generate_access_token(
            user_id=user_id,
            user_email=user_email,
            scopes=["user"],  # Default scope for alpha users
            username=username,  # Issue #730: Include username in token
        )

        # Issue #857: Generate refresh token for seamless session continuity.
        # The refresh token has a longer lifetime than the access token and is
        # used by the frontend to silently obtain a new access token when the
        # access token expires. Stored in a separate httponly cookie.
        refresh_token = jwt_service.generate_refresh_token(
            user_id=user_id,
            user_email=user_email,
            session_id=None,
            workspace_id=None,
        )

        # Set cookie for web clients
        # Detect if request is HTTPS to set secure flag appropriately
        # This allows HTTP development while enforcing HTTPS cookies in production
        is_https = (
            request.headers.get("x-forwarded-proto", request.url.scheme).lower() == "https"
        )  # behind fly-proxy the internal hop is http; trust the edge proto so the
        # auth cookie carries Secure on the real HTTPS site (2026-07-12)
        response.set_cookie(
            key="auth_token",
            value=token,
            httponly=True,
            secure=is_https,  # Only set secure flag for HTTPS requests
            samesite="lax",
            max_age=86400,  # 24 hours for alpha testing UX
        )

        # Issue #857: refresh-token cookie. 7-day max-age matches JWTService's
        # refresh_token_expire_days default. Httponly + same security flags as
        # auth_token. The /api/v1/auth/refresh endpoint reads this cookie.
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=is_https,
            samesite="lax",
            max_age=7 * 86400,  # 7 days
        )

        logger.info(
            "login_successful",
            user_id=user_id,
            username=username,
            ip_address=request.client.host if request.client else None,
        )

        return LoginResponse(
            token=token,
            user_id=user_id,
            username=username,
        )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, auth failures)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "login_error",
            username=username,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed",
        )


@router.post("/refresh", response_model=LoginResponse)
async def refresh_token(
    request: Request,
    response: Response,
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Generate new access token from a valid refresh token.

    Issue #857: INFRA token refresh mechanism for seamless session continuity.

    Reads `refresh_token` cookie set at login. Validates via
    JWTService.refresh_access_token. Generates a fresh access token AND
    rotates the refresh token (new refresh token issued on every use per AC).
    Both new tokens set as cookies; client doesn't need to handle them
    directly (cookies are httponly).

    Returns:
        LoginResponse with the new access token.

    Raises:
        HTTPException 401: No refresh token cookie, or refresh token invalid
            or expired. Cookies are cleared on 401 so client falls back to
            login flow.
    """
    # Read refresh token from cookie
    refresh_token_value = request.cookies.get("refresh_token")
    if not refresh_token_value:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
        )

    audit_context = build_audit_context(request)

    # Try to refresh; JWTService validates the refresh token + returns new access token
    try:
        async with AsyncSessionFactory.session_scope_fresh() as db_session:
            new_access_token = await jwt_service.refresh_access_token(
                refresh_token=refresh_token_value,
                session=db_session,
                audit_context=audit_context,
            )
    except Exception as e:
        logger.warning("refresh_token_validation_error", error=str(e))
        new_access_token = None

    if not new_access_token:
        # Invalid/expired refresh token — clear cookies so client falls back
        # to login. #1078: route through HTTPExceptionWithCookieClear so the
        # #283 friendly-error handler preserves the Set-Cookie headers on
        # the rebuilt JSONResponse. (Setting them on `response` directly is
        # silently dropped during the handler's rebuild.)
        from web.api.exceptions import HTTPExceptionWithCookieClear

        raise HTTPExceptionWithCookieClear(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalid or expired",
            clear_cookies=["auth_token", "refresh_token"],
        )

    # Decode the new access token to get claims for the response + new refresh token
    new_claims = await jwt_service.validate_token(new_access_token)
    if not new_claims:
        # Sanity check; shouldn't fire since we just generated the token
        logger.error("refresh_decoded_invalid", token_preview=new_access_token[:20])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed",
        )

    # Issue #857: Refresh token rotation — generate NEW refresh token on every use.
    # The old refresh token is naturally invalidated by being replaced in the cookie.
    new_refresh_token = jwt_service.generate_refresh_token(
        user_id=new_claims.user_id,
        user_email=new_claims.user_email,
        session_id=new_claims.session_id,
        workspace_id=new_claims.workspace_id,
    )

    # Set both cookies (same flags as login)
    is_https = (
        request.headers.get("x-forwarded-proto", request.url.scheme).lower() == "https"
    )  # behind fly-proxy the internal hop is http; trust the edge proto so the
    # auth cookie carries Secure on the real HTTPS site (2026-07-12)
    response.set_cookie(
        key="auth_token",
        value=new_access_token,
        httponly=True,
        secure=is_https,
        samesite="lax",
        max_age=86400,
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=is_https,
        samesite="lax",
        max_age=7 * 86400,
    )

    logger.info(
        "token_refreshed",
        user_id=new_claims.user_id,
        ip_address=request.client.host if request.client else None,
    )

    return LoginResponse(
        token=new_access_token,
        user_id=new_claims.user_id,
        username=new_claims.username or new_claims.user_email,
    )


@router.post("/logout")
async def logout(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Logout user by revoking their access token.

    The token will be added to the blacklist and no longer valid for authentication.
    Even if the token hasn't expired, it will be rejected by the middleware.

    piper-morgan-fb9: This endpoint now handles authentication gracefully:
    - If valid token: revoke it and return success
    - If invalid/expired/revoked token: return success (already logged out)
    - If no token: return success (nothing to log out)

    Args:
        request: FastAPI Request object for audit context
        credentials: Bearer token credentials (optional with auto_error=False)
        jwt_service: JWT service for token revocation

    Returns:
        Success message with user ID (if known)

    Raises:
        HTTPException 500: If token revocation fails unexpectedly

    Issue #249: Added audit logging
    piper-morgan-fb9: Handle missing/invalid tokens gracefully
    """
    # piper-morgan-fb9: Extract token from Authorization header or cookie
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Try auth_token cookie (for web UI)
        token = request.cookies.get("auth_token")

    if not token:
        # No token provided - user is already logged out or never logged in
        # Issue #723: Still delete cookie in case browser has stale cookie
        logger.info("Logout called with no token - user already logged out")
        from fastapi.responses import JSONResponse

        response = JSONResponse(
            content={"message": format_logout_success_conscious(), "user_id": None}
        )
        response.delete_cookie(key="auth_token", path="/")
        return response

    try:
        # Build audit context from request (Issue #249)
        audit_context = build_audit_context(request)

        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # piper-morgan-fb9: Try to validate token to get user_id for logging
        # If token is invalid/expired/revoked, we still consider logout successful
        user_id = None
        try:
            claims = await jwt_service.validate_token(token)
            if claims:
                user_id = claims.user_id
        except Exception:
            # Token is invalid/expired/revoked - that's fine for logout
            # Try to decode without validation to get user_id for logging
            try:
                import jwt as pyjwt

                decoded = pyjwt.decode(token, options={"verify_signature": False})
                user_id = decoded.get("sub") or decoded.get("user_id")
            except Exception:
                pass

        # Revoke the token via blacklist with audit logging
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            success = await jwt_service.revoke_token(
                token=token,
                reason="logout",
                user_id=user_id,
                session=session,
                audit_context=audit_context,
            )
            await session.commit()

        # piper-morgan-fb9: Always return success - user is logged out either way
        # Even if revoke_token returns False (e.g., token already revoked), the user is still logged out
        if success:
            logger.info("User logged out successfully", user_id=user_id)
        else:
            logger.info(
                "Token may already be revoked, treating as successful logout", user_id=user_id
            )

        # Issue #723: Clear the auth_token cookie so browser stops sending revoked token
        from fastapi.responses import JSONResponse

        response = JSONResponse(
            content={"message": format_logout_success_conscious(), "user_id": user_id}
        )
        response.delete_cookie(key="auth_token", path="/")
        return response

    except Exception as e:
        logger.error("Logout error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Logout failed: {str(e)}"
        )


@router.get("/me")
async def get_me(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get current authenticated user's information.

    Returns the user's basic profile information by querying the database
    with the user_id from the authenticated JWT token.

    Args:
        current_user: Current authenticated user (from JWT token)

    Returns:
        User information (user_id, username, email)

    Raises:
        HTTPException 401: If not authenticated or token invalid
        HTTPException 404: If user not found in database

    Issue #281: CORE-ALPHA-WEB-AUTH
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Query user by ID from token
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(select(User).where(User.id == current_user.user_id))
            user = result.scalar_one_or_none()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )

            return {
                "user_id": str(user.id),
                "username": user.username,
                "email": user.email,
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_me_error", user_id=current_user.user_id, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user information",
        )


@router.post("/change-password", response_model=PasswordChangeResponse)
async def change_password(
    request: Request,
    data: PasswordChangeRequest,
    current_user: JWTClaims = Depends(get_current_user),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    jwt_service: JWTService = Depends(get_jwt_service),
):
    """
    Change user password and invalidate current token.

    Requires valid authentication. User must provide their current password
    for verification. New password is validated for strength requirements.

    After successful password change:
    - Current token is added to blacklist
    - User must log in again with new password
    - Old token will be rejected (401 Unauthorized)

    Args:
        request: FastAPI Request object for audit context
        data: PasswordChangeRequest with current_password, new_password, new_password_confirm
        current_user: Current authenticated user (from JWT token)
        credentials: Bearer token credentials
        jwt_service: JWT service for token management

    Returns:
        PasswordChangeResponse with success=True and success message

    Raises:
        HTTPException 400: Password validation fails (specific requirement)
        HTTPException 400: New passwords don't match
        HTTPException 401: Current password incorrect
        HTTPException 401: Token invalid/expired
        HTTPException 500: Unexpected server error

    Security:
    - Current password verified before accepting change
    - New password validated for strength (8+ chars, upper, lower, number, special)
    - Passwords must match exactly (case-sensitive)
    - Token invalidated immediately (force re-authentication)
    - Constant-time password comparison (bcrypt)

    Issue #298: AUTH-PASSWORD-CHANGE
    """
    try:
        # Initialize database if needed
        if not db._initialized:
            await db.initialize()

        # Verify new passwords match
        if data.new_password != data.new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New passwords do not match",
            )

        # Validate new password strength
        is_valid, error_message = PasswordValidator.validate(data.new_password)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        # Get database session for password update
        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Hash new password
            password_service = PasswordService()
            new_password_hash = password_service.hash_password(data.new_password)

            # Change password via JWT service
            # This will verify current password, update password hash, and revoke token
            # piper-morgan-fb9: Handle optional credentials (should not happen due to get_current_user)
            if not credentials:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )
            token = credentials.credentials
            try:
                success = await jwt_service.change_password(
                    user_id=current_user.user_id,
                    current_password=data.current_password,
                    new_password_hash=new_password_hash,
                    current_token=token,
                    session=session,
                    password_service=password_service,
                )

                if success:
                    logger.info(
                        "Password changed successfully",
                        user_id=current_user.user_id,
                        username=current_user.user_email,
                    )
                    return PasswordChangeResponse(
                        success=True,
                        message=format_password_changed_conscious(),
                    )
                else:
                    logger.error(
                        "Password change failed in service",
                        user_id=current_user.user_id,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Failed to change password",
                    )

            except ValueError as e:
                # Current password incorrect or validation error
                if "Current password is incorrect" in str(e):
                    logger.warning(
                        "Password change failed: incorrect current password",
                        user_id=current_user.user_id,
                    )
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Current password is incorrect",
                    )
                else:
                    logger.warning(
                        "Password change failed: validation error",
                        user_id=current_user.user_id,
                        error=str(e),
                    )
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=str(e),
                    )

    except HTTPException:
        # Re-raise HTTP exceptions (validation errors, auth failures)
        raise
    except Exception as e:
        # Unexpected errors
        logger.error(
            "password_change_error",
            user_id=current_user.user_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password change failed",
        )


# ---------------------------------------------------------------------------
# #441 Phase 3 / #1261 — password reset via PM-issued reset code (beta model)
# ---------------------------------------------------------------------------
from pydantic import BaseModel, Field  # noqa: E402

from services.auth.password_reset_service import consume_reset_token  # noqa: E402


class PasswordResetRequest(BaseModel):
    """Reset payload: the PM-issued code + the new password (pre-login flow)."""

    reset_token: str = Field(min_length=1, description="PM-issued reset code")
    new_password: str = Field(min_length=8, description="New password")
    new_password_confirm: str = Field(min_length=8, description="Confirmation")


class PasswordResetResponse(BaseModel):
    success: bool
    message: str


@router.post("/reset-password", response_model=PasswordResetResponse)
async def reset_password(request: Request, data: PasswordResetRequest):
    """Reset a forgotten password with a PM-issued reset code (#441/#1261).

    The beta auth model's equivalent of an email reset link: no mailer exists
    in the product, so PM/HOST mint a single-use, expiring, account-bound code
    (scripts/mint_password_reset_token.py) and hand it to the tester over the
    #1344 invite channel. The code determines WHICH account is reset — the
    request never names a user, so the endpoint can't be pointed at an
    arbitrary account (you reset exactly the account the code was minted for).

    Security:
    - Token consumption is a single atomic conditional UPDATE (unused +
      unexpired), in the SAME transaction as the password write — a burned
      code and a failed write commit or roll back together.
    - Generic 400 on any invalid/expired/used code (no oracle for which).
    - New password strength-validated (same PasswordValidator as change-password).
    - Auth-exempt by necessity (the caller can't log in — that's the point),
      justified in AUTH_EXEMPT_JUSTIFIED per #1308.
    """
    try:
        if data.new_password != data.new_password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New passwords do not match",
            )

        is_valid, error_message = PasswordValidator.validate(data.new_password)
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)

        if not db._initialized:
            await db.initialize()

        async with AsyncSessionFactory.session_scope_fresh() as session:
            user_id = await consume_reset_token(session, data.reset_token)
            if user_id is None:
                logger.warning(
                    "password_reset_failed_invalid_token",
                    ip_address=request.client.host if request.client else None,
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset code",
                )

            password_service = PasswordService()
            new_hash = password_service.hash_password(data.new_password)
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            if user is None or not user.is_active:
                # Bound account vanished/deactivated since mint — same generic 400.
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or expired reset code",
                )
            user.password_hash = new_hash
            user.updated_at = datetime.now(timezone.utc)
            await session.commit()

        logger.info("password_reset_succeeded", user_id=str(user_id))
        return PasswordResetResponse(
            success=True, message="Password reset. You can now log in with your new password."
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("password_reset_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password reset failed",
        )
