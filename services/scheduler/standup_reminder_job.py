"""
Standup Reminder Job

Sends daily Slack reminders for standup generation.
Queries user preferences, checks timezone/time, and sends DMs via SlackClient.

Issue: #161 (CORE-STAND-SLACK-REMIND)
Task: 1 of 4 - Reminder Job Implementation
"""

import asyncio
from datetime import datetime, time
from typing import Any, Dict, List, Optional
from uuid import UUID
from zoneinfo import ZoneInfo

import structlog

from services.domain.user_preference_manager import UserPreferenceManager
from services.infrastructure.task_manager import RobustTaskManager
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

logger = structlog.get_logger(__name__)


class StandupReminderJob:
    """
    Daily standup reminder job.

    Responsibilities:
    - Query users with reminders enabled
    - Check if it's reminder time for each user (timezone-aware)
    - Send Slack DMs via SlackIntegrationRouter
    - Log results for monitoring

    Architecture:
    - Integrates with RobustTaskManager for error handling
    - Uses SlackIntegrationRouter for DM delivery
    - Uses UserPreferenceManager for user configuration
    """

    def __init__(
        self,
        task_manager: RobustTaskManager,
        slack_router: SlackIntegrationRouter,
        preference_manager: UserPreferenceManager,
    ):
        """
        Initialize reminder job with dependencies.

        Args:
            task_manager: RobustTaskManager for error handling and tracking
            slack_router: SlackIntegrationRouter for sending Slack DMs
            preference_manager: UserPreferenceManager for user preferences
        """
        self.task_manager = task_manager
        self.slack_router = slack_router
        self.preference_manager = preference_manager

    async def execute_daily_reminders(self) -> Dict[str, Any]:
        """
        Execute daily reminder check and send.

        Process:
        1. Get all users with reminders enabled
        2. For each user, check if it's their reminder time
        3. Send reminder DM via SlackClient
        4. Log and return results

        Returns:
            Dict with results:
            {
                "checked": int,      # Users checked
                "sent": int,         # Reminders sent successfully
                "failed": int,       # Failed deliveries
                "errors": List[str]  # Error messages
            }
        """
        logger.info("Starting daily reminder execution")

        results = {"checked": 0, "sent": 0, "failed": 0, "errors": []}

        try:
            # Get all users with reminders enabled
            enabled_users = await self._get_enabled_users()
            results["checked"] = len(enabled_users)

            logger.info(
                "Checked enabled users",
                count=len(enabled_users),
            )

            # Process each enabled user
            for user_id in enabled_users:
                try:
                    # Check if it's reminder time for this user
                    should_send = await self._should_send_reminder(user_id)

                    if should_send:
                        # Send the reminder
                        success = await self._send_reminder(user_id)

                        if success:
                            results["sent"] += 1
                            logger.info("Reminder sent successfully", user_id=user_id)
                        else:
                            results["failed"] += 1
                            error_msg = f"Failed to send reminder to {user_id}"
                            results["errors"].append(error_msg)
                            logger.warning(error_msg)

                except Exception as e:
                    results["failed"] += 1
                    error_msg = f"Error processing user {user_id}: {str(e)}"
                    results["errors"].append(error_msg)
                    logger.error(
                        "Error processing user reminder",
                        user_id=user_id,
                        error=str(e),
                    )

            logger.info(
                "Daily reminder execution complete",
                checked=results["checked"],
                sent=results["sent"],
                failed=results["failed"],
            )

        except Exception as e:
            error_msg = f"Critical error in reminder execution: {str(e)}"
            results["errors"].append(error_msg)
            logger.error("Critical error in reminder execution", error=str(e))

        return results

    async def _get_enabled_users(self) -> List[str]:
        """
        Get list of user IDs with reminders enabled.

        NOTE: This is a placeholder implementation for Task 1.
        Task 2 will implement actual preference keys and querying.

        For now, returns empty list (no users) to prevent spam during testing.

        Returns:
            List of user IDs with reminders enabled
        """
        # TODO (Task 2): Query UserPreferenceManager for users with
        # standup_reminder_enabled = True

        # Placeholder: Return empty list to prevent accidental spam
        # Task 2 will implement:
        # users = await self.preference_manager.get_users_with_preference(
        #     "standup_reminder_enabled", True
        # )

        logger.debug("Getting enabled users (placeholder implementation)")
        return []  # Empty for Task 1 safety

    async def _should_send_reminder(self, user_id: str) -> bool:
        """
        Check if reminder should be sent for user based on time/timezone.

        Logic:
        1. Get user's reminder time preference (e.g., "06:00")
        2. Get user's timezone preference (e.g., "America/Los_Angeles")
        3. Get user's reminder days preference (e.g., [0,1,2,3,4] for Mon-Fri)
        4. Convert current time to user's timezone
        5. Check if current time matches reminder time
        6. Check if today is a reminder day

        Args:
            user_id: Slack user ID

        Returns:
            True if reminder should be sent now, False otherwise
        """
        try:
            # Get user preferences (placeholder for Task 1)
            prefs = await self._get_user_reminder_preferences(user_id)

            # Parse reminder time (format: "HH:MM")
            reminder_time_str = prefs.get("time", "06:00")
            reminder_hour, reminder_minute = map(int, reminder_time_str.split(":"))

            # Get user's timezone
            user_tz_str = prefs.get("timezone", "America/Los_Angeles")
            user_tz = ZoneInfo(user_tz_str)

            # Get current time in user's timezone
            user_now = datetime.now(user_tz)

            # Check if it's the right time (within 1-hour window since we check hourly)
            # This allows for reminder time between HH:00 and HH:59
            time_matches = user_now.hour == reminder_hour

            if not time_matches:
                return False

            # Check if today is a reminder day
            reminder_days = prefs.get("days", [0, 1, 2, 3, 4])  # Mon-Fri default
            today_weekday = user_now.weekday()  # 0=Monday, 6=Sunday

            if today_weekday not in reminder_days:
                logger.debug(
                    "Not a reminder day for user",
                    user_id=user_id,
                    weekday=today_weekday,
                    reminder_days=reminder_days,
                )
                return False

            logger.debug(
                "Reminder time matched for user",
                user_id=user_id,
                user_time=user_now.strftime("%Y-%m-%d %H:%M %Z"),
            )

            return True

        except Exception as e:
            logger.error(
                "Error checking reminder time for user",
                user_id=user_id,
                error=str(e),
            )
            return False

    async def _send_reminder(self, user_id: str) -> bool:
        """
        Send reminder DM to user via SlackIntegrationRouter.

        Uses ReminderMessageFormatter to create personalized, timezone-aware
        reminder with web/CLI/API access methods.

        Args:
            user_id: Slack user ID (used as channel for DM)

        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            # Get user's timezone for personalized greeting
            user_tz = await self.preference_manager.get_reminder_timezone(user_id)

            # Format message using ReminderMessageFormatter
            from services.integrations.slack.reminder_formatter import get_reminder_formatter

            formatter = get_reminder_formatter()
            message = formatter.format_reminder_message(user_id, user_tz)

            # Send DM via SlackIntegrationRouter
            # User ID as channel = Direct Message
            # #1110: the reminder recipient IS the user whose credentials we use,
            # so user_id scopes both the DM target and the config lookup.
            response = await self.slack_router.send_message(
                channel=user_id, text=message, user_id=user_id
            )

            # Check if send was successful
            # SlackResponse has success property
            success = response.success if hasattr(response, "success") else False

            if success:
                logger.info("Reminder DM sent successfully", user_id=user_id, timezone=user_tz)
            else:
                logger.warning(
                    "Reminder DM failed",
                    user_id=user_id,
                    response=str(response),
                )

            return success

        except Exception as e:
            logger.error(
                "Error sending reminder DM",
                user_id=user_id,
                error=str(e),
            )
            return False

    async def _get_user_reminder_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get reminder preferences for user from UserPreferenceManager.

        Uses the preference_manager.get_reminder_preferences() method which
        returns defaults if not explicitly set.

        Args:
            user_id: Slack user ID

        Returns:
            Dict with reminder preferences:
            {
                "enabled": bool,
                "time": str (HH:MM format),
                "timezone": str (timezone name),
                "days": List[int] (0=Mon, 6=Sun)
            }
        """
        # Query actual preferences from UserPreferenceManager (Task 2 implementation)
        return await self.preference_manager.get_reminder_preferences(user_id)
