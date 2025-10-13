# Prompt for Code Agent: GREAT-5 Phase 1.5 - Fix IntentService Test Fixtures

## Context

GREAT-5 Phase 1 revealed a critical issue: IntentService initialization fails in test environment.

**This is Phase 1.5**: Fix IntentService test initialization so all tests can run reliably.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-1535-prog-code-log.md`

## Mission

Fix IntentService initialization in test environment so that:
1. All existing tests can run without "IntentService not available" errors
2. Tests can properly validate intent classification functionality
3. Phase 2 performance benchmarks can run against working system

---

## Background from Phase 1

**Discovery**: Stricter test assertions revealed hidden initialization issue

**Problem**:
- Tests now fail with: "IntentService not available - initialization failed"
- Previously hidden by permissive `[200, 422, 500]` patterns
- Tests were passing even when IntentService wasn't working

**Impact**:
- Blocks Phase 2 (performance benchmarks need working IntentService)
- Blocks Phase 3 (integration tests need working IntentService)
- Multiple test files affected

**Files revealing the issue**:
- `tests/intent/test_user_flows_complete.py`
- `tests/intent/test_integration_complete.py`
- `tests/intent/test_enforcement_integration.py`

---

## Task 1: Diagnose the Issue

### Understand Current State

**Check how tests currently initialize IntentService**:

```bash
# Find existing test fixtures
grep -r "@pytest.fixture" tests/intent/ | grep -i "intent\|service"

# Find how IntentService is imported in tests
grep -r "from.*IntentService" tests/intent/

# Find how IntentService is instantiated
grep -r "IntentService()" tests/intent/
```

**Common initialization patterns**:
1. Direct instantiation: `service = IntentService()`
2. Test client injection: Using FastAPI TestClient
3. Fixture-based: Using pytest fixtures
4. Mock-based: Using unittest.mock

### Identify Root Cause

**Likely issues**:
1. **Missing dependencies**: IntentService requires LLM service, config, etc.
2. **Environment setup**: Test environment missing required files/config
3. **Async initialization**: IntentService needs async setup not happening in tests
4. **Import path issues**: Similar to personality_integration issue from GREAT-4E-2

---

## Task 2: Create Proper Test Fixtures

### Option A: Pytest Fixture (Recommended)

Create fixture in `tests/conftest.py` or `tests/intent/conftest.py`:

```python
import pytest
from services.intent_service import IntentService

@pytest.fixture
async def intent_service():
    """
    Provide properly initialized IntentService for testing.

    Handles all required setup:
    - Configuration loading
    - LLM service initialization
    - Cache setup
    - Any other dependencies
    """
    # Initialize service with test configuration
    service = IntentService()

    # Ensure async initialization complete
    await service.initialize()  # If needed

    yield service

    # Cleanup after test
    await service.cleanup()  # If needed


@pytest.fixture
def intent_service_sync():
    """
    Synchronous version for non-async tests.
    """
    service = IntentService()
    # Synchronous initialization if available
    return service
```

### Option B: Test Client Fixture

If using FastAPI TestClient:

```python
@pytest.fixture
def client_with_intent():
    """
    FastAPI TestClient with IntentService properly initialized.
    """
    from web.app import app
    from fastapi.testclient import TestClient

    # Ensure app is initialized with all services
    client = TestClient(app)

    return client
```

### Option C: Mock for Unit Tests

For tests that don't need real IntentService:

```python
@pytest.fixture
def mock_intent_service():
    """
    Mock IntentService for unit tests.
    Use only when testing code that depends on IntentService
    but doesn't need real classification.
    """
    from unittest.mock import AsyncMock, MagicMock

    service = MagicMock()
    service.classify_intent = AsyncMock(return_value=...)
    service.process_message = AsyncMock(return_value=...)

    return service
```

---

## Task 3: Fix Affected Tests

### Strategy

For each test file revealing issues:

**1. Determine what the test needs**:
- Real intent classification? → Use fixture with real IntentService
- Just endpoint validation? → Use TestClient fixture
- Unit test logic only? → Use mock fixture

**2. Update test to use fixture**:

```python
# BEFORE
def test_something():
    # Test tries to use IntentService but it's not initialized
    response = client.post("/api/v1/intent", ...)
    assert response.status_code in [200, 422]  # Fails with uninitialized service

# AFTER
def test_something(client_with_intent):
    # Test uses properly initialized client
    response = client_with_intent.post("/api/v1/intent", ...)
    assert response.status_code in [200, 422]  # Now works
```

**3. Verify test passes**:
```bash
pytest tests/intent/test_user_flows_complete.py::test_something -v
```

### Files to Fix

Based on Phase 1 report, these files need updates:

1. **tests/intent/test_user_flows_complete.py** (8 tests)
   - `test_intent_endpoint_basic_flow`
   - `test_temporal_query_flow`
   - `test_status_query_flow`
   - `test_priority_query_flow`
   - `test_duplicate_queries_use_cache`
   - `test_personality_enhance_is_exempt`
   - Others using intent endpoint

2. **tests/intent/test_integration_complete.py** (1+ tests)
   - `test_complete_pipeline_exists`
   - Others testing full pipeline

3. **tests/intent/test_enforcement_integration.py** (2+ tests)
   - `test_intent_endpoint_works`
   - `test_standup_uses_backend_intent`

---

## Task 4: Verify All Tests Pass

### Run Full Test Suite

```bash
# Run all intent tests
pytest tests/intent/ -v

# Should show all tests passing now
# If any still fail, investigate why fixture didn't help

# Run regression suite specifically
pytest tests/regression/test_critical_no_mocks.py -v

# Should still show 10/10 passing
```

### Check for Other Failures

```bash
# Run full test suite to catch any other issues
pytest tests/ -v --tb=short

# Document any other initialization issues found
```

---

## Task 5: Document the Fix

Create: `dev/2025/10/07/great5-phase1.5-intent-fixtures.md`

Include:
- What the problem was (IntentService not initialized)
- Why it was hidden (permissive test patterns)
- How it was fixed (proper fixtures created)
- Which tests were updated (file list)
- Test results (before/after counts)
- Lessons learned (test fixture patterns)

---

## Success Criteria

- [ ] Root cause identified and documented
- [ ] Proper test fixtures created (in conftest.py or similar)
- [ ] All affected test files updated to use fixtures
- [ ] All intent tests passing (no "IntentService not available" errors)
- [ ] Regression suite still passing (10/10)
- [ ] Full test suite run successful
- [ ] Changes documented
- [ ] Session log updated

---

## Critical Notes

- **Priority**: This blocks Phase 2 and 3 - must be fixed before proceeding
- **Test types**: Different tests need different fixtures (real vs mock)
- **Async handling**: IntentService may need async initialization
- **Don't skip**: Every test revealing the issue must be fixed or understood
- **Verify thoroughly**: Run full test suite to catch any missed issues

---

## STOP Conditions

- If IntentService requires production credentials to initialize, document and ask PM
- If fixing requires major architectural changes, document scope and ask PM
- If >20 tests affected, document count and ask PM
- If issue is deeper than test fixtures (e.g., broken service), document and ask PM

---

**Effort**: Small-Medium (~30-45 minutes)
**Priority**: CRITICAL (blocks rest of GREAT-5)
**Deliverable**: Working test fixtures + all tests passing
