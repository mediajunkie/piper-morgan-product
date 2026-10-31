"""
Setup Wizard API Routes

Provides REST endpoints for the web-based setup wizard UI.
Mirrors functionality from scripts/setup_wizard.py with async HTTP wrappers.

Issue #390: ALPHA-SETUP-UI Phase 1.1 - Backend API
"""

import asyncio
import os
import subprocess
import urllib.parse
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select, text

from services.auth.auth_middleware import get_current_user
from services.auth.invite_token_service import check_invite_token, consume_invite_token
from services.auth.jwt_service import JWTClaims
from services.auth.password_service import PasswordService
from services.auth.session_cookies import set_session_cookies
from services.config.llm_config_service import KEY_CHECK_UNAVAILABLE_MESSAGE, KeyCheckUnavailable
from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.deployment import is_hosted_deployment
from services.integrations.integration_status_service import (
    connector_offered,
    refuse_unless_offered,
)
from services.security.field_encryption import KeyStoreConfigError
from services.security.user_api_key_service import UserAPIKeyService

router = APIRouter(prefix="/api/v1/setup", tags=["setup"])
logger = structlog.get_logger(__name__)


# ============================================================================
# Pydantic Models
# ============================================================================


class SystemCheckResponse(BaseModel):
    """Response model for system requirements check"""

    docker_available: bool = Field(description="Docker installed and running")
    postgres_ready: bool = Field(description="PostgreSQL accessible on port 5433")
    redis_ready: bool = Field(description="Redis accessible on port 6379")
    chromadb_ready: bool = Field(description="ChromaDB accessible on port 8000")
    temporal_ready: bool = Field(description="Temporal accessible on port 7233 (optional)")
    database_migrated: bool = Field(
        default=False, description="Database schema is up to date (migrations applied)"
    )
    all_required_ready: bool = Field(description="All required services ready (excludes Temporal)")
    message: str = Field(description="Human-readable status message")


class ApiKeyValidateRequest(BaseModel):
    """Request model for API key validation"""

    provider: str = Field(description="API provider: openai, anthropic, github, or notion")
    api_key: str = Field(description="API key to validate")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in ["openai", "anthropic", "github", "notion"]:
            raise ValueError("provider must be one of: openai, anthropic, github, notion")
        return v


class ApiKeyValidateResponse(BaseModel):
    """Response model for API key validation"""

    provider: str = Field(description="API provider that was validated")
    valid: bool = Field(description="Whether the key is valid")
    message: str = Field(description="Validation result message")
    workspace_name: Optional[str] = Field(
        default=None, description="Workspace name (for Notion integration)"
    )


class CreateUserRequest(BaseModel):
    """Request model for user account creation"""

    username: str = Field(min_length=1, max_length=100, description="Username (required)")
    # #1348: required, matching the DB (User.email is NOT NULL + unique) — and
    # since #1261, email is a real login identifier AND the password-reset mint
    # key, so a user without one would be locked out of both recovery paths.
    # Previously Optional -> a missing email leaked a Postgres NotNullViolation
    # as a confusing 500 instead of a clean 422.
    email: str = Field(min_length=3, max_length=255, description="Email (required)")
    password: str = Field(min_length=8, description="Password (minimum 8 characters)")
    password_confirm: str = Field(min_length=8, description="Password confirmation")
    invite_token: str = Field(min_length=1, description="Alpha invite token (#1344, required)")

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class CreateUserResponse(BaseModel):
    """Response model for user account creation"""

    success: bool = Field(description="Whether user creation succeeded")
    user_id: Optional[str] = Field(default=None, description="Created user ID (UUID)")
    message: str = Field(description="Result message")


class KeychainCheckResponse(BaseModel):
    """Response model for keychain key check"""

    provider: str = Field(description="API provider checked")
    exists: bool = Field(description="Whether key exists in keychain")
    message: str = Field(description="Human-readable status")


class KeychainUseRequest(BaseModel):
    """Request model for using key from keychain"""

    provider: str = Field(description="API provider: openai, anthropic, gemini, or notion")

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in ["openai", "anthropic", "gemini", "notion"]:
            raise ValueError("provider must be one of: openai, anthropic, gemini, notion")
        return v


class KeychainUseResponse(BaseModel):
    """Response model for using key from keychain"""

    provider: str = Field(description="API provider")
    success: bool = Field(description="Whether key was retrieved and validated")
    valid: bool = Field(description="Whether the key is valid (if retrieved)")
    message: str = Field(description="Result message")


class SetupCompleteRequest(BaseModel):
    """Request model for completing setup"""

    # #2078: the principal is the signed-in session; a body user_id is accepted
    # only when it matches it (a stale client fails loudly with 403).
    user_id: Optional[str] = Field(
        default=None, description="Must match the signed-in user, if sent (#2078)"
    )
    default_llm_provider: Optional[str] = Field(
        default=None, description="User's chosen LLM provider (openai or anthropic)"
    )
    openai_key: Optional[str] = Field(default=None, description="OpenAI API key (optional)")
    anthropic_key: Optional[str] = Field(default=None, description="Anthropic API key (optional)")
    notion_key: Optional[str] = Field(default=None, description="Notion API key (optional)")


class SetupCompleteResponse(BaseModel):
    """Response model for completing setup"""

    success: bool = Field(description="Whether setup completion succeeded")
    message: str = Field(description="Result message")
    redirect_url: str = Field(description="URL to redirect to after setup")


# ============================================================================
# Helper Functions (adapted from setup_wizard.py)
# ============================================================================

# True when running on managed/containerized infrastructure — Docker
# (/.dockerenv sentinel), Fly.io (FLY_APP_NAME — Firecracker microVMs have NO
# /.dockerenv, the 2026-07-12 beta.pipermorgan.ai live find), or any deployment
# declaring PIPER_ENVIRONMENT=production. On managed infra the platform runs
# the services; wizard "system requirements" reflect that instead of probing
# for a Docker CLI in the tester's browser-facing container.
# #2151: the signal lives in services/infrastructure/deployment.py so other surfaces
# (local_git_status_query) use the same one. Still read once, at import, here.
_IN_DOCKER = is_hosted_deployment()


def wizard_is_hosted() -> bool:
    """#2089 (CXO 2026-10-19): the setup page renders without the System step
    when the platform runs the services (Fly, Docker, or a declared production
    environment), the same signals check_docker trusts. With none present the
    wizard keeps the System check rather than hide a real failure."""
    return _IN_DOCKER


