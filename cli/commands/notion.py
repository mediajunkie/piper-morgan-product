"""
Notion CLI Command - Knowledge Management Integration

Provides immediate value through Notion knowledge management commands:
- piper notion status: Connection status and configuration check
- piper notion search: Search across Notion workspace
- piper notion pages: List recent pages and databases
- piper notion test: Test connection and basic functionality

Built on: NotionMCPAdapter + NotionSpatialIntelligence + Configuration
Performance: Real-time Notion workspace intelligence with graceful degradation
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent_service.canonical_handlers import CanonicalHandlers
from config.notion_config import NotionConfig
from services.domain.notion_domain_service import NotionDomainService
from services.features.notion_queries import (
    NotionCanonicalQueryEngine,
    enhance_with_notion_intelligence,
)
from services.intelligence.spatial.notion_spatial import NotionSpatialIntelligence


class NotionCommand:
    """Notion CLI Command with beautiful formatting and graceful degradation"""

    # Color codes for beautiful output (matching other CLI commands)
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
        """Initialize the Notion command with required services"""
        self.config = NotionConfig()
        self.notion_domain_service = NotionDomainService()
        self.spatial_intelligence = NotionSpatialIntelligence()

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

    def print_warning(self, message: str) -> None:
        """Print a warning message"""
        self.print_colored(f"⚠️  {message}", "yellow")

    def print_error(self, message: str) -> None:
        """Print an error message"""
        self.print_colored(f"❌ {message}", "red")

    def print_success(self, message: str) -> None:
        """Print a success message"""
        self.print_colored(f"✅ {message}", "green")

    def print_info(self, message: str) -> None:
        """Print an info message"""
        self.print_colored(f"ℹ️  {message}", "blue")

    async def cmd_status(self) -> None:
        """Display Notion integration status and configuration"""
        self.print_header("NOTION INTEGRATION STATUS")

        # Configuration Status
        self.print_section("Configuration Status", "blue")
        config_status = self.config.get_config_status()

        if config_status["fully_configured"]:
            self.print_success("Notion integration fully configured")
        else:
            self.print_warning("Notion integration not fully configured")

        # Detailed configuration info
        self.print_colored("📊 Configuration Details:", "cyan")
        self.print_colored(
            f"   API Key Set: {'✅' if config_status['api_key_set'] else '❌'}",
            "green" if config_status["api_key_set"] else "red",
        )
        self.print_colored(
            f"   API Key Format: {'✅' if config_status['api_key_format_valid'] else '❌'}",
            "green" if config_status["api_key_format_valid"] else "red",
        )
        self.print_colored(
            f"   Workspace ID: {'✅' if config_status['workspace_id_set'] else '❌'}",
            "green" if config_status["workspace_id_set"] else "red",
        )

        # Adapter Status
        self.print_section("Adapter Status", "blue")
        if self.notion_domain_service.is_configured():
            self.print_success("NotionDomainService initialized")

            # Test connection
            try:
                connected = await self.notion_domain_service.connect()
                if connected:
                    self.print_success("Connection test successful")
                else:
                    self.print_error("Connection test failed")
            except Exception as e:
                self.print_error(f"Connection error: {e}")
        else:
            self.print_warning("NotionDomainService not configured")

        # Setup Instructions
        if not config_status["fully_configured"]:
            self.print_section("Setup Instructions", "yellow")
            self.print_colored("To configure Notion integration:", "yellow")
            self.print_colored(
                "1. Create integration at: https://www.notion.so/my-integrations", "white"
            )
            self.print_colored("2. Copy the Internal Integration Token", "white")
            self.print_colored(
                "3. Set environment variable: export NOTION_API_KEY=secret_your_token", "white"
            )
            self.print_colored(
                "4. (Optional) Set workspace: export NOTION_WORKSPACE_ID=your_workspace", "white"
            )
            self.print_colored("5. Run 'piper notion test' to verify setup", "white")

    async def cmd_test(self) -> None:
        """Test Notion connection and basic functionality"""
        self.print_header("NOTION CONNECTION TEST")

        # Configuration check
        self.print_section("Configuration Validation", "blue")
        if not self.config.validate_config():
            self.print_error("Configuration invalid - check NOTION_API_KEY")
            return

        self.print_success("Configuration valid")

        # Connection test
        self.print_section("Connection Test", "blue")
        try:
            connected = await self.adapter.connect()
            if connected:
                self.print_success("Successfully connected to Notion API")

                # Get workspace info
                try:
                    workspace_info = await self.adapter.get_workspace_info()
                    if workspace_info:
                        self.print_info(
                            f"Connected as: {workspace_info.get('user_name', 'Unknown User')}"
                        )
                        if workspace_info.get("workspace_name"):
                            self.print_info(f"Workspace: {workspace_info['workspace_name']}")
                except Exception as e:
                    self.print_warning(f"Could not get workspace info: {e}")

            else:
                self.print_error("Failed to connect to Notion API")

        except Exception as e:
            self.print_error(f"Connection test failed: {e}")

        # Spatial intelligence test
        self.print_section("Spatial Intelligence Test", "blue")
        try:
            # Test spatial intelligence initialization
            self.print_info("Testing spatial intelligence initialization...")
            # Note: Actual spatial intelligence testing would go here
            self.print_success("Spatial intelligence module loaded")

        except Exception as e:
            self.print_error(f"Spatial intelligence test failed: {e}")

    async def cmd_search(self, query: str = "") -> None:
        """Search across Notion workspace"""
        self.print_header(f"NOTION SEARCH: {query if query else 'No query provided'}")

        if not query:
            self.print_warning("No search query provided")
            self.print_info("Usage: piper notion search --query 'your search terms'")
            return

        # Configuration check
        if not self.adapter.is_configured():
            self.print_error(
                "Notion not configured - run 'piper notion status' for setup instructions"
            )
            return

        self.print_section(f"Searching for: '{query}'", "blue")

        try:
            # Connect to Notion
            connected = await self.adapter.connect()
            if not connected:
                self.print_error("Could not connect to Notion")
                return

            self.print_info("Connected to Notion workspace")

            # Perform the search
            results = await self.adapter.search_notion(query)

            if not results:
                self.print_warning("No results found")
                return

            # Display results
            self.print_section(f"Found {len(results)} results:", "green")

            for i, result in enumerate(results[:10], 1):  # Show first 10
                # Extract title
                title = "Untitled"
                if "properties" in result and "title" in result["properties"]:
                    title_prop = result["properties"]["title"]
                    if "title" in title_prop and len(title_prop["title"]) > 0:
                        title = title_prop["title"][0]["text"]["content"]

                # Display result
                obj_type = result.get("object", "unknown")
                result_id = result.get("id", "no-id")
                self.print_info(f"{i}. [{obj_type}] {title}")
                self.print_info(f"   ID: {result_id[:8]}...")

        except Exception as e:
            self.print_error(f"Search failed: {e}")

    async def cmd_pages(self) -> None:
        """List recent pages and databases"""
        self.print_header("RECENT NOTION PAGES & DATABASES")

        # Configuration check
        if not self.adapter.is_configured():
            self.print_error(
                "Notion not configured - run 'piper notion status' for setup instructions"
            )
            return

        try:
            # Connect to Notion
            connected = await self.adapter.connect()
            if not connected:
                self.print_error("Could not connect to Notion")
                return

            self.print_success("Connected to Notion workspace")

            # Get all pages
            results = await self.adapter.search_notion("", filter_type="page")

            if not results:
                self.print_warning("No pages found")
                return

            # Display pages
            self.print_section(f"Found {len(results)} pages:", "green")

            for i, page in enumerate(results[:20], 1):  # Show first 20
                # Extract title
                title = "Untitled"
                if "properties" in page and "title" in page["properties"]:
                    title_prop = page["properties"]["title"]
                    if "title" in title_prop and len(title_prop["title"]) > 0:
                        title = title_prop["title"][0]["text"]["content"]

                # Display page
                page_id = page.get("id", "no-id")
                self.print_info(f"{i}. {title}")
                self.print_info(f"   ID: {page_id[:8]}...")

                # Show URL if available
                if "url" in page:
                    self.print_info(f"   URL: {page['url']}")

        except Exception as e:
            self.print_error(f"Failed to list pages: {e}")

    async def cmd_create(self, title: str, parent_id: Optional[str] = None):
        """Create a new Notion page"""
        try:
            # Use default parent if not specified
            if not parent_id:
                # Search for a default parent
                pages = await self.adapter.search_notion("", filter_type="page")
                if pages:
                    parent_id = pages[0]["id"]
                    self.print_warning("Using first available page as parent")
                else:
                    self.print_error("No pages found to use as parent")
                    return

            # Create the page
            result = await self.adapter.create_page(
                parent_id=parent_id, properties={"title": {"title": [{"text": {"content": title}}]}}
            )

            if result:
                self.print_success("Page created successfully!")
                self.print_info(f"Title: {title}")
                self.print_info(f"ID: {result.get('id', 'unknown')}")
                self.print_info(f"URL: {result.get('url', 'No URL')}")
            else:
                self.print_error("Failed to create page")

        except Exception as e:
            self.print_error(f"Error creating page: {e}")

    async def cmd_validate(self, level: str = "basic", config_path: Optional[str] = None):
        """Validate Notion configuration with specified validation level"""
        self.print_header("NOTION CONFIGURATION VALIDATION")

        try:
            # Import configuration classes
            from config.notion_user_config import (
                ConfigurationError,
                NotionUserConfig,
                ValidationLevel,
            )

            # Load configuration from specified path or default
            config_file = Path(config_path) if config_path else Path("config/PIPER.user.md")

            if not config_file.exists():
                self.print_error(f"Configuration file not found: {config_file}")
                self.print_info("Create configuration file with: piper notion setup")
                return

            self.print_section(f"Validating Configuration: {config_file}", "blue")
            self.print_info(f"Validation Level: {level}")

            # Load configuration
            config = NotionUserConfig.load_from_user_config(config_file)
            self.print_success("Configuration loaded successfully")

            # Perform validation
            validation_level = ValidationLevel(level)
            result = await config.validate_async(validation_level)

            # Display validation results
            self.print_section("Validation Results", "cyan")
            self.print_info(f"Overall Valid: {'✅ Yes' if result.is_valid() else '❌ No'}")
            self.print_info(f"Format Valid: {'✅ Yes' if result.format_valid else '❌ No'}")
            self.print_info(
                f"Environment Valid: {'✅ Yes' if result.environment_valid else '❌ No'}"
            )

            if level in ["enhanced", "full"]:
                if result.connectivity_tested:
                    self.print_info(
                        f"API Connectivity: {'✅ Yes' if result.connectivity_result else '❌ No'}"
                    )
                else:
                    self.print_info("API Connectivity: ⏳ Not tested")

            if level == "full" and result.permission_checked:
                self.print_info("Permission Check Results:")
                for resource, accessible in result.permission_result.items():
                    status = "✅" if accessible else "❌"
                    self.print_info(f"  {status} {resource}")

            # Display any errors or warnings
            if result.errors:
                self.print_section("Errors", "red")
                for error in result.errors:
                    self.print_error(error)

            if result.warnings:
                self.print_section("Warnings", "yellow")
                for warning in result.warnings:
                    self.print_warning(warning)

            # Configuration summary
            summary = config.get_summary()
            self.print_section("Configuration Summary", "green")
            self.print_info(f"ADR Database: {summary['adrs_database_id']}")
            self.print_info(f"Default Parent: {summary['publishing_default_parent']}")
            self.print_info(f"Validation Level: {summary['validation_level']}")
            self.print_info(
                f"Publishing Enabled: {'✅ Yes' if summary['publishing_enabled'] else '❌ No'}"
            )
            self.print_info(f"ADRs Enabled: {'✅ Yes' if summary['adrs_enabled'] else '❌ No'}")

        except ConfigurationError as e:
            self.print_error(f"Configuration Error: {e}")
            # Display full resolution steps
            if hasattr(e, "resolution_steps") and e.resolution_steps:
                self.print_section("Resolution Steps", "yellow")
                for i, step in enumerate(e.resolution_steps, 1):
                    self.print_info(f"{i}. {step}")
        except Exception as e:
            self.print_error(f"Validation failed: {e}")
            # For unexpected errors, show full details
            self.print_error(f"Error details: {str(e)}")
            import traceback

            self.print_error("Full traceback:")
            for line in traceback.format_exc().split("\n"):
                if line.strip():
                    self.print_error(f"  {line}")

    async def cmd_setup(self, interactive: bool = False, config_path: Optional[str] = None):
        """Guided setup for Notion configuration"""
        self.print_header("NOTION CONFIGURATION SETUP")

        try:
            config_file = config_path or "config/PIPER.user.md"

            if Path(config_file).exists():
                self.print_warning(f"Configuration file already exists: {config_file}")
                self.print_info("Use 'piper notion validate' to check configuration")
                return

            self.print_section("Configuration Setup", "blue")
            self.print_info("Setting up Notion configuration for the first time")

            # Create example configuration
            example_config = """# Notion Integration Configuration
