#!/usr/bin/env python3
"""
Password Setup Script for Alpha Users (Issue #281: CORE-ALPHA-WEB-AUTH)

Sets passwords for alpha_users table entries to enable web authentication.

Usage:
    # Set password for specific user
    python scripts/setup_alpha_passwords.py xian --password "test123"

    # Set password for specific user (interactive prompt)
    python scripts/setup_alpha_passwords.py xian

    # Set passwords for all users (interactive for each)
    python scripts/setup_alpha_passwords.py --all

    # List all alpha users
    python scripts/setup_alpha_passwords.py --list

Security Notes:
- Passwords are hashed with bcrypt (12 rounds)
- Never stores plaintext passwords
- Uses secure password validation
- Requires direct database access
"""

import argparse
import asyncio
import getpass
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.password_service import PasswordService
from services.database.connection import db
from services.database.models import AlphaUser


async def list_alpha_users():
    """List all alpha users in the database."""
    print("\n📋 Alpha Users")
    print("=" * 60)

    async with await db.get_session() as session:
        result = await session.execute(select(AlphaUser).order_by(AlphaUser.username))
        users = result.scalars().all()

        if not users:
            print("No alpha users found in database.")
            return

        for user in users:
            has_password = "✅" if user.password_hash else "❌"
            is_active = "✅" if user.is_active else "❌"
            print(f"{has_password} {user.username:20} | Active: {is_active} | Email: {user.email}")

    print(f"\nTotal: {len(users)} users")


async def set_user_password(username: str, password: str = None, interactive: bool = True):
    """
    Set password for a specific user.

    Args:
        username: Username to set password for
        password: Password to set (if None and interactive=True, prompts user)
        interactive: Whether to prompt for password if not provided

    Returns:
        True if successful, False otherwise
    """
    # Initialize database
    if not db._initialized:
        await db.initialize()

    # Find user
    async with await db.get_session() as session:
        result = await session.execute(select(AlphaUser).where(AlphaUser.username == username))
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ User '{username}' not found in alpha_users table")
            return False

        # Get password
        if password is None:
            if not interactive:
                print("❌ Password required (use --password or run interactively)")
                return False

            print(f"\n🔐 Set password for user: {username}")
            print(f"   Email: {user.email}")
            print(
                f"   Current status: {'Has password' if user.password_hash else 'No password set'}"
            )
            print()

            password = getpass.getpass("Enter password: ")
            password_confirm = getpass.getpass("Confirm password: ")

            if password != password_confirm:
                print("❌ Passwords do not match")
                return False

        if not password:
            print("❌ Password cannot be empty")
            return False

        # Validate password strength. Issue 2438: the rules are PasswordValidator's, the
        # same ones the web wizard, a reset and a change apply; no second copy here.
        from services.auth.password_validator import PASSWORD_RULE_LINE, PasswordValidator

        if PasswordValidator.failed_rule(password) is not None:
            print(f"❌ {PASSWORD_RULE_LINE}")
            return False

        # Hash password
        password_service = PasswordService()
        password_hash = password_service.hash_password(password)

        # Update user
        user.password_hash = password_hash
        user.updated_at = datetime.utcnow()
        await session.commit()

        print(f"✅ Password set for user: {username}")
        print(f"   Hash: {password_hash[:20]}...{password_hash[-10:]}")
        print(f"   Length: {len(password_hash)} chars")
        return True


async def set_all_passwords(interactive: bool = True):
    """Set passwords for all alpha users."""
    print("\n🔐 Setting passwords for all alpha users")
    print("=" * 60)

    async with await db.get_session() as session:
        result = await session.execute(select(AlphaUser).order_by(AlphaUser.username))
        users = result.scalars().all()

        if not users:
            print("No alpha users found in database.")
            return

        print(f"Found {len(users)} users")
        print()

        success_count = 0
        for user in users:
            has_password = "✅" if user.password_hash else "❌"
            print(f"{has_password} {user.username} ({user.email})")

            if user.password_hash and interactive:
                response = input(f"   User already has password. Reset? (y/N): ").strip().lower()
                if response not in ["y", "yes"]:
                    print("   Skipped")
                    continue

            success = await set_user_password(user.username, interactive=interactive)
            if success:
                success_count += 1
            print()

        print(f"✅ Set passwords for {success_count}/{len(users)} users")


async def generate_temp_password_for_user(username: str):
    """Generate a temporary password for a user."""
    print(f"\n🔐 Generating temporary password for: {username}")
    print("=" * 60)

    async with await db.get_session() as session:
        result = await session.execute(select(AlphaUser).where(AlphaUser.username == username))
        user = result.scalar_one_or_none()

        if not user:
            print(f"❌ User '{username}' not found in alpha_users table")
            return False

        # Generate temp password
        password_service = PasswordService()
        temp_password = password_service.generate_temp_password(length=16)

        # Hash and save
        password_hash = password_service.hash_password(temp_password)
        user.password_hash = password_hash
        user.updated_at = datetime.utcnow()
        await session.commit()

        print(f"✅ Temporary password generated for: {username}")
        print(f"   Email: {user.email}")
        print()
        print(f"   PASSWORD: {temp_password}")
        print()
        print("   ⚠️  IMPORTANT: Share this password securely!")
        print("   ⚠️  User should change it after first login")
        return True


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Set passwords for alpha users",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all users
  python scripts/setup_alpha_passwords.py --list

  # Set password for specific user (interactive)
  python scripts/setup_alpha_passwords.py xian

  # Set password for specific user (non-interactive)
  python scripts/setup_alpha_passwords.py xian --password "test123"

  # Generate temporary password
  python scripts/setup_alpha_passwords.py xian --generate-temp

  # Set passwords for all users (interactive)
  python scripts/setup_alpha_passwords.py --all

Security:
  - Passwords are hashed with bcrypt (12 rounds)
  - Minimum 8 characters required
  - Use strong, unique passwords for each user
        """,
    )

    parser.add_argument("username", nargs="?", help="Username to set password for")
    parser.add_argument(
        "--password", "-p", help="Password to set (not recommended - use interactive mode)"
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Set passwords for all alpha users (interactive)"
    )
    parser.add_argument("--list", "-l", action="store_true", help="List all alpha users")
    parser.add_argument(
        "--generate-temp", "-g", action="store_true", help="Generate temporary password for user"
    )
    parser.add_argument(
        "--non-interactive", action="store_true", help="Non-interactive mode (requires --password)"
    )

    args = parser.parse_args()

    # Initialize database
    if not db._initialized:
        await db.initialize()

    # List users
    if args.list:
        await list_alpha_users()
        return

    # Set all passwords
    if args.all:
        await set_all_passwords(interactive=not args.non_interactive)
        return

    # Generate temp password
    if args.generate_temp:
        if not args.username:
            print("❌ Username required with --generate-temp")
            parser.print_help()
            sys.exit(1)
        await generate_temp_password_for_user(args.username)
        return

    # Set single user password
    if args.username:
        interactive = not args.non_interactive
        success = await set_user_password(args.username, args.password, interactive=interactive)
        sys.exit(0 if success else 1)

    # No action specified
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