async def check_docker() -> bool:
    """Check if Docker is available.

    Inside a Docker container (hosted alpha, CI), Docker-managed services are running
    by definition — the container itself proves that. Returns True immediately rather
    than shelling out to a Docker CLI that doesn't exist inside the app container.
    Local dev: falls back to the CLI check.
    """
    if _IN_DOCKER:
        return True
    try:
        result = await asyncio.to_thread(
            subprocess.run, ["docker", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return False


async def check_service_port(host: str, port: int) -> bool:
    """Check if a service is accessible on a specific port (from setup_wizard.py line 451)"""
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=2.0)
        writer.close()
        await writer.wait_closed()
        return True
    except Exception:
        return False


async def check_database() -> bool:
    """Check PostgreSQL database connectivity.

    Reads POSTGRES_HOST / POSTGRES_PORT from the environment (loaded by python-dotenv
    at app startup from .env). On the hosted Droplet these are 'postgres' / 5432 (Docker
    internal); local dev defaults to localhost:5433 (published port).
    """
    # #1278/Fly: 12-factor deployments carry DATABASE_URL, not POSTGRES_* —
    # honor it first (same convention fix as the engines).
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        parsed = urllib.parse.urlparse(db_url)
        return await check_service_port(parsed.hostname or "localhost", parsed.port or 5432)
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", "5433"))
    return await check_service_port(host, port)


async def check_redis() -> bool:
    """Check Redis connectivity.

    Parses host and port from REDIS_URL (e.g. redis://:password@redis:6379).
    Falls back to localhost:6379 for local dev without REDIS_URL set.
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    parsed = urllib.parse.urlparse(redis_url)
    host = parsed.hostname or "localhost"
    port = parsed.port or 6379
    return await check_service_port(host, port)


async def check_chromadb() -> bool:
    """Check ChromaDB connectivity.

    Reads CHROMADB_HOST / CHROMADB_PORT from env. Defaults to 'chromadb:8000'
    when running inside Docker (service name), 'localhost:8000' for local dev.
    """
    # Fly names it CHROMA_HOST/CHROMA_PORT (fly.toml [env]) — honor both spellings.
    if os.getenv("CHROMA_HOST"):
        return await check_service_port(
            os.getenv("CHROMA_HOST"), int(os.getenv("CHROMA_PORT", "8000"))
        )
    default_host = "chromadb" if _IN_DOCKER else "localhost"
    host = os.getenv("CHROMADB_HOST", default_host)
    port = int(os.getenv("CHROMADB_PORT", "8000"))
    return await check_service_port(host, port)


async def check_temporal() -> bool:
    """Check Temporal connectivity.

    Reads TEMPORAL_HOST / TEMPORAL_PORT from env (set in .env on the Droplet).
    Defaults to localhost:7233 for local dev.
    """
    host = os.getenv("TEMPORAL_HOST", "localhost")
    port = int(os.getenv("TEMPORAL_PORT", "7233"))
    return await check_service_port(host, port)


# ============================================================================
# API Endpoints
# ============================================================================


async def _completed_setup_exists() -> bool:
    """#1504: does any user have setup_complete = true? Same predicate the
    /status route has used since #389 — reused as the lockout condition so
    "set up" means one thing."""
    from sqlalchemy import text

    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope_fresh() as session:
        result = await session.execute(
            text("SELECT COUNT(*) FROM users WHERE setup_complete = true")
        )
        return (result.scalar() or 0) > 0


async def require_setup_incomplete() -> None:
    """#1504 lockout: the /api/v1/setup prefix is auth-exempt (first-run needs
    it), which left these WRITE routes callable by anyone forever — global
    LLM-key overwrite, global Slack creds, project rows with attacker-chosen
    owner_id, and an unauthenticated alembic-upgrade trigger (F1-F4, audit
    2026-08-07). Once ANY user has completed setup the wizard's writes refuse;
    signed-in management lives in Settings → Integrations. Fail-closed: a DB
    error refuses rather than allows.
    """
    try:
        already = await _completed_setup_exists()
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Couldn't verify setup state — try again in a moment.",
        )
    if already:
        raise HTTPException(
            status_code=403,
            detail=(
                "Setup is already complete on this server. Sign in and manage "
                "credentials and projects from Settings → Integrations instead."
            ),
        )


def _setup_principal(current_user: JWTClaims, body_user_id: Optional[str]) -> str:
    """#2078: a per-user wizard write takes its principal from the SESSION, never
    from the request body (Arch's rule, 2026-10-17; ADR-080 D3: code decides
    permission). create-user signs the new account in, so on a fresh instance
    and an initialized one alike the wizard's own calls carry the cookie. A body
    ``user_id`` is tolerated only when it equals the principal: a stale client
    fails with 403 rather than being silently redirected onto another account.
    This replaces the #1504 lockout on ``/complete`` and ``/projects``: the
    principal check is what stops F1 (anyone writing anyone's keys)."""
    principal = str(current_user.sub)
    if body_user_id is not None and str(body_user_id) != principal:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This setup step applies to the signed-in account only.",
        )
    return principal