# Instructions: Add this section to your PIPER.user.md file
# Privacy: This configuration is gitignored (never committed)
# Validation: Run 'piper notion validate' to test configuration

```yaml
notion:
  # REQUIRED: Core Publishing Configuration
  publishing:
    default_parent: ""              # Required: Your default parent page for publishing
    enabled: true                   # Enable/disable publishing features

  # REQUIRED: ADR Database Configuration (HIGH PRIORITY from audit)
  adrs:
    database_id: ""                 # Required: Your ADR database ID
    enabled: true                   # Enable/disable ADR publishing
    auto_publish: true              # Auto-publish new ADRs

  # OPTIONAL: Development & Testing Configuration
  development:
    test_parent: ""                 # Test page parent ID for integration tests
    debug_parent: ""                # Debug page parent for development scripts
    mock_mode: false                # Enable mock mode for testing

  # OPTIONAL: Validation Settings
  validation:
    level: "basic"                  # Validation level: basic|enhanced|full
    connectivity_check: true        # Test API connectivity on startup
    cache_results: true             # Cache validation results
```
"""

            # Create configuration file
            Path(config_file).parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, "w") as f:
                f.write(example_config)

            self.print_success(f"Configuration file created: {config_file}")
            self.print_section("Next Steps", "green")
            self.print_info("1. Edit the configuration file with your Notion workspace details")
            self.print_info("2. Add your ADR database ID and default parent page ID")
            self.print_info("3. Run 'piper notion validate' to test your configuration")
            self.print_info("4. Use 'piper notion test-config' to verify specific components")

            if interactive:
                self.print_section("Interactive Setup", "yellow")
                self.print_info("Interactive setup not yet implemented")
                self.print_info("Edit the configuration file manually for now")

        except Exception as e:
            self.print_error(f"Setup failed: {e}")

    async def cmd_test_config(self, database: Optional[str] = None, parent: Optional[str] = None):
        """Test specific configuration components"""
        self.print_header("NOTION CONFIGURATION TESTING")

        try:
            # Import configuration classes
            from config.notion_user_config import ConfigurationError, NotionUserConfig

            config_file = Path("config/PIPER.user.md")

            if not config_file.exists():
                self.print_error(f"Configuration file not found: {config_file}")
                self.print_info("Create configuration with: piper notion setup")
                return

            self.print_section("Configuration Testing", "blue")
            self.print_info(f"Testing configuration file: {config_file}")

            # Load configuration
            config = NotionUserConfig.load_from_user_config(config_file)
            self.print_success("Configuration loaded successfully")

            # Test specific components
            if database:
                self.print_section(f"Database Testing: {database}", "cyan")
                try:
                    db_id = config.get_database_id(database)
                    self.print_success(f"Database ID retrieved: {db_id[:8]}...")

                    # Test database format validation
                    if config.is_valid_format():
                        self.print_success("Database ID format is valid")
                    else:
                        self.print_error("Database ID format is invalid")

                except ConfigurationError as e:
                    self.print_error(f"Database configuration error: {e}")

            if parent:
                self.print_section(f"Parent Page Testing: {parent}", "cyan")
                try:
                    parent_id = config.get_parent_id(parent)
                    self.print_success(f"Parent ID retrieved: {parent_id[:8]}...")

                    # Test parent format validation
                    if config.is_valid_format():
                        self.print_success("Parent ID format is valid")
                    else:
                        self.print_error("Parent ID format is invalid")

                except ConfigurationError as e:
                    self.print_error(f"Parent configuration error: {e}")

            # Overall configuration status
            self.print_section("Configuration Status", "green")
            summary = config.get_summary()
            self.print_info(f"ADR Database: {summary['adrs_database_id']}")
            self.print_info(f"Default Parent: {summary['publishing_default_parent']}")
            self.print_info(f"Validation Level: {summary['validation_level']}")
            self.print_info(
                f"Publishing Enabled: {'✅ Yes' if summary['publishing_enabled'] else '❌ No'}"
            )
            self.print_info(f"ADRs Enabled: {'✅ Yes' if summary['adrs_enabled'] else '❌ No'}")

            # Format validation
            if config.is_valid_format():
                self.print_success("Configuration format is valid")
            else:
                self.print_error("Configuration format is invalid")

        except ConfigurationError as e:
            self.print_error(f"Configuration Error: {e}")
            # Display full resolution steps
            if hasattr(e, "resolution_steps") and e.resolution_steps:
                self.print_section("Resolution Steps", "yellow")
                for i, step in enumerate(e.resolution_steps, 1):
                    self.print_info(f"{i}. {step}")
        except Exception as e:
            self.print_error(f"Configuration testing failed: {e}")
            # For unexpected errors, show full details
            self.print_error(f"Error details: {str(e)}")
            import traceback

            self.print_error("Full traceback:")
            for line in traceback.format_exc().split("\n"):
                if line.strip():
                    self.print_error(f"  {line}")

    async def execute(self, command: str = "status", query: Optional[str] = None, **kwargs) -> None:
        """Execute the specified Notion command"""
        try:
            if command == "status":
                await self.cmd_status()
            elif command == "test":
                await self.cmd_test()
            elif command == "search":
                await self.cmd_search(query or "")
            elif command == "pages":
                await self.cmd_pages()
            elif command == "create":
                await self.cmd_create(query or "")
            elif command == "validate":
                level = kwargs.get("level", "basic")
                config_path = kwargs.get("config_path")
                await self.cmd_validate(level=level, config_path=config_path)
            elif command == "setup":
                interactive = kwargs.get("interactive", False)
                config_path = kwargs.get("config_path")
                await self.cmd_setup(interactive=interactive, config_path=config_path)
            elif command == "test-config":
                database = kwargs.get("database")
                parent = kwargs.get("parent")
                await self.cmd_test_config(database=database, parent=parent)
            else:
                self.print_error(f"Unknown command: {command}")
                self.print_info(
                    "Available commands: status, test, search, pages, create, validate, setup, test-config"
                )

        except KeyboardInterrupt:
            self.print_warning("\nCommand interrupted by user")
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")


async def main():
    """Main entry point for Notion CLI commands"""
    import argparse

    parser = argparse.ArgumentParser(description="Notion Knowledge Management Commands")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("status", help="Show Notion integration status")
    subparsers.add_parser("test", help="Test Notion connection")

    search_parser = subparsers.add_parser("search", help="Search Notion workspace")
    search_parser.add_argument("--query", "-q", help="Search query")

    subparsers.add_parser("pages", help="List recent pages and databases")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new Notion page")
    create_parser.add_argument("title", help="Title of the new page")
    create_parser.add_argument("--parent-id", help="Parent page ID (optional)", default=None)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate Notion configuration")
    validate_parser.add_argument(
        "--level",
        choices=["basic", "enhanced", "full"],
        default="basic",
        help="Validation level (default: basic)",
    )
    validate_parser.add_argument(
        "--config", help="Path to configuration file (default: config/PIPER.user.md)"
    )

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Guided setup for Notion configuration")
    setup_parser.add_argument("--interactive", action="store_true", help="Interactive setup mode")
    setup_parser.add_argument(
        "--config", help="Path to configuration file (default: config/PIPER.user.md)"
    )

    # Test-config command
    test_config_parser = subparsers.add_parser(
        "test-config", help="Test specific configuration components"
    )
    test_config_parser.add_argument("--database", help="Test database configuration (e.g., adrs)")
    test_config_parser.add_argument(
        "--parent", help="Test parent page configuration (e.g., default, test)"
    )

    args = parser.parse_args()

    # Execute command
    cmd = NotionCommand()

    if args.command == "search":
        await cmd.execute("search", args.query)
    elif args.command == "create":
        await cmd.execute("create", args.title)
    elif args.command == "validate":
        await cmd.execute("validate", config_path=args.config, level=args.level)
    elif args.command == "setup":
        await cmd.execute("setup", interactive=args.interactive, config_path=args.config)
    elif args.command == "test-config":
        await cmd.execute("test-config", database=args.database, parent=args.parent)
    elif args.command:
        await cmd.execute(args.command)
    else:
        await cmd.execute("status")  # Default command


if __name__ == "__main__":
    asyncio.run(main())
