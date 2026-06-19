"""
Standup API Routes - Multi-Modal Generation REST API

CORE-STAND-MODES-API (Issue #162)
Exposes 5 standup generation modes via REST API:
- standard: Basic standup generation
- issues: Standup with GitHub issues intelligence
- documents: Standup with document suggestions
- calendar: Standup with calendar integration
- trifecta: All intelligence sources combined

Supports 4 output formats:
- json: Raw structured data
- slack: Slack-formatted with emoji and sections
- markdown: Markdown-formatted text
- text: Plain text format

Pattern-034: Error Handling Standards (REST-compliant)
Performance: <2s end-to-end target
"""

import os
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from services.auth import get_current_user
from services.auth.jwt_service import JWTClaims, JWTService
from services.domain.standup_orchestration_service import (
    StandupIntegrationError,
    StandupOrchestrationService,
)
from services.features.morning_standup import StandupResult
from services.utils.standup_formatting import format_standup_metrics
from web.utils.error_responses import internal_error, not_found_error, validation_error

# Create router with prefix and tags for OpenAPI
router = APIRouter(prefix="/api/v1/standup", tags=["standup"])

# Auth enabled by default (Task 3 complete)
# Set REQUIRE_AUTH=false for testing only
# See: dev/active/code-auth-testing-guidance.md
REQUIRE_AUTH = os.getenv("REQUIRE_AUTH", "true").lower() == "true"


# ============================================================================
# Request/Response Models (Pydantic)
# ============================================================================


class StandupRequest(BaseModel):
    """
    Request model for standup generation.

    Attributes:
        mode: Generation mode (standard, issues, documents, calendar, trifecta)
        format: Output format (json, slack, markdown, text)
        user_id: Optional user identifier (resolved from config if not provided)
    """

    mode: Literal["standard", "issues", "documents", "calendar", "trifecta"] = Field(
        default="standard", description="Standup generation mode"
    )
    format: Literal["json", "slack", "markdown", "text"] = Field(
        default="json", description="Output format"
    )
    user_id: Optional[str] = Field(
        default=None, description="User identifier (resolved from config if not provided)"
    )

    class Config:
        json_schema_extra = {
            "example": {"mode": "trifecta", "format": "slack", "user_id": "user-001"}
        }


class StandupData(BaseModel):
    """Structured standup data (for JSON format)"""

    user_id: str
    generated_at: str
    # Per #1034: items are dicts {display, source, lifecycle_state, icon}.
    # `Any` rather than `List[Dict[...]]` for forward compatibility.
    yesterday_accomplishments: List[Any]
    today_priorities: List[Any]
    blockers: List[Any]
    context_source: str
    github_activity: Dict[str, Any]
    time_saved_minutes: int


class StandupResponse(BaseModel):
    """
    Response model for standup generation.

    Attributes:
        success: Whether generation succeeded
        standup: Standup content (format depends on request.format)
        metadata: Generation metadata (mode, format, user_id, timestamp)
        performance_metrics: Performance data (generation_time_ms, formatted metrics)
    """

    success: bool = Field(description="Whether generation succeeded")
    standup: Any = Field(description="Standup content (type varies by format)")
    metadata: Dict[str, Any] = Field(description="Generation metadata")
    performance_metrics: Dict[str, Any] = Field(description="Performance metrics")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "standup": {
                    "user_id": "user-001",
                    "generated_at": "2025-10-19T14:30:00",
                    "yesterday_accomplishments": [
                        {
                            "display": "Completed Phase Z",
                            "source": "commit",
                            "lifecycle_state": None,
                            "icon": "✅",
                        }
                    ],
                    "today_priorities": [
                        {
                            "display": "Start Phase 2 API",
                            "source": "active_repo",
                            "lifecycle_state": None,
                            "icon": "🎯",
                        }
                    ],
                    "blockers": [],
                    "context_source": "persistent",
                    "github_activity": {},
                    "time_saved_minutes": 15,
                },
                "metadata": {
                    "mode": "standard",
                    "format": "json",
                    "user_id": "user-001",
                    "timestamp": "2025-10-19T14:30:00.123456",
                },
                "performance_metrics": {
                    "generation_time_ms": 950,
                    "generation_time_formatted": "0.95s",
                    "generation_time_with_context": "0.95s (lightning fast ⚡)",
                    "efficiency_multiplier": "947x faster",
                    "time_saved_formatted": "15m saved",
                },
            }
        }


