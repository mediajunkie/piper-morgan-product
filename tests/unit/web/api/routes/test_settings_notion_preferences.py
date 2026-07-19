"""#1400: slack/calendar/notion prefs live in the DB connector_configs store.

Replaces the flat-file-era suite (data/notion_preferences.json et al.) — those
files were hosted data loss (Fly's FS is ephemeral; every deploy wiped every
user's prefs) and the helpers they pinned are deleted. Pref round-trips run
the route functions against the REAL dev Postgres (B15/#1421 house pattern):

- save -> get round-trip per connector (slack / calendar / notion)
- owner isolation (user B never sees A's prefs — connector_configs is
  owner-scoped by construction, ADR-070 D4)
- the one-time legacy flat-file migration shim (droplet case)
- merge semantics (a save never clobbers cohabiting blob keys)

The Notion databases-endpoint tests (aiohttp-mocked, #572) are ported from the
old suite with the prefs helper swapped to the DB one.
"""

import json
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import web.api.routes.settings_integrations as si
from web.api.routes.settings_integrations import (
    CalendarPreferencesRequest,
    NotionPreferencesRequest,
    SlackPreferencesRequest,
    _load_prefs_db,
    _save_prefs_db,
    get_calendar_preferences,
    get_notion_databases,
    get_notion_preferences,
    get_slack_preferences,
    save_calendar_preferences,
    save_notion_preferences,
    save_slack_preferences,
)

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def two_users():
    """Two real user rows; yields (a_id, b_id); cleans users + connector_configs."""
    engine = create_async_engine(_DB_URL, echo=False)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    now = datetime.now(timezone.utc)
    async with factory() as s:
        for uid in (a_id, b_id):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {
                    "id": uid,
                    "u": f"p1400_{uid[:8]}",
                    "e": f"p1400_{uid[:8]}@test.example.com",
                    "now": now,
                },
            )
        await s.commit()
    try:
        yield a_id, b_id
    finally:
        async with factory() as s:
            for uid in (a_id, b_id):
                await s.execute(
                    text("DELETE FROM connector_configs WHERE owner_id = CAST(:u AS uuid)"),
                    {"u": uid},
                )
                await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
            await s.commit()
        await engine.dispose()


def _claims(uid: str):
    return SimpleNamespace(sub=uid)


class TestPrefsRoundTrips:
    @pytest.mark.asyncio
    async def test_slack_save_then_get(self, two_users):
        a, _ = two_users
        req = SlackPreferencesRequest(
            notification_channel="#piper",
            monitored_channels=["#eng", "#product"],
            default_response_channel="#piper",
        )
        await save_slack_preferences(req, current_user=_claims(a))
        resp = await get_slack_preferences(current_user=_claims(a))
        assert resp.notification_channel == "#piper"
        assert resp.monitored_channels == ["#eng", "#product"]
        assert resp.default_response_channel == "#piper"

    @pytest.mark.asyncio
    async def test_calendar_save_then_get(self, two_users):
        a, _ = two_users
        req = CalendarPreferencesRequest(
            selected_calendars=["primary", "team"], primary_calendar="primary"
        )
        await save_calendar_preferences(req, current_user=_claims(a))
        resp = await get_calendar_preferences(current_user=_claims(a))
        assert resp.selected_calendars == ["primary", "team"]
        assert resp.primary_calendar == "primary"

    @pytest.mark.asyncio
    async def test_notion_save_then_get_and_overwrite(self, two_users):
        a, _ = two_users
        await save_notion_preferences(
            NotionPreferencesRequest(selected_databases=["db1"], default_database="db1"),
            current_user=_claims(a),
        )
        await save_notion_preferences(
            NotionPreferencesRequest(selected_databases=["db2", "db3"], default_database="db2"),
            current_user=_claims(a),
        )
        resp = await get_notion_preferences(current_user=_claims(a))
        assert resp.selected_databases == ["db2", "db3"]
        assert resp.default_database == "db2"

    @pytest.mark.asyncio
    async def test_owner_isolation(self, two_users):
        a, b = two_users
        await save_notion_preferences(
            NotionPreferencesRequest(
                selected_databases=["private-db"], default_database="private-db"
            ),
            current_user=_claims(a),
        )
        resp_b = await get_notion_preferences(current_user=_claims(b))
        assert resp_b.selected_databases == []
        assert resp_b.default_database is None

    @pytest.mark.asyncio
    async def test_unset_user_gets_empty(self, two_users):
        _, b = two_users
        resp = await get_slack_preferences(current_user=_claims(b))
        assert resp.notification_channel is None
        assert resp.monitored_channels == []


