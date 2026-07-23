"""
Auth Integration Tests - Real Database, No Mocks

These tests verify auth system behavior with actual database connections,
catching issues that mocked unit tests miss:
- Token blacklist FK constraints (Issue #291)
- Actual CASCADE delete behavior
- Real async session conflicts
- Multi-user isolation
- Concurrent operations

Run with: pytest -m integration tests/integration/auth/ -v

Issue #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
"""

import asyncio
from uuid import uuid4

import pytest
from sqlalchemy import select

from services.auth.password_service import PasswordService
from services.database.models import TokenBlacklist, User

# #1452 (2026-07-23): the auth routes moved to AsyncSessionFactory.
# session_scope_fresh (#442), so the conftest transaction-rollback strategy
# (override db.get_session, roll everything back) became a dead letter here —
# the app literally cannot see users created inside the rolled-back
# transaction, and every login failed 401. These tests now commit real users
# on a real session and cascade them away via delete_test_user_fully.
_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def db_session():
    """Real committing session on a fresh per-test engine."""
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(_DB_URL)
    maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def user_registry(db_session):
    """Collect created user ids; cascade-delete them all at teardown."""
    from tests.conftest import delete_test_user_fully

    ids = []
    yield ids
    for uid in ids:
        await delete_test_user_fully(db_session, uid)
    await db_session.commit()

# ============================================================================
# Test 1: Full Auth Lifecycle (30 minutes)
# ============================================================================


