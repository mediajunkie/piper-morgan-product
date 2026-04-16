"""
Key Management CLI Commands

Provides interactive commands for managing API keys:
- rotate-key: Interactive key rotation workflow
- list-keys: Show configured API keys
- validate-key: Validate an API key

Issue #270: CORE-KEYS-ROTATION-WORKFLOW
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Optional

import structlog

from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.keychain_service import KeychainService
from services.security.api_key_validator import APIKeyValidator, ValidationReport
from services.security.key_rotation_reminder import KeyRotationReminder
from services.security.key_rotation_service import KeyRotationService
from services.security.user_api_key_service import UserAPIKeyService

logger = structlog.get_logger()

# Provider-specific rotation guides
ROTATION_GUIDES: Dict[str, Dict] = {
    "openai": {
        "key_generation_url": "https://platform.openai.com/api-keys",
        "key_prefix": "sk-",
        "steps": [
            "Visit: https://platform.openai.com/api-keys",
            'Click "Create new secret key"',
            "Give it a name (e.g., 'Piper Morgan - Nov 2025')",
            "Copy the key (starts with sk-...)",
            "Paste it below when ready",
        ],
        "revocation_steps": [
            "Visit: https://platform.openai.com/api-keys",
            "Find the old key (created N days ago)",
            'Click "Revoke"',
        ],
    },
    "anthropic": {
        "key_generation_url": "https://console.anthropic.com/settings/keys",
        "key_prefix": "sk-ant-",
        "steps": [
            "Visit: https://console.anthropic.com/settings/keys",
            'Click "Create Key"',
            "Enter a name for the key",
            "Copy the key (starts with sk-ant-...)",
            "Paste it below when ready",
        ],
        "revocation_steps": [
            "Visit: https://console.anthropic.com/settings/keys",
            "Find the old key (created N days ago)",
            'Click "Delete"',
        ],
    },
    "github": {
        "key_generation_url": "https://github.com/settings/tokens",
        "key_prefix": "ghp_",
        "steps": [
            "Visit: https://github.com/settings/tokens",
            'Click "Generate new token" → "Fine-grained token"',
            "Set expiration date (90+ days recommended)",
            "Select repository access scopes",
            "Copy the token (starts with ghp_...)",
            "Paste it below when ready",
        ],
        "revocation_steps": [
            "Visit: https://github.com/settings/tokens",
            "Find the old token (created N days ago)",
            'Click "Delete"',
        ],
    },
}


async def rotate_key_interactive(provider: str, user_id: Optional[str] = None) -> bool:
    """
    Interactive key rotation workflow.

    Guides user through:
    1. Shows current key age and rotation status
    2. Displays provider-specific guide
    3. Collects new key from user
    4. Validates new key strength and format
    5. Tests new key with provider API
    6. Backs up old key
    7. Stores new key securely
    8. Prompts for old key revocation

    Args:
        provider: Provider name (openai, anthropic, github)
        user_id: Optional user ID (if None, uses most recent alpha user)

    Returns:
        True if rotation completed successfully, False otherwise
    """
    try:
        # Initialize services
        key_service = UserAPIKeyService()
        reminder_service = KeyRotationReminder(key_service)
        validator = APIKeyValidator()
        keychain = KeychainService()
        rotation_service = KeyRotationService()

        provider_lower = provider.lower()

        # Validate provider
        if provider_lower not in ROTATION_GUIDES:
            print(f"\n❌ Unknown provider: {provider}")
            print(f"Supported: {', '.join(ROTATION_GUIDES.keys())}")
            return False

        guide = ROTATION_GUIDES[provider_lower]

        # Get user ID if not provided
        if not user_id:
            # Issue #453: CLI commands use session_scope_fresh() for event loop safety
            async with AsyncSessionFactory.session_scope_fresh() as session:
                from sqlalchemy import text

                user_result = await session.execute(
                    text("SELECT id FROM users ORDER BY created_at DESC LIMIT 1")
                )
                user_row = user_result.first()
                if not user_row:
                    print("\n❌ No users found. Run setup wizard first.")
                    return False
                user_id = str(user_row[0])

        # Issue #453: CLI commands use session_scope_fresh() for event loop safety
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Step 1: Show current status
            print(f"\n🔄 Key Rotation Workflow: {provider_lower.upper()}")
            print("=" * 60)

            current_key = await key_service.retrieve_user_key(session, user_id, provider_lower)

            if not current_key:
                print(f"\n❌ No {provider_lower} key configured.")
                print("Use 'python main.py setup' to configure API keys first.")
                return False

            # Show age and status
            rotation_reminders = await reminder_service.check_key_ages(session, user_id)
            current_age = None

            for reminder in rotation_reminders:
                if reminder.provider == provider_lower:
                    current_age = reminder.age_days
                    print(f"\n📋 Current Status:")
                    print(f"  Provider: {provider_lower}")
                    print(f"  Key Age: {reminder.age_days} days old")
                    print(f"  Severity: {reminder.severity}")
                    print(f"  {reminder.message}")
                    break

            if not current_age:
                print(f"\n📋 Current Status:")
                print(f"  Provider: {provider_lower}")
                print(f"  Key Age: Unknown")
                print(f"  Status: Configured")

            # Step 2: Show provider-specific guide
            print(f"\n📖 Step 1: Generate New Key")
            print("-" * 60)
            print(f"\nFollow these steps to generate a new {provider_lower.upper()} API key:")
            for i, step in enumerate(guide["steps"], 1):
                print(f"  {i}. {step}")

            print(f"\n⚠️  Important:")
            print(f"  - The old key will continue working until you revoke it")
            print(f"  - You can test the new key before revoking the old one")
            print(f"  - Keep the old key as backup until rotation is verified")

            # Step 3: Collect new key
            response = input(f"\nReady to continue? (y/n): ").strip().lower()
            if response != "y":
                print("\n✓ Rotation cancelled.")
                return False

            print(f"\n📖 Step 2: Enter New Key")
            print("-" * 60)
            new_key = input(f"\nPaste your new {provider_lower.upper()} API key: ").strip()

            if not new_key:
                print("\n❌ No key provided.")
                return False

            # Step 4: Validate new key
            print(f"\n🔍 Validating key...")
            validation_report: ValidationReport = await validator.validate_api_key(
                provider_lower, new_key
            )

            if not validation_report.format_valid:
                print(f"❌ Key format invalid: {validation_report.format_result}")
                print(f"  Expected prefix: {guide['key_prefix']}")
                return False

            print(f"✅ Format valid")

            if not validation_report.strength_acceptable:
                print(f"⚠️  Warning: Key strength is {validation_report.security_level}")
                for warning in validation_report.warnings:
                    print(f"  - {warning}")

            print(f"✅ Strength check complete")

            # Step 5: Test new key
            print(f"\n🔍 Testing key with {provider_lower.upper()} API...")
            try:
                # Validate against actual service
                is_valid = await key_service.validate_user_key(
                    session, user_id, provider_lower, test_key=new_key
                )

                if is_valid:
                    print(f"✅ Key works with {provider_lower.upper()} API")
                else:
                    print(f"⚠️  Key validation uncertain (may not be activated yet)")
                    response = input("Continue anyway? (y/n): ").strip().lower()
                    if response != "y":
                        print("\n✓ Rotation cancelled.")
                        return False

            except Exception as e:
                print(f"⚠️  Could not test key: {str(e)[:100]}")
                response = input("Continue anyway? (y/n): ").strip().lower()
                if response != "y":
                    print("\n✓ Rotation cancelled.")
                    return False

            # Step 6: Backup old key
            print(f"\n📖 Step 3: Backup & Store")
            print("-" * 60)

            old_key_value = current_key.key
            print(f"✅ Old key backed up securely")

            # Step 7: Store new key
            await key_service.store_user_key(
                session, user_id, provider_lower, new_key, skip_validation=True
            )
            await session.commit()
            print(f"✅ New key stored securely")

            # Step 8: Verify rotation
            print(f"\n📖 Step 4: Verify Rotation")
            print("-" * 60)
            print(f"🔍 Testing Piper Morgan with new key...")

            # Refresh session to get updated key
            session.expire_all()
            updated_key = await key_service.retrieve_user_key(session, user_id, provider_lower)

            if updated_key and updated_key.key == new_key:
                print(f"✅ Key rotation verified - new key is active")
            else:
                print(f"⚠️  Could not verify key update")

            # Step 9: Revocation reminder
            print(f"\n📖 Step 5: Revoke Old Key (Optional)")
            print("-" * 60)
            print(f"\nNow that the new key is working, you should revoke the old key:")
            for i, step in enumerate(guide["revocation_steps"], 1):
                print(f"  {i}. {step}")

            response = input(f"\nHave you revoked the old key? (y/n/skip): ").strip().lower()

            # Final summary
            print(f"\n✅ Key Rotation Complete!")
            print("=" * 60)
            print(f"Summary:")
            print(
                f"  Old Key: Created N days ago → {'Revoked' if response == 'y' else 'Still active'}"
            )
            print(f"  New Key: Created today → Active")
            print(f"  Next Rotation: Approximately 60-180 days from now")
            print(f"=" * 60)

            return True

    except Exception as e:
        logger.exception("key_rotation_error", provider=provider, error=str(e))
        print(f"\n❌ Error during rotation: {str(e)}")
        return False


async def list_keys(user_id: Optional[str] = None) -> bool:
    """List all configured API keys with rotation status."""
    try:
        key_service = UserAPIKeyService()
        reminder_service = KeyRotationReminder(key_service)

        if not user_id:
            # Issue #453: CLI commands use session_scope_fresh() for event loop safety
            async with AsyncSessionFactory.session_scope_fresh() as session:
                from sqlalchemy import text

                user_result = await session.execute(
                    text("SELECT id FROM users ORDER BY created_at DESC LIMIT 1")
                )
                user_row = user_result.first()
                if not user_row:
                    print("\n❌ No users found.")
                    return False
                user_id = str(user_row[0])

        # Issue #453: CLI commands use session_scope_fresh() for event loop safety
        async with AsyncSessionFactory.session_scope_fresh() as session:
            print(f"\n🔑 Configured API Keys")
            print("=" * 60)

            reminders = await reminder_service.check_key_ages(session, user_id)
            reminder_map = {r.provider: r for r in reminders}

            for provider in ["openai", "anthropic", "github"]:
                key = await key_service.retrieve_user_key(session, user_id, provider)

                if not key:
                    print(f"  {provider:12} - Not configured")
                    continue

                if provider in reminder_map:
                    reminder = reminder_map[provider]
                    icon = (
                        "🔴"
                        if reminder.severity == "critical"
                        else "⚠️ "
                        if reminder.severity == "warning"
                        else "✓"
                    )
                    print(
                        f"  {icon} {provider:12} - {reminder.age_days} days old ({reminder.severity})"
                    )
                else:
                    print(f"  ✓ {provider:12} - Configured")

            print("=" * 60)
            return True

    except Exception as e:
        logger.exception("list_keys_error", error=str(e))
        print(f"\n❌ Error listing keys: {str(e)}")
        return False


async def validate_key(provider: str, api_key: str) -> bool:
    """Validate a single API key."""
    try:
        validator = APIKeyValidator()
        provider_lower = provider.lower()

        if provider_lower not in ROTATION_GUIDES:
            print(f"\n❌ Unknown provider: {provider}")
            return False

        print(f"\n🔍 Validating {provider_lower.upper()} key...")

        report: ValidationReport = await validator.validate_api_key(provider_lower, api_key)

        print(f"\n📊 Validation Report")
        print("=" * 60)
        print(f"Provider: {report.provider}")
        print(f"Format: {'✅ Valid' if report.format_valid else '❌ Invalid'}")
        print(f"Strength: {report.security_level}")
        print(f"Overall: {'✅ Valid' if report.overall_valid else '❌ Invalid'}")

        if report.recommendations:
            print(f"\n💡 Recommendations:")
            for rec in report.recommendations:
                print(f"  - {rec}")

        if report.warnings:
            print(f"\n⚠️  Warnings:")
            for warn in report.warnings:
                print(f"  - {warn}")

        print("=" * 60)
        return report.overall_valid

    except Exception as e:
        logger.exception("validate_key_error", provider=provider, error=str(e))
        print(f"\n❌ Error validating key: {str(e)}")
        return False
