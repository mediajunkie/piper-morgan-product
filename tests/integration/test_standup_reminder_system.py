"""
Integration tests for Slack standup reminder system.

Tests the complete flow:
- Timer loop → User preferences → Message formatting → Slack delivery

Verifies:
- End-to-end integration
- Error handling
- Edge cases
- Performance

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 4 of 4 - Integration Testing & Final Verification
"""

import asyncio
import time as time_module
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from services.domain.user_preference_manager import UserPreferenceManager
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.reminder_formatter import ReminderMessageFormatter
from services.scheduler.standup_reminder_job import StandupReminderJob


class TestStandupReminderIntegration:
    """Integration tests for complete reminder system."""

    @pytest.fixture
    async def reminder_system(self):
        """Set up complete reminder system with mocked dependencies."""
        # Create real components
        task_manager = RobustTaskManager()
        preference_manager = UserPreferenceManager()
        formatter = ReminderMessageFormatter()

        # Mock SlackIntegrationRouter (avoid real Slack calls)
        mock_slack_router = AsyncMock()
        mock_response = MagicMock()
        mock_response.success = True
        mock_slack_router.send_message.return_value = mock_response

        # Create reminder job with mocked Slack
        reminder_job = StandupReminderJob(
            task_manager=task_manager,
            slack_router=mock_slack_router,
            preference_manager=preference_manager,
        )

        return {
            "job": reminder_job,
            "preferences": preference_manager,
            "formatter": formatter,
            "slack_mock": mock_slack_router,
            "task_manager": task_manager,
        }

    @pytest.mark.asyncio
    async def test_complete_reminder_flow(self, reminder_system):
        """
        Test complete reminder flow from preferences to Slack delivery.

        Verifies:
        - User preferences retrieved
        - Timezone checking works
        - Message formatted correctly
        - Slack message sent
        """
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Set up test user with reminders enabled
        test_user_id = "test_user_123"
        await prefs.set_reminder_enabled(test_user_id, True)
        await prefs.set_reminder_time(test_user_id, "06:00")
        await prefs.set_reminder_timezone(test_user_id, "America/Los_Angeles")
        await prefs.set_reminder_days(test_user_id, [0, 1, 2, 3, 4])  # Mon-Fri

        # Mock _get_enabled_users to return our test user
        with patch.object(job, "_get_enabled_users", return_value=[test_user_id]):
            # Mock time to 6:00 AM PT on a Monday
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                mock_now = datetime(2025, 10, 20, 6, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now
                mock_dt.side_effect = lambda *args, **kw: datetime(*args, **kw)

                # Execute reminder check
                result = await job.execute_daily_reminders()

                # Verify Slack message was sent
                assert slack_mock.send_message.called
                call_args = slack_mock.send_message.call_args

                # Verify message to correct user
                assert call_args[1]["channel"] == test_user_id

                # Verify message content
                message = call_args[1]["text"]
                # day-part-agnostic (#1452: 'Good morning' failed afternoon CI
                # runs — the greeting varies by wall clock; the standup content
                # is the stable contract)
                assert "Time for your daily standup" in message
                assert "Web:" in message
                assert "CLI:" in message
                assert "API:" in message

    @pytest.mark.asyncio
    async def test_reminder_disabled(self, reminder_system):
        """Test that reminders are not sent when disabled."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Set up test user with reminders DISABLED
        test_user_id = "test_user_456"
        await prefs.set_reminder_enabled(test_user_id, False)

        # Execute reminder check
        result = await job.execute_daily_reminders()

        # Verify NO Slack message was sent
        assert not slack_mock.send_message.called

    @pytest.mark.asyncio
    async def test_wrong_time(self, reminder_system):
        """Test that reminders are not sent at wrong time."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Set up test user with reminder at 6 AM
        test_user_id = "test_user_789"
        await prefs.set_reminder_enabled(test_user_id, True)
        await prefs.set_reminder_time(test_user_id, "06:00")
        await prefs.set_reminder_timezone(test_user_id, "America/Los_Angeles")

        # Mock _get_enabled_users to return our test user
        with patch.object(job, "_get_enabled_users", return_value=[test_user_id]):
            # Mock time to 3 PM PT (wrong time)
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                mock_now = datetime(2025, 10, 20, 15, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now

                # Execute reminder check
                result = await job.execute_daily_reminders()

                # Verify NO message sent
                assert not slack_mock.send_message.called

    @pytest.mark.asyncio
    async def test_wrong_day(self, reminder_system):
        """Test that reminders are not sent on disabled days."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Set up test user with reminders on weekdays only
        test_user_id = "test_user_101"
        await prefs.set_reminder_enabled(test_user_id, True)
        await prefs.set_reminder_time(test_user_id, "06:00")
        await prefs.set_reminder_timezone(test_user_id, "America/Los_Angeles")
        await prefs.set_reminder_days(test_user_id, [0, 1, 2, 3, 4])  # Mon-Fri

        # Mock _get_enabled_users to return our test user
        with patch.object(job, "_get_enabled_users", return_value=[test_user_id]):
            # Mock time to 6 AM PT on a Sunday (wrong day)
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                # Sunday = weekday 6
                mock_now = datetime(2025, 10, 26, 6, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now

                # Execute reminder check
                result = await job.execute_daily_reminders()

                # Verify NO message sent
                assert not slack_mock.send_message.called

    @pytest.mark.asyncio
    async def test_slack_failure_handling(self, reminder_system):
        """Test that Slack send failures are handled gracefully."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Make Slack mock fail
        mock_response = MagicMock()
        mock_response.success = False
        slack_mock.send_message.return_value = mock_response

        # Set up test user
        test_user_id = "test_user_202"
        await prefs.set_reminder_enabled(test_user_id, True)
        await prefs.set_reminder_time(test_user_id, "06:00")

        # Mock _get_enabled_users to return our test user
        with patch.object(job, "_get_enabled_users", return_value=[test_user_id]):
            # Mock correct time
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                mock_now = datetime(2025, 10, 20, 6, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now

                # Execute - should not crash
                result = await job.execute_daily_reminders()

                # System should handle failure gracefully
                assert result is not None

    @pytest.mark.asyncio
    async def test_timezone_edge_cases(self, reminder_system):
        """Test timezone boundary conditions."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]

        # Test various timezones
        timezones = [
            "America/Los_Angeles",  # PT
            "America/New_York",  # ET
            "Europe/London",  # GMT
            "Asia/Tokyo",  # JST
        ]

        for tz in timezones:
            user_id = f"user_{tz.replace('/', '_')}"
            await prefs.set_reminder_enabled(user_id, True)
            await prefs.set_reminder_time(user_id, "06:00")
            await prefs.set_reminder_timezone(user_id, tz)

            # Should not crash for any timezone
            result = await job.execute_daily_reminders()
            assert result is not None

    @pytest.mark.asyncio
    async def test_message_formatting_integration(self, reminder_system):
        """Test that message formatter integrates correctly."""
        formatter = reminder_system["formatter"]

        # Test message formatting for various timezones
        timezones = ["America/Los_Angeles", "America/New_York", "Europe/London"]

        for tz in timezones:
            message = formatter.format_reminder_message("test_user", tz)

            # Verify all required components
            assert "Generate your standup:" in message
            assert "Web:" in message
            assert "CLI:" in message
            assert "API:" in message
            assert "Disable reminders:" in message

            # Verify greeting is present (any greeting)
            greetings = ["Good morning", "Good afternoon", "Good evening", "Hello"]
            assert any(greeting in message for greeting in greetings)

    @pytest.mark.asyncio
    async def test_multiple_users(self, reminder_system):
        """Test handling multiple users with different preferences."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]
        slack_mock = reminder_system["slack_mock"]

        # Set up multiple users
        users = [
            ("user_1", True, "06:00", "America/Los_Angeles"),
            ("user_2", True, "06:00", "America/New_York"),
            ("user_3", False, "06:00", "Europe/London"),  # Disabled
        ]

        for user_id, enabled, time, tz in users:
            await prefs.set_reminder_enabled(user_id, enabled)
            await prefs.set_reminder_time(user_id, time)
            await prefs.set_reminder_timezone(user_id, tz)
            await prefs.set_reminder_days(user_id, [0, 1, 2, 3, 4])

        # Mock _get_enabled_users to return all users
        user_ids = [user[0] for user in users]
        with patch.object(job, "_get_enabled_users", return_value=user_ids):
            # Mock time to 6 AM PT on Monday
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                mock_now = datetime(2025, 10, 20, 6, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now

                # Execute
                result = await job.execute_daily_reminders()

                # Should handle multiple users
                assert result is not None

    @pytest.mark.asyncio
    async def test_performance_multiple_users(self, reminder_system):
        """Test performance with many users."""
        job = reminder_system["job"]
        prefs = reminder_system["preferences"]

        # Set up 50 users
        user_ids = []
        for i in range(50):
            user_id = f"user_{i}"
            user_ids.append(user_id)
            await prefs.set_reminder_enabled(user_id, True)
            await prefs.set_reminder_time(user_id, "06:00")
            await prefs.set_reminder_timezone(user_id, "America/Los_Angeles")

        # Measure execution time
        start = time_module.time()

        # Mock _get_enabled_users to return all 50 users
        with patch.object(job, "_get_enabled_users", return_value=user_ids):
            with patch("services.scheduler.standup_reminder_job.datetime") as mock_dt:
                mock_now = datetime(2025, 10, 20, 6, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
                mock_dt.now.return_value = mock_now

                result = await job.execute_daily_reminders()

        duration = time_module.time() - start

        # Should complete in reasonable time (< 5 seconds for 50 users)
        assert duration < 5.0
        print(f"\nPerformance: 50 users processed in {duration:.2f}s")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
