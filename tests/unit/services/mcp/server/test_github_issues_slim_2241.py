"""#2241 + #2022 — the MCP github section is slim, budgeted, and says what it searched.

One served ``what_piper_knows_about_me`` call returned 431,097 characters: 50 raw GitHub
REST issue objects (bodies, reactions, ``*_url``s). Arch's ruling (issue comment, 2026-10-31):
- each item is exactly ``ISSUE_ITEM_KEYS`` (number, title, repository, state, labels as
  names, assignees as logins, created_at, updated_at, html_url); no body;
- the serialized github section stays under ``GITHUB_SECTION_BUDGET_CHARS`` (20,000) for a
  50-item page, trimming from the TAIL when it must; ``truncated`` stays derived
  (``total > count``), ``capped_at`` stays the page cap;
- the ``scope`` phrase and the ``note`` sentence are rendered FROM the adapter's own query
  and sort constants, so changing the sort changes the ordering word (and this pin);
  the query excludes archived repos and covers only what the token sees, so the words never
  claim "all your repositories";
- the #2005 fields and the degradation payloads are unchanged.

LAYER (m-43): the resource function called directly with identity and the connector read
stubbed (function layer); ``test_resources_unit2.py`` still drives the same resource over
the real MCP client for isolation and the #2005 fields. DENOMINATOR: the github resource
(and therefore the ``what_piper_knows_about_me`` tool section that composes it).
"""

from __future__ import annotations

import json
import uuid

import pytest

from services.mcp.consumer import github_adapter as gh
from services.mcp.consumer.github_adapter import GitHubIssuesResult, GitHubMCPSpatialAdapter
from services.mcp.server import resources
from services.mcp.server.resources import (
    GITHUB_ISSUES_PAGE_CAP,
    GITHUB_SECTION_BUDGET_CHARS,
    ISSUE_ITEM_KEYS,
    _issues_note,
    render_issues_scope,
    slim_issue,
)

CALLER = uuid.UUID("dddddddd-dddd-dddd-dddd-dddddddddddd")


def _raw(n: int, *, title_len: int = 60, labels: int = 2, body_len: int = 2_000) -> dict:
    """A raw GitHub REST issue object of the shape the search tool returns (24 keys)."""
    return {
        "number": n,
        "title": ("T" * title_len) + f" {n}",
        "state": "open",
        "body": "b" * body_len,
        "repository_url": "https://api.github.com/repos/octo/repo",
        "html_url": f"https://github.com/octo/repo/issues/{n}",
        "url": f"https://api.github.com/repos/octo/repo/issues/{n}",
        "events_url": f"https://api.github.com/repos/octo/repo/issues/{n}/events",
        "comments_url": f"https://api.github.com/repos/octo/repo/issues/{n}/comments",
        "labels_url": "https://api.github.com/repos/octo/repo/labels{/name}",
        "node_id": "I_kwDO" + str(n),
        "id": 10_000 + n,
        "user": {"login": "someone", "id": 1, "avatar_url": "https://x/y.png"},
        "labels": [
            {"id": i, "name": f"label-{i}-" + ("x" * 20), "color": "fff"} for i in range(labels)
        ],
        "assignees": [{"login": "me", "id": 2}, {"login": "you", "id": 3}],
        "reactions": {"+1": 0, "-1": 0, "total_count": 0, "url": "https://x"},
        "created_at": "2026-10-01T00:00:00Z",
        "updated_at": "2026-10-30T00:00:00Z",
        "closed_at": None,
        "comments": 3,
        "locked": False,
        "milestone": {"title": "MVP"},
        "author_association": "OWNER",
        "draft": False,
    }


def _stub(items: list[dict], total: int | None, monkeypatch) -> None:
    async def _bound(self, user_id, *, limit=50, repository=None, **kw):
        return GitHubIssuesResult(issues=items, total=total)

    monkeypatch.setattr(GitHubMCPSpatialAdapter, "list_open_issues", _bound)
    monkeypatch.setattr(resources, "current_user_id", lambda: str(CALLER))


async def _payload() -> dict:
    return json.loads(await resources._read_github_issues())


# ---- the slim item -----------------------------------------------------------------


