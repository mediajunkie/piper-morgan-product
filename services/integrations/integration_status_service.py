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
- ``IntegrationHealthMonitor`` cached results — ``healthy`` / ``last_check``.

The web route now delegates its decision primitives here (thin consumer); chat /
floor / standup / Radar surfaces read this service instead of the registry.

Demo is STRUCTURALLY excluded: ``KNOWN_INTEGRATIONS`` is the user-facing set,
and asking for anything else raises — no downstream filtering required.
"""

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

import structlog

from services.health.integration_health_monitor import (
    ComponentStatus,
    IntegrationHealthMonitor,
)

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

# Module-level health monitor singleton — moved here from
# web/api/routes/integrations.py so service consumers and the /test/* routes
# share ONE cache of active-test results.
_health_monitor: Optional[IntegrationHealthMonitor] = None


def get_health_monitor() -> IntegrationHealthMonitor:
    """Get or create the shared health monitor singleton."""
    global _health_monitor
    if _health_monitor is None:
        _health_monitor = IntegrationHealthMonitor()
        for integration_id in KNOWN_INTEGRATIONS:
            _health_monitor.register_component(integration_id, ComponentStatus.UNKNOWN)
    return _health_monitor


async def github_oauth_bound(user_id: Optional[str]) -> bool:
    """True if the user has a BOUND github OAuth-connector binding (#1329 / ADR-070 C).

    GitHub health follows the OAuth connector after the #1322 cutover, not the legacy
    native PAT — so a dead/expired PAT must NOT make GitHub read as unhealthy when the
    connector is bound and the chat reads work through it. Mirrors the binding check in
    ``GET /github/oauth-status``. (Hoisted verbatim from web/api/routes/integrations.py.)
    """
    if not user_id:
        return False
    try:
        from services.connectors.binding_repository import ConnectorBindingRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.mcp.consumer.connector import ConnectorStatusState

        async with AsyncSessionFactory.session_scope() as session:
            binding = await ConnectorBindingRepository(session).get(user_id, "github")
        return binding is not None and binding.status == ConnectorStatusState.BOUND.value
    except Exception as e:
        logger.warning("github oauth-binding status check failed", error=str(e))
        return False


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
    """
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
                except Exception:
                    pass
        elif integration_id == "slack":
            # Env-var path (production / explicit-config deployment)
            if os.environ.get("SLACK_BOT_TOKEN"):
                return "configured", "env"
            # Keychain path (OAuth-completed deployment per ADR-058 — bot token
            # stored under user-scoped keychain key after a successful OAuth callback).
            if user_id:
                try:
                    from services.infrastructure.keychain_service import KeychainService

                    keychain = KeychainService()
                    if keychain.get_api_key("slack_bot", username=user_id):
                        return "configured", "keychain"
                except Exception:
                    pass
        elif integration_id == "github":
            if os.environ.get("GITHUB_TOKEN") or os.environ.get("GITHUB_ACCESS_TOKEN"):
                return "configured", "env"
            # #1513: PAT saves store the token user-scoped in the keychain ONLY
            # (the process-env write was restart-volatile and removed in #1507).
            if user_id:
                try:
                    from services.infrastructure.keychain_service import KeychainService

                    if KeychainService().get_api_key("github_token", username=user_id):
                        return "configured", "keychain"
                except Exception:
                    pass
        elif integration_id == "calendar":
            # Calendar uses keychain token (Issue #529) or legacy MCP/credentials
            # Issue #839: Use user-scoped key when user_id available
            try:
                from services.infrastructure.keychain_service import KeychainService

                keychain = KeychainService()
                key_name = f"google_calendar_{user_id}" if user_id else "google_calendar"
                if keychain.get_api_key(key_name):
                    return "configured", "keychain"
            except Exception:
                pass
            # Fallback to legacy check
            if os.environ.get("GOOGLE_CALENDAR_CREDENTIALS") or os.environ.get("MCP_ENABLED"):
                return "configured", "env"

        return "not_configured", None

    except Exception as e:
        logger.warning(f"Failed to check {integration_id} config", error=str(e))
        return "unknown", None


class IntegrationStatusService:
    """The canonical status source. Stateless; construct freely.

    ``get_status`` / ``get_all`` return per-integration dicts:
    ``{"configured": bool, "via": Optional[str], "healthy": Optional[bool],
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

        # RECONNECT (#1329): GitHub follows the OAuth connector binding FIRST —
        # a BOUND connector is connected even if the legacy PAT is dead/absent.
        if integration_id == "github" and await github_oauth_bound(user_id):
            configured, via = True, "oauth_binding"
        else:
            status, via = await get_config_status(integration_id, user_id=user_id)
            configured = status == "configured"

        healthy: Optional[bool] = None
        last_check: Optional[str] = None
        if via == "oauth_binding":
            # Mirrors /health's short-circuit: a BOUND connector reports healthy
            # (the chat reads go through it).
            healthy = True
        elif configured:
            component_health = get_health_monitor().get_component_health(integration_id)
            if component_health and component_health.last_check > 0:
                if component_health.status == ComponentStatus.HEALTHY:
                    healthy = True
                elif component_health.status in (
                    ComponentStatus.DEGRADED,
                    ComponentStatus.FAILED,
                ):
                    healthy = False
                # UNKNOWN keeps healthy=None AND last_check=None:
                # register_component stamps last_check at registration time, so
                # for a never-tested component the timestamp is registration
                # noise, not a check (m-44 — don't report a measurement that
                # never ran).
                if healthy is not None:
                    last_check = datetime.fromtimestamp(
                        component_health.last_check, tz=timezone.utc
                    ).isoformat()

        return {
            "configured": configured,
            "via": via,
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
