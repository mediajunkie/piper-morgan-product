"""
Integration Tests for CLI Standup Command
Tests the complete CLI standup functionality with real service integration
"""

import asyncio
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from cli.commands.standup import StandupCommand


class TestCLIStandupIntegration:
    """Integration tests for CLI standup command"""

    @pytest.fixture
    def standup_command(self):
        """Create a standup command instance with mocked skill"""
        with patch("cli.commands.standup.StandupWorkflowSkill") as mock_skill_cls:
            mock_skill = MagicMock()
            mock_skill_cls.return_value = mock_skill
            cmd = StandupCommand()
            cmd._mock_skill = mock_skill  # expose for assertions
            yield cmd

    @pytest.fixture
    def mock_skill(self):
        """Mock StandupWorkflowSkill at the import location"""
        with patch("cli.commands.standup.StandupWorkflowSkill") as mock_skill_cls:
            mock_skill_instance = MagicMock()
            mock_skill_cls.return_value = mock_skill_instance
            yield mock_skill_cls, mock_skill_instance

    @pytest.mark.asyncio
    async def test_standup_command_initialization(self, mock_skill):
        """Test that standup command initializes correctly with mocked skill"""
        mock_skill_cls, mock_skill_instance = mock_skill
        standup = StandupCommand()

        assert standup.skill is not None
        mock_skill_cls.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_standup_complete_sequence(self, mock_skill):
        """Test complete standup sequence execution"""
        mock_skill_cls, mock_skill_instance = mock_skill

        mock_skill_instance.execute = AsyncMock(
            return_value={
                "success": True,
                "standup": {
                    "yesterday_accomplishments": ["Closed issue #1302", "Deployed fix"],
                    "today_priorities": ["Review PR", "Write tests"],
                    "blockers": [],
                },
                "execution_time_ms": 500,
                "tokens_saved": 12000,
                "posted_to": [],
                "issues_created": 0,
                "issues_closed": 0,
            }
        )

        standup = StandupCommand()
        results = await standup.run_standup()

        assert results.get("success") is True
        assert "yesterday_accomplishments" in results
        assert "today_priorities" in results
        assert "blockers" in results
        assert "error" not in results
        mock_skill_instance.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_standup_with_skill_failure(self, mock_skill):
        """Test standup execution when skill fails"""
        mock_skill_cls, mock_skill_instance = mock_skill

        mock_skill_instance.execute = AsyncMock(
            return_value={"success": False, "message": "Skill execution failed"}
        )

        standup = StandupCommand()
        results = await standup.run_standup()

        assert "error" in results

    @pytest.mark.asyncio
    async def test_run_standup_exception_handling(self, mock_skill):
        """Test graceful error handling when skill raises an exception"""
        mock_skill_cls, mock_skill_instance = mock_skill

        mock_skill_instance.execute = AsyncMock(side_effect=Exception("Unexpected failure"))

        standup = StandupCommand()
        results = await standup.run_standup()

        assert "error" in results

    def test_format_slack_message(self, standup_command):
        """Test Slack message formatting"""
        # Test markdown conversion
        test_content = "**Bold text** and __italic text__ with `code`"
        slack_output = standup_command.format_slack_message(test_content)

        assert "*Bold text*" in slack_output  # ** converted to *
        assert "_italic text_" in slack_output  # __ converted to _
        assert "`code`" in slack_output  # Code blocks preserved

        # Test link removal
        test_content_with_links = "Check [this link](http://example.com) for more info"
        slack_output = standup_command.format_slack_message(test_content_with_links)

        assert "this link" in slack_output
        assert "http://example.com" not in slack_output

        # Test header removal
        test_content_with_headers = "# Header 1\n## Header 2\nContent"
        slack_output = standup_command.format_slack_message(test_content_with_headers)

        # Headers should be removed (regex should strip # and ##)
        assert "# Header 1" not in slack_output
        assert "## Header 2" not in slack_output
        assert "Content" in slack_output

    def test_generate_slack_output(self, standup_command):
        """Test Slack output generation"""
        test_results = {
            "greeting": "Good morning!",
            "time": "Today is Thursday, August 21, 2025 at 4:27 PM",
            "focus": "Q4 2025: MCP implementation",
            "status": "All systems operational",
            "help": "I can help with project management",
        }

        slack_output = standup_command.generate_slack_output(test_results)

        # Verify Slack formatting
        assert "🌅 *Morning Standup Report*" in slack_output
        assert "*Greeting:* Good morning!" in slack_output
        assert "*Current Time:* Today is Thursday" in slack_output
        assert "*Current Focus:* Q4 2025: MCP implementation" in slack_output
        assert "*System Status:* All systems operational" in slack_output

    def test_generate_slack_output_with_error(self, standup_command):
        """Test Slack output generation when there's an error"""
        test_results = {"error": "Service unavailable"}

        slack_output = standup_command.generate_slack_output(test_results)

        assert "❌ Standup failed: Service unavailable" in slack_output

    def test_color_formatting(self, standup_command):
        """Test color formatting methods"""
        # Test basic color formatting
        with patch("builtins.print") as mock_print:
            standup_command.print_colored("Test message", "green")
            mock_print.assert_called_once()

            # Verify color codes are applied
            call_args = mock_print.call_args[0][0]
            assert "\033[92m" in call_args  # Green color code
            assert "\033[0m" in call_args  # Reset color code

    def test_section_formatting(self, standup_command):
        """Test section formatting methods"""
        with patch("builtins.print") as mock_print:
            standup_command.print_section("Test Section", "blue")

            # Should make multiple print calls for section
            assert mock_print.call_count >= 2

    def test_message_formatting(self, standup_command):
        """Test message formatting methods"""
        with patch("builtins.print") as mock_print:
            standup_command.print_success("Success message")
            standup_command.print_info("Info message")
            standup_command.print_warning("Warning message")
            standup_command.print_error("Error message")

            # Should make 4 print calls
            assert mock_print.call_count == 4


class TestCLIStandupErrorHandling:
    """Test error handling in CLI standup command"""

    @pytest.mark.asyncio
    async def test_graceful_skill_failure_handling(self):
        """Test graceful handling when StandupWorkflowSkill fails at init"""
        with patch(
            "cli.commands.standup.StandupWorkflowSkill",
            side_effect=Exception("Service unavailable"),
        ):
            try:
                standup = StandupCommand()
                assert False, "Should have failed gracefully"
            except Exception as e:
                assert "Service unavailable" in str(e)

    @pytest.mark.asyncio
    async def test_standup_execution_error_handling(self):
        """Test error handling during standup execution"""
        with patch("cli.commands.standup.StandupWorkflowSkill") as mock_skill_cls:
            mock_skill_instance = MagicMock()
            mock_skill_instance.execute = AsyncMock(
                side_effect=Exception("Standup skill failed")
            )
            mock_skill_cls.return_value = mock_skill_instance

            standup = StandupCommand()
            results = await standup.run_standup()

            assert "error" in results


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
