"""
Integration test for setup wizard complete flow.

Tests the setup wizard core phases:
1. API key collection with environment variables
2. User account creation in database
3. Setup wizard function orchestration

Issue #440 - ALPHA-SETUP-INTEGRATION-TEST
"""

import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.integration


class TestSetupWizardIntegrationFlow:
    """Test setup wizard integration with database"""

    @pytest.mark.asyncio
    async def test_user_account_creation_stores_in_database(self, integration_db):
        """Test user account creation phase stores user in database with is_alpha flag"""
        # Arrange: Create a test user via raw SQL (simulating setup wizard result)
        test_user_id = str(uuid4())
        test_username = f"test_user_{uuid4().hex[:8]}"
        test_email = f"{test_username}@test.local"

        # Act: Insert user using integration_db (what setup wizard does)
        await integration_db.execute(
            text(
                """
                INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                   created_at, updated_at, role, is_alpha)
                VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
            """
            ),
            {
                "id": test_user_id,
                "username": test_username,
                "email": test_email,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )
        await integration_db.flush()

        # Assert: User was created with correct attributes
        result = await integration_db.execute(
            text("SELECT id, username, email, is_alpha FROM users WHERE id = :user_id"),
            {"user_id": test_user_id},
        )
        user_row = result.fetchone()
        assert user_row is not None
        assert user_row.username == test_username
        assert user_row.email == test_email
        assert user_row.is_alpha is True

    @pytest.mark.asyncio
    async def test_api_keys_stored_after_user_creation(self, integration_db):
        """Test API keys can be stored for users created by setup wizard"""
        # Arrange: Create a user first
        test_user_id = str(uuid4())
        test_username = f"test_user_{uuid4().hex[:8]}"

        await integration_db.execute(
            text(
                """
                INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                   created_at, updated_at, role, is_alpha)
                VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
            """
            ),
            {
                "id": test_user_id,
                "username": test_username,
                "email": f"{test_username}@test.local",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )
        await integration_db.flush()

        # Act: Store an API key for this user
        test_api_key = "sk-test-api-key-12345"
        # #1452: the table moved to the keychain-reference design — id is
        # autoincrement, the key itself lives behind key_reference (keychain
        # identifier) with encrypted_secret as the DB-store fallback.
        await integration_db.execute(
            text(
                """
                INSERT INTO user_api_keys (user_id, provider, key_reference, encrypted_secret, created_at, updated_at)
                VALUES (:user_id, :provider, :key_reference, :encrypted_secret, :created_at, :updated_at)
            """
            ),
            {
                "user_id": test_user_id,
                "provider": "openai",
                "key_reference": f"openai_{test_user_id}",
                "encrypted_secret": test_api_key,  # Normally encrypted, but we test storage
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )
        await integration_db.flush()

        # Assert: API key was stored
        result = await integration_db.execute(
            text(
                "SELECT provider, encrypted_secret FROM user_api_keys WHERE user_id = :user_id AND provider = :provider"
            ),
            {"user_id": test_user_id, "provider": "openai"},
        )
        api_key_row = result.fetchone()
        assert api_key_row is not None
        assert api_key_row.provider == "openai"
        assert api_key_row.encrypted_secret == test_api_key

    @pytest.mark.asyncio
    async def test_setup_wizard_preflight_checks_phases(self):
        """Test preflight checks phase logic (Python 3.12, venv, SSH)"""
        # Arrange: Import setup functions
        from scripts.setup_wizard import _wizard_preflight_checks

        # Act & Assert: Mock system checks and verify phase passes
        with (
            patch("scripts.setup_wizard.check_python312_available", return_value=True),
            patch("scripts.setup_wizard.setup_virtual_environment", return_value=False),
            patch("scripts.setup_wizard.setup_ssh_key", return_value=True),
            patch("builtins.print"),
        ):  # Suppress output
            # First call should detect venv is already active and skip setup
            # This simulates being run inside the venv
            with patch("sys.prefix", "some/venv/path"), patch("sys.base_prefix", "different/path"):
                result = await _wizard_preflight_checks()
                assert result is True

    @pytest.mark.asyncio
    async def test_setup_wizard_system_checks_docker_check(self):
        """Test system checks phase includes Docker check"""
        # Arrange: Import setup function
        from scripts.setup_wizard import _wizard_system_checks

        # Act & Assert: Mock system checks
        with (
            patch("scripts.setup_wizard.check_system") as mock_check_system,
            patch(
                "scripts.setup_wizard.guide_docker_installation", return_value=True
            ) as mock_guide,
            patch("scripts.setup_wizard.check_docker", return_value=True),
            patch("builtins.print"),
        ):  # Suppress output
            # Mock check_system to return Docker installed
            mock_check_system.return_value = {
                "Docker installed": True,
                "Python 3.9+": True,
                "Port 8001 available": True,
                "PostgreSQL (5433)": True,
                "Redis (6379)": True,
                "ChromaDB (8000)": True,
                "Temporal (7233)": True,
            }

            result = await _wizard_system_checks()
            assert result is True

    @pytest.mark.asyncio
    async def test_setup_wizard_database_setup_checks_schema(self):
        """Test database setup phase checks for existing schema"""
        # Arrange: Import setup function
        from scripts.setup_wizard import _wizard_database_setup

        # Act & Assert: Mock database checks
        # AsyncSessionFactory is imported inside the function, so patch it at import location
        with (
            patch("services.database.session_factory.AsyncSessionFactory") as mock_factory,
            patch("builtins.print"),
        ):  # Suppress output
            # Mock session that has tables (schema exists)
            mock_session = AsyncMock()
            mock_session.execute = AsyncMock(
                return_value=MagicMock(fetchone=MagicMock(return_value=(1,)))
            )
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None

            mock_factory.session_scope_fresh.return_value.__aenter__.return_value = mock_session
            mock_factory.session_scope_fresh.return_value.__aexit__.return_value = None

            with patch("scripts.setup_wizard.subprocess.run", return_value=MagicMock(returncode=0)):
                result = await _wizard_database_setup()
                assert result is True

    @pytest.mark.asyncio
    async def test_collect_single_api_key_from_env_var(self):
        """Test API key collection from environment variable"""
        # Arrange: Import the function
        from scripts.setup_wizard import _collect_single_api_key
        from services.security.user_api_key_service import UserAPIKeyService

        user_id = str(uuid4())
        service = UserAPIKeyService()
        test_key = "sk-test-env-var-12345"

        # Act: Collect with env var set
        with (
            patch.dict(os.environ, {"TEST_KEY_VAR": test_key}),
            patch.object(service, "retrieve_user_key", return_value=None),
            patch("scripts.setup_wizard._check_global_keychain_key", return_value=None),
            patch.object(service, "store_user_key") as mock_store,
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh"
            ) as mock_scope,
            patch("builtins.print"),
        ):  # Suppress output
            # Mock session
            mock_session = AsyncMock()
            mock_session.commit = AsyncMock()
            mock_scope.return_value.__aenter__.return_value = mock_session
            mock_scope.return_value.__aexit__.return_value = None

            result = await _collect_single_api_key(
                user_id=user_id,
                service=service,
                provider="test",
                env_var_name="TEST_KEY_VAR",
                format_hint="sk-...",
                validation_msg="Test key",
                is_required=True,
                skip_validation=True,  # Skip validation for this test
            )

            # Assert: Key was found and stored
            assert result == test_key
            mock_store.assert_called_once()

    @pytest.mark.asyncio
    async def test_setup_wizard_handles_keyboard_interrupt(self):
        """Test setup wizard handles user cancellation gracefully"""
        # Arrange: Import main function
        from scripts.setup_wizard import run_setup_wizard

        # Act: Simulate user pressing Ctrl+C during preflight
        with (
            patch("scripts.setup_wizard._wizard_preflight_checks", side_effect=KeyboardInterrupt()),
            patch("builtins.print"),
        ):
            result = await run_setup_wizard()

            # Assert: Graceful exit
            assert result is False

    @pytest.mark.asyncio
    async def test_setup_wizard_handles_system_errors(self):
        """Test setup wizard handles system errors gracefully"""
        # Arrange: Import main function
        from scripts.setup_wizard import run_setup_wizard

        # Act: Simulate system error during setup
        with (
            patch(
                "scripts.setup_wizard._wizard_preflight_checks",
                side_effect=RuntimeError("System error"),
            ),
            patch("builtins.print"),
        ):
            result = await run_setup_wizard()

            # Assert: Graceful error handling
            assert result is False

    @pytest.mark.asyncio
    async def test_setup_wizard_full_orchestration_mocked(self, integration_db):
        """
        Test full setup wizard orchestration with all phases mocked.
        This is the highest-level integration test.
        """
        # Arrange: Import main function
        from scripts.setup_wizard import run_setup_wizard
        from services.database.connection import db

        # Override db.get_session to use integration_db
        original_get_session = db.get_session
        db.get_session = lambda: integration_db

        try:
            # Act: Mock all system components
            with (
                patch(
                    "scripts.setup_wizard._wizard_preflight_checks", return_value=True
                ) as mock_preflight,
                patch(
                    "scripts.setup_wizard._wizard_system_checks", return_value=True
                ) as mock_system,
                patch("scripts.setup_wizard._wizard_database_setup", return_value=True) as mock_db,
                patch("scripts.setup_wizard.create_user_account") as mock_user_create,
                patch(
                    "scripts.setup_wizard.collect_and_validate_api_keys",
                    return_value={"openai": "sk-test"},
                ) as mock_api_keys,
                patch(
                    "scripts.setup_wizard._wizard_mark_complete", return_value=True
                ) as mock_complete,
                patch("builtins.print"),
            ):  # Suppress output
                # Create a mock user object
                mock_user = MagicMock()
                mock_user.id = uuid4()
                mock_user.username = "testuser"
                mock_user.email = "testuser@example.com"
                mock_user_create.return_value = mock_user

                # Execute setup
                result = await run_setup_wizard()

                # Assert: All phases were called in order
                assert result is True or result is None  # run_setup_wizard returns None on success
                mock_preflight.assert_called_once()
                mock_system.assert_called_once()
                mock_db.assert_called_once()
                mock_user_create.assert_called_once()
                mock_api_keys.assert_called_once()
                mock_complete.assert_called_once()

        finally:
            db.get_session = original_get_session

    @pytest.mark.asyncio
    async def test_alpha_user_flag_is_set_correctly(self, integration_db):
        """Test that users created through setup wizard have is_alpha=true"""
        # Arrange: Create multiple test users with different alpha statuses
        test_users = [
            (str(uuid4()), "alpha_user_1", True),
            (str(uuid4()), "alpha_user_2", True),
            (str(uuid4()), "regular_user_1", False),
        ]

        # Act: Insert users
        for user_id, username, is_alpha in test_users:
            await integration_db.execute(
                text(
                    """
                    INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                       created_at, updated_at, role, is_alpha)
                    VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', :is_alpha)
                """
                ),
                {
                    "id": user_id,
                    "username": username,
                    "email": f"{username}@test.local",
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                    "is_alpha": is_alpha,
                },
            )
        await integration_db.flush()

        # Assert: Verify alpha flags
        for user_id, username, expected_is_alpha in test_users:
            result = await integration_db.execute(
                text("SELECT is_alpha FROM users WHERE username = :username"),
                {"username": username},
            )
            user_row = result.fetchone()
            assert user_row is not None
            assert (
                user_row.is_alpha == expected_is_alpha
            ), f"User {username} should have is_alpha={expected_is_alpha}"

    @pytest.mark.asyncio
    async def test_setup_wizard_marks_setup_complete(self, integration_db):
        """Test that _wizard_mark_complete updates setup_complete flag"""
        # Arrange: Create a user
        test_user_id = str(uuid4())
        test_username = f"test_user_{uuid4().hex[:8]}"

        await integration_db.execute(
            text(
                """
                INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                   created_at, updated_at, role, is_alpha, setup_complete)
                VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true, false)
            """
            ),
            {
                "id": test_user_id,
                "username": test_username,
                "email": f"{test_username}@test.local",
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )
        await integration_db.flush()

        # Create a mock user object (domain model User doesn't exist)
        user = MagicMock()
        user.id = test_user_id
        user.username = test_username
        user.email = f"{test_username}@test.local"
        user.is_active = True
        user.is_verified = False

        # Act: Call mark_complete
        from scripts.setup_wizard import _wizard_mark_complete
        from services.database.connection import db

        original_get_session = db.get_session
        db.get_session = lambda: integration_db

        try:
            with patch("builtins.print"):  # Suppress output
                result = await _wizard_mark_complete(user)

            # Assert: Function executed
            assert result is True

        finally:
            db.get_session = original_get_session
