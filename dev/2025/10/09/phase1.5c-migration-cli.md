# Phase 1.5 Sub-Phase C: Migration CLI Tools

**Issue**: #217 - CORE-LLM-CONFIG
**Phase**: 1.5C of 4 - Migration Tooling
**Agent**: Code Agent
**Date**: October 9, 2025, 9:15 PM
**Time Estimate**: 45-60 minutes
**Priority**: HIGH - User experience for migration

---

## Mission

Create user-friendly CLI tools for migrating API keys from plaintext environment variables to encrypted OS keychain storage.

---

## Context from Sub-Phases A & B

**✅ Sub-Phase A**: KeychainService created and tested
**✅ Sub-Phase B**: LLMConfigService integrated with keychain-first fallback

**Now**: Create CLI tools so users (including PM) can easily migrate their keys.

---

## Sub-Phase C Tasks

### Task 1: Create Migration CLI Script (30 min)

**File**: `scripts/migrate_keys_to_keychain.py` (NEW)

**Purpose**: Interactive CLI for migrating API keys from .env to keychain

**Implementation**:
```python
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

import sys
import os
from pathlib import Path
from typing import List, Optional
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.config.llm_config_service import LLMConfigService
from services.infrastructure.keychain_service import KeychainService
import structlog

logger = structlog.get_logger(__name__)

# ANSI color codes for pretty output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

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
    for provider, entry in status['providers'].items():
        keychain_status = f"{Colors.GREEN}✓{Colors.END}" if entry.exists_in_keychain else f"{Colors.RED}✗{Colors.END}"
        env_status = f"{Colors.YELLOW}✓{Colors.END}" if entry.exists_in_env else f"{Colors.RED}✗{Colors.END}"

        print(f"  {provider:12} - Keychain: {keychain_status}  Environment: {env_status}")

    return status

def migrate_provider(
    config_service: LLMConfigService,
    provider: str,
    dry_run: bool = False
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
            if response.lower() != 'y':
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
    return response.lower() == 'y'

def print_post_migration_instructions():
    """Print instructions after successful migration"""
    print_section("Next Steps")
    print("1. Verify keys work:")
    print(f"   {Colors.BLUE}python -m scripts.test_llm_keys{Colors.END}")
    print()
    print("2. Remove keys from .env file:")
    print(f"   {Colors.YELLOW}# Edit .env and remove migrated keys{Colors.END}")
    print()
    print("3. Restart Piper to use keychain keys:")
    print(f"   {Colors.BLUE}./stop.sh && ./start.sh{Colors.END}")
    print()
    print_success("Migration complete! Your API keys are now secure.")

def main():
    """Main migration script"""
    parser = argparse.ArgumentParser(
        description="Migrate API keys from environment to keychain"
    )
    parser.add_argument(
        '--providers',
        nargs='+',
        help='Specific providers to migrate (default: all)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be migrated without making changes'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompts'
    )

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
                p for p in args.providers
                if status['providers'][p].exists_in_env and not status['providers'][p].exists_in_keychain
            ]
        else:
            providers_to_migrate = [
                p for p, entry in status['providers'].items()
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
            print_info(f"Dry run complete: {success_count}/{len(providers_to_migrate)} keys would be migrated")
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
```

**Acceptance Criteria**:
- [ ] File created at scripts/migrate_keys_to_keychain.py
- [ ] Interactive CLI with colored output
- [ ] Shows migration status
- [ ] Confirms before migrating
- [ ] Handles errors gracefully
- [ ] Provides post-migration instructions
- [ ] Supports --dry-run flag
- [ ] Supports --providers filter
- [ ] Supports --force flag

---

### Task 2: Create Key Testing Script (15 min)

**File**: `scripts/test_llm_keys.py` (NEW)

**Purpose**: Test that API keys work after migration

**Implementation**:
```python
#!/usr/bin/env python3
"""
Test LLM API Keys

Validates that API keys are accessible and work with actual provider APIs.

Usage:
    python scripts/test_llm_keys.py

    # Test specific providers
    python scripts/test_llm_keys.py --providers openai anthropic
"""

import sys
import asyncio
from pathlib import Path
from typing import List
import argparse

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from services.config.llm_config_service import LLMConfigService

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

def print_header():
    """Print script header"""
    print(f"\n{BOLD}{BLUE}╔═══════════════════════════════════════════════╗")
    print(f"║   Piper Morgan - API Key Validator           ║")
    print(f"║   Test keys from keychain and environment    ║")
    print(f"╚═══════════════════════════════════════════════╝{END}\n")

async def test_keys(providers: List[str] = None):
    """Test API keys for all or specific providers"""
    print_header()

    config_service = LLMConfigService()

    # Get providers to test
    if providers:
        test_providers = providers
    else:
        test_providers = ["openai", "anthropic", "gemini", "perplexity"]

    print(f"{BOLD}Testing API Keys{END}")
    print("─" * 40)

    results = await config_service.validate_all_providers()

    success_count = 0
    for provider in test_providers:
        if provider in results:
            result = results[provider]

            # Show where key came from
            key = config_service.get_api_key(provider)
            source = "keychain" if config_service._keychain_service.get_api_key(provider) else "environment"

            if result.is_valid:
                print(f"{GREEN}✓{END} {provider:12} - Valid (from {source})")
                success_count += 1
            else:
                print(f"{RED}✗{END} {provider:12} - {result.error_message}")
        else:
            print(f"{YELLOW}⚠{END} {provider:12} - Not configured")

    print()
    print(f"Results: {GREEN}{success_count}{END}/{len(test_providers)} providers valid")

    return success_count == len(test_providers)

def main():
    """Main test script"""
    parser = argparse.ArgumentParser(
        description="Test LLM API keys"
    )
    parser.add_argument(
        '--providers',
        nargs='+',
        help='Specific providers to test (default: all)'
    )

    args = parser.parse_args()

    try:
        success = asyncio.run(test_keys(args.providers))
        return 0 if success else 1
    except Exception as e:
        print(f"{RED}✗{END} Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Acceptance Criteria**:
- [ ] File created at scripts/test_llm_keys.py
- [ ] Tests all providers
- [ ] Shows key source (keychain vs env)
- [ ] Validates with real API calls
- [ ] Clear pass/fail output
- [ ] Supports --providers filter

---

### Task 3: Make Scripts Executable (5 min)

**Make scripts executable and add to git**:
```bash
# Make executable
chmod +x scripts/migrate_keys_to_keychain.py
chmod +x scripts/test_llm_keys.py

