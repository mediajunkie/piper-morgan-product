"""Unit tests for #1314 "default default" auto-default repo logic.

PM's rule (2026-07-04, verbatim): "default is easy if one exists. if multiple exist
and none is designated as primary/default by user then first/oldest active one should
be system default."

Covers:
- `compute_default_default`: the pure selection function (empty / single / multiple /
  all-archived-fallback / missing-created_at edge cases).
- `apply_default_default_if_unset`: the persistence wrapper — never overwrites an
  existing preference, no-ops on empty repos, sets the computed default otherwise.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.repo_resolver import (
    apply_default_default_if_unset,
    compute_default_default,
)


def _repo(full_name: str, created_at=None, archived: bool = False) -> dict:
    return {"full_name": full_name, "created_at": created_at, "archived": archived}


class TestComputeDefaultDefault:
    """Pure selection function: empty / single / multiple / all-archived / missing-dates."""

    def test_empty_list_returns_none(self):
        assert compute_default_default([]) is None

    def test_single_repo_used_regardless_of_fields(self):
        # PM: "default is easy if one exists" — no created_at/archived needed.
        assert compute_default_default([_repo("owner/only")]) == "owner/only"

    def test_single_archived_repo_still_used(self):
        assert compute_default_default([_repo("owner/only", archived=True)]) == "owner/only"

    def test_multiple_repos_oldest_active_wins(self):
        repos = [
            _repo("owner/newer", created_at="2026-05-01T00:00:00Z"),
            _repo("owner/oldest", created_at="2026-01-01T00:00:00Z"),
            _repo("owner/middle", created_at="2026-03-01T00:00:00Z"),
        ]
        assert compute_default_default(repos) == "owner/oldest"

    def test_archived_skipped_even_if_older(self):
        repos = [
            _repo("owner/archived-oldest", created_at="2020-01-01T00:00:00Z", archived=True),
            _repo("owner/active-newer", created_at="2026-01-01T00:00:00Z", archived=False),
        ]
        assert compute_default_default(repos) == "owner/active-newer"

    def test_all_archived_falls_back_to_oldest_overall(self):
        """Edge case PM's rule didn't name: some default beats no default."""
        repos = [
            _repo("owner/newer-archived", created_at="2026-05-01T00:00:00Z", archived=True),
            _repo("owner/oldest-archived", created_at="2026-01-01T00:00:00Z", archived=True),
        ]
        assert compute_default_default(repos) == "owner/oldest-archived"

    def test_missing_created_at_sorts_after_dated_repos(self):
        repos = [
            _repo("owner/no-date"),
            _repo("owner/dated", created_at="2026-06-01T00:00:00Z"),
        ]
        assert compute_default_default(repos) == "owner/dated"

    def test_all_missing_created_at_still_returns_a_repo(self):
        repos = [_repo("owner/a"), _repo("owner/b")]
        assert compute_default_default(repos) in ("owner/a", "owner/b")


class TestApplyDefaultDefaultIfUnset:
    """Persistence wrapper: never overwrites, no-ops on empty repos, sets otherwise."""

    def _patch_config_service(self, mock_config_service):
        return patch(
            "services.connectors.config_service.ConnectorConfigService",
            return_value=mock_config_service,
        ), patch("services.database.session_factory.AsyncSessionFactory.session_scope")

    async def test_never_overwrites_existing_preference(self):
        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(return_value="existing/repo")
        mock_config_service.set_default_repo = AsyncMock()

        patch_config, patch_scope = self._patch_config_service(mock_config_service)
        with patch_config, patch_scope as mock_scope:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            await apply_default_default_if_unset(
                "user-1", [_repo("owner/candidate")]
            )

        mock_config_service.set_default_repo.assert_not_awaited()

    async def test_sets_computed_default_when_unset(self):
        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(return_value=None)
        mock_config_service.set_default_repo = AsyncMock()

        repos = [
            _repo("owner/newer", created_at="2026-05-01T00:00:00Z"),
            _repo("owner/oldest", created_at="2026-01-01T00:00:00Z"),
        ]

        patch_config, patch_scope = self._patch_config_service(mock_config_service)
        with patch_config, patch_scope as mock_scope:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            await apply_default_default_if_unset("user-1", repos)

        mock_config_service.set_default_repo.assert_awaited_once_with("user-1", "owner/oldest")

    async def test_noop_on_empty_repos(self):
        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(return_value=None)
        mock_config_service.set_default_repo = AsyncMock()

        patch_config, patch_scope = self._patch_config_service(mock_config_service)
        with patch_config, patch_scope as mock_scope:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            await apply_default_default_if_unset("user-1", [])

        mock_config_service.set_default_repo.assert_not_awaited()
