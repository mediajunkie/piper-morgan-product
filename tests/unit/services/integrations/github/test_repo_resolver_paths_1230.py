"""#1230 — per-path reachability proof-tests for resolve_repo.

The failure #1230 guards against: a resolution-order reorder (the order churned 3× in
~5 weeks) silently leaving a *code*-dead branch — a path that can never be reached.
Each test sets up inputs so that ONLY one path is live (earlier paths return None) and
asserts resolve_repo returns THAT path's source label. If a path is reordered, shadowed,
or removed, its test falls through to a different source / UnresolvedRepoError and fails
loudly.

RETIRED (#1315, 2026-07-04): the project-scoped and default-project paths were removed
from resolve_repo (project_repository_links/repositories were empty system-wide with no
population path; PM ruled retire over ship). Their proof-tests are removed with them —
the remaining decision tree is explicit > user_default > env_var > unresolved.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.integrations.github import repo_resolver as rr
from services.integrations.github.repo_resolver import (
    ENV_DEFAULT_REPO,
    UnresolvedRepoError,
    resolve_repo,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def _all_db_paths_off():
    """Default the DB-backed helper to 'no data' (None) so each test lights up
    exactly one path. Individual tests override the helper for the path they prove."""
    with (
        patch.object(rr, "_read_user_default_repo_from_db", new=AsyncMock(return_value=None)),
        patch.dict("os.environ", {}, clear=False),
    ):
        # ensure the env path is off unless a test sets it
        import os

        os.environ.pop(ENV_DEFAULT_REPO, None)
        yield


async def test_path1_explicit_wins():
    got = await resolve_repo(user_id=uuid4(), explicit="octo/repo")
    assert (got.owner, got.name, got.source) == ("octo", "repo", "explicit")


async def test_path2_user_default_reachable():
    rr._read_user_default_repo_from_db.return_value = "o/userdef"
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "user_default"


async def test_path3_env_var_reachable():
    import os

    os.environ[ENV_DEFAULT_REPO] = "o/envrepo"
    got = await resolve_repo(user_id=uuid4())
    assert got.source == "env_var"


async def test_path4_unresolved_when_all_paths_dry():
    with pytest.raises(UnresolvedRepoError):
        await resolve_repo(user_id=uuid4())


async def test_order_explicit_beats_user_default():
    """Ordering proof: when BOTH explicit and user-default have data, explicit wins —
    catches a reorder that would flip their precedence."""
    rr._read_user_default_repo_from_db.return_value = "o/userdef"
    got = await resolve_repo(user_id=uuid4(), explicit="explicit/repo")
    assert got.source == "explicit"
