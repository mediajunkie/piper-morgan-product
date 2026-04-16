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
        """Create a standup command instance for testing"""
        return StandupCommand()

    @pytest.fixture
    def mock_services(self):
        """Mock the required services"""
        with (
            patch("cli.commands.standup.SessionManager") as mock_session_manager,
            patch("cli.commands.standup.ConversationHandler") as mock_conversation_handler,
            patch("cli.commands.standup.ConversationQueryService") as mock_conversation_queries,
        ):
            # Mock session manager
            mock_session_manager.return_value = MagicMock()

            # Mock conversation handler
            mock_conversation_handler.return_value = MagicMock()

            # Mock conversation queries service
            mock_queries = MagicMock()
            mock_queries.get_greeting = AsyncMock(
                return_value="Good morning! Ready for our daily standup?"
            )
            mock_queries.get_help = AsyncMock(
                return_value="I can help you with project management, daily operations, and development support."
            )
            mock_queries.get_status = AsyncMock(
                return_value="I'm operating normally. All systems are go!"
            )
            mock_conversation_queries.return_value = mock_queries

            yield {
                "session_manager": mock_session_manager,
                "conversation_handler": mock_conversation_handler,
                "conversation_queries": mock_conversation_queries,
            }

    @pytest.mark.asyncio
    async def test_standup_command_initialization(self, mock_services):
        """Test that standup command initializes correctly with mocked services"""
        standup = StandupCommand()

        assert standup.session_manager is not None
        assert standup.conversation_handler is not None
        assert standup.conversation_queries is not None

        # Verify services were called
        mock_services["session_manager"].assert_called_once_with(ttl_minutes=30)
        mock_services["conversation_handler"].assert_called_once()
        mock_services["conversation_queries"].assert_called_once()

    @pytest.mark.asyncio
    async def test_get_greeting_success(self, mock_services):
        """Test successful greeting retrieval with mocked services"""
        # Create standup command with mocked services
        with (
            patch("cli.commands.standup.SessionManager") as mock_session_manager,
            patch("cli.commands.standup.ConversationHandler") as mock_conversation_handler,
            patch("cli.commands.standup.ConversationQueryService") as mock_conversation_queries,
        ):
            # Mock session manager
            mock_session_manager.return_value = MagicMock()

            # Mock conversation handler
            mock_conversation_handler.return_value = MagicMock()

            # Mock conversation queries service
            mock_queries = MagicMock()
            mock_queries.get_greeting = AsyncMock(
                return_value="Good morning! Ready for our daily standup?"
            )
            mock_conversation_queries.return_value = mock_queries

            # Create standup command with mocked services
            standup = StandupCommand()
            greeting = await standup.get_greeting()

            # Verify greeting
            assert greeting == "Good morning! Ready for our daily standup?"
            mock_queries.get_greeting.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_greeting_fallback(self, standup_command):
        """Test greeting fallback when service fails"""
        with patch.object(
            standup_command.conversation_queries,
            "get_greeting",
            side_effect=Exception("Service unavailable"),
        ):
            greeting = await standup_command.get_greeting()

            assert "Good morning" in greeting
            assert "standup" in greeting.lower()

    @pytest.mark.asyncio
    async def test_get_help_success(self, standup_command, mock_services):
        """Test successful help retrieval"""
        help_text = await standup_command.get_help()

        assert "project management" in help_text.lower()
        assert "daily operations" in help_text.lower()
        assert "development support" in help_text.lower()
        mock_services["conversation_queries"].return_value.get_help.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_status_success(self, standup_command, mock_services):
        """Test successful status retrieval"""
        status = await standup_command.get_status()

        assert "operating normally" in status.lower()
        assert "systems are go" in status.lower()
        mock_services["conversation_queries"].return_value.get_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_standup_complete_sequence(self, standup_command, mock_services):
        """Test complete standup sequence execution"""
        results = await standup_command.run_standup()

        # Verify all expected results are present
        assert "greeting" in results
        assert "help" in results
        assert "status" in results
        assert "time" in results
        assert "focus" in results
        assert "error" not in results

        # Verify service calls
        mock_queries = mock_services["conversation_queries"].return_value
        mock_queries.get_greeting.assert_called_once()
        mock_queries.get_help.assert_called_once()
        mock_queries.get_status.assert_called_once()

    @pytest.mark.asyncio
    async def test_run_standup_with_service_failure(self, standup_command):
        """Test standup execution when services fail"""
        with patch.object(
            standup_command.conversation_queries,
            "get_greeting",
            side_effect=Exception("Service error"),
        ):
            results = await standup_command.run_standup()

            # Should still get some results
            assert "time" in results
            assert "focus" in results
            # Greeting should have fallback
            assert "greeting" in results

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
    async def test_graceful_service_failure_handling(self):
        """Test graceful handling when all services fail"""
        with patch(
            "cli.commands.standup.SessionManager", side_effect=Exception("Service unavailable")
        ):
            # Should not crash, should handle gracefully
            try:
                standup = StandupCommand()
                # This should fail gracefully
                assert False, "Should have failed gracefully"
            except Exception as e:
                # Should fail with a meaningful error
                assert "Service unavailable" in str(e)

    @pytest.mark.asyncio
    async def test_standup_execution_error_handling(self):
        """Test error handling during standup execution"""
        standup = StandupCommand()

        # Mock all services to fail
        with (
            patch.object(
                standup.conversation_queries,
                "get_greeting",
                side_effect=Exception("Greeting service failed"),
            ),
            patch.object(
                standup.conversation_queries,
                "get_help",
                side_effect=Exception("Help service failed"),
            ),
            patch.object(
                standup.conversation_queries,
                "get_status",
                side_effect=Exception("Status service failed"),
            ),
        ):
            results = await standup.run_standup()

            # Should still get time and focus (hardcoded)
            assert "time" in results
            assert "focus" in results
            # Should have fallback values for failed services
            assert "greeting" in results
            assert "help" in results
            assert "status" in results


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
