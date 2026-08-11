"""Read-time default-repo recovery (#1590).

Diagnosis (live Fly logs, v48, PM's 02:08Z session): ``resolve_repo`` raised
``UnresolvedRepoError`` ten times in one window — "no user default_repo, no
PIPER_DEFAULT_REPO env var" — for an account whose GitHub connector WAS bound
(Radar's binding-first gate passed). #1314's ``apply_default_default_if_unset``
exists but is wired ONLY into the OAuth callback
(``web/api/routes/settings_integrations.py``), behind ``if repos_result.repositories:``.
Any account that connected before that shipped (2026-07-04), or whose repo search
was empty/failed at that instant, is permanently stuck at zero with NO read-time
recovery: every GitHub read returns empty and the #1536 first-contact demo
correctly refuses to show anything — the exact "blank generic interface" it exists
to prevent.

The fix is at the resolver seam, so EVERY surface benefits (first-contact, Radar,
the adapter's repo-scoped reads, the router, spatial, intent handlers, and #1342's
``resolve_target``) rather than one call site.

What these tests pin:

1. GitHub-configured user + zero default repo → recovery selects the single
   accessible repo and resolution SUCCEEDS (red before the recovery exists).
2. A genuinely-zero-repo user does not loop/hammer the GitHub search API.
3. The anonymous path (``user_id=None``) is untouched — no status check, no search.
4. A user without GitHub configured never triggers a search.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.integrations.github.repo_resolver import (
    ENV_DEFAULT_REPO,
    UnresolvedRepoError,
    reset_recovery_guard,
    resolve_repo,
)

_STATUS = "services.integrations.integration_status_service.IntegrationStatusService"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"


def _repo(full_name: str, *, created_at: Optional[str] = None, archived: bool = False):
    """The normalized shape ``GitHubMCPSpatialAdapter._parse_repo_search`` emits."""
    return {
        "id": 1,
        "name": full_name.split("/", 1)[1],
        "full_name": full_name,
        "description": "",
        "created_at": created_at,
        "archived": archived,
    }


@pytest.fixture(autouse=True)
def _clean_env_and_guard(monkeypatch):
    """No env escape hatch, and a cleared once-per-user guard, per test."""
    monkeypatch.delenv(ENV_DEFAULT_REPO, raising=False)
    reset_recovery_guard()
    yield
    reset_recovery_guard()


class _StatefulConfigService:
    """Stand-in for ``ConnectorConfigService`` backed by a plain dict.

    Real ``apply_default_default_if_unset`` + ``get_user_default_repo`` run against
    it, so the #1314 selection rule and the never-overwrite guarantee stay under
    test here rather than being stubbed away.
    """

    def __init__(self, store: Dict[str, str]):
        self._store = store

    async def get_default_repo(self, user_id) -> Optional[str]:
        return self._store.get(str(user_id))

    async def set_default_repo(self, user_id, full_name: str) -> None:
        self._store[str(user_id)] = full_name


class _Ctx:
    """Async context manager yielding a dummy session."""

    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


def _patch_db(store: Dict[str, str]):
    return (
        patch(
            "services.connectors.config_service.ConnectorConfigService",
            side_effect=lambda _session: _StatefulConfigService(store),
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            side_effect=lambda *a, **k: _Ctx(),
        ),
    )


def _patch_status(configured: bool):
    instance = MagicMock()
    instance.is_configured = AsyncMock(return_value=configured)
    return patch(_STATUS, return_value=instance), instance


def _patch_search(repos: Optional[List[Dict[str, Any]]]):
    from services.mcp.consumer.github_adapter import GitHubReposResult

    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(
        return_value=GitHubReposResult(repositories=repos)
    )
    return patch(_ADAPTER, return_value=instance), instance


class TestRecoverySucceeds:
    """The #1590 case: connected user, zero default repo → recovery, then resolution."""

    async def test_single_accessible_repo_is_adopted_and_resolution_succeeds(self):
        store: Dict[str, str] = {}
        user_id = uuid4()

        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(True)
        patch_search, search = _patch_search([_repo("octocat/hello-world")])

        with patch_cfg, patch_scope, patch_status, patch_search:
            resolved = await resolve_repo(user_id=user_id)

        assert resolved.full_name == "octocat/hello-world"
        assert resolved.source == "user_default"
        # The recovery PERSISTS — the next read resolves without another search.
        assert store[str(user_id)] == "octocat/hello-world"
        search.search_user_repositories.assert_awaited_once()

    async def test_multiple_repos_use_the_1314_oldest_active_rule(self):
        store: Dict[str, str] = {}
        user_id = uuid4()

        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(True)
        patch_search, _ = _patch_search(
            [
                _repo("owner/newer", created_at="2026-05-01T00:00:00Z"),
                _repo("owner/archived-oldest", created_at="2024-01-01T00:00:00Z", archived=True),
                _repo("owner/oldest-active", created_at="2026-01-01T00:00:00Z"),
            ]
        )

        with patch_cfg, patch_scope, patch_status, patch_search:
            resolved = await resolve_repo(user_id=user_id)

        assert resolved.full_name == "owner/oldest-active"

    async def test_existing_preference_is_never_overwritten_by_recovery(self):
        """Recovery only runs when resolution already failed, so a user WITH a
        preference never reaches it — the preference resolves at path 2."""
        user_id = uuid4()
        store = {str(user_id): "mine/chosen"}

        patch_cfg, patch_scope = _patch_db(store)
        patch_status, status = _patch_status(True)
        patch_search, search = _patch_search([_repo("other/repo")])

        with patch_cfg, patch_scope, patch_status, patch_search:
            resolved = await resolve_repo(user_id=user_id)

        assert resolved.full_name == "mine/chosen"
        status.is_configured.assert_not_awaited()
        search.search_user_repositories.assert_not_awaited()


