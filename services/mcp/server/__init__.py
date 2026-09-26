"""MCP server surface (Phase C, #1462) — Piper as an MCP *server*.

Sibling to ``services/mcp/consumer/`` (Piper as an MCP client) and
``services/mcp/protocol/``. Do not import from those two here or vice versa
beyond what each already re-exports; this package is a separate build unit
(the Lead's phase-c-build-plan-2026-09-25.md "unit 0").
"""
