"""Notion URL unfurling for inbound Slack messages (#1081).

Per the audit-cascade finding 2026-05-18: the original #1081 framing
("verify Slack→Notion cross-references render correctly post-#304
activation") asserted infrastructure that didn't exist — Pattern-073
Instance 13 at the issue-body layer. This module builds the actual
unfurling path the issue body had presumed.

Scope:
- Detect Notion URLs in Slack message text (regex match)
- Extract the 32-hex-char page ID from each URL
- Resolve each via NotionIntegrationRouter.get_page
- Return list of `{url, page_id, title, ok, error}` dicts

The unfurled refs are intended to enrich the Slack message context so
downstream consumers (response handler, intent classifier) can surface
Notion document context alongside the Slack message.

Per Pattern-073 discipline: returns bounded observation per URL — the
`ok` field reflects whether resolution succeeded; `error` carries the
failure mode when it didn't. No over-claiming "Notion content available"
when the resolution failed.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# Match Notion URLs in these forms:
#   https://www.notion.so/Page-Title-32hexchars
#   https://notion.so/32hexchars
#   https://workspace.notion.site/Page-Title-32hexchars
#   https://www.notion.so/workspace/Page-Title-32hexchars
#
# The 32-hex page ID is the load-bearing component; it appears at the end
# of the URL path (potentially preceded by a slug like "Page-Title-").
NOTION_URL_RE = re.compile(
    r"https?://(?:[a-zA-Z0-9-]+\.)?notion\.(?:so|site)/[^\s<>\"]*[a-f0-9]{32}[^\s<>\"]*",
    re.IGNORECASE,
)

# Extract the 32-hex page ID from a Notion URL path.
# Page IDs are 32 hex chars (sometimes with dashes in UUID format, but
# the URL form is always undashed 32-hex).
PAGE_ID_RE = re.compile(r"([a-f0-9]{32})", re.IGNORECASE)


def extract_notion_urls(text: Optional[str]) -> List[str]:
    """Find all Notion URLs in a Slack message text.

    Returns list preserving order. Empty list if text is None/empty or
    no matches.
    """
    if not text:
        return []
    return NOTION_URL_RE.findall(text)


def extract_page_id(url: str) -> Optional[str]:
    """Extract the 32-hex page ID from a Notion URL.

    Returns the page ID as lowercase string, or None if not extractable.
    Per Pattern-073 discipline: bounded observation; we don't guess the
    page ID — if the URL doesn't carry a 32-hex segment, return None.
    """
    if not url:
        return None
    match = PAGE_ID_RE.search(url)
    if not match:
        return None
    return match.group(1).lower()


async def unfurl_notion_urls(
    text: Optional[str], notion_router: Any
) -> List[Dict[str, Any]]:
    """Unfurl all Notion URLs in a message into title/preview metadata.

    Returns one dict per URL found. Each dict has:
        url: the matched URL string
        page_id: extracted 32-hex page ID (None if not extractable)
        title: page title from Notion (None if resolution failed)
        ok: bool — True if Notion returned a page successfully
        error: str — failure mode when ok=False

    Per Pattern-073 discipline: the `ok` field is the verifiable signal.
    Downstream consumers should branch on `ok` rather than assuming
    `title` is populated. Fail-graceful at the per-URL level — one URL's
    failure does not affect the others.
    """
    urls = extract_notion_urls(text)
    if not urls:
        return []
    if notion_router is None:
        # No Notion integration available — return refs with ok=False
        # so the consumer sees the URLs were detected but couldn't be
        # resolved.
        return [
            {
                "url": url,
                "page_id": extract_page_id(url),
                "title": None,
                "ok": False,
                "error": "notion_router_unavailable",
            }
            for url in urls
        ]

    refs: List[Dict[str, Any]] = []
    for url in urls:
        page_id = extract_page_id(url)
        if page_id is None:
            refs.append(
                {
                    "url": url,
                    "page_id": None,
                    "title": None,
                    "ok": False,
                    "error": "page_id_not_extractable",
                }
            )
            continue
        try:
            page = await notion_router.get_page(page_id)
        except Exception as e:
            logger.warning(
                "notion_unfurl_get_page_exception", extra={"page_id": page_id, "error": str(e)}
            )
            refs.append(
                {
                    "url": url,
                    "page_id": page_id,
                    "title": None,
                    "ok": False,
                    "error": f"get_page_exception: {e}",
                }
            )
            continue
        if not page:
            refs.append(
                {
                    "url": url,
                    "page_id": page_id,
                    "title": None,
                    "ok": False,
                    "error": "page_not_found",
                }
            )
            continue
        # Extract the title from Notion's page object. Notion's title
        # property lives under properties.{title or Name}.title[0].text.content
        title = _extract_page_title(page)
        refs.append(
            {
                "url": url,
                "page_id": page_id,
                "title": title,
                "ok": True,
                "error": None,
            }
        )
    return refs


def _extract_page_title(page: Dict[str, Any]) -> Optional[str]:
    """Best-effort title extraction from a Notion page object.

    Notion's page schema has the title under different paths depending
    on whether it's a database row (`properties.Name.title`) or a
    standalone page (`properties.title.title`). Returns the first
    plain-text content found, or None.
    """
    if not isinstance(page, dict):
        return None
    properties = page.get("properties", {})
    if not isinstance(properties, dict):
        return None
    # Try a few common property names where Notion stores the title.
    for prop_name in ("title", "Name", "Title"):
        prop = properties.get(prop_name)
        if not isinstance(prop, dict):
            continue
        title_list = prop.get("title")
        if not isinstance(title_list, list) or not title_list:
            continue
        first = title_list[0]
        if not isinstance(first, dict):
            continue
        text = first.get("text")
        if isinstance(text, dict):
            content = text.get("content")
            if content:
                return content
        # Fall back to plain_text if present.
        plain = first.get("plain_text")
        if plain:
            return plain
    return None


def format_notion_refs_for_slack(refs: List[Dict[str, Any]]) -> str:
    """Render unfurled Notion refs as a short Slack message fragment.

    Returns a markdown-formatted block listing successfully-resolved
    refs. Failed-to-resolve refs are surfaced honestly so the user
    knows we tried + couldn't (rather than silently dropping).

    Empty refs list → empty string (caller can skip rendering).
    """
    if not refs:
        return ""
    lines = ["*Notion documents referenced:*"]
    for ref in refs:
        url = ref.get("url", "")
        if ref.get("ok"):
            title = ref.get("title") or "(untitled)"
            lines.append(f"• <{url}|{title}>")
        else:
            # Honest about resolution failure — Pattern-073 discipline:
            # don't pretend the title is available when it isn't.
            error = ref.get("error", "unknown")
            lines.append(f"• <{url}|link> (couldn't resolve: {error})")
    return "\n".join(lines)
