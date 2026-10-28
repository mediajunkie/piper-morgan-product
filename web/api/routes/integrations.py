"""
Integration Health Check API Routes
Issue #530: ALPHA-SETUP-VERIFY - Integration Health Check Dashboard

Provides API endpoints for checking and testing integration health status.
"""

import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.integrations.principal_test_results import (
    PrincipalTestResultStore,
    get_test_result_store,
)

logger = structlog.get_logger()

# Router for integration health endpoints
router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


class IntegrationStatus(BaseModel):
    """Status information for a single integration"""

    name: str
    display_name: str
    status: str  # healthy, degraded, failed, connected (#2044: configured, never tested), unknown, not_configured
    status_message: str
    last_check: Optional[str] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None
    configure_url: Optional[str] = None
    can_test: bool = True
    # #2031 (CXO's GitHub card states): a warning glyph before the status line, a
    # second line under it, whether the Test button shows at all, and a card action
    # that replaces the default buttons ("reconnect" → a Reconnect link to
    # ``configure_url``). All optional; other integrations leave them unset.
    status_icon: Optional[str] = None
    status_detail: Optional[str] = None
    show_test: bool = True
    action: Optional[str] = None


class IntegrationHealthResponse(BaseModel):
    """Response model for integration health check"""

    overall_status: str
    timestamp: str
    integrations: List[IntegrationStatus]
    healthy_count: int
    total_count: int
    # #2068 (CXO ruling): the headline and the count line are computed here, once,
    # over the CONNECTED integrations only; the page renders them as given.
    headline: str = ""
    summary: str = ""


class ConnectionTestResponse(BaseModel):
    """Response model for testing a single connection"""

    integration: str
    success: bool
    message: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    fix_suggestion: Optional[str] = None
    # #2037 (ADR-070 B4/B5): the resolver's serving leg ("oauth" | "pat") and, when a
    # personal token is covering for a stale OAuth grant, the degradation reason.
    # GitHub only; None for every other integration. Clients key state on these,
    # never on ``message`` copy.
    leg: Optional[str] = None
    stale_reason: Optional[str] = None


# Integration metadata and error guidance
INTEGRATION_REGISTRY = {
    "notion": {
        "display_name": "Notion",
        "icon": "📝",
        "configure_url": "/settings/integrations/notion",  # Issue #540: Dedicated settings page
        "errors": {
            "api_key_invalid": {
                "message": "Invalid Notion API key",
                "fix": "Check your Notion integration token in Settings → Integrations → Notion",
            },
            "connection_failed": {
                "message": "Cannot connect to Notion API",
                "fix": "Check your internet connection and Notion service status",
            },
            "permission_denied": {
                "message": "Integration lacks required permissions",
                "fix": "Ensure the integration has access to the required databases in Notion",
            },
        },
    },
    "slack": {
        "display_name": "Slack",
        "icon": "💬",
        "configure_url": "/settings/integrations/slack",  # Issue #528: Dedicated settings page
        "errors": {
            "token_expired": {
                "message": "Slack OAuth token has expired",
                "fix": "Re-authorize Slack in Settings → Integrations → Slack",
            },
            "token_invalid": {
                "message": "Invalid Slack token",
                "fix": "Re-connect your Slack workspace",
            },
            "scope_missing": {
                "message": "Missing required Slack permissions",
                "fix": "Re-authorize with updated permissions",
            },
        },
    },
    "github": {
        "display_name": "GitHub",
        "icon": "🐙",
        "configure_url": "/settings/integrations/github",
        "errors": {
            "token_invalid": {
                "message": "Invalid GitHub token",
                "fix": "Update your GitHub personal access token in Settings",
            },
            "rate_limited": {
                "message": "GitHub API rate limit exceeded",
                "fix": "Wait for rate limit reset or use authenticated requests",
            },
            "repo_not_found": {
                "message": "Repository not found or inaccessible",
                "fix": "Check repository permissions and token scope",
            },
            # #2012: the OAuth Test's live probe degrades with the connector taxonomy.
            # #2029: one step — the OAuth callback upserts the grant and sets the binding
            # BOUND over a STALE row, so no Disconnect is needed first.
            "stale_token": {
                "message": "Your GitHub connection needs re-authorizing",
                "fix": "In Settings → Integrations → GitHub, Reconnect with GitHub",
            },
            "connect_required": {
                "message": "GitHub is not connected for your account",
                "fix": "In Settings → Integrations → GitHub, Connect with GitHub",
            },
            "unreachable": {
                "message": "GitHub's MCP server is unreachable right now",
                "fix": "Try again in a few minutes",
            },
        },
    },
    "calendar": {
        "display_name": "Google Calendar",
        "icon": "📅",
        "configure_url": "/settings/integrations/calendar",  # Issue #537: Dedicated settings page
        "errors": {
            "auth_failed": {
                "message": "Calendar authentication failed",
                "fix": "Re-authorize Google Calendar access",
            },
            "mcp_not_running": {
                "message": "Calendar MCP server not running",
                "fix": "Start the Google Calendar MCP server",
            },
        },
    },
}


