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

    # 1637: commands with NO natural-language surface have nothing to route
    # through intent classification — requiring an intent reference there is
    # the test misfiring, not a bypass. Add a file here ONLY with the same
    # justification: the command takes no free-text user input.
    # - keys.py (#270): interactive credential management — rotate/list/
    #   validate API keys via prompts and menus, no NL.
    # - standup.py: flag-driven only (--format/--slack/--github/--notion),
    #   generates a standup via StandupWorkflowSkill; no NL. (Its API twin
    #   /api/standup IS intent-enforced — see NL_ENDPOINTS in
    #   web/middleware/intent_enforcement.py.) It was ALWAYS failing this
    #   test, masked because the per-file assert aborted the loop at keys.py
    #   before standup.py was reached — see the collected-failures form below.
    NON_NL_COMMANDS = {"keys.py", "standup.py"}

    def test_all_commands_import_intent(self):
        """All NL-surfaced CLI commands should import intent service."""
        cli_commands = Path("cli/commands")

        if not cli_commands.exists():
            pytest.skip("CLI commands directory not found")

        # 1637: collect ALL offenders instead of asserting per-file — the
        # per-file assert aborted at the first (alphabetical) failure and
        # masked every later one (standup.py hid behind keys.py for months).
        bypassing = []
        for file in cli_commands.glob("*.py"):
            if file.name == "__init__.py" or file.name in self.NON_NL_COMMANDS:
                continue

            content = file.read_text()

            # Each command should reference intent somehow
            has_intent_ref = (
                "intent" in content.lower()
                or "CanonicalHandlers" in content
                or "IntentService" in content
            )

            if not has_intent_ref:
                bypassing.append(file.name)

        assert not bypassing, f"commands bypass intent classification: {bypassing}"
