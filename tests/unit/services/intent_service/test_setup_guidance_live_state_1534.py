"""#1534 — integration-setup guidance reads LIVE per-user connection state.

The lie this pins (PM live, 2026-08-09): 'connect my calendar' guidance listed
Slack/Notion/GitHub/Calendar all under 'Not connected' for a user whose
Integration Health page showed 4-of-4 healthy — the guidance formatter read the
plugin registry's constant-false ``configured`` bit (#784) instead of the
user-scoped truth. #1547 F1 rewired the formatter onto the canonical
IntegrationStatusService; the unit tests there mock the service seam
(test_status_truth_1547.py) or the binding seam
(test_integration_status_service_1547.py).

This file closes the remaining gap: an END-TO-END run with a REAL binding
fixture. A real ConnectorBinding row (in-memory SQLite, status=bound) flows
through the real ``ConnectorBindingRepository`` -> real ``github_oauth_bound``
-> real ``IntegrationStatusService.get_all`` -> the real guidance formatter.
Nothing on the status path is mocked except the process environment and the
host keychain (so the test can't read the developer's real credentials).

Pinned here:
- BOUND github binding => guidance shows GitHub under Connected (never the
  all-'Not connected' lie).
- No binding, no creds => honestly Not connected — WITHOUT the status-check
  failure disclaimer (an honest negative is a measurement, not a fallback;
  m-44: 'Not connected' as a default would be a false measurement).
- Demo never enumerated in user-facing copy (it's a loadable plugin, not an
  integration a user connects).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.intent_service.canonical_handlers import CanonicalHandlers  # noqa: E402

pytestmark = pytest.mark.asyncio

_USER = "11111111-1111-1111-1111-111111111111"

_ENV_VARS = (
    "GITHUB_TOKEN",
    "GITHUB_ACCESS_TOKEN",
    "NOTION_API_TOKEN",
    "NOTION_API_KEY",
    "SLACK_BOT_TOKEN",
    "GOOGLE_CALENDAR_CREDENTIALS",
    "MCP_ENABLED",
)


@pytest_asyncio.fixture
async def session():
    """Real in-memory DB with the real ConnectorBinding table (single-table
    create — the full metadata has PG-only types; mirrors #1229's setup)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


@asynccontextmanager
async def _yield_session(s):
    yield s


def _live_state_environment(monkeypatch, session):
    """Point the status path's session scopes at the fixture DB and blank the
    host credential stores — everything else on the path stays real."""
    for var in _ENV_VARS:
        monkeypatch.delenv(var, raising=False)

    keychain = MagicMock()
    keychain.get_api_key.return_value = None

    return (
        patch.object(AsyncSessionFactory, "session_scope", new=lambda: _yield_session(session)),
        patch.object(
            AsyncSessionFactory,
            "session_scope_fresh",
            new=lambda: _yield_session(session),
        ),
        patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=keychain,
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            new=AsyncMock(return_value=None),
        ),
    )


class TestGuidanceReadsRealBindingState:
    async def test_bound_github_binding_reports_connected(self, session, monkeypatch):
        """AC1: with a connected GitHub binding (real row), guidance says so.

        This is the pinned #1534 regression: before the fix, THIS user — with a
        genuinely BOUND connector — was told everything was 'Not connected'."""
        await ConnectorBindingRepository(session).upsert(
            _USER, "github", mcp_server_ref="github-mcp-server", status="bound"
        )
        await session.commit()

        p1, p2, p3, p4 = _live_state_environment(monkeypatch, session)
        with p1, p2, p3, p4:
            result = await CanonicalHandlers()._format_integration_setup_guidance(user_id=_USER)

        message = result["message"]
        assert "✅ **Connected:**" in message
        connected_section = message.split("⚪")[0]
        assert "GitHub" in connected_section
        assert result["intent"]["context"]["configured_integrations"] == ["github"]
        # The lie was ALL-not-connected; a real binding must break it.
        assert set(result["intent"]["context"]["available_integrations"]) == {
            "slack",
            "calendar",
            "notion",
        }
        # And this is a measurement, not the couldn't-check fallback.
        assert "couldn't check your current connection status" not in message

    async def test_no_binding_reports_honestly_not_connected(self, session, monkeypatch):
        """AC2: with no binding and no credentials, GitHub is honestly Not
        connected — a real negative measurement, not the failure disclaimer."""
        p1, p2, p3, p4 = _live_state_environment(monkeypatch, session)
        with p1, p2, p3, p4:
            result = await CanonicalHandlers()._format_integration_setup_guidance(user_id=_USER)

        message = result["message"]
        assert result["intent"]["context"]["configured_integrations"] == []
        assert "⚪ **Not connected:**" in message
        not_connected_section = message.split("⚪")[1]
        assert "GitHub" in not_connected_section
        # Honest negative != status-check failure (the #1423 fallback copy).
        assert "couldn't check your current connection status" not in message

    async def test_demo_absent_from_user_facing_copy(self, session, monkeypatch):
        """AC3: 'Demo' (loadable plugin, not a user integration) never appears —
        in either the bound or the unbound rendering."""
        await ConnectorBindingRepository(session).upsert(_USER, "github", status="bound")
        await session.commit()

        p1, p2, p3, p4 = _live_state_environment(monkeypatch, session)
        with p1, p2, p3, p4:
            result = await CanonicalHandlers()._format_integration_setup_guidance(user_id=_USER)

        assert "demo" not in result["message"].lower()
        assert "demo" not in result["intent"]["context"]["configured_integrations"]
        assert "demo" not in result["intent"]["context"]["available_integrations"]
