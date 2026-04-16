"""
Ensure no hardcoded user context in handlers.
Prevents single-user assumptions that break multi-user deployment.
"""

import re
from pathlib import Path

import pytest


class TestNoHardcodedContext:
    """Validate removal of hardcoded user context."""

    def test_no_hardcoded_va_references(self):
        """Handlers should not contain hardcoded VA references."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Check for hardcoded strings that break multi-user support
        forbidden_patterns = [
            r'"VA Q4"',
            r"'VA Q4'",
            r'"VA".*onramp',
            r"'VA'.*onramp",
            r'if.*"VA".*in.*str\(',  # Pattern: if "VA" in str(config)
            r'if.*"VA".*in.*config',
        ]

        violations = []
        line_numbers = []

        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if re.search(pattern, line):
                    violations.append(f"Line {i}: {line.strip()}")
                    line_numbers.append(i)

        assert len(violations) == 0, (
            f"Found {len(violations)} hardcoded VA references:\n" + "\n".join(violations)
        )

    def test_no_hardcoded_kind_systems_references(self):
        """Handlers should not contain hardcoded Kind Systems references."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Check for hardcoded organization strings
        forbidden_patterns = [
            r'"Kind Systems"',
            r"'Kind Systems'",
            r'if.*"Kind Systems".*in',
            r'if.*"Kind Systems".*==',
        ]

        violations = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if re.search(pattern, line):
                    violations.append(f"Line {i}: {line.strip()}")

        assert len(violations) == 0, (
            f"Found {len(violations)} hardcoded Kind Systems references:\n" + "\n".join(violations)
        )

    def test_no_hardcoded_project_references(self):
        """Handlers should not contain hardcoded project references."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Check for hardcoded project strings
        forbidden_patterns = [
            r'"Q4 onramp"',
            r"'Q4 onramp'",
            r'"onramp implementation"',
            r"'onramp implementation'",
        ]

        violations = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if re.search(pattern, line):
                    violations.append(f"Line {i}: {line.strip()}")

        assert len(violations) == 0, (
            f"Found {len(violations)} hardcoded project references:\n" + "\n".join(violations)
        )

    def test_user_context_service_imported(self):
        """Handlers should import user context service."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Check for proper import
        import_patterns = [
            r"from services\.user_context_service import user_context_service",
            r"import.*user_context_service",
        ]

        has_import = any(re.search(pattern, content) for pattern in import_patterns)

        assert has_import, "Handlers must import user_context_service for multi-user support"

    def test_handlers_use_context_service(self):
        """Handlers should use user context service instead of hardcoded values."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Look for usage of context service
        usage_patterns = [
            r"user_context_service\.get_user_context",
            r"await.*get_user_context",
        ]

        has_usage = any(re.search(pattern, content) for pattern in usage_patterns)

        # If handlers exist, they should use the context service
        # (This test may pass initially if handlers don't exist yet)
        if "class CanonicalHandlers" in content:
            assert has_usage, "CanonicalHandlers should use user_context_service.get_user_context()"

    def test_no_string_config_matching(self):
        """Handlers should not use string matching on config values."""
        handlers_file = Path("services/intent_service/canonical_handlers.py")

        if not handlers_file.exists():
            pytest.skip("Canonical handlers file not found")

        content = handlers_file.read_text()

        # Check for problematic config string matching patterns
        forbidden_patterns = [
            r"if.*str\(config.*\)",  # if "something" in str(config.values())
            r"str\(config\.values\(\)\)",  # str(config.values())
            r"config.*values.*str",  # config.values() converted to string
        ]

        violations = []
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            for pattern in forbidden_patterns:
                if re.search(pattern, line):
                    violations.append(f"Line {i}: {line.strip()}")

        assert len(violations) == 0, (
            f"Found {len(violations)} problematic config string matching patterns:\n"
            + "\n".join(violations)
            + "\nUse user_context_service instead of string matching on config"
        )


class TestMultiUserSupport:
    """Test multi-user context isolation."""

    def test_user_context_service_exists(self):
        """UserContextService should exist."""
        service_file = Path("services/user_context_service.py")

        # This will be created by Code Agent
        if service_file.exists():
            content = service_file.read_text()
            assert "class UserContextService" in content
            assert "class UserContext" in content
        else:
            pytest.skip("UserContextService not yet implemented")

    def test_user_context_dataclass(self):
        """UserContext should have required fields."""
        service_file = Path("services/user_context_service.py")

        if not service_file.exists():
            pytest.skip("UserContextService not yet implemented")

        content = service_file.read_text()

        # Check for required fields
        required_fields = ["user_id", "organization", "projects", "priorities", "preferences"]

        for field in required_fields:
            assert field in content, f"UserContext should have {field} field"
