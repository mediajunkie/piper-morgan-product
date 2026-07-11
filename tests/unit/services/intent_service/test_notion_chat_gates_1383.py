"""#1383 — Notion chat gates must check the REQUESTING USER, not the global plugin.

The live failure (found 2026-07-09, PM-directed same-oversight audit after the
GitHub #1220 first-real-write miss): all three Notion chat handlers gated on
``notion_router.is_configured()`` — no user argument — whose delegate plugin
documents itself as returning False until a user context exists (#781). On
hosted, a tester with a UI-saved Notion key (Settings → Notion, stored via
UserAPIKeyService → user-scoped keychain → #1382 encrypted-DB store) was told
"Notion isn't configured." And past the gate, the bare ``connect()`` resolved
static/env config only — the user's token never reached the client.

Contract pinned here (the GitHub #1220 shape):
1. The gate is ``NotionIntegrationRouter.is_available(user_id)`` — per-user
   config chain (env > user config > user-scoped keychain), global fallback
   only for principal-less calls, never raises.
2. The connect is ``connect_for_user(user_id)`` — resolves the SAME chain and
   passes the user's token explicitly; legacy resolution when no principal.
3. Handlers thread ``_principal_from_intent(intent)`` into both.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.integrations.notion.notion_integration_router import (
    NotionIntegrationRouter,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"


def _router_with_config(is_configured=None, api_key=None, raises=None):
    cfg = MagicMock()
    if raises:
        cfg.is_configured.side_effect = raises
        cfg.get_config.side_effect = raises
    else:
        cfg.is_configured.return_value = bool(is_configured)
        cfg.get_config.return_value.get_api_key.return_value = api_key or ""
    r = NotionIntegrationRouter(config_service=cfg)
    return r, cfg


class TestIsAvailable:
    def test_user_with_saved_key_passes_even_when_global_check_is_false(self):
        """THE live bug: per-user key present, plugin's no-user check False."""
        r, cfg = _router_with_config(is_configured=True)
        with patch.object(r, "is_configured", return_value=False):
            assert r.is_available("user-1") is True
        cfg.is_configured.assert_called_once_with("user-1")

    def test_user_without_key_is_unavailable(self):
        r, _ = _router_with_config(is_configured=False)
        with patch.object(r, "is_configured", return_value=True):
            # per-user answer wins for a principal'd call — no global bleed-through
            assert r.is_available("user-1") is False

    def test_per_user_check_error_degrades_false_not_raise(self):
        r, _ = _router_with_config(raises=RuntimeError("db down"))
        assert r.is_available("user-1") is False

    def test_principal_less_falls_back_to_global(self):
        r, _ = _router_with_config(is_configured=False)
        with patch.object(r, "is_configured", return_value=True):
            assert r.is_available(None) is True

    def test_principal_less_global_error_degrades_false(self):
        r, _ = _router_with_config()
        with patch.object(r, "is_configured", side_effect=RuntimeError("no integration")):
            assert r.is_available(None) is False


class TestConnectForUser:
    @pytest.mark.asyncio
    async def test_user_token_threads_into_connect(self):
        r, _ = _router_with_config(api_key="secret_user_token")
        with patch.object(
            r, "connect", new=AsyncMock(return_value=True)
        ) as connect:
            assert await r.connect_for_user("user-1") is True
        connect.assert_awaited_once_with(integration_token="secret_user_token")

    @pytest.mark.asyncio
    async def test_no_principal_uses_legacy_resolution(self):
        r, _ = _router_with_config()
        with patch.object(r, "connect", new=AsyncMock(return_value=True)) as connect:
            await r.connect_for_user(None)
        connect.assert_awaited_once_with(integration_token=None)

    @pytest.mark.asyncio
    async def test_config_error_degrades_to_legacy_resolution(self):
        r, _ = _router_with_config(raises=RuntimeError("keychain down"))
        with patch.object(r, "connect", new=AsyncMock(return_value=False)) as connect:
            await r.connect_for_user("user-1")
        connect.assert_awaited_once_with(integration_token=None)


def _search_intent(user_id="694d8f4e-0000-0000-0000-000000000042"):
    return Intent(
        original_message="search our docs for the roadmap",
        category=IntentCategory.ANALYSIS,
        action="search_documents",
        confidence=0.9,
        context={"search_query": "roadmap", "user_id": user_id},
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    return IntentService()


class TestSearchHandlerThreadsPrincipal:
    @pytest.mark.asyncio
    async def test_unavailable_user_gets_settings_guidance(self, svc):
        with patch(f"{ROUTER}.is_available", return_value=False) as gate:
            result = await svc._handle_search_documents_notion(
                _search_intent(), "wf-1", "sess-1"
            )
        assert "Settings → Notion" in result.message
        gate.assert_called_once_with("694d8f4e-0000-0000-0000-000000000042")

    @pytest.mark.asyncio
    async def test_available_user_connects_as_themselves(self, svc):
        with (
            patch(f"{ROUTER}.is_available", return_value=True),
            patch(f"{ROUTER}.connect_for_user", new=AsyncMock(return_value=True)) as cfu,
            patch(f"{ROUTER}.search_notion", new=AsyncMock(return_value=[])),
        ):
            result = await svc._handle_search_documents_notion(
                _search_intent(), "wf-1", "sess-1"
            )
        assert result.success
        cfu.assert_awaited_once_with("694d8f4e-0000-0000-0000-000000000042")
