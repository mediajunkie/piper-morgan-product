"""Notion MCP Spatial Adapter — DEPRECATED, transitional re-export (2026-07-04).

This import path is deprecated. The canonical implementation lives at
`services.mcp.consumer.notion_adapter` (the #1232 Connector-contract home,
per Arch's connector-alignment ruling — mirrors the GitBook duplicate-adapter
precedent: `services/mcp/consumer/` is the #1232 home, `services/integrations/
mcp/` is legacy).

Arch ratified (2026-07-04) that this shim fully closes the single-canonical
invariant: there is exactly ONE implementation now, not two — this module is
an import alias to the identical class object (`is`-true), not a second,
independently-editable copy, so there's no drift risk. It's kept only so the
~20 existing callers (production code, the full test suite, and assorted
debug/manual scripts) don't need to change their imports. Repointing those
callers and deleting this file outright is tracked as a bounded post-beta
follow-up: #1361.

New code MUST import from `services.mcp.consumer.notion_adapter` directly —
do not add new callers of this deprecated path.
"""

from services.mcp.consumer.notion_adapter import NotionMCPAdapter

__all__ = ["NotionMCPAdapter"]
