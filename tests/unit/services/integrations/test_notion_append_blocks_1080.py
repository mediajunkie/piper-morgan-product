"""Tests for #1080 NOTION-WRITE — append_blocks implementation.

Covers the full chain:
- `services/integrations/mcp/notion_adapter.py:NotionMCPAdapter.append_blocks`
- `services/integrations/notion/notion_integration_router.py:NotionIntegrationRouter.append_blocks`
- `services/intent/intent_service.py:_handle_update_document_notion` (handler now
  appends a paragraph block + reports honestly; Pattern-073 Instance 12 closure)

Previously: handler called `update_page(page_id, properties={})` — a no-op — and
asserted "✓ Updated X / Added: <content>". The success message lied about the
behavior. This was Pattern-073 at the user-facing handler layer.

Now: handler builds a paragraph block from `update_content`, calls
`append_blocks(page_id, [block])`, and reports honestly either:
- "✓ Appended to X / Added paragraph: ..." on success
- "I found X but couldn't append the content. The Notion API call returned no
  result..." on append failure
"""

import inspect
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ===== Adapter layer =====


@pytest.mark.asyncio
async def test_adapter_append_blocks_calls_notion_client_correctly():
    """NotionMCPAdapter.append_blocks wraps blocks.children.append with token counting."""
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    adapter = NotionMCPAdapter.__new__(NotionMCPAdapter)
    adapter._notion_client = MagicMock()
    adapter._notion_client.blocks = MagicMock()
    adapter._notion_client.blocks.children = MagicMock()
    adapter._notion_client.blocks.children.append = MagicMock(
        return_value={"results": [{"id": "block-1"}]}
    )

    # Mock token counter to just await the coroutine
    adapter.token_counter = MagicMock()

    async def _passthrough(name, coro, input_data=None):
        return await coro

    adapter.token_counter.wrap_mcp_call = _passthrough

    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "hi"}}]},
        }
    ]
    result = await adapter.append_blocks(page_id="page-123", blocks=blocks)

    assert result == {"results": [{"id": "block-1"}]}
    adapter._notion_client.blocks.children.append.assert_called_once_with(
        block_id="page-123", children=blocks
    )


@pytest.mark.asyncio
async def test_adapter_append_blocks_empty_page_id_returns_none():
    """Empty page_id is a no-op; returns None without API call."""
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    adapter = NotionMCPAdapter.__new__(NotionMCPAdapter)
    adapter._notion_client = MagicMock()

    result = await adapter.append_blocks(page_id="", blocks=[{"type": "paragraph"}])
    assert result is None


@pytest.mark.asyncio
async def test_adapter_append_blocks_empty_blocks_returns_none():
    """Empty blocks list is a no-op; returns None without API call."""
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    adapter = NotionMCPAdapter.__new__(NotionMCPAdapter)
    adapter._notion_client = MagicMock()

    result = await adapter.append_blocks(page_id="page-1", blocks=[])
    assert result is None


@pytest.mark.asyncio
async def test_adapter_append_blocks_exception_returns_none():
    """Exception from notion_client is caught + returns None (fail-graceful)."""
    from services.integrations.mcp.notion_adapter import NotionMCPAdapter

    adapter = NotionMCPAdapter.__new__(NotionMCPAdapter)
    adapter._notion_client = MagicMock()
    adapter._notion_client.blocks = MagicMock()
    adapter._notion_client.blocks.children = MagicMock()
    adapter._notion_client.blocks.children.append = MagicMock(
        side_effect=Exception("notion api error")
    )
    adapter.token_counter = MagicMock()

    async def _passthrough(name, coro, input_data=None):
        return await coro

    adapter.token_counter.wrap_mcp_call = _passthrough

    result = await adapter.append_blocks(page_id="p1", blocks=[{"type": "paragraph"}])
    assert result is None


# ===== Router layer =====


