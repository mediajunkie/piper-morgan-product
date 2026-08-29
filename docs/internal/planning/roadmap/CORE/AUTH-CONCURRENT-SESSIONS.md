# AUTH-CONCURRENT-SESSIONS - Add Concurrent Session Handling Test + Architecture

**Priority**: P4 (Performance/Scale Feature)
**Labels**: `auth`, `performance`, `testing`, `enterprise`, `technical-debt`
**Milestone**: Post-MVP or Enterprise
**Related**: #292 (Integration Tests), #281 (JWT Auth)
**Created From**: Technical debt identified during #292

---

## Problem Statement

**Architecture Limitation**: Current async authentication implementation doesn't support true concurrent load testing in integration tests.

**Testing Gap**: Cannot verify system behavior under high concurrent load (multiple simultaneous logins, token validations, logouts).

**Origin**: During #292 (Auth Integration Tests), Test 4 (Concurrent Session Handling) was skipped due to documented architecture limitation.

**Why This Matters**:
- Production systems face concurrent requests
- Race conditions can cause data corruption
- Performance under load needs verification
- Enterprise customers expect high concurrency

---

## Current State

**What Works** ✅:
- Single-user auth flows
- Sequential operations
- Basic async support
- Token isolation

**What's Missing** ⚠️:
- Concurrent load testing
- Race condition verification
- Connection pool stress testing
- Multi-user simultaneous operations

**Architecture Issue**:
```python
# Current transaction rollback strategy for test isolation
async with conn.begin_nested() as transaction:
    # Run test
    await transaction.rollback()

# This doesn't support true concurrent operations testing
# because each test runs in isolated transaction
```

---

## Goal

Enable concurrent session testing to verify:
1. **Race Conditions**: No data corruption under load
2. **Connection Pool**: Handles multiple simultaneous requests
3. **Token Uniqueness**: Concurrent logins generate unique tokens
4. **Performance**: Response times acceptable under load

---

## Required Functionality

### Investigation Phase (Understand the Problem)

**Questions to Answer**:
1. What prevents concurrent testing with current architecture?
2. Is it transaction rollback strategy?
3. Is it async implementation?
4. Is it connection pooling config?
5. What approach do other projects use?

**Research**:
- FastAPI concurrent testing patterns
- SQLAlchemy async + pytest patterns
- Transaction isolation + concurrent operations
- Load testing async endpoints

### Architecture Options

**Option A: Separate Load Test Suite** (Recommended for Enterprise)

**Approach**: Integration tests stay transaction-isolated, add separate load tests

```python
# tests/load/test_auth_load.py

import pytest
import asyncio
from locust import HttpUser, task, between

@pytest.mark.load
class AuthLoadTest(HttpUser):
    """Load testing for auth endpoints"""
    wait_time = between(1, 2)

    @task
    def login_concurrent(self):
        """Simulate concurrent logins"""
        self.client.post("/auth/login", json={
            "username": f"user{random.randint(1,100)}",
            "password": "password123"
        })

    @task
    def validate_token(self):
        """Simulate concurrent token validation"""
        self.client.get("/auth/me", headers={
            "Authorization": f"Bearer {self.token}"
        })
```

**Pros**:
- Separate concerns (unit/integration vs load)
- Use proper load testing tools (Locust, K6)
- Real-world simulation
- Doesn't conflict with transaction rollback

**Cons**:
- Requires separate test infrastructure
- More complex setup
- Slower to run

---

**Option B: Modified Integration Test** (If Architecture Allows)

**Approach**: Find way to support concurrent operations within integration tests

```python
@pytest.mark.integration
@pytest.mark.concurrent
async def test_concurrent_session_handling(real_client, integration_db):
    """Verify concurrent operations don't cause conflicts"""

    # Create test user
    user_id = await create_test_user(...)

    # Concurrent login attempts
    async def login_attempt():
        return await real_client.post("/auth/login", json=...)

    # Launch 10 concurrent logins
    tasks = [login_attempt() for _ in range(10)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Verify all succeeded
    tokens = [r.json()["token"] for r in results if r.status_code == 200]
    assert len(tokens) == 10, "All logins should succeed"
    assert len(set(tokens)) == 10, "All tokens should be unique"

    # Concurrent token validation
    async def verify_token(token):
        return await real_client.get("/auth/me",
            headers={"Authorization": f"Bearer {token}"})

    tasks = [verify_token(token) for token in tokens]
    results = await asyncio.gather(*tasks)

    assert all(r.status_code == 200 for r in results)
```

