"""
System Health Checker for Piper Morgan

Checks health of database, API keys, and performance metrics.
Provides actionable recommendations for issues.

Issue #218 CORE-USERS-ONBOARD Phase 1B
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Any, Dict

# Add parent directory to path for imports
sys.path.insert(0, ".")

logger = logging.getLogger(__name__)


class StatusChecker:
    """Check system health and provide diagnostics"""

    async def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and health"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope() as session:
                # Check basic connectivity
                await session.execute(text("SELECT 1"))

                # Count users
                user_count_result = await session.execute(text("SELECT COUNT(*) FROM users"))
                user_count = user_count_result.scalar_one()

                # Get database size (optional, might not work on all setups)
                try:
                    size_result = await session.execute(
                        text("SELECT pg_database_size(current_database())")
                    )
                    db_size_bytes = size_result.scalar_one()
                    db_size_mb = db_size_bytes / (1024 * 1024)
                    size_info = f"{db_size_mb:.1f} MB"
                except Exception:
                    size_info = "unknown"

            return {
                "status": "✓",
                "message": "PostgreSQL connected",
                "details": f"{user_count} users registered, database size: {size_info}",
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Database error: {str(e)[:100]}",
                "details": None,
            }

    async def check_api_keys(self, key_service=None, reminder_service=None) -> Dict[str, Any]:
        """Check API key validity for all providers"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory
            from services.security.key_rotation_reminder import KeyRotationReminder
            from services.security.user_api_key_service import UserAPIKeyService

            # Use provided services or create new ones (for backwards compatibility)
            service = key_service or UserAPIKeyService()
            reminder_service = reminder_service or KeyRotationReminder(service)

            async with AsyncSessionFactory.session_scope() as session:
                # Get most recent user
                user_result = await session.execute(
                    text("SELECT id, username FROM users ORDER BY created_at DESC LIMIT 1")
                )
                user = user_result.first()

                if not user:
                    return {
                        "status": "⚠",
                        "message": "No users found. Run setup wizard first.",
                        "details": {},
                    }

                # Convert UUID to string for alpha users
                user_id, username = str(user[0]), user[1]

                # Check rotation reminders (Issue #250 CORE-KEYS-ROTATION-REMINDERS)
                rotation_reminders = await reminder_service.check_key_ages(session, user_id)
                rotation_status = reminder_service.format_reminder_for_status(rotation_reminders)

                # Check each provider
                results = {}
                for provider in ["openai", "anthropic", "github"]:
                    try:
                        # Retrieve key
                        key = await service.retrieve_user_key(session, user_id, provider)

                        if not key:
                            results[provider] = {"status": "○", "message": "Not configured"}
                            continue

                        # Check for rotation reminders first
                        base_message = ""
                        base_status = "✓"

                        # Validate (only for OpenAI/Anthropic, skip GitHub)
                        if provider in ["openai", "anthropic"]:
                            is_valid = await service.validate_user_key(session, user_id, provider)

                            if is_valid:
                                base_message = "Valid"
                                base_status = "✓"
                            else:
                                base_message = "Invalid or expired"
                                base_status = "✗"
                        else:
                            # GitHub token (don't validate, expensive)
                            base_message = "Configured (not validated)"
                            base_status = "✓"

                        # Add rotation reminder if present
                        if provider in rotation_status:
                            rotation_msg = rotation_status[provider]
                            # Extract just the message part (after the icon)
                            rotation_text = (
                                rotation_msg.split(" ", 1)[1]
                                if " " in rotation_msg
                                else rotation_msg
                            )
                            results[provider] = {
                                "status": rotation_msg.split(" ")[0],  # Use rotation icon
                                "message": f"{base_message} - {rotation_text}",
                            }
                        else:
                            results[provider] = {"status": base_status, "message": base_message}

                    except Exception as e:
                        results[provider] = {
                            "status": "✗",
                            "message": f"Error: {str(e)[:50]}",
                        }

            return {
                "status": "✓",
                "message": f"API Keys for user: {username}",
                "details": results,
                "username": username,
                "user_id": user_id,
            }

        except Exception as e:
            return {
                "status": "✗",
                "message": f"Error checking API keys: {e}",
                "details": {},
            }

    async def check_integrations(self) -> Dict[str, Any]:
        """Check integration health status (Issue #530 ALPHA-SETUP-VERIFY)"""
        try:
            from web.api.routes.integrations import get_integrations_health

            response = await get_integrations_health()

            # Build details dictionary
            details = {}
            for integration in response.integrations:
                status_icons = {
                    "healthy": "✓",
                    "degraded": "⚠",
                    "failed": "✗",
                    "unknown": "○",
                    "not_configured": "○",
                }
                details[integration.display_name] = {
                    "status": status_icons.get(integration.status, "○"),
                    "message": integration.status_message,
                }

            overall_icons = {
                "healthy": "✓",
                "degraded": "⚠",
                "unhealthy": "✗",
            }

            return {
                "status": overall_icons.get(response.overall_status, "○"),
                "message": f"{response.healthy_count}/{response.total_count} integrations healthy",
                "details": details,
            }

        except Exception as e:
            return {
                "status": "✗",
                "message": f"Error checking integrations: {str(e)[:100]}",
                "details": {},
            }

    async def check_performance(self) -> Dict[str, Any]:
        """Check basic performance metrics"""
        try:
            from sqlalchemy import text

            from services.database.session_factory import AsyncSessionFactory

            start = datetime.now()

            # Quick database query
            async with AsyncSessionFactory.session_scope() as session:
                await session.execute(text("SELECT 1"))

            end = datetime.now()
            response_time_ms = (end - start).total_seconds() * 1000

            if response_time_ms < 100:
                status = "✓"
                details = "Good"
            elif response_time_ms < 500:
                status = "⚠"
                details = "Acceptable"
            else:
                status = "✗"
                details = "Slow"

            return {
                "status": status,
                "message": f"Response time: {response_time_ms:.1f}ms",
                "details": details,
            }
        except Exception as e:
            return {
                "status": "✗",
                "message": f"Performance check failed: {e}",
                "details": None,
            }


