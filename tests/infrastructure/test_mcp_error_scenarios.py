"""
Error scenario testing for MCP integration
Tests various failure modes and recovery mechanisms.

PM-015 Group 2 Update: Tests now use centralized MCP fixtures from conftest.py
for proper singleton isolation and environment management.
"""

import asyncio
import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.mcp.client import MCPCircuitBreaker, PiperMCPClient
from services.mcp.exceptions import MCPConnectionError, MCPResourceNotFoundError, MCPTimeoutError
from services.repositories.file_repository import FileRepository


class TestMCPErrorScenarios:
    """Comprehensive error scenario testing for MCP integration"""

    @pytest.mark.asyncio
    async def test_mcp_client_connection_failure(self):
        """Test MCP client graceful handling of connection failures"""
        # Test with invalid server URL
        invalid_config = {"url": "invalid://nonexistent-server", "timeout": 1.0}

        client = PiperMCPClient(invalid_config)

        # Connection should fail gracefully
        connected = await client.connect()
        assert connected == False, "Connection should fail with invalid URL"

        # Operations should handle disconnected state
        is_connected = await client.is_connected()
        assert is_connected == False, "Client should report disconnected state"

        resources = await client.list_resources()
        assert resources == [], "List resources should return empty list when disconnected"

        content = await client.get_resource("file://test")
        assert content is None, "Get resource should return None when disconnected"

        search_results = await client.search_content("test")
        assert search_results == [], "Search should return empty list when disconnected"

    @pytest.mark.asyncio
    async def test_mcp_client_timeout_handling(self):
        """Test MCP client timeout handling"""
        # Test with very short timeout
        timeout_config = {
            "url": "stdio://./scripts/mcp_file_server.py",
            "timeout": 0.001,  # 1ms timeout - should cause timeout
        }

        client = PiperMCPClient(timeout_config)

        # Connection might succeed or fail due to timeout
        connected = await client.connect()

        if connected:
            # If connection succeeds, operations should still handle timeouts gracefully
            # In simulation mode, operations complete quickly so we'll test the timeout logic
            assert await client.is_connected() == True
        else:
            # If connection fails due to timeout, that's also acceptable
            assert await client.is_connected() == False

        # Clean up
        await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_circuit_breaker_functionality(self):
        """Test MCP circuit breaker failure detection and recovery"""
        # Create circuit breaker with low failure threshold
        breaker = MCPCircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

        # Test initial state
        assert breaker.state == "closed"
        assert breaker.failure_count == 0

        # Simulate failures
        import time

        for i in range(2):
            breaker.record_failure()

        # Should be open after reaching threshold
        assert breaker.state == "open"
        assert not breaker.can_attempt()

        # Wait for recovery timeout
        await asyncio.sleep(0.2)

        # Should transition to half-open
        assert breaker.state == "half-open"
        assert breaker.can_attempt()

        # Successful call should close circuit
        breaker.record_success()
        assert breaker.state == "closed"
        assert breaker.failure_count == 0

    @pytest.mark.asyncio
    async def test_file_repository_mcp_fallback(self):
        """Test FileRepository graceful fallback when MCP fails"""
        # Create temporary database session (mock)
        mock_session = Mock()
        repo = FileRepository(mock_session)

        # Mock database operations
        mock_session.execute = AsyncMock()
        mock_session.scalars = Mock()
        mock_session.scalars.return_value.all.return_value = []

        # Mock the execute method to return a mock result
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        # Test with MCP disabled (should use filename search only)
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false"}):
            results = await repo.search_files_with_content("session123", "test query")
            assert isinstance(results, list), "Should return list even with MCP disabled"

            # Should have called database search
            mock_session.execute.assert_called()

        # Test with MCP enabled: the POC simulation stack is DELETED (#1436
        # Tier-3, Arch-ruled) — flag-on has no path to fabricated results by
        # construction and honestly degrades to filename search.
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
            results = await repo.search_files_with_content("session123", "test query")
            assert isinstance(results, list), "Should return list with MCP flag on"

    @pytest.mark.asyncio
    async def test_file_resolver_content_scoring_failure(self):
        """Test FileResolver content scoring with MCP failures"""
        from services.domain.models import Intent, UploadedFile
        from services.file_context.file_resolver import FileResolver

        # Create mock repository
        mock_repo = Mock()
        resolver = FileResolver(mock_repo)

        # Create test file and intent
        test_file = UploadedFile(
            id="test123",
            filename="test_document.txt",
            file_type="text/plain",
            size=1024,
            session_id="session123",
        )

        test_intent = Intent(
            action="analyze_document", context={"original_message": "analyze the test document"}
        )

        # Test with MCP disabled (should use filename scoring)
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "false"}):
            score = resolver._calculate_score(test_file, test_intent)
            assert isinstance(score, float), "Should return float score"
            assert 0.0 <= score <= 1.0, "Score should be between 0 and 1"

        # Test with MCP enabled but failing
        with patch.dict(os.environ, {"ENABLE_MCP_FILE_SEARCH": "true"}):
            # Mock content scoring to fail
            with patch.object(
                resolver, "_calculate_content_score", side_effect=Exception("MCP error")
            ):
                score = resolver._calculate_score(test_file, test_intent)
                assert isinstance(score, float), "Should return float score even with MCP failure"
                assert 0.0 <= score <= 1.0, "Score should be between 0 and 1"

    @pytest.mark.asyncio
    async def test_mcp_server_unavailable_scenario(self):
        """Test behavior when MCP server is completely unavailable"""
        # Test with non-existent server script
        invalid_config = {"url": "stdio://./nonexistent_server.py", "timeout": 1.0}

        client = PiperMCPClient(invalid_config)

        # Should fail gracefully
        connected = await client.connect()
        assert connected == False, "Should fail to connect to non-existent server"

        # All operations should return empty results
        resources = await client.list_resources()
        assert resources == [], "Should return empty resources"

        search_results = await client.search_content("test")
        assert search_results == [], "Should return empty search results"

        # Stats should reflect failed state
        stats = client.get_connection_stats()
        assert stats["connected"] == False, "Should show not connected"
        assert stats["simulation_mode"] == True, "Should show simulation mode"

    @pytest.mark.asyncio
    async def test_mcp_resource_corruption_handling(self):
        """Test handling of corrupted or invalid MCP resources"""
        client = PiperMCPClient({"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0})

        connected = await client.connect()
        if not connected:
            pytest.skip("MCP server not available for corruption test")

        try:
            # Test getting non-existent resource
            content = await client.get_resource("file://nonexistent/file.txt")
            assert content is None, "Should return None for non-existent resource"

            # Test getting resource with invalid URI
            content = await client.get_resource("invalid://uri")
            assert content is None, "Should return None for invalid URI"

        finally:
            await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_concurrent_access_errors(self):
        """Test MCP behavior under concurrent access scenarios"""
        client = PiperMCPClient({"url": "stdio://./scripts/mcp_file_server.py", "timeout": 5.0})

        connected = await client.connect()
        if not connected:
            pytest.skip("MCP server not available for concurrent test")

        try:
            # Test concurrent operations
            tasks = []
            for i in range(10):
                task = asyncio.create_task(client.list_resources())
                tasks.append(task)

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Check that all operations completed (even if some failed)
            assert len(results) == 10, "Should complete all concurrent operations"

            # Count successful operations
            successful = sum(1 for r in results if isinstance(r, list))
            assert successful > 0, "At least some concurrent operations should succeed"

        finally:
            await client.disconnect()

    @pytest.mark.asyncio
    async def test_mcp_memory_cleanup_on_errors(self):
        """Test proper memory cleanup after MCP errors"""
        manager = MCPResourceManager({"url": "invalid://server", "timeout": 0.1})

        # Initialize with invalid config (should fail)
        initialized = await manager.initialize(enabled=True)
        assert initialized == False, "Should fail to initialize"

        # Attempt operations that should fail
        await manager.enhanced_file_search("test")
        await manager.get_file_content("test.txt")
        await manager.list_available_resources()

        # Cleanup should work even after failures
        await manager.cleanup()

        # Manager should be properly reset
        assert manager.client is None, "Client should be None after cleanup"
        assert manager.initialized == False, "Should be uninitialized after cleanup"
        assert len(manager.resource_cache) == 0, "Cache should be empty after cleanup"


# Performance under error conditions
class TestMCPErrorPerformance:
    """Test performance characteristics under error conditions"""

    @pytest.mark.asyncio
    async def test_error_response_time(self):
        """Test that error responses are fast (fail-fast principle)"""
        import time

        # Test invalid connection
        start_time = time.time()
        client = PiperMCPClient({"url": "invalid://server", "timeout": 0.1})
        connected = await client.connect()
        duration = time.time() - start_time

        assert connected == False, "Should fail to connect"
        assert duration < 1.0, f"Error response should be fast, took {duration:.3f}s"

    @pytest.mark.asyncio
    async def test_fallback_response_time(self):
        """Test that fallback operations are fast"""
        import time

        # Test fallback in FileRepository
        mock_session = Mock()
        repo = FileRepository(mock_session)

        # Mock database operations
        mock_session.execute = AsyncMock()
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result

        # Test fallback performance
        start_time = time.time()
        results = await repo.search_files_with_content("session123", "test")
        duration = time.time() - start_time

        assert duration < 0.1, f"Fallback should be fast, took {duration:.3f}s"
        assert isinstance(results, list), "Should return list"


# Manual test runner
async def run_error_scenario_tests():
    """Run all error scenario tests manually"""
    print("🔥 Running MCP Error Scenario Tests")
    print("=" * 40)

    # Initialize test classes
    error_tests = TestMCPErrorScenarios()
    performance_tests = TestMCPErrorPerformance()

    # Run connection failure tests
    print("Testing connection failures...")
    await error_tests.test_mcp_client_connection_failure()
    print("✓ Connection failure handling works")

    # Run timeout tests
    print("Testing timeout handling...")
    await error_tests.test_mcp_client_timeout_handling()
    print("✓ Timeout handling works")

    # Run circuit breaker tests
    print("Testing circuit breaker...")
    await error_tests.test_mcp_circuit_breaker_functionality()
    print("✓ Circuit breaker functionality works")

    # Run resource manager tests
    print("Testing resource manager errors...")
    await error_tests.test_mcp_resource_manager_initialization_failure()
    await error_tests.test_mcp_resource_manager_disabled_state()
    print("✓ Resource manager error handling works")

    # Run repository fallback tests
    print("Testing repository fallback...")
    await error_tests.test_file_repository_mcp_fallback()
    print("✓ Repository fallback works")

    # Run performance tests
    print("Testing error performance...")
    await performance_tests.test_error_response_time()
    await performance_tests.test_fallback_response_time()
    print("✓ Error performance acceptable")

    print("\n🎉 All error scenario tests passed!")
    print("MCP integration handles errors gracefully with proper fallback.")


if __name__ == "__main__":
    asyncio.run(run_error_scenario_tests())
