#!/usr/bin/env python3
"""
Standalone Test Runner for Database-Free Testing

This script bypasses the global conftest.py database fixtures and runs tests directly
without requiring PostgreSQL connections. Use this for testing core logic that doesn't
depend on database operations.

Usage:
    python tests/orchestration/run_standalone_tests.py
"""

import asyncio
import os
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import test modules directly
from tests.orchestration.test_excellence_flywheel_unittest import TestExcellenceFlywheelUnittest


def run_standalone_tests():
    """Run database-free tests without pytest infrastructure"""
    print("🧪 Running Database-Free Excellence Flywheel Tests")
    print("=" * 60)

    # Create test suite
    suite = unittest.TestSuite()

    # Create test suite with unittest-compatible tests
    test_class = TestExcellenceFlywheelUnittest

    # Add all test methods from the unittest class
    for method_name in dir(test_class):
        if method_name.startswith("test_"):
            # Create test case for this specific method
            test_case = test_class(method_name)
            suite.addTest(test_case)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {len(result.failures) + len(result.errors)} tests failed")
        return 1


if __name__ == "__main__":
    # Set up asyncio for async tests
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # Run tests
    exit_code = run_standalone_tests()
    sys.exit(exit_code)
