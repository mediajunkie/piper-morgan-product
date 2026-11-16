"""#2379 (Arch 2026-11-15 15:49): on a GitHub App grant, a read of one repository
(branches, releases, one issue, and the close/reopen probe) runs only when the App is
installed on that repository.

Before this, those reads called github-mcp-server with ``{owner, repo}`` on the App
user token, which can read a public repository with no installation. So a person could
get branches or an issue from a repository they never gave the App, while "my
repositories" (#2342) and "my issues" (#2374) left it out.

Layer: unit. The MCP client, the repository resolver and the installation read are
fakes; nothing calls GitHub. Not covered here: the write paths (create, update,
comment), which Arch ruled get the same check before the confirm; they are a later unit.
"""

from __future__ import annotations

import contextlib
import json
from typing import Any, Dict, List
from unittest.mock import AsyncMock

import pytest

from services.integrations.github.repo_resolver import ResolutionSource, ResolvedRepo
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer import github_app_install as install_mod
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    DETAIL_APP_NOT_ON_REPOSITORY,
    InstallationReadFailed,
    InstalledRepositories,
    installation_read_scope,
)

pytestmark = pytest.mark.asyncio

_OWNER = "11111111-1111-1111-1111-111111111111"
_ISSUE = json.dumps({"number": 7, "title": "t", "state": "open", "html_url": "u"})
_LIST = json.dumps([{"name": "main", "tag_name": "v1"}])


@pytest.fixture(autouse=True)
def _install_link(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_SLUG, "piper-example")


def _credential(leg="oauth", app_grant=True):
    return GitHubCredential(
        owner_id=_OWNER, mcp_server_ref="github", token="access-live", leg=leg, app_grant=app_grant
    )


def _installed(*names):
    return InstalledRepositories(
        installations=1 if names else 0,
        repositories=[
            {"id": i, "name": n.split("/")[1], "full_name": n} for i, n in enumerate(names)
        ],
    )


def _adapter(monkeypatch, installed, *, credential=None, target="octo/public"):
    """An adapter that resolves every read to ``target``, records each MCP call, and
    whose installation read answers ``installed``."""
    seen: List[Dict[str, Any]] = []

    class _Client:
        async def call_tool(self, tool, args):
            seen.append({"tool": tool, **args})
            return _ISSUE if tool == gh_mod._ISSUE_READ_TOOL else _LIST

    @contextlib.asynccontextmanager
    async def _ctx(_binding):
        yield _Client()

    owner, name = target.split("/")
    monkeypatch.setattr(
        gh_mod,
        "resolve_repo",
        AsyncMock(
            return_value=ResolvedRepo(owner=owner, name=name, source=list(ResolutionSource)[0])
        ),
    )
    adapter = GitHubMCPSpatialAdapter()
    adapter.resolve_credential = AsyncMock(return_value=credential or _credential())
    adapter._mcp_client_ctx = _ctx
    monkeypatch.setattr(GitHubMCPSpatialAdapter, "_tool_text", classmethod(lambda cls, r: r))
    read = (
        AsyncMock(side_effect=installed)
        if isinstance(installed, Exception)
        else AsyncMock(return_value=installed)
    )
    monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
    return adapter, seen, read


#: name -> (the call, the attribute that holds what was read)
_READS = {
    "branches": (lambda a: a.list_branches_connector(_OWNER), "items"),
    "releases": (lambda a: a.list_releases_connector(_OWNER), "items"),
    "one issue": (lambda a: a.get_issue_connector(_OWNER, issue_number=7), "item"),
}


@pytest.mark.parametrize("read_name", sorted(_READS))
class TestARepoScopedReadOnAnAppGrant:
    async def test_installed_on_the_repository_reads_it(self, monkeypatch, read_name):
        call, holds = _READS[read_name]
        adapter, seen, read = _adapter(monkeypatch, _installed("octo/a", "octo/public"))
        result = await call(adapter)
        assert result.degradation is None
        assert getattr(result, holds)
        assert [(s["owner"], s["repo"]) for s in seen] == [("octo", "public")]
        read.assert_awaited_once_with("access-live")

    async def test_the_match_ignores_case(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("Octo/Public"))
        result = await call(adapter)
        assert result.degradation is None and len(seen) == 1

    async def test_not_installed_on_it_refuses_with_no_client_call(self, monkeypatch, read_name):
        call, holds = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await call(adapter)
        assert seen == []  # the public repository was never read
        assert getattr(result, holds) is None
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_ON_REPOSITORY
        assert result.degradation.user_message == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_REPLY

    async def test_not_installed_on_it_with_no_install_link_is_the_on_our_side_line(
        self, monkeypatch, read_name
    ):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await call(adapter)
        assert seen == []
        assert result.degradation.detail == DETAIL_APP_INSTALL_LINK_MISSING

    async def test_installed_nowhere_is_the_install_step(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed())
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED

    @pytest.mark.parametrize("status", [None, 403, 500])
    async def test_a_failed_installation_read_degrades_and_never_reads(
        self, monkeypatch, read_name, status
    ):
        call, holds = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(status))
        result = await call(adapter)
        assert seen == []
        assert getattr(result, holds) is None
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    async def test_a_401_on_the_installation_read_is_the_stale_path(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(401))
        adapter._rejected_token_was_replaced = AsyncMock(return_value=False)
        adapter._mark_oauth_binding_stale = AsyncMock()
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.STALE_TOKEN

    async def test_a_malformed_installed_name_fails_the_read(self, monkeypatch, read_name):
        call, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/public", "not a name/x y"))
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    @pytest.mark.parametrize(
        "credential",
        [_credential(leg="pat", app_grant=False), _credential(leg="oauth", app_grant=False)],
        ids=["personal token", "classic grant"],
    )
    async def test_the_other_legs_make_no_installation_read(
        self, monkeypatch, read_name, credential
    ):
        call, holds = _READS[read_name]
        adapter, seen, read = _adapter(
            monkeypatch, AssertionError("no installation read"), credential=credential
        )
        result = await call(adapter)
        assert result.degradation is None and getattr(result, holds)
        assert len(seen) == 1
        read.assert_not_awaited()