class TestLegacyFileMigrationShim:
    @pytest.mark.asyncio
    async def test_legacy_file_entry_migrates_once(self, two_users, tmp_path, monkeypatch):
        """A pre-#1400 droplet flat file's entry is read once, written to the
        DB, and served from the DB thereafter (file deleted -> prefs survive)."""
        a, _ = two_users
        legacy = tmp_path / "slack_preferences.json"
        legacy.write_text(json.dumps({a: {"notification_channel": "#legacy"}}))
        monkeypatch.setitem(si._LEGACY_PREF_FILES, "slack", str(legacy))
        first = await _load_prefs_db(a, "slack")
        assert first == {"notification_channel": "#legacy"}
        legacy.unlink()  # file gone (the deploy-wipe case) — DB now owns it
        second = await _load_prefs_db(a, "slack")
        assert second == {"notification_channel": "#legacy"}

    @pytest.mark.asyncio
    async def test_no_file_no_db_is_plain_empty(self, two_users):
        _, b = two_users
        assert await _load_prefs_db(b, "calendar") == {}


class TestSaveMergesBlob:
    @pytest.mark.asyncio
    async def test_save_preserves_cohabiting_keys(self, two_users):
        """Merge semantics (mirrors the github helper): a save must not clobber
        other keys already in the same connector blob."""
        a, _ = two_users
        await _save_prefs_db(a, "slack", {"workspace_name": "piperhq"})
        await _save_prefs_db(a, "slack", {"notification_channel": "#piper"})
        blob = await _load_prefs_db(a, "slack")
        assert blob["workspace_name"] == "piperhq"
        assert blob["notification_channel"] == "#piper"


class TestGetNotionDatabases:
    """Ported from the flat-file-era suite (#572) — prefs helper swapped to DB."""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        mock_config = MagicMock()
        mock_config.api_key = None
        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.notion.config_service.NotionConfigService",
            return_value=mock_config_service,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_notion_databases(current_user=mock_user)
            assert exc_info.value.status_code == 401
            assert "not connected" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_returns_database_list_when_connected(self):
        mock_config = MagicMock()
        mock_config.api_key = "secret_test_key"
        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        mock_notion_response = {
            "results": [
                {
                    "id": "abc123",
                    "title": [{"plain_text": "Work Tasks"}],
                    "description": [{"plain_text": "Team task tracker"}],
                },
                {
                    "id": "def456",
                    "title": [{"plain_text": "Project Notes"}],
                    "description": [],
                },
            ]
        }
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_notion_response)
        mock_session_instance = MagicMock()
        mock_session_instance.post = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )
        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
            patch(
                "web.api.routes.settings_integrations._load_prefs_db",
                new=AsyncMock(return_value={}),
            ),
        ):
            result = await get_notion_databases(current_user=mock_user)
            assert len(result.databases) == 2
            assert result.databases[0].id == "abc123"
            assert result.databases[0].name == "Work Tasks"
            assert result.databases[0].description == "Team task tracker"
            assert result.databases[1].id == "def456"
            assert result.databases[1].name == "Project Notes"
            assert result.databases[1].description == ""

    @pytest.mark.asyncio
    async def test_returns_error_when_notion_api_fails(self):
        mock_config = MagicMock()
        mock_config.api_key = "secret_test_key"
        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Invalid API key")
        mock_session_instance = MagicMock()
        mock_session_instance.post = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )
        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_notion_databases(current_user=mock_user)
            assert exc_info.value.status_code >= 500
