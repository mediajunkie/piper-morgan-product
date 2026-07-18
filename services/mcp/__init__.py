"""
MCP (Model Context Protocol) integration for Piper Morgan

This module provides MCP client functionality for enhanced file search capabilities.
Currently implements a compatibility layer for Python 3.9.6 (MCP SDK requires 3.10+).
"""

# #1436 Tier-3 (Arch-ruled 2026-07-18): the POC MCP family (server/, protocol/,
# resources) is DELETED — superseded by services/mcp/consumer/* (ADR-070).
# client.py is HELD pending the connection_pool->adapters->spatial cascade
# ruling (protected-adjacent; see decisions.log).
from .client import PiperMCPClient
from .exceptions import MCPCircuitBreakerOpenError, MCPConnectionError

__all__ = [
    "PiperMCPClient",
    "MCPConnectionError",
    "MCPCircuitBreakerOpenError",
]