def test_slim_issue_is_exactly_the_key_set_and_carries_no_body() -> None:
    item = slim_issue(_raw(7))
    assert tuple(item.keys()) == ISSUE_ITEM_KEYS
    assert item == {
        "number": 7,
        "title": ("T" * 60) + " 7",
        "repository": "octo/repo",
        "state": "open",
        "labels": ["label-0-" + "x" * 20, "label-1-" + "x" * 20],
        "assignees": ["me", "you"],
        "created_at": "2026-10-01T00:00:00Z",
        "updated_at": "2026-10-30T00:00:00Z",
        "html_url": "https://github.com/octo/repo/issues/7",
    }
    text = json.dumps(item)
    assert "bbbb" not in text and "reactions" not in text and "node_id" not in text
    assert "events_url" not in text and "avatar" not in text


def test_slim_issue_tolerates_a_sparse_item() -> None:
    item = slim_issue({"number": 1, "title": "A's issue"})
    assert tuple(item.keys()) == ISSUE_ITEM_KEYS
    assert item["repository"] is None and item["labels"] == [] and item["assignees"] == []


def test_repository_falls_back_to_html_url_then_none() -> None:
    assert slim_issue({"html_url": "https://github.com/o/r/issues/3"})["repository"] == "o/r"
    assert slim_issue({"html_url": "https://example.com/x"})["repository"] is None


# ---- the payload: scope, note, #2005 fields ------------------------------------------


@pytest.mark.asyncio
async def test_payload_states_scope_and_note_and_keeps_2005_fields(monkeypatch) -> None:
    _stub([_raw(1), _raw(2)], total=255, monkeypatch=monkeypatch)
    p = await _payload()
    assert p["available"] is True
    assert p["count"] == 2 and p["total"] == 255 and p["truncated"] is True
    assert p["capped_at"] == GITHUB_ISSUES_PAGE_CAP
    assert all(tuple(i.keys()) == ISSUE_ITEM_KEYS for i in p["issues"])
    assert p["scope"] == (
        "open issues assigned to you, in the repositories your GitHub connection can see, "
        "archived repositories excluded"
    )
    assert p["note"] == (
        "255 open issues assigned to you, in the repositories your GitHub connection can "
        "see, archived repositories excluded; showing 2 of them, most recently opened first."
    )
    assert "all your repositories" not in json.dumps(p)


@pytest.mark.asyncio
async def test_missing_total_falls_back_to_page_length_not_truncated(monkeypatch) -> None:
    _stub([_raw(1)], total=None, monkeypatch=monkeypatch)
    p = await _payload()
    assert p["total"] == 1 and p["count"] == 1 and p["truncated"] is False
    assert p["note"] == (
        "1 open issue assigned to you, in the repositories your GitHub connection can see, "
        "archived repositories excluded; showing it, most recently opened first."
    )


def test_showing_it_needs_the_one_issue_on_the_page() -> None:
    """Arch 10-31: total 1 with an empty page (the item was filtered out) must not say
    "showing it"; it says what is there, 0 of them."""
    scope, ordering = render_issues_scope()
    assert _issues_note(total=1, count=1, scope=scope, ordering=ordering).endswith(
        f"; showing it, {ordering}."
    )
    dropped = _issues_note(total=1, count=0, scope=scope, ordering=ordering)
    assert dropped == f"1 {scope.replace('issues', 'issue', 1)}; I couldn't show it."
    assert "issues" not in dropped.split(";")[0]  # singular noun on the fallthrough (Arch)


def test_zero_total_says_no_issues_without_a_showing_clause() -> None:
    """CXO 10-31: a successful empty read is "No open issues assigned to you, <scope>."."""
    scope, ordering = render_issues_scope()
    note = _issues_note(total=0, count=0, scope=scope, ordering=ordering)
    assert note == f"No {scope}."
    assert "showing" not in note and ordering not in note


@pytest.mark.asyncio
async def test_whole_page_says_all_of_them_not_n_of_them(monkeypatch) -> None:
    """CXO 10-31: "showing 3 of them" when total is 3 reads as if something is missing."""
    _stub([_raw(1), _raw(2), _raw(3)], total=3, monkeypatch=monkeypatch)
    p = await _payload()
    assert p["count"] == 3 and p["total"] == 3 and p["truncated"] is False
    assert p["note"].endswith("; showing all of them, most recently opened first.")
    assert " of them" not in p["note"].replace("all of them", "")


