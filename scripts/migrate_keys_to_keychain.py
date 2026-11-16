#!/usr/bin/env python3
"""
Migrate API Keys to Keychain

Interactive script to migrate API keys from environment variables
or .env files to secure OS keychain storage.

Usage:
    python scripts/migrate_keys_to_keychain.py

    # Or migrate specific providers
    python scripts/migrate_keys_to_keychain.py --providers openai anthropic

    # Dry run (show what would be migrated)
    python scripts/migrate_keys_to_keychain.py --dry-run
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import structlog

from services.config.llm_config_service import LLMConfigService
from services.infrastructure.keychain_service import KeychainService

logger = structlog.get_logger(__name__)


# ANSI color codes for pretty output
class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    BOLD = "\033[1m"
    END = "\033[0m"


def print_header():
    """Print script header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔═══════════════════════════════════════════════╗")
    print(f"║   Piper Morgan - API Key Migration Tool      ║")
    print(f"║   Migrate keys to secure keychain storage    ║")
    print(f"╚═══════════════════════════════════════════════╝{Colors.END}\n")


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{title}{Colors.END}")
    print("─" * len(title))


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def check_migration_status(config_service: LLMConfigService) -> dict:
    """Get and display current migration status"""
    print_section("Current Status")

    status = config_service.get_migration_status()

    print(f"Total providers: {status['total_providers']}")
    print(f"  In keychain: {Colors.GREEN}{status['in_keychain']}{Colors.END}")
    print(f"  In .env only: {Colors.YELLOW}{status['in_env']}{Colors.END}")
    print(f"  Missing: {Colors.RED}{status['missing']}{Colors.END}")
    print(f"  Need migration: {Colors.YELLOW}{status['needs_migration']}{Colors.END}")

    print_section("Provider Details")
    for provider, entry in status["providers"].items():
        keychain_status = (
            f"{Colors.GREEN}✓{Colors.END}"
            if entry.exists_in_keychain
            else f"{Colors.RED}✗{Colors.END}"
        )
        env_status = (
            f"{Colors.YELLOW}✓{Colors.END}" if entry.exists_in_env else f"{Colors.RED}✗{Colors.END}"
        )

        print(f"  {provider:12} - Keychain: {keychain_status}  Environment: {env_status}")

    return status


def migrate_provider(
    config_service: LLMConfigService, provider: str, dry_run: bool = False
) -> bool:
    """
    Migrate a single provider's key to keychain

    Args:
        config_service: Configuration service
        provider: Provider name
        dry_run: If True, only show what would be done

    Returns:
        True if migration successful (or would be in dry run)
    """
    # Check current status
    env_var = f"{provider.upper()}_API_KEY"
    key = os.getenv(env_var)

    if not key:
        print_error(f"No {provider} key found in environment variable {env_var}")
        return False

    # Check if already in keychain
    keychain_key = config_service._keychain_service.get_api_key(provider)
    if keychain_key:
        if keychain_key == key:
            print_info(f"{provider} key already in keychain (matches environment)")
            return True
        else:
            print_warning(f"{provider} key exists in keychain but differs from environment")
            response = input(f"  Overwrite keychain with environment key? (y/N): ")
            if response.lower() != "y":
                print_info(f"Skipping {provider}")
                return False

    if dry_run:
        print_info(f"[DRY RUN] Would migrate {provider} key to keychain")
        return True

    # Perform migration
    try:
        success = config_service.migrate_key_to_keychain(provider)
        if success:
            print_success(f"Migrated {provider} key to keychain")
            print_info(f"  You can now remove {env_var} from .env file")
            return True
        else:
            print_error(f"Failed to migrate {provider} key")
            return False
    except Exception as e:
        print_error(f"Error migrating {provider}: {e}")
        return False


def confirm_migration(providers_to_migrate: List[str], dry_run: bool) -> bool:
    """Confirm migration with user"""
    if not providers_to_migrate:
        print_info("No providers need migration")
        return False

    print_section("Migration Plan")
    for provider in providers_to_migrate:
        action = "Would migrate" if dry_run else "Will migrate"
        print(f"  • {action} {provider} key to keychain")

    if dry_run:
        print_info("\nThis is a dry run - no changes will be made")
        return True

    print()
    response = input(f"Proceed with migration? (y/N): ")
    return response.lower() == "y"


def print_post_migration_instructions():
    """Print instructions after successful migration"""
    print_section("Next Steps")
    print("1. Verify keys work:")
    print(f"   {Colors.BLUE}python scripts/test_llm_keys.py{Colors.END}")
    print()
    print("2. Remove keys from .env file:")
    print(f"   {Colors.YELLOW}# Edit .env and remove migrated keys{Colors.END}")
    print()
    print("3. Restart Piper to use keychain keys:")
    print(f"   {Colors.BLUE}Stop the running server, then: python main.py{Colors.END}")
    print()
    print_success("Migration complete! Your API keys are now secure.")


def main():
    """Main migration script"""
    parser = argparse.ArgumentParser(description="Migrate API keys from environment to keychain")
    parser.add_argument(
        "--providers", nargs="+", help="Specific providers to migrate (default: all)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be migrated without making changes"
    )
    parser.add_argument("--force", action="store_true", help="Skip confirmation prompts")

    args = parser.parse_args()

    try:
        print_header()

        # Initialize services
        config_service = LLMConfigService()

        # Check current status
        status = check_migration_status(config_service)

        # Determine which providers to migrate
        if args.providers:
            providers_to_migrate = [
                p
                for p in args.providers
                if status["providers"][p].exists_in_env
                and not status["providers"][p].exists_in_keychain
            ]
        else:
            providers_to_migrate = [
                p
                for p, entry in status["providers"].items()
                if entry.exists_in_env and not entry.exists_in_keychain
            ]

        if not providers_to_migrate:
            print()
            print_success("All keys already migrated or no keys found to migrate")
            return 0

        # Confirm migration
        if not args.force:
            if not confirm_migration(providers_to_migrate, args.dry_run):
                print_info("Migration cancelled")
                return 0

        # Perform migration
        print_section("Migrating Keys")
        success_count = 0
        for provider in providers_to_migrate:
            if migrate_provider(config_service, provider, args.dry_run):
                success_count += 1

        # Summary
        print()
        if args.dry_run:
            print_info(
                f"Dry run complete: {success_count}/{len(providers_to_migrate)} keys would be migrated"
            )
        else:
            print_success(f"Successfully migrated {success_count}/{len(providers_to_migrate)} keys")
            if success_count > 0:
                print_post_migration_instructions()

        return 0 if success_count == len(providers_to_migrate) else 1

    except KeyboardInterrupt:
        print()
        print_warning("Migration cancelled by user")
        return 130
    except Exception as e:
        print()
        print_error(f"Migration failed: {e}")
        logger.exception("Migration error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
