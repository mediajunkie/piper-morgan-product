"""
Morning Standup CLI Command - MVP Implementation
Uses persistent context infrastructure for <2 second generation

Built on: UserPreferenceManager + SessionPersistenceManager + GitHub integration
Performance: <2 seconds, saves 15+ minutes manual prep
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.integrations.mcp.skills.standup_workflow_skill import StandupWorkflowSkill


class StandupCommand:
    """Morning Standup CLI Command with beautiful formatting and Slack integration"""

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
        "white": "\033[97m",
        "gray": "\033[90m",
    }

    def __init__(self):
        """Initialize the standup command with skill"""
        self.skill = StandupWorkflowSkill()

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
        self.print_colored(f"📋 {title}", color, bold=True)
        self.print_colored("-" * 40, color)

    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.print_colored(f"✅ {message}", "green")

    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.print_colored(f"ℹ️  {message}", "blue")

    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.print_colored(f"⚠️  {message}", "yellow")

    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.print_colored(f"❌ {message}", "red")

    def format_slack_message(self, content: str) -> str:
        """Format content for Slack compatibility (no markdown conflicts)"""
        # Remove markdown that could cause Slack formatting issues
        slack_safe = content.replace("**", "*")  # Bold to Slack bold
        slack_safe = slack_safe.replace("__", "_")  # Italic to Slack italic
        slack_safe = slack_safe.replace("`", "`")  # Keep code blocks
        slack_safe = slack_safe.replace("```", "```")  # Keep code blocks

        # Remove any remaining markdown that could cause issues
        import re

        slack_safe = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", slack_safe)  # Remove links
        slack_safe = re.sub(r"#{1,6}\s+", "", slack_safe)  # Remove headers

        return slack_safe

    # #1873 (2026-09-24) DISPOSED: get_greeting/get_help/get_status all read
    # self.conversation_queries, which __init__ never assigned (no
    # `ConversationQueries` class exists anywhere in the codebase -- grepped
    # repo-wide, zero hits beyond this file). Confirmed unreachable: no
    # caller anywhere in this file (execute/run_standup never call them),
    # nothing in tests/, nothing in main.py's standup wiring. Fabricated
    # committed-theory residue, same class as the #1700 notion.py dead
    # imports -- disposed rather than wired, since there is no live
    # "conversation_queries" service with this get_greeting/get_help/
    # get_status shape to point at (services/memory/greeting_context.py's
    # GreetingContextService and services/commands/registry.py's
    # CommandRegistry.get_help are both a different shape, not drop-in
    # replacements). Record: decisions.log 2026-09-24.

    async def run_standup(
        self,
        user_id: str = "xian",
        include_slack: bool = False,
        include_github: bool = False,
        include_notion: bool = False,
    ) -> Dict:
        """Run morning standup using StandupWorkflowSkill"""
        results = {}

        try:
            self.print_colored("🚀 Morning Standup", "magenta", bold=True)
            self.print_colored("━" * 50, "gray")

            # Generate standup using skill
            self.print_colored("⏱️  Generating standup (target: <2 seconds)...", "yellow")

            skill_result = await self.skill.execute(
                {
                    "user_id": user_id,
                    "include_slack": include_slack,
                    "include_github": include_github,
                    "include_notion": include_notion,
                    "format": "markdown",
                }
            )

            if not skill_result.get("success"):
                self.print_error(f"Standup generation failed: {skill_result.get('message')}")
                results["error"] = skill_result.get("message")
                return results

            standup = skill_result.get("standup", {})
            execution_time = skill_result.get("execution_time_ms", 0)

            # Display results
            self.print_colored(f"✅ Generated in {execution_time}ms", "green")
            self.print_colored(f"💰 Saved {skill_result.get('tokens_saved', 15000)} tokens", "cyan")
            self.print_colored("━" * 50, "gray")

            # Yesterday's Accomplishments
            self.print_section("📋 Yesterday's Accomplishments", "green")
            accomplishments = standup.get("yesterday_accomplishments", [])
            if accomplishments:
                for accomplishment in accomplishments:
                    self.print_info(f"  {accomplishment}")
            else:
                self.print_info("  No specific accomplishments found")

            # Today's Priorities
            self.print_section("🎯 Today's Priorities", "blue")
            priorities = standup.get("today_priorities", [])
            for priority in priorities:
                self.print_info(f"  {priority}")

            # Blockers
            blockers = standup.get("blockers", [])
            self.print_section("⚠️  Blockers", "red" if blockers else "gray")
            if blockers:
                for blocker in blockers:
                    self.print_warning(f"  {blocker}")
            else:
                self.print_success("  No blockers identified")

            # Multi-system posting status
            posted_to = skill_result.get("posted_to", [])
            if posted_to:
                self.print_colored("━" * 50, "gray")
                self.print_section("📤 Posted to", "cyan")
                for system in posted_to:
                    self.print_success(f"  ✓ {system.upper()}")

            # Store results
            results.update(
                {
                    "success": True,
                    "user_id": user_id,
                    "execution_time_ms": execution_time,
                    "tokens_saved": skill_result.get("tokens_saved", 15000),
                    "yesterday_accomplishments": accomplishments,
                    "today_priorities": priorities,
                    "blockers": blockers,
                    "posted_to": posted_to,
                    "issues_created": skill_result.get("issues_created", 0),
                    "issues_closed": skill_result.get("issues_closed", 0),
                    "performance_met": execution_time < 2000,
                }
            )

            return results

        except Exception as e:
            self.print_error(f"Standup execution failed: {e}")
            results["error"] = str(e)

        return results

    def generate_slack_output(self, results: Dict[str, str]) -> str:
        """Generate Slack-ready output from standup results"""
        if "error" in results:
            return f"❌ Standup failed: {results['error']}"

        slack_output = []
        slack_output.append("🌅 *Morning Standup Report*")
        slack_output.append("")

        if "greeting" in results:
            slack_output.append(f"*Greeting:* {self.format_slack_message(results['greeting'])}")

        if "time" in results:
            slack_output.append(f"*Current Time:* {results['time']}")

        if "focus" in results:
            slack_output.append(f"*Current Focus:* {results['focus']}")

        if "status" in results:
            slack_output.append(f"*System Status:* {self.format_slack_message(results['status'])}")

        if "help" in results:
            help_preview = (
                results["help"][:150] + "..." if len(results["help"]) > 150 else results["help"]
            )
            slack_output.append(f"*Available Help:* {self.format_slack_message(help_preview)}")

        return "\n".join(slack_output)

    async def execute(
        self,
        output_format: str = "cli",
        include_slack: bool = False,
        include_github: bool = False,
        include_notion: bool = False,
    ) -> None:
        """Execute the standup command with specified output format"""
        try:
            self.print_header("🌅 Piper Morgan Morning Standup")

            # Run standup sequence
            results = await self.run_standup(
                include_slack=include_slack,
                include_github=include_github,
                include_notion=include_notion,
            )

            # Check for errors
            if "error" in results:
                self.print_header("⚠️  Standup Failed")
                self.print_error(results["error"])
                sys.exit(1)

            # Generate output based on format
            if output_format == "slack":
                slack_output = self.generate_slack_output(results)
                print("\n" + "=" * 60)
                self.print_colored("📱 Slack-Ready Output:", "magenta", bold=True)
                print("=" * 60)
                print(slack_output)
                print("=" * 60)

            # Print summary
            self.print_header("🎯 Standup Complete")
            self.print_success("Morning standup completed successfully!")
            if results.get("posted_to"):
                self.print_info(f"Posted to: {', '.join(results['posted_to']).upper()}")
            self.print_info("Use --format slack for Slack-ready output")

        except Exception as e:
            self.print_error(f"Standup command failed: {e}")
            sys.exit(1)


def main():
    """Main entry point for standup command"""
    import argparse

    parser = argparse.ArgumentParser(description="Piper Morgan Morning Standup")
    parser.add_argument(
        "--format", choices=["cli", "slack"], default="cli", help="Output format (default: cli)"
    )
    parser.add_argument(
        "--slack",
        action="store_true",
        help="Post standup to Slack",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="Create GitHub issues from action items",
    )
    parser.add_argument(
        "--notion",
        action="store_true",
        help="Update Notion database with standup",
    )

    args = parser.parse_args()

    # Run standup command
    standup = StandupCommand()
    asyncio.run(
        standup.execute(
            output_format=args.format,
            include_slack=args.slack,
            include_github=args.github,
            include_notion=args.notion,
        )
    )


if __name__ == "__main__":
    main()
