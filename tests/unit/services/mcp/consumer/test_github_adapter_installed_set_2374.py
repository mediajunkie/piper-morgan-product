"""#2374 (Arch 2026-11-15): on a GitHub App grant, the issue and pull-request searches
cover the repositories the App is installed on, and nothing else.

Before this, ``assignee:@me`` and ``author:@me`` ran user-wide on an App grant, so a
person saw issues in public repositories they never gave the App, and the install step
could appear only on an empty search (PA's read of 2026-11-15: 365 issues, no install
step). The repository list has read installations since #2342 (Arch 2026-11-12 08:02);
this puts the two searches on the same source.

Layer: unit. The MCP client and the installation read are fakes; nothing calls GitHub.
"""

from __future__ import annotations

import contextlib
import json
from typing import Any, Dict, List
from unittest.mock import AsyncMock

import pytest

from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    DETAIL_APP_NOT_ON_REPOSITORY,
    DETAIL_APP_TOO_MANY_REPOSITORIES,
    InstallationReadFailed,
    InstalledRepositories,
)

pytestmark = pytest.mark.asyncio

_OWNER = "11111111-1111-1111-1111-111111111111"
_ISSUES_BASE = "assignee:@me is:open is:issue archived:false"
_PRS_BASE = "author:@me is:open is:pr"


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


def _page(total, *created):
    return json.dumps(
        {
            "total_count": total,
            "items": [
                {"number": i, "title": f"t{i}", "created_at": c} for i, c in enumerate(created)
            ],
        }
    )


def _adapter(monkeypatch, installed, *, pages=None, credential=None):
    """An adapter whose MCP client records each search and answers from ``pages`` in
    turn (the last page repeats), and whose installation read answers ``installed``."""
    seen: List[Dict[str, Any]] = []
    answers = list(pages or [_page(1, "2026-11-01T00:00:00Z")])

    class _Client:
        async def call_tool(self, tool, args):
            seen.append({"tool": tool, **args})
            return answers[min(len(seen) - 1, len(answers) - 1)]

    @contextlib.asynccontextmanager
    async def _ctx(_binding):
        yield _Client()

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


_READS = {
    "issues": (lambda a, **k: a.list_open_issues(_OWNER, **k), _ISSUES_BASE, gh_mod._ISSUES_TOOL),
    "pull requests": (lambda a, **k: a.list_open_prs(_OWNER, **k), _PRS_BASE, gh_mod._PRS_TOOL),
}


@pytest.mark.parametrize("read_name", sorted(_READS))
class TestTheSearchCoversTheInstalledSetOnly:
    """Acceptance rows 1 to 3, and row 4 (the same for pull requests)."""

    async def test_installed_on_a_only_searches_a_only(self, monkeypatch, read_name):
        # The person is also assigned in public octo/b; the query can't return it.
        call, base, tool = _READS[read_name]
        adapter, seen, read = _adapter(
            monkeypatch, _installed("octo/a"), pages=[_page(7, "2026-11-01T00:00:00Z")]
        )
        result = await call(adapter)
        assert [s["query"] for s in seen] == [f"{base} repo:octo/a"]
        assert seen[0]["tool"] == tool
        assert result.degradation is None
        assert result.total == 7  # GitHub's own count on the qualified query
        read.assert_awaited_once_with("access-live")

    async def test_every_installed_repository_is_in_the_query(self, monkeypatch, read_name):
        call, base, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a", "Org-2/b.c", "u_1/d"))
        await call(adapter)
        assert [s["query"] for s in seen] == [f"{base} repo:octo/a repo:Org-2/b.c repo:u_1/d"]

    async def test_installed_nowhere_is_the_install_step_with_no_search(
        self, monkeypatch, read_name
    ):
        call, _, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, _installed())
        result = await call(adapter)
        assert seen == []
        assert result.issues is None
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED

    @pytest.mark.parametrize("status", [None, 403, 500, 502])
    async def test_a_failed_installation_read_degrades_with_no_search(
        self, monkeypatch, read_name, status
    ):
        call, _, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(status))
        result = await call(adapter)
        assert seen == []  # never a fall-back to the user-wide search
        assert result.issues is None
        assert result.degradation.reason is DegradationReason.UNREACHABLE

    async def test_a_401_on_the_installation_read_is_the_stale_path(self, monkeypatch, read_name):
        call, _, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(401))
        adapter._rejected_token_was_replaced = AsyncMock(return_value=False)
        adapter._mark_oauth_binding_stale = AsyncMock()
        result = await call(adapter)
        assert seen == []
        assert result.degradation.reason is DegradationReason.STALE_TOKEN
        adapter._mark_oauth_binding_stale.assert_awaited_once()

    async def test_a_401_after_the_token_was_replaced_is_a_wait_not_stale(
        self, monkeypatch, read_name
    ):
        call, _, _ = _READS[read_name]
        adapter, seen, _ = _adapter(monkeypatch, InstallationReadFailed(401))
        adapter._rejected_token_was_replaced = AsyncMock(return_value=True)
        adapter._mark_oauth_binding_stale = AsyncMock()
        result = await call(adapter)
        assert result.degradation.reason is DegradationReason.UNREACHABLE
        adapter._mark_oauth_binding_stale.assert_not_awaited()

    async def test_an_empty_search_of_installed_repositories_is_a_true_empty(
        self, monkeypatch, read_name
    ):
        call, _, _ = _READS[read_name]
        adapter, _, read = _adapter(monkeypatch, _installed("octo/a"), pages=[_page(0)])
        result = await call(adapter)
        assert result.issues == [] and result.total == 0 and result.degradation is None
        read.assert_awaited_once()  # one installation read, not a second on the empty result


