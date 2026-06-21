"""Tests for default_repo preference helpers (Issue #1042)."""

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
    """WS-1 (#1226): get_default_repo now reads the DB-backed store FIRST. Default it OFF
    (None) for every test so the in-memory round-trip/validation assertions stay deterministic
    + DB-free; the DB-first tests below override this with their own patch."""
    with patch.object(
        UserPreferenceManager, "_read_default_repo_from_db", new=AsyncMock(return_value=None)
    ):
        yield


@pytest.fixture
def manager() -> UserPreferenceManager:
    return UserPreferenceManager()


class TestDefaultRepoRoundTrip:
    """``get_default_repo`` / ``set_default_repo`` round-trip."""

    async def test_default_is_none_when_never_set(self, manager):
        user_id = uuid4()
        assert await manager.get_default_repo(user_id) is None

    async def test_set_then_get_round_trip(self, manager):
        user_id = uuid4()
        await manager.set_default_repo(user_id, "myorg/myrepo")
        assert await manager.get_default_repo(user_id) == "myorg/myrepo"

    async def test_set_to_none_clears(self, manager):
        user_id = uuid4()
        await manager.set_default_repo(user_id, "myorg/myrepo")
        await manager.set_default_repo(user_id, None)
        assert await manager.get_default_repo(user_id) is None

    async def test_per_user_isolation(self, manager):
        user_a = uuid4()
        user_b = uuid4()
        await manager.set_default_repo(user_a, "a-org/a-repo")
        await manager.set_default_repo(user_b, "b-org/b-repo")
        assert await manager.get_default_repo(user_a) == "a-org/a-repo"
        assert await manager.get_default_repo(user_b) == "b-org/b-repo"


class TestDefaultRepoFromDB:
    """WS-1 (#1226): get_default_repo reads the DB-backed connector_configs store FIRST,
    falling back to the legacy in-memory preference. The autouse fixture defaults the DB read
    OFF; these tests turn it on."""

    _DB = "services.domain.user_preference_manager.UserPreferenceManager._read_default_repo_from_db"

    async def test_db_value_used_when_set(self, manager):
        user_id = uuid4()
        with patch(self._DB, new=AsyncMock(return_value="dborg/dbrepo")):
            assert await manager.get_default_repo(user_id) == "dborg/dbrepo"

    async def test_db_beats_in_memory(self, manager):
        user_id = uuid4()
        await manager.set_default_repo(user_id, "memorg/memrepo")  # legacy in-memory
        with patch(self._DB, new=AsyncMock(return_value="dborg/dbrepo")):
            assert await manager.get_default_repo(user_id) == "dborg/dbrepo"  # DB-first

    async def test_db_miss_falls_back_to_in_memory(self, manager):
        user_id = uuid4()
        await manager.set_default_repo(user_id, "memorg/memrepo")
        # autouse fixture returns None from DB → honest-degrade to the in-memory value
        assert await manager.get_default_repo(user_id) == "memorg/memrepo"


class TestDefaultRepoValidation:
    """Setter rejects values outside the ``owner/name`` shape."""

    @pytest.mark.parametrize(
        "bad_value",
        [
            "no-slash",
            "owner/",
            "/name",
            "owner/name/extra",
            "owner name",
            "owner/name with space",
            "",
        ],
    )
    async def test_rejects_invalid(self, manager, bad_value):
        user_id = uuid4()
        with pytest.raises(ValueError):
            await manager.set_default_repo(user_id, bad_value)


class TestDefaultRepoConstants:
    """Smoke checks on exported constants."""

    def test_preference_key_is_stable(self):
        # Renaming would break persisted user data — guard against drift.
        assert DEFAULT_REPO == "default_repo"