class ModesResponse(BaseModel):
    """Response model for modes endpoint"""

    modes: List[str] = Field(description="Supported generation modes")
    descriptions: Dict[str, str] = Field(description="Mode descriptions")

    class Config:
        json_schema_extra = {
            "example": {
                "modes": ["standard", "issues", "documents", "calendar", "trifecta"],
                "descriptions": {
                    "standard": "Basic standup generation",
                    "issues": "Standup with GitHub issues intelligence",
                    "documents": "Standup with document suggestions",
                    "calendar": "Standup with calendar integration",
                    "trifecta": "All intelligence sources combined",
                },
            }
        }


class FormatsResponse(BaseModel):
    """Response model for formats endpoint"""

    formats: List[str] = Field(description="Supported output formats")
    descriptions: Dict[str, str] = Field(description="Format descriptions")

    class Config:
        json_schema_extra = {
            "example": {
                "formats": ["json", "slack", "markdown", "text"],
                "descriptions": {
                    "json": "Raw structured data",
                    "slack": "Slack-formatted with emoji and sections",
                    "markdown": "Markdown-formatted text",
                    "text": "Plain text format",
                },
            }
        }


class HealthResponse(BaseModel):
    """Response model for health endpoint"""

    status: str = Field(description="Health status")
    service: str = Field(description="Service name")
    timestamp: str = Field(description="Check timestamp")
    modes_available: int = Field(description="Number of available modes")
    formats_available: int = Field(description="Number of available formats")


# ============================================================================
# Dependency Injection
# ============================================================================


def get_standup_service(request: Request) -> StandupOrchestrationService:
    """
    Dependency injection for StandupOrchestrationService.

    Gets service from ServiceContainer via app.state.
    Uses dependency injection pattern for testability.
    """
    # Check if service container is available
    if not hasattr(request.app.state, "service_container"):
        raise HTTPException(status_code=500, detail="ServiceContainer not initialized")

    container = request.app.state.service_container

    # Get standup orchestration service from container
    # For Phase 2, we'll create the service directly
    # In future, this should come from container.get_service("standup")
    return StandupOrchestrationService()


security = HTTPBearer(auto_error=False)


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[JWTClaims]:
    """
    Authentication dependency with optional bypass for testing.

    When REQUIRE_AUTH=true (DEFAULT/PRODUCTION - Task 3):
    - JWT auth required via Authorization: Bearer header OR auth_token cookie
    - Full JWT validation per ADR-012
    - Returns JWTClaims with user_id, user_email, scopes, etc.
    - Raises 401 Unauthorized if token missing or invalid

    When REQUIRE_AUTH=false (testing only):
    - Auth bypassed, returns None
    - For development/testing purposes only
    - Not for production use

    Note:
        Issue #455: Now checks both Authorization header AND auth_token cookie
        to support web UI authentication with credentials: 'include'.

    See: dev/active/code-auth-testing-guidance.md
    See: ADR-012: Protocol-Ready JWT Authentication
    """
    if not REQUIRE_AUTH:
        # Auth disabled for testing only (not for production)
        return None

    # Extract token from Authorization header or cookie (Issue #455)
    token = None
    if credentials:
        token = credentials.credentials
    else:
        # Try auth_token cookie (for web UI)
        token = request.cookies.get("auth_token")

    if not token:
        # Issue #283: Use APIError so exception handler can convert to friendly message
        from services.api.errors import APIError

        raise APIError(
            status_code=401,
            error_code="AUTHENTICATION_REQUIRED",
            details={"detail": "Authentication required"},
        )

    # Validate token
    from services.api.errors import APIError
    from services.auth.jwt_service import TokenExpired, TokenInvalid, TokenRevoked

    jwt_service = JWTService()

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


# ============================================================================
# Format Converters
# ============================================================================


