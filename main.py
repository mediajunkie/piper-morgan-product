#!/usr/bin/env python3
"""
Piper Morgan - Main Entry Point

This is the proper way to start Piper Morgan.
It initializes services via ServiceContainer and starts the web server.
"""

# Load environment variables from .env file FIRST (before any other imports)
from dotenv import load_dotenv

load_dotenv()

import argparse
import asyncio
import logging
import os
import sys
import webbrowser

# Parse arguments early to set logging level
parser = argparse.ArgumentParser(description="Piper Morgan - AI Assistant")
parser.add_argument(
    "--verbose", "-v", action="store_true", help="Show detailed startup information"
)
parser.add_argument(
    "--no-browser",
    action="store_true",
    help="Don't auto-launch browser on startup (Issue #461: on by default)",
)
parser.add_argument(
    "command",
    nargs="?",
    help="Command to run (setup, status, preferences, migrate-user, keys, rotate-key)",
)
parser.add_argument(
    "provider",
    nargs="?",
    help="Provider for rotate-key command (openai, anthropic, github)",
)

# Parse known args to handle both flags and commands
args, unknown = parser.parse_known_args()

# Setup logging based on verbosity (Issue #254 CORE-UX-QUIET)
if args.verbose:
    # Verbose mode - show all details
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
else:
    # Quiet mode (default) - minimal output
    logging.basicConfig(level=logging.WARNING, format="%(message)s")

# SECURITY: Install URL parameter redaction filter to prevent API key leaks in logs
# See: 2026-01-17 security incident (Gemini API key leaked via httpx INFO logs)
from services.infrastructure.logging.url_redaction import (
    install_root_redaction_filter,
    install_url_redaction_filter,
)

# Install on HTTP client loggers (httpx, httpcore, urllib3, etc.)
install_url_redaction_filter()
# Also install on root logger for comprehensive coverage
install_root_redaction_filter()

logger = logging.getLogger(__name__)

# Consciousness-enhanced CLI messages (Issue #633)
from services.consciousness.cli_consciousness import (
    format_cli_error_conscious,
    format_cli_success_conscious,
    format_ready_conscious,
    format_services_ready_conscious,
    format_shutdown_conscious,
    format_startup_conscious,
)


def should_open_browser() -> bool:
    """Check if browser should be opened (Issue #461: on by default)"""
    # Don't open if explicitly disabled with --no-browser flag
    if args.no_browser:
        return False

    # Don't open if no display (CI/CD, SSH)
    if not os.environ.get("DISPLAY") and sys.platform != "darwin":
        return False

    # Don't open for commands (setup, status, etc.)
    if args.command:
        return False

    return True


async def open_browser_delayed():
    """Open browser after verifying server is ready via health endpoint.

    Issue #645: Fixed race condition where browser opened before server ready.
    Now polls /health endpoint instead of using fixed 2-second delay.
    """
    import aiohttp

    max_attempts = 30  # 30 seconds max wait
    health_url = "http://localhost:8001/health"

    for attempt in range(max_attempts):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(health_url, timeout=aiohttp.ClientTimeout(total=1)) as resp:
                    if resp.status == 200:
                        webbrowser.open("http://localhost:8001")
                        if args.verbose:
                            logger.info(f"Browser opened after {attempt + 1} health check(s)")
                        else:
                            print("   🌐 Browser opened")
                        return
        except Exception:
            pass  # Server not ready yet, retry
        await asyncio.sleep(1)

    # Fallback: open browser anyway after timeout (better than nothing)
    if args.verbose:
        logger.warning(
            f"Server health check timed out after {max_attempts}s, opening browser anyway"
        )
    else:
        print("   ⚠️ Server slow to start, opening browser anyway")
    webbrowser.open("http://localhost:8001")


