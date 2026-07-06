"""Unit tests for the GitHub repo-resolution helper (Issue #1042)."""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.integrations.github.repo_resolver import (
    ENV_DEFAULT_REPO,
    ResolvedRepo,
    UnresolvedRepoError,
    parse_full_name,
    resolve_repo,
)


@pytest.fixture(autouse=True)
def _db_default_repo_off():
    """WS-1 (#1226): repo_resolver now reads the DB-backed default-repo FIRST. Default it OFF
    (returns None) for every test so the existing flat-file/env/project assertions stay
    deterministic + DB-free; the DB-first tests below override this with their own patch."""
    with patch(
        "services.integrations.github.repo_resolver.get_user_default_repo",
        new=AsyncMock(return_value=None),
    ):
        yield


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
        assert resolved == ResolvedRepo(owner="myorg", name="myrepo", source="explicit")

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
        assert resolved == ResolvedRepo(owner="envowner", name="envrepo", source="env_var")

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
    """Path 3: user's ``default_repo`` preference.

    WS-1 P4 (#1226 / #1199): the resolver reads the DB-backed connector_configs store
    (``get_user_default_repo``) — the SOLE store. The flat-file store and the
    old in-memory UserPreferenceManager path are RETIRED. We patch the DB reader.
    """

    _READER = "services.integrations.github.repo_resolver.get_user_default_repo"

    async def test_user_default_used_when_set(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._READER, new=AsyncMock(return_value="userowner/userrepo")):
            resolved = await resolve_repo(user_id=uuid4())
        assert resolved == ResolvedRepo(owner="userowner", name="userrepo", source="user_default")

    async def test_user_default_none_when_no_entry_falls_through(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._READER, new=AsyncMock(return_value=None)):
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

    async def test_user_default_malformed_value_skipped(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._READER, new=AsyncMock(return_value="not-a-valid-fullname")):
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

    async def test_user_default_beats_env(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "env/repo")
        with patch(self._READER, new=AsyncMock(return_value="userowner/userrepo")):
            resolved = await resolve_repo(user_id=uuid4())
        assert resolved.source == "user_default"
        assert resolved.full_name == "userowner/userrepo"


class TestUserDefaultFromDB:
    """WS-1 P4 (#1226 / #1199): path 3 reads the DB-backed connector_configs store — the SOLE
    store. The autouse fixture defaults the DB read OFF; these tests turn it on."""

    _DB = "services.integrations.github.repo_resolver.get_user_default_repo"

    async def test_db_value_used_when_set(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._DB, new=AsyncMock(return_value="dbowner/dbrepo")):
            resolved = await resolve_repo(user_id=uuid4())
        assert resolved == ResolvedRepo(owner="dbowner", name="dbrepo", source="user_default")

    async def test_db_miss_unresolved(self, monkeypatch):
        """WS-1 P4: a DB miss yields nothing on path 3 (no second store to fall back to). With
        no env var set, resolution falls through to ``UnresolvedRepoError``."""
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._DB, new=AsyncMock(return_value=None)):
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())


class TestResolutionOrder:
    """Decision tree priority: explicit > user > env > raise.

    RETIRED (#1315, 2026-07-04): TestDefaultProjectResolution (project-scoped +
    default-project paths) removed along with the resolve_repo paths themselves.
    """

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
