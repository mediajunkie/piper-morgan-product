# CORE-TEST-CACHE: Fix Cache Metrics Test in Test Environment

## Context
During GREAT-5 Phase 1.5, discovered that 1 test fails in test environment while production cache works perfectly. The test expects cache hits but canonical handlers bypass cache in test environment.

## Current State
- Test failing: `tests/intent/test_enforcement_integration.py::test_intent_cache_metrics_endpoint`
- Production cache: Working perfectly (84.6% hit rate, 7.6x speedup)
- Issue: Test environment differs from production behavior
- Non-blocking: 26/27 tests passing, production operational

## Root Cause
In test environment:
1. TestClient creates new app instance
2. Canonical queries bypass cache (go straight to handlers)
3. Cache metrics remain at 0
4. Test expects cache hits, gets 0

In production:
1. Cache properly utilized
2. 84.6% hit rate achieved
3. 7.6x speedup measured

## Scope

### Option 1: Fix Test Environment (Recommended)
Make test environment match production:
```python
@pytest.fixture
def persistent_test_client():
    """Client that maintains cache state across requests"""
    # Share cache instance across test requests
    # Or use actual server instance
```

### Option 2: Adjust Test Expectations
Accept different behavior in test:
```python
def test_intent_cache_metrics_endpoint():
    if TEST_ENVIRONMENT:
        # Skip cache hit assertions
        # Just verify endpoint works
    else:
        # Full cache testing
```

### Option 3: Mock Cache for Test
Use mock to simulate cache hits:
```python
@patch('services.cache.IntentCache')
def test_with_mock_cache(mock_cache):
    mock_cache.hits = 5
    mock_cache.misses = 1
    # Test metrics endpoint
```

## Acceptance Criteria
- [ ] Cache metrics test passes in test environment
- [ ] Solution documented
- [ ] No impact on production cache
- [ ] All 27 tests passing
- [ ] Clear comment explaining the fix

## Success Validation
```bash
# Run the specific test
pytest tests/intent/test_enforcement_integration.py::test_intent_cache_metrics_endpoint -v
# Should pass

# Run all integration tests
pytest tests/intent/test_enforcement_integration.py -v
# 27/27 passing

# Verify production cache unaffected
curl http://localhost:8001/api/admin/intent-cache-metrics
# Should show real metrics
```

## Time Estimate
30-60 minutes

## Priority
Low - Production works perfectly, this is test-only

## Implementation Notes
- Option 1 is cleanest (make test match production)
- Option 2 is fastest (accept the difference)
- Option 3 is middle ground (mock the behavior)
- Choose based on time available

## Files to Modify
- `tests/intent/test_enforcement_integration.py` - The failing test
- Possibly `tests/conftest.py` - If adding new fixture

## Related Documentation
- `dev/2025/10/07/known-issue-cache-metrics-test.md` - Full investigation
- `dev/2025/10/07/great5-phase1.5-intent-fixtures.md` - Discovery context

---

**Note**: This is purely a test environment issue. Production cache operates perfectly with excellent metrics.
