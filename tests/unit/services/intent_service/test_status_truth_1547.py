"""#1547: chat/floor surfaces read the canonical IntegrationStatusService, not the
constant-false plugin registry (#784 root; status-truth audit 2026-08-09).

Covers the migrated surfaces:
- F1 `_format_integration_setup_guidance` — a connected user's integrations show
  under Connected; Demo never enumerated (#1534).
- F2 the floor is no longer blind — identity context carries per-user integration
  status; the renderer emits BOTH directions; `github_connected` is a real flag
  AND actually rendered (was computed-and-dropped).
- F3 `_get_project_metadata` gate is service-fed (was plugin.is_configured()
  constant-false).
- F4 `_get_priority_metadata` is binding-first (was PAT-only
  GitHubConfigService.is_configured — OAuth-bound-no-PAT users degraded).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor
from services.mcp.consumer.connector import DegradationReason

SVC = "services.integrations.integration_status_service.IntegrationStatusService"


def _all_statuses(**configured):
    """Build a get_all() return: {"github": True, ...} — unnamed default False."""
    out = {}
    for name in ("github", "slack", "calendar", "notion"):
        out[name] = {
            "configured": configured.get(name, False),
            "via": "keychain" if configured.get(name) else None,
            "healthy": None,
            "last_check": None,
        }
    return out


@pytest.fixture
def handlers():
    return CanonicalHandlers()


# ---------------------------------------------------------------------------
# F1 — integration setup guidance
# ---------------------------------------------------------------------------


class TestSetupGuidanceUsesCanonicalService:
    @pytest.mark.asyncio
    async def test_connected_user_sees_integration_under_connected(self, handlers):
        """The #1534 lie: a GitHub-connected user was told all four 'Not connected'.
        With the canonical service, their GitHub shows under Connected."""
        with patch(
            f"{SVC}.get_all",
            new=AsyncMock(return_value=_all_statuses(github=True)),
        ):
            result = await handlers._format_integration_setup_guidance(user_id="u1")
        message = result["message"]
        assert "✅ **Connected:**" in message
        connected_section = message.split("⚪")[0]
        assert "GitHub" in connected_section
        assert result["intent"]["context"]["configured_integrations"] == ["github"]

    @pytest.mark.asyncio
    async def test_unconnected_integrations_listed_not_connected(self, handlers):
        with patch(
            f"{SVC}.get_all",
            new=AsyncMock(return_value=_all_statuses(github=True)),
        ):
            result = await handlers._format_integration_setup_guidance(user_id="u1")
        not_connected = result["intent"]["context"]["available_integrations"]
        assert set(not_connected) == {"slack", "calendar", "notion"}

    @pytest.mark.asyncio
    async def test_demo_never_enumerated(self, handlers):
        """Demo disappears for free — the canonical set excludes it structurally."""
        with patch(
            f"{SVC}.get_all",
            new=AsyncMock(return_value=_all_statuses()),
        ):
            result = await handlers._format_integration_setup_guidance(user_id="u1")
        assert "demo" not in result["message"].lower()

    @pytest.mark.asyncio
    async def test_status_check_failure_stays_honest(self, handlers):
        """#1423 behavior preserved: a failed status check is NAMED, not silent."""
        with patch(
            f"{SVC}.get_all",
            new=AsyncMock(side_effect=RuntimeError("status source down")),
        ):
            result = await handlers._format_integration_setup_guidance(user_id="u1")
        assert "couldn't check your current connection status" in result["message"]


# ---------------------------------------------------------------------------
# F2 — the floor sees per-user integration status, both directions
# ---------------------------------------------------------------------------


