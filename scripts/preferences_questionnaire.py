"""
Preference Questionnaire CLI

Structured questionnaire for collecting user preferences about communication style,
work style, decision-making, learning, and feedback preferences.

Issue #267 CORE-PREF-QUEST
"""

import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List

def _ensure_venv_when_run_directly() -> None:
    """Re-exec inside ./venv when this script is RUN outside it (CLI affordance).

    Must only run under __main__, never at import: os.execv would replace the
    importing process (pytest collection) with the app, and sys.exit(1) kills
    collection on machines with no ./venv (CI installs into the system env).
    """
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    if in_venv:
        return
    venv_python = os.path.join(os.getcwd(), "venv", "bin", "python")
    if os.path.exists(venv_python):
        print("🔄 Activating virtual environment...")
        os.execv(venv_python, [venv_python, "main.py", "preferences"])
    else:
        print("❌ Error: Virtual environment not found!")
        print("   Run setup wizard first: python3.12 main.py setup")
        sys.exit(1)


from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory

logger = logging.getLogger(__name__)


def parse_choice(input_str: str, options: List[str]) -> str:
    """
    Parse user input (1-N) to option value

    Args:
        input_str: User input string
        options: List of option values

    Returns:
        Selected option or middle option if invalid
    """
    try:
        choice = int(input_str.strip())
        if 1 <= choice <= len(options):
            return options[choice - 1]
    except (ValueError, IndexError):
        pass

    # Default to middle option if invalid input
    return options[len(options) // 2]


async def store_user_preferences(user_id: str, preferences: Dict) -> bool:
    """
    Store preferences in users.preferences JSONB column

    Args:
        user_id: User ID to update
        preferences: Preference dictionary to store

    Returns:
        True if successful, False otherwise
    """
    import json
    import uuid

    try:
        # Add timestamp
        preferences["configured_at"] = datetime.utcnow().isoformat()

        async with AsyncSessionFactory.session_scope() as session:
            # Convert string to UUID for users table
            uid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id

            # Check if user exists in users table
            result = await session.execute(
                text("SELECT id FROM users WHERE id = :user_id"), {"user_id": uid}
            )

            if not result.fetchone():
                logger.error(f"User {user_id} not found in users table")
                return False

            # Update preferences - use CAST for proper JSONB binding
            await session.execute(
                text(
                    """
                    UPDATE users
                    SET preferences = CAST(:prefs AS jsonb)
                    WHERE id = :user_id
                """
                ),
                {"prefs": json.dumps(preferences), "user_id": uid},
            )

            logger.info(f"Stored preferences for user {user_id}")
            return True

    except Exception as e:
        logger.error(f"Failed to store preferences: {e}")
        return False


async def get_current_user_id() -> str:
    """Get the current user ID from the database"""
    try:
        async with AsyncSessionFactory.session_scope() as session:
            # Get the most recent user
            result = await session.execute(
                text("SELECT id FROM users ORDER BY created_at DESC LIMIT 1")
            )

            user = result.fetchone()
            if user:
                # Convert UUID to string for consistency
                return str(user[0])

            logger.error("No users found in database")
            return None

    except Exception as e:
        logger.error(f"Failed to get current user: {e}")
        return None


async def get_existing_preferences(user_id: str) -> Dict:
    """Get existing preferences for user"""
    import uuid

    try:
        async with AsyncSessionFactory.session_scope() as session:
            # Convert string to UUID for users table
            uid = uuid.UUID(user_id) if isinstance(user_id, str) else user_id
            result = await session.execute(
                text("SELECT preferences FROM users WHERE id = :user_id"),
                {"user_id": uid},
            )

            row = result.fetchone()
            if row and row[0]:
                return row[0]  # JSONB column returns dict

            return {}

    except Exception as e:
        logger.error(f"Failed to get existing preferences: {e}")
        return {}


def display_current_preferences(preferences: Dict) -> None:
    """Display current preferences if they exist"""
    if not preferences or "configured_at" not in preferences:
        print("No preferences configured yet.\n")
        return

    print("Current preferences:")
    print(f"  Communication Style: {preferences.get('communication_style', 'not set')}")
    print(f"  Work Style: {preferences.get('work_style', 'not set')}")
    print(f"  Decision Making: {preferences.get('decision_making', 'not set')}")
    print(f"  Learning Style: {preferences.get('learning_style', 'not set')}")
    print(f"  Feedback Level: {preferences.get('feedback_level', 'not set')}")

    configured_at = preferences.get("configured_at", "")
    if configured_at:
        try:
            dt = datetime.fromisoformat(configured_at.replace("Z", "+00:00"))
            print(f"  Last updated: {dt.strftime('%Y-%m-%d %H:%M')}")
        except Exception:
            print(f"  Last updated: {configured_at}")

    print()


async def run_preference_questionnaire(user_id: str) -> bool:
    """
    Run structured preference questionnaire

    Args:
        user_id: User ID to configure preferences for

    Returns:
        True if successful, False otherwise
    """
    try:
        print("\n" + "=" * 50)
        print("🎯 Piper Morgan Preference Setup")
        print("=" * 50)
        print("Let's customize how Piper works for you.")
        print("This will take about 2 minutes.\n")

        # Show existing preferences if any
        existing = await get_existing_preferences(user_id)
        display_current_preferences(existing)

        if existing and "configured_at" in existing:
            update = input("Update your preferences? (y/N): ").strip().lower()
            if update not in ["y", "yes"]:
                print("Preferences unchanged.")
                return True
            print()

        preferences = {}

        # 1. Communication Style
        print("1/5: Communication Style")
        print("How do you prefer Piper Morgan to communicate?")
        print("  1) Concise - Brief, to-the-point responses")
        print("  2) Balanced - Mix of detail and brevity")
        print("  3) Detailed - Comprehensive explanations")
        response = input("Your choice (1-3): ")
        preferences["communication_style"] = parse_choice(
            response, ["concise", "balanced", "detailed"]
        )

        # 2. Work Style
        print("\n2/5: Work Style")
        print("What's your typical work style?")
        print("  1) Structured - Clear plans and schedules")
        print("  2) Flexible - Adaptable to changing needs")
        print("  3) Exploratory - Creative and experimental")
        response = input("Your choice (1-3): ")
        preferences["work_style"] = parse_choice(
            response, ["structured", "flexible", "exploratory"]
        )

        # 3. Decision-Making Style
        print("\n3/5: Decision-Making Style")
        print("How do you prefer to make decisions?")
        print("  1) Data-driven - Based on facts and metrics")
        print("  2) Intuitive - Based on experience and gut feel")
        print("  3) Collaborative - Based on team input")
        response = input("Your choice (1-3): ")
        preferences["decision_making"] = parse_choice(
            response, ["data-driven", "intuitive", "collaborative"]
        )

        # 4. Learning Preference
        print("\n4/5: Learning Preference")
        print("How do you prefer to learn new things?")
        print("  1) Examples - Show me how it's done")
        print("  2) Explanations - Tell me why it works")
        print("  3) Exploration - Let me try it myself")
        response = input("Your choice (1-3): ")
        preferences["learning_style"] = parse_choice(
            response, ["examples", "explanations", "exploration"]
        )

        # 5. Feedback Style
        print("\n5/5: Feedback Style")
        print("What level of feedback do you prefer?")
        print("  1) Minimal - Only essential updates")
        print("  2) Moderate - Key milestones and issues")
        print("  3) Detailed - Comprehensive progress reports")
        response = input("Your choice (1-3): ")
        preferences["feedback_level"] = parse_choice(response, ["minimal", "moderate", "detailed"])

        # Store in database
        success = await store_user_preferences(user_id, preferences)

        if success:
            print("\n" + "=" * 50)
            print("✅ Preferences saved successfully!")
            print("\nYour preferences:")
            for key, value in preferences.items():
                if key != "configured_at":
                    print(f"  {key.replace('_', ' ').title()}: {value}")

            print(f"\nYou can update these anytime with:")
            print(f"  python main.py preferences")
            print("=" * 50)
            return True
        else:
            print("\n❌ Failed to save preferences. Please try again.")
            return False

    except KeyboardInterrupt:
        print("\n\nPreference setup cancelled.")
        return False
    except Exception as e:
        logger.error(f"Error in preference questionnaire: {e}")
        print(f"\n❌ Error: {e}")
        return False


async def main():
    """Main entry point for preference questionnaire"""
    # Get current user
    user_id = await get_current_user_id()

    if not user_id:
        print("❌ No user found. Please run setup first:")
        print("  python main.py setup")
        sys.exit(1)

    # Run questionnaire
    success = await run_preference_questionnaire(user_id)

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    # Allow running directly
    _ensure_venv_when_run_directly()
    asyncio.run(main())