# #2044 (CXO, 2026-10-15): a card with a connection but no test result reads
# "Connected" with the health line "Not checked yet. Press Test." (a statement plus
# a plain instruction; nothing to arm). "unknown" is internal vocabulary and never
# reaches a configured card. One source for every provider's card; the healthy
# summary does not count an unchecked connection.
UNCHECKED_STATUS = "connected"
UNCHECKED_MESSAGE = "Connected"
UNCHECKED_DETAIL = "Not checked yet. Press Test."
# #2044 (CXO, 19:01): when the health CHECK itself throws, the card says so in plain
# words and offers the retry; the raw error goes to the log, never the card.
CHECK_FAILED_MESSAGE = "Couldn't check this just now. Press Test to try again."


def _unchecked_card(integration_id: str, metadata: Dict[str, Any]) -> "IntegrationStatus":
    """The configured-but-never-tested card (#2044): this principal has no Test result
    on record (#2071; another account's result never counts)."""
    return IntegrationStatus(
        name=integration_id,
        display_name=metadata["display_name"],
        status=UNCHECKED_STATUS,
        status_message=UNCHECKED_MESSAGE,
        status_detail=UNCHECKED_DETAIL,
        configure_url=metadata.get("configure_url"),
        can_test=True,
    )


def _get_test_result_store() -> PrincipalTestResultStore:
    """The per-principal Test result store (#2071).

    A Test result is keyed by ``(principal, integration)``: the Test route writes under
    the caller's principal and every card reader passes the viewer's principal. Before
    #2071 this was the host-wide ``IntegrationHealthMonitor`` singleton keyed by
    integration name alone, so one account's Test showed on every account's card.
    """
    return get_test_result_store()


def _get_error_guidance(integration: str, error_type: str) -> tuple[str, Optional[str]]:
    """Get user-friendly error message and fix suggestion"""
    registry = INTEGRATION_REGISTRY.get(integration, {})
    errors = registry.get("errors", {})
    error_info = errors.get(error_type, {})

    message = error_info.get("message", f"Error: {error_type}")
    fix = error_info.get("fix")

    return message, fix