@pytest.mark.asyncio
async def test_router_append_blocks_passes_through_to_integration():
    """NotionIntegrationRouter.append_blocks delegates to the underlying integration."""
    from services.integrations.notion.notion_integration_router import (
        NotionIntegrationRouter,
    )

    router = NotionIntegrationRouter.__new__(NotionIntegrationRouter)
    mock_integration = MagicMock()
    mock_integration.append_blocks = AsyncMock(return_value={"results": []})
    router._get_preferred_integration = MagicMock(return_value=(mock_integration, False))
    router._warn_deprecation_if_needed = MagicMock()

    blocks = [{"type": "paragraph"}]
    result = await router.append_blocks(page_id="p1", blocks=blocks)
    assert result == {"results": []}
    mock_integration.append_blocks.assert_called_once_with("p1", blocks)


@pytest.mark.asyncio
async def test_router_append_blocks_raises_when_no_integration():
    """Router raises RuntimeError when no Notion integration is available."""
    from services.integrations.notion.notion_integration_router import (
        NotionIntegrationRouter,
    )

    router = NotionIntegrationRouter.__new__(NotionIntegrationRouter)
    router._get_preferred_integration = MagicMock(return_value=(None, False))

    with pytest.raises(RuntimeError, match="No Notion integration available"):
        await router.append_blocks(page_id="p1", blocks=[])


# ===== Handler layer =====


def test_handler_no_longer_calls_update_page_with_empty_properties():
    """Pattern-073 fix: the handler source no longer calls update_page with
    empty properties + lying message."""
    src = Path("services/intent/intent_service.py").read_text()
    start = src.find("async def _handle_update_document_notion")
    # Find the end of this function (next async def at same indent)
    end = src.find("\n    async def ", start + 1)
    if end == -1:
        end = len(src)
    block = src[start:end]

    # The previous bug: passing empty `properties={}` to update_page
    # with no actual property name/value pairs. After fix, the handler
    # uses append_blocks instead.
    assert "notion_router.append_blocks" in block, (
        "Handler must call append_blocks (the real mechanism for "
        "'update doc with content' semantics)"
    )

    # The success message must NOT claim "Updated" without grounding —
    # the new copy says "Appended to X" which is honest about what
    # actually happened.
    assert "Appended to" in block, (
        "Success message must reflect the actual append semantics " "(Pattern-073 discipline)"
    )


def test_handler_documents_pattern_073_instance_12():
    """The handler change includes a comment citing #1080 + Pattern-073
    Instance 12 so future readers see the discipline."""
    src = Path("services/intent/intent_service.py").read_text()
    start = src.find("async def _handle_update_document_notion")
    end = src.find("\n    async def ", start + 1)
    block = src[start:end]
    assert "#1080" in block, "Handler change must cite #1080"
    assert "Pattern-073" in block, "Handler change must cite Pattern-073"
    assert "Instance 12" in block, "Comment should call out this is Instance 12 (handler-layer)"


def test_handler_has_honest_failure_fallback():
    """When append_blocks returns None, the handler reports honestly rather
    than claiming success."""
    src = Path("services/intent/intent_service.py").read_text()
    start = src.find("async def _handle_update_document_notion")
    end = src.find("\n    async def ", start + 1)
    block = src[start:end]
    assert (
        "append_result is None" in block
    ), "Handler must check the append result + branch on failure"
    assert "couldn't append" in block, (
        "Honest failure message must surface the actual failure mode "
        "(string may span lines in the source)"
    )


def test_handler_builds_paragraph_block_with_correct_shape():
    """The paragraph block follows Notion's schema (object/type/paragraph/rich_text)."""
    src = Path("services/intent/intent_service.py").read_text()
    start = src.find("async def _handle_update_document_notion")
    end = src.find("\n    async def ", start + 1)
    block = src[start:end]
    # The block dict must include the canonical Notion shape
    assert '"object": "block"' in block
    assert '"type": "paragraph"' in block
    assert '"rich_text"' in block
