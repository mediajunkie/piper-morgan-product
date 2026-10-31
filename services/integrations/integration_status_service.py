"""Canonical integration status service (#1547).

ONE source of truth for "is integration X connected for user U?".

Why this exists (status-truth audit, docs/internal/operations/
status-truth-audit-2026-08-09.md): all four real plugins hardcode
``is_configured() -> False`` (#784 — the plugin interface has no user, and
integration truth is user-scoped), so every registry status-dict
consumer reported real integrations never-connected — while the env-fed Demo
plugin was the only one that could ever appear connected. Chat guidance (#1534),
the conversational floor, standup/Radar, and four public ``/status`` endpoints
all lied in the same direction.

The composition below is hoisted EXACTLY from the already-correct
``GET /api/v1/integrations/health`` internals (web/api/routes/integrations.py):

- ``github_oauth_bound`` — binding-FIRST github check (#1329 / ADR-070 C): a
  BOUND OAuth connector means connected, regardless of PAT/env state.
- ``get_config_status`` — per-integration user-scoped store checks: github
  user-scoped keychain PAT (#1513), slack keychain bot token (ADR-058), notion
  #358 user-secret store (#1337), calendar user-scoped keychain key (#839),
  each behind its env-var fast path.
- The caller's own Test result (``healthy`` / ``last_check``), keyed by
  ``(principal, integration)`` in ``principal_test_results`` (#2071; before
  that it was one host-wide entry per integration).

The web route now delegates its decision primitives here (thin consumer); chat /
floor / standup / Radar surfaces read this service instead of the registry.

Demo is STRUCTURALLY excluded: ``KNOWN_INTEGRATIONS`` is the user-facing set,
and asking for anything else raises — no downstream filtering required.
"""

import asyncio
import os
from typing import Any, Dict, Optional, Tuple

import structlog

from services.integrations.principal_test_results import get_test_result_store

# #2072: binding states, by value, so this module does not import the connector enum at
# module import time (it is imported lazily inside the DB-touching helpers).
_BOUND = "bound"
_BROKEN_BINDING_STATES = frozenset({"stale", "unreachable"})

logger = structlog.get_logger()

#: The user-facing integration set. Demo (a loadable plugin, not a user-facing
#: integration — audit F9) is structurally excluded by not being here.
KNOWN_INTEGRATIONS: Tuple[str, ...] = ("github", "slack", "calendar", "notion")

#: Proper display names for user-facing copy (``"github".title()`` yields
#: "Github", which is wrong in prose).
DISPLAY_NAMES: Dict[str, str] = {
    "github": "GitHub",
    "slack": "Slack",
    "calendar": "Google Calendar",
    "notion": "Notion",
}


#: #2151 ISS-STATUS: the binding check itself raised (distinct from "no binding").
#: Neither ``bound`` nor broken, so ``github_oauth_bound`` and
#: ``github_needs_reconnecting`` read it as False, as they read None.
#: The connectors Piper reads in chat and the beta letter offers (CXO 2026-10-30; Slack
#: descoped 08-27). Keyed as the status/health payload names them. The Integrations
#: page's own JS lists (templates/integrations.html:430-433, OAUTH_INTEGRATIONS /
#: API_KEY_INTEGRATIONS) move onto this constant under a follow-up issue.
BETA_OFFERED_CONNECTORS: Dict[str, str] = {"github": "GitHub", "calendar": "Google Calendar"}

BINDING_CHECK_FAILED = "check_failed"

#: ``via`` for a GitHub binding GitHub has rejected (#2072): configured, and broken.
VIA_OAUTH_BINDING_STALE = "oauth_binding_stale"


def needs_reconnecting(status: Dict[str, Any]) -> bool:
    """True when a ``get_status`` dict is a connection that exists but GitHub rejected.

    #2072 follow-up (Arch's ruling, issuecomment-6234453553): ``configured`` means a
    connection EXISTS, not that it works. Gates read ``configured`` (the read runs and
    discloses STALE_TOKEN). A surface that CLAIMS a working connection ("connected",
    "active", ``valid: True``) must also ask this, and render a True here as #2029's
    "Needs reconnecting", never as connected.
    """
    return bool(status.get("configured")) and status.get("via") == VIA_OAUTH_BINDING_STALE


async def github_oauth_binding_state(user_id: Optional[str]) -> Optional[str]:
    """The user's github OAuth-connector binding state (``ConnectorStatusState`` value),
    or None when there is no binding or the check itself failed (#2072).

    ``bound`` is connected and healthy. ``stale`` is a binding GitHub has rejected
    (#2029 writes it on a 401): the connection EXISTS and is BROKEN, which the status
    surfaces must say, never "not configured". ``unreachable`` likewise.
    """
    if not user_id:
        return None
    try:
        from services.connectors.binding_repository import ConnectorBindingRepository
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, "github")
        return None if binding is None else str(binding.status)
    except Exception as e:
        logger.warning("github oauth-binding status check failed", error=str(e))
        return BINDING_CHECK_FAILED  # #2151: not "no binding"


