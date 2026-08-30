#!/usr/bin/env python3
"""
Pre-commit hook to prevent direct adapter imports in favor of router pattern.
Enforces architectural protection established in CORE-QUERY-1 Phase 4-6.

Usage:
    python scripts/check_direct_imports.py <file1> [file2] ...

Returns:
    Exit code 0 if no violations found
    Exit code 1 if violations detected
"""

import re
import sys
from pathlib import Path

# Prohibited import patterns - these should use routers instead
PROHIBITED_PATTERNS = [
    # Calendar direct imports
    (
        r"from\s+services\.mcp\.consumer\.google_calendar_adapter\s+import",
        "Calendar: Use CalendarIntegrationRouter instead of direct google_calendar_adapter import",
    ),
    (
        r"GoogleCalendarMCPAdapter(?!Router)",
        "Calendar: Use CalendarIntegrationRouter instead of GoogleCalendarMCPAdapter",
    ),
    # Notion direct imports
    (
        r"from\s+services\.integrations\.mcp\.notion_adapter\s+import",
        "Notion: Use NotionIntegrationRouter instead of direct notion_adapter import",
    ),
    (
        r"NotionMCPAdapter(?!Router)",
        "Notion: Use NotionIntegrationRouter instead of NotionMCPAdapter",
    ),
    # Slack direct imports
    (
        r"from\s+services\.integrations\.slack\.spatial_adapter\s+import.*SlackSpatialAdapter",
        "Slack: Use SlackIntegrationRouter instead of direct spatial_adapter import",
    ),
    (
        r"from\s+services\.integrations\.slack\.slack_client\s+import.*SlackClient(?!\w)",
        "Slack: Use SlackIntegrationRouter instead of direct slack_client import",
    ),
]

# Files to exclude from checking (internal router implementations)
EXCLUDED_FILES = [
    "services/integrations/calendar/calendar_integration_router.py",
    "services/integrations/notion/notion_integration_router.py",
    "services/integrations/slack/slack_integration_router.py",
    "services/integrations/slack/response_handler.py",  # Internal component
    # Adapter definition files - can self-reference
    "services/mcp/consumer/google_calendar_adapter.py",
    "services/integrations/mcp/notion_adapter.py",
    # Canonical NotionMCPAdapter definition since the #1232 Connector port
    # (5050ed024, 2026-07-04) — the old integrations/mcp path above is now a
    # deprecated import alias to this module. The defining module must be able
    # to self-reference (class statement, docstrings, log strings).
    "services/mcp/consumer/notion_adapter.py",
    # Configuration/documentation files
    "services/infrastructure/config/feature_flags.py",
]


def should_check_file(file_path: str) -> bool:
    """Determine if file should be checked for direct imports"""
    # Skip excluded files
    for excluded in EXCLUDED_FILES:
        if file_path.endswith(excluded):
            return False

    # Skip test files
    if "/tests/" in file_path or file_path.startswith("tests/"):
        return False

    # Skip backup files
    if file_path.endswith(".backup"):
        return False

    return True


def check_file(file_path: str) -> list:
    """Check a single file for prohibited imports"""
    violations = []

    if not should_check_file(file_path):
        return violations

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        for line_num, line in enumerate(content.splitlines(), 1):
            for pattern, description in PROHIBITED_PATTERNS:
                if re.search(pattern, line):
                    violations.append(
                        {
                            "file": file_path,
                            "line": line_num,
                            "content": line.strip(),
                            "description": description,
                        }
                    )

    except Exception as e:
        violations.append(
            {
                "file": file_path,
                "line": 0,
                "content": str(e),
                "description": f"Error reading file: {e}",
            }
        )

    return violations


def main():
    """Main pre-commit hook function"""
    if len(sys.argv) < 2:
        print("Usage: check_direct_imports.py <file1> [file2] ...")
        sys.exit(1)

    all_violations = []
    files_checked = 0

    for file_path in sys.argv[1:]:
        if Path(file_path).suffix == ".py":
            files_checked += 1
            violations = check_file(file_path)
            all_violations.extend(violations)

    if all_violations:
        print("=" * 80)
        print("❌ ARCHITECTURAL VIOLATIONS DETECTED")
        print("=" * 80)
        print()
        print(f"Found {len(all_violations)} violation(s) in {files_checked} file(s):")
        print()

        for violation in all_violations:
            print(f"  {violation['file']}:{violation['line']}")
            print(f"    Code: {violation['content']}")
            print(f"    Fix:  {violation['description']}")
            print()

        print("=" * 80)
        print("Router Pattern Enforcement (CORE-QUERY-1)")
        print("=" * 80)
        print()
        print("Migration Examples:")
        print()
        print("  Calendar:")
        print(
            "    ❌ from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter"
        )
        print(
            "    ✅ from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter"
        )
        print()
        print("  Notion:")
        print("    ❌ from services.integrations.mcp.notion_adapter import NotionMCPAdapter")
        print(
            "    ✅ from services.integrations.notion.notion_integration_router import NotionIntegrationRouter"
        )
        print()
        print("  Slack:")
        print("    ❌ from services.integrations.slack.spatial_adapter import SlackSpatialAdapter")
        print(
            "    ✅ from services.integrations.slack.slack_integration_router import SlackIntegrationRouter"
        )
        print()
        print("See docs/migration/router-migration-guide.md for complete examples.")
        print("=" * 80)
        sys.exit(1)
    else:
        print(f"✅ No direct adapter imports detected ({files_checked} files checked)")
        sys.exit(0)


if __name__ == "__main__":
    main()
