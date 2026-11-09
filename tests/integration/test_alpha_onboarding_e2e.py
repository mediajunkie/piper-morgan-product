"""
End-to-End Test for Alpha User Onboarding Flow

When this test passes, we can invite Beatrice as alpha tester #2!

Tests the complete happy path:
1. Setup wizard creates alpha user account
2. User can check system status
3. User sets preferences via questionnaire
4. Final status shows configured state

Issue #259: CORE-USER-ALPHA-TABLE (Alpha/production data separation)
Issue #218: CORE-USERS-ONBOARD (Setup wizard)
"""

import pytest

# ADR-059: Onboarding on ice
pytestmark = pytest.mark.skip(reason="ADR-059: onboarding on ice")


import asyncio
import uuid
from datetime import datetime, timezone
from typing import Optional

import pytest
import sqlalchemy
from sqlalchemy import select, text

from services.database.models import User, UserAPIKey
from services.database.session_factory import AsyncSessionFactory
from services.security.user_api_key_service import UserAPIKeyService


class TestAlphaOnboardingE2E:
    """End-to-end tests for alpha user onboarding flow."""

    @pytest.fixture
    async def clean_test_user(self):
        """Clean up test user before and after test."""
        test_username = f"test_alpha_{uuid.uuid4().hex[:8]}"

        yield test_username

        # Cleanup: Remove test user if it exists
        try:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                result = await session.execute(select(User).where(User.username == test_username))
                user = result.scalar_one_or_none()
                if user:
                    await session.delete(user)
                    await session.commit()
        except Exception:
            pass  # User may not exist

    async def test_alpha_user_creation(self, clean_test_user):
        """
        Test Step 1: Setup wizard creates alpha user account

        Verifies:
        - User record created in users table with is_alpha=True
        - UUID primary key assigned
        - Username and email stored
        - Alpha flag set to True (Issue #262 schema migration)
        - Timestamps created
        """
        username = clean_test_user
        email = f"{username}@test.com"

        # Simulate what setup_wizard.create_user_account() does
        user = User(
            id=uuid.uuid4(),
            username=username,
            email=email,
            is_alpha=True,  # Alpha user flag (Issue #262 schema migration)
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(user)
            await session.commit()

            # Verify user was created
            result = await session.execute(select(User).where(User.username == username))
            created_user = result.scalar_one()

            assert created_user is not None
            assert created_user.username == username
            assert created_user.email == email
            assert created_user.is_alpha is True
            assert isinstance(created_user.id, uuid.UUID)
            assert created_user.created_at is not None
            # migrated_to_prod field removed in Issue #262 schema consolidation

    async def test_system_status_check(self, clean_test_user):
        """
        Test Step 2: Check system status

        Verifies:
        - Database connectivity works
        - Can query users table for alpha users
        - Can retrieve user by ID
        - Status checker finds the user
        """
        # Create user first
        username = clean_test_user
        user_id = uuid.uuid4()

        # Create user in first session
        async with AsyncSessionFactory.session_scope_fresh() as session:
            user = User(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                is_alpha=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(user)
            await session.commit()

        # Verify in separate session
        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Simulate what status_checker.check_database() does
            result = await session.execute(text("SELECT 1"))
            assert result.scalar_one() == 1

            # Count alpha users
            count_result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE is_alpha = true")
            )
            user_count = count_result.scalar_one()
            assert user_count >= 1

            # Retrieve most recent user (what status_checker does)
            user_result = await session.execute(
                text(
                    "SELECT id, username FROM users WHERE is_alpha = true ORDER BY created_at DESC LIMIT 1"
                )
            )
            retrieved_user = user_result.first()
            assert retrieved_user is not None
            assert retrieved_user[1] == username

    @pytest.mark.skip(
        reason="Preferences JSONB column removed in Issue #262 schema migration. Needs redesign to use PersonalityProfile or separate preferences table."
    )
    async def test_preferences_storage(self, clean_test_user):
        """
        Test Step 3: Store and retrieve preferences

        DEPRECATED: User model no longer has preferences JSONB column (Issue #262)
        This test needs redesign to use current PersonalityProfile system.

        Original intent:
        - Preferences saved to alpha_users.preferences JSONB column
        - All 5 preference types stored correctly
        - Can retrieve preferences
        - Timestamp added to preferences
        """
        import json

        username = clean_test_user
        user_id = uuid.uuid4()

        # Create user
        async with AsyncSessionFactory.session_scope_fresh() as session:
            user = User(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                is_alpha=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(user)
            await session.commit()

        # Store preferences (simulating questionnaire)
        preferences = {
            "communication_style": "balanced",
            "work_style": "flexible",
            "decision_making": "collaborative",
            "learning_style": "explanations",
            "feedback_level": "moderate",
            "configured_at": datetime.now(timezone.utc).isoformat(),
        }

        async with AsyncSessionFactory.session_scope_fresh() as session:
            # Simulate what store_user_preferences() does
            await session.execute(
                text(
                    """
                    UPDATE alpha_users
                    SET preferences = CAST(:prefs AS jsonb)
                    WHERE id = :user_id
                """
                ),
                {
                    "prefs": json.dumps(preferences),
                    "user_id": user_id,
                },
            )
            await session.commit()

        # Verify preferences were stored in separate session
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                text("SELECT preferences FROM alpha_users WHERE id = :user_id"),
                {"user_id": user_id},
            )
            row = result.fetchone()
            assert row is not None
            stored_prefs = row[0]

            # JSONB column returns dict
            assert isinstance(stored_prefs, dict)
            assert stored_prefs["communication_style"] == "balanced"
            assert stored_prefs["work_style"] == "flexible"
            assert stored_prefs["decision_making"] == "collaborative"
            assert stored_prefs["learning_style"] == "explanations"
            assert stored_prefs["feedback_level"] == "moderate"
            assert "configured_at" in stored_prefs

    async def test_api_key_storage_with_user(self, clean_test_user):
        """
        Test Step 4: API key storage (integration with alpha user)

        Verifies:
        - API keys can be stored for alpha users
        - UUID to string conversion works
        - No FK violations after migration 648730a3238d
        - UserAPIKey properly linked to alpha user
        """
        username = clean_test_user
        user_id = uuid.uuid4()
        # High-entropy fake: the #268 validator rejects "test123"-style keys as weak,
        # and this test is about storage, not the validator.
        test_key = "sk-proj-Hq4Tz8Wm2Rk7Vb1Nc5Xj9Lp3Fd6Gs0Ya"

        # Create user
        async with AsyncSessionFactory.session_scope_fresh() as session:
            user = User(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                is_alpha=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(user)
            await session.commit()

        # Store API key (user_id converted to string for compatibility)
        service = UserAPIKeyService()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            try:
                # This is what wizard does: convert UUID to string
                user_id_str = str(user_id)

                # Store key using service
                result = await service.store_user_key(
                    session=session,
                    user_id=user_id_str,
                    provider="openai",
                    api_key=test_key,
                    validate=False,
                )

                assert result is not None, "API key storage should return UserAPIKey"
                assert result.provider == "openai"

                # Verify key was stored
                retrieved_key = await service.retrieve_user_key(
                    session=session,
                    user_id=user_id_str,
                    provider="openai",
                )
                assert retrieved_key == test_key

            except sqlalchemy.exc.IntegrityError as e:
                pytest.fail(
                    f"FK constraint violation (should be fixed by migration 648730a3238d): {e}"
                )

    @pytest.mark.skip(
        reason="Preferences JSONB column removed in Issue #262 schema migration. Test needs redesign for current PersonalityProfile system."
    )
    async def test_complete_onboarding_happy_path(self, clean_test_user):
        """
        Test Complete Happy Path: wizard → status → preferences → final status

        DEPRECATED: Depends on preferences JSONB column (removed in Issue #262)

        This is the "birthday success" test!
        Verifies the complete end-to-end flow works:
        1. User created
        2. System status checks pass
        3. Preferences configured (DEPRECATED - column removed)
        4. Final status shows configured
        """
        import json

        username = clean_test_user
        user_id = uuid.uuid4()

        # STEP 1: Create user (setup wizard)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            user = User(
                id=user_id,
                username=username,
                email=f"{username}@test.com",
                is_alpha=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            session.add(user)
            await session.commit()

        # STEP 2: Check status (should find user) - in new session
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(
                text(
                    "SELECT id, username FROM users WHERE is_alpha = true ORDER BY created_at DESC LIMIT 1"
                )
            )
            retrieved = result.first()
            assert retrieved is not None
            assert retrieved[1] == username

        # STEP 3: Configure preferences - in new session
        preferences = {
            "communication_style": "balanced",
            "work_style": "flexible",
            "decision_making": "collaborative",
            "learning_style": "explanations",
            "feedback_level": "moderate",
            "configured_at": datetime.now(timezone.utc).isoformat(),
        }

        # NOTE: Preferences storage removed in Issue #262 schema consolidation
        # User model no longer has preferences JSONB column
        # This test needs redesign to use PersonalityProfile or separate preferences table
        #
        # async with AsyncSessionFactory.session_scope_fresh() as session:
        #     await session.execute(
        #         text(
        #             """
        #             UPDATE users
        #             SET preferences = CAST(:prefs AS jsonb)
        #             WHERE id = :user_id
        #         """
        #         ),
        #         {
        #             "prefs": json.dumps(preferences),
        #             "user_id": user_id,
        #         },
        #     )
        #     await session.commit()

        # STEP 4: Verify final state - in new session
        async with AsyncSessionFactory.session_scope_fresh() as session:
            result = await session.execute(select(User).where(User.id == user_id))
            final_user = result.scalar_one()

            assert final_user.username == username
            # Preferences assertions removed - functionality not implemented in current schema
            # assert final_user.preferences is not None
            # assert final_user.preferences["communication_style"] == "balanced"
            assert final_user.is_alpha is True
            # migrated_to_prod field removed in Issue #262

        # 🎉 Success!


# Async test support (use pytest-asyncio)
pytestmark = pytest.mark.asyncio
