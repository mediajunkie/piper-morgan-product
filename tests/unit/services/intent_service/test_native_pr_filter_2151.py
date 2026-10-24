"""#2151 (read-claim inventory, red rows list_prs and stale_prs): the native path saw no PRs.

``get_open_issues`` on the native path returns ``list_github_issues_direct`` items (or the
spatial read's), which mark a PR with ``is_pull_request``. The handlers filtered on
``pull_request``, a raw-API field those items never carry, so the native path always
said "You don't have any open pull requests right now." The #1782 pins built items with
``pull_request`` and so never saw it. These pins use the shape the read really returns.

LAYER: unit, the real IntentService with the LLM boundary explosive, the OAuth connector
degraded (so the native path runs) and ``get_open_issues`` mocked. DENOMINATOR: both
native-path PR filters (list_prs, stale_prs) plus the helper.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from services.intent.intent_service import _is_pr_item

_ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def test_the_helper_reads_both_shapes():
    assert _is_pr_item({"is_pull_request": True})
    assert _is_pr_item({"pull_request": {"url": "x"}})
    assert not _is_pr_item({"is_pull_request": False})
    assert not _is_pr_item({})


@pytest.fixture
def live_service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(action):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        context={"user_id": "5a2c9d10-2151-4b00-9e00-000000002151"},
    )


def _direct_items(n, *, old=False):
    """The shape ``list_github_issues_direct`` returns: every 4th item a PR."""
    created = datetime.now(timezone.utc) - timedelta(days=30 if old else 1)
    return [
        {
            "number": i,
            "title": f"item {i}",
            "state": "open",
            "is_pull_request": i % 4 == 0,
            "created_at": created.isoformat().replace("+00:00", "Z"),
            "uri": f"https://github.com/o/r/pull/{i}",
        }
        for i in range(n)
    ]


def _native_path(page):
    from services.mcp.consumer.connector import DegradationReason, DegradationResponse
    from services.mcp.consumer.github_adapter import GitHubIssuesResult

    degraded = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="connect"
        ),
    )
    return (
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_prs",
            AsyncMock(return_value=degraded),
        ),
        patch(f"{_ROUTER}.initialize", AsyncMock()),
        patch(f"{_ROUTER}.is_available", AsyncMock(return_value=True)),
        patch(f"{_ROUTER}.get_open_items_strict", AsyncMock(return_value=page)),
    )


@pytest.mark.asyncio
async def test_list_prs_native_path_counts_the_prs(live_service):
    a, b, c, d = _native_path(_direct_items(40))
    with a, b, c, d:
        result = await live_service._handle_list_prs_query(_intent("list_prs_query"), "wf-2151")
    assert "**10 open PRs**" in result.message
    assert "don't have any open pull requests" not in result.message


@pytest.mark.asyncio
async def test_stale_prs_native_path_finds_the_old_prs(live_service):
    a, b, c, d = _native_path(_direct_items(8, old=True))
    with a, b, c, d:
        result = await live_service._handle_stale_prs(_intent("stale_prs"), "wf-2151b")
    assert "#0" in result.message or "item 0" in result.message
    assert "#4" in result.message or "item 4" in result.message