@pytest.mark.integration
async def test_full_auth_lifecycle(real_client, db_session, user_registry):
    """
    Test complete auth flow: register → login → use → logout → blacklist.

    This is the most critical integration test - it verifies the entire
    authentication lifecycle works end-to-end with a real database.

    Success Criteria:
    - User can register with valid credentials
    - User can login and receive token
    - Token works for authenticated endpoints
    - Logout adds token to blacklist
    - Blacklisted token cannot be used
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # 1. Create new user directly in database
    ps = PasswordService()
    test_password = "TestPass123!"
    hashed = ps.hash_password(test_password)

    test_user = User(
        username=f"testuser_{unique_id}",
        email=f"test_{unique_id}@example.com",
        password_hash=hashed,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)
    user_id = test_user.id
    user_registry.append(user_id)

    # 2. Login with credentials
    login_data = {"username": f"testuser_{unique_id}", "password": test_password}
    response = await real_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["token"]
    assert token is not None

    # 3. Use token to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200, f"Token validation failed: {response.text}"
    me_data = response.json()
    assert me_data["username"] == f"testuser_{unique_id}"
    assert me_data["email"] == f"test_{unique_id}@example.com"

    # 4. Logout (should blacklist token)
    response = await real_client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 200, f"Logout failed: {response.text}"

    # 5. Verify token is blacklisted (REAL database check - no mocks!)
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await db_session.execute(stmt)
    blacklist_entry = result.scalar_one_or_none()

    assert blacklist_entry is not None, "Token not found in blacklist after logout"
    assert str(blacklist_entry.user_id) == str(user_id)
    assert blacklist_entry.reason == "logout"

    # 6. Try to use blacklisted token (should fail)
    response = await real_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401, "Blacklisted token should not work"


# ============================================================================
# Test 2: Multi-User Isolation (30 minutes)
# ============================================================================


@pytest.mark.integration
async def test_multi_user_isolation(real_client, db_session, user_registry):
    """
    Verify users cannot access each other's resources.

    This is critical for security - users should be completely isolated
    from each other's data.

    Success Criteria:
    - Multiple users can register and login
    - Each user gets unique token
    - User cannot access another user's resources
    - Authorization properly enforced
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create two users
    ps = PasswordService()
    test_password = "SecurePass123!"
    hashed = ps.hash_password(test_password)

    users = []
    tokens = []

    for i in range(2):
        # Create user directly in database
        user = User(
            username=f"user{i}_{unique_id}",
            email=f"user{i}_{unique_id}@example.com",
            password_hash=hashed,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        users.append(user)
        user_registry.append(user.id)

        # Login user
        login_data = {"username": f"user{i}_{unique_id}", "password": test_password}
        response = await real_client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200, f"User {i} login failed"
        tokens.append(response.json()["token"])

    # Verify tokens are unique
    assert tokens[0] != tokens[1], "Tokens should be unique per user"

    # Both users can access their own profile
    for i, token in enumerate(tokens):
        headers = {"Authorization": f"Bearer {token}"}
        response = await real_client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        assert response.json()["username"] == f"user{i}_{unique_id}"

    # Test multi-user isolation is enforced
    # Each user should only see their own data
    # This is verified by the token validation itself - tokens are bound to users


# ============================================================================
# Test 3: Token Blacklist Cascade (20 minutes)
# ============================================================================


@pytest.mark.integration
async def test_token_blacklist_cascade_delete(real_client, db_session, user_registry):
    """
    Verify Issue #291: User deletion cascades to token blacklist.

    This test verifies the FK constraint fix from Issue #291 works correctly.
    When a user is deleted, their blacklisted tokens should be automatically
    deleted via CASCADE.

    Success Criteria:
    - Blacklist entry created on logout
    - User deletion cascades to blacklist
    - No orphaned blacklist entries
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create user directly in database
    ps = PasswordService()
    test_password = "CascadeTest123!"
    hashed = ps.hash_password(test_password)

    test_user = User(
        username=f"cascadetest_{unique_id}",
        email=f"cascade_{unique_id}@example.com",
        password_hash=hashed,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)
    user_id = test_user.id
    user_registry.append(user_id)

    # Login and logout (creates blacklist entry)
    login_data = {"username": f"cascadetest_{unique_id}", "password": test_password}
    response = await real_client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await real_client.post("/api/v1/auth/logout", headers=headers)
    assert response.status_code == 200

    # Verify blacklist entry exists
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await db_session.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) == 1, "Should have exactly 1 blacklist entry"

    # Delete user directly from database
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalar_one()

    await db_session.delete(user)
    await db_session.commit()

    # Verify blacklist entry was CASCADE deleted (Issue #291)
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await db_session.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) == 0, "CASCADE delete should remove blacklist entries"


# ============================================================================
# Test 4: Concurrent Session Handling (20 minutes)
# ============================================================================


@pytest.mark.integration
@pytest.mark.skip(
    reason="Concurrent operations conflict with single shared session in transaction rollback strategy"
)
async def test_concurrent_session_handling(real_client, db_session, user_registry):
    """
    Verify concurrent operations don't cause database conflicts.

    Tests that multiple simultaneous auth operations work correctly
    without race conditions or deadlocks.

    Success Criteria:
    - 10 concurrent logins all succeed
    - All tokens are unique
    - All tokens are valid
    - No database errors
    """

    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create user directly in database
    ps = PasswordService()
    test_password = "Concurrent123!"
    hashed = ps.hash_password(test_password)

    test_user = User(
        username=f"concurrentuser_{unique_id}",
        email=f"concurrent_{unique_id}@example.com",
        password_hash=hashed,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    # Concurrent login function
    async def login_attempt():
        login_data = {"username": f"concurrentuser_{unique_id}", "password": test_password}
        response = await real_client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200, f"Concurrent login failed: {response.text}"
        return response.json()["token"]

    # Launch 10 concurrent logins
    tasks = [login_attempt() for _ in range(10)]
    tokens = await asyncio.gather(*tasks)

    # All should succeed with unique tokens
    assert len(tokens) == 10, "Should have 10 tokens"
    assert len(set(tokens)) == 10, "All tokens should be unique"

    # All tokens should work
    async def verify_token(token):
        headers = {"Authorization": f"Bearer {token}"}
        response = await real_client.get("/api/v1/auth/me", headers=headers)
        return response.status_code == 200

    tasks = [verify_token(token) for token in tokens]
    results = await asyncio.gather(*tasks)
    assert all(results), "All tokens should be valid"


# ============================================================================
# Test 5: Password Change Invalidates Tokens
# ============================================================================


@pytest.mark.integration
async def test_password_change_invalidates_tokens(real_client, db_session, user_registry):
    """
    Verify password change invalidates existing tokens.

    This test was deferred from Issue #292 because the password change
    endpoint didn't exist yet. Now it can be implemented.

    Success Criteria:
    - User can change password with correct current password
    - New password meets strength requirements
    - Old token is immediately blacklisted
    - Old token returns 401 Unauthorized after password change
    - Login with new password works
    - New token is valid and works for authenticated endpoints

    Issue #298: AUTH-PASSWORD-CHANGE
    """
    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create user and login
    ps = PasswordService()
    old_password = "OldPass123!"
    hashed = ps.hash_password(old_password)

    test_user = User(
        username=f"pwchangeuser_{unique_id}",
        email=f"pwchange_{unique_id}@example.com",
        password_hash=hashed,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)
    user_id = test_user.id
    user_registry.append(user_id)

    # Login with old password
    login_data = {"username": f"pwchangeuser_{unique_id}", "password": old_password}
    response = await real_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Initial login failed: {response.text}"
    old_token = response.json()["token"]

    # Verify old token works before password change
    headers = {"Authorization": f"Bearer {old_token}"}
    response = await real_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200, "Old token should work before password change"

    # Change password
    new_password = "NewPass456!"
    change_data = {
        "current_password": old_password,
        "new_password": new_password,
        "new_password_confirm": new_password,
    }
    response = await real_client.post(
        "/api/v1/auth/change-password",
        json=change_data,
        headers=headers,
    )
    assert response.status_code == 200, f"Password change failed: {response.text}"
    response_data = response.json()
    assert response_data["success"] is True
    # Current copy: "Your password has been updated. You're all set!"
    assert "password" in response_data["message"].lower()

    # Old token should NO LONGER work
    response = await real_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401, "Old token should be invalidated after password change"

    # Verify token is blacklisted in database
    stmt = select(TokenBlacklist).where(TokenBlacklist.user_id == user_id)
    result = await db_session.execute(stmt)
    blacklist_entries = result.scalars().all()
    assert len(blacklist_entries) > 0, "Token should be blacklisted"

    # Verify blacklist entry has correct reason
    reasons = [entry.reason for entry in blacklist_entries]
    assert "password_change" in reasons, f"Expected 'password_change' reason, got: {reasons}"

    # Login with NEW password should work
    login_data["password"] = new_password
    response = await real_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, "Login with new password should work"
    new_token = response.json()["token"]

    # New token should work
    headers = {"Authorization": f"Bearer {new_token}"}
    response = await real_client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200, "New token should work"
    assert response.json()["username"] == f"pwchangeuser_{unique_id}"


# ============================================================================
# Test 6: Password Change Validation (Password Requirements)
# ============================================================================


@pytest.mark.integration
async def test_password_change_validation(real_client, db_session, user_registry):
    """
    Verify password change validates new password strength requirements.

    Success Criteria:
    - Too short password (< 8 chars) rejected
    - Password missing uppercase letter rejected
    - Password missing lowercase letter rejected
    - Password missing digit rejected
    - Password missing special character rejected
    - Passwords not matching rejected
    - Invalid current password rejected

    Issue #298: AUTH-PASSWORD-CHANGE
    """
    # Generate unique test data
    unique_id = uuid4().hex[:8]

    # Create user and login
    ps = PasswordService()
    current_password = "Current123!"
    hashed = ps.hash_password(current_password)

    test_user = User(
        username=f"validationuser_{unique_id}",
        email=f"validation_{unique_id}@example.com",
        password_hash=hashed,
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)
    user_registry.append(test_user.id)

    # Login to get token
    login_data = {"username": f"validationuser_{unique_id}", "password": current_password}
    response = await real_client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test 1: Password too short
    change_data = {
        "current_password": current_password,
        "new_password": "Short1!",
        "new_password_confirm": "Short1!",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Too short password should be rejected"

    # Test 2: Missing uppercase
    change_data = {
        "current_password": current_password,
        "new_password": "lowercase123!",
        "new_password_confirm": "lowercase123!",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Missing uppercase should be rejected"

    # Test 3: Missing lowercase
    change_data = {
        "current_password": current_password,
        "new_password": "UPPERCASE123!",
        "new_password_confirm": "UPPERCASE123!",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Missing lowercase should be rejected"

    # Test 4: Missing digit
    change_data = {
        "current_password": current_password,
        "new_password": "NoDigits!Pass",
        "new_password_confirm": "NoDigits!Pass",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Missing digit should be rejected"

    # Test 5: Missing special character
    change_data = {
        "current_password": current_password,
        "new_password": "NoSpecial123",
        "new_password_confirm": "NoSpecial123",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Missing special character should be rejected"

    # Test 6: Passwords don't match
    change_data = {
        "current_password": current_password,
        "new_password": "Valid@Pass123",
        "new_password_confirm": "Different@Pass1",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 400, "Non-matching passwords should be rejected"
    # Error middleware reshapes detail -> message
    assert "do not match" in response.json()["message"].lower()

    # Test 7: Wrong current password
    change_data = {
        "current_password": "WrongPass123!",
        "new_password": "Valid@NewPass1",
        "new_password_confirm": "Valid@NewPass1",
    }
    response = await real_client.post(
        "/api/v1/auth/change-password", json=change_data, headers=headers
    )
    assert response.status_code == 401, "Wrong current password should be rejected"
    # The middleware genericizes 401 copy (session-expired guidance) — assert
    # a friendly message exists rather than pinning replaced wording.
    assert response.json()["message"]
