# CORE-ALPHA-AUTH-INTEGRATION-TESTS - Add Integration Tests for Auth (Reduce Mocking)

**Priority**: P3 (Quality Improvement - Nice to Have)
**Labels**: `testing`, `technical-debt`, `quality`, `post-alpha`
**Milestone**: Sprint A5-A7 (when time allows)
**Related**: #281 (JWT Auth implementation)

---

## Problem Statement

Current auth tests (15/15 passing) heavily rely on mocks, particularly for database operations and token blacklist checking. While unit tests with mocks are valuable, they don't catch integration issues that occur when components interact in the real system.

**Current Test Architecture** ⚠️:
```python
# Global mock in tests/conftest.py
@pytest.fixture(autouse=True)
async def mock_token_blacklist():
    """Mocks TokenBlacklist.is_blacklisted() for ALL tests"""
    with patch("services.auth.models.TokenBlacklist.is_blacklisted", return_value=False):
        yield

# Tests using mock database sessions
async def test_login_success(async_client, db_session):
    # Overrides real database with test session
    # Doesn't test actual DB interactions
```

**What This Hides**:
- ❌ Real database constraint violations
- ❌ Actual blacklist lookup behavior
- ❌ Transaction isolation issues
- ❌ Performance problems (N+1 queries)
- ❌ Connection pool issues

**Evidence This Is a Problem**:
During #281 development, manual testing revealed:
1. Token blacklist FK constraint violation (not caught by tests)
2. Logout not actually blacklisting tokens (tests mocked it)
3. Async session conflicts (hidden by mocks)

**Quote from PM**:
> "I don't love that a lot of these tests use mocks. I know mocks are needed in unit tests but we also need integration testing... the truth will out!"

---

## Goal

**Add integration tests** that hit real database and test full auth flows end-to-end, while **keeping existing unit tests** for fast feedback.

**Test Pyramid**:
```
         Unit Tests (Fast, Mocked)
              /\
             /  \
            /    \
           /      \
          /        \
    Integration     \
    Tests (Slower,  \
    Real DB)        \
                    \
Manual/E2E Tests
```

**Current**: Heavy unit tests (15), minimal integration (0)
**Goal**: Balanced - 15 unit tests + 5-10 integration tests

---

## What Integration Tests Should Cover

### Critical Auth Flows

**Test 1: Full Login → Use Token → Logout → Verify Blacklisted**
```python
@pytest.mark.integration
async def test_full_auth_lifecycle_integration():
    """Test complete auth flow with real database"""
    # No mocks - hits real DB, real blacklist

    # 1. Login
    response = await real_client.post("/auth/login", ...)
    token = response.json()["token"]

    # 2. Use token
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # 3. Logout
    response = await real_client.post("/auth/logout",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # 4. Verify token blacklisted (REAL CHECK)
    is_blacklisted = await TokenBlacklist.is_blacklisted(token)
    assert is_blacklisted is True

    # 5. Try to use token again
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401  # Actually blocked
```

**Test 2: Multi-User Session Isolation**
```python
@pytest.mark.integration
async def test_multi_user_session_isolation():
    """Verify users can't access each other's resources"""
    # Create two real users
    user1 = await create_real_user("alice")
    user2 = await create_real_user("bob")

    # Login as both
    token1 = await login("alice")
    token2 = await login("bob")

    # Upload file as alice
    file_id = await upload_file(token1, "alice-secret.txt")

    # Try to access as bob (should fail)
    response = await download_file(token2, file_id)
    assert response.status_code == 403  # Forbidden
```

**Test 3: Token Expiration**
```python
@pytest.mark.integration
async def test_token_expiration():
    """Verify tokens actually expire"""
    # Login with short-lived token (5 seconds)
    token = await login_with_ttl(ttl_seconds=5)

    # Use immediately (should work)
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

    # Wait for expiration
    await asyncio.sleep(6)

    # Try to use expired token (should fail)
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
```

