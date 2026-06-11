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
    """Path 3: user's ``default_repo`` preference.

    #1192 slice (a): the resolver reads the persistent GitHub-prefs store the
    settings UI writes (``data/github_preferences.json``, via
    ``_read_user_default_repository``) — NOT the old in-memory
    UserPreferenceManager (which never resolved). We patch that reader.
    """

    _READER = "services.integrations.github.repo_resolver._read_user_default_repository"

    async def test_user_default_used_when_set(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        user_id = uuid4()
        # The reader is keyed by str(user_id); return that user's full_name.
        with patch(self._READER, side_effect=lambda key: "userowner/userrepo" if key == str(user_id) else None):
            resolved = await resolve_repo(user_id=user_id)
        assert resolved == ResolvedRepo(
            owner="userowner", name="userrepo", source="user_default"
        )

    async def test_user_default_none_when_no_entry_falls_through(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._READER, return_value=None):
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

    async def test_user_default_malformed_value_skipped(self, monkeypatch):
        monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
        with patch(self._READER, return_value="not-a-valid-fullname"):
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

    async def test_user_default_beats_env(self, monkeypatch):
        monkeypatch.setenv(ENV_DEFAULT_REPO, "env/repo")
        with patch(self._READER, return_value="userowner/userrepo"):
            resolved = await resolve_repo(user_id=uuid4())
        assert resolved.source == "user_default"
        assert resolved.full_name == "userowner/userrepo"


class TestReadUserDefaultRepository:
    """#1192 slice (a): the persistent-store reader (real JSON file I/O)."""

    def _write(self, tmp_path, monkeypatch, payload):
        import json as _json

        from services.integrations.github import repo_resolver

        f = tmp_path / "github_preferences.json"
        f.write_text(_json.dumps(payload))
        monkeypatch.setattr(repo_resolver, "_GITHUB_PREFERENCES_FILE", str(f))

    def test_returns_full_name_for_user(self, tmp_path, monkeypatch):
        from services.integrations.github.repo_resolver import _read_user_default_repository

        self._write(tmp_path, monkeypatch, {"user-abc": {"default_repository": "o/r"}})
        assert _read_user_default_repository("user-abc") == "o/r"

    def test_returns_none_for_unknown_user(self, tmp_path, monkeypatch):
        from services.integrations.github.repo_resolver import _read_user_default_repository

        self._write(tmp_path, monkeypatch, {"someone-else": {"default_repository": "o/r"}})
        assert _read_user_default_repository("user-abc") is None

    def test_returns_none_when_file_absent(self, tmp_path, monkeypatch):
        from services.integrations.github import repo_resolver
        from services.integrations.github.repo_resolver import _read_user_default_repository

        monkeypatch.setattr(
            repo_resolver, "_GITHUB_PREFERENCES_FILE", str(tmp_path / "nonexistent.json")
        )
        assert _read_user_default_repository("user-abc") is None

    def test_returns_none_when_field_missing(self, tmp_path, monkeypatch):
        from services.integrations.github.repo_resolver import _read_user_default_repository

        self._write(tmp_path, monkeypatch, {"user-abc": {"selected_repositories": ["o/r"]}})
        assert _read_user_default_repository("user-abc") is None


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