def format_as_slack(result: StandupResult) -> str:
    """
    Format StandupResult as Slack message with emoji and sections.

    Args:
        result: StandupResult from orchestration service

    Returns:
        Slack-formatted string with emoji and sections
    """
    lines = []

    # Header
    lines.append(f"*Morning Standup for {result.user_id}* :sunrise:")
    lines.append(f"_{result.generated_at.strftime('%Y-%m-%d %H:%M')}_\n")

    # Yesterday
    lines.append("*:calendar: Yesterday's Accomplishments*")
    if result.yesterday_accomplishments:
        for item in result.yesterday_accomplishments:
            lines.append(f"  • {item}")
    else:
        lines.append("  _No accomplishments recorded_")
    lines.append("")

    # Today
    lines.append("*:dart: Today's Priorities*")
    if result.today_priorities:
        for item in result.today_priorities:
            lines.append(f"  • {item}")
    else:
        lines.append("  _No priorities set_")
    lines.append("")

    # Blockers
    lines.append("*:warning: Blockers*")
    if result.blockers:
        for item in result.blockers:
            lines.append(f"  • {item}")
    else:
        lines.append("  _No blockers :white_check_mark:_")
    lines.append("")

    # GitHub Activity (if present)
    if result.github_activity:
        commits = result.github_activity.get("commits", [])
        prs = result.github_activity.get("prs", [])
        if commits or prs:
            lines.append("*:octocat: GitHub Activity*")
            if commits:
                lines.append(f"  • {len(commits)} commits")
            if prs:
                lines.append(f"  • {len(prs)} pull requests")
            lines.append("")

    # Footer with metrics
    time_saved = result.time_saved_minutes
    gen_time_sec = result.generation_time_ms / 1000
    lines.append(
        f"_Generated in {gen_time_sec:.2f}s • Saved {time_saved}m • :robot_face: Piper Morgan_"
    )

    return "\n".join(lines)


def format_as_markdown(result: StandupResult) -> str:
    """
    Format StandupResult as Markdown.

    Args:
        result: StandupResult from orchestration service

    Returns:
        Markdown-formatted string
    """
    lines = []

    # Header
    lines.append(f"# Morning Standup for {result.user_id}")
    lines.append(f"*{result.generated_at.strftime('%Y-%m-%d %H:%M')}*\n")

    # Yesterday
    lines.append("## Yesterday's Accomplishments")
    if result.yesterday_accomplishments:
        for item in result.yesterday_accomplishments:
            lines.append(f"- {item}")
    else:
        lines.append("*No accomplishments recorded*")
    lines.append("")

    # Today
    lines.append("## Today's Priorities")
    if result.today_priorities:
        for item in result.today_priorities:
            lines.append(f"- {item}")
    else:
        lines.append("*No priorities set*")
    lines.append("")

    # Blockers
    lines.append("## Blockers")
    if result.blockers:
        for item in result.blockers:
            lines.append(f"- {item}")
    else:
        lines.append("*No blockers* ✅")
    lines.append("")

    # GitHub Activity (if present)
    if result.github_activity:
        commits = result.github_activity.get("commits", [])
        prs = result.github_activity.get("prs", [])
        if commits or prs:
            lines.append("## GitHub Activity")
            if commits:
                lines.append(f"- {len(commits)} commits")
            if prs:
                lines.append(f"- {len(prs)} pull requests")
            lines.append("")

    # Footer
    time_saved = result.time_saved_minutes
    gen_time_sec = result.generation_time_ms / 1000
    lines.append("---")
    lines.append(f"*Generated in {gen_time_sec:.2f}s | Saved {time_saved}m | Piper Morgan*")

    return "\n".join(lines)


def format_as_text(result: StandupResult) -> str:
    """
    Format StandupResult as plain text.

    Args:
        result: StandupResult from orchestration service

    Returns:
        Plain text formatted string
    """
    lines = []

    # Header
    lines.append(f"Morning Standup for {result.user_id}")
    lines.append(f"{result.generated_at.strftime('%Y-%m-%d %H:%M')}")
    lines.append("=" * 60)
    lines.append("")

    # Yesterday
    lines.append("YESTERDAY'S ACCOMPLISHMENTS:")
    if result.yesterday_accomplishments:
        for item in result.yesterday_accomplishments:
            lines.append(f"  * {item}")
    else:
        lines.append("  (No accomplishments recorded)")
    lines.append("")

    # Today
    lines.append("TODAY'S PRIORITIES:")
    if result.today_priorities:
        for item in result.today_priorities:
            lines.append(f"  * {item}")
    else:
        lines.append("  (No priorities set)")
    lines.append("")

    # Blockers
    lines.append("BLOCKERS:")
    if result.blockers:
        for item in result.blockers:
            lines.append(f"  * {item}")
    else:
        lines.append("  (No blockers)")
    lines.append("")

    # GitHub Activity (if present)
    if result.github_activity:
        commits = result.github_activity.get("commits", [])
        prs = result.github_activity.get("prs", [])
        if commits or prs:
            lines.append("GITHUB ACTIVITY:")
            if commits:
                lines.append(f"  * {len(commits)} commits")
            if prs:
                lines.append(f"  * {len(prs)} pull requests")
            lines.append("")

    # Footer
    time_saved = result.time_saved_minutes
    gen_time_sec = result.generation_time_ms / 1000
    lines.append("=" * 60)
    lines.append(f"Generated in {gen_time_sec:.2f}s | Saved {time_saved}m | Piper Morgan")

    return "\n".join(lines)