**Test 4: Concurrent Login/Logout**
```python
@pytest.mark.integration
async def test_concurrent_auth_operations():
    """Test auth under concurrent load"""
    # Multiple users logging in simultaneously
    tasks = [
        login_user(f"user{i}")
        for i in range(10)
    ]
    tokens = await asyncio.gather(*tasks)

    # All should succeed
    assert len(tokens) == 10
    assert all(token is not None for token in tokens)

    # All should be able to use tokens
    tasks = [
        get_current_user(token)
        for token in tokens
    ]
    responses = await asyncio.gather(*tasks)
    assert all(r.status_code == 200 for r in responses)
```

**Test 5: Password Change Invalidates Old Tokens**
```python
@pytest.mark.integration
async def test_password_change_invalidates_tokens():
    """Verify password change revokes existing tokens"""
    # Login
    token = await login("alice", "oldpassword")

    # Change password
    await change_password("alice", "newpassword")

    # Old token should no longer work
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401

    # New login should work
    new_token = await login("alice", "newpassword")
    response = await real_client.get("/auth/me",
        headers={"Authorization": f"Bearer {new_token}"})
    assert response.status_code == 200
```

---

## Implementation Plan

### Phase 1: Setup Integration Test Infrastructure (1 hour)

**Create**: `tests/integration/test_auth_integration.py`

```python
"""
Integration tests for auth - use real database, minimal mocking.

These tests are slower but catch issues that unit tests miss.
Run separately: pytest tests/integration/ -v
"""

import pytest
from httpx import AsyncClient

# Mark all tests in this module as integration
pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
async def real_db():
    """Use real test database (not mocked)"""
    # Initialize real test database
    # Don't mock db.get_session()
    yield
    # Cleanup


@pytest.fixture
async def real_client(real_db):
    """HTTP client with real database"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    # Don't override db.get_session() - use real DB
```

**Configure pytest**:
```ini
# pytest.ini
[pytest]
markers =
    integration: marks tests as integration tests (slow, real DB)
    unit: marks tests as unit tests (fast, mocked)

# Run only unit tests by default
addopts = -m "not integration"

# Run integration tests explicitly
# pytest -m integration
```

### Phase 2: Implement Critical Flow Tests (2 hours)

**Implement 5 tests**:
1. Full auth lifecycle (login → use → logout → verify)
2. Multi-user isolation
3. Token expiration
4. Concurrent operations
5. Password change invalidation

**Each test**:
- Uses real database
- Minimal mocking (only external services if needed)
- Tests actual behavior, not mocked behavior

### Phase 3: Add Performance Benchmarks (30 min)

```python
@pytest.mark.integration
@pytest.mark.benchmark
async def test_auth_performance():
    """Benchmark auth operations"""
    import time

    # Login performance
    start = time.time()
    for _ in range(100):
        await login("testuser")
    duration = time.time() - start

    # Should handle 100 logins in < 10 seconds
    assert duration < 10.0

    # Token validation performance
    token = await login("testuser")
    start = time.time()
    for _ in range(1000):
        await validate_token(token)
    duration = time.time() - start

    # Should validate 1000 tokens in < 1 second
    assert duration < 1.0
```

### Phase 4: Document Test Strategy (30 min)

**Create**: `docs/testing/auth-test-strategy.md`

```markdown
# Auth Testing Strategy

## Test Pyramid

### Unit Tests (Fast, Mocked)
- tests/auth/test_auth_endpoints.py
- 15 tests covering individual components
- Mocked database, mocked blacklist
- Run on every commit (~3 seconds)

### Integration Tests (Slower, Real)
- tests/integration/test_auth_integration.py
- 5-10 tests covering full flows
- Real database, real blacklist
- Run before deploy (~30 seconds)

### Manual Tests (Slowest, Complete)
- dev/active/manual-auth-test-guide.md
- 4 tests covering user experience
- Real server, real browser
- Run before release (~5 minutes)

## When to Use Each

- **Unit tests**: TDD, rapid feedback, CI/CD
- **Integration tests**: Pre-deploy, catch interaction bugs
- **Manual tests**: Pre-release, UX validation
```

---

## Acceptance Criteria