class TestFloorIntegrationVisibility:
    @pytest.mark.asyncio
    async def test_identity_context_integrations_are_user_scoped(self):
        assembler = ContextAssembler()
        with patch(
            f"{SVC}.get_all",
            new=AsyncMock(return_value=_all_statuses(github=True)),
        ):
            result = await assembler._gather_identity_context(user_id="u1", session_id=None)
        integrations = {i["name"]: i["status"] for i in result["integrations"]}
        assert integrations["github"] == "active"
        assert integrations["notion"] == "inactive"

    def test_renderer_emits_both_directions(self):
        """The two-direction line: 'GitHub connected; Notion isn't' — not omission."""
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {
                "integrations": [
                    {"name": "github", "status": "active"},
                    {"name": "notion", "status": "inactive"},
                ]
            }
        )
        assert "Connected integrations: GitHub" in out
        assert "Not connected" in out
        assert "Notion" in out

    def test_renderer_honest_when_nothing_connected(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {"integrations": [{"name": "github", "status": "inactive"}]}
        )
        assert "Connected integrations: none" in out
        assert "GitHub" in out

    @pytest.mark.asyncio
    async def test_status_context_github_flag_from_service(self):
        """github_connected is a real per-user flag now (was registry constant-false)."""
        assembler = ContextAssembler()
        with patch(
            f"{SVC}.get_status",
            new=AsyncMock(
                return_value={
                    "configured": True,
                    "via": "oauth_binding",
                    "healthy": True,
                    "last_check": None,
                }
            ),
        ):
            ctx = {}
            # only exercise the github-flag block — other gathers need user infra
            with (
                patch.object(assembler, "_gather_calendar_context", new=AsyncMock(return_value={})),
                patch.object(
                    assembler, "_get_user_context_cached", new=AsyncMock(return_value=None)
                ),
                patch.object(
                    assembler, "_get_pending_todos_cached", new=AsyncMock(return_value=None)
                ),
                patch.object(
                    assembler,
                    "_gather_blocked_items_context",
                    new=AsyncMock(return_value={}),
                ),
                patch.object(
                    assembler,
                    "_gather_active_milestones_context",
                    new=AsyncMock(return_value={}),
                ),
                patch.object(
                    assembler,
                    "_gather_recent_activity_context",
                    new=AsyncMock(return_value={}),
                ),
                patch.object(
                    assembler,
                    "_gather_high_priority_issues_context",
                    new=AsyncMock(return_value={}),
                ),
            ):
                ctx = await assembler._gather_status_priority_context(user_id="u1")
        assert ctx["github_connected"] is True

    def test_renderer_actually_renders_github_connected(self):
        """Was computed-and-dropped (comment-only) — now an actual line, both ways."""
        floor = ConversationalFloor(llm_client=MagicMock())
        assert "GitHub: connected" in floor._format_domain_context({"github_connected": True})
        assert "GitHub: not connected" in floor._format_domain_context({"github_connected": False})


# ---------------------------------------------------------------------------
# F3 — project metadata gate is service-fed
# ---------------------------------------------------------------------------


class TestProjectMetadataGate:
    @pytest.mark.asyncio
    async def test_not_configured_degrades_honestly(self, handlers):
        with patch(f"{SVC}.is_configured", new=AsyncMock(return_value=False)):
            md = await handlers._get_project_metadata(["Proj A"], user_id="u1")
        assert md == {"__degrade_reason__": DegradationReason.NOT_CONFIGURED}

    @pytest.mark.asyncio
    async def test_configured_user_passes_the_gate(self, handlers):
        """A connected user (e.g. OAuth-bound) is NOT told to connect at the gate —
        the constant-false plugin gate sent #1231 nudges to CONNECTED users."""
        with (
            patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
            patch("services.domain.github_domain_service.GitHubDomainService") as DS,
        ):
            DS.return_value.get_connection_status.return_value = {"connected": False}
            md = await handlers._get_project_metadata(["Proj A"], user_id="u1")
        # passes the gate; the (legacy PAT-side) connection check governs after
        assert md == {"__degrade_reason__": DegradationReason.CONNECT_REQUIRED}


# ---------------------------------------------------------------------------
# F4 — priority metadata is binding-first
# ---------------------------------------------------------------------------


class TestPriorityMetadataBindingFirst:
    @pytest.mark.asyncio
    async def test_oauth_bound_no_pat_user_is_not_degraded(self, handlers):
        """The F4 case: OAuth-bound, no PAT. PAT-only GitHubConfigService would say
        False; the canonical (binding-first) service says True → no degrade."""
        with (
            patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
            patch("services.integrations.github.config_service.GitHubConfigService") as CS,
            patch("services.domain.github_domain_service.GitHubDomainService") as DS,
            patch(
                "services.integrations.github.repo_resolver.get_user_default_repo",
                new_callable=AsyncMock,
            ) as repo,
        ):
            CS.return_value.is_configured.return_value = False  # PAT-only view
            DS.return_value.get_connection_status.return_value = {"connected": True}
            repo.return_value = None
            md = await handlers._get_priority_metadata(
                user_id="12345678-1234-5678-1234-567812345678"
            )
        assert md == {"has_github": True, "high_priority_issues": []}

    @pytest.mark.asyncio
    async def test_truly_unconfigured_still_degrades(self, handlers):
        with patch(f"{SVC}.is_configured", new=AsyncMock(return_value=False)):
            md = await handlers._get_priority_metadata(user_id="u1")
        assert md == {"degrade_reason": DegradationReason.NOT_CONFIGURED}