async def ensure_database_migrated() -> bool:
    """
    Check for pending migrations and auto-apply them if needed.

    This ensures the web-based setup wizard works on a fresh database
    without requiring the user to manually run alembic. Returns True
    if the database schema is up to date after this call.
    """
    try:
        from services.infrastructure.migration_checker import check_pending_migrations

        pending = await check_pending_migrations()
        if not pending:
            logger.debug("database_migration_check", status="up_to_date")
            return True

        logger.info(
            "database_migrations_pending",
            count=len(pending),
            action="auto_applying",
        )

        # Run alembic upgrade head as a subprocess
        # This is the same approach used by scripts/setup_wizard.py
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        result = await asyncio.to_thread(
            subprocess.run,
            ["python", "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=project_root,
        )

        if result.returncode == 0:
            logger.info("database_migrations_applied", output=result.stdout.strip())
            return True
        else:
            logger.error(
                "database_migration_failed",
                returncode=result.returncode,
                stderr=result.stderr.strip(),
            )
            return False

    except Exception as e:
        logger.error("database_migration_error", error=str(e))
        return False


@router.post(
    "/check-system",
    response_model=SystemCheckResponse,
)
async def check_system():
    """
    Check system requirements and service availability.

    NOT gated by require_setup_incomplete (#1875): this is a READ — the #1504
    lockout was about the wizard's WRITES (F1–F4). Gating it 403'd Step 1 for
    every new user on an already-initialized instance, which is the invite
    path alpha testers actually take.

    Verifies Docker installation and checks connectivity to all required services:
    - PostgreSQL (port 5433) - required
    - Redis (port 6379) - required
    - ChromaDB (port 8000) - required
    - Temporal (port 7233) - optional

    Returns:
        SystemCheckResponse with service availability status
    """
    try:
        # Run all checks in parallel
        docker_ok, postgres_ok, redis_ok, chromadb_ok, temporal_ok = await asyncio.gather(
            check_docker(),
            check_database(),
            check_redis(),
            check_chromadb(),
            check_temporal(),
            return_exceptions=False,
        )

        # If Postgres is reachable, auto-apply any pending migrations
        # so the schema is ready before the user reaches account creation
        db_migrated = False
        if postgres_ok:
            db_migrated = await ensure_database_migrated()

        # All required services must be ready (Temporal is optional)
        all_required = docker_ok and postgres_ok and redis_ok and chromadb_ok

        # Build status message
        if all_required:
            if not db_migrated:
                message = "Services ready but database migration failed — check logs"
            elif temporal_ok:
                message = "All services ready"
            else:
                message = "Core services ready (Temporal optional)"
        else:
            failed_services = []
            if not docker_ok:
                failed_services.append("Docker")
            if not postgres_ok:
                failed_services.append("PostgreSQL")
            if not redis_ok:
                failed_services.append("Redis")
            if not chromadb_ok:
                failed_services.append("ChromaDB")
            message = f"Services not ready: {', '.join(failed_services)}"

        return SystemCheckResponse(
            docker_available=docker_ok,
            postgres_ready=postgres_ok,
            redis_ready=redis_ok,
            chromadb_ready=chromadb_ok,
            temporal_ready=temporal_ok,
            database_migrated=db_migrated,
            all_required_ready=all_required,
            message=message,
        )

    except Exception as e:
        logger.error("system_check_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SYSTEM_CHECK_COULD_NOT_RUN_MESSAGE,
        )


# #2151 route group 4 (Arch 10-24 09:09, the #2125 shape): Notion answered with a server
# error, so the key was never checked. Never "Invalid API key". Wording pending CXO.
NOTION_CHECK_FAILED_MESSAGE = (
    "Couldn't check this key with Notion just now, so it wasn't saved. "
    "Try again in a moment; if it keeps failing, tell us."
)
_NOTION_SERVER_ERROR_CODES = frozenset({"internal_server_error", "service_unavailable"})


async def validate_notion_key_and_get_workspace(
    api_key: str,
) -> tuple[bool, Optional[str], Optional[str]]:
    """
    Validate a Notion API key and get workspace name.

    Issue #527: ALPHA-SETUP-NOTION

    Uses the official Notion SDK to test the API key by calling users.me()
    endpoint, which returns workspace information for bot integrations.

    Args:
        api_key: Notion API key (starts with 'secret_' or 'ntn_')

    Returns:
        Tuple of (is_valid, workspace_name, error_message)
        - is_valid: True if key is valid and has workspace access
        - workspace_name: Name of the workspace, or None if invalid
        - error_message: Human-friendly error message, or None if valid
    """
    try:
        from notion_client import Client
        from notion_client.client import ClientOptions
        from notion_client.errors import APIResponseError

        # Create a temporary client with the provided key
        options = ClientOptions(auth=api_key, notion_version="2025-09-03")
        client = Client(options=options)

        # Test the key by calling users.me()
        user_info = client.users.me()

        # Extract workspace name from bot info
        workspace_name = user_info.get("bot", {}).get("workspace", {}).get("name")

        # If no workspace name in bot info, fall back to user name
        if not workspace_name:
            workspace_name = user_info.get("name", "Unknown Workspace")

        logger.info(
            "notion_key_validated",
            workspace=workspace_name,
            user_type=user_info.get("type", "unknown"),
        )

        return True, workspace_name, None

    except APIResponseError as e:
        # Issue #527: Provide specific error guidance based on error code
        error_code = getattr(e, "code", "unknown")
        error_str = str(e).lower()
        logger.warning("notion_key_invalid", error=str(e), error_code=error_code)

        # Map Notion API errors to user-friendly messages
        code_value = getattr(error_code, "value", error_code)
        http_status = getattr(e, "status", None)
        if code_value in _NOTION_SERVER_ERROR_CODES or (
            isinstance(http_status, int) and http_status >= 500
        ):
            # #2151: a Notion 5xx is a check that couldn't run, not a rejected key.
            error_msg = NOTION_CHECK_FAILED_MESSAGE
        elif "unauthorized" in error_str or error_code == "unauthorized":
            error_msg = "Invalid API key. Check your key at notion.so/my-integrations"
        elif "forbidden" in error_str or error_code == "restricted_resource":
            error_msg = "Key lacks required permissions. Ensure integration has workspace access"
        elif "rate_limited" in error_str:
            error_msg = "Rate limited by Notion. Wait a moment and try again"
        else:
            error_msg = "Invalid API key or insufficient permissions"

        return False, None, error_msg
    except ImportError:
        logger.error("notion_sdk_not_installed")
        return False, None, "Notion SDK not installed. Contact support."
    except Exception as e:
        error_str = str(e).lower()
        logger.error("notion_key_validation_error", error=str(e), exc_info=True)

        # Network errors
        if "connect" in error_str or "network" in error_str or "timeout" in error_str:
            return False, None, "Could not reach Notion API. Check your internet connection"

        return False, None, "Validation failed. Please try again"


# #2117: the wizard's words when a provider key passes its check.
KEY_ACCEPTED_MESSAGE = "Key accepted."

# #2151 route group 3: GitHub refused the token (401/403). Wording pending CXO.
GITHUB_TOKEN_REFUSED_MESSAGE = "GitHub didn't accept that token. Check it and try again."


async def _github_token_status(token: str) -> Optional[int]:
    """GitHub's HTTP status for ``GET /user`` with this token; None when the call
    didn't complete (network, timeout). Never logs or returns the token."""
    import aiohttp

    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github+json",
                },
            ) as response:
                return response.status
    except Exception as e:
        logger.warning("github_token_check_did_not_run", error_type=type(e).__name__)
        return None


INVITE_REFUSED_MESSAGE = (
    "That code isn't valid or has already been used. Check it and try again, "
    "or ask whoever sent it for a new one."
)


class InviteCheckRequest(BaseModel):
    """#2088: the hosted wizard's step 1 asks for the code first."""

    invite_token: str = Field(min_length=1, description="Alpha invite token, checked, not spent")


class InviteCheckResponse(BaseModel):
    valid: bool
    message: Optional[str] = None


@router.post("/check-invite", response_model=InviteCheckResponse)
async def check_invite(req: InviteCheckRequest) -> InviteCheckResponse:
    """#2088 (CXO 2026-10-19): check an invite code WITHOUT spending it, so the
    hosted wizard can ask for it first. The code is spent only inside
    create_user's transaction (#1344). A READ, so not behind the #1504 lockout
    (the check-system reasoning, #1875). The token itself is never logged.
    """
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            valid = await check_invite_token(session, req.invite_token)
    except Exception as e:
        logger.error("invite_check_failed", error_type=type(e).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The invite check couldn't run. Try again in a moment.",
        )
    logger.info("invite_check", valid=valid)
    return InviteCheckResponse(valid=valid, message=None if valid else INVITE_REFUSED_MESSAGE)


# #2125 (Web on staging, 2026-10-21): a server whose encryption key is unusable told the
# person their API key failed validation and printed the parameter. Say whose fault it is,
# and never render an exception to the page; the server log carries the cause.
# CXO (2026-10-22 07:02): "has been told" would claim an action; this route only writes a
# log line, so the sentence asks the person to tell us instead.
SERVER_CANNOT_STORE_KEYS_MESSAGE = (
    "The server can't store keys right now, so no key can be saved. Your key isn't the "
    "problem. This is on our side, so please tell us."
)
# CXO (2026-10-22): the display name, not the provider id, in lines a person reads.
PROVIDER_DISPLAY_NAMES = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "gemini": "Gemini",
    "notion": "Notion",
    "github": "GitHub",
}


def provider_display_name(provider: str) -> str:
    return PROVIDER_DISPLAY_NAMES.get(provider, provider)


KEY_CHECK_COULD_NOT_RUN_MESSAGE = KEY_CHECK_UNAVAILABLE_MESSAGE  # one sentence, one source
# #2125 (Arch, CXO): no page prints str(e). One tail, one line per route; the cause is logged.
_TRY_AGAIN = "Try again in a moment; if it keeps failing, tell us."
SYSTEM_CHECK_COULD_NOT_RUN_MESSAGE = f"The system check couldn't run just now. {_TRY_AGAIN}"
CREDENTIALS_COULD_NOT_BE_SAVED_MESSAGE = f"The credentials couldn't be saved just now. {_TRY_AGAIN}"
ACCOUNT_COULD_NOT_BE_CREATED_MESSAGE = f"The account couldn't be created just now. {_TRY_AGAIN}"
PROJECT_COULD_NOT_BE_CREATED_MESSAGE = f"The project couldn't be created just now. {_TRY_AGAIN}"
SLACK_CONNECT_COULD_NOT_START_MESSAGE = (
    f"The Slack connection couldn't start just now. {_TRY_AGAIN}"
)
CALENDAR_CONNECT_COULD_NOT_START_MESSAGE = (
    f"The Google Calendar connection couldn't start just now. {_TRY_AGAIN}"
)
SETUP_COULD_NOT_FINISH_MESSAGE = (
    "Setup couldn't finish just now. Try again in a moment; if it keeps failing, tell us."
)


