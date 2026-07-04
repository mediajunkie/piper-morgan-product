"""#1231 (WS-4) — GitHub honest-degrade: no silent {}, carry DegradationReason, derive
copy from the shared policy (Arch-ratified 2026-07-01).

When GitHub is not-configured/not-connected, the metadata-enrichment functions carry a
`DegradationReason` (not a bespoke string, not a silent {}); the formatter/handler surface
a "connect me" nudge from the one shared reason→copy policy. NOT_CONFIGURED (onboard gap)
and CONNECT_REQUIRED (reconnect gap) are distinct reasons with distinct copy.
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.degradation_copy import _NUDGES, degrade_nudge
from services.mcp.consumer.connector import DegradationReason


@pytest.fixture
def handlers():
    return CanonicalHandlers()


# ---- priority-metadata: carries DegradationReason ----


@pytest.mark.asyncio
async def test_priority_metadata_not_configured_is_not_configured_reason(handlers):
    with patch("services.integrations.github.config_service.GitHubConfigService") as CS:
        CS.return_value.is_configured.return_value = False
        md = await handlers._get_priority_metadata(user_id="u1")
    assert md == {"degrade_reason": DegradationReason.NOT_CONFIGURED}  # onboard gap


@pytest.mark.asyncio
async def test_priority_metadata_not_connected_is_connect_required_reason(handlers):
    with (
        patch("services.integrations.github.config_service.GitHubConfigService") as CS,
        patch("services.domain.github_domain_service.GitHubDomainService") as DS,
    ):
        CS.return_value.is_configured.return_value = True
        DS.return_value.get_connection_status.return_value = {"connected": False}
        md = await handlers._get_priority_metadata(user_id="u1")
    assert md == {"degrade_reason": DegradationReason.CONNECT_REQUIRED}  # reconnect gap


def test_detailed_priorities_surfaces_nudge_from_reason(handlers):
    uc = MagicMock(organization=None)
    out = handlers._format_detailed_priorities(
        ["Ship beta"], uc, {"degrade_reason": DegradationReason.NOT_CONFIGURED}
    )
    assert "connect" in out.lower()  # honest nudge, not silent
    assert "Ship beta" in out


def test_detailed_priorities_silent_without_reason(handlers):
    uc = MagicMock(organization=None)
    out = handlers._format_detailed_priorities(["Ship beta"], uc, {})
    assert "connect it" not in out.lower()


# ---- project-metadata: carries DegradationReason via sentinel key ----


@pytest.mark.asyncio
async def test_project_metadata_not_configured_reason(handlers):
    with patch("services.intent_service.canonical_handlers.get_plugin_registry") as reg:
        plugin = MagicMock()
        plugin.is_configured.return_value = False
        reg.return_value.get_plugin.return_value = plugin
        md = await handlers._get_project_metadata(["Proj A"])
    assert md == {"__degrade_reason__": DegradationReason.NOT_CONFIGURED}


@pytest.mark.asyncio
async def test_project_metadata_not_connected_reason(handlers):
    with (
        patch("services.intent_service.canonical_handlers.get_plugin_registry") as reg,
        patch("services.domain.github_domain_service.GitHubDomainService") as DS,
    ):
        plugin = MagicMock()
        plugin.is_configured.return_value = True
        reg.return_value.get_plugin.return_value = plugin
        DS.return_value.get_connection_status.return_value = {"connected": False}
        md = await handlers._get_project_metadata(["Proj A"])
    assert md == {"__degrade_reason__": DegradationReason.CONNECT_REQUIRED}


def test_degrade_nudge_helper_surfaces_on_reason_else_silent(handlers):
    assert "connect" in handlers._degrade_nudge(
        {"__degrade_reason__": DegradationReason.CONNECT_REQUIRED}
    ).lower()
    assert handlers._degrade_nudge({}) == ""
    assert handlers._degrade_nudge({"MyProj": {"has_github": True}}) == ""


# ---- the shared reason→copy policy ----


def test_policy_distinguishes_onboard_from_reconnect():
    """The whole point of the NOT_CONFIGURED enum-add (Arch): onboard vs reconnect get
    DIFFERENT copy, not one collapsed message."""
    onboard = degrade_nudge(DegradationReason.NOT_CONFIGURED)
    reconnect = degrade_nudge(DegradationReason.CONNECT_REQUIRED)
    assert onboard and reconnect
    assert onboard != reconnect
    assert "set up" in onboard.lower()  # onboard framing
    assert "connected" in reconnect.lower()  # reconnect framing


def test_policy_is_connector_parameterized():
    assert "Calendar" in degrade_nudge(DegradationReason.CONNECT_REQUIRED, connector="Calendar")
    assert "GitHub" in degrade_nudge(DegradationReason.CONNECT_REQUIRED)  # default


def test_policy_unknown_reason_is_empty():
    assert degrade_nudge(None) == ""


def test_every_degradation_reason_has_nudge_copy():
    """Completeness guard (Arch/HOST, 2026-07-03): a DegradationReason with no _NUDGES
    entry silently produces no nudge (honest but useless). Mirrors #1308's derive-don't-
    list shape — a future reason with missing copy fails the build instead of shipping
    silent-empty."""
    missing = [r for r in DegradationReason if r not in _NUDGES]
    assert not missing, f"DegradationReason members with no nudge copy: {missing}"
