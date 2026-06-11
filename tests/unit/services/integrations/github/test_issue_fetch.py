"""#1187 Option C: direct GitHub issue + comments fetch (issue_fetch).

httpx is mocked — no network. The client makes up to two GETs (issue, then
comments); we feed sequential responses via side_effect.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.issue_fetch import fetch_issue_with_comments


def _resp(status, json_data):
    r = MagicMock()
    r.status_code = status
    r.json.return_value = json_data
    return r


def _client(*responses):
    """httpx.AsyncClient() replacement; client.get returns the given responses in order."""
    client = MagicMock()
    client.get = AsyncMock(side_effect=list(responses))
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=None)
    return MagicMock(return_value=cm), client


_ISSUE = {"number": 1124, "title": "T", "body": "B", "html_url": "u"}
_COMMENTS = [{"body": "c1"}, {"body": "c2"}]


class TestFetchIssueWithComments:
    @pytest.mark.asyncio
    async def test_success_embeds_comments(self):
        factory, _ = _client(_resp(200, _ISSUE), _resp(200, _COMMENTS))
        with patch("httpx.AsyncClient", factory):
            issue = await fetch_issue_with_comments("o", "r", 1124, "tok")
        assert issue["title"] == "T"
        assert issue["comments"] == _COMMENTS

    @pytest.mark.asyncio
    async def test_issue_non_200_returns_none(self):
        factory, _ = _client(_resp(404, {}))
        with patch("httpx.AsyncClient", factory):
            assert await fetch_issue_with_comments("o", "r", 1124, "tok") is None

    @pytest.mark.asyncio
    async def test_max_comments_zero_skips_comments_call(self):
        factory, client = _client(_resp(200, _ISSUE))  # only ONE response provided
        with patch("httpx.AsyncClient", factory):
            issue = await fetch_issue_with_comments("o", "r", 1124, "tok", max_comments=0)
        assert issue["comments"] == []
        assert client.get.await_count == 1  # comments endpoint NOT hit

    @pytest.mark.asyncio
    async def test_comments_non_200_degrades_to_empty(self):
        factory, _ = _client(_resp(200, _ISSUE), _resp(403, {}))
        with patch("httpx.AsyncClient", factory):
            issue = await fetch_issue_with_comments("o", "r", 1124, "tok")
        assert issue["title"] == "T"
        assert issue["comments"] == []

    @pytest.mark.asyncio
    async def test_caps_comments_at_max(self):
        many = [{"body": f"c{i}"} for i in range(20)]
        factory, _ = _client(_resp(200, _ISSUE), _resp(200, many))
        with patch("httpx.AsyncClient", factory):
            issue = await fetch_issue_with_comments("o", "r", 1124, "tok", max_comments=5)
        assert len(issue["comments"]) == 5