@router.post("/validate-key", response_model=ApiKeyValidateResponse)
async def validate_api_key(req: ApiKeyValidateRequest):
    """
    Validate an API key with the provider.

    Uses UserAPIKeyService to validate keys against provider APIs:
    - OpenAI / Anthropic: a minimal request with the key (the reply names no model, #2117)
    - GitHub: GET /user with the token (#2151: it was skipped and answered valid=True)
    - Notion: Tests workspace access with users.me() (#527)

    Args:
        req: ApiKeyValidateRequest with provider and api_key

    Returns:
        ApiKeyValidateResponse with validation result
    """
    # #2237: Notion is outside the offered set; refuse before any call to Notion.
    if req.provider == "notion":
        refuse_unless_offered("notion")
    try:
        if req.provider == "github":
            # #2151 route group 3: a real check (it answered valid=True and "saved" with
            # nothing checked and nothing saved). 401/403 is GitHub's refusal; anything
            # else is a check that couldn't run (#2125's KeyCheckUnavailable path).
            http_status = await _github_token_status(req.api_key)
            if http_status == 200:
                return ApiKeyValidateResponse(
                    provider=req.provider, valid=True, message=KEY_ACCEPTED_MESSAGE
                )
            if http_status in (401, 403):
                return ApiKeyValidateResponse(
                    provider=req.provider, valid=False, message=GITHUB_TOKEN_REFUSED_MESSAGE
                )
            raise KeyCheckUnavailable("github token check did not run")

        # Notion validation uses dedicated helper (#527)
        if req.provider == "notion":
            is_valid, workspace_name, error_msg = await validate_notion_key_and_get_workspace(
                req.api_key
            )
            if is_valid:
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=True,
                    message=f"Valid (Connected to '{workspace_name}')",
                    workspace_name=workspace_name,
                )
            else:
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=False,
                    message=error_msg or "Invalid API key or insufficient permissions",
                )

        # For OpenAI and Anthropic, use UserAPIKeyService validation
        service = UserAPIKeyService()

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            try:
                # Issue #485: Validate the key WITHOUT storing (store=False)
                # No temp_user_id needed - validation-only mode doesn't touch DB
                await service.store_user_key(
                    user_id="validation-only",  # Placeholder, not used when store=False
                    provider=req.provider,
                    api_key=req.api_key,
                    session=session,
                    validate=True,
                    store=False,  # Issue #485: Don't create DB records during validation
                )

                # Validation succeeded. #2117 (CXO): the old line named a model
                # that was a constant here, not anything the check reached; say
                # only what was checked.
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=True,
                    message=KEY_ACCEPTED_MESSAGE,
                )

            except KeyStoreConfigError:
                # #2125 (Arch): a ValueError by type; must reach the server-fault branch
                # below, never this one, even if a later change builds an encryptor here.
                raise
            except KeyCheckUnavailable:
                raise
            except ValueError as e:
                # The provider's own refusal of the key: the person reads its reason
                return ApiKeyValidateResponse(
                    provider=req.provider,
                    valid=False,
                    message=str(e),
                )

    except KeyCheckUnavailable:
        # #2125: the check did not run (timeout, network, a fault of ours); the key is unjudged
        logger.warning("key_check_unavailable_at_route", provider=req.provider)
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=False,
            message=KEY_CHECK_COULD_NOT_RUN_MESSAGE,
        )
    except KeyStoreConfigError as e:
        # #2125: the instance cannot encrypt (master key length/encoding, both modes set).
        logger.error("key_store_unavailable", provider=req.provider, error_type=type(e).__name__)
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=False,
            message=SERVER_CANNOT_STORE_KEYS_MESSAGE,
        )
    except Exception as e:
        logger.error(
            "api_key_validation_failed", provider=req.provider, error=str(e), exc_info=True
        )
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=False,
            message=KEY_CHECK_COULD_NOT_RUN_MESSAGE,
        )


# #2151 route group 3: what the wizard hears on a hosted deploy, where no keychain is the
# visitor's own. Wording pending CXO.
HOSTED_NO_KEYCHAIN_MESSAGE = (
    "Paste your key here. This hosted instance doesn't read keys from a keychain."
)


@router.get("/check-keychain/{provider}", response_model=KeychainCheckResponse)
async def check_keychain(provider: str):
    """
    Check if an API key exists in the system keychain.

    This allows the UI to show "Use from Keychain" button only when
    a key is available. Accessing the actual key requires explicit
    user action (triggers OS keychain permission dialog).

    Args:
        provider: API provider (openai, anthropic, gemini, notion)

    Returns:
        KeychainCheckResponse with exists status
    """
    if provider not in ["openai", "anthropic", "gemini", "notion"]:
        return KeychainCheckResponse(
            provider=provider,
            exists=False,
            message=f"Unknown provider: {provider}",
        )

    from services.infrastructure.deployment import is_hosted_deployment

    if is_hosted_deployment():
        # #2151 route group 3 (Arch 10-24): on a hosted deploy the "keychain" is the
        # operator's store, never this visitor's; the wizard must not offer it.
        return KeychainCheckResponse(
            provider=provider, exists=False, message=HOSTED_NO_KEYCHAIN_MESSAGE
        )

    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        key = keychain.get_api_key(provider)
        exists = key is not None

        if exists:
            message = f"{provider.capitalize()} key found in keychain"
        else:
            message = f"No {provider} key in keychain"

        return KeychainCheckResponse(
            provider=provider,
            exists=exists,
            message=message,
        )

    except Exception as e:
        logger.error("keychain_check_failed", provider=provider, error=str(e), exc_info=True)
        return KeychainCheckResponse(
            provider=provider,
            exists=False,
            message=KEY_CHECK_COULD_NOT_RUN_MESSAGE,  # #2125: no exception text on the page
        )


@router.post("/use-keychain", response_model=KeychainUseResponse)
async def use_keychain(req: KeychainUseRequest):
    """
    Retrieve API key from keychain and validate it.

    This endpoint triggers the OS keychain permission dialog,
    requiring explicit user consent. If the key is found, we trust it
    since it was previously validated when stored.

    Note: We skip re-validation here to avoid event loop mismatch issues
    with the database session. Keys in keychain were validated when stored.

    Args:
        req: KeychainUseRequest with provider

    Returns:
        KeychainUseResponse with validation result
    """
    from services.infrastructure.deployment import is_hosted_deployment

    if is_hosted_deployment():
        # #2151 route group 3: never hand a visitor the operator's stored key.
        return KeychainUseResponse(
            provider=req.provider, success=False, valid=False, message=HOSTED_NO_KEYCHAIN_MESSAGE
        )

    try:
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        api_key = keychain.get_api_key(req.provider)

        if not api_key:
            return KeychainUseResponse(
                provider=req.provider,
                success=False,
                valid=False,
                message=f"No {req.provider} key found in keychain",
            )

        # Key exists in keychain - trust it was validated when stored
        # We skip re-validation to avoid event loop issues with database sessions.
        # #2117's rule (CXO): say only what was checked. Nothing here reached a model;
        # the old line named one from a constant table.
        return KeychainUseResponse(
            provider=req.provider,
            success=True,
            valid=True,
            message=f"Using the {provider_display_name(req.provider)} key from your keychain.",
        )

    except Exception as e:
        logger.error("keychain_use_failed", provider=req.provider, error=str(e), exc_info=True)
        return KeychainUseResponse(
            provider=req.provider,
            success=False,
            valid=False,
            message=KEY_CHECK_COULD_NOT_RUN_MESSAGE,
        )


