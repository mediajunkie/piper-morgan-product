"""Fixtures for the MCP connection pool tests.

`mcp_connection_pool` lived in the root conftest.py until the 2025-09-02 file
reorganization dropped it; nine tests in test_connection_pool.py kept asking for it
and sat on the full-suite backlog as fixture rot.
"""

import pytest

from services.infrastructure.mcp.connection_pool import MCPConnectionPool


@pytest.fixture
async def mcp_connection_pool():
    """A fresh MCPConnectionPool singleton, shut down and reset after the test."""
    MCPConnectionPool._reset_instance()
    pool = MCPConnectionPool.get_instance()

    yield pool

    try:
        await pool.shutdown()
    except Exception:
        pass
    finally:
        MCPConnectionPool._reset_instance()