async def main():
    """Main entry point."""
    try:
        # Human-readable startup messages (Issue #254 CORE-UX-QUIET)
        if args.verbose:
            logger.info("Starting Piper Morgan...")
        else:
            print(format_startup_conscious())

        # Initialize service container
        from services.container import ServiceContainer

        container = ServiceContainer()

        if args.verbose:
            logger.info("Initializing services...")
        else:
            print("   ⏳ Initializing services...")

        await container.initialize()

        if args.verbose:
            logger.info(f"Services initialized: {container.list_services()}")
        else:
            services = container.list_services()
            print(f"   {format_services_ready_conscious(len(services))}")

        # Start web server
        import uvicorn

        if args.verbose:
            logger.info("Starting web server on http://127.0.0.1:8001")
        else:
            # G50: Clear Server Startup Message with all necessary URLs
            # Issue #633: Consciousness-enhanced messaging
            print("\n" + "=" * 60)
            print(format_ready_conscious("http://localhost:8001"))
            print("=" * 60)
            print("\n   Web Interface:     http://localhost:8001")
            print("   API Documentation: http://localhost:8001/docs")
            print("   Health Check:      http://localhost:8001/health")
            print("\nPress Ctrl+C to stop the server")
            print("=" * 60 + "\n")

        # Auto-launch browser by default unless --no-browser flag specified (Issue #461)
        if should_open_browser():
            asyncio.create_task(open_browser_delayed())
            if not args.verbose:
                print("   ⏳ Browser will open when server is ready...")

        # Issue #720: Race condition - "Ready" message printed before server binds socket
        # Solution: Use log_level="info" to show uvicorn's startup message, which only
        # appears AFTER the socket is bound. Users should wait for that message.
        # The open_browser_delayed() already polls /health before opening browser.
        if not args.verbose:
            print("\n   Note: Wait for 'Application startup complete' before navigating manually")

        config = uvicorn.Config(
            "web.app:app",
            host="127.0.0.1",
            port=8001,
            reload=False,  # Disable reload (incompatible with initialized services)
            # Issue #720: Always show INFO level to display "Application startup complete"
            # This message only appears after socket is bound, signaling true readiness
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()

    except KeyboardInterrupt:
        if args.verbose:
            logger.info("Shutting down gracefully...")
        else:
            print(f"\n{format_shutdown_conscious()}")
        container = ServiceContainer()
        container.shutdown()
    except Exception as e:
        if args.verbose:
            logger.error(f"Startup failed: {e}", exc_info=True)
        else:
            print(format_cli_error_conscious(str(e)))
        sys.exit(1)


if __name__ == "__main__":
    # Check for CLI commands (Issue #218 CORE-USERS-ONBOARD)
    if args.command:
        command = args.command

        if command == "setup":
            # Run interactive setup wizard
            from scripts.setup_wizard import run_setup_wizard

            success = asyncio.run(run_setup_wizard())
            sys.exit(0 if success else 1)

        elif command == "status":
            # Run system health check
            from scripts.status_checker import run_status_check

            asyncio.run(run_status_check())
            sys.exit(0)

        elif command == "preferences":
            # Run preference questionnaire (Issue #267 CORE-PREF-QUEST)
            from scripts.preferences_questionnaire import main as run_preferences

            success = asyncio.run(run_preferences())
            sys.exit(0 if success else 1)

        elif command == "keys":
            # Lightweight key management CLI (keychain-first)
            # Usage:
            #   python main.py keys add <provider>
            #   python main.py keys list
            #   python main.py keys validate [provider]
            from getpass import getpass

            from services.config.llm_config_service import LLMConfigService
            from services.infrastructure.keychain_service import KeychainService

            # Main parser consumes second positional as "provider", so for "keys add anthropic"
            # we get args.provider="add" and unknown=["anthropic"]. Rebuild subargs for keys.
            subargs = ([args.provider] + list(unknown)) if args.provider else list(unknown)

            def print_keys_help():
                print("Usage:")
                print("  python main.py keys add <provider>")
                print("  python main.py keys list")
                print("  python main.py keys validate [provider]")
                print()
                print("Providers: openai, anthropic, gemini, perplexity")

            if not subargs:
                print_keys_help()
                sys.exit(1)

            action = subargs[0]
            keychain = KeychainService()
            llm_config = LLMConfigService()

            if action == "add":
                if len(subargs) < 2:
                    print("Error: provider required\n")
                    print_keys_help()
                    sys.exit(1)
                provider = subargs[1].lower()
                secret = getpass(f"Enter {provider} API key: ")
                if not secret:
                    print("No key entered. Aborting.")
                    sys.exit(1)
                # Store in OS keychain (global scope)
                try:
                    keychain.store_api_key(provider, secret)
                    print(
                        format_cli_success_conscious(
                            "stored", f"your {provider} key in the OS keychain"
                        )
                    )
                except Exception as e:
                    print(f"❌ Failed to store key: {e}")
                    sys.exit(1)
                # Optional validation
                try:
                    valid = asyncio.run(llm_config.validate_api_key(provider, secret))
                    if valid:
                        print(f"✓ {provider} key validated successfully")
                    else:
                        print(
                            f"⚠ Validation failed for {provider}. Key saved; re-check provider/limits."
                        )
                except Exception as e:
                    print(f"⚠ Validation error: {e}")
                sys.exit(0)

            elif action == "list":
                configured = llm_config.get_configured_providers()
                if not configured:
                    print("No providers configured.")
                else:
                    print("Configured providers:")
                    for p in configured:
                        print(f"  - {p}")
                sys.exit(0)

            elif action == "validate":
                # Validate one or all configured providers
                if len(subargs) >= 2:
                    provider = subargs[1].lower()
                    try:
                        result = asyncio.run(llm_config.validate_provider(provider))
                        if result.is_valid:
                            print(f"✓ {provider}: valid")
                            sys.exit(0)
                        else:
                            print(f"❌ {provider}: {result.error_message}")
                            sys.exit(2)
                    except Exception as e:
                        print(f"❌ Validation error for {provider}: {e}")
                        sys.exit(2)
                else:
                    try:
                        results = asyncio.run(llm_config.validate_all_providers())
                        if not results:
                            print("No providers configured.")
                            sys.exit(1)
                        exit_code = 0
                        for provider, res in results.items():
                            if res.is_valid:
                                print(f"✓ {provider}: valid")
                            else:
                                print(f"❌ {provider}: {res.error_message}")
                                exit_code = 2
                        sys.exit(exit_code)
                    except Exception as e:
                        print(f"❌ Validation error: {e}")
                        sys.exit(2)
            else:
                print_keys_help()
                sys.exit(1)

        elif command == "rotate-key":
            # Interactive key rotation workflow (Issue #270 CORE-KEYS-ROTATION-WORKFLOW)
            from cli.commands.keys import rotate_key_interactive

            if not args.provider:
                print("Error: provider required\n")
                print("Usage: python main.py rotate-key <provider>")
                print()
                print("Providers: openai, anthropic, github")
                sys.exit(1)

            provider = args.provider.lower()
            success = asyncio.run(rotate_key_interactive(provider))
            sys.exit(0 if success else 1)

        else:
            print(f"Unknown command: {command}")
            print()
            print("Available commands:")
            print("  python main.py setup              - Interactive setup wizard")
            print("  python main.py status             - Check system health")
            print("  python main.py preferences        - Configure user preferences")
            print("  python main.py keys               - Manage API keys (keychain)")
            print(
                "  python main.py rotate-key <prov>  - Rotate API key (openai, anthropic, github)"
            )
            print("  python main.py migrate-user       - Migrate alpha user to production")
            print("  python main.py [--verbose]        - Start Piper Morgan")
            print()
            print("Options:")
            print("  --verbose, -v               - Show detailed startup information")
            print("  --no-browser                - Don't auto-launch browser (on by default)")
            sys.exit(1)

    # Check for pending database migrations (Issue #605: prevent cryptic errors)
    from services.infrastructure.migration_checker import check_pending_migrations

    pending = asyncio.run(check_pending_migrations())
    if pending:
        print("\n" + "=" * 60)
        print("⚠️  Database migrations pending!")
        print("=" * 60)
        print(f"\nYou have {len(pending)} pending migration(s):")
        for migration in pending[:5]:  # Show first 5
            print(f"  • {migration}")
        if len(pending) > 5:
            print(f"  ... and {len(pending) - 5} more")
        print("\nRun this command to apply migrations:")
        print("  python -m alembic upgrade head")
        print("\nThen restart the server.\n")
        sys.exit(1)

    # Check if setup is complete before starting normally
    from scripts.setup_wizard import is_setup_complete

    setup_complete = asyncio.run(is_setup_complete())

    if not setup_complete:
        print("\n" + "=" * 60)
        print("🚀 Welcome to Piper Morgan!")
        print("=" * 60)
        print("\nFirst-time setup required.")
        print("The server will start and you'll complete setup in your browser.")
        print("\n👉 Visit: http://localhost:8001/setup")
        print("=" * 60 + "\n")

    # Normal startup (start server regardless of setup status)
    # The web UI will redirect to /setup if needed
    asyncio.run(main())