**Pros**:
- Fits with existing integration test suite
- Same infrastructure
- Simpler setup

**Cons**:
- May conflict with transaction rollback
- Not true load testing
- Limited concurrency simulation

---

**Option C: Hybrid Approach** (Recommended)

**Approach**: Both!

1. **Integration Test** (Option B): Verify basic concurrent safety
   - 5-10 concurrent operations
   - Checks for race conditions
   - Part of integration suite

2. **Load Test** (Option A): Verify performance at scale
   - 100+ concurrent operations
   - Real-world load simulation
   - Separate load test suite

**Pros**:
- Best of both worlds
- Progressive validation
- Different concerns tested appropriately

**Cons**:
- More work to implement
- Two test suites to maintain

---

## Implementation Plan (Option C Recommended)

### Phase 1: Investigation (1-2 hours)

**Research concurrent testing approaches**:
1. Review FastAPI + pytest-asyncio concurrent patterns
2. Test if asyncio.gather() works with transaction rollback
3. Identify connection pool configuration
4. Document findings and recommendations

**Deliverable**: Investigation report with approach decision

---

### Phase 2A: Basic Integration Test (1 hour)

**If investigation shows it's possible**:

```python
@pytest.mark.integration
@pytest.mark.concurrent
async def test_concurrent_operations_basic(real_client, integration_db):
    """
    Basic concurrent operations test.

    Verifies no race conditions with 5-10 concurrent operations.
    Not a load test - just checking basic concurrent safety.
    """
    # Implementation based on investigation findings
```

**Add to**: `tests/integration/auth/test_auth_integration.py`

---

### Phase 2B: Load Test Suite (2-3 hours)

**Create**: `tests/load/`

**Structure**:
```
tests/load/
├── __init__.py
├── conftest.py          # Load test fixtures
├── test_auth_load.py    # Auth endpoint load tests
└── README.md            # How to run load tests
```

**Using Locust** (recommended):
```python
# tests/load/test_auth_load.py

from locust import HttpUser, task, between
import random

class AuthUser(HttpUser):
    """Simulates concurrent user auth operations"""

    wait_time = between(1, 3)

    def on_start(self):
        """Login when test starts"""
        response = self.client.post("/auth/login", json={
            "username": f"loadtest_user{random.randint(1,1000)}",
            "password": "LoadTest123!"
        })
        self.token = response.json().get("token")

    @task(3)
    def validate_token(self):
        """Most common operation - validate token"""
        self.client.get("/auth/me", headers={
            "Authorization": f"Bearer {self.token}"
        })

    @task(1)
    def logout_and_relogin(self):
        """Less common - logout and login again"""
        self.client.post("/auth/logout", headers={
            "Authorization": f"Bearer {self.token}"
        })

        response = self.client.post("/auth/login", json={
            "username": f"loadtest_user{random.randint(1,1000)}",
            "password": "LoadTest123!"
        })
        self.token = response.json().get("token")
```

**Run**:
```bash
# Start Piper Morgan
python main.py

# In another terminal, run load test
locust -f tests/load/test_auth_load.py --host=http://localhost:8001

# Open browser to http://localhost:8089
# Configure: 100 users, 10 users/second spawn rate
# Run for 60 seconds
```

---

### Phase 3: Connection Pool Configuration (30 min)

**Verify**: Connection pool can handle concurrent load

```python
# config/database.py

# Current (default)
engine = create_async_engine(
    database_url,
    echo=False,
    # pool_size=5,      # Default
    # max_overflow=10,  # Default
)

# For high concurrency (update if needed)
engine = create_async_engine(
    database_url,
    echo=False,
    pool_size=20,           # More connections
    max_overflow=30,        # More overflow
    pool_recycle=3600,      # Recycle after 1 hour
    pool_pre_ping=True,     # Check connection before use
)
```

**Test**: Verify connection pool doesn't exhaust under load

---

### Phase 4: Documentation (30 min)

**Update**: `docs/testing/integration-test-strategy.md`

