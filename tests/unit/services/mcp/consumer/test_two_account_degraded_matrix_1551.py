"""#1551 workstream 5, the behaviour half (Arch's design 2026-11-04 15:54; xian: it lands
before any new invite): the two-account degraded matrix for GitHub.

Account A is healthy: a bound binding with a readable grant, a personal token, a saved
handle and a saved default repository. Account B is bound too but BROKEN in one of four
ways: no grant, an unreadable grant, no handle, no default repository. The deployment
carries an env token, an env handle and an env default repository. Every chokepoint a
user-facing GitHub read or write passes through must answer for B from B's own state,
or refuse; it must never answer with A's value or the deployment's.

The chokepoints (every GitHub chat handler reaches GitHub through these):
- ``GitHubMCPSpatialAdapter.resolve_credential``: the credential for a principal;
- ``GitHubMCPSpatialAdapter._grant_headers_or_raise``: the bearer the client sends;
- ``repo_resolver.read_user_github_handle``: the identity behind "assigned to me";
- ``repo_resolver.resolve_repo``: the repository a read or write targets.
The #2266 pins (no connect without a bearer; env handle never a real account's) are
the first two cells; the matrix holds them against a healthy neighbour.
"""

from __future__ import annotations

import contextlib
from unittest.mock import AsyncMock, patch
from uuid import UUID

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.connectors.binding_repository import ConnectorBindingRepository
from services.database.models import ConnectorBinding
from services.integrations.github import repo_resolver as rr
from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.security.user_api_key_service import UserKeyReadFailed

pytestmark = pytest.mark.asyncio

A = "aaaaaaaa-1551-4b00-9e00-00000000000a"
B = "bbbbbbbb-1551-4b00-9e00-00000000000b"
A_GRANT, A_PAT, A_HANDLE, A_REPO = "gho_account_a", "ghp_account_a", "alice", "alice/repo"
ENV_TOKEN, ENV_HANDLE, ENV_REPO = "ghp_deployment", "mediajunkie", "mediajunkie/deployment"
FORBIDDEN_FOR_B = (A_GRANT, A_PAT, A_HANDLE, A_REPO, ENV_TOKEN, ENV_HANDLE, ENV_REPO)

STATES = ("no_grant", "unreadable_grant", "no_handle", "no_default_repo")


@pytest_asyncio.fixture
async def two_accounts(monkeypatch):
    """Both accounts BOUND in a real binding table; the per-account stores are seams keyed
    by account id, so A's values are present in the same process while B is read."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    async with maker() as s:
        repo = ConnectorBindingRepository(s)
        await repo.upsert(A, "github", status="bound", mcp_server_ref="github")
        await repo.upsert(B, "github", status="bound", mcp_server_ref="github")
        await s.commit()

    monkeypatch.setenv("GITHUB_TOKEN", ENV_TOKEN)
    monkeypatch.setenv("PIPER_GITHUB_HANDLE", ENV_HANDLE)
    monkeypatch.setenv("PIPER_DEFAULT_REPO", ENV_REPO)
    monkeypatch.setenv("FLY_APP_NAME", "piper-morgan")  # hosted: the env token is the host's
    yield maker
    await engine.dispose()


def _seams(monkeypatch, state: str):
    """A has everything; B is broken in ``state``. Everything B lacks is absent, not A's."""
    grants = {A: A_GRANT}
    pats = {A: A_PAT}
    handles = {A: A_HANDLE}
    repos = {A: A_REPO}
    if state == "unreadable_grant":

        async def _grant(owner_id):
            if str(owner_id) == B:
                raise UserKeyReadFailed("decrypt failed")
            return grants.get(str(owner_id))

    else:

        async def _grant(owner_id):
            return grants.get(str(owner_id))

    if state in ("no_handle", "no_default_repo"):
        # B's grant is fine in these two states; only the identity or the target is missing.
        grants[B] = "gho_account_b"
    if state != "no_handle":
        handles[B] = "bob"
    if state != "no_default_repo":
        repos[B] = "bob/repo"

    async def _pat(user_id):
        return pats.get(str(user_id))

    monkeypatch.setattr(GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(_grant))
    monkeypatch.setattr(GitHubMCPSpatialAdapter, "account_pat", staticmethod(_pat))

    class _Configs:
        def __init__(self, session):
            pass

        async def get_config(self, user_id, connector):
            h = handles.get(str(user_id))
            return {"github_username": h} if h else {}

        async def get_default_repo(self, user_id):
            return repos.get(str(user_id))

        async def get_default_repo_source(self, user_id):
            return "user_default" if str(user_id) in repos else None

    monkeypatch.setattr("services.connectors.config_service.ConnectorConfigService", _Configs)
    # The read-time recovery (#1590) would ask GitHub; here it finds nothing for B.
    monkeypatch.setattr(rr, "_attempt_default_repo_recovery", AsyncMock(return_value=None))
    return grants


