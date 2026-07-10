"""
User Interface Template Routes

Provides endpoints for rendering UI pages with Jinja2 templates.

Routes:
- GET / - Home page
- GET /login - Login page (Issue #393)
- GET /setup - Setup wizard page (Issue #390)
- GET /standup - Standup UI
- GET /personality-preferences - Personality preferences configuration
- GET /learning - Learning dashboard
- GET /settings - Settings index page
- GET /account - Account settings page
- GET /files - Files management page
- GET /settings/integrations - Integrations management page
- GET /lists - Lists management page
- GET /todos - Todos management page
- GET /projects - Projects management page
- GET /settings/privacy - Privacy & data settings page
- GET /settings/advanced - Advanced settings page

Issue #123: Phase 3 Route Organization (Part of INFR-MAINT-REFACTOR)
Previously: Inline in web/app.py (lines 411-874)
Now: Extracted to separate router module
"""

from pathlib import Path

import structlog
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse

logger = structlog.get_logger()

# Router configuration
router = APIRouter(tags=["ui", "templates"])


def _get_templates(request: Request):
    """
    Get Jinja2Templates from app state.

    Templates are initialized in WebComponentsInitializationPhase during startup
    and stored in app.state for dependency injection (Phase 4 - INFR-MAINT-REFACTOR).

    Args:
        request: FastAPI Request object with templates in app.state

    Returns:
        Jinja2Templates instance from app.state

    Raises:
        RuntimeError: If templates not initialized in app state
    """
    if not hasattr(request.app.state, "templates"):
        raise RuntimeError("Jinja2Templates not initialized in app state")

    templates = request.app.state.templates
    if templates is None:
        raise RuntimeError("Jinja2Templates initialization failed")

    return templates


def _extract_user_context(request: Request) -> dict:
    """
    Extract user context from request state for template injection.

    Retrieves authenticated user information from request.state (set by auth middleware)
    and returns it as a dict for passing to templates. The navigation component uses this
    to populate the user dropdown menu with the actual username instead of the default
    "user" placeholder.

    Args:
        request: FastAPI Request object with user_claims/user_id in state

    Returns:
        dict with 'user_id', 'username', and 'is_admin' keys for template context
    """
    user_id = getattr(request.state, "user_id", "user")

    # Try to get username from user_claims if available
    # JWTClaims has user_email but not username, so we try multiple sources
    username = user_id  # Default to user_id (UUID)
    user_claims = getattr(request.state, "user_claims", None)
    if user_claims:
        # First try username attribute (if it exists)
        if hasattr(user_claims, "username") and user_claims.username:
            username = user_claims.username
        # Then try user_email - extract username part before @ for display
        elif hasattr(user_claims, "user_email") and user_claims.user_email:
            email = user_claims.user_email
            # Use part before @ as username for display
            username = email.split("@")[0] if "@" in email else email
        # Also handle dict-style claims
        elif isinstance(user_claims, dict):
            if "username" in user_claims:
                username = user_claims["username"]
            elif "user_email" in user_claims:
                email = user_claims["user_email"]
                username = email.split("@")[0] if "@" in email else email

    # Extract is_admin flag from user claims (SEC-RBAC Phase 3)
    is_admin = False
    if user_claims:
        is_admin = getattr(user_claims, "is_admin", False) or (
            isinstance(user_claims, dict) and user_claims.get("is_admin", False)
        )

    return {"user_id": user_id, "username": username, "is_admin": is_admin}