Add section:
```markdown
## Concurrent Operations Testing

### Integration Tests
Basic concurrent safety verification (5-10 operations).
Run with: `pytest -m "integration and concurrent" -v`

### Load Tests
Performance validation under real load (100+ operations).
Run with: `locust -f tests/load/test_auth_load.py`

### When to Run
- Integration concurrent: Before every deploy
- Load tests: Before major releases, after performance changes

### What They Catch
- Race conditions
- Connection pool exhaustion
- Token uniqueness issues
- Performance degradation
```

---

## Success Metrics

### Basic Concurrent Test (Phase 2A)
- [ ] 10 concurrent logins all succeed
- [ ] All tokens are unique
- [ ] All tokens can be validated simultaneously
- [ ] No database deadlocks
- [ ] No connection pool errors

### Load Test (Phase 2B)
- [ ] Handles 100 concurrent users
- [ ] 95th percentile response time < 500ms
- [ ] 99th percentile response time < 1000ms
- [ ] Error rate < 1%
- [ ] No connection pool exhaustion

### Connection Pool
- [ ] Can handle expected peak load
- [ ] Connections properly recycled
- [ ] No connection leaks
- [ ] Graceful degradation under overload

---

## Acceptance Criteria

### Investigation Complete
- [ ] Documented what prevents concurrent testing now
- [ ] Evaluated Options A, B, C
- [ ] Chosen approach with rationale
- [ ] Implementation plan updated based on findings

### Testing Infrastructure
- [ ] Basic concurrent integration test (if possible)
- [ ] Load test suite with Locust (or similar)
- [ ] Connection pool configuration verified
- [ ] Both test types documented

### Quality
- [ ] Basic concurrent test passing (if implemented)
- [ ] Load test can run successfully
- [ ] Performance metrics meet targets
- [ ] No flakiness in concurrent tests

### Documentation
- [ ] Testing strategy updated
- [ ] How to run load tests documented
- [ ] Performance targets documented
- [ ] Known limitations listed

---

## Estimated Effort

**Investigation**: 1-2 hours
**Basic Integration Test**: 1 hour (if possible)
**Load Test Suite**: 2-3 hours
**Connection Pool**: 30 minutes
**Documentation**: 30 minutes

**Total**: 5-7 hours

---

## Priority Justification

**P4 (Not P1-P3)** because:
- ✅ Auth works correctly for single users
- ✅ Not blocking MVP
- ✅ Sequential operations tested
- ✅ No evidence of concurrency issues yet

**Should be Post-MVP or Enterprise** because:
- 🏢 Enterprise customers need high concurrency
- 📊 Performance validation before scaling
- 🔒 Race condition verification important
- ⚡ Not critical for small-scale MVP

**When to Prioritize**:
- Before scaling to 100+ users
- When adding Enterprise tier
- If concurrent issues reported
- Before production launch with high load

---

## Alternative: Manual Load Testing

**If automated load testing is too much work**:

```bash
# Use Apache Bench for quick load test
ab -n 1000 -c 10 http://localhost:8001/auth/me \
  -H "Authorization: Bearer {token}"

# -n 1000: 1000 requests total
# -c 10:   10 concurrent requests
# Shows: Requests/sec, response times, failures
```

**Pros**: Quick and simple
**Cons**: Not repeatable, no assertions, manual verification

---

## Related Documentation

- **FastAPI Concurrency**: https://fastapi.tiangolo.com/async/
- **Locust Load Testing**: https://docs.locust.io/
- **SQLAlchemy Pooling**: https://docs.sqlalchemy.org/en/20/core/pooling.html
- **Async Testing Patterns**: https://pytest-asyncio.readthedocs.io/

---

## Milestone Decision Guidance

**Choose MVP If**:
- Planning to launch with >50 users
- Expect high concurrent load
- Time allows (5-7 hours)
- Want confidence in scale

**Choose Post-MVP If**:
- MVP launch is small scale (<50 users)
- Can monitor and respond to issues
- Want to defer complexity
- Focus on other features first

**Choose Enterprise If**:
- Only needed for large customers
- MVP doesn't need this scale
- Can add when needed
- Enterprise features bundled together

**Recommendation**: Post-MVP (defer until scale is needed)

---

**Created From**: Issue #292 scope adjustment
**Milestone**: Post-MVP or Enterprise (PM decision)
**Priority**: P4 (Performance/Scale)
**Effort**: 5-7 hours

---

_This issue captures technical debt from #292 where Test 4 (Concurrent Session Handling) was skipped due to architecture limitations. Requires investigation to determine best approach for concurrent testing at scale._