def format_standup(result: StandupResult, output_format: str) -> Any:
    """
    Format StandupResult according to requested output format.

    Args:
        result: StandupResult from orchestration service
        output_format: One of: json, slack, markdown, text

    Returns:
        Formatted standup (type depends on format)
    """
    if output_format == "json":
        # Return structured data. Per #1034: each list item is a StandupItem
        # dataclass; serialize via .to_dict() so the API response carries
        # structured per-item data (display + source + lifecycle_state + icon).
        return {
            "user_id": result.user_id,
            "generated_at": result.generated_at.isoformat(),
            "yesterday_accomplishments": [
                item.to_dict() for item in result.yesterday_accomplishments
            ],
            "today_priorities": [item.to_dict() for item in result.today_priorities],
            "blockers": [item.to_dict() for item in result.blockers],
            "context_source": result.context_source,
            "github_activity": result.github_activity,
            "time_saved_minutes": result.time_saved_minutes,
        }
    elif output_format == "slack":
        return format_as_slack(result)
    elif output_format == "markdown":
        return format_as_markdown(result)
    elif output_format == "text":
        return format_as_text(result)
    else:
        # Default to json
        return format_standup(result, "json")


# ============================================================================
# API Endpoints
# ============================================================================


@router.post("/generate", response_model=StandupResponse)
async def generate_standup(
    request: StandupRequest,
    service: StandupOrchestrationService = Depends(get_standup_service),
    current_user: Optional[JWTClaims] = Depends(get_current_user_optional),
):
    """
    Generate standup in specified mode and format.

    This is the main endpoint for standup generation. It supports 5 modes:
    - standard: Basic standup generation
    - issues: GitHub issues intelligence
    - documents: Document suggestions
    - calendar: Calendar integration
    - trifecta: All intelligence sources

    And 4 output formats:
    - json: Raw structured data
    - slack: Slack-formatted message
    - markdown: Markdown text
    - text: Plain text

    Performance target: <2s end-to-end

    Authentication (Task 2 vs Task 3):
    - Task 2 (REQUIRE_AUTH=false): Auth optional, uses request.user_id or "default"
    - Task 3+ (REQUIRE_AUTH=true): JWT required via Authorization: Bearer header

    Args:
        request: StandupRequest with mode, format, and optional user_id
        service: Injected StandupOrchestrationService
        current_user: Optional JWT claims (None if auth disabled, JWTClaims if enabled)

    Returns:
        StandupResponse with generated standup and metadata

    Raises:
        401: Unauthorized (missing or invalid JWT token when REQUIRE_AUTH=true)
        422: Validation error (invalid mode/format)
        500: Internal error (service failure)
    """
    start_time = time.time()

    try:
        # Map mode to workflow_type
        # Request uses: standard, issues, documents, calendar, trifecta
        # Service uses: standard, with_issues, with_documents, with_calendar, trifecta
        mode_mapping = {
            "standard": "standard",
            "issues": "with_issues",
            "documents": "with_documents",
            "calendar": "with_calendar",
            "trifecta": "trifecta",
        }

        workflow_type = mode_mapping.get(request.mode)
        if not workflow_type:
            return validation_error(
                f"Invalid mode: {request.mode}",
                {"field": "mode", "valid_values": list(mode_mapping.keys())},
            )

        # Validate format
        valid_formats = ["json", "slack", "markdown", "text"]
        if request.format not in valid_formats:
            return validation_error(
                f"Invalid format: {request.format}",
                {"field": "format", "valid_values": valid_formats},
            )

        # Resolve user_id based on auth status
        # Priority: request > JWT claims (if auth enabled) > None (service will use default)
        if current_user:
            # Auth enabled - use JWT claims
            user_id = request.user_id or current_user.user_id
        else:
            # Auth disabled (Task 2 testing) - use request or None (service default)
            user_id = request.user_id or None

        # Generate standup via service
        result: StandupResult = await service.orchestrate_standup_workflow(
            user_id=user_id, workflow_type=workflow_type
        )

        # Format according to requested output format
        formatted_standup = format_standup(result, request.format)

        # Calculate total generation time
        end_time = time.time()
        total_time_ms = int((end_time - start_time) * 1000)

        # Build performance metrics
        performance_metrics = {
            "generation_time_ms": total_time_ms,
            "service_time_ms": result.generation_time_ms,
            "formatting_time_ms": total_time_ms - result.generation_time_ms,
        }

        # Add formatted metrics
        performance_metrics.update(format_standup_metrics(performance_metrics))

        # Build metadata
        metadata = {
            "mode": request.mode,
            "format": request.format,
            "user_id": result.user_id,
            "timestamp": datetime.now().isoformat(),
            "context_source": result.context_source,
        }

        # Return response
        return StandupResponse(
            success=True,
            standup=formatted_standup,
            metadata=metadata,
            performance_metrics=performance_metrics,
        )

    except StandupIntegrationError as e:
        # Service-level integration errors (graceful degradation handled by service)
        # This shouldn't normally happen as service handles degradation
        return internal_error(f"Standup generation failed: {str(e)}")
    except Exception as e:
        # Unexpected errors
        return internal_error("Unexpected error during standup generation")