async def github_needs_reconnecting(user_id: Optional[str]) -> bool:
    """``needs_reconnecting(await IntegrationStatusService().get_status(user_id, "github"))``
    without the credential-path reads (#2076).

    ``get_status`` sets ``via == VIA_OAUTH_BINDING_STALE`` (always with ``configured``)
    exactly when the binding state is in ``_BROKEN_BINDING_STATES``, and on no other
    branch, so this binding-state read is the same answer with no env/keychain probe.
    False when there is no user, no binding, or the check itself failed (the reply then
    stays as it was: never claim a broken connection the read could not see).
    """
    return (await github_oauth_binding_state(user_id)) in _BROKEN_BINDING_STATES


async def github_oauth_bound(user_id: Optional[str]) -> bool:
    """True if the user has a BOUND github OAuth-connector binding (#1329 / ADR-070 C).

    GitHub health follows the OAuth connector after the #1322 cutover, not the legacy
    native PAT — so a dead/expired PAT must NOT make GitHub read as unhealthy when the
    connector is bound and the chat reads work through it. Mirrors the binding check in
    ``GET /github/oauth-status``. (Hoisted verbatim from web/api/routes/integrations.py.)
    """
    from services.mcp.consumer.connector import ConnectorStatusState

    return (await github_oauth_binding_state(user_id)) == ConnectorStatusState.BOUND.value


async def _keychain_has(provider: str, username: Optional[str] = None) -> bool:
    """#2151 ISS-STATUS (route group 1): a keychain read that says WHY. ``get_api_key``
    returns None for "absent" and for "the store failed" alike, so a failed lookup read as
    "Not configured"; ``read_secret`` tells them apart, and a failed store RAISES here (the
    caller marks the lookup failed)."""
    from services.infrastructure.keychain_service import KeychainService, SecretProvenance

    read = await KeychainService().aread_secret(provider, username)
    if read.provenance is SecretProvenance.STORE_FAILED:
        raise RuntimeError(read.error or f"{provider} credential store failed")
    return read.is_present


async def get_config_status(
    integration_id: str, user_id: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """Check whether an integration is configured, and via which credential path.

    Returns ``(status, via)`` where ``status`` is ``"configured"`` /
    ``"not_configured"`` / ``"unknown"`` (check itself failed) and ``via`` is
    ``"env"`` / ``"keychain"`` / ``"user_secret_store"`` / ``None``.

    Hoisted from ``_get_integration_config_status`` in
    web/api/routes/integrations.py (the #1513/#1337/#839 composition), extended
    only to report WHICH path matched.

    #2151 ISS-STATUS (Arch 10-23): a user-scoped lookup that RAISED makes the
    answer ``"unknown"``, never ``"not_configured"``: a check that couldn't run
    is not a verified absence.
    """
    lookup_failed = False
    try:
        if integration_id == "notion":
            if os.environ.get("NOTION_API_TOKEN") or os.environ.get("NOTION_API_KEY"):
                return "configured", "env"
            # #1337: user-scoped path. save_notion_key stores the key in the #358
            # user-secret store (UserAPIKeyService, provider "notion") — NOT the keychain
            # that slack/calendar use.
            if user_id:
                try:
                    from services.database.session_factory import AsyncSessionFactory
                    from services.security.user_api_key_service import UserAPIKeyService

                    async with AsyncSessionFactory.session_scope_fresh() as session:
                        if await UserAPIKeyService().retrieve_user_key(session, user_id, "notion"):
                            return "configured", "user_secret_store"
                except Exception as e:
                    lookup_failed = (
                        True  # #2151 ISS-STATUS: a failed lookup is not "not configured"
                    )
                    logger.warning(f"{integration_id} credential lookup failed", error=str(e))
        elif integration_id == "slack":
            # Env-var path (production / explicit-config deployment)
            if os.environ.get("SLACK_BOT_TOKEN"):
                return "configured", "env"
            # Keychain path (OAuth-completed deployment per ADR-058 — bot token
            # stored under user-scoped keychain key after a successful OAuth callback).
            if user_id:
                try:
                    if await _keychain_has("slack_bot", username=user_id):
                        return "configured", "keychain"
                except Exception as e:
                    lookup_failed = (
                        True  # #2151 ISS-STATUS: a failed lookup is not "not configured"
                    )
                    logger.warning(f"{integration_id} credential lookup failed", error=str(e))
        elif integration_id == "github":
            # ADR-081 D1 / Amendment B4 (Arch 10-24): a user's GitHub status derives from the
            # connector resolver's own PAT legs (the binding is read first, in get_status), never
            # from the deployment's env. The env counts only for a principal-less local call.
            if not user_id:
                from services.integrations.github.config_service import GitHubConfigService

                # The one local-only helper (ADR-081 D2): None on a hosted deploy.
                if await asyncio.to_thread(
                    GitHubConfigService().get_authentication_token, "system"
                ):
                    return "configured", "env"
            if user_id:
                try:
                    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

                    # #1966: the one PAT read, both legs in the resolver's order.
                    if await GitHubMCPSpatialAdapter.account_pat(user_id):
                        return "configured", "keychain"
                except Exception as e:
                    lookup_failed = (
                        True  # #2151 ISS-STATUS: a failed lookup is not "not configured"
                    )
                    logger.warning(f"{integration_id} credential lookup failed", error=str(e))
        elif integration_id == "calendar":
            # Calendar uses keychain token (Issue #529) or legacy MCP/credentials
            # Issue #839: Use user-scoped key when user_id available
            try:
                key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
                if await _keychain_has(key_name):
                    return "configured", "keychain"
            except Exception as e:
                lookup_failed = True  # #2151 ISS-STATUS
                logger.warning("calendar credential lookup failed", error=str(e))
            # Fallback to legacy check
            if os.environ.get("GOOGLE_CALENDAR_CREDENTIALS") or os.environ.get("MCP_ENABLED"):
                return "configured", "env"

        if lookup_failed:
            return "unknown", None
        return "not_configured", None

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} config", error=str(e))
        return "unknown", None


