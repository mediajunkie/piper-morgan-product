"""#2072 follow-up: a STALE GitHub binding never RENDERS as a working connection.

Arch's ruling (issuecomment-6234453553): b1fbfa3da1 made a STALE/UNREACHABLE binding
``configured=True, via="oauth_binding_stale", healthy=False``. That is right for gates
(the read runs and discloses STALE_TOKEN), but four renderers turned ``configured`` alone
into a connection claim:

1. Settings → GitHub status (``get_github_settings``): ``valid: True`` with no PAT.
2. Chat floor (``_gather_status_priority_context`` → ``_format_domain_context``):
   "- GitHub: connected".
3. Setup guidance (``_format_integration_setup_guidance``): GitHub under Connected.
4. Identity context (``_gather_identity_context``): ``status: "active"``.

Each pin runs the REAL ``IntegrationStatusService`` with only the binding state (and the
non-binding credential paths) patched, so the served status dict reaches the renderer.
A STALE binding with no PAT yields "Needs reconnecting" on all four; a BOUND binding
still yields the connected claim (the fix does not over-reach).
"""

from __future__ import annotations

import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import services.integrations.integration_status_service as iss_mod
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor
from web.api.routes.integrations import GITHUB_CARD_RECONNECT_DETAIL
from web.api.routes.settings_integrations import get_github_settings

CONFIG_SVC = "services.integrations.github.config_service.GitHubConfigService"

# CXO's copy (2026-10-17), pinned verbatim so the served acceptance (Web: "what's
# connected?" and a work-focus reply with the grant revoked) has a unit twin.
STALE_FLOOR_LINE = (
    "- GitHub: needs reconnecting (the grant was revoked or expired; issue/PR data is "
    "unavailable until it is reconnected: say so and point to Settings → Integrations → "
    "GitHub; do not imply there are no open issues)"
)
STALE_GUIDANCE_GROUP = (
    "\n🟡 **Needs reconnecting:**\n  - GitHub\nReconnect it in Settings → Integrations → GitHub.\n"
)
# Whole word: "reconnected" / "reconnecting" are not a connection claim.
CONNECTED_WORD = re.compile(r"\bconnected\b", re.IGNORECASE)


def _github_lines_claiming_connected(lines):
    return [ln for ln in lines if "GitHub" in ln and CONNECTED_WORD.search(ln)]


def _binding(state):
    """Patch the binding state; every non-binding credential path reads not configured."""
    return (
        patch.object(iss_mod, "github_oauth_binding_state", new=AsyncMock(return_value=state)),
        patch.object(
            iss_mod, "get_config_status", new=AsyncMock(return_value=("not_configured", None))
        ),
    )


def _claims(sub: str = "11111111-2222-3333-4444-555555555555"):
    c = MagicMock()
    c.sub = sub
    return c


def _no_account_pat():
    """#1966: the card reads the account's own PAT through account_pat; none here."""
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return patch.object(GitHubMCPSpatialAdapter, "account_pat", AsyncMock(return_value=None))


async def _status_priority_context(assembler: ContextAssembler) -> dict:
    """Run only the GitHub-flag block of the STATUS/PRIORITY gatherer."""
    empty = AsyncMock(return_value={})
    with (
        patch.object(assembler, "_gather_calendar_context", new=empty),
        patch.object(assembler, "_get_user_context_cached", new=AsyncMock(return_value=None)),
        patch.object(assembler, "_get_pending_todos_cached", new=AsyncMock(return_value=None)),
        patch.object(assembler, "_gather_blocked_items_context", new=empty),
        patch.object(assembler, "_gather_active_milestones_context", new=empty),
        patch.object(assembler, "_gather_recent_activity_context", new=empty),
        patch.object(assembler, "_gather_high_priority_issues_context", new=empty),
    ):
        return await assembler._gather_status_priority_context(user_id="u1")


def _floor_lines(domain_context: dict) -> list:
    out = ConversationalFloor(llm_client=MagicMock())._format_domain_context(domain_context)
    return [line.strip() for line in out.splitlines()]


