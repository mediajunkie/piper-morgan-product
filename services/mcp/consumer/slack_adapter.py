"""Slack — the #1232 Connector-contract home (ADR-070 D5).

⚠️ PARKED WITH ITS MILESTONE — PM ruling 2026-08-30: "ok to park slack."
Held from the Batch-1 spatial disposal (2026-08-29, epic 1698) when the fresh sweep showed this
is NOT committed-theory residue but the 2026-07-06 Connector-contract port (1317 Epic C) —
75%-complete alignment work for a capability PM deliberately deferred (Slack → Fast Follow,
ratified 2026-08-28). In-tree, unwired, neither deleted nor built until Fast Follow picks it up.
Do not dispose without a new PM ruling; do not wire before its milestone.

Per Arch's 2026-07-04 3-layer connector-alignment ruling: the #1232 interface
(`connect`/`status`/`resolve`/`degrade`) is Layer 1 -- no exceptions. Slack's
credential backend (Layer 2) is the per-user keychain entry `SlackConfigService`
already reads (`keychain.get_api_key("slack_bot", username=user_id)`, ADR-058)
-- a keychain-backed connector conforms to the contract the same as a
binding-table one (github_adapter.py / google_calendar_adapter.py); the
credential model is below the interface, not a contract variant.

Unlike Notion's port, this is a standalone adapter rather than a subclass/
consolidation of a pre-existing operations class -- Slack has no single
equivalent to Notion's legacy 22-method class, so there's nothing to
consolidate. Slack's existing operational code (sending messages, reading
channels, spatial-timestamp mapping) stays exactly where it is
(`services/integrations/slack/slack_client.py`, `.../spatial_adapter.py`,
`.../response_handler.py`, etc.), untouched. This class's only job is the
connector contract: bound/unbound status + resource resolution.
"""

from __future__ import annotations

import logging
from typing import Optional
from uuid import UUID

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.spatial_adapter import BaseSpatialAdapter

from .connector import (
    Binding,
    ConnectorStatus,
    ConnectorStatusState,
    ConnectRequired,
    ConnectResult,
    DegradationReason,
    DegradationResponse,
    ResolveMiss,
    ResolveResult,
    ResourceHandle,
    ResourceQuery,
)

logger = logging.getLogger(__name__)


class SlackMCPAdapter(BaseSpatialAdapter):
    """Slack connector-contract adapter (#1232 / ADR-070 D5).

    Credential-check-only -- no message-sending or channel-reading operations
    live here (see module docstring for where those remain).
    """

    def __init__(self, config_service: Optional["SlackConfigService"] = None):
        super().__init__("slack")
        self.config_service = config_service or SlackConfigService()

    # #1232: AST-guard enforces the 4 methods on declared conformers.
    IMPLEMENTS_CONNECTOR = True

    async def connect(self, user_id: str) -> ConnectResult:
        """Bound already (keychain has a Slack bot token for this user) -> Binding;
        otherwise the must-be-handled ConnectRequired. Slack's credential backend
        is keychain (ADR-058), not the connector_bindings table -- the Binding here
        is a pointer to that keychain grant (Arch's Layer-2 ruling: keychain is
        just another encrypted grant store, not a contract variant)."""
        if self.config_service.is_configured(user_id):
            return Binding(binding_id=f"slack-keychain:{user_id}")
        return ConnectRequired(degradation=await self.degrade(DegradationReason.CONNECT_REQUIRED))

    async def status(self, user_id: str) -> ConnectorStatus:
        """The user's Slack connection health -- keychain-backed, no separate
        binding row to query (D3/D5: health without a resource fetch or token)."""
        if self.config_service.is_configured(user_id):
            return ConnectorStatus(
                state=ConnectorStatusState.BOUND, detail="Slack bot token configured."
            )
        return ConnectorStatus(
            state=ConnectorStatusState.UNBOUND,
            detail="No Slack bot token configured -- connect to continue.",
        )

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult:
        """Unlike Notion (no default-resource concept), Slack has a real one:
        the user's default-channel preference (#693,
        `UserPreferenceManager.get_slack_default_channel`), already consumed by
        the standup-workflow skill. `resource.kind == "channel"` resolves to
        that preference; any other kind is an honest RESOURCE_NOT_FOUND -- no
        other Slack resource kind exists yet."""
        if not self.config_service.is_configured(user_id):
            return ResolveMiss(await self.degrade(DegradationReason.CONNECT_REQUIRED))

        if resource.kind == "channel":
            try:
                from services.domain.user_preference_manager import UserPreferenceManager

                channel = await UserPreferenceManager().get_slack_default_channel(UUID(user_id))
            except Exception:
                logger.warning("Slack default-channel lookup failed", exc_info=True)
                return ResolveMiss(await self.degrade(DegradationReason.UNREACHABLE))
            if channel:
                return ResourceHandle(handle=channel, kind="channel")
            return ResolveMiss(await self.degrade(DegradationReason.RESOURCE_NOT_FOUND))

        return ResolveMiss(await self.degrade(DegradationReason.RESOURCE_NOT_FOUND))

    async def degrade(self, reason: DegradationReason) -> DegradationResponse:
        messages = {
            DegradationReason.CONNECT_REQUIRED: "Connect Slack to continue.",
            DegradationReason.RESOURCE_NOT_FOUND: "That Slack resource wasn't found.",
            DegradationReason.UNREACHABLE: "Slack is unreachable right now.",
            DegradationReason.STALE_TOKEN: "Your Slack connection needs re-authorizing.",
        }
        return DegradationResponse(
            reason=reason, user_message=messages.get(reason, "The Slack connector is degraded.")
        )
