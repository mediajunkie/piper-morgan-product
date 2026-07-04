"""Notion — the #1232 Connector-contract home (ADR-070 D5).

Per Arch's 2026-07-04 3-layer connector-alignment ruling: the #1232 interface
(`connect`/`status`/`resolve`/`degrade`) is Layer 1 — no exceptions. Notion's
credential backend (Layer 2) is the per-user keychain entry `NotionConfigService`
already reads (`keychain.get_api_key("notion", username=user_id)`, ADR-058) — a
keychain-backed connector conforms to the contract the same as a binding-table
one; the credential model is below the interface, not a contract variant.

This module subclasses the legacy `services.integrations.mcp.notion_adapter.
NotionMCPAdapter` (22 existing data-operation methods — get_page, search_notion,
query_database, etc.) rather than duplicating them, and adds ONLY the 4 contract
methods. The legacy module's own `connect(integration_token) -> bool` is left
completely untouched — ~15 live call sites (the NotionIntegrationRouter,
services/publishing/publisher.py, services/domain/notion_domain_service.py,
cli/commands/notion.py, plus manual/debug scripts) depend on that exact
signature today, and renaming it was a materially larger, riskier change than
what this pass scoped (Arch's own framing — "the smaller migration... mostly
the connect signature + return type" — undersold the live-caller blast radius
once actually checked; narrowing scope here rather than a wide risky rename).

Mirrors the GitBook precedent in Arch's same ruling: "one canonical adapter
per connector, on the #1232 protocol, in services/mcp/consumer/... the
integrations/mcp/ location is legacy." Retiring the legacy module (moving its
22 methods here, updating callers) is future work, not attempted in this pass.
"""

from __future__ import annotations

import logging

from services.integrations.mcp.notion_adapter import NotionMCPAdapter as _LegacyNotionMCPAdapter
from services.integrations.notion.config_service import NotionConfigService

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
    ResourceQuery,
)

logger = logging.getLogger(__name__)


class NotionMCPAdapter(_LegacyNotionMCPAdapter):
    """The #1232-conformant Notion connector — legacy 22 methods inherited unchanged,
    the 4 contract methods added on top. See module docstring for the full rationale."""

    # #1232: AST-guard enforces the 4 methods on declared conformers.
    IMPLEMENTS_CONNECTOR = True

    async def connect(self, user_id: str) -> ConnectResult:
        """Bound already (keychain has a Notion API key for this user) -> Binding;
        otherwise the must-be-handled ConnectRequired. Notion's credential backend
        is keychain (ADR-058), not the connector_bindings table -- the Binding here
        is a pointer to that keychain grant (Arch's Layer-2 ruling: keychain is
        just another encrypted grant store, not a contract variant)."""
        config_service = self.config_service or NotionConfigService()
        if config_service.is_configured(user_id):
            return Binding(binding_id=f"notion-keychain:{user_id}")
        return ConnectRequired(degradation=await self.degrade(DegradationReason.CONNECT_REQUIRED))

    async def status(self, user_id: str) -> ConnectorStatus:
        """The user's Notion connection health -- keychain-backed, no separate
        binding row to query (D3/D5: health without a resource fetch or token)."""
        config_service = self.config_service or NotionConfigService()
        if config_service.is_configured(user_id):
            return ConnectorStatus(state=ConnectorStatusState.BOUND, detail="Notion API key configured.")
        return ConnectorStatus(
            state=ConnectorStatusState.UNBOUND,
            detail="No Notion API key configured -- connect to continue.",
        )

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult:
        """Notion has no per-user default-resource concept yet (no analog to
        GitHub's default_repo preference) -- honest RESOURCE_NOT_FOUND rather than
        inventing selection semantics that don't exist anywhere in the codebase
        today (checked: no default-database/default-page concept found). Revisit
        if/when a default-database preference is added."""
        config_service = self.config_service or NotionConfigService()
        if not config_service.is_configured(user_id):
            return ResolveMiss(await self.degrade(DegradationReason.CONNECT_REQUIRED))
        return ResolveMiss(await self.degrade(DegradationReason.RESOURCE_NOT_FOUND))

    async def degrade(self, reason: DegradationReason) -> DegradationResponse:
        messages = {
            DegradationReason.CONNECT_REQUIRED: "Connect Notion to continue.",
            DegradationReason.RESOURCE_NOT_FOUND: "That Notion resource wasn't found.",
            DegradationReason.UNREACHABLE: "Notion is unreachable right now.",
            DegradationReason.STALE_TOKEN: "Your Notion connection needs re-authorizing.",
        }
        return DegradationResponse(
            reason=reason, user_message=messages.get(reason, "The Notion connector is degraded.")
        )
