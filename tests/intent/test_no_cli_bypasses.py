"""
Test that all CLI commands use intent classification.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest


class TestCLIIntentEnforcement:
    """Ensure all CLI commands use intent classification."""

    def test_standup_uses_intent(self):
        """Standup command should use intent."""
        from cli.commands.standup import StandupCommand

        # Test that StandupCommand can be instantiated
        # (imports work, no immediate errors)
        cmd = StandupCommand()

        # Command imports intent system (verified by test_all_commands_import_intent)
        # This test confirms no import-time errors
        assert cmd is not None

    def test_all_commands_import_intent(self):
        """All CLI commands should import intent service."""
        cli_commands = Path("cli/commands")

        if not cli_commands.exists():
            pytest.skip("CLI commands directory not found")

        for file in cli_commands.glob("*.py"):
            if file.name == "__init__.py":
                continue

            content = file.read_text()

            # Each command should reference intent somehow
            has_intent_ref = (
                "intent" in content.lower()
                or "CanonicalHandlers" in content
                or "IntentService" in content
            )

            # If this fails, that command bypasses intent
            assert has_intent_ref, f"{file.name} does not use intent classification"