@router.get("/modes", response_model=ModesResponse)
async def get_modes():
    """
    Get list of supported standup generation modes.

    Returns mode names and descriptions for all available generation modes.
    Useful for clients to discover what modes are available.

    Returns:
        ModesResponse with modes list and descriptions
    """
    return ModesResponse(
        modes=["standard", "issues", "documents", "calendar", "trifecta"],
        descriptions={
            "standard": "Basic standup generation with session context",
            "issues": "Standup with GitHub issues intelligence",
            "documents": "Standup with document suggestions from knowledge graph",
            "calendar": "Standup with calendar integration and meeting context",
            "trifecta": "All intelligence sources combined (issues + documents + calendar)",
        },
    )


@router.get("/formats", response_model=FormatsResponse)
async def get_formats():
    """
    Get list of supported output formats.

    Returns format names and descriptions for all available output formats.
    Useful for clients to discover what formats are available.

    Returns:
        FormatsResponse with formats list and descriptions
    """
    return FormatsResponse(
        formats=["json", "slack", "markdown", "text"],
        descriptions={
            "json": "Raw structured data with all fields",
            "slack": "Slack-formatted message with emoji and sections",
            "markdown": "Markdown-formatted text for documentation",
            "text": "Plain text format for simple display",
        },
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for standup API.

    Returns service status and availability information.
    Useful for monitoring and load balancers.

    Returns:
        HealthResponse with status and service info
    """
    return HealthResponse(
        status="healthy",
        service="standup-api",
        timestamp=datetime.now(timezone.utc).isoformat(),
        modes_available=5,
        formats_available=4,
    )


class TodayStandupResponse(BaseModel):
    """#1269 — the honest derived standup: prose narrative + the structured slots."""

    prose: str
    summary: Dict[str, Any]  # {yesterday, today, watch} of StandupItem dicts


@router.get("/today", response_model=TodayStandupResponse)
async def get_today_standup(
    current_user: Optional[JWTClaims] = Depends(get_current_user_optional),
) -> TodayStandupResponse:
    """#1269 — the on-demand DERIVED standup (StandupAssembler over the live entity
    catalog: conversations + documents + work items + calendar). The honest surface the
    `/standup` page + the morning card (#1269 P4) consume.

    PARALLEL to ``POST /generate`` (the legacy MorningStandupWorkflow path): this adds the
    honest derived standup WITHOUT changing the /generate contract, so the Slack skill +
    consciousness/personality bridges that depend on ``StandupResult`` stay untouched (the
    full migration off the hollow path is a later, adapter-guarded step). Scopes to the
    authenticated user (``current_user.sub`` — the identity Radar uses); anonymous → honest
    empty. Same chat-path derivation #1269 P5 already ships, exposed as an endpoint.
    """
    from services.standup.assembler import build_user_standup_summary

    user_id = current_user.sub if current_user else None
    summary = await build_user_standup_summary(user_id)
    return TodayStandupResponse(prose=summary.to_prose(), summary=summary.to_dict())
