"""Notion MCP Spatial Adapter — LEGACY re-export (2026-07-04).

The implementation moved to `services.mcp.consumer.notion_adapter` (the
#1232 Connector-contract canonical location, per Arch's connector-alignment
ruling — mirrors the GitBook duplicate-adapter precedent: `services/mcp/
consumer/` is the #1232 home, `services/integrations/mcp/` is legacy).

This module is kept as a thin re-export so the ~20 existing callers
(production code, the full test suite, and assorted debug/manual scripts)
keep working with zero changes to their own imports — `NotionMCPAdapter`
here IS the same class object as the canonical one, not a copy.

New code should import from `services.mcp.consumer.notion_adapter` directly.
"""

from services.mcp.consumer.notion_adapter import NotionMCPAdapter

__all__ = ["NotionMCPAdapter"]