class TestTheCloseReopenProbe:
    async def test_installed_reads_the_issue(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/public"))
        status, item, repo = await adapter.probe_issue_connector(_OWNER, issue_number=7)
        assert status == "found" and item["number"] == 7 and repo == "octo/public"

    @pytest.mark.parametrize(
        "installed",
        [_installed("octo/a"), _installed(), InstallationReadFailed(500)],
        ids=["not on it", "installed nowhere", "read failed"],
    )
    async def test_otherwise_unknown_with_no_client_call(self, monkeypatch, installed):
        adapter, seen, _ = _adapter(monkeypatch, installed)
        assert await adapter.probe_issue_connector(_OWNER, issue_number=7) == (
            "unknown",
            None,
            None,
        )
        assert seen == []  # never "not found" from a read that didn't run


class TestOneInstallationReadPerRequest:
    """Arch's cost ruling: once per request, held on the request, never across."""

    @pytest.fixture
    def github(self, monkeypatch):
        calls: List[str] = []
        answers: List[Any] = []

        async def _read(token):
            calls.append(token)
            answer = answers.pop(0) if answers else _installed("octo/a")
            if isinstance(answer, Exception):
                raise answer
            return answer

        monkeypatch.setattr(install_mod, "_read_installed_repositories", _read)
        return calls, answers

    async def test_outside_a_request_every_call_reads(self, github):
        calls, _ = github
        await install_mod.list_installed_repositories("t1")
        await install_mod.list_installed_repositories("t1")
        assert calls == ["t1", "t1"]

    async def test_inside_a_request_the_second_call_reuses_the_answer(self, github):
        calls, _ = github
        with installation_read_scope():
            first = await install_mod.list_installed_repositories("t1")
            second = await install_mod.list_installed_repositories("t1")
        assert calls == ["t1"] and first is second

    async def test_the_answer_is_per_token(self, github):
        calls, _ = github
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t2")
        assert calls == ["t1", "t2"]

    async def test_nothing_is_held_into_the_next_request(self, github):
        calls, answers = github
        answers.extend([_installed("octo/a"), _installed("octo/a", "octo/b")])
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
        with installation_read_scope():
            later = await install_mod.list_installed_repositories("t1")
        assert calls == ["t1", "t1"]
        assert [r["full_name"] for r in later.repositories] == ["octo/a", "octo/b"]
        assert install_mod._request_reads.get() is None

    async def test_a_failed_read_is_not_held(self, github):
        calls, answers = github
        answers.extend([InstallationReadFailed(502), _installed("octo/a")])
        with installation_read_scope():
            with pytest.raises(InstallationReadFailed):
                await install_mod.list_installed_repositories("t1")
            assert (await install_mod.list_installed_repositories("t1")).repositories
        assert calls == ["t1", "t1"]

    async def test_a_scope_inside_a_scope_keeps_the_outer_answers(self, github):
        calls, _ = github
        with installation_read_scope():
            await install_mod.list_installed_repositories("t1")
            with installation_read_scope():
                await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t1")
        assert calls == ["t1"]

    async def test_the_middleware_opens_one_scope_per_http_request(self, github):
        from web.middleware.installation_read_scope import InstallationReadScopeMiddleware

        calls, _ = github
        held_inside: List[Any] = []

        async def app(scope, receive, send):
            await install_mod.list_installed_repositories("t1")
            await install_mod.list_installed_repositories("t1")
            held_inside.append(install_mod._request_reads.get() is not None)

        wrapped = InstallationReadScopeMiddleware(app)
        await wrapped({"type": "http"}, None, None)
        await wrapped({"type": "http"}, None, None)
        assert calls == ["t1", "t1"] and held_inside == [True, True]
        await wrapped({"type": "lifespan"}, None, None)
        assert held_inside[-1] is False and len(calls) == 4  # no scope: both calls read

    async def test_the_app_registers_the_middleware(self):
        source = open("web/app.py", encoding="utf-8").read()
        assert "app.add_middleware(InstallationReadScopeMiddleware)" in source
