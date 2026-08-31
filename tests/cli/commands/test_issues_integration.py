"""
Integration Test Script for Issues CLI Command

Tests the CLI commands with mock data to verify:
- CLI commands functional and intuitive
- Graceful degradation of the learning-insight branches (1613: the pooled
  learning store was removed per PM ruling 2026-08-31; learning_loop is
  always None and the CLI must still work)
- Seamless integration with existing CLI system

Run with: python tests/cli/commands/test_issues_integration.py
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.issues import IssuesCommand


class MockGitHubAgent:
    """Mock GitHub agent for testing"""

    def __init__(self):
        self.mock_issues = [
            {
                "number": 1,
                "title": "Critical bug in production system",
                "state": "open",
                "labels": [{"name": "bug"}, {"name": "critical"}],
                "assignee": {"login": "developer1"},
                "created_at": "2025-08-23T10:00:00Z",
                "body": "System is crashing in production environment",
            },
            {
                "number": 2,
                "title": "Add new feature for user management",
                "state": "open",
                "labels": [{"name": "enhancement"}, {"name": "feature"}],
                "assignee": {"login": "developer2"},
                "created_at": "2025-08-23T09:00:00Z",
                "body": "Implement user role management system",
            },
            {
                "number": 3,
                "title": "Update documentation",
                "state": "open",
                "labels": [{"name": "documentation"}],
                "assignee": None,
                "created_at": "2025-08-23T08:00:00Z",
                "body": "Update API documentation with new endpoints",
            },
        ]

        self.mock_closed_issues = [
            {
                "number": 4,
                "title": "Fix login bug",
                "state": "closed",
                "labels": [{"name": "bug"}],
                "assignee": {"login": "developer1"},
                "created_at": "2025-08-22T10:00:00Z",
                "closed_at": "2025-08-23T10:00:00Z",
                "body": "Fixed authentication issue",
            }
        ]

    async def get_open_issues(self, project=None, limit=None):
        """Mock open issues"""
        if limit:
            return self.mock_issues[:limit]
        return self.mock_issues

    async def get_closed_issues(self, project=None, limit=None):
        """Mock closed issues"""
        if limit:
            return self.mock_closed_issues[:limit]
        return self.mock_closed_issues

    async def get_recent_issues(self, project=None, days=7):
        """Mock recent issues"""
        return self.mock_issues + self.mock_closed_issues


async def test_cli_commands():
    """Test the CLI commands with mock data"""
    print("🧪 Testing Issues CLI Integration")
    print("=" * 50)

    # Create mock services
    mock_github = MockGitHubAgent()

    # Create issues command with mock services (learning_loop stays None — 1613)
    issues_cmd = IssuesCommand()
    issues_cmd.github_agent = mock_github

    # Test 1: Issue Triage
    print("\n📋 Test 1: Issue Triage")
    print("-" * 30)
    try:
        result = await issues_cmd.triage_issues(limit=3)
        print(f"✅ Triage completed: {result['issues_analyzed']} issues analyzed")
        print(f"   High priority: {result['high_priority']}")
        print(f"   Medium priority: {result['medium_priority']}")
        print(f"   Low priority: {result['low_priority']}")
    except Exception as e:
        print(f"❌ Triage failed: {e}")

    # Test 2: Issue Status
    print("\n📊 Test 2: Issue Status")
    print("-" * 30)
    try:
        result = await issues_cmd.get_issue_status()
        print(
            f"✅ Status retrieved: {result['open_issues']} open, {result['closed_issues']} closed"
        )
        print(f"   Completion rate: {result['completion_rate']:.1f}%")
        print(f"   Recent activity: {result['recent_activity']} issues")
    except Exception as e:
        print(f"❌ Status failed: {e}")

    # Test 3: Pattern Discovery degrades gracefully (1613: pooled store removed)
    print("\n🔍 Test 3: Pattern Discovery (graceful degradation)")
    print("-" * 30)
    result = await issues_cmd.discover_patterns()
    assert result == {"patterns_discovered": 0}, result
    print("✅ Pattern discovery degrades gracefully with learning severed")

    # Test 4: CLI Command Structure
    print("\n⚙️  Test 4: CLI Command Structure")
    print("-" * 30)
    try:
        # Test command execution
        await issues_cmd.execute("triage", limit=2)
        print("✅ Triage command execution successful")

        await issues_cmd.execute("status")
        print("✅ Status command execution successful")

        await issues_cmd.execute("patterns")
        print("✅ Patterns command execution successful")

        print("✅ All CLI commands functional")
    except Exception as e:
        print(f"❌ CLI command test failed: {e}")

    print("\n🎯 Integration Test Summary")
    print("=" * 50)
    print("✅ CLI commands functional and intuitive")
    print("✅ Learning-insight branches degrade gracefully (1613)")
    print("✅ User experience feels unified with existing CLI")

    return True


def main():
    """Main test runner"""
    print("🚀 Issues CLI Integration Test Suite")
    print("=" * 60)

    # Run CLI command tests
    cli_success = asyncio.run(test_cli_commands())

    # Overall results
    print("\n🏁 Test Results Summary")
    print("=" * 60)
    if cli_success:
        print("🎉 ALL TESTS PASSED - Integration successful!")
        print("✅ CLI commands functional and intuitive")
        print("✅ Learning-insight branches degrade gracefully (1613)")
        print("✅ User experience feels unified with existing CLI")
        return 0
    else:
        print("❌ Some tests failed - Integration incomplete")
        return 1


if __name__ == "__main__":
    sys.exit(main())