def summarize_integrations(integrations: List["IntegrationStatus"]) -> tuple:
    """#2068 (CXO's ruling): the Integrations headline counts only integrations the
    person has connected (card status other than ``not_configured``); an
    unconnected integration is never an issue.

    Returns ``(overall_status, headline, summary, working_count, connected_count)``.
    - none connected: "Nothing connected yet"
    - two or more failing (``failed``): "Multiple Issues"
    - one failing, or any connected one in a warning state (degraded / unknown):
      "Needs attention"; the count line counts CHECKED integrations only and names
      the untested ones ("0 of 1 checked integrations working, 1 not yet tested")
    - every connected one healthy: "All Systems Healthy"
    - otherwise (connected, none tested yet, nothing wrong): "Connected, not yet tested"
    """
    connected = [i for i in integrations if i.status != "not_configured"]
    working = sum(1 for i in connected if i.status == "healthy")
    failing = sum(1 for i in connected if i.status in ("failed", "unhealthy"))
    warning = sum(1 for i in connected if i.status in ("degraded", "unknown"))
    n = len(connected)
    if n == 0:
        return "none", "Nothing connected yet", "", 0, 0
    # #2075 (CXO, 2026-10-17): an untested integration (card status "connected",
    # no recorded check and no recorded fault) is neither working nor failing in
    # ANY branch. The failure branches count only checked integrations in the
    # denominator and name the untested ones separately.
    untested = sum(1 for i in connected if i.status == "connected")
    checked = n - untested
    if failing or warning:
        summary = f"{working} of {checked} checked integrations working"
        if untested:
            summary += f", {untested} not yet tested"
        if failing >= 2:
            return "unhealthy", "Multiple Issues", summary, working, n
        return "degraded", "Needs attention", summary, working, n
    if working == n:
        return (
            "healthy",
            "All Systems Healthy",
            f"{working} of {n} connected integrations working",
            working,
            n,
        )
    # Nothing wrong, but not every connected one has a recorded check; the
    # count line counts checks, not health ("0 of 1 checked").
    return "unknown", "Connected, not yet tested", f"{checked} of {n} checked", working, n


