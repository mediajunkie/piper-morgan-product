"""#1587 — WorkItemProvider's honest three-valued read.

The pre-existing ``list_for_user`` conflated a FAILED GitHub read with a
genuinely-empty one (both returned ``[]`` — the m-44 false-clear at the
provider layer), and its assignee filter zeroed out brand-new bindings with
nothing assigned yet. ``gather_for_user`` fixes both: FAILED is its own kind
(never confused with VERIFIED_EMPTY), and ``include_unassigned`` lets a
caller opt out of the "assigned to me" filter.

``list_for_user`` itself is kept as a back-compat shim (asserted here too) so
any caller not yet migrated keeps the exact old list-or-empty contract.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.radar.feed_factory import (
    WorkItemOutcome,
    WorkItemProvider,
    WorkItemReadKind,
)

SVC = "services.integrations.integration_status_service.IntegrationStatusService"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
HANDLE_READER = "services.integrations.github.repo_resolver.read_user_github_handle"


def _mock_router(*, issues=None, boom=False):
    router = MagicMock()
    router.initialize = AsyncMock()
    if boom:
        router.get_open_issues = AsyncMock(side_effect=RuntimeError("github down"))
    else:
        router.get_open_issues = AsyncMock(return_value=issues or [])
    router.close = AsyncMock()
    return router


def _issue(num, assignees=None):
    return {"number": num, "title": f"#{num}", "state": "open", "assignees": assignees or []}


@pytest.mark.asyncio
async def test_unconfigured_connector_is_verified_empty_not_failed():
    """No GitHub connector configured -> genuinely nothing to read, honestly
    VERIFIED_EMPTY, not SOURCE_FAILED (we never attempted a read that failed)."""
    with patch(f"{SVC}.is_configured", new=AsyncMock(return_value=False)):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome == WorkItemOutcome(kind=WorkItemReadKind.VERIFIED_EMPTY)
    assert not outcome.failed


@pytest.mark.asyncio
async def test_configured_but_no_issues_is_verified_empty():
    router = _mock_router(issues=[])
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value=None)),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind == WorkItemReadKind.VERIFIED_EMPTY
    assert outcome.items == ()
    assert not outcome.failed


@pytest.mark.asyncio
async def test_configured_with_issues_is_items():
    router = _mock_router(issues=[_issue(1), _issue(2)])
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value=None)),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind == WorkItemReadKind.ITEMS
    assert [i["number"] for i in outcome.items] == [1, 2]
    assert not outcome.failed


@pytest.mark.asyncio
async def test_read_failure_is_source_failed_not_empty():
    """The #1587 regression case: a genuine GitHub read failure must surface
    as SOURCE_FAILED, never collapse to an empty-looking result."""
    router = _mock_router(boom=True)
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value=None)),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind == WorkItemReadKind.SOURCE_FAILED
    assert outcome.items == ()
    assert outcome.failed


@pytest.mark.asyncio
async def test_configured_status_check_itself_failing_is_source_failed():
    """The status-service probe raising (not just returning False) must also
    read as a failed attempt, not a verified emptiness."""
    with patch(f"{SVC}.is_configured", new=AsyncMock(side_effect=RuntimeError("db down"))):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind == WorkItemReadKind.SOURCE_FAILED


# --- include_unassigned switch (#1587: new bindings must not be filtered to nothing) ---


@pytest.mark.asyncio
async def test_default_filters_to_assignee_handle():
    """Default behavior (include_unassigned=False) preserves the pre-#1587
    "assigned to me" scoping (#6) — a handle with nothing assigned reads empty."""
    router = _mock_router(issues=[_issue(1, ["someone-else"])])
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value="me")),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1")
    assert outcome.kind == WorkItemReadKind.VERIFIED_EMPTY
    assert outcome.items == ()


@pytest.mark.asyncio
async def test_include_unassigned_bypasses_the_filter():
    """A brand-new binding with nothing assigned yet must be able to see the
    repo's open issues rather than read as "you have no work items"."""
    router = _mock_router(issues=[_issue(1, ["someone-else"]), _issue(2, [])])
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value="me")),
    ):
        outcome = await WorkItemProvider().gather_for_user("u1", include_unassigned=True)
    assert outcome.kind == WorkItemReadKind.ITEMS
    assert [i["number"] for i in outcome.items] == [1, 2]


# --- list_for_user back-compat shim ---


@pytest.mark.asyncio
async def test_list_for_user_still_flattens_failed_to_empty_list():
    """Back-compat: callers still on the old contract keep the old (dishonest
    for their purposes, but previously-tested) FAILED==EMPTY conflation."""
    router = _mock_router(boom=True)
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value=None)),
    ):
        result = await WorkItemProvider().list_for_user("u1")
    assert result == []


@pytest.mark.asyncio
async def test_list_for_user_still_returns_items():
    router = _mock_router(issues=[_issue(1)])
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(ROUTER, return_value=router),
        patch(HANDLE_READER, new=AsyncMock(return_value=None)),
    ):
        result = await WorkItemProvider().list_for_user("u1")
    assert result == [_issue(1)]
