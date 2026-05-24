"""Tests for active_repos preference helpers (Issue #1050 STANDUP-ACTIVE-REPOS).

Mirrors the structure of `test_user_preference_manager_default_repo_1042.py`
and extends with list-shape + entry-shape validation.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from services.domain.user_preference_manager import (
    ACTIVE_REPOS,
    UserPreferenceManager,
)


@pytest.fixture
def manager() -> UserPreferenceManager:
    return UserPreferenceManager()


class TestActiveReposRoundTrip:
    """``get_active_repos`` / ``set_active_repos`` round-trip."""

    async def test_default_is_none_when_never_set(self, manager):
        """`None` is the not-set sentinel — falls through the standup chain."""
        user_id = uuid4()
        assert await manager.get_active_repos(user_id) is None

    async def test_set_single_entry_round_trip(self, manager):
        user_id = uuid4()
        await manager.set_active_repos(user_id, ["myorg/myrepo"])
        assert await manager.get_active_repos(user_id) == ["myorg/myrepo"]

    async def test_set_multi_entry_round_trip(self, manager):
        user_id = uuid4()
        await manager.set_active_repos(
            user_id, ["myorg/repo-a", "myorg/repo-b", "other-org/repo-c"]
        )
        assert await manager.get_active_repos(user_id) == [
            "myorg/repo-a",
            "myorg/repo-b",
            "other-org/repo-c",
        ]

    async def test_explicit_empty_list_preserved(self, manager):
        """Empty list is a VALID saved value meaning 'explicitly no active
        repos' — distinct from None (preference unset). Standup resolution
        chain treats them differently per the #1050 design."""
        user_id = uuid4()
        await manager.set_active_repos(user_id, [])
        result = await manager.get_active_repos(user_id)
        assert result == []
        assert result is not None  # None-vs-empty distinction is load-bearing

    async def test_set_to_none_clears(self, manager):
        user_id = uuid4()
        await manager.set_active_repos(user_id, ["myorg/myrepo"])
        await manager.set_active_repos(user_id, None)
        assert await manager.get_active_repos(user_id) is None

    async def test_per_user_isolation(self, manager):
        user_a = uuid4()
        user_b = uuid4()
        await manager.set_active_repos(user_a, ["a-org/a-repo-1", "a-org/a-repo-2"])
        await manager.set_active_repos(user_b, ["b-org/b-repo"])
        assert await manager.get_active_repos(user_a) == [
            "a-org/a-repo-1",
            "a-org/a-repo-2",
        ]
        assert await manager.get_active_repos(user_b) == ["b-org/b-repo"]


class TestActiveReposListShapeValidation:
    """Setter rejects non-list values."""

    @pytest.mark.parametrize(
        "bad_value",
        [
            "owner/name",  # bare string — caller meant DEFAULT_REPO
            42,
            {"owner/name"},  # set, not list
            ("owner/name",),  # tuple, not list
            {"key": "owner/name"},  # dict
        ],
    )
    async def test_rejects_non_list(self, manager, bad_value):
        user_id = uuid4()
        with pytest.raises(TypeError):
            await manager.set_active_repos(user_id, bad_value)


class TestActiveReposEntryShapeValidation:
    """Setter rejects lists with malformed entries."""

    @pytest.mark.parametrize(
        "bad_entry",
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
    async def test_rejects_malformed_string_entry(self, manager, bad_entry):
        user_id = uuid4()
        with pytest.raises(ValueError):
            await manager.set_active_repos(user_id, [bad_entry])

    @pytest.mark.parametrize(
        "bad_entry",
        [
            42,
            None,
            ["nested"],
            {"owner": "name"},
        ],
    )
    async def test_rejects_non_string_entry(self, manager, bad_entry):
        user_id = uuid4()
        with pytest.raises(ValueError):
            await manager.set_active_repos(user_id, [bad_entry])

    async def test_rejects_when_one_entry_bad_in_otherwise_valid_list(self, manager):
        """List validation is all-or-nothing — one bad entry blocks the set."""
        user_id = uuid4()
        with pytest.raises(ValueError):
            await manager.set_active_repos(
                user_id, ["valid-org/valid-repo", "INVALID", "other-org/other-repo"]
            )
        # No partial save: the preference stays unset.
        assert await manager.get_active_repos(user_id) is None


class TestActiveReposConstants:
    """Smoke checks on exported constants."""

    def test_preference_key_is_stable(self):
        """Renaming the persisted key would break user data — guard it."""
        assert ACTIVE_REPOS == "active_repos"

    def test_distinct_from_default_repo_key(self):
        """The two preferences are distinct — accidentally aliasing them
        would conflate single-value and list-value semantics."""
        from services.domain.user_preference_manager import DEFAULT_REPO

        assert ACTIVE_REPOS != DEFAULT_REPO
