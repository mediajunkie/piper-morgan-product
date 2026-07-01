"""#1231 (WS-4) — GitHub honest-degrade for the priority-metadata path (no silent {}).

Before: when GitHub was not-configured / not-connected, `_get_priority_metadata` returned
{} → `_format_detailed_priorities` silently omitted GitHub entirely (the #1226 silent-empty
shape — reads as "nothing there"). Now it returns a `github_unavailable` marker → the
formatter surfaces a "connect me" nudge instead of nothing.
"""

from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers


@pytest.fixture
def handlers():
    return CanonicalHandlers()


@pytest.mark.asyncio
async def test_priority_metadata_not_configured_signals_degrade(handlers):
    with patch("services.integrations.github.config_service.GitHubConfigService") as CS:
        CS.return_value.is_configured.return_value = False
        md = await handlers._get_priority_metadata(user_id="u1")
    assert md == {"github_unavailable": "not_configured"}  # not a silent {}


@pytest.mark.asyncio
async def test_priority_metadata_not_connected_signals_degrade(handlers):
    with (
        patch("services.integrations.github.config_service.GitHubConfigService") as CS,
        patch("services.domain.github_domain_service.GitHubDomainService") as DS,
    ):
        CS.return_value.is_configured.return_value = True
        DS.return_value.get_connection_status.return_value = {"connected": False}
        md = await handlers._get_priority_metadata(user_id="u1")
    assert md == {"github_unavailable": "not_connected"}


def test_detailed_priorities_surfaces_connect_nudge_when_degraded(handlers):
    uc = MagicMock(organization=None)
    out = handlers._format_detailed_priorities(
        ["Ship beta"], uc, {"github_unavailable": "not_configured"}
    )
    assert "connect" in out.lower()  # honest nudge, not silent omission
    assert "Ship beta" in out


def test_detailed_priorities_no_github_text_when_genuinely_empty(handlers):
    """Regression: genuinely-empty metadata (no marker, GitHub not involved) stays silent
    on GitHub — we only nudge when there's a real not-connected signal."""
    uc = MagicMock(organization=None)
    out = handlers._format_detailed_priorities(["Ship beta"], uc, {})
    assert "connect it" not in out.lower()
    assert "isn't connected" not in out.lower()
