"""#1436 Tier-3 "sleeper" guard: the MCP content-search flag must not serve
simulated results.

MCPResourceManager wraps the simulation-only PiperMCPClient. Before the guard,
flipping ``mcp_search_enabled`` blended FABRICATED search hits into real file
search. Until the path is wired to the real consumer client (or the POC family
is deleted — Arch ruling pending), flag-on honestly degrades to filename-only.
These tests pin that neither search method constructs the simulation stack.
"""

from unittest.mock import AsyncMock, MagicMock, patch

from services.repositories.file_repository import FileRepository


def _repo_with_flag_on():
    config = MagicMock()
    config.get_mcp_search_enabled.return_value = True
    repo = FileRepository.__new__(FileRepository)
    repo.config_service = config
    return repo


async def test_flag_on_degrades_to_filename_search_not_simulation():
    repo = _repo_with_flag_on()
    sentinel = [MagicMock(name="filename-match")]
    # #1452: services.mcp.resources was DELETED (the #1436 POC removal) — the
    # guard's subject no longer exists to patch. The contract survives it:
    # flag-on returns filename matches only.
    with patch.object(FileRepository, "search_files_by_name", new=AsyncMock(return_value=sentinel)):
        out = await repo.search_files_with_content("owner-1", "roadmap", limit=10)
    assert out == sentinel


async def test_all_sessions_variant_same_guard():
    repo = _repo_with_flag_on()
    sentinel = [MagicMock(name="filename-match")]
    with patch.object(
        FileRepository, "search_files_by_name_all_sessions", new=AsyncMock(return_value=sentinel)
    ):
        out = await repo.search_files_with_content_all_sessions(
            "owner-1", "roadmap", limit=10
        )
    assert out == sentinel