# ============================================================================
# Integration Credentials (Setup Flow - No Auth Required)
# Issue #772: These endpoints mirror settings_integrations.py but work during
# setup when user isn't authenticated yet.
# ============================================================================


class SlackCredentialsRequest(BaseModel):
    """Request body for Slack app credentials during setup."""

    client_id: str
    client_secret: str


class SlackCredentialsResponse(BaseModel):
    """Response for Slack credentials save."""

    success: bool
    message: str


@router.post(
    "/slack-credentials",
    response_model=SlackCredentialsResponse,
    dependencies=[Depends(require_setup_incomplete)],
)
async def save_slack_credentials_setup(credentials: SlackCredentialsRequest):
    """
    Save Slack app credentials during setup wizard.

    This endpoint does NOT require authentication, allowing users to configure
    Slack integration before their account is fully created.

    Issue #772: Mirrors /api/v1/settings/integrations/slack/app-credentials
    but works during setup flow.

    Security Note: Credentials are stored in OS keychain, never logged.
    """
    refuse_unless_offered("slack")  # #2237
    from services.integrations.integration_config_service import IntegrationConfigService

    try:
        # Validate both fields are non-empty
        if not credentials.client_id.strip():
            return SlackCredentialsResponse(
                success=False,
                message="Client ID is required and cannot be empty",
            )
        if not credentials.client_secret.strip():
            return SlackCredentialsResponse(
                success=False,
                message="Client Secret is required and cannot be empty",
            )

        # Store via IntegrationConfigService
        config_service = IntegrationConfigService()
        config_service.store_slack_credentials(
            credentials.client_id.strip(), credentials.client_secret.strip()
        )

        logger.info("slack_credentials_saved_during_setup")

        return SlackCredentialsResponse(
            success=True,
            message="Slack app credentials saved securely",
        )

    except Exception as e:
        logger.error("slack_credentials_setup_error", error=str(e), exc_info=True)
        return SlackCredentialsResponse(
            success=False,
            message=CREDENTIALS_COULD_NOT_BE_SAVED_MESSAGE,
        )


def _sign_in_new_user(request: Request, response: Response, user: User) -> None:
    """#2078: set the session cookies for the account create-user just made.
    Same tokens and cookie flags as login (one helper, services/auth/session_cookies)."""
    from services.auth.container import AuthContainer  # noqa: PLC0415

    jwt_service = AuthContainer.get_jwt_service()
    user_uuid = uuid.UUID(str(user.id))
    email = str(user.email)
    access = jwt_service.generate_access_token(
        user_id=user_uuid,
        user_email=email,
        scopes=["user"],
        username=str(user.username),
    )
    refresh = jwt_service.generate_refresh_token(
        user_id=user_uuid,
        user_email=email,
        session_id=None,
        workspace_id=None,
    )
    set_session_cookies(response, request, access_token=access, refresh_token=refresh)
    logger.info("setup_user_signed_in", user_id=str(user_uuid), username=str(user.username))


@router.post("/create-user", response_model=CreateUserResponse)
async def create_user_route(
    req: CreateUserRequest, request: Request, response: Response
) -> "CreateUserResponse":
    """The HTTP entry: FastAPI injects the request and response so the new
    account can be signed in (#2078). The logic lives in ``create_user``, which
    direct callers (tests, scripts) invoke without a request."""
    return await create_user(req, request, response)


async def create_user(
    req: CreateUserRequest,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
) -> "CreateUserResponse":
    """
    Create a new user account with secure password.

    Validates username uniqueness and a valid, unused invite token (#1344),
    hashes password with bcrypt, and creates user in database with alpha flag.

    #2078: once the row is committed, the new account is SIGNED IN here (the
    same cookie pair login sets), so the wizard's next steps (``/complete``,
    ``/projects``) carry a principal. The atomically consumed invite is what
    authorized the account; the session belongs to that account only, and is
    exactly what the person would get by signing in with the password they
    just typed. Direct (non-HTTP) callers get no cookies and no session.

    Args:
        req: CreateUserRequest with username, email, password, invite_token

    Returns:
        CreateUserResponse with user_id and success status

    Raises:
        HTTPException 400: If username already exists, or invite_token is invalid/already used
        HTTPException 500: If user creation fails
    """
    try:
        # Hash password with bcrypt
        password_service = PasswordService()
        password_hash = password_service.hash_password(req.password)

        # Create user account
        user = User(
            id=uuid.uuid4(),
            username=req.username,
            email=req.email,
            password_hash=password_hash,
            role="user",
            is_active=True,
            is_verified=True,
            is_alpha=True,  # Alpha tester flag
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(user)
            # #1344: atomic validate-and-consume in the SAME transaction as the user
            # INSERT (not a separate call) — burn-and-create commit or roll back
            # together, so a token can never be spent without an account, and two
            # concurrent registrations can't both consume the same token (Arch's
            # atomicity requirement — see services/auth/invite_token_service.py).
            consumed = await consume_invite_token(session, req.invite_token, user.id)
            if not consumed:
                logger.warning("user_creation_failed_invalid_invite_token", username=req.username)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or already-used invite token",
                )
            await session.commit()

        logger.info("user_created", user_id=str(user.id), username=user.username)

        if request is not None and response is not None:
            _sign_in_new_user(request, response, user)

        return CreateUserResponse(
            success=True,
            user_id=str(user.id),
            message=f"Account created: {user.username}",
        )

    except HTTPException:
        raise  # #1344: pass the invite-token 400 through unchanged, don't remap below
    except Exception as e:
        error_str = str(e).lower()
        if "duplicate" in error_str or "unique" in error_str:
            # #1348: email is unique too — say which field collided instead of
            # blaming the username for an email conflict.
            field = "Email" if "email" in error_str else "Username"
            value = req.email if field == "Email" else req.username
            logger.warning("user_creation_failed_duplicate", username=req.username, field=field)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field} '{value}' already exists",
            )
        # Provide helpful error messages for common database issues
        elif "relation" in error_str and "does not exist" in error_str:
            logger.error("user_creation_failed_missing_table", username=req.username, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Database tables are missing. "
                    "Run 'python -m alembic upgrade head' to create them, "
                    "then try again."
                ),
            )
        elif "connection" in error_str or "connect" in error_str:
            logger.error("user_creation_failed_db_connection", username=req.username, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "Cannot connect to database. "
                    "Ensure Docker is running: 'docker compose up -d', "
                    "then try again."
                ),
            )
        else:
            logger.error("user_creation_failed", username=req.username, error=str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ACCOUNT_COULD_NOT_BE_CREATED_MESSAGE,
            )


