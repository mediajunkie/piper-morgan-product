"""
Calendar CLI Commands - Test calendar integration with Morning Standup
Built on GoogleCalendarMCPAdapter for temporal awareness
Note: Named 'cal.py' to avoid conflict with Python's calendar module
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter


class CalendarCommand:
    """Calendar CLI Commands for testing MCP adapter integration"""

    # Color codes for beautiful output
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
    }

    def __init__(self):
        """Initialize calendar command with MCP adapter"""
        self.calendar_adapter = GoogleCalendarMCPAdapter()

    def print_colored(self, text: str, color: str = "reset", bold: bool = False) -> None:
        """Print colored and optionally bold text"""
        color_code = self.COLORS.get(color, self.COLORS["reset"])
        bold_code = self.COLORS["bold"] if bold else ""
        print(f"{bold_code}{color_code}{text}{self.COLORS['reset']}")

    def print_header(self, title: str) -> None:
        """Print a beautiful header"""
        print()
        self.print_colored("=" * 60, "cyan", bold=True)
        self.print_colored(f"  {title}", "cyan", bold=True)
        self.print_colored("=" * 60, "cyan", bold=True)
        print()

    def print_section(self, title: str, color: str = "blue") -> None:
        """Print a section header"""
        print()
        self.print_colored(f"📅 {title}", color, bold=True)
        self.print_colored("-" * 40, color)

    async def cmd_today(self) -> None:
        """Display today's calendar events"""
        self.print_header("TODAY'S CALENDAR")

        try:
            # Get today's events
            events = await self.calendar_adapter.get_todays_events()

            if not events:
                self.print_colored("No events scheduled for today", "yellow")
                return

            for event in events:
                if event.get("is_all_day"):
                    self.print_colored(f"🌅 All Day: {event.get('title', 'Event')}", "magenta")
                else:
                    start = event.get("start_time", "")
                    end = event.get("end_time", "")
                    title = event.get("title", "Event")
                    duration = event.get("duration_minutes", 0)

                    self.print_colored(f"📍 {start} - {end}: {title} ({duration} mins)", "blue")

                    if event.get("attendees"):
                        self.print_colored(f"   👥 {len(event['attendees'])} attendees", "cyan")

        except Exception as e:
            self.print_colored(f"Error fetching calendar: {e}", "red")

    async def cmd_temporal(self) -> None:
        """Display temporal summary for standup integration"""
        self.print_header("TEMPORAL AWARENESS SUMMARY")

        try:
            # Get temporal summary
            summary = await self.calendar_adapter.get_temporal_summary()

            # Current meeting
            if summary.get("current_meeting"):
                current = summary["current_meeting"]
                self.print_section("CURRENTLY IN MEETING", "red")
                self.print_colored(
                    f"🔴 {current.get('title', 'Meeting')} (ends {current.get('end_time', 'soon')})",
                    "red",
                    bold=True,
                )

            # Next meeting
            if summary.get("next_meeting"):
                next_meeting = summary["next_meeting"]
                self.print_section("NEXT MEETING", "yellow")
                self.print_colored(
                    f"⏰ {next_meeting.get('title', 'Meeting')} at {next_meeting.get('start_time', 'TBD')}",
                    "yellow",
                )

            # Free time blocks
            free_blocks = summary.get("free_blocks", [])
            if free_blocks:
                self.print_section("FOCUS TIME BLOCKS", "green")
                for block in free_blocks[:3]:  # Top 3 blocks
                    duration = block.get("duration_minutes", 0)
                    if duration >= 30:  # Only show blocks 30+ mins
                        self.print_colored(
                            f"🎯 {block.get('start', '')} - {block.get('end', '')}: {duration} mins free",
                            "green",
                        )

            # Statistics
            stats = summary.get("stats", {})
            if stats:
                self.print_section("TODAY'S STATISTICS", "cyan")
                self.print_colored(f"📊 Meetings: {stats.get('total_meetings_today', 0)}", "cyan")
                self.print_colored(
                    f"⏱️  Meeting time: {stats.get('total_meeting_time_minutes', 0) / 60:.1f} hours",
                    "cyan",
                )
                self.print_colored(
                    f"🆓 Free time: {stats.get('total_free_time_minutes', 0) / 60:.1f} hours",
                    "cyan",
                )

        except Exception as e:
            self.print_colored(f"Error getting temporal summary: {e}", "red")

    async def cmd_health(self) -> None:
        """Check calendar adapter health"""
        self.print_header("CALENDAR ADAPTER HEALTH CHECK")

        try:
            # Check adapter health
            health_result = await self.calendar_adapter.health_check()

            if health_result:
                self.print_colored("✅ Calendar adapter is healthy", "green", bold=True)

                # Try to get minimal data to confirm connectivity
                events = await self.calendar_adapter.get_todays_events()
                if isinstance(events, list):
                    self.print_colored(f"📅 Found {len(events)} events today", "green")
                else:
                    self.print_colored("⚠️  Calendar accessible but no events retrieved", "yellow")
            else:
                self.print_colored("❌ Calendar adapter is not healthy", "red")
                self.print_colored("Check Google Calendar authentication and credentials", "yellow")

        except Exception as e:
            self.print_colored(f"❌ Health check failed: {e}", "red")


async def main():
    """Main entry point for calendar CLI commands"""
    import argparse

    parser = argparse.ArgumentParser(description="Calendar CLI Commands")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subcommands
    subparsers.add_parser("today", help="Show today's calendar events")
    subparsers.add_parser("temporal", help="Show temporal awareness summary")
    subparsers.add_parser("health", help="Check calendar adapter health")

    args = parser.parse_args()

    # Execute command
    cmd = CalendarCommand()

    if args.command == "today":
        await cmd.cmd_today()
    elif args.command == "temporal":
        await cmd.cmd_temporal()
    elif args.command == "health":
        await cmd.cmd_health()
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
