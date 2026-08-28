"""Tests for Slack→Notion URL unfurling (#1081).

Per the audit-cascade finding 2026-05-18: the original #1081 framing
asserted a "Slack→Notion cross-reference rendering" path that didn't
exist (Pattern-073 Instance 13 at the issue-body layer). This module
+ wiring builds the actual path the issue body had presumed.

Covers:
- URL extraction (regex pattern + page-ID parsing)
- `unfurl_notion_urls` happy path + per-URL fail-graceful paths
- `format_notion_refs_for_slack` rendering (honest about resolution failures)
- Spatial adapter preserves `notion_refs` through the response-context round-trip
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.integrations.slack.notion_url_unfurler import (
    extract_notion_urls,
    extract_page_id,
    format_notion_refs_for_slack,
    unfurl_notion_urls,
)

# ===== URL extraction =====


def test_extract_notion_urls_finds_canonical_url() -> None:
    text = "Check out https://www.notion.so/Design-Doc-abc123def456abc123def456abc12345 for details"
    urls = extract_notion_urls(text)
    assert len(urls) == 1
    assert "abc123def456abc123def456abc12345" in urls[0]


def test_extract_notion_urls_finds_multiple() -> None:
    text = (
        "Two docs: "
        "https://www.notion.so/First-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
        "and https://notion.so/Second-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    )
    urls = extract_notion_urls(text)
    assert len(urls) == 2


def test_extract_notion_urls_handles_notion_site_subdomain() -> None:
    text = "https://piper.notion.site/Workspace-Doc-cccccccccccccccccccccccccccccccc"
    urls = extract_notion_urls(text)
    assert len(urls) == 1


def test_extract_notion_urls_empty_for_non_notion_text() -> None:
    assert extract_notion_urls("Just talking about GitHub") == []
    assert extract_notion_urls("https://example.com/notion-fake") == []


def test_extract_notion_urls_handles_none() -> None:
    assert extract_notion_urls(None) == []
    assert extract_notion_urls("") == []


def test_extract_page_id_extracts_32_hex() -> None:
    url = "https://www.notion.so/My-Page-abc123def456abc123def456abc12345"
    assert extract_page_id(url) == "abc123def456abc123def456abc12345"


def test_extract_page_id_lowercases() -> None:
    url = "https://www.notion.so/My-Page-ABC123DEF456ABC123DEF456ABC12345"
    assert extract_page_id(url) == "abc123def456abc123def456abc12345"


def test_extract_page_id_returns_none_when_no_hex() -> None:
    assert extract_page_id("https://example.com/some-path") is None
    assert extract_page_id("") is None
    assert extract_page_id(None) is None


# ===== unfurl_notion_urls =====


@pytest.mark.asyncio
async def test_unfurl_returns_empty_for_no_urls() -> None:
    refs = await unfurl_notion_urls("Just plain text", MagicMock())
    assert refs == []


@pytest.mark.asyncio
async def test_unfurl_returns_empty_when_router_is_none() -> None:
    """No router → marks refs as ok=False so consumer sees URLs were detected
    but couldn't be resolved (Pattern-073 discipline: honest fallback)."""
    text = "https://www.notion.so/Doc-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    refs = await unfurl_notion_urls(text, None)
    assert len(refs) == 1
    assert refs[0]["ok"] is False
    assert refs[0]["error"] == "notion_router_unavailable"


@pytest.mark.asyncio
async def test_unfurl_happy_path_returns_title() -> None:
    notion_router = MagicMock()
    notion_router.get_page = AsyncMock(
        return_value={"properties": {"title": {"title": [{"text": {"content": "Design Doc"}}]}}}
    )
    text = "https://www.notion.so/Design-Doc-abc123def456abc123def456abc12345"
    refs = await unfurl_notion_urls(text, notion_router)
    assert len(refs) == 1
    assert refs[0]["ok"] is True
    assert refs[0]["title"] == "Design Doc"
    assert refs[0]["page_id"] == "abc123def456abc123def456abc12345"


@pytest.mark.asyncio
async def test_unfurl_uses_name_property_for_database_rows() -> None:
    """Database rows store title under properties.Name instead of properties.title."""
    notion_router = MagicMock()
    notion_router.get_page = AsyncMock(
        return_value={"properties": {"Name": {"title": [{"text": {"content": "DB Row"}}]}}}
    )
    text = "https://www.notion.so/DB-Row-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    refs = await unfurl_notion_urls(text, notion_router)
    assert refs[0]["title"] == "DB Row"