@router.post("/complete", response_model=SetupCompleteResponse)
async def complete_setup(
    req: SetupCompleteRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Finalize setup by storing API keys and marking user as setup complete.

    #2078: the principal is the signed-in user (create-user signs the new
    account in); every write below is for that user only. The #1504 lockout
    came off this route because the principal check is what stops F1 now;
    before, every invited tester on an initialized instance was refused here
    and the wizard ended in "Setup Failed" with the account already created.

    This endpoint:
    1. Stores provided API keys (OpenAI, Anthropic, Notion) in keychain
    2. Updates user.setup_complete flag to true
    3. Generates CLI auto-auth token

    Args:
        req: SetupCompleteRequest with user_id and optional API keys

    Returns:
        SetupCompleteResponse with success status and redirect URL

    Issue #527: Added Notion key storage support
    """
    user_id = _setup_principal(current_user, req.user_id)
    try:
        # Store API keys if provided
        service = UserAPIKeyService()

        # Use fresh session to avoid event loop mismatch (#442)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Store OpenAI key
            if req.openai_key:
                try:
                    await service.store_user_key(
                        user_id=user_id,
                        provider="openai",
                        api_key=req.openai_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning("openai_key_storage_failed", user_id=user_id, error=str(e))

            # Store Anthropic key
            if req.anthropic_key:
                try:
                    await service.store_user_key(
                        user_id=user_id,
                        provider="anthropic",
                        api_key=req.anthropic_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning("anthropic_key_storage_failed", user_id=user_id, error=str(e))

            # Store Notion key (Issue #527: ALPHA-SETUP-NOTION)
            # #2237: Notion is outside the offered set; a key sent anyway is not stored.
            if req.notion_key and connector_offered("notion"):
                try:
                    await service.store_user_key(
                        user_id=user_id,
                        provider="notion",
                        api_key=req.notion_key,
                        session=session,
                        validate=False,  # Already validated in previous step
                    )
                except Exception as e:
                    logger.warning("notion_key_storage_failed", user_id=user_id, error=str(e))

            # #1810: Issue #724 used to ALSO store GLOBAL, unprefixed copies of
            # the LLM keys here ("openai_api_key" / "anthropic_api_key", no
            # username) "so LLMClient can find keys during server startup when
            # no user context exists." That global slot is exactly what
            # LLMConfigService.get_api_key()/LLMClient._init_clients() resolve
            # as "the server's key" — every user completing setup silently
            # overwrote whichever key the operator (or an earlier user) had in
            # place, last-writer-wins, no audit, no confirmation. PM ruling
            # 2026-09-14 (decisions.log): "the server key is not a real
            # concept and will not be supported in any sense" — #724's stated
            # startup consumer does not survive tracing (see #1812). The
            # per-user write below (unchanged) is the only credential setup
            # completion ever needs to create.
            from services.infrastructure.keychain_service import KeychainService

            keychain = KeychainService()

            # Issue #946: Store the user's chosen LLM provider as the system default
            # AND the authorized providers list (consent boundary).
            # This ensures the runtime uses ONLY the provider(s) the user authorized,
            # not stale keys from the keychain or env vars from previous installs.
            authorized_providers = []
            if req.openai_key:
                authorized_providers.append("openai")
            if req.anthropic_key:
                authorized_providers.append("anthropic")
            if req.default_llm_provider and req.default_llm_provider not in authorized_providers:
                authorized_providers.append(req.default_llm_provider)

            if authorized_providers:
                try:
                    # #1415: selection state is PER-USER. The old global write
                    # here is the exact mechanism of the 2026-07-16 incident —
                    # one tester's setup pinned the provider (and consent list)
                    # for the whole instance. Legacy global slots remain honored
                    # read-side as the server-level fallback.
                    keychain.store_api_key(
                        "authorized_llm_providers",
                        ",".join(authorized_providers),
                        username=user_id,
                    )
                    logger.info(
                        "authorized_llm_providers_stored",
                        providers=authorized_providers,
                        user_scoped=True,
                    )
                except Exception as e:
                    logger.warning("authorized_llm_providers_storage_failed", error=str(e))

            if req.default_llm_provider:
                try:
                    # #1415: per-user (see consent-list note above).
                    keychain.store_api_key(
                        "default_llm_provider",
                        req.default_llm_provider,
                        username=user_id,
                    )
                    logger.info(
                        "default_llm_provider_stored",
                        provider=req.default_llm_provider,
                        user_scoped=True,
                    )
                except Exception as e:
                    logger.warning("default_llm_provider_storage_failed", error=str(e))

            # Mark setup as complete (Issue #389)
            # Issue #771: Use utc_now() - DB columns now use timestamptz
            from services.utils.datetime_utils import utc_now

            await session.execute(
                text(
                    "UPDATE users SET setup_complete = true, "
                    "setup_completed_at = :now WHERE id = :user_id"
                ),
                {"user_id": user_id, "now": utc_now()},
            )
            await session.commit()

        # Generate CLI token (non-blocking, best effort)
        try:
            from services.auth.jwt_service import JWTService
            from services.infrastructure.keychain_service import KeychainService

            jwt_service = JWTService()
            keychain = KeychainService()

            # Get user email for CLI token
            # Use fresh session to avoid event loop mismatch (#442)
            async with AsyncSessionFactory.session_scope_fresh() as session:
                result = await session.execute(select(User).where(User.id == uuid.UUID(user_id)))
                user = result.scalar_one_or_none()
                user_email = user.email if user else ""

            cli_token = jwt_service.generate_cli_token(user_id=user_id, user_email=user_email)
            keychain.store_cli_token(user_id, cli_token)
            logger.info("cli_auth_configured", user_id=user_id)
        except Exception as e:
            logger.warning("cli_auth_setup_failed", user_id=user_id, error=str(e))

        logger.info("setup_completed", user_id=user_id)

        return SetupCompleteResponse(
            success=True,
            message="Setup complete! You're signed in.",
            redirect_url="/",  # #2078: the session was issued at create-user
        )

    except HTTPException:
        raise
    except KeyStoreConfigError as e:
        # #2125: the instance cannot encrypt; say so, never the parameter
        logger.error("key_store_unavailable", user_id=user_id, error_type=type(e).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=SERVER_CANNOT_STORE_KEYS_MESSAGE,
        )
    except Exception as e:
        logger.error("setup_completion_failed", user_id=user_id, error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SETUP_COULD_NOT_FINISH_MESSAGE,
        )


# ============================================================================
# Project Setup Endpoints (Issue #860: Setup Wizard Project-Repo Linking)
# ============================================================================


class SetupProjectRequest(BaseModel):
    """Request model for creating a project during setup."""

    user_id: Optional[str] = Field(
        default=None, description="Must match the signed-in user, if sent (#2078)"
    )
    project_name: str = Field(description="Project name")
    project_description: str = Field(default="", description="Optional project description")
    github_repo: Optional[str] = Field(
        default=None, description="GitHub repo in owner/repo format (optional)"
    )


class SetupProjectResponse(BaseModel):
    """Response model for project creation during setup."""

    success: bool
    project_id: str = ""
    message: str = ""


@router.post("/projects", response_model=SetupProjectResponse)
async def create_setup_project(
    req: SetupProjectRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Create a project (and optionally link a GitHub repo) during setup wizard.

    #2078: the owner is the signed-in user (create-user signs the new account
    in); a body user_id must match it. The #1504 lockout came off for the same
    reason as ``/complete``.

    Issue #860: Setup wizard project-repo linking step.
    Issue #866 introduced a dual-write (Repository entity + a "legacy" GitHub
    ProjectIntegration mirror). #1945 retired the mirror (Arch GO 2026-10-05):
    nothing read it — the Config panel just showed the same repo twice — and
    unlink now deletes any mirror rows that already exist.
    """
    from services.database.repositories import ProjectRepository, RepositoryRepository
    from services.domain import models as domain

    user_id = _setup_principal(current_user, req.user_id)
    try:
        if not req.project_name or not req.project_name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Project name is required",
            )

        async with AsyncSessionFactory.session_scope_fresh() as session:
            project_repo = ProjectRepository(session)

            # Create the project
            created_project = await project_repo.create(
                name=req.project_name.strip(),
                description=req.project_description,
                owner_id=user_id,
            )

            project_id = created_project.id

            # Optionally link a GitHub repo
            if req.github_repo and req.github_repo.strip():
                repo_name = req.github_repo.strip()
                # Basic format validation (owner/repo)
                if "/" not in repo_name:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="GitHub repo must be in owner/repo format",
                    )

                # Issue #867: Soft-validate via GitHub API
                from services.infrastructure.github_repo_validator import (
                    apply_validation_metadata,
                    validate_github_repo_for_account,
                )

                validation = await validate_github_repo_for_account(repo_name, user_id)
                if validation.validated and not validation.exists:
                    logger.warning(
                        "setup_repo_validation_warning",
                        full_name=repo_name,
                        error=validation.error,
                    )

                # Create Repository entity (#866)
                repo_repo = RepositoryRepository(session)
                repo_domain = domain.Repository(
                    owner_id=user_id,
                    provider="github",
                    full_name=repo_name,
                    display_name=repo_name.split("/")[-1],
                    url=f"https://github.com/{repo_name}",
                )
                apply_validation_metadata(repo_domain, validation)
                repo_entity = await repo_repo.create_repository(repo_domain)

                # New: Link to project (#866)
                await repo_repo.link_to_project(
                    repository_id=repo_entity.id,
                    project_id=project_id,
                    linked_by=user_id,
                    is_primary=True,
                )

                # #2205 (Arch 2026-10-29 13:58): choosing a repo here is the user
                # designating it. Nothing has read the project link since the
                # resolver's project path retired (#1315), so the choice goes to the
                # ONE store the resolver reads: the default, source "user", unless the
                # user already designated one. Stored even when GitHub isn't connected
                # yet; a refused write later says GitHub's reason (#2205 part 1).
                from services.connectors.config_service import (
                    SOURCE_USER,
                    ConnectorConfigService,
                )

                configs = ConnectorConfigService(session)
                if await configs.get_default_repo_source(user_id) != SOURCE_USER:
                    await configs.set_default_repo(user_id, repo_name, source=SOURCE_USER)

            await session.commit()

        logger.info(
            "setup_project_created",
            user_id=user_id,
            project_id=project_id,
            has_github_repo=bool(req.github_repo),
        )

        return SetupProjectResponse(
            success=True,
            project_id=project_id,
            message=f"Project '{req.project_name}' created",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "setup_project_creation_failed",
            user_id=user_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=PROJECT_COULD_NOT_BE_CREATED_MESSAGE,
        )


