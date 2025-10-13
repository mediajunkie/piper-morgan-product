#!/usr/bin/env python3
"""
Publish Command - CLI interface for publishing content to various platforms

Supports publishing markdown files to Notion with proper error handling
and user feedback for conversion warnings.
"""

import argparse
import asyncio
import os

# Add the project root to Python path
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# CRITICAL: Load environment variables FIRST before importing services
from dotenv import load_dotenv

load_dotenv()

# Now safe to import services that depend on environment variables
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.publishing.publisher import Publisher


class PublishCommand:
    """CLI command for publishing content to various platforms"""

    def __init__(self):
        self.publisher = None

    async def execute(
        self,
        command: str,
        file_path: str = None,
        platform: str = None,
        location: str = None,
        database: str = None,
        format_type: str = None,
    ):
        """Main command execution router"""
        try:
            if command == "publish":
                await self.cmd_publish(file_path, platform, location, database, format_type)
            else:
                self.print_error(f"Unknown command: {command}")
                self.print_info("Available commands: publish")

        except KeyboardInterrupt:
            self.print_info("\nOperation cancelled by user")
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")

    async def cmd_publish(
        self, file_path: str, platform: str, location: str, database: str, format_type: str
    ):
        """Publish file to specified platform"""
        try:
            # Validate inputs
            if not file_path:
                self.print_error("File path is required")
                return

            if not os.path.exists(file_path):
                self.print_error(f"File not found: {file_path}")
                return

            if not platform:
                platform = "notion"  # Default platform

            # Validate location or database (mutually exclusive)
            if not location and not database:
                self.print_error(
                    "Either --location (parent ID) or --database (database ID) is required"
                )
                return

            if location and database:
                self.print_error(
                    "Cannot specify both --location and --database. Use one or the other."
                )
                return

            if not format_type:
                format_type = "markdown"  # Default format

            # Initialize publisher
            self.publisher = Publisher()

            # Set database mode if publishing to database
            if database:
                self.publisher.database_mode = True
                location = database  # Use database_id as location for database publishing

            # Publish the file
            if database:
                self.print_info(f"📤 Publishing {file_path} to Notion database...")
            else:
                self.print_info(f"📤 Publishing {file_path} to {platform}...")

            result = await self.publisher.publish(
                file_path=file_path, platform=platform, location=location, format=format_type
            )

            if result["success"]:
                self.print_success(f"✅ Published successfully!")
                self.print_info(f"📄 Page ID: {result.get('page_id', 'unknown')}")
                self.print_info(f"🔗 URL: {result.get('url', 'No URL')}")

                # Show metadata if publishing to database
                if (
                    hasattr(self.publisher, "database_mode")
                    and self.publisher.database_mode
                    and result.get("metadata")
                ):
                    self.print_info("📊 ADR Metadata:")
                    metadata = result["metadata"]
                    self.print_info(f"  - Title: {metadata.get('title', 'Unknown')}")
                    self.print_info(f"  - Number: {metadata.get('number', 'Unknown')}")
                    self.print_info(f"  - Status: {metadata.get('status', 'Unknown')}")
                    self.print_info(f"  - Author: {metadata.get('author', 'Unknown')}")
                    if metadata.get("date"):
                        self.print_info(f"  - Date: {metadata['date']}")

                # Show warnings if any
                if result.get("warnings"):
                    self.print_warning("⚠️ Conversion notes:")
                    for warning in result["warnings"]:
                        self.print_info(f"  - {warning}")
            else:
                self.print_error(f"❌ Publication failed: {result.get('error', 'Unknown error')}")

        except ValueError as e:
            # Display helpful error message for user errors (parent validation, etc.)
            self.print_error(f"❌ {str(e)}")
        except Exception as e:
            self.print_error(f"❌ Unexpected error during publication: {e}")

    def print_success(self, message: str):
        """Print success message with green color"""
        print(f"\033[92m{message}\033[0m")

    def print_error(self, message: str):
        """Print error message with red color"""
        print(f"\033[91m{message}\033[0m")

    def print_info(self, message: str):
        """Print info message with blue color"""
        print(f"\033[94m{message}\033[0m")

    def print_warning(self, message: str):
        """Print warning message with yellow color"""
        print(f"\033[93m{message}\033[0m")


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Publish content to various platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Publish to Notion page
  python cli/commands/publish.py publish README.md --to notion --location parent-id

  # Publish to Notion database (for ADRs)
  python cli/commands/publish.py publish docs/architecture/adr/adr-026.md --to notion --database database-id

  # Publish with custom format
  python cli/commands/publish.py publish docs/guide.md --to notion --location parent-id --format markdown
        """,
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Publish command
    publish_parser = subparsers.add_parser("publish", help="Publish file to specified platform")
    publish_parser.add_argument("file_path", help="Path to the file to publish")
    publish_parser.add_argument(
        "--to", default="notion", help="Publishing platform (default: notion)"
    )
    publish_parser.add_argument("--location", help="Parent location ID (for page publishing)")
    publish_parser.add_argument("--database", help="Database ID (for database publishing)")
    publish_parser.add_argument(
        "--format", default="markdown", help="Content format (default: markdown)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Execute command
    cmd = PublishCommand()
    if args.command == "publish":
        await cmd.execute(
            "publish",
            file_path=args.file_path,
            platform=args.to,
            location=args.location,
            database=args.database,
            format_type=args.format,
        )
    else:
        await cmd.execute(args.command)


if __name__ == "__main__":
    asyncio.run(main())