async def _resolve_trust_stage(user_context: dict) -> int:
    """Resolve the user's real trust stage for server-rendering into window.trustStage.

    #1031 Q4 / #1132 / #1147: templates (insights.html, documents.html) gate
    content with data-min-stage against window.trustStage. The stage MUST be
    server-rendered from TrustComputationService — hardcoding it (the original
    Pattern-045 bug) collapses all users to Stage 1; NOT passing it leaves
    window.trustStage undefined unless home.html ran first.

    Shared helper (extracted when /documents became the 2nd route needing the
    identical block). Fail-safe: any error → Stage 1 (privacy-leaning — better
    to under-show gated content than over-show it).

    Returns int stage (NEW=1, BUILDING=2, ESTABLISHED=3, TRUSTED=4).
    """
    raw_user_id = user_context.get("user_id")
    if not raw_user_id or raw_user_id == "user":
        return 1
    try:
        from uuid import UUID

        from services.database.session_factory import AsyncSessionFactory
        from services.repositories.user_trust_profile_repository import (
            UserTrustProfileRepository,
        )
        from services.trust.trust_computation_service import TrustComputationService

        async with AsyncSessionFactory.session_scope() as session:
            trust_service = TrustComputationService(UserTrustProfileRepository(session))
            stage_enum = await trust_service.get_trust_stage(UUID(str(raw_user_id)))
            return int(stage_enum)  # TrustStage is IntEnum
    except Exception as e:
        import structlog

        structlog.get_logger().warning(
            "resolve_trust_stage_error",
            user_id=str(raw_user_id),
            error=str(e),
        )
        return 1


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Render home page or redirect to setup/login as needed.

    If user is authenticated: show home page
    If no users exist: redirect to setup wizard
    If setup complete but not authenticated: redirect to login

    Issue #390: Smart setup/login routing
    Issue #549: Post-setup orientation modal context
    Issue #419: Trust-gated home state (MUX-NAV-HOME)
    """
    from uuid import UUID

    from sqlalchemy import text

    from services.database.session_factory import AsyncSessionFactory
    from services.repositories.user_trust_profile_repository import UserTrustProfileRepository
    from services.shared_types import TrustStage
    from services.trust import TrustComputationService

    user_id = getattr(request.state, "user_id", None)

    # If user is authenticated, show home page
    if user_id and user_id != "user":
        templates = _get_templates(request)
        user_context = _extract_user_context(request)

        # Issue #549: Get setup_complete and orientation_seen for orientation modal
        # Issue #419: Get trust_stage for trust-gated home state
        setup_complete = False
        orientation_seen = True  # Default to True so modal doesn't show if lookup fails
        trust_stage = TrustStage.NEW  # Default to NEW if lookup fails
        try:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                result = await session.execute(
                    text("SELECT setup_complete, orientation_seen FROM users WHERE id = :user_id"),
                    {"user_id": str(user_id)},  # Convert UUID to string for SQL comparison
                )
                row = result.fetchone()
                if row:
                    setup_complete = row[0]
                    orientation_seen = row[1]

                # Issue #419: Get user's trust stage for consciousness-aware home state
                trust_repo = UserTrustProfileRepository(session)
                trust_service = TrustComputationService(trust_repo)
                trust_stage = await trust_service.get_trust_stage(UUID(str(user_id)))
        except Exception as e:
            logger.warning(f"Error fetching user setup status: {e}, skipping orientation modal")

        # Issue #1194 / #1033: surface composted reflections ("Recently" module) on
        # the home start-screen for Stage 3+ users. Degrades to [] on any failure so
        # the home page never breaks on surfacing.
        surfaced_insights = []
        try:
            from datetime import datetime as _dt
            from datetime import timezone as _tz

            from services.home.home_state_service import HomeStateContext, HomeStateService

            _hour = _dt.now().hour
            _tod = "morning" if 5 <= _hour < 12 else ("evening" if _hour >= 17 else "midday")
            _home = await HomeStateService().generate_home_state(
                HomeStateContext(
                    user_id=UUID(str(user_id)),
                    trust_stage=trust_stage,
                    timestamp=_dt.now(_tz.utc),
                    time_of_day=_tod,
                )
            )
            surfaced_insights = _home.surfaced_insights
        except Exception as e:
            logger.warning(f"home-state reflection surfacing failed: {e}")

        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user_context,
                "setup_complete": setup_complete,
                "orientation_seen": orientation_seen,
                # Issue #419: Trust stage for trust-gated home state rendering
                # Note: Per ADR-053, trust is "invisible to users but effects noticeable"
                # We don't show "Stage 2" to users, just vary the experience
                "trust_stage": trust_stage.value,  # Pass as int for template logic
                "trust_stage_name": trust_stage.name,  # Pass name for debugging/logging
                # F2 #1266: home renders the INLINE chat → suppress the shell floating widget
                "hide_floating_widget": True,
                # #1280 v2: home gets the persistent 320px Radar column (app_shell aside)
                "show_radar": True,
                # Issue #1194 / #1033: composted reflections for the "Recently" module
                "surfaced_insights": surfaced_insights,
            },
        )

    # Check if any users exist in database
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar_one()

        # If no users exist, show setup wizard
        if user_count == 0:
            return RedirectResponse(url="/setup", status_code=302)
    except Exception as e:
        # Issue #722: If database query fails (e.g., during startup race condition),
        # redirect to setup rather than login. First-time users shouldn't see login.
        # Setup wizard handles its own error states more gracefully.
        logger.warning(f"Error checking user count: {e}, redirecting to setup wizard")
        return RedirectResponse(url="/setup", status_code=302)

    # Users exist and user not authenticated - redirect to login
    return RedirectResponse(url="/login", status_code=302)


@router.post("/api/v1/orientation/dismiss")
async def dismiss_orientation(request: Request):
    """
    Mark orientation modal as seen for current user.

    Issue #549: Post-setup orientation persistence
    """
    from fastapi.responses import JSONResponse
    from sqlalchemy import text

    from services.database.session_factory import AsyncSessionFactory

    user_id = getattr(request.state, "user_id", None)
    if not user_id or user_id == "user":
        return JSONResponse({"status": "error", "message": "Not authenticated"}, status_code=401)

    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            await session.execute(
                text("UPDATE users SET orientation_seen = true WHERE id = :user_id"),
                {"user_id": user_id},
            )
            await session.commit()
        return JSONResponse({"status": "ok"})
    except Exception as e:
        logger.error(f"Error dismissing orientation: {e}")
        return JSONResponse({"status": "error", "message": "Failed to save"}, status_code=500)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serve login page.

    If user is already authenticated, redirect to homepage.
    If no users exist, redirect to setup wizard.
    Otherwise, show login form.

    Issue #393: CORE-UX-AUTH - Login UI
    Issue #722: Redirect to setup if no users exist
    """
    from sqlalchemy import text

    from services.database.session_factory import AsyncSessionFactory

    templates = _get_templates(request)

    # Check if user is already authenticated (has valid user_id in state)
    user_id = getattr(request.state, "user_id", None)
    if user_id and user_id != "user":  # "user" is the default placeholder
        return RedirectResponse(url="/", status_code=302)

    # Issue #722: Check if any users exist - if not, redirect to setup wizard
    # First-time users shouldn't see login page, they should see setup
    try:
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM users"))
            user_count = result.scalar_one()

        if user_count == 0:
            return RedirectResponse(url="/setup", status_code=302)
    except Exception as e:
        # If database query fails, redirect to setup (safer for first-time users)
        logger.warning(f"Error checking user count on login page: {e}, redirecting to setup")
        return RedirectResponse(url="/setup", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    """Serve the password-reset page (#441/#1261).

    Pre-login by definition (a forgotten password is why you're here), so no
    auth/redirect logic — the page itself is inert without a valid PM-issued
    reset code (the POST endpoint enforces the real gate).
    """
    templates = _get_templates(request)
    return templates.TemplateResponse("reset_password.html", {"request": request})


@router.get("/setup", response_class=HTMLResponse)
async def setup_page(request: Request):
    """
    Setup wizard page (Issue #390).

    Renders multi-step setup wizard for new installations.
    Accessible without authentication.
    """
    templates = _get_templates(request)
    return templates.TemplateResponse("setup.html", {"request": request})


@router.get("/standup", response_class=HTMLResponse)
async def standup_ui(request: Request):
    """Render standup UI"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("standup.html", {"request": request, "user": user_context})


@router.get("/personality-preferences", response_class=HTMLResponse)
async def personality_preferences_ui(request: Request):
    """Serve the personality preferences interface"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "personality-preferences.html", {"request": request, "user": user_context}
    )