# ============================================================================
# Slack OAuth Endpoints (Issue #528: ALPHA-SETUP-SLACK)
# ============================================================================


@router.get("/slack/oauth/start")
async def start_slack_oauth(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Generate Slack OAuth URL for setup wizard.

    Issue #528: ALPHA-SETUP-SLACK
    Issue #575: Added credential validation before OAuth
    Issue #734: SEC-MULTITENANCY - Requires authentication, embeds user_id in state.

    Returns authorization URL and state token for CSRF protection.
    User redirects to Slack, authorizes, then returns to callback.

    Returns:
        dict with auth_url and state
    """
    refuse_unless_offered("slack")  # #2237
    try:
        from services.integrations.slack.config_service import SlackConfigService
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        # Issue #575: Verify credentials are configured BEFORE starting OAuth
        # #1436 B16: get_config requires the principal — this route has it.
        config_service = SlackConfigService()
        config = config_service.get_config(str(current_user.sub))

        if not config.client_id or not config.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Slack OAuth not configured. Set SLACK_CLIENT_ID and SLACK_CLIENT_SECRET environment variables, or configure in PIPER.user.md.",
            )

        handler = SlackOAuthHandler(config_service=config_service)

        # Use setup-specific redirect URI if available
        # This returns user to wizard instead of general callback
        # 2026-08-07 (route audit, #1324 class): the "" fallback sent Slack an
        # EMPTY redirect_uri when neither env was set — same defect fixed live
        # on the settings routes today. Derive from PIPER_BASE_URL instead.
        _base = os.getenv("PIPER_BASE_URL", "http://localhost:8001").rstrip("/")
        redirect_uri = os.getenv(
            "SLACK_SETUP_REDIRECT_URI",
            os.getenv("SLACK_REDIRECT_URI", f"{_base}/api/v1/setup/slack/oauth/callback"),
        )

        # Issue #734: Pass user_id for multi-tenant state
        # Issue #1109: generate_authorization_url is async (Redis-backed state)
        auth_url, state = await handler.generate_authorization_url(
            user_id=current_user.sub, redirect_uri=redirect_uri if redirect_uri else None
        )

        logger.info("slack_oauth_started", user_id=current_user.sub, state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("slack_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=SLACK_CONNECT_COULD_NOT_START_MESSAGE,
        )


@router.get("/slack/oauth/callback")
async def handle_slack_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Slack OAuth callback for setup wizard.

    Issue #528: ALPHA-SETUP-SLACK
    Issue #734: SEC-MULTITENANCY - user_id extracted from state and used
    for per-user token storage in SlackOAuthHandler.

    Exchanges authorization code for tokens and redirects back to
    setup wizard with success/error status in query params.

    Args:
        code: Authorization code from Slack
        state: State token for CSRF verification (includes user_id)
        error: Error from Slack (if authorization denied)

    Returns:
        RedirectResponse to setup wizard with status
    """
    refuse_unless_offered("slack")  # #2237
    from urllib.parse import quote

    from starlette.responses import RedirectResponse

    # Handle OAuth error (user denied, etc.)
    if error:
        logger.warning("slack_oauth_denied", error=error)
        return RedirectResponse(url=f"/setup?slack_error={error}#step-2", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning("slack_oauth_missing_params", has_code=bool(code), has_state=bool(state))
        return RedirectResponse(url="/setup?slack_error=missing_params#step-2", status_code=302)

    try:
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        handler = SlackOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Issue #734: user_id is already extracted and used for storage in handler
        user_id = result.get("user_id")

        # Extract workspace name from result
        workspace_name = result.get("workspace", {}).get("workspace_name", "Workspace")
        workspace_name_encoded = quote(workspace_name)

        logger.info("slack_oauth_success", user_id=user_id, workspace=workspace_name)

        # Redirect back to setup wizard with success
        return RedirectResponse(
            url=f"/setup?slack_success=true&slack_workspace={workspace_name_encoded}#step-2",
            status_code=302,
        )

    except ValueError as e:
        # Invalid state or other validation error
        logger.warning("slack_oauth_validation_error", error=str(e))
        return RedirectResponse(url="/setup?slack_error=callback_failed#step-2", status_code=302)
    except Exception as e:
        logger.error("slack_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(url="/setup?slack_error=callback_failed#step-2", status_code=302)


@router.get("/slack/status")
async def get_slack_status(request: Request):
    """
    Get Slack configuration status for setup wizard.

    Checks if Slack bot token exists and returns connection status.

    Issue #528: ALPHA-SETUP-SLACK
    #1436 B16: get_config requires a principal — optional-auth via
    request.state (the calendar-status pattern, #1434): the acting user's
    scope when authenticated, the "system" marker otherwise.

    Returns:
        dict with configured status and optional workspace info
    """
    try:
        from services.integrations.slack.config_service import SlackConfigService

        user_id = getattr(request.state, "user_id", None)
        if not user_id:
            # #2151 route group 3: with no signed-in user there is no one's Slack to read;
            # the "system" principal's token is never this visitor's connection.
            return {"configured": False, "message": "Not connected"}
        config_service = SlackConfigService()
        slack_config = config_service.get_config(str(user_id))

        if slack_config.bot_token:
            return {
                "configured": True,
                "message": "Slack connected",
            }
        else:
            return {
                "configured": False,
                "message": "Not connected",
            }

    except Exception as e:
        logger.error("slack_status_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "message": "Status check failed",
        }


# ============================================================================
# Google Calendar OAuth Endpoints (Issue #529: ALPHA-SETUP-CALENDAR)
# ============================================================================


@router.get("/calendar/oauth/start")
async def start_calendar_oauth(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Generate Google Calendar OAuth URL for setup wizard.

    Issue #529: ALPHA-SETUP-CALENDAR
    Issue #734: SEC-MULTITENANCY - Requires authentication, embeds user_id in state.

    Returns authorization URL and state token for CSRF protection.
    User redirects to Google, authorizes, then returns to callback.

    Returns:
        dict with auth_url and state
    """
    try:
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()

        # Verify credentials are configured
        if not handler.client_id or not handler.client_secret:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Google Calendar OAuth not configured. Set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.",
            )

        # Issue #734: Pass user_id for multi-tenant state
        auth_url, state = handler.generate_authorization_url(user_id=current_user.sub)

        logger.info("calendar_oauth_started", user_id=current_user.sub, state=state[:8] + "...")

        return {
            "auth_url": auth_url,
            "state": state,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("calendar_oauth_start_failed", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=CALENDAR_CONNECT_COULD_NOT_START_MESSAGE,
        )


@router.get("/calendar/oauth/callback")
async def handle_calendar_oauth_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    """
    Handle Google Calendar OAuth callback.

    Issue #529: ALPHA-SETUP-CALENDAR
    Issue #734: SEC-MULTITENANCY - Extracts user_id from state for per-user storage.

    Exchanges authorization code for tokens and redirects back to
    setup wizard with success/error status in query params.

    Args:
        code: Authorization code from Google
        state: State token for CSRF verification (includes user_id)
        error: Error from Google (if authorization denied)

    Returns:
        RedirectResponse to setup wizard with status
    """
    from urllib.parse import quote

    from starlette.responses import RedirectResponse

    # Handle OAuth error (user denied, etc.)
    if error:
        logger.warning("calendar_oauth_denied", error=error)
        return RedirectResponse(url=f"/setup?calendar_error={error}#step-2", status_code=302)

    # Handle missing parameters
    if not code or not state:
        logger.warning("calendar_oauth_missing_params", has_code=bool(code), has_state=bool(state))
        return RedirectResponse(url="/setup?calendar_error=missing_params#step-2", status_code=302)

    try:
        from services.infrastructure.keychain_service import KeychainService
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        handler = GoogleCalendarOAuthHandler()
        result = await handler.handle_oauth_callback(code, state)

        # Issue #734: Extract user_id from callback result
        user_id = result.get("user_id")

        # Store refresh token securely with user-scoped key
        tokens = result["tokens"]
        # #2148: a grant without calendar access is not a connection (CXO's words).
        from services.integrations.calendar.oauth_handler import resolve_calendar_grant

        grant = await resolve_calendar_grant(tokens)
        granted = {"granted": True, "not_granted": False}.get(grant)  # None: unconfirmed
        if granted is False:
            logger.warning("calendar_oauth_scope_missing", user_id=result.get("user_id"))
            # Arch 10-23: revoke the scope-less grant (best-effort, logged, never blocks
            # the redirect), so the user's Google account keeps nothing Piper can't revoke.
            if getattr(tokens, "refresh_token", None):
                try:
                    await handler.revoke_token(tokens.refresh_token)
                except Exception as revoke_error:  # silent-ok: best-effort revoke; logged, the honest redirect still follows (#2148)
                    logger.warning("calendar_scope_missing_revoke_failed", error=str(revoke_error))
            return RedirectResponse(
                url="/setup?calendar_error=scope_missing#step-2", status_code=302
            )
        if tokens.refresh_token:
            keychain = KeychainService()
            # Issue #734/#917: Use ONLY user-scoped key for per-user storage.
            # Never store to the global "google_calendar" key — that causes
            # cross-user credential leakage (see #917).
            if not user_id:
                logger.error(
                    "calendar_oauth_no_user_id",
                    reason="Cannot store refresh token without user_id — "
                    "would create global key causing credential leakage",
                )
                return RedirectResponse(
                    url="/setup?calendar_error=missing_user_id#step-2",
                    status_code=302,
                )
            key_name = f"google_calendar_{user_id}"
            keychain.store_api_key(key_name, tokens.refresh_token)
            logger.info("calendar_refresh_token_stored", user_id=user_id)

        # Get user email for display
        user_email = result["user"].get("email", "Calendar")
        email_encoded = quote(user_email)

        logger.info("calendar_oauth_success", user_id=user_id, email=user_email)

        if granted is None:
            # #2148: the granted scopes couldn't be read; never a success state.
            return RedirectResponse(url="/setup?calendar_unconfirmed=true#step-2", status_code=302)
        # Redirect back to setup wizard with success
        return RedirectResponse(
            url=f"/setup?calendar_success=true&calendar_email={email_encoded}#step-2",
            status_code=302,
        )

    except ValueError as e:
        # Invalid state or other validation error
        logger.warning("calendar_oauth_validation_error", error=str(e))
        return RedirectResponse(url="/setup?calendar_error=callback_failed#step-2", status_code=302)
    except Exception as e:
        logger.error("calendar_oauth_callback_error", error=str(e), exc_info=True)
        return RedirectResponse(url="/setup?calendar_error=callback_failed#step-2", status_code=302)


@router.get("/calendar/status")
async def get_calendar_status(request: Request):
    """
    Get Calendar configuration status for setup wizard.

    Checks if refresh token exists in keychain.

    Issue #529: ALPHA-SETUP-CALENDAR
    Issue #839: Use user-scoped keychain key

    Returns:
        dict with configured status
    """
    try:
        from services.infrastructure.keychain_service import KeychainService

        # Issue #839: Get user_id for user-scoped keychain lookup
        user_id = None
        try:
            from services.auth.jwt_service import JWTService

            token = request.cookies.get("auth_token")
            if token:
                jwt_service = JWTService()
                # #1434: validate_token is async — un-awaited, the truthy coroutine
                # made claims.sub raise into the except below, so EVERY request
                # silently fell back to the non-scoped key.
                claims = await jwt_service.validate_token(token)
                if claims:
                    user_id = claims.sub
        except Exception:
            pass  # silent-ok: anonymous setup flow legitimately has no token; scoped-vs-global selection is asserted by test_calendar_status_scoped_key_1434

        if not user_id:
            # #2151 route group 3 (the #2127 shape): the unscoped "google_calendar" entry
            # is the host's, never this visitor's calendar. No user, nothing to read.
            return {"configured": False, "message": "Not connected"}

        from services.infrastructure.keychain_service import SecretProvenance

        keychain = KeychainService()
        # #2151 (Arch 10-24 12:32): read with provenance; a store failure is a failed
        # check, never "Not connected".
        read = keychain.read_secret(f"google_calendar_{user_id}")
        if read.provenance is SecretProvenance.STORE_FAILED:
            return {"configured": False, "message": "Status check failed"}
        refresh_token = read.value if read.is_present else None

        if refresh_token:
            return {
                "configured": True,
                "message": "Calendar connected",
            }
        else:
            return {
                "configured": False,
                "message": "Not connected",
            }

    except Exception as e:
        logger.error("calendar_status_check_failed", error=str(e), exc_info=True)
        return {
            "configured": False,
            "message": "Status check failed",
        }
