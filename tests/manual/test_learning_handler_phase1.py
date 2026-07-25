"""
Manual check for Learning Handler Phase 1 integration.

#1452: hand-run CLI script (sequenced via __main__, hardcodes a live user
UUID, prints). Its former test_ names made pytest collect it — one function
even takes a parameter pytest read as a missing fixture. Renamed check_* so
pytest skips it; run directly: python tests/manual/test_learning_handler_phase1.py
Manual test for Learning Handler Phase 1 integration.

Tests pattern capture, confidence updates, and database persistence.
Run manually: python tests/manual/test_learning_handler_phase1.py

Issue #300: CORE-ALPHA-LEARNING-BASIC - Phase 1 testing
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from uuid import UUID

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.database.session_factory import AsyncSessionFactory
from services.learning.learning_handler import LearningHandler
from services.shared_types import IntentCategory

# Test user (xian)
TEST_USER_ID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")


async def check_pattern_capture():
    """Test pattern capture creates database entry."""
    print("\n" + "=" * 60)
    print("TEST 1: Pattern Capture")
    print("=" * 60)

    handler = LearningHandler()

    async with AsyncSessionFactory.session_scope_fresh() as session:
        # Capture an action
        pattern_id = await handler.capture_action(
            user_id=TEST_USER_ID,
            action_type=IntentCategory.QUERY,
            context={"intent": "test_query", "message": "What's my status?"},
            session=session,
        )

        print(f"✓ Pattern captured with ID: {pattern_id}")

        if pattern_id:
            # Verify pattern exists in database
            from sqlalchemy import select

            from services.database.models import LearnedPattern

            result = await session.execute(
                select(LearnedPattern).where(LearnedPattern.id == pattern_id)
            )
            pattern = result.scalar_one_or_none()

            if pattern:
                print(f"✓ Pattern found in database")
                print(f"  - Pattern Type: {pattern.pattern_type.value}")
                print(f"  - Confidence: {pattern.confidence}")
                print(f"  - Usage Count: {pattern.usage_count}")
                print(f"  - Success Count: {pattern.success_count}")
                print(f"  - Failure Count: {pattern.failure_count}")
                print(f"  - Enabled: {pattern.enabled}")
                return pattern_id
            else:
                print(f"✗ Pattern NOT found in database!")
                return None
        else:
            print(f"✗ Pattern capture failed!")
            return None


async def check_outcome_recording(pattern_id: UUID):
    """Test outcome recording updates confidence."""
    print("\n" + "=" * 60)
    print("TEST 2: Outcome Recording")
    print("=" * 60)

    if not pattern_id:
        print("✗ Skipping - no pattern_id from previous test")
        return

    handler = LearningHandler()

    # Get initial confidence
    async with AsyncSessionFactory.session_scope_fresh() as session:
        from sqlalchemy import select

        from services.database.models import LearnedPattern

        result = await session.execute(
            select(LearnedPattern).where(LearnedPattern.id == pattern_id)
        )
        pattern = result.scalar_one_or_none()
        initial_confidence = pattern.confidence if pattern else None
        print(f"Initial confidence: {initial_confidence}")

    # Record a successful outcome
    async with AsyncSessionFactory.session_scope_fresh() as session:
        success = await handler.record_outcome(
            user_id=TEST_USER_ID,
            pattern_id=pattern_id,
            success=True,
            session=session,
        )

        print(f"✓ Outcome recorded: {success}")

    # Check updated confidence
    async with AsyncSessionFactory.session_scope_fresh() as session:
        result = await session.execute(
            select(LearnedPattern).where(LearnedPattern.id == pattern_id)
        )
        pattern = result.scalar_one_or_none()

        if pattern:
            print(f"✓ Pattern updated in database")
            print(f"  - Confidence: {initial_confidence} → {pattern.confidence}")
            print(f"  - Success Count: {pattern.success_count}")
            print(f"  - Failure Count: {pattern.failure_count}")
            print(f"  - Enabled: {pattern.enabled}")

            if pattern.confidence != initial_confidence:
                print(f"✓ Confidence updated successfully!")
            else:
                print(f"⚠ Confidence unchanged (expected for first use with low volume factor)")
        else:
            print(f"✗ Pattern not found after outcome recording!")


async def check_similar_pattern_detection():
    """Test that similar patterns reuse existing pattern."""
    print("\n" + "=" * 60)
    print("TEST 3: Similar Pattern Detection")
    print("=" * 60)

    handler = LearningHandler()

    # Capture first pattern
    async with AsyncSessionFactory.session_scope_fresh() as session:
        pattern_id_1 = await handler.capture_action(
            user_id=TEST_USER_ID,
            action_type=IntentCategory.QUERY,
            context={"intent": "test_query", "message": "Show me my tasks"},
            session=session,
        )
        print(f"✓ First pattern captured: {pattern_id_1}")

    # Capture similar pattern (same action type)
    async with AsyncSessionFactory.session_scope_fresh() as session:
        pattern_id_2 = await handler.capture_action(
            user_id=TEST_USER_ID,
            action_type=IntentCategory.QUERY,
            context={"intent": "test_query", "message": "What are my tasks?"},
            session=session,
        )
        print(f"✓ Second pattern captured: {pattern_id_2}")

    if pattern_id_1 == pattern_id_2:
        print(f"✓ Similar patterns correctly reused same pattern ID")
    else:
        print(f"⚠ Different pattern IDs (may be expected if similarity logic is strict)")

    # Check usage count increased
    async with AsyncSessionFactory.session_scope_fresh() as session:
        from sqlalchemy import select

        from services.database.models import LearnedPattern

        result = await session.execute(
            select(LearnedPattern).where(LearnedPattern.id == pattern_id_1)
        )
        pattern = result.scalar_one_or_none()

        if pattern and pattern.usage_count > 1:
            print(f"✓ Usage count increased: {pattern.usage_count}")
        elif pattern:
            print(f"⚠ Usage count not increased: {pattern.usage_count}")


async def check_suggestions():
    """Test getting high-confidence suggestions."""
    print("\n" + "=" * 60)
    print("TEST 4: Pattern Suggestions")
    print("=" * 60)

    handler = LearningHandler()

    # Create a pattern and record multiple successes to boost confidence
    async with AsyncSessionFactory.session_scope_fresh() as session:
        pattern_id = await handler.capture_action(
            user_id=TEST_USER_ID,
            action_type=IntentCategory.STATUS,
            context={"intent": "check_status", "message": "What's my current status?"},
            session=session,
        )
        print(f"✓ Pattern created: {pattern_id}")

    # Record multiple successful outcomes to boost confidence
    for i in range(8):
        async with AsyncSessionFactory.session_scope_fresh() as session:
            await handler.record_outcome(
                user_id=TEST_USER_ID,
                pattern_id=pattern_id,
                success=True,
                session=session,
            )
    print(f"✓ Recorded 8 successful outcomes")

    # Check confidence after multiple successes
    async with AsyncSessionFactory.session_scope_fresh() as session:
        from sqlalchemy import select

        from services.database.models import LearnedPattern

        result = await session.execute(
            select(LearnedPattern).where(LearnedPattern.id == pattern_id)
        )
        pattern = result.scalar_one_or_none()
        print(f"  - Confidence after 8 successes: {pattern.confidence}")

    # Get suggestions
    async with AsyncSessionFactory.session_scope_fresh() as session:
        suggestions = await handler.get_suggestions(
            user_id=TEST_USER_ID,
            context={},
            session=session,
        )

        print(f"✓ Retrieved {len(suggestions)} suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. Pattern {suggestion['pattern_id'][:8]}...")
            print(f"     - Confidence: {suggestion['confidence']}")
            print(f"     - Type: {suggestion['pattern_type']}")
            print(f"     - Usage: {suggestion['usage_count']} times")


async def cleanup():
    """Clean up test patterns."""
    print("\n" + "=" * 60)
    print("CLEANUP: Removing test patterns")
    print("=" * 60)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        from sqlalchemy import delete

        from services.database.models import LearnedPattern

        # Delete all patterns for test user
        result = await session.execute(
            delete(LearnedPattern).where(LearnedPattern.user_id == TEST_USER_ID)
        )
        await session.commit()

        print(f"✓ Deleted {result.rowcount} test patterns")


async def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("Learning Handler Phase 1 - Manual Test Suite")
    print("Issue #300: CORE-ALPHA-LEARNING-BASIC")
    print("=" * 60)
    print(f"Test User: {TEST_USER_ID} (xian)")
    print(f"Time: {datetime.now().isoformat()}")

    try:
        # Test 1: Pattern Capture
        pattern_id = await check_pattern_capture()

        # Test 2: Outcome Recording
        if pattern_id:
            await check_outcome_recording(pattern_id)

        # Test 3: Similar Pattern Detection
        await check_similar_pattern_detection()

        # Test 4: Suggestions
        await check_suggestions()

        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETE")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Cleanup
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