@router.get("/learning", response_class=HTMLResponse)
async def learning_dashboard_ui(request: Request):
    """Serve the learning dashboard interface"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "learning-dashboard.html", {"request": request, "user": user_context}
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_index_ui(request: Request):
    """Serve the settings index page (G2: Settings Index Page)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings-index.html", {"request": request, "user": user_context}
    )


@router.get("/account", response_class=HTMLResponse)
async def account_settings_ui(request: Request):
    """Serve the account settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("account.html", {"request": request, "user": user_context})


@router.get("/transparency", response_class=HTMLResponse)
async def transparency_ui(request: Request):
    """Serve the transparency & audit log page (#1099 MUX/UI Round 2 Surface 7).

    Renders audit-envelope entries for the user's active conversation, fetched
    client-side from /api/v1/transparency/audit-log/{session_id} (shipped via
    #1095 with Pattern-071 user-binding + uniform 403). Per ADR-063
    (User-Facing Audit Envelope Read Surface).
    """
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "transparency.html", {"request": request, "user": user_context}
    )


@router.get("/files", response_class=HTMLResponse)
async def files_ui(request: Request):
    """Serve the files page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("files.html", {"request": request, "user": user_context})


@router.get("/documents", response_class=HTMLResponse)
async def documents_ui(request: Request):
    """
    #1270 beta band-aid (PM-approved 2026-06-19): /documents and /files read as
    near-duplicates (PM UAT 2026-06-17). Collapsed to the single working surface —
    /files (the fuller file browser, 22 JS fns vs documents.html's 7) — presented under
    the "Documents" nav label. /documents redirects here so old links/bookmarks survive.

    The full source-type object-model refactor (uploaded/generated/federated) plus a
    restored Q&A-perspective view is #1270 in D2; this band-aid defers documents.html's
    Stage-4+ perspective (#422) to that refactor. To restore the perspective view, revert
    this redirect (the old render is in git history) — but reconcile it with #1270 first.
    """
    return RedirectResponse(url="/files", status_code=302)


@router.get("/insights", response_class=HTMLResponse)
async def insights_ui(request: Request):
    """
    Insight Journal page (#424 MUX-IMPLEMENT-COMPOST).

    Browse all learnings organized by topic.
    Control actions: Correct, Delete, Confirm, "Why?"
    Design: D2 Control Interface Patterns

    Per #1031 Q4 (May 3): trust_stage is server-rendered into
    `window.trustStage` so the page's `data-min-stage` gating works
    against the actual user stage rather than defaulting to 1.
    """
    templates = _get_templates(request)
    user_context = _extract_user_context(request)

    # #1031 Q4 / #1132: trust_stage server-rendered into window.trustStage so
    # the page's data-min-stage gating works against the user's actual stage.
    # Uses shared _resolve_trust_stage helper (Pattern-045 fix).
    trust_stage = await _resolve_trust_stage(user_context)

    return templates.TemplateResponse(
        "insights.html",
        {"request": request, "user": user_context, "trust_stage": trust_stage},
    )


@router.get("/settings/integrations", response_class=HTMLResponse)
async def integrations_page(request: Request):
    """Integrations management page - Coming soon"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "integrations.html", {"request": request, "user": user_context}
    )


@router.get("/settings/llm-keys", response_class=HTMLResponse)
async def llm_keys_settings_page(request: Request):
    """LLM API key management (#1380) — the Settings surface for the
    /api/v1/keys backend, which was UI-orphaned outside the setup wizard."""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_llm_keys.html", {"request": request, "user": user_context}
    )


@router.get("/settings/integrations/notion", response_class=HTMLResponse)
async def notion_settings_page(request: Request):
    """Notion API key settings page (Issue #540)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_notion.html", {"request": request, "user": user_context}
    )


@router.get("/settings/integrations/github", response_class=HTMLResponse)
async def github_settings_page(request: Request):
    """GitHub token settings page (Issue #541)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_github.html", {"request": request, "user": user_context}
    )


@router.get("/settings/integrations/slack", response_class=HTMLResponse)
async def slack_settings_page(request: Request):
    """Slack OAuth settings page (Issue #528)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_slack.html", {"request": request, "user": user_context}
    )


@router.get("/settings/integrations/calendar", response_class=HTMLResponse)
async def calendar_settings_page(request: Request):
    """Google Calendar OAuth settings page (Issue #537)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_calendar.html", {"request": request, "user": user_context}
    )


@router.get("/settings/projects", response_class=HTMLResponse)
async def settings_projects_page(request: Request):
    """Project integration and repository management settings (Issue #861)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "settings_projects.html", {"request": request, "user": user_context}
    )


@router.get("/lists", response_class=HTMLResponse)
async def lists_ui(request: Request):
    """Lists management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    lists_data = []
    return templates.TemplateResponse(
        "lists.html", {"request": request, "user": user_context, "lists": lists_data}
    )


@router.get("/todos", response_class=HTMLResponse)
async def todos_ui(request: Request):
    """Todos management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    todos_data = []
    return templates.TemplateResponse(
        "todos.html", {"request": request, "user": user_context, "todos": todos_data}
    )


@router.get("/projects", response_class=HTMLResponse)
async def projects_ui(request: Request):
    """Projects management page with permission-aware UI (Issue #376)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    projects_data = []
    return templates.TemplateResponse(
        "projects.html", {"request": request, "user": user_context, "projects": projects_data}
    )


@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def project_detail_ui(request: Request, project_id: str):
    """Project detail view with lifecycle indicators (#711 MUX-PROJECT-DETAIL-VIEW)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "project_detail.html",
        {"request": request, "user": user_context, "project_id": project_id},
    )


@router.get("/work-items", response_class=HTMLResponse)
async def work_items_ui(request: Request):
    """Work Items view with lifecycle indicators (Issue #710)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse("work_items.html", {"request": request, "user": user_context})


@router.get("/settings/privacy", response_class=HTMLResponse)
async def privacy_settings_ui(request: Request):
    """Serve the privacy & data settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "privacy-settings.html", {"request": request, "user": user_context}
    )


@router.get("/settings/advanced", response_class=HTMLResponse)
async def advanced_settings_ui(request: Request):
    """Serve the advanced settings page (Coming Soon)"""
    templates = _get_templates(request)
    user_context = _extract_user_context(request)
    return templates.TemplateResponse(
        "advanced-settings.html", {"request": request, "user": user_context}
    )
