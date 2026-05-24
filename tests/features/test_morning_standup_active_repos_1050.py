"""Tests for the #1050 STANDUP-ACTIVE-REPOS 4-step resolution chain.

Covers `MorningStandupWorkflow._resolve_active_repos` (the chain) and
`_resolve_repos_from_default_project` (path 1 implementation), introduced
in Increment 2 to add project-scoped resolution alongside the existing
preference-based paths.

Resolution chain:
  1. Project-scoped (default Project's linked active Repositories)
  2. User's `active_repos` preference (None = unset → fall through; [] =
     explicit empty → respect)
  3. `default_repo` preference single-element fallback (#1042 interim)
  4. Empty + structured-log warning
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.features.morning_standup import MorningStandupWorkflow


# -------------------------------------------------------------------
# Fixtures
# -------------------------------------------------------------------


def _make_workflow(
    *,
    active_repos_pref=None,
    default_repo_pref=None,
) -> MorningStandupWorkflow:
    """Construct a workflow with mocked deps.

    `active_repos_pref` / `default_repo_pref` configure what the mocked
    preference manager returns for the typed accessors.
    """
    preference_manager = MagicMock()
    preference_manager.get_active_repos = AsyncMock(return_value=active_repos_pref)
    preference_manager.get_default_repo = AsyncMock(return_value=default_repo_pref)

    session_manager = MagicMock()
    github_domain_service = MagicMock()

    return MorningStandupWorkflow(
        preference_manager=preference_manager,
        session_manager=session_manager,
        github_domain_service=github_domain_service,
        user_id=str(uuid4()),  # Valid UUID by default
    )


# -------------------------------------------------------------------
# _resolve_active_repos — chain behavior (paths 1→2→3→4)
# -------------------------------------------------------------------


class TestResolveActiveReposChain:
    """The 4-step resolution chain in `_resolve_active_repos`."""

    @pytest.mark.asyncio
    async def test_path_1_wins_when_default_project_has_repos(self):
        """Path 1 fires first — if it returns non-empty, paths 2-4 skipped."""
        wf = _make_workflow(
            active_repos_pref=["pref-org/pref-repo"],  # would win at path 2
            default_repo_pref="def-org/def-repo",       # would win at path 3
        )
        with patch.object(
            wf,
            "_resolve_repos_from_default_project",
            AsyncMock(return_value=["proj-org/proj-repo-1", "proj-org/proj-repo-2"]),
        ):
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == ["proj-org/proj-repo-1", "proj-org/proj-repo-2"]
        # Preference accessors NEVER consulted when path 1 wins.
        wf.preference_manager.get_active_repos.assert_not_called()
        wf.preference_manager.get_default_repo.assert_not_called()

    @pytest.mark.asyncio
    async def test_path_2_wins_when_path_1_empty_and_pref_set(self):
        """Path 1 returns [] → fall through to path 2; pref-set wins."""
        wf = _make_workflow(active_repos_pref=["pref-org/pref-repo"])
        with patch.object(
            wf, "_resolve_repos_from_default_project", AsyncMock(return_value=[])
        ):
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == ["pref-org/pref-repo"]
        # default_repo NEVER consulted when path 2 wins.
        wf.preference_manager.get_default_repo.assert_not_called()

    @pytest.mark.asyncio
    async def test_path_2_explicit_empty_respected(self):
        """`active_repos=[]` is "user said no" — respect it; don't fall through.

        This is the load-bearing None-vs-[] distinction from Increment 1:
        a user who explicitly empties their active_repos preference is
        OPTING OUT of repo activity in the standup, not asking for the
        default_repo fallback.
        """
        wf = _make_workflow(
            active_repos_pref=[],            # Explicit empty
            default_repo_pref="def-org/def-repo",  # Would win at path 3 if consulted
        )
        with patch.object(
            wf, "_resolve_repos_from_default_project", AsyncMock(return_value=[])
        ):
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == []  # Explicit empty preserved
        wf.preference_manager.get_default_repo.assert_not_called()

    @pytest.mark.asyncio
    async def test_path_3_wins_when_paths_1_2_empty_and_default_repo_set(self):
        """Path 1 empty + path 2 unset (None) → path 3 fallback."""
        wf = _make_workflow(
            active_repos_pref=None,  # Unset
            default_repo_pref="def-org/def-repo",
        )
        with patch.object(
            wf, "_resolve_repos_from_default_project", AsyncMock(return_value=[])
        ):
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == ["def-org/def-repo"]

    @pytest.mark.asyncio
    async def test_path_4_empty_when_all_paths_empty(self):
        """All paths empty → return [] + warning log."""
        wf = _make_workflow(active_repos_pref=None, default_repo_pref=None)
        with patch.object(
            wf, "_resolve_repos_from_default_project", AsyncMock(return_value=[])
        ), patch.object(wf, "logger") as mock_logger:
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == []
        # Warning log was emitted.
        mock_logger.warning.assert_called_once()
        warn_msg = mock_logger.warning.call_args.args[0]
        assert "Issues #1042, #1050" in warn_msg


class TestResolveActiveReposInvalidUserId:
    """Resolution when user_id isn't UUID-parseable."""

    @pytest.mark.asyncio
    async def test_invalid_user_id_skips_preferences_and_warns(self):
        """If user_id doesn't parse as UUID, can't call typed pref accessors
        (which expect UUID). Return empty + warning. Path 1 still attempted
        (it doesn't need user_id today since `get_default_project` is global)."""
        wf = _make_workflow()
        wf.user_id = "not-a-uuid"  # Override to invalid value
        with patch.object(
            wf, "_resolve_repos_from_default_project", AsyncMock(return_value=[])
        ), patch.object(wf, "logger") as mock_logger:
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == []
        mock_logger.warning.assert_called_once()
        warn_msg = mock_logger.warning.call_args.args[0]
        assert "user_id missing or invalid" in warn_msg

    @pytest.mark.asyncio
    async def test_invalid_user_id_still_uses_path_1_when_available(self):
        """Path 1 doesn't depend on a parseable user_id — if default
        project has repos, it wins even with bogus user_id."""
        wf = _make_workflow()
        wf.user_id = "not-a-uuid"
        with patch.object(
            wf,
            "_resolve_repos_from_default_project",
            AsyncMock(return_value=["proj-org/proj-repo"]),
        ):
            result = await wf._resolve_active_repos(wf.user_id)
        assert result == ["proj-org/proj-repo"]


