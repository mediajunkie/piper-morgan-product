"""#1220/#1382 — chat write handlers must use the binding-aware gate + the guarded router.

The miss these tests pin (found live 2026-07-09, PM's first-real-write attempt):
``_handle_create_issue``/``_handle_update_issue`` gated on GITHUB_TOKEN/PAT only —
telling OAuth-connected users "GitHub isn't connected" — and then called the legacy
``GitHubDomainService`` directly, bypassing the #1220 connector-first router writes
and their #1322 read-back guard entirely. "Building a feature Piper can't use is
not done" (PM, 2026-07-09).

Contract pinned here:
1. The gate is ``GitHubIntegrationRouter.is_available()`` (binding OR PAT) — no
   env/keychain PAT check in the handler.
2. The write goes through ``github_router.create_issue``/``update_issue`` (the
   guarded, connector-first methods) — never ``GitHubDomainService`` directly.
3. A fired-but-unverified connector write surfaces honest uncertainty verbatim.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


def _intent(action="create_issue", **ctx):
    defaults = {"title": "Test issue", "repository": "acme/widgets"}
    defaults.update(ctx)
    return Intent(
        original_message="create an issue",
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        context=defaults,
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    return IntentService()


class TestCreateIssueGate:
    @pytest.mark.asyncio
    async def test_oauth_binding_passes_gate_and_write_goes_through_router(self, svc):
        """A user with ONLY an OAuth binding (no PAT anywhere) must reach the
        guarded router write — the exact case the legacy gate refused."""
        created = {"number": 7, "html_url": "https://x/7", "title": "Test issue"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert result.success
        assert "#7" in result.message
        w.assert_awaited_once()
        kwargs = w.await_args.kwargs
        assert kwargs["owner"] == "acme" and kwargs["repo_name"] == "widgets"

    @pytest.mark.asyncio
    async def test_unavailable_degrades_with_settings_guidance(self, svc):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=False)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert "Settings" in result.message and "Integrations" in result.message
        w.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_unverified_write_surfaces_honest_uncertainty(self, svc):
        boom = RuntimeError(
            "GitHub write could not be verified — it may or may not have landed. "
            "Check the repository directly before retrying; do not assume success."
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(side_effect=boom)),
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert "may or may not" in result.message
        assert "duplicate" in result.message


class TestUpdateIssueGate:
    @pytest.mark.asyncio
    async def test_update_goes_through_router(self, svc):
        updated = {"number": 42, "title": "New title"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)) as w,
        ):
            result = await svc._handle_update_issue(
                _intent(action="update_issue", issue_number=42, title="New title"),
                "wf-1",
            )
        assert result.success and "#42" in result.message
        w.assert_awaited_once()
        assert w.await_args.kwargs["owner"] == "acme"

    @pytest.mark.asyncio
    async def test_update_unavailable_degrades(self, svc):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=False)),
        ):
            result = await svc._handle_update_issue(
                _intent(action="update_issue", issue_number=42, title="t"), "wf-1"
            )
        assert "Settings" in result.message


class TestRouterIsAvailable:
    """The gate itself: OAuth binding (BOUND) OR legacy PAT — either suffices."""

    def _router(self, user_id="694d8f4e-0000-0000-0000-000000000042"):
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        r = GitHubIntegrationRouter()
        r._user_id = user_id
        return r

    @pytest.mark.asyncio
    async def test_bound_binding_without_pat_is_available(self):
        r = self._router()
        binding = type("B", (), {"status": "bound"})()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=binding),
            ),
            patch.object(r.config_service, "is_configured", return_value=False),
        ):
            assert await r.is_available() is True

    @pytest.mark.asyncio
    async def test_no_binding_no_pat_unavailable(self):
        r = self._router()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=None),
            ),
            patch.object(r.config_service, "is_configured", return_value=False),
        ):
            assert await r.is_available() is False

    @pytest.mark.asyncio
    async def test_pat_only_still_available(self):
        r = self._router()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=None),
            ),
            patch.object(r.config_service, "is_configured", return_value=True),
        ):
            assert await r.is_available() is True
