"""Unit tests for the GitHub repo-resolution helper (Issue #1042)."""

from __future__ import annotations

import os
from unittest.mock import patch
from uuid import uuid4

import pytest

from services.integrations.github.repo_resolver import (
    ENV_DEFAULT_REPO,
    ResolvedRepo,
    UnresolvedRepoError,
    parse_full_name,
    resolve_repo,
)


class TestParseFullName:
    """``owner/name`` parsing accepts valid shapes and rejects bad ones."""

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("owner/name", ("owner", "name")),
            ("octocat/hello-world", ("octocat", "hello-world")),
            ("with.dots/name_underscore", ("with.dots", "name_underscore")),
            ("MyOrg/MyRepo", ("MyOrg", "MyRepo")),
        ],
    )
    def test_parses_valid(self, value, expected):
        assert parse_full_name(value) == expected

    @pytest.mark.parametrize(
        "value",
        ["", "no-slash", "owner/", "/name", "owner/name/extra", "owner name"],
    )
    def test_rejects_invalid(self, value):
        with pytest.raises(ValueError):
            parse_full_name(value)


class TestExplicitResolution:
    """When ``explicit`` is passed, it wins over everything else."""

    async def test_explicit_returns_resolved(self):
        resolved = await resolve_repo(explicit="myorg/myrepo")
        assert resolved == ResolvedRepo(
            owner="myorg", name="myrepo", source="explicit"
        )

    async def test_explicit_wins_over_env(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "ignored/value")
        resolved = await resolve_repo(explicit="myorg/myrepo")
        assert resolved.source == "explicit"

    async def test_explicit_invalid_raises(self):
        with pytest.raises(ValueError):
            await resolve_repo(explicit="bad-shape")


class TestEnvVarFallback:
    """``PIPER_DEFAULT_REPO`` is the dev escape hatch (Q4 disposition)."""

    async def test_env_var_used_when_nothing_else_resolves(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "envowner/envrepo")
        resolved = await resolve_repo()
        assert resolved == ResolvedRepo(
            owner="envowner", name="envrepo", source="env_var"
        )

    async def test_env_var_invalid_falls_through_to_unresolved(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "bad-shape")
        with pytest.raises(UnresolvedRepoError):
            await resolve_repo()


class TestUnresolved:
    """When no path resolves, raise ``UnresolvedRepoError``."""

    async def test_unresolved_raises(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with pytest.raises(UnresolvedRepoError) as exc_info:
            await resolve_repo()
        assert "no repo could be resolved" in str(exc_info.value).lower()

    async def test_unresolved_with_user_id_no_preference(self, monkeypatch):
        # User has no default_repo preference set; should still raise.
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with pytest.raises(UnresolvedRepoError):
            await resolve_repo(user_id=uuid4())


class TestUserDefaultPreference:
    """Path 3: user's ``default_repo`` preference."""

    async def test_user_default_used_when_set(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        from services.domain.user_preference_manager import UserPreferenceManager

        user_id = uuid4()
        pm = UserPreferenceManager()
        await pm.set_default_repo(user_id, "userowner/userrepo")

        # The resolver constructs its own UserPreferenceManager via lazy
        # import inside ``_resolve_from_user_default``; patch the source
        # module so the in-test manager is used.
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=pm,
        ):
            resolved = await resolve_repo(user_id=user_id)
        assert resolved == ResolvedRepo(
            owner="userowner", name="userrepo", source="user_default"
        )


class TestResolutionOrder:
    """Decision tree priority: explicit > project > user > env > raise."""

    async def test_env_does_not_override_explicit(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "env/repo")
        resolved = await resolve_repo(explicit="caller/wins")
        assert resolved.source == "explicit"
        assert resolved.full_name == "caller/wins"


class TestResolvedRepoDataclass:
    """``ResolvedRepo`` is frozen + has full_name property."""

    def test_full_name_property(self):
        r = ResolvedRepo(owner="o", name="n", source="explicit")
        assert r.full_name == "o/n"

    def test_is_frozen(self):
        r = ResolvedRepo(owner="o", name="n", source="explicit")
        with pytest.raises(Exception):
            r.owner = "x"  # type: ignore[misc]