@pytest.mark.asyncio
async def test_unfurl_per_url_failure_does_not_break_others() -> None:
    """One URL's fetch failure doesn't affect resolution of other URLs in the message."""
    notion_router = MagicMock()

    async def _get(page_id):
        if page_id.startswith("aaa"):
            raise Exception("notion api error")
        return {"properties": {"title": {"title": [{"text": {"content": "Good Doc"}}]}}}

    notion_router.get_page = AsyncMock(side_effect=_get)
    text = (
        "https://www.notion.so/Bad-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
        "https://www.notion.so/Good-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
    )
    refs = await unfurl_notion_urls(text, notion_router)
    assert len(refs) == 2
    bad = next(r for r in refs if r["page_id"].startswith("aaa"))
    good = next(r for r in refs if r["page_id"].startswith("bbb"))
    assert bad["ok"] is False
    assert "get_page_exception" in bad["error"]
    assert good["ok"] is True
    assert good["title"] == "Good Doc"


@pytest.mark.asyncio
async def test_unfurl_page_not_found_marks_ok_false() -> None:
    """If Notion returns None/empty for a page, mark the ref as not-resolved."""
    notion_router = MagicMock()
    notion_router.get_page = AsyncMock(return_value=None)
    text = "https://www.notion.so/Missing-cccccccccccccccccccccccccccccccc"
    refs = await unfurl_notion_urls(text, notion_router)
    assert refs[0]["ok"] is False
    assert refs[0]["error"] == "page_not_found"


# ===== format_notion_refs_for_slack =====


def test_format_empty_refs_returns_empty_string() -> None:
    assert format_notion_refs_for_slack([]) == ""


def test_format_renders_successful_refs() -> None:
    refs = [
        {"url": "https://notion.so/A", "title": "Doc A", "ok": True, "error": None},
        {"url": "https://notion.so/B", "title": "Doc B", "ok": True, "error": None},
    ]
    out = format_notion_refs_for_slack(refs)
    assert "Notion documents referenced" in out
    assert "Doc A" in out
    assert "Doc B" in out


def test_format_surfaces_failure_honestly() -> None:
    """Pattern-073 discipline: failed-to-resolve refs surface honestly rather
    than being silently dropped."""
    refs = [
        {
            "url": "https://notion.so/Broken",
            "title": None,
            "ok": False,
            "error": "page_not_found",
        }
    ]
    out = format_notion_refs_for_slack(refs)
    assert "couldn't resolve" in out
    assert "page_not_found" in out


# ===== Spatial adapter round-trip =====


@pytest.mark.asyncio
async def test_spatial_adapter_preserves_notion_refs_through_response_context() -> None:
    """The spatial adapter's `get_response_context` must include `notion_refs`
    so the response handler can render them."""
    from services.integrations.slack.spatial_adapter import SlackSpatialAdapter

    adapter = SlackSpatialAdapter.__new__(SlackSpatialAdapter)
    adapter._context_storage = {
        "1234.5678": {
            "room_id": "C123",
            "user_id": "U456",
            "territory_id": "T789",
            "content": "msg with https://notion.so/X-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "notion_refs": [
                {
                    "url": "https://notion.so/X-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "title": "Doc X",
                    "ok": True,
                    "error": None,
                }
            ],
        }
    }
    import asyncio

    adapter._lock = asyncio.Lock()

    response_context = await adapter.get_response_context("1234.5678")
    assert response_context is not None
    assert "notion_refs" in response_context
    assert len(response_context["notion_refs"]) == 1
    assert response_context["notion_refs"][0]["title"] == "Doc X"


@pytest.mark.asyncio
async def test_spatial_adapter_defaults_notion_refs_to_empty_list() -> None:
    """Missing notion_refs in stored context defaults to [] (backward-compatible)."""
    from services.integrations.slack.spatial_adapter import SlackSpatialAdapter

    adapter = SlackSpatialAdapter.__new__(SlackSpatialAdapter)
    adapter._context_storage = {
        "1234.5678": {
            "room_id": "C123",
            "user_id": "U456",
            "territory_id": "T789",
            "content": "plain message",
            # no notion_refs key
        }
    }
    import asyncio

    adapter._lock = asyncio.Lock()

    response_context = await adapter.get_response_context("1234.5678")
    assert response_context["notion_refs"] == []
