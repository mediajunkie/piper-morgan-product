"""Tests for default_repo preference helpers (Issue #1042).

WS-1 P4 (#1226 / #1199): the in-memory default-repo store was RETIRED — the DB-backed
connector_configs store is the SOLE store. ``get_default_repo`` is DB-only;
``UserPreferenceManager.set_default_repo`` was removed (zero non-test callers — writes go
through ``ConnectorConfigService.set_default_repo``). The in-memory round-trip / validation /
fallback tests are gone with the machinery they covered; ``DEFAULT_REPO`` is retained as a
stable preference-key name (the #1050 active_repos tests guard it against aliasing).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.user_preference_manager import (
    DEFAULT_REPO,
    UserPreferenceManager,
)


@pytest.fixture(autouse=True)
def _db_default_repo_off():
    """WS-1 P4: get_default_repo reads the DB-backed store. Default it OFF (None) for every test
    so assertions stay deterministic + DB-free; the DB-value test below overrides this."""
    with patch.object(
        UserPreferenceManager, "_read_default_repo_from_db", new=AsyncMock(return_value=None)
    ):
        yield


@pytest.fixture
def manager() -> UserPreferenceManager:
    return UserPreferenceManager()


class TestDefaultRepoFromDB:
    """WS-1 P4 (#1226 / #1199): get_default_repo reads the DB-backed connector_configs store —
    the SOLE store. The autouse fixture defaults the DB read OFF; these tests turn it on."""

    _DB = "services.domain.user_preference_manager.UserPreferenceManager._read_default_repo_from_db"

    async def test_db_value_used_when_set(self, manager):
        user_id = uuid4()
        with patch(self._DB, new=AsyncMock(return_value="dborg/dbrepo")):
            assert await manager.get_default_repo(user_id) == "dborg/dbrepo"

    async def test_db_miss_returns_none(self, manager):
        """WS-1 P4: a DB miss returns None — there is no second store to fall back to."""
        user_id = uuid4()
        # autouse fixture returns None from DB → get_default_repo returns None
        assert await manager.get_default_repo(user_id) is None


class TestDefaultRepoConstants:
    """Smoke checks on exported constants.

    ``DEFAULT_REPO`` is retained post-P4 as the stable preference-key name (no longer a live
    read/write target). Renaming it would break the #1050 active_repos distinctness guard.
    """

    def test_preference_key_is_stable(self):
        assert DEFAULT_REPO == "default_repo"
