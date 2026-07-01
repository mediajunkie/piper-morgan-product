"""#1230 — per-path reachability proof-tests for resolve_repo.

The failure #1230 guards against: a resolution-order reorder (the order churned 3× in
~5 weeks) silently leaving a *code*-dead branch — a path that can never be reached.
Each test sets up inputs so that ONLY one path is live (earlier paths return None) and
asserts resolve_repo returns THAT path's source label. If a path is reordered, shadowed,
or removed, its test falls through to a different source / UnresolvedRepoError and fails
loudly. (Empty *data* is a separate concern — population is #1199/#1314/#1315; these
tests prove the code paths are wired, not that prod data exists.)
"""

from __future__ import annotations

import logging
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.integrations.github import repo_resolver as rr
from services.integrations.github.repo_resolver import (
    ENV_DEFAULT_REPO,
    ResolvedRepo,
    UnresolvedRepoError,
    resolve_repo,
)

# Real function reference captured BEFORE the autouse fixture patches the module
# attribute — the guard tests exercise the real helper's branches, not the mock.
_real_resolve_default_project = rr._resolve_from_default_project

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def _all_db_paths_off():
    """Default every DB-backed helper to 'no data' (None) so each test lights up
    exactly one path. Individual tests override the helper for the path they prove."""
    with (
        patch.object(rr, "_resolve_from_project", new=AsyncMock(return_value=None)),
        patch.object(rr, "_resolve_from_default_project", new=AsyncMock(return_value=None)),
        patch.object(rr, "_read_user_default_repo_from_db", new=AsyncMock(return_value=None)),
        patch.dict("os.environ", {}, clear=False),
    ):
        # ensure the env path is off unless a test sets it
        import os

        os.environ.pop(ENV_DEFAULT_REPO, None)
        yield


async def test_path1_explicit_wins():
    got = await resolve_repo(user_id=uuid4(), project_id="p", explicit="octo/repo")
    assert (got.owner, got.name, got.source) == ("octo", "repo", "explicit")


async def test_path2_project_reachable():
    rr._resolve_from_project.return_value = ResolvedRepo("o", "proj", source="project")
    got = await resolve_repo(user_id=uuid4(), project_id="p-123")
    assert got.source == "project"


async def test_path3_default_project_reachable():
    # no explicit, no project_id → path 3 (user's default project) is first live path
    rr._resolve_from_default_project.return_value = ResolvedRepo("o", "dp", source="default_project")
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "default_project"


async def test_path4_user_default_reachable():
    # default-project None (autouse) → falls to user-default preference
    rr._read_user_default_repo_from_db.return_value = "o/userdef"
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "user_default"


async def test_path5_env_var_reachable():
    import os

    os.environ[ENV_DEFAULT_REPO] = "o/envrepo"
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "env_var"


async def test_path6_unresolved_when_all_paths_dry():
    with pytest.raises(UnresolvedRepoError):
        await resolve_repo(user_id=uuid4())


async def test_order_default_project_beats_user_default():
    """Ordering proof: when BOTH path 3 and path 4 have data, path 3 (default project)
    wins — catches a reorder that would flip their precedence."""
    rr._resolve_from_default_project.return_value = ResolvedRepo("o", "dp", source="default_project")
    rr._read_user_default_repo_from_db.return_value = "o/userdef"
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "default_project"


# ---- the #1230 default-project observability guard ----


def _session_scope_returning(scalar_value):
    """Build a mocked AsyncSessionFactory whose session.execute().scalar_one_or_none()
    returns scalar_value (the default-project id, or None)."""
    from unittest.mock import MagicMock

    result = MagicMock()
    result.scalar_one_or_none = MagicMock(return_value=scalar_value)
    session = MagicMock()
    session.execute = AsyncMock(return_value=result)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope.return_value = cm
    return factory


async def test_guard_logs_no_default_project(caplog):
    """Guard case A: user has no default project → distinct debug message, None result."""
    with patch(
        "services.database.session_factory.AsyncSessionFactory",
        _session_scope_returning(None),
    ):
        with caplog.at_level(logging.DEBUG, logger=rr.logger.name):
            caplog.clear()
            out = await _real_resolve_default_project(uuid4())
    assert out is None
    assert any("has no default project" in r.getMessage() for r in caplog.records)


async def test_guard_logs_default_project_has_no_link(caplog):
    """Guard case B: default project exists but has no linked repo → distinct message
    (different remediation than case A), None result."""
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory",
            _session_scope_returning("proj-1"),
        ),
        patch.object(rr, "_resolve_from_project", new=AsyncMock(return_value=None)),
    ):
        with caplog.at_level(logging.DEBUG, logger=rr.logger.name):
            caplog.clear()
            out = await _real_resolve_default_project(uuid4())
    assert out is None
    assert any("has no linked repo" in r.getMessage() for r in caplog.records)
