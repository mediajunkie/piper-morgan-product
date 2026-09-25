"""#1761 — MCP resource listing must not fabricate absence.

``MCPConsumerCore._execute_list_issues`` (the resources-fallback path of
``execute("list_issues", ...)``) used to render a missing ``description``
field as the prose ``"No description available"`` and a missing ``mime_type``
as ``"text/plain"`` — indistinguishable, downstream, from the MCP server
explicitly saying so (fabricated absence, same class #1736 fixed on the
GitHub issue read-back surface; precedent commit 24cd313eb).

Layer named (m-43): these tests exercise ``_execute_list_issues`` directly
with a mocked ``MCPProtocolClient`` — the DATA layer contract only. No live
render currently consumes this shape (``MCPConsumerCore`` is not constructed
on any production path today, per #1699 /
``test_no_eager_sim_stack_1699.py``), so there is no user-facing render to
pin here; per
``docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md``
§3, absent must stay absent (``None``) at the data layer regardless of
whether a renderer exists yet.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.mcp.consumer.consumer_core import MCPConsumerCore


def _mock_client(resources):
    """A client whose tool-call path fails (forcing the resources fallback)
    and whose ``list_resources_protocol`` returns the given raw resources."""
    client = MagicMock()
    client.call_tool_protocol = AsyncMock(side_effect=RuntimeError("tool not available"))
    client.list_resources_protocol = AsyncMock(return_value=resources)
    return client


class TestResourceListingHonestEmpty1761:
    @pytest.mark.asyncio
    async def test_absent_description_is_none_not_fabricated_prose(self):
        """A resource with no 'description' key renders as None — never
        'No description available'."""
        consumer = MCPConsumerCore()
        client = _mock_client([{"name": "widget", "uri": "mcp://widget/1"}])

        issues = await consumer._execute_list_issues(client, repo="owner/repo")

        assert len(issues) == 1
        assert issues[0]["description"] is None
        assert "No description available" not in str(issues[0]["description"])

    @pytest.mark.asyncio
    async def test_present_description_carried_verbatim(self):
        """A resource that DOES carry a description renders it verbatim,
        unchanged by the honest-empty fix."""
        consumer = MCPConsumerCore()
        client = _mock_client(
            [{"name": "widget", "description": "a real description", "uri": "mcp://widget/1"}]
        )

        issues = await consumer._execute_list_issues(client, repo="owner/repo")

        assert issues[0]["description"] == "a real description"

    @pytest.mark.asyncio
    async def test_delivered_empty_description_carried_as_empty_not_none(self):
        """A resource that delivers an explicit empty description is a
        DIFFERENT provenance state (verified_empty) than absent — the data
        layer must not collapse the two."""
        consumer = MCPConsumerCore()
        client = _mock_client([{"name": "widget", "description": "", "uri": "mcp://widget/1"}])

        issues = await consumer._execute_list_issues(client, repo="owner/repo")

        assert issues[0]["description"] == ""
        assert issues[0]["description"] is not None

    @pytest.mark.asyncio
    async def test_absent_mime_type_is_none_not_fabricated_text_plain(self):
        """Same fabricated-absence class as description: a missing
        'mime_type' must not become a fabricated 'text/plain' claim."""
        consumer = MCPConsumerCore()
        client = _mock_client([{"name": "widget", "uri": "mcp://widget/1"}])

        issues = await consumer._execute_list_issues(client, repo="owner/repo")

        assert issues[0]["mime_type"] is None
        assert issues[0]["mime_type"] != "text/plain"

    @pytest.mark.asyncio
    async def test_present_mime_type_carried_verbatim(self):
        consumer = MCPConsumerCore()
        client = _mock_client(
            [{"name": "widget", "mime_type": "application/json", "uri": "mcp://widget/1"}]
        )

        issues = await consumer._execute_list_issues(client, repo="owner/repo")

        assert issues[0]["mime_type"] == "application/json"