# ---- the sentence is rendered from the constants that build the call -----------------


def test_scope_and_ordering_are_rendered_from_the_adapter_constants() -> None:
    scope, ordering = render_issues_scope()
    # The adapter's real constants today: created desc, archived excluded.
    assert gh._SEARCH_SORT == "created" and gh._SEARCH_ORDER == "desc"
    assert "archived:false" in gh._MY_OPEN_ISSUES_QUERY
    assert ordering == "most recently opened first"
    assert "archived repositories excluded" in scope


def test_changing_the_sort_constant_changes_the_ordering_word(monkeypatch) -> None:
    monkeypatch.setattr(gh, "_SEARCH_SORT", "updated")
    _, ordering = render_issues_scope()
    assert ordering == "most recently updated first"
    assert ordering != "most recently opened first"
    monkeypatch.setattr(gh, "_SEARCH_SORT", "comments")
    _, ordering = render_issues_scope()
    assert ordering == "ordered by comments desc"  # an unknown sort is never an old word


def test_dropping_the_archived_qualifier_drops_the_words(monkeypatch) -> None:
    monkeypatch.setattr(gh, "_MY_OPEN_ISSUES_QUERY", "assignee:@me is:open is:issue")
    scope, _ = render_issues_scope()
    assert "archived" not in scope
    assert scope.startswith("open issues assigned to you")


# ---- the budget ----------------------------------------------------------------------


@pytest.mark.asyncio
async def test_a_realistic_50_item_page_fits_the_budget_untrimmed(monkeypatch) -> None:
    _stub([_raw(n) for n in range(50)], total=255, monkeypatch=monkeypatch)
    raw = await _payload()
    text = json.dumps(raw)
    assert len(text) < GITHUB_SECTION_BUDGET_CHARS
    assert raw["count"] == 50 and raw["truncated"] is True


@pytest.mark.asyncio
async def test_a_worst_case_50_item_page_is_trimmed_from_the_tail_under_budget(
    monkeypatch,
) -> None:
    worst = [_raw(n, title_len=250, labels=12) for n in range(50)]
    assert len(json.dumps([slim_issue(i) for i in worst])) > GITHUB_SECTION_BUDGET_CHARS
    _stub(worst, total=60, monkeypatch=monkeypatch)
    p = await _payload()
    assert len(json.dumps(p)) <= GITHUB_SECTION_BUDGET_CHARS
    assert 0 < p["count"] < 50
    assert [i["number"] for i in p["issues"]] == list(range(p["count"]))  # head kept
    assert p["total"] == 60 and p["truncated"] is True  # derived, not set
    assert p["capped_at"] == GITHUB_ISSUES_PAGE_CAP
    assert p["note"].startswith(f"60 open issues") and f"showing {p['count']} of them" in p["note"]


@pytest.mark.asyncio
async def test_the_served_shape_that_measured_431k_now_fits(monkeypatch) -> None:
    # PA's measurement: bodies alone 101,070 chars over 50 items; largest body 6,151.
    heavy = [_raw(n, body_len=6_151 if n % 5 == 0 else 2_021) for n in range(50)]
    assert len(json.dumps(heavy)) > 150_000  # raw page, an order of magnitude over budget
    _stub(heavy, total=255, monkeypatch=monkeypatch)
    p = await _payload()
    assert len(json.dumps(p)) < GITHUB_SECTION_BUDGET_CHARS
    assert p["count"] == 50
    assert "bbbb" not in json.dumps(p)


# ---- degradation payloads unchanged ---------------------------------------------------


@pytest.mark.asyncio
async def test_degradation_payload_is_unchanged(monkeypatch) -> None:
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse

    deg = DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub first."
    )

    async def _unbound(self, user_id, *, limit=50, repository=None, **kw):
        return GitHubIssuesResult(degradation=deg)

    monkeypatch.setattr(GitHubMCPSpatialAdapter, "list_open_issues", _unbound)
    monkeypatch.setattr(resources, "current_user_id", lambda: str(CALLER))
    p = await _payload()
    assert p == {
        "available": False,
        "connector": "github",
        "reason": "connect_required",
        "message": "Connect GitHub first.",
    }
