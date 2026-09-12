"""#1736 — get_github_issue_direct must carry the issue body under BOTH keys.

Layer named (m-43): mocks the adapter's REST transport helper ``_call_github_api``
(the sibling-suite idiom — #1709/#1039/#1040), so the field MAPPING is real and
only the HTTP round-trip is not.

The defect this pins: the native PAT shape mapped GitHub's ``body`` into
``description`` and emitted NO ``body`` key, while the review-issue composer read
only ``issue["body"]`` — so a fetched, present description rendered as the
fabricated "Description: No description" (PM live 2026-09-09, v70). The connector
parser (``_parse_issue_detail``) already emits both keys and its docstring claims
to mirror "the native get_github_issue_direct shape" — after #1736 that claim is
finally true.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

RAW_ISSUE = {
    "number": 112,
    "title": "issue body test",
    "body": "checking that stated slots are used",
    "state": "open",
    "html_url": "https://github.com/mediajunkie/test-piper-morgan/issues/112",
    "created_at": "2026-09-09T00:00:00Z",
    "updated_at": "2026-09-09T00:00:00Z",
    "labels": [{"name": "enhancement"}],
    "assignees": [],
    "milestone": None,
    "user": {"login": "mediajunkie"},
}


@pytest.fixture
def adapter():
    return GitHubMCPSpatialAdapter()


class TestGetGithubIssueDirectBodyMapping1736:
    async def test_body_present_lands_under_both_keys(self, adapter):
        adapter._call_github_api = AsyncMock(return_value=dict(RAW_ISSUE))
        issue = await adapter.get_github_issue_direct("112", repo="test-piper-morgan", owner="me")
        assert issue["body"] == "checking that stated slots are used"
        assert issue["description"] == "checking that stated slots are used"

    async def test_null_body_is_delivered_verified_empty_not_absent(self, adapter):
        """GitHub returns body: null for a truly-description-less issue. That is a
        DELIVERED empty (verified_empty), so the key must be present as "" — the
        composer distinguishes delivered-empty from field-absent."""
        raw = dict(RAW_ISSUE, body=None)
        adapter._call_github_api = AsyncMock(return_value=raw)
        issue = await adapter.get_github_issue_direct("112", repo="test-piper-morgan", owner="me")
        assert "body" in issue and issue["body"] == ""
        assert "description" in issue and issue["description"] == ""