### Infrastructure
- [ ] `tests/integration/` directory created
- [ ] `pytest.ini` configured with integration marker
- [ ] `real_db` fixture that doesn't mock database
- [ ] `real_client` fixture that doesn't override db.get_session()

### Test Coverage
- [ ] Test 1: Full auth lifecycle (5 steps)
- [ ] Test 2: Multi-user isolation
- [ ] Test 3: Token expiration
- [ ] Test 4: Concurrent operations
- [ ] Test 5: Password change invalidation

### Documentation
- [ ] `docs/testing/auth-test-strategy.md` created
- [ ] README updated with integration test instructions
- [ ] CI/CD updated to run integration tests separately

### Quality
- [ ] All 5 integration tests passing
- [ ] Integration tests catch at least one issue unit tests missed
- [ ] Integration test suite runs in < 60 seconds
- [ ] No flaky tests (run 10 times, all pass)

---

## Benefits

### Catches Real Issues
- FK constraint violations
- Transaction isolation bugs
- Connection pool exhaustion
- Race conditions

### Confidence
- Developers can trust that auth works end-to-end
- Deployment confidence higher
- Regressions caught before production

### Documentation
- Integration tests serve as examples of real usage
- Shows how components interact
- Living documentation

---

## Trade-offs

### Pros ✅
- Catches integration issues unit tests miss
- Higher confidence in system behavior
- Better regression detection
- Serves as documentation

### Cons ⚠️
- Slower to run (~30-60 seconds vs 3 seconds)
- Requires test database setup
- More complex to maintain
- Can be flaky if not careful

### Mitigation
- Run unit tests on every commit (fast feedback)
- Run integration tests on push/PR (before merge)
- Keep integration tests focused (5-10, not 50)
- Use pytest markers to control when they run

---

## Testing Strategy

### Run Unit Tests Often
```bash
# Fast feedback during development
pytest tests/auth/test_auth_endpoints.py -v
# 15 passed in 3.48s
```

### Run Integration Tests Before Deploy
```bash
# Comprehensive check before push
pytest -m integration -v
# 5 passed in 42.13s
```

### Run All Tests Before Release
```bash
# Complete validation
pytest tests/ -v
# 20 passed (15 unit + 5 integration) in 45.61s
```

---

## Implementation Priority

**Phase 1**: MUST HAVE (1.5 hours)
- Infrastructure setup
- Test 1 (full lifecycle)
- Test 2 (multi-user isolation)

**Phase 2**: SHOULD HAVE (1 hour)
- Test 3 (token expiration)
- Test 4 (concurrent ops)

**Phase 3**: NICE TO HAVE (30 min)
- Test 5 (password change)
- Performance benchmarks

**Total**: 3 hours for complete implementation

---

## Success Metrics

### Coverage
- Integration tests catch issues unit tests miss
- At least 5 critical flows covered
- Test failures are actionable

### Performance
- Integration suite runs in < 60 seconds
- No flaky tests (99%+ reliability)
- Can run in CI/CD pipeline

### Maintenance
- Tests self-documenting
- Easy to add new integration tests
- Clear separation from unit tests

---

## Related Issues

- **#281**: JWT Auth (where this testing gap was identified)
- **#282**: File Upload (will benefit from integration tests)
- **Token Blacklist FK**: Issue discovered by lack of integration tests

---

## Evidence Required

**Before claiming complete**:

```bash
# 1. Show integration tests exist
ls -la tests/integration/
# Expected: test_auth_integration.py

# 2. Show tests pass
pytest -m integration -v
# Expected: 5 passed

# 3. Show they use real DB (not mocked)
grep -r "mock.*is_blacklisted" tests/integration/
# Expected: No matches (no mocking in integration tests)

# 4. Show configuration works
pytest -m "not integration" -v  # Should skip integration
pytest -m integration -v        # Should run only integration
```

---

**Priority**: P3 - Quality improvement, not blocking
**Effort**: 3 hours (can be split across sprints)
**Value**: High confidence, catches real bugs, better documentation

---

*This issue addresses the testing strategy gap identified during #281, where heavy mocking hid real integration issues. Integration tests complement unit tests to provide comprehensive coverage.*