def _nothing_forbidden(value):
    text = str(value)
    for bad in FORBIDDEN_FOR_B:
        assert (
            bad not in text
        ), f"B's answer carries another account's or the deployment's value: {bad}"


class TestTheHealthyNeighbourProvesTheSeams:
    @pytest.mark.parametrize("state", STATES)
    async def test_a_reads_its_own_everything(self, two_accounts, monkeypatch, state):
        _seams(monkeypatch, state)
        cred = await GitHubMCPSpatialAdapter().resolve_credential(A)
        assert isinstance(cred, GitHubCredential) and cred.token == A_GRANT and cred.leg == "oauth"
        assert await rr.read_user_github_handle(A) == A_HANDLE
        resolved = await rr.resolve_repo(user_id=UUID(A))
        assert resolved is not None and f"{resolved.owner}/{resolved.name}" == A_REPO


class TestAccountBNeverGetsAnothersValue:
    @pytest.mark.parametrize("state", STATES)
    async def test_credential(self, two_accounts, monkeypatch, state):
        _seams(monkeypatch, state)
        cred = await GitHubMCPSpatialAdapter().resolve_credential(B)
        if state == "no_grant":
            assert isinstance(cred, DegradationResponse)
            assert cred.reason is DegradationReason.STALE_TOKEN  # re-authorize, no PAT of B's
        elif state == "unreadable_grant":
            assert isinstance(cred, DegradationResponse)
            assert cred.reason is DegradationReason.UNREACHABLE  # refuse, never guess
        else:
            assert isinstance(cred, GitHubCredential) and cred.token == "gho_account_b"
        _nothing_forbidden(getattr(cred, "token", None))
        _nothing_forbidden(getattr(cred, "user_message", ""))

    @pytest.mark.parametrize("state", ("no_grant", "unreadable_grant"))
    async def test_no_bearer_is_ever_sent_for_b(self, two_accounts, monkeypatch, state):
        _seams(monkeypatch, state)
        with pytest.raises((GitHubReadFailed, gh_mod.GitHubGrantMissing)):
            await GitHubMCPSpatialAdapter()._grant_headers_or_raise(B)

    @pytest.mark.parametrize("state", STATES)
    async def test_handle(self, two_accounts, monkeypatch, state):
        _seams(monkeypatch, state)
        handle = await rr.read_user_github_handle(B)
        if state == "no_handle":
            assert handle is None  # no filter, never the env handle or A's
        else:
            assert handle == "bob"
        _nothing_forbidden(handle)

    @pytest.mark.parametrize("state", STATES)
    async def test_default_repo(self, two_accounts, monkeypatch, state):
        _seams(monkeypatch, state)
        if state == "no_default_repo":
            # The honest refusal: the caller asks which repository; never the env
            # repo or A's. (#1590's recovery found nothing for B above.)
            with pytest.raises(rr.UnresolvedRepoError) as exc:
                await rr.resolve_repo(user_id=UUID(B))
            _nothing_forbidden(exc.value)
            return
        resolved = await rr.resolve_repo(user_id=UUID(B))
        assert f"{resolved.owner}/{resolved.name}" == "bob/repo"
        _nothing_forbidden(resolved)

    async def test_the_system_principal_is_the_only_reader_of_the_env_values(
        self, two_accounts, monkeypatch
    ):
        """The 13:16 family rule's other half: with no principal at all the deployment's
        own values apply (system jobs), and only then."""
        _seams(monkeypatch, "no_grant")
        assert await rr.read_user_github_handle(None) == ENV_HANDLE
        resolved = await rr.resolve_repo(user_id=None)
        assert resolved is not None and f"{resolved.owner}/{resolved.name}" == ENV_REPO