class TestZeroRepoUserDoesNotHammer:
    """A user with genuinely zero accessible repos degrades exactly as today,
    and costs ONE search — not one per read."""

    async def test_zero_repos_still_raises(self):
        store: Dict[str, str] = {}
        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(True)
        patch_search, _ = _patch_search([])

        with patch_cfg, patch_scope, patch_status, patch_search:
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

    async def test_repeated_reads_attempt_recovery_only_once(self):
        store: Dict[str, str] = {}
        user_id = uuid4()

        patch_cfg, patch_scope = _patch_db(store)
        patch_status, status = _patch_status(True)
        patch_search, search = _patch_search([])

        with patch_cfg, patch_scope, patch_status, patch_search:
            for _ in range(10):  # the live burst was ten in one window
                with pytest.raises(UnresolvedRepoError):
                    await resolve_repo(user_id=user_id)

        assert search.search_user_repositories.await_count == 1
        # The status check is inside the guard too — one probe, not ten.
        assert status.is_configured.await_count == 1

    async def test_a_failing_search_does_not_retry_on_the_next_read(self):
        store: Dict[str, str] = {}
        user_id = uuid4()
        instance = MagicMock()
        instance.search_user_repositories = AsyncMock(side_effect=RuntimeError("boom"))

        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(True)

        with patch_cfg, patch_scope, patch_status, patch(_ADAPTER, return_value=instance):
            for _ in range(3):
                with pytest.raises(UnresolvedRepoError):
                    await resolve_repo(user_id=user_id)

        assert instance.search_user_repositories.await_count == 1


class TestPrincipalSafety:
    """Anonymous callers are unchanged (audit rule): no status check, no search."""

    async def test_anonymous_caller_untouched(self):
        patch_status, status = _patch_status(True)
        patch_search, search = _patch_search([_repo("octocat/hello-world")])

        with patch_status, patch_search:
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo()

        status.is_configured.assert_not_awaited()
        search.search_user_repositories.assert_not_awaited()

    async def test_unconfigured_user_never_searches(self):
        store: Dict[str, str] = {}
        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(False)
        patch_search, search = _patch_search([_repo("octocat/hello-world")])

        with patch_cfg, patch_scope, patch_status, patch_search:
            with pytest.raises(UnresolvedRepoError):
                await resolve_repo(user_id=uuid4())

        search.search_user_repositories.assert_not_awaited()

    async def test_explicit_repo_short_circuits_before_any_recovery(self):
        patch_status, status = _patch_status(True)
        patch_search, search = _patch_search([_repo("octocat/hello-world")])

        with patch_status, patch_search:
            resolved = await resolve_repo(user_id=uuid4(), explicit="caller/wins")

        assert resolved.source == "explicit"
        status.is_configured.assert_not_awaited()
        search.search_user_repositories.assert_not_awaited()

    async def test_env_var_fallback_still_wins_before_recovery(self, monkeypatch):
        """Strictly additive: recovery fires only where today's code raises."""
        monkeypatch.setenv(ENV_DEFAULT_REPO, "envowner/envrepo")
        store: Dict[str, str] = {}
        patch_cfg, patch_scope = _patch_db(store)
        patch_status, _ = _patch_status(True)
        patch_search, search = _patch_search([_repo("octocat/hello-world")])

        with patch_cfg, patch_scope, patch_status, patch_search:
            resolved = await resolve_repo(user_id=uuid4())

        assert resolved.source == "env_var"
        search.search_user_repositories.assert_not_awaited()
