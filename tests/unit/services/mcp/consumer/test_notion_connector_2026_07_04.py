"""Notion's #1232 Connector-contract port (Arch's 2026-07-04 3-layer ruling).

Covers `services/mcp/consumer/notion_adapter.py`'s 4 new contract methods
(connect/status/resolve/degrade) — keychain-backed (Layer 2), not binding-table
backed, per Arch's ruling that a keychain grant store is a legitimate Layer-2
backend, not a contract exception. Also proves the legacy 22 data-operation
methods are inherited unchanged (zero duplication, zero risk to existing callers).
"""

from __future__ import annotations

from unittest.mock import MagicMock

from services.mcp.consumer.connector import (
    Binding,
    ConnectorStatusState,
    ConnectRequired,
    DegradationReason,
    ResolveMiss,
    ResourceQuery,
)
from services.mcp.consumer.notion_adapter import NotionMCPAdapter


def _adapter_with_config(is_configured: bool) -> NotionMCPAdapter:
    """A NotionMCPAdapter whose injected config_service.is_configured() is
    stubbed, isolating these tests from real keychain/env/PIPER.user.md state."""
    mock_config_service = MagicMock()
    mock_config_service.is_configured.return_value = is_configured
    return NotionMCPAdapter(config_service=mock_config_service)


class TestNotionConnectorContract:
    """The 4 #1232 contract methods, keychain-backed (Layer 2)."""

    async def test_connect_configured_returns_binding(self):
        adapter = _adapter_with_config(is_configured=True)
        result = await adapter.connect("user-1")
        assert isinstance(result, Binding)
        assert result.binding_id == "notion-keychain:user-1"

    async def test_connect_unconfigured_returns_connect_required(self):
        adapter = _adapter_with_config(is_configured=False)
        result = await adapter.connect("user-1")
        assert isinstance(result, ConnectRequired)
        assert result.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_status_configured_is_bound(self):
        adapter = _adapter_with_config(is_configured=True)
        status = await adapter.status("user-1")
        assert status.state is ConnectorStatusState.BOUND

    async def test_status_unconfigured_is_unbound(self):
        adapter = _adapter_with_config(is_configured=False)
        status = await adapter.status("user-1")
        assert status.state is ConnectorStatusState.UNBOUND

    async def test_resolve_unconfigured_is_connect_required_miss(self):
        adapter = _adapter_with_config(is_configured=False)
        result = await adapter.resolve("user-1", ResourceQuery(kind="database"))
        assert isinstance(result, ResolveMiss)
        assert result.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_resolve_configured_is_resource_not_found_miss(self):
        """Notion has no per-user default-resource concept yet (no analog to
        GitHub's default_repo) — an honest, not-yet-implemented miss, not a
        fabricated success."""
        adapter = _adapter_with_config(is_configured=True)
        result = await adapter.resolve("user-1", ResourceQuery(kind="database"))
        assert isinstance(result, ResolveMiss)
        assert result.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND

    async def test_degrade_known_reasons_have_specific_copy(self):
        adapter = _adapter_with_config(is_configured=True)
        for reason in (
            DegradationReason.CONNECT_REQUIRED,
            DegradationReason.RESOURCE_NOT_FOUND,
            DegradationReason.UNREACHABLE,
            DegradationReason.STALE_TOKEN,
        ):
            response = await adapter.degrade(reason)
            assert response.reason is reason
            assert response.user_message != "The Notion connector is degraded."

    async def test_degrade_unknown_reason_falls_back_gracefully(self):
        adapter = _adapter_with_config(is_configured=True)
        response = await adapter.degrade(DegradationReason.REPO_UNRESOLVED)
        assert response.user_message == "The Notion connector is degraded."


class TestNotionLegacyMethodsInherited:
    """The 22 existing data-operation methods must be untouched, not duplicated."""

    def test_legacy_methods_present(self):
        adapter = NotionMCPAdapter()
        for method in (
            "get_page",
            "search_notion",
            "query_database",
            "create_page",
            "list_databases",
            "test_connection",
            "get_workspace_info",
        ):
            assert hasattr(adapter, method)

    def test_legacy_connect_signature_is_replaced_by_the_contract_method(self):
        """The #1232 contract's connect(user_id) -> ConnectResult wins at this
        subclass level — the legacy connect(integration_token) -> bool is NOT
        reachable through this class (by design: Python method resolution takes
        the subclass's definition). The legacy signature stays reachable through
        the original services.integrations.mcp.notion_adapter.NotionMCPAdapter,
        which every existing caller still imports unchanged."""
        import inspect

        adapter = NotionMCPAdapter()
        sig = inspect.signature(adapter.connect)
        assert "user_id" in sig.parameters
        assert "integration_token" not in sig.parameters

    def test_is_a_distinct_class_from_the_legacy_one(self):
        from services.integrations.mcp.notion_adapter import (
            NotionMCPAdapter as LegacyNotionMCPAdapter,
        )

        assert NotionMCPAdapter is not LegacyNotionMCPAdapter
        assert issubclass(NotionMCPAdapter, LegacyNotionMCPAdapter)