# -------------------------------------------------------------------
# _resolve_repos_from_default_project — path 1 helper
# -------------------------------------------------------------------


class TestResolveReposFromDefaultProject:
    """The DB-touching path-1 helper."""

    @pytest.mark.asyncio
    async def test_returns_active_repo_full_names_from_default_project(self):
        """Happy path: default project has 2 active repos; we get
        `owner/name` strings."""
        wf = _make_workflow()

        # Mock Project with 2 active repos
        repo_a = MagicMock(full_name="org-a/repo-a", is_active=True)
        repo_b = MagicMock(full_name="org-b/repo-b", is_active=True)
        project = MagicMock(repositories=[repo_a, repo_b])

        with self._patch_default_project(project):
            result = await wf._resolve_repos_from_default_project()
        assert result == ["org-a/repo-a", "org-b/repo-b"]

    @pytest.mark.asyncio
    async def test_filters_out_inactive_repos(self):
        """Inactive repos (is_active=False) are excluded from path-1 result."""
        wf = _make_workflow()

        active_repo = MagicMock(full_name="org/active-repo", is_active=True)
        inactive_repo = MagicMock(full_name="org/inactive-repo", is_active=False)
        project = MagicMock(repositories=[active_repo, inactive_repo])

        with self._patch_default_project(project):
            result = await wf._resolve_repos_from_default_project()
        assert result == ["org/active-repo"]

    @pytest.mark.asyncio
    async def test_no_default_project_returns_empty(self):
        """If `get_default_project` returns None, helper returns []."""
        wf = _make_workflow()
        with self._patch_default_project(None):
            result = await wf._resolve_repos_from_default_project()
        assert result == []

    @pytest.mark.asyncio
    async def test_project_with_no_repos_returns_empty(self):
        """Default project exists but has no linked repos → []."""
        wf = _make_workflow()
        project = MagicMock(repositories=[])
        with self._patch_default_project(project):
            result = await wf._resolve_repos_from_default_project()
        assert result == []

    @pytest.mark.asyncio
    async def test_project_with_only_inactive_repos_returns_empty(self):
        """All repos inactive → all filtered → []."""
        wf = _make_workflow()
        inactive_repo = MagicMock(full_name="org/inactive", is_active=False)
        project = MagicMock(repositories=[inactive_repo])
        with self._patch_default_project(project):
            result = await wf._resolve_repos_from_default_project()
        assert result == []

    @pytest.mark.asyncio
    async def test_repo_with_empty_full_name_skipped(self):
        """Defensive: skip repo entries with falsy full_name."""
        wf = _make_workflow()
        good_repo = MagicMock(full_name="org/good", is_active=True)
        bad_repo = MagicMock(full_name="", is_active=True)
        project = MagicMock(repositories=[good_repo, bad_repo])
        with self._patch_default_project(project):
            result = await wf._resolve_repos_from_default_project()
        assert result == ["org/good"]

    @pytest.mark.asyncio
    async def test_db_error_returns_empty_fail_graceful(self):
        """If the DB session blows up, return [] (don't propagate); log a
        warning so the failure is observable in production."""
        wf = _make_workflow()

        # Make session_scope raise when entered.
        from services.database import session_factory as sf_mod
        with patch.object(
            sf_mod.AsyncSessionFactory,
            "session_scope",
            side_effect=RuntimeError("DB unavailable"),
        ), patch.object(wf, "logger") as mock_logger:
            result = await wf._resolve_repos_from_default_project()
        assert result == []
        mock_logger.warning.assert_called_once()

    @staticmethod
    def _patch_default_project(project):
        """Build the context-manager+patch chain for the DB layer.

        Returns a context manager you can `with` over — inside, the
        session_scope yields a session whose ProjectRepository returns
        `project` from get_default_project.
        """
        # Build async context manager mock for session_scope
        cm = MagicMock()
        cm.__aenter__ = AsyncMock(return_value=MagicMock())  # The session
        cm.__aexit__ = AsyncMock(return_value=None)

        # ProjectRepository class mock — instantiates to an instance whose
        # get_default_project returns our test project
        repo_instance = MagicMock()
        repo_instance.get_default_project = AsyncMock(return_value=project)

        from services.database import session_factory as sf_mod
        from services.database import repositories as repos_mod

        return _MultiPatch(
            patch.object(sf_mod.AsyncSessionFactory, "session_scope", return_value=cm),
            patch.object(repos_mod, "ProjectRepository", return_value=repo_instance),
        )


class _MultiPatch:
    """Tiny composite context manager — enters/exits a list of patches in order."""

    def __init__(self, *patches):
        self._patches = patches

    def __enter__(self):
        self._entered = [p.__enter__() for p in self._patches]
        return self._entered

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exit in reverse order
        for p in reversed(self._patches):
            p.__exit__(exc_type, exc_val, exc_tb)
        return False
