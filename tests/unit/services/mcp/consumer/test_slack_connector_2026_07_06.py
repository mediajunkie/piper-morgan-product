"""Slack's #1232 Connector-contract port (task #98, following Arch's 2026-07-04
3-layer ruling + the notion_adapter.py reference port).

Covers `services/mcp/consumer/slack_adapter.py`'s 4 contract methods
(connect/status/resolve/degrade) — keychain-backed (Layer 2), not binding-table
backed, per Arch's ruling that a keychain grant store is a legitimate Layer-2
backend, not a contract exception. Unlike Notion (no default-resource concept),
Slack has a real one — the default-channel preference (#693) — so `resolve()`
is exercised against both the "channel set" and "channel unset" cases, not just
an honest not-yet-implemented miss.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

from services.mcp.consumer.connector import (
    Binding,
    ConnectorStatusState,
    ConnectRequired,
    DegradationReason,
    ResolveMiss,
    ResourceHandle,
    ResourceQuery,
)
from services.mcp.consumer.slack_adapter import SlackMCPAdapter

_USER_ID = "22222222-2222-2222-2222-222222222222"


def _adapter_with_config(is_configured: bool) -> SlackMCPAdapter:
    """A SlackMCPAdapter whose injected config_service.is_configured() is
    stubbed, isolating these tests from real keychain/env/PIPER.user.md state."""
    mock_config_service = MagicMock()
    mock_config_service.is_configured.return_value = is_configured
    return SlackMCPAdapter(config_service=mock_config_service)


class TestSlackConnectorContract:
    """The 4 #1232 contract methods, keychain-backed (Layer 2)."""

    async def test_connect_configured_returns_binding(self):
        adapter = _adapter_with_config(is_configured=True)
        result = await adapter.connect(_USER_ID)
        assert isinstance(result, Binding)
        assert result.binding_id == f"slack-keychain:{_USER_ID}"

    async def test_connect_unconfigured_returns_connect_required(self):
        adapter = _adapter_with_config(is_configured=False)
        result = await adapter.connect(_USER_ID)
        assert isinstance(result, ConnectRequired)
        assert result.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_status_configured_is_bound(self):
        adapter = _adapter_with_config(is_configured=True)
        status = await adapter.status(_USER_ID)
        assert status.state is ConnectorStatusState.BOUND

    async def test_status_unconfigured_is_unbound(self):
        adapter = _adapter_with_config(is_configured=False)
        status = await adapter.status(_USER_ID)
        assert status.state is ConnectorStatusState.UNBOUND

    async def test_resolve_unconfigured_is_connect_required_miss(self):
        adapter = _adapter_with_config(is_configured=False)
        result = await adapter.resolve(_USER_ID, ResourceQuery(kind="channel"))
        assert isinstance(result, ResolveMiss)
        assert result.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_resolve_non_channel_kind_is_resource_not_found_miss(self):
        """No Slack resource kind other than 'channel' exists yet — an honest
        miss, not a fabricated success."""
        adapter = _adapter_with_config(is_configured=True)
        result = await adapter.resolve(_USER_ID, ResourceQuery(kind="database"))
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
            assert response.user_message != "The Slack connector is degraded."

    async def test_degrade_unknown_reason_falls_back_gracefully(self):
        adapter = _adapter_with_config(is_configured=True)
        response = await adapter.degrade(DegradationReason.REPO_UNRESOLVED)
        assert response.user_message == "The Slack connector is degraded."


class TestSlackResolveChannelPreference:
    """`resolve(kind="channel")` — Slack's real default-resource concept (#693),
    unlike Notion's honest not-yet-implemented miss. Patches the true import
    origin (`services.domain.user_preference_manager.UserPreferenceManager`),
    not the local-import call site — mirrors the personalization_service.py
    patching lesson from #1366 (patching the call-site module attribute fails
    since the import is local to the method, not module-level)."""

    async def test_channel_preference_set_returns_resource_handle(self):
        adapter = _adapter_with_config(is_configured=True)
        mock_instance = MagicMock()
        mock_instance.get_slack_default_channel = AsyncMock(return_value="#standups")
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_instance,
        ):
            result = await adapter.resolve(_USER_ID, ResourceQuery(kind="channel"))
        assert isinstance(result, ResourceHandle)
        assert result.handle == "#standups"
        assert result.kind == "channel"
        mock_instance.get_slack_default_channel.assert_awaited_once_with(UUID(_USER_ID))

    async def test_channel_preference_unset_returns_resource_not_found_miss(self):
        adapter = _adapter_with_config(is_configured=True)
        mock_instance = MagicMock()
        mock_instance.get_slack_default_channel = AsyncMock(return_value=None)
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_instance,
        ):
            result = await adapter.resolve(_USER_ID, ResourceQuery(kind="channel"))
        assert isinstance(result, ResolveMiss)
        assert result.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND

    async def test_channel_preference_lookup_failure_degrades_to_unreachable(self):
        """Never raise, never silently empty — a preference-lookup failure is
        the closest existing DegradationReason to 'our own backend hiccuped',
        not a user-facing CONNECT_REQUIRED/RESOURCE_NOT_FOUND."""
        adapter = _adapter_with_config(is_configured=True)
        mock_instance = MagicMock()
        mock_instance.get_slack_default_channel = AsyncMock(side_effect=RuntimeError("db down"))
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_instance,
        ):
            result = await adapter.resolve(_USER_ID, ResourceQuery(kind="channel"))
        assert isinstance(result, ResolveMiss)
        assert result.degradation.reason is DegradationReason.UNREACHABLE


class TestSlackAdapterDefaultConstruction:
    """No injected config_service — the real SlackConfigService is used
    (mirrors NotionMCPAdapter()'s default-construction path)."""

    def test_constructs_with_real_config_service(self):
        adapter = SlackMCPAdapter()
        assert adapter.config_service is not None
        assert adapter.system_name == "slack"


class TestSlackAdapterSatisfiesRuntimeConnectorProtocol:
    def test_isinstance_of_connector_protocol(self):
        from services.mcp.consumer.connector import Connector

        assert isinstance(SlackMCPAdapter(), Connector)