class IntegrationStatusService:
    """The canonical status source. Stateless; construct freely.

    ``get_status`` / ``get_all`` return per-integration dicts:
    ``{"configured": bool, "check_failed": bool, "via": Optional[str], "healthy": Optional[bool],
    "last_check": Optional[str]}`` where ``via`` is one of ``"oauth_binding"`` /
    ``"keychain"`` / ``"user_secret_store"`` / ``"env"`` and ``healthy`` is
    tri-state (None = no cached active-test result — m-44: absence of a check is
    not a clear).
    """

    KNOWN = KNOWN_INTEGRATIONS

    async def get_status(self, user_id: Optional[str], integration_id: str) -> Dict[str, Any]:
        if integration_id not in self.KNOWN:
            raise ValueError(
                f"Unknown user-facing integration: {integration_id!r} "
                f"(known: {', '.join(self.KNOWN)})"
            )

        configured = False
        via: Optional[str] = None
        check_failed = False

        # RECONNECT (#1329): GitHub follows the OAuth connector binding FIRST —
        # a BOUND connector is connected even if the legacy PAT is dead/absent.
        # #2072: a STALE (or UNREACHABLE) binding is a connection that EXISTS and is
        # BROKEN: configured, via "oauth_binding_stale", healthy False. Reading it as
        # "not configured" made the radar/standup gate skip the read silently, so a
        # revoked grant was never disclosed once #2029 had marked the binding STALE
        # (xian's A1 run on d741214b6c, 2026-10-16: ``degraded []``).
        github_state: Optional[str] = None
        if integration_id == "github":
            github_state = await github_oauth_binding_state(user_id)
        if github_state == _BOUND:
            configured, via = True, "oauth_binding"
        elif github_state in _BROKEN_BINDING_STATES:
            configured, via = True, VIA_OAUTH_BINDING_STALE
        else:
            status, via = await get_config_status(integration_id, user_id=user_id)
            configured = status == "configured"
            # #2151 ISS-STATUS: say "couldn't check", never "not connected", when the
            # check itself failed (the binding read or a credential lookup raised).
            check_failed = not configured and (
                status == "unknown" or github_state == BINDING_CHECK_FAILED
            )

        healthy: Optional[bool] = None
        last_check: Optional[str] = None
        last_error: Optional[str] = None  # #2093: this principal's own failed-check text
        if via == "oauth_binding":
            # Mirrors /health's short-circuit: a BOUND connector reports healthy
            # (the chat reads go through it).
            healthy = True
        elif via == VIA_OAUTH_BINDING_STALE:
            # #2072: GitHub has rejected this grant; the connection is known broken.
            healthy = False
        elif configured:
            # #2071: THIS user's own Test result only. No record for this principal
            # keeps healthy=None and last_check=None (never checked); there is no
            # host-wide entry to fall back to (m-44: absence of a check is not a clear).
            result = get_test_result_store().get_test_result(user_id, integration_id)
            if result is not None:
                healthy = result.ok
                last_check = result.checked_at_iso
                last_error = result.error

        return {
            "configured": configured,
            "check_failed": check_failed,
            "via": via,
            "last_error": last_error,
            "healthy": healthy,
            "last_check": last_check,
        }

    async def get_all(self, user_id: Optional[str]) -> Dict[str, Dict[str, Any]]:
        """Status for the whole user-facing set — demo structurally absent."""
        return {
            integration_id: await self.get_status(user_id, integration_id)
            for integration_id in self.KNOWN
        }

    async def is_configured(self, user_id: Optional[str], integration_id: str) -> bool:
        """Convenience gate for surfaces that only need the boolean (binding-first)."""
        return bool((await self.get_status(user_id, integration_id))["configured"])
