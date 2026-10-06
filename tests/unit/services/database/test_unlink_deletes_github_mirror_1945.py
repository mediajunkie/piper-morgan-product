"""#1945 slice 2 — unlinking a repo deletes the same-project GitHub mirror.

CXO's ruling (2026-10-05): once the Config panel hides a GitHub-type project
integration that mirrors a linked repo, unlinking the repo must not leave the
mirror to reappear alone under "Project integrations" — "I unlinked it and
it's still here." Rule: unlink also deletes a ``type=GITHUB`` integration in
the same project whose ``config.repository`` equals the repo's ``full_name``.
Gate (held): nothing live reads that row — Arch found the one dormant reader
(``Project.get_github_repository``'s fallback, zero callers); it is removed
in the same commit as the setup-wizard dual-write that created the rows.

These tests drive ``RepositoryRepository.unlink_from_project`` against a
mocked session: the link delete and the mirror delete share one session and
one flush, so they land or fail together.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.database.repositories import RepositoryRepository
from services.shared_types import IntegrationType


def _result(scalar=None, scalars=None):
    r = MagicMock()
    r.scalar_one_or_none.return_value = scalar
    r.scalars.return_value.all.return_value = list(scalars or [])
    return r


def _integration(repository: str, type_=IntegrationType.GITHUB):
    m = MagicMock()
    m.type = type_
    m.config = {"repository": repository}
    return m


def _repo_with(*executes):
    session = MagicMock()
    session.execute = AsyncMock(side_effect=list(executes))
    session.delete = AsyncMock()
    session.flush = AsyncMock()
    return RepositoryRepository(session), session


@pytest.mark.asyncio
async def test_unlink_deletes_the_matching_github_mirror():
    link = MagicMock(name="link")
    mirror = _integration("owner/repo")
    repo, session = _repo_with(
        _result(scalar=link),  # the ProjectRepositoryLink row
        _result(scalar="owner/repo"),  # RepositoryDB.full_name
        _result(scalars=[mirror]),  # active GITHUB integrations in the project
    )

    assert await repo.unlink_from_project("r1", "p1") is True

    deleted = [c.args[0] for c in session.delete.await_args_list]
    assert deleted == [link, mirror]
    session.flush.assert_awaited_once()


@pytest.mark.asyncio
async def test_unlink_leaves_a_github_integration_for_a_different_repo():
    link = MagicMock(name="link")
    other = _integration("owner/other-repo")
    repo, session = _repo_with(
        _result(scalar=link),
        _result(scalar="owner/repo"),
        _result(scalars=[other]),
    )

    assert await repo.unlink_from_project("r1", "p1") is True

    deleted = [c.args[0] for c in session.delete.await_args_list]
    assert deleted == [link], "a non-mirror GitHub integration must survive the unlink"


@pytest.mark.asyncio
async def test_unlink_with_no_link_touches_nothing():
    repo, session = _repo_with(_result(scalar=None))

    assert await repo.unlink_from_project("r1", "p1") is False

    session.delete.assert_not_awaited()
    assert session.execute.await_count == 1, "no mirror lookup when there was no link to remove"


@pytest.mark.asyncio
async def test_unlink_tolerates_a_vanished_repository_row():
    link = MagicMock(name="link")
    repo, session = _repo_with(
        _result(scalar=link),
        _result(scalar=None),  # repository row gone: nothing to match on
    )

    assert await repo.unlink_from_project("r1", "p1") is True

    deleted = [c.args[0] for c in session.delete.await_args_list]
    assert deleted == [link]
    assert session.execute.await_count == 2


def test_the_dormant_fallback_reader_is_gone():
    """Arch's condition: retire the dual-write AND the fallback that read the
    mirror's ``config["repository"]`` in the same commit, so no dormant reader
    can quietly revive the mirror's meaning later."""
    from services.domain.models import Project

    assert not hasattr(Project, "get_github_repository")


def test_setup_wizard_no_longer_dual_writes():
    """The source of the mirror rows: the setup wizard's "Legacy: Also create
    ProjectIntegration" block is gone."""
    from pathlib import Path

    src = Path("web/api/routes/setup.py").read_text()
    assert "Also create ProjectIntegration" not in src
    assert 'config={"repository": repo_name}' not in src