# ---------------------------------------------------------------------------
# STALE (and UNREACHABLE): never "connected", "active" or valid: True
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("state", ["stale", "unreachable"])
class TestStaleBindingNeverRendersConnected:
    @pytest.mark.asyncio
    async def test_settings_github_status_is_not_valid(self, state):
        b, c = _binding(state)
        with b, c, _no_account_pat():
            result = await get_github_settings(current_user=_claims())
        assert result["configured"] is True
        assert result["valid"] is False
        assert result["error"] == GITHUB_CARD_RECONNECT_DETAIL
        assert result["username"] is None

    @pytest.mark.asyncio
    async def test_chat_floor_says_needs_reconnecting(self, state):
        b, c = _binding(state)
        with b, c:
            ctx = await _status_priority_context(ContextAssembler())
        assert ctx["github_needs_reconnecting"] is True
        lines = _floor_lines(ctx)
        assert STALE_FLOOR_LINE in lines
        assert "- GitHub: connected" not in lines
        assert _github_lines_claiming_connected(lines) == []
        assert "issue/PR data is unavailable" in STALE_FLOOR_LINE  # says it can't be read

    @pytest.mark.asyncio
    async def test_setup_guidance_lists_github_under_needs_reconnecting(self, state):
        b, c = _binding(state)
        with b, c:
            result = await CanonicalHandlers()._format_integration_setup_guidance(user_id="u1")
        message = result["message"]
        assert "✅ **Connected:**" not in message
        assert STALE_GUIDANCE_GROUP in message
        not_connected = message.split("⚪ **Not connected yet:**")[1].split("To connect")[0]
        assert "GitHub" not in not_connected
        # Ordered between Connected (absent here) and Not connected.
        assert message.index(STALE_GUIDANCE_GROUP) < message.index("⚪ **Not connected yet:**")
        context = result["intent"]["context"]
        assert "github" not in context["configured_integrations"]
        assert context["needs_reconnecting_integrations"] == ["github"]
        assert "github" not in context["available_integrations"]

    @pytest.mark.asyncio
    async def test_identity_context_is_not_active(self, state):
        b, c = _binding(state)
        with b, c:
            ctx = await ContextAssembler()._gather_identity_context(user_id="u1", session_id=None)
        statuses = {i["name"]: i["status"] for i in ctx["integrations"]}
        assert statuses["github"] == "needs_reconnecting"
        assert "active" not in statuses.values()
        lines = _floor_lines({"integrations": ctx["integrations"]})
        assert "- Connected integrations: none" in lines
        reconnect = [ln for ln in lines if ln.startswith("- Needs reconnecting")]
        assert reconnect and reconnect[0].endswith(": GitHub")
        assert _github_lines_claiming_connected(lines) == []
        not_connected = [ln for ln in lines if ln.startswith("- Not connected")]
        assert not_connected and "GitHub" not in not_connected[0]


# ---------------------------------------------------------------------------
# BOUND: the connected claim still holds on all four
# ---------------------------------------------------------------------------


class TestBoundBindingStillRendersConnected:
    @pytest.mark.asyncio
    async def test_settings_github_status_is_valid(self):
        b, c = _binding("bound")
        with b, c, _no_account_pat():
            result = await get_github_settings(current_user=_claims())
        assert (result["configured"], result["valid"], result["error"]) == (True, True, None)

    @pytest.mark.asyncio
    async def test_chat_floor_says_connected(self):
        b, c = _binding("bound")
        with b, c:
            ctx = await _status_priority_context(ContextAssembler())
        assert ctx["github_needs_reconnecting"] is False
        assert "- GitHub: connected" in _floor_lines(ctx)

    @pytest.mark.asyncio
    async def test_setup_guidance_lists_github_under_connected(self):
        b, c = _binding("bound")
        with b, c:
            result = await CanonicalHandlers()._format_integration_setup_guidance(user_id="u1")
        message = result["message"]
        assert "Needs reconnecting" not in message
        assert "🟡" not in message
        assert "GitHub" in message.split("✅ **Connected:**")[1].split("⚪")[0]
        assert result["intent"]["context"]["configured_integrations"] == ["github"]

    @pytest.mark.asyncio
    async def test_identity_context_is_active(self):
        b, c = _binding("bound")
        with b, c:
            ctx = await ContextAssembler()._gather_identity_context(user_id="u1", session_id=None)
        statuses = {i["name"]: i["status"] for i in ctx["integrations"]}
        assert statuses["github"] == "active"
        assert "- Connected integrations: GitHub" in _floor_lines(
            {"integrations": ctx["integrations"]}
        )
