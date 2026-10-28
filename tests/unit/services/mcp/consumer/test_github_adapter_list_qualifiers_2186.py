"""#2186 — the search rail takes the router's list qualifiers and sorts newest first.

``list_open_issues`` builds ``milestone:"X"`` / ``label:"Y"`` / ``is:closed`` terms in
code from already-checked values (ADR-080: the model never writes the query), and
``_search_via_connector`` sends ``sort: created`` / ``order: desc`` the way the module's
two other search calls do, so a page (and a count slice of it) is the newest items.
``list_open_prs`` rides the same rail, so it sorts too; its signature is unchanged.
"""

from __future__ import annotations

import contextlib
import json
from typing import Any, Dict, List

import pytest

from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter, _qualified_search_query

pytestmark = pytest.mark.asyncio

_PAYLOAD = json.dumps({"total_count": 1, "items": [{"number": 1, "title": "x", "labels": []}]})


class _RecordingClient:
    def __init__(self, seen: List[Dict[str, Any]]):
        self._seen = seen

    async def call_tool(self, tool: str, args: Dict[str, Any]):
        self._seen.append({"tool": tool, **args})
        return _PAYLOAD


def _adapter(seen):
    adapter = GitHubMCPSpatialAdapter()

    async def _bound(_user_id):
        return object()

    @contextlib.asynccontextmanager
    async def _ctx(_binding):
        yield _RecordingClient(seen)

    adapter.resolve_credential = _bound
    adapter._mcp_client_ctx = _ctx
    adapter._tool_text = staticmethod(lambda result: result)
    return adapter


@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, "assignee:@me is:open is:issue archived:false"),
        ({"milestone": "MVP"}, 'assignee:@me is:open is:issue archived:false milestone:"MVP"'),
        (
            {"label": "needs-triage"},
            'assignee:@me is:open is:issue archived:false label:"needs-triage"',
        ),
        ({"state": "closed"}, "assignee:@me is:closed is:issue archived:false"),
        ({"state": "open"}, "assignee:@me is:open is:issue archived:false"),
        (
            {"state": "all"},
            "assignee:@me is:open is:issue archived:false",
        ),  # anything else reads open
        (
            {"repository": "o/r", "milestone": "Sprint 4", "label": "bug", "state": "closed"},
            'repo:o/r is:issue is:closed milestone:"Sprint 4" label:"bug"',
        ),
        ({"milestone": 'M"V"P'}, 'assignee:@me is:open is:issue archived:false milestone:"MVP"'),
        ({"milestone": '""', "label": "  "}, "assignee:@me is:open is:issue archived:false"),
    ],
)
async def test_query_built_in_code(kwargs, expected):
    seen: List[Dict[str, Any]] = []
    res = await _adapter(seen).list_open_issues("u", **kwargs)
    assert res.issues is not None
    assert seen[0]["query"] == expected
    assert seen[0]["tool"] == gh_mod._ISSUES_TOOL


async def test_search_sends_sort_created_desc():
    seen: List[Dict[str, Any]] = []
    await _adapter(seen).list_open_issues("u", limit=50, milestone="MVP")
    assert seen[0]["sort"] == "created"
    assert seen[0]["order"] == "desc"
    assert seen[0]["perPage"] == 50


async def test_list_open_prs_sorts_too():
    seen: List[Dict[str, Any]] = []
    await _adapter(seen).list_open_prs("u", limit=20)
    assert seen[0] == {
        "tool": gh_mod._PRS_TOOL,
        "query": gh_mod._MY_OPEN_PRS_QUERY,
        "perPage": 20,
        "sort": "created",
        "order": "desc",
    }


async def test_helper_leaves_the_base_alone_without_qualifiers():
    assert _qualified_search_query(gh_mod._MY_OPEN_ISSUES_QUERY) == gh_mod._MY_OPEN_ISSUES_QUERY
