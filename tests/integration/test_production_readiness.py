"""
Production readiness tests with real-world scenarios.
Tests PM-specific use cases with actual data.

This test suite validates that the Notion MCP adapter integration
is ready for production deployment with real PM workflows.

2026-08-29 surgery (spatial cold-island disposal, PM-ruled 2026-08-15/16):
the NotionSpatialIntelligence-subject classes (TestPMWorkflowScenarios,
TestSpatialIntelligenceValue, TestCanonicalQueryEnhancement) were excised
with the module they tested (services/intelligence/spatial/notion_spatial.py,
the superseded direct-API predecessor of the live Notion path). The live
NotionMCPAdapter coverage below stays.
"""

import asyncio
import time
from typing import Any, Dict, Optional
from unittest.mock import patch

import pytest

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


class TestRateLimitingCompliance:
    """Ensure production rate limiting works under load"""

    @pytest.mark.skip(
        reason="#1362: tests a bespoke _call_notion_api()/manual-sleep throttle that no "
        "longer exists -- the adapter now delegates HTTP + auth to the official "
        "notion-client SDK (see git history of services/integrations/mcp/notion_adapter.py, "
        "commit ddf5e66f6 era), which owns its own rate-limit handling. Confirmed via grep: "
        "no _call_notion_api, no sleep-based throttle anywhere in the current adapter."
    )
    async def test_notion_rate_limiting_compliance(self):
        """Test Notion 3 req/sec compliance"""
        print("\n⏱️ Testing Notion Rate Limiting Compliance")

        adapter = NotionMCPAdapter()

        try:
            # Configure adapter (without real token for testing)
            await adapter.configure_notion_api("test_token")

            # Test rate limiting by making multiple calls
            start_time = time.time()

            # Make 3 API calls to test rate limiting
            for i in range(3):
                await adapter._call_notion_api("test_endpoint")

            end_time = time.time()
            elapsed_time = end_time - start_time

            # Should take at least 0.68 seconds due to rate limiting (2 * 0.34s)
            assert elapsed_time >= 0.6, f"Rate limiting not working: {elapsed_time:.3f}s elapsed"

            print(f"✅ Rate limiting compliance verified: {elapsed_time:.3f}s for 3 calls")
            return True

        finally:
            await adapter.close()

    @pytest.mark.skip(
        reason="#1362: same stale premise as test_notion_rate_limiting_compliance above "
        "-- _call_notion_api() no longer exists."
    )
    async def test_graceful_throttling(self):
        """Test graceful throttling under load"""
        print("\n🔄 Testing Graceful Throttling Under Load")

        adapter = NotionMCPAdapter()

        try:
            await adapter.configure_notion_api("test_token")

            # Test that rate limiting doesn't break functionality
            start_time = time.time()

            # Make multiple calls rapidly
            for i in range(5):
                result = await adapter._call_notion_api("test_endpoint")
                # Should handle gracefully even with rate limiting
                assert result is None  # Expected for test endpoint

            end_time = time.time()
            total_time = end_time - start_time

            # Should take reasonable time due to rate limiting
            assert total_time >= 1.0, f"Rate limiting too aggressive: {total_time:.3f}s"
            assert total_time < 10.0, f"Rate limiting too slow: {total_time:.3f}s"

            print(f"✅ Graceful throttling verified: {total_time:.3f}s for 5 calls")
            return True

        finally:
            await adapter.close()


class TestAuthenticationFlows:
    """Test authentication for production deployment"""

    async def test_notion_integration_token_flow(self):
        """Test Notion integration token authentication flow.

        Fix (2026-07-04/05): `configure_notion_api` doesn't exist -- the real method is
        `connect_with_token` (renamed 2026-07-04). Also, `test_connection()` makes a
        real Notion API call; this dev machine has real credentials configured, so
        the original "no token → fails" assertion was environment-dependent (it
        passed only on machines/CI with no Notion key set). Mock at the
        `test_connection()` boundary instead, so this test verifies
        `connect_with_token`'s own branching/return-value logic deterministically,
        independent of ambient machine credentials or real network calls.
        """
        print("\n🔐 Testing Notion Integration Token Flow")

        with patch("services.mcp.consumer.notion_adapter.NotionConfig") as MockConfig:
            MockConfig.return_value.get_api_key.return_value = None
            adapter = NotionMCPAdapter()

            try:
                # Test without token (should fail gracefully) -- no key anywhere,
                # so _notion_client is never initialized.
                connection_result = await adapter.test_connection()
                assert not connection_result, "Should fail without token"

                # Test with invalid token (should fail gracefully)
                with patch.object(adapter, "test_connection", return_value=False):
                    connection_result = await adapter.connect_with_token("invalid_token")
                    assert not connection_result, "Should fail with invalid token"

                # Test token configuration succeeding
                with patch.object(adapter, "test_connection", return_value=True):
                    config_result = await adapter.connect_with_token("test_token")
                    assert config_result, "Should configure successfully with valid token format"

                print("✅ Notion authentication flow validated")
                return True

            finally:
                await adapter.close()

    async def test_secure_credential_handling(self):
        """Test secure credential handling.

        Fix (2026-07-04/05): `configure_notion_api` -> `connect_with_token` (renamed 2026-07-04).
        There's no `_notion_token` attribute to check anymore -- connect_with_token
        wraps the raw string in a notion_client Client immediately, so the plaintext
        token is never stored as a bare attribute at all (stricter than the original
        test's own intent: don't leak the credential).
        """
        print("\n🔒 Testing Secure Credential Handling")

        adapter = NotionMCPAdapter()

        try:
            # Test that credentials are not exposed in string representations
            adapter_str = str(adapter)
            adapter_repr = repr(adapter)

            # Should not contain actual token values
            assert "test_token" not in adapter_str, "Token exposed in string representation"
            assert "test_token" not in adapter_repr, "Token exposed in repr representation"

            # Test that the client gets configured, with no raw-token attribute leak
            with patch.object(adapter, "test_connection", return_value=True):
                await adapter.connect_with_token("test_token")
            assert adapter._notion_client is not None, "Client not configured"
            assert not hasattr(
                adapter, "_notion_token"
            ), "Raw token should never be stored as a bare attribute"

            print("✅ Secure credential handling verified")
            return True

        finally:
            await adapter.close()


async def run_production_readiness_tests():
    """Run all production readiness tests"""
    print("🚀 Production Readiness Test Suite")
    print("=" * 60)

    test_classes = [
        TestRateLimitingCompliance,
        TestAuthenticationFlows,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        print("-" * 40)

        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]

        for test_method in test_methods:
            total_tests += 1
            try:
                test_func = getattr(test_instance, test_method)
                if asyncio.iscoroutinefunction(test_func):
                    await test_func()
                else:
                    test_func()
                print(f"  ✅ {test_method}: PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"  ❌ {test_method}: FAILED - {e}")

    print("\n" + "=" * 60)
    print("📊 Production Readiness Test Results")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if passed_tests == total_tests:
        print("\n🎉 All production readiness tests passed!")
        print("🚀 MCP+Spatial integration ready for production deployment!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed.")
        print("🔧 Review implementation before production deployment.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(run_production_readiness_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test suite interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite failed with unexpected error: {e}")
        exit(1)