@pytest.mark.parametrize("read_name", sorted(_READS))
class TestTheOtherLegsSearchAsBefore:
    """The issue's last mechanism line: the personal-token leg and classic grants are
    unchanged. No installation read, and the query is the user-wide one."""

    @pytest.mark.parametrize(
        "credential",
        [_credential(leg="pat", app_grant=False), _credential(leg="oauth", app_grant=False)],
        ids=["personal token", "classic grant"],
    )
    async def test_no_installation_read_and_the_user_wide_query(
        self, monkeypatch, read_name, credential
    ):
        call, base, _ = _READS[read_name]
        adapter, seen, read = _adapter(
            monkeypatch, AssertionError("no installation read"), credential=credential
        )
        result = await call(adapter)
        assert [s["query"] for s in seen] == [base]
        assert result.degradation is None
        read.assert_not_awaited()


class TestANamedRepository:
    async def test_inside_the_installed_set_the_query_is_unchanged(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a", "octo/b"))
        result = await adapter.list_open_issues(_OWNER, repository="octo/b", label="bug")
        assert [s["query"] for s in seen] == ['repo:octo/b is:issue is:open label:"bug"']
        assert result.degradation is None

    async def test_the_match_ignores_case_as_github_does(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("Octo/Repo"))
        result = await adapter.list_open_issues(_OWNER, repository="octo/repo")
        assert len(seen) == 1 and result.degradation is None

    async def test_outside_the_installed_set_is_said_and_nothing_is_read(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await adapter.list_open_issues(_OWNER, repository="someone/public")
        assert seen == []  # never a public read of it
        assert result.issues is None
        assert result.degradation.reason is DegradationReason.REPO_UNRESOLVED
        assert result.degradation.detail == DETAIL_APP_NOT_ON_REPOSITORY
        assert result.degradation.user_message == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_REPLY
        assert (
            gh_mod.github_degrade_reply(result.degradation)
            == gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_REPLY
        )
        assert (
            gh_mod.github_connector_reply(result.degradation)
            == gh_mod.GITHUB_CONNECTOR_APP_NOT_ON_REPOSITORY_REPLY
        )

    async def test_with_no_install_link_it_is_the_on_our_side_state(self, monkeypatch):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG)
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a"))
        result = await adapter.list_open_issues(_OWNER, repository="someone/public")
        assert seen == []
        assert result.degradation.detail == DETAIL_APP_INSTALL_LINK_MISSING

    async def test_installed_nowhere_wins_over_the_named_repository(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed())
        result = await adapter.list_open_issues(_OWNER, repository="octo/a")
        assert seen == []
        assert result.degradation.detail == DETAIL_APP_NOT_INSTALLED

    async def test_a_personal_token_still_reads_any_named_repository(self, monkeypatch):
        adapter, seen, read = _adapter(
            monkeypatch,
            AssertionError("no installation read"),
            credential=_credential(leg="pat", app_grant=False),
        )
        result = await adapter.list_open_issues(_OWNER, repository="someone/public")
        assert [s["query"] for s in seen] == ["repo:someone/public is:issue is:open"]
        assert result.degradation is None


class TestManyInstalledRepositories:
    """One query's ``repo:`` qualifiers stay under the length GitHub was seen to accept;
    a longer set is split, the counts add up, and the page is still the newest items."""

    @staticmethod
    def _names(n):
        return [f"octo-organization/repository-number-{i:04d}" for i in range(n)]

    async def test_a_long_set_is_split_and_every_repository_is_searched_once(self, monkeypatch):
        names = self._names(100)  # about 4,400 characters of qualifiers: three queries
        adapter, seen, _ = _adapter(
            monkeypatch,
            _installed(*names),
            pages=[
                _page(10, "2026-11-03T00:00:00Z", "2026-10-01T00:00:00Z"),
                _page(5, "2026-11-05T00:00:00Z"),
                _page(2, "2026-11-04T00:00:00Z", "2026-09-01T00:00:00Z"),
            ],
        )
        result = await adapter.list_open_issues(_OWNER, limit=3)
        assert len(seen) == 3
        searched = []
        for call in seen:
            assert call["query"].startswith(_ISSUES_BASE + " repo:")
            qualifiers = call["query"][len(_ISSUES_BASE) + 1 :]
            assert len(qualifiers) <= gh_mod._REPO_QUALIFIER_BUDGET
            searched += [q[len("repo:") :] for q in qualifiers.split(" ")]
        assert searched == names  # each exactly once, none dropped
        assert result.total == 17  # disjoint sets: the counts add up to GitHub's own
        assert [it["created_at"] for it in result.issues] == [
            "2026-11-05T00:00:00Z",
            "2026-11-04T00:00:00Z",
            "2026-11-03T00:00:00Z",
        ]

    async def test_an_unknown_count_on_one_query_is_an_unknown_total(self, monkeypatch):
        adapter, _, _ = _adapter(
            monkeypatch, _installed(*self._names(100)), pages=[_page(4), "not json", _page(1)]
        )
        result = await adapter.list_open_issues(_OWNER)
        assert result.total is None  # never a partial sum shown as the count

    async def test_more_than_the_bound_is_said_and_nothing_is_searched(self, monkeypatch):
        names = self._names(400)  # about 17,600 characters: nine queries, over the bound
        assert len(gh_mod._repo_qualifier_chunks(names)) > gh_mod._INSTALLED_SEARCH_MAX_QUERIES
        adapter, seen, _ = _adapter(monkeypatch, _installed(*names))
        result = await adapter.list_open_issues(_OWNER)
        assert seen == []  # never part of the set as if it were all of it
        assert result.issues is None
        assert result.degradation.detail == DETAIL_APP_TOO_MANY_REPOSITORIES
        for reply in (gh_mod.github_degrade_reply, gh_mod.github_connector_reply):
            assert reply(result.degradation) == gh_mod.GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY

    async def test_a_named_repository_is_read_however_many_are_installed(self, monkeypatch):
        # CXO's condition on the too-many line (2026-11-15 15:33) and Arch's on the
        # mechanism: "Ask me about one repository by name" has to work in that state.
        names = self._names(400)
        adapter, seen, _ = _adapter(monkeypatch, _installed(*names))
        result = await adapter.list_open_issues(_OWNER, repository=names[399])
        assert [s["query"] for s in seen] == [f"repo:{names[399]} is:issue is:open"]
        assert result.degradation is None and result.issues

    async def test_a_named_repository_outside_a_too_many_set_is_still_refused(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed(*self._names(400)))
        result = await adapter.list_open_issues(_OWNER, repository="someone/public")
        assert seen == []
        assert result.degradation.detail == DETAIL_APP_NOT_ON_REPOSITORY


class TestTheWordsAreCXOs:
    """CXO 2026-11-15 15:33, verbatim."""

    async def test_the_three_lines(self):
        assert gh_mod.GITHUB_APP_NOT_ON_REPOSITORY_REPLY == (
            "The Piper GitHub app isn't installed on that repository, so I can't read it. "
            "If it's yours, install it there in Settings, under Integrations."
        )
        assert gh_mod.GITHUB_CONNECTOR_APP_NOT_ON_REPOSITORY_REPLY == (
            "The Piper GitHub app isn't installed on that repository, so I can't read it. "
            "If it's yours, install it there in the Piper Morgan app, in Settings under "
            "Integrations."
        )
        assert gh_mod.GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY == (
            "The Piper GitHub app is installed on more repositories than I can search at "
            "once. Ask me about one repository by name."
        )

    async def test_a_malformed_name_in_the_listing_fails_the_read(self, monkeypatch):
        adapter, seen, _ = _adapter(monkeypatch, _installed("octo/a", "octo/b is:closed"))
        result = await adapter.list_open_issues(_OWNER)
        assert seen == []  # nothing from the listing reaches a query unchecked
        assert result.degradation.reason is DegradationReason.UNREACHABLE


class TestTheHelpers:
    @pytest.mark.parametrize(
        "name,ok",
        [
            ("octo/a", True),
            ("Org-2/b.c_d", True),
            ("octo", False),
            ("/a", False),
            ("octo/", False),
            ("octo/a b", False),
            ("octo/a/b", False),
            ('octo/a"', False),
            ("", False),
        ],
    )
    async def test_a_full_name_is_owner_slash_name_in_githubs_characters(self, name, ok):
        assert gh_mod._is_repo_full_name(name) is ok

    async def test_the_chunks_hold_every_name_once_within_the_budget(self):
        names = [f"o/r{i}" for i in range(1000)]
        chunks = gh_mod._repo_qualifier_chunks(names)
        assert all(len(c) <= gh_mod._REPO_QUALIFIER_BUDGET for c in chunks)
        assert " ".join(chunks).split(" ") == [f"repo:{n}" for n in names]
        assert gh_mod._repo_qualifier_chunks([]) == []

    async def test_newest_first_puts_an_item_without_a_date_last(self):
        items = [{"created_at": "2026-01-01T00:00:00Z"}, {}, {"created_at": "2026-02-01T00:00:00Z"}]
        assert gh_mod._newest_first(items) == [items[2], items[0], items[1]]