# Verify they run
python scripts/migrate_keys_to_keychain.py --dry-run
python scripts/test_llm_keys.py --help
```

**Acceptance Criteria**:
- [ ] Scripts are executable
- [ ] --help works for both scripts
- [ ] --dry-run works for migration script

---

## Verification Commands

### After Task 1 (Migration Script)
```bash
# Test dry run
python scripts/migrate_keys_to_keychain.py --dry-run

# Expected: Shows current status, migration plan, no changes

# Test help
python scripts/migrate_keys_to_keychain.py --help

# Expected: Shows usage and options
```

### After Task 2 (Test Script)
```bash
# Test help
python scripts/test_llm_keys.py --help

# Expected: Shows usage

# Test validation (with current keys)
python scripts/test_llm_keys.py

# Expected: Tests all providers, shows results
```

### After Task 3 (Executable)
```bash
# Verify executable
ls -la scripts/*.py | grep "migrate_keys\|test_llm"

# Expected: Shows -rwxr-xr-x permissions
```

---

## Success Criteria

Sub-Phase C complete when:
- [ ] Migration script created (200+ lines)
- [ ] Test script created (80+ lines)
- [ ] Both scripts executable
- [ ] Migration script shows status correctly
- [ ] Migration script performs dry run
- [ ] Migration script can migrate keys
- [ ] Test script validates keys
- [ ] Both scripts have --help
- [ ] Clear, user-friendly output

---

## Evidence Format

```markdown
# Sub-Phase C Completion Report

## Task 1: Migration Script ✅

**File Created**: scripts/migrate_keys_to_keychain.py (250 lines)

**Features**:
- Interactive CLI with colored output ✅
- Migration status display ✅
- Dry run mode ✅
- Provider filtering ✅
- Confirmation prompts ✅
- Post-migration instructions ✅

**Test Run**:
```bash
$ python scripts/migrate_keys_to_keychain.py --dry-run

╔═══════════════════════════════════════════════╗
║   Piper Morgan - API Key Migration Tool      ║
║   Migrate keys to secure keychain storage    ║
╚═══════════════════════════════════════════════╝

Current Status
─────────────────
Total providers: 4
  In keychain: 0
  In .env only: 2
  Missing: 2
  Need migration: 2

Provider Details
────────────────
  openai       - Keychain: ✗  Environment: ✓
  anthropic    - Keychain: ✗  Environment: ✓
  gemini       - Keychain: ✗  Environment: ✗
  perplexity   - Keychain: ✗  Environment: ✗

Migration Plan
──────────────
  • Would migrate openai key to keychain
  • Would migrate anthropic key to keychain

ℹ This is a dry run - no changes will be made
```

## Task 2: Test Script ✅

**File Created**: scripts/test_llm_keys.py (95 lines)

**Features**:
- Validates all providers ✅
- Shows key source ✅
- Real API validation ✅
- Provider filtering ✅

**Test Run**:
```bash
$ python scripts/test_llm_keys.py

╔═══════════════════════════════════════════════╗
║   Piper Morgan - API Key Validator           ║
║   Test keys from keychain and environment    ║
╚═══════════════════════════════════════════════╝

Testing API Keys
────────────────────────────────────────────
✓ openai      - Valid (from environment)
✗ anthropic   - Invalid key format
⚠ gemini      - Not configured
⚠ perplexity  - Not configured

Results: 1/4 providers valid
```

## Task 3: Executable ✅

```bash
$ ls -la scripts/*.py | grep "migrate_keys\|test_llm"
-rwxr-xr-x  1 user  staff  8234 Oct  9 21:30 migrate_keys_to_keychain.py
-rwxr-xr-x  1 user  staff  3156 Oct  9 21:30 test_llm_keys.py
```

## Success Criteria: 9/9 ✅

All criteria met - Ready for Phase 4 (PM Configuration)
```

---

## Important Notes

1. **User-Friendly**: Clear output, confirmations, instructions
2. **Safe**: Dry run mode, confirmations before changes
3. **Helpful**: Shows status, provides next steps
4. **Flexible**: Can migrate all or specific providers
5. **Testable**: Validation script to confirm keys work

---

## Time Breakdown

| Task | Description | Time |
|------|-------------|------|
| 1 | Migration script | 30 min |
| 2 | Test script | 15 min |
| 3 | Make executable | 5 min |

**Total**: 50 minutes

---

**After completion, Phase 4 (PM Configuration) uses these tools to migrate your keys**

---

*Sub-Phase 1.5C - October 9, 2025, 9:15 PM*