@router.get("/health", response_model=IntegrationHealthResponse)
async def get_integrations_health(
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Get health status of all configured integrations.

    Returns status information for Notion, Slack, GitHub, Calendar, etc.
    Issue #530: ALPHA-SETUP-VERIFY

    2026-05-21: Added auth dependency to thread user_id down to per-integration
    config-status checks. Without it, user-scoped credentials in keychain
    (like Slack tokens stored under user_id per ADR-058) are invisible to the
    config-status check and integrations forever appear "Not configured" after
    successful OAuth.
    """
    try:
        integrations = []

        # Check each integration
        for integration_id, metadata in INTEGRATION_REGISTRY.items():
            integration_status = await _check_integration_health(
                integration_id, metadata, user_id=current_user.sub
            )
            integrations.append(integration_status)

        overall, headline, summary, healthy_count, _connected = summarize_integrations(integrations)

        # total_count stays the number of integrations listed (all four), as the
        # field's name says and the dashboard pin asserts; the #2068 connected
        # count lives in ``summary`` ("N of M connected integrations working").
        return IntegrationHealthResponse(
            overall_status=overall,
            timestamp=datetime.now(timezone.utc).isoformat(),
            integrations=integrations,
            healthy_count=healthy_count,
            total_count=len(integrations),
            headline=headline,
            summary=summary,
        )

    except Exception as e:
        logger.error("Failed to check integrations health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Health check failed: {str(e)}",
        )


@router.post("/test/{integration_name}", response_model=ConnectionTestResponse)
async def check_integration_connection(
    integration_name: str, current_user: JWTClaims = Depends(get_current_user)
):
    """
    Test connection to a specific integration.

    Performs an active health check and returns detailed results.
    Issue #530: ALPHA-SETUP-VERIFY
    """
    if integration_name not in INTEGRATION_REGISTRY:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unknown integration: {integration_name}",
        )

    metadata = INTEGRATION_REGISTRY[integration_name]
    start_time = time.time()
    # #2071: the result is recorded under THIS caller's principal only.
    principal = current_user.sub
    results = _get_test_result_store()

    try:
        result = await _test_integration(integration_name, user_id=current_user.sub)
        latency_ms = (time.time() - start_time) * 1000

        if result["success"]:
            results.record_test_result(principal, integration_name, ok=True, latency_ms=latency_ms)
            # #2012: the GitHub Test names its serving leg (CXO's lines); other
            # integrations keep the generic line.
            message = f"{metadata['display_name']} connection successful"
            if integration_name == "github" and result.get("message"):
                message = result["message"]
            # #2037: the structured leg/stale flag rides beside the message (GitHub
            # only; other integrations' results carry neither key, so both stay None).
            return ConnectionTestResponse(
                integration=integration_name,
                success=True,
                message=message,
                latency_ms=round(latency_ms, 2),
                leg=result.get("leg"),
                stale_reason=result.get("stale_oauth_reason"),
            )
        elif result.get("error_type") in ("check_failed", "connection_failed", "unreachable"):
            # #2151 (route group 1): the check couldn't run. Nothing is recorded, so the
            # card never turns "failed" over a connection nobody could check. Arch 10-24
            # 12:32: ``connection_failed`` (every ``_test_*``'s ``except``) is the same
            # thing: a timeout or DNS failure on our side, never the user's internet. Arch
            # 15:29 (gap C): ``unreachable`` (a GitHub transport degrade) too.
            return ConnectionTestResponse(
                integration=integration_name,
                success=False,
                message=CHECK_FAILED_MESSAGE,
                latency_ms=round(latency_ms, 2),
            )
        else:
            error_msg = result.get("error", result.get("error_type", "Unknown error"))
            results.record_test_result(
                principal, integration_name, ok=False, error=error_msg, latency_ms=latency_ms
            )
            message, fix = _get_error_guidance(
                integration_name, result.get("error_type", "unknown")
            )
            return ConnectionTestResponse(
                integration=integration_name,
                success=False,
                message=message,
                latency_ms=round(latency_ms, 2),
                error=result.get("error"),
                fix_suggestion=fix,
            )

    except Exception as e:
        # #2151 (Arch 10-24 12:32): a Test that raised is a check that couldn't run: no
        # failed result is recorded, and no exception text reaches the page.
        latency_ms = (time.time() - start_time) * 1000
        logger.error(f"Integration test failed: {integration_name}", error=str(e))
        return ConnectionTestResponse(
            integration=integration_name,
            success=False,
            message=CHECK_FAILED_MESSAGE,
            latency_ms=round(latency_ms, 2),
        )


@router.post("/test-all", response_model=List[ConnectionTestResponse])
async def check_all_connections(current_user: JWTClaims = Depends(get_current_user)):
    """
    Test all configured integrations.

    Issue #530: ALPHA-SETUP-VERIFY
    """
    results = []
    for integration_name in INTEGRATION_REGISTRY.keys():
        try:
            result = await check_integration_connection(integration_name, current_user=current_user)
            results.append(result)
        except Exception as e:
            results.append(
                ConnectionTestResponse(
                    integration=integration_name,
                    success=False,
                    message=f"Test failed: {str(e)}",
                    error=str(e),
                )
            )
    return results


# #2031 — CXO's GitHub card words (2026-10-15), verbatim. The card is the third consumer
# of the one credential resolver (ADR-070 B4), after the #2012 Test and #2029's
# Settings → GitHub page; its state comes from ``resolve_credential``, never from
# whether a binding row is BOUND.
_GITHUB_CARD_CONNECTED = "Connected with your GitHub account."
_GITHUB_CARD_PAT_TITLE = "Connected via your personal token"
_GITHUB_CARD_PAT_DETAIL = (
    "Your GitHub connection needs re-authorizing, so I'm not using it right now."
)
_GITHUB_CARD_RECONNECT_TITLE = "Needs reconnecting"
GITHUB_CARD_RECONNECT_DETAIL = "GitHub no longer accepts your connection."
_GITHUB_CARD_NOT_CONFIGURED = "Not configured"
_WARNING_ICON = "⚠️"


def _recorded_check_iso(principal: Optional[str], integration_id: str) -> Optional[str]:
    """ISO timestamp of THIS principal's last Test of ``integration_id``, else None.

    #2066 added the time line; #2071 keys it by principal, so another account's Test
    never stamps this account's card. No record for this principal is None (never
    checked, #2044, m-44); there is no host-wide entry to fall back to.
    """
    result = _get_test_result_store().get_test_result(principal, integration_id)
    return result.checked_at_iso if result is not None else None


async def _github_card(
    metadata: Dict[str, Any], user_id: Optional[str]
) -> Optional[IntegrationStatus]:
    """GitHub's Integrations card from the resolver's outcome (#2031, ADR-070 B4/B5).

    - OAuth leg serving → Connected.
    - PAT leg serving with a STALE OAuth grant, and the token answers one read (the
      #2012 Test's probe, the evidence #2029's page uses) → ⚠️ token-serving.
    - Nothing serving with a STALE grant (no token, or a token GitHub also refuses)
      → ⚠️ Needs reconnecting, a Reconnect action, Test hidden.
    - Nothing serving and no stale grant → Not configured.

    The words name the reason (B5), so they are used only where it is STALE_TOKEN.
    Any other resolver outcome (the user's own PAT with no stale grant; a non-stale
    degrade such as UNREACHABLE) returns ``None`` and the generic configured path
    (cached Test result, else "Click 'Test'") governs, as it did before.
    """
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    def card(**fields: Any) -> IntegrationStatus:
        return IntegrationStatus(
            name="github",
            display_name=metadata["display_name"],
            configure_url=metadata.get("configure_url"),
            **fields,
        )

    not_configured = card(
        status="not_configured", status_message=_GITHUB_CARD_NOT_CONFIGURED, can_test=False
    )
    needs_reconnecting = card(
        status="degraded",
        status_icon=_WARNING_ICON,
        status_message=_GITHUB_CARD_RECONNECT_TITLE,
        status_detail=GITHUB_CARD_RECONNECT_DETAIL,
        can_test=False,
        show_test=False,
        action="reconnect",
    )
    if not user_id:
        return not_configured

    adapter = GitHubMCPSpatialAdapter()
    credential = await adapter.resolve_credential(user_id)
    if isinstance(credential, DegradationResponse):
        if credential.reason == DegradationReason.STALE_TOKEN:
            return needs_reconnecting
        if credential.reason in (
            DegradationReason.CONNECT_REQUIRED,
            DegradationReason.NOT_CONFIGURED,
        ):
            return not_configured
        return None
    if getattr(credential, "leg", None) == "oauth":
        # #2066: the OAuth-leg card carries the last recorded check like the generic
        # path below does, so the #2045 time line ("Healthy. Checked just now." /
        # "Last checked at …") can render. This account's own Test only (#2071).
        # #2075 (CXO): health is claimed only on a recorded check. A bound grant
        # nobody has tested is "connected" (the #2044 unchecked status), so the
        # headline reads "Connected, not yet tested", never "All Systems Healthy".
        # The card line stays "Connected with your GitHub account." either way.
        oauth_result = _get_test_result_store().get_test_result(user_id, "github")
        if oauth_result is None:
            oauth_status, oauth_error = "connected", None
        elif oauth_result.ok:
            oauth_status, oauth_error = "healthy", None
        else:
            oauth_status, oauth_error = "failed", oauth_result.error or "Connection failed"
        return card(
            status=oauth_status,
            status_message=_GITHUB_CARD_CONNECTED,
            # #2187 (CXO 14:32 10-28): with no Test on record the card says what it
            # knows, Slack's form: "Connected with your GitHub account." plus the
            # health line "Not checked yet. Press Test." A binding alone never
            # reads as a checked connection (the #2044 unchecked state, applied here).
            status_detail=UNCHECKED_DETAIL if oauth_result is None else None,
            can_test=True,
            last_check=oauth_result.checked_at_iso if oauth_result is not None else None,
            error=oauth_error,
        )
    if getattr(credential, "stale_oauth_reason", None) == DegradationReason.STALE_TOKEN:
        probe = await adapter.search_user_repositories(user_id, limit=1)
        if probe.degradation is not None:
            return needs_reconnecting
        return card(
            status="degraded",
            status_icon=_WARNING_ICON,
            status_message=_GITHUB_CARD_PAT_TITLE,
            status_detail=_GITHUB_CARD_PAT_DETAIL,
            can_test=True,
            # #2053 (CXO): Reconnect in every stale state, beside Test.
            action="reconnect",
        )
    return None


async def _check_integration_health(
    integration_id: str, metadata: Dict[str, Any], user_id: Optional[str] = None
) -> IntegrationStatus:
    """Check health of a specific integration without active testing.

    Args:
        integration_id: integration name (e.g. "slack", "calendar")
        metadata: registry entry from INTEGRATION_REGISTRY
        user_id: authenticated user id (used to look up user-scoped keychain
            credentials per ADR-058; if None, only env-var configuration is
            visible — fine for non-user-scoped integrations).
    """
    try:
        # #2031 (ADR-070 B4): GitHub's card derives from the one credential resolver.
        # A mapped outcome is the card; ``None`` means the user's own token serves with
        # nothing stale, so the configured path below (cached Test result) governs.
        if integration_id == "github":
            github_card = await _github_card(metadata, user_id)
            if github_card is not None:
                return github_card
            config_status = "configured"
        else:
            config_status = await _get_integration_config_status(integration_id, user_id=user_id)

        if config_status == "unknown":
            # #2151 ISS-STATUS: the credential lookup itself failed. Neither "Not
            # configured" nor connected: the card says the check failed (CXO's line).
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status="unknown",
                status_message=CHECK_FAILED_MESSAGE,
                configure_url=metadata.get("configure_url"),
                can_test=True,
            )

        if config_status == "not_configured":
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status="not_configured",
                status_message="Not configured",
                configure_url=metadata.get("configure_url"),
                can_test=False,
            )

        # #2071: THIS user's own Test result. No record for this principal is the
        # unchecked card (#2044); another account's result never reaches this card.
        result = _get_test_result_store().get_test_result(user_id, integration_id)
        if result is not None:
            if result.ok:
                # #2049: the page renders the check time from last_check in the viewer's zone.
                status_str, status_message = "healthy", "Healthy"
            else:
                status_str, status_message = "failed", result.error or "Connection failed"
            return IntegrationStatus(
                name=integration_id,
                display_name=metadata["display_name"],
                status=status_str,
                status_message=status_message,
                last_check=result.checked_at_iso,
                error=result.error,
                configure_url=metadata.get("configure_url"),
                can_test=True,
            )

        # Configured but never tested by this principal (#2044, #2071).
        return _unchecked_card(integration_id, metadata)

    except Exception as e:
        # #2044: the raw error is logged here; the card carries CXO's line only
        # (``error`` unset, so the page does not redden a line that is not a failure
        # of the integration itself).
        logger.warning(f"Failed to check {integration_id} health", error=str(e))
        return IntegrationStatus(
            name=integration_id,
            display_name=metadata["display_name"],
            status="unknown",
            status_message=CHECK_FAILED_MESSAGE,
            configure_url=metadata.get("configure_url"),
            can_test=True,
        )


async def _get_integration_config_status(integration_id: str, user_id: Optional[str] = None) -> str:
    """Check if an integration is configured (user-scoped stores + env).

    #1547: canonical logic hoisted to
    services/integrations/integration_status_service.py — the #1513 (github
    keychain) / #1337 (notion user-secret store) / #839 (calendar user-scoped
    key) / ADR-058 (slack keychain) composition lives there now. This thin
    delegate preserves the route's historical name and status-string contract.
    """
    from services.integrations.integration_status_service import get_config_status

    status, _via = await get_config_status(integration_id, user_id=user_id)
    return status


async def _test_integration(integration_id: str, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Perform active connection test for an integration"""
    try:
        if integration_id == "notion":
            return await _test_notion(user_id=user_id)
        elif integration_id == "slack":
            return await _test_slack(user_id=user_id)
        elif integration_id == "github":
            return await _test_github(user_id=user_id)
        elif integration_id == "calendar":
            return await _test_calendar(user_id=user_id)
        else:
            return {"success": False, "error": f"Unknown integration: {integration_id}"}

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_notion(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Notion API connection using stored API key (Issue #562).

    #1436 B16: get_config requires a principal — the acting user's key when
    present, the "system" marker otherwise (the router:157 convention), same
    as the sibling _test_slack/_test_github helpers.
    """
    try:
        import aiohttp

        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()
        config = config_service.get_config(user_id or "system")
        api_key = config.api_key

        if not api_key:
            return {
                "success": False,
                "error": "Notion not connected. Please add your API key.",
                "error_type": "not_configured",
            }

        # Test with users/me endpoint using stored API key
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.notion.com/v1/users/me",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28",
                },
            ) as response:
                if response.status == 200:
                    return {"success": True}
                if response.status in (401, 403):
                    return {
                        "success": False,
                        "error": "API key invalid or expired",
                        "error_type": "api_key_invalid",
                    }
                # #2151 (#2125 shape): a 5xx or rate limit is a check that couldn't run,
                # never an invalid key.
                return {
                    "success": False,
                    "error": CHECK_FAILED_MESSAGE,
                    "error_type": "check_failed",
                }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_slack(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Slack API connection using stored OAuth token (Issue #562)"""
    try:
        import aiohttp

        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        token = (
            keychain.get_api_key("slack_bot", username=user_id)
            if user_id
            else keychain.get_api_key("slack_bot")
        )  # Issue #849: Correct key name + user-scoped

        if not token:
            return {
                "success": False,
                "error": "Slack not connected. Click Connect to authorize.",
                "error_type": "not_configured",
            }

        # Test with auth.test endpoint using stored OAuth token
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://slack.com/api/auth.test",
                headers={"Authorization": f"Bearer {token}"},
            ) as response:
                data = await response.json()

                if data.get("ok"):
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Token invalid or expired"),
                        "error_type": "token_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


_GITHUB_WORKING_OAUTH = "GitHub is working, using your GitHub connection."
_GITHUB_WORKING_PAT = "GitHub is working, using your personal token."
_GITHUB_WORKING_PAT_STALE_OAUTH = (
    "GitHub is working, using your personal token. "
    "Your GitHub connection needs re-authorizing, so I'm not using it right now."
)


def _github_success_line(credential) -> str:
    """CXO's Test-button lines (2026-10-14): name the serving leg; never a plain green
    when only the fallback leg works and the OAuth grant is stale (B3)."""
    if getattr(credential, "leg", None) == "pat":
        if getattr(credential, "stale_oauth_reason", None) is not None:
            return _GITHUB_WORKING_PAT_STALE_OAUTH
        return _GITHUB_WORKING_PAT
    return _GITHUB_WORKING_OAUTH


def _github_failure(degradation) -> Dict[str, Any]:
    """A connector degrade → the Test result; ``error_type`` is the taxonomy value the
    registry's guidance table maps to a message and a fix."""
    from services.mcp.consumer.connector import DegradationReason

    reason = getattr(degradation, "reason", None)
    return {
        "success": False,
        "error": getattr(degradation, "user_message", "") or "GitHub is not reachable.",
        "error_type": reason.value
        if isinstance(reason, DegradationReason)
        else "connection_failed",
    }


async def _test_github(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test GitHub connection (Issue #562; reshaped for #2012, Arch's Amendment B).

    ONE probe through the adapter for both legs: ``resolve_credential`` picks the leg
    exactly as the reads do (a BOUND binding's grant, else the user's own PAT from
    ``user_api_keys`` then the keychain; never a global token), then one real
    authenticated read (``search_user_repositories``, limit 1) says whether GitHub
    answers. The result names the serving leg and surfaces a stale OAuth grant that a
    working PAT is covering for (B3). A BOUND row alone is not "connected" (a revoked
    grant leaves the row in place; xian, alpha, 2026-10-14), and a missing user is
    not-configured, never a fallback to a global key.
    """
    if not user_id:
        return {
            "success": False,
            "error": "GitHub not connected. Please add your token.",
            "error_type": "not_configured",
        }
    try:
        from services.mcp.consumer.connector import DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        adapter = GitHubMCPSpatialAdapter()
        credential = await adapter.resolve_credential(user_id)
        if isinstance(credential, DegradationResponse):
            return _github_failure(credential)
        result = await adapter.search_user_repositories(user_id, limit=1)
        if result.degradation is not None:
            return _github_failure(result.degradation)
        stale = getattr(credential, "stale_oauth_reason", None)
        return {
            "success": True,
            "message": _github_success_line(credential),
            "leg": getattr(credential, "leg", None),
            "stale_oauth_reason": getattr(stale, "value", stale),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}


async def _test_calendar(user_id: Optional[str] = None) -> Dict[str, Any]:
    """Test Google Calendar OAuth connection (Issue #539)"""
    try:
        from services.infrastructure.keychain_service import KeychainService, SecretProvenance
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        keychain = KeychainService()
        # Issue #839: Use user-scoped key when user_id available
        key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
        # #2151 (route group 1): read with provenance; a store that failed to answer is a
        # check that couldn't run, never "not connected".
        read = await keychain.aread_secret(key_name)
        if read.provenance is SecretProvenance.STORE_FAILED:
            return {"success": False, "error": CHECK_FAILED_MESSAGE, "error_type": "check_failed"}
        refresh_token = read.value if read.is_present else None

        if not refresh_token:
            return {
                "success": False,
                "error": "Calendar not connected. Click Connect to authorize.",
                "error_type": "not_configured",
            }

        # Validate by attempting to refresh the token (Issue #539)
        handler = GoogleCalendarOAuthHandler()
        tokens = await handler.refresh_access_token(refresh_token)

        if not tokens:
            if getattr(handler, "last_refresh_error", None) != "revoked":
                # #2151 (#2125 shape): Google didn't answer (a 5xx, an unexpected status);
                # the check couldn't run, so never "revoked".
                return {
                    "success": False,
                    "error": CHECK_FAILED_MESSAGE,
                    "error_type": "check_failed",
                }
            return {
                "success": False,
                "error": "Token expired or revoked. Please reconnect.",
                "error_type": "token_invalid",
            }

        # #2092: a refresh succeeds with ANY scope; only a real read shows the grant
        # can see the calendar (xian's 10-19 grant was email-only and read "Healthy").
        from services.integrations.calendar.oauth_handler import probe_calendar_read

        read_error = await probe_calendar_read(tokens.access_token)
        if read_error == "insufficient_scope":
            return {
                "success": False,
                "error": (
                    "Google refused the calendar read: the connection doesn't include "
                    "calendar access. Disconnect, connect again, and approve calendar access."
                ),
                "error_type": "insufficient_scope",
            }
        if read_error == "api_not_enabled":
            # CXO's words (2026-10-21 10:21).
            return {
                "success": False,
                "error": (
                    "Google refused the calendar read: the Calendar service isn't switched on "
                    "for this app yet. That's a setup step on our side. Reconnecting won't help."
                ),
                "error_type": "api_not_enabled",
            }
        if read_error == "error":
            # CXO (2026-10-21): the unclassified refusal must not promise that
            # reconnecting fixes it; the cause may be ours.
            return {
                "success": False,
                "error": (
                    "Google refused the calendar read, and I couldn't tell why. "
                    "Reconnecting may help. If it doesn't, tell us."
                ),
                "error_type": "error",
            }
        if read_error is not None:
            return {
                "success": False,
                "error": f"Google refused the calendar read ({read_error}). Reconnect and try again.",
                "error_type": read_error,
            }
        return {"success": True}

    except ImportError:
        return {"success": False, "error": "Calendar integration not available"}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