async def run_status_check():
    """Main status check entry point"""

    print("\n" + "=" * 50)
    print("Piper Morgan System Status")
    print("=" * 50)

    checker = StatusChecker()

    # Initialize services once to avoid duplicate logging
    from services.security.key_rotation_reminder import KeyRotationReminder
    from services.security.user_api_key_service import UserAPIKeyService

    key_service = UserAPIKeyService()
    reminder_service = KeyRotationReminder(key_service)

    # Database
    print("Database:")
    db_status = await checker.check_database()
    print(f"  {db_status['status']} {db_status['message']}")
    if db_status["details"]:
        print(f"     {db_status['details']}")

    # API Keys
    print("\nAPI Keys:")
    key_status = await checker.check_api_keys(key_service, reminder_service)

    if isinstance(key_status, dict) and "status" in key_status:
        if "username" in key_status:
            # Success case with user info (Issue #255 CORE-UX-STATUS-USER)
            print(f"User: {key_status['username']}")
            print()
            for provider, status in key_status["details"].items():
                print(f"  {status['status']} {provider}: {status['message']}")
        else:
            # Error case
            print(f"  {key_status['status']} {key_status['message']}")
    else:
        # Legacy format (shouldn't happen with new code)
        for provider, status in key_status.items():
            print(f"  {status['status']} {provider}: {status['message']}")

    # Integrations (Issue #530 ALPHA-SETUP-VERIFY)
    print("\nIntegrations:")
    integration_status = await checker.check_integrations()
    print(f"  {integration_status['status']} {integration_status['message']}")
    for name, status in integration_status.get("details", {}).items():
        print(f"    {status['status']} {name}: {status['message']}")

    # Performance
    print("\nPerformance:")
    perf_status = await checker.check_performance()
    print(f"  {perf_status['status']} {perf_status['message']}")
    if perf_status["details"]:
        print(f"     {perf_status['details']}")

    # Recommendations
    print("\nRecommendations:")

    recommendations = []

    if db_status["status"] == "✗":
        recommendations.append("  • Fix database connectivity (see error above)")
        recommendations.append("  • Try: docker compose up -d postgres")

    if isinstance(key_status, dict):
        if "status" in key_status:
            if "username" in key_status:
                # Success case - check details
                valid_keys = [
                    p for p, s in key_status["details"].items() if s["status"] in ["✓", "○"]
                ]
                if not valid_keys:
                    recommendations.append(
                        "  • Configure at least one API provider (run: python main.py setup)"
                    )
            else:
                # Error case
                if key_status["status"] == "⚠":
                    recommendations.append(
                        "  • Configure at least one API provider (run: python main.py setup)"
                    )
        else:
            # Legacy format - check if any valid keys
            valid_keys = [p for p, s in key_status.items() if s["status"] in ["✓", "○"]]
            if not valid_keys:
                recommendations.append(
                    "  • Configure at least one API provider (run: python main.py setup)"
                )

    if perf_status["status"] in ["⚠", "✗"]:
        recommendations.append("  • System performance is slow - check database load")
        recommendations.append("  • Try: docker-compose restart")

    # Integration recommendations (Issue #530 ALPHA-SETUP-VERIFY)
    if integration_status["status"] in ["⚠", "✗"]:
        for name, status in integration_status.get("details", {}).items():
            if status["status"] in ["✗", "○"]:
                recommendations.append(
                    f"  • Configure {name}: Visit /settings/integrations/{name.lower()}"
                )

    # Add rotation recommendations (Issue #250 CORE-KEYS-ROTATION-REMINDERS)
    if isinstance(key_status, dict) and "username" in key_status:
        try:
            from services.database.session_factory import AsyncSessionFactory

            # Already in async context, just await directly
            # Reuse reminder_service from initialization to avoid duplicate logging
            async with AsyncSessionFactory.session_scope() as session:
                rotation_recs = await reminder_service.get_rotation_recommendations(
                    session, key_status["user_id"]
                )
                recommendations.extend(rotation_recs)
        except Exception as e:
            logger.warning(f"Failed to get rotation recommendations: {e}")

    if not recommendations:
        recommendations.append("  ✓ All systems operational!")

    for rec in recommendations:
        print(rec)

    print()


if __name__ == "__main__":
    # Allow running directly
    asyncio.run(run_status_check())
