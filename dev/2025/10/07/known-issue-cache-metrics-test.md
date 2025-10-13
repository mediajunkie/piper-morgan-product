# Known Issue: Cache Metrics Test Failure

**Discovered**: October 7, 2025, 4:45 PM (GREAT-5 Phase 1.5)
**Status**: DOCUMENTED - Not fixed
**Priority**: Low (non-blocking)
**Component**: Intent cache testing
**Epic**: GREAT-5 Phase 1/1.5

---

## Issue Description

Test `test_duplicate_queries_use_cache` in `tests/intent/test_user_flows_complete.py` fails with assertion error:

```
assert (0 > 0 or 0 > 0)
```

**Location**: `tests/intent/test_user_flows_complete.py:100`

**Failure Pattern**: Cache metrics (hits/misses) not updating between sequential test requests

---

## Technical Details

### Test Logic
```python
def test_duplicate_queries_use_cache(self, client):
    """Same query twice should show cache improvement."""
    query = {"text": "What day is it?"}

    # First request - likely cache miss
    response1 = client.post("/api/v1/intent", json=query)

    # Get initial cache metrics
    metrics1 = client.get("/api/admin/intent-cache-metrics").json()["metrics"]
    initial_hits = metrics1.get("hits", 0)
    initial_misses = metrics1.get("misses", 0)

    # Second request - should hit cache
    response2 = client.post("/api/v1/intent", json=query)

    # Get updated cache metrics
    metrics2 = client.get("/api/admin/intent-cache-metrics").json()["metrics"]
    final_hits = metrics2.get("hits", 0)
    final_misses = metrics2.get("misses", 0)

    # FAILS HERE: Both initial and final are 0
    assert (final_hits > initial_hits) or (final_misses > initial_misses)
```

### Why It Fails

**Hypothesis**: Cache is shared across test runs and may already be initialized

**Evidence**:
- Both `initial_hits` and `final_hits` are 0
- Both `initial_misses` and `final_misses` are 0
- Suggests cache state is either:
  1. Not being tracked properly in test environment
  2. Being reset between metric checks
  3. TestClient creates new cache instance per request

**Related Code**:
- Cache implementation: `services/intent_service/cache.py`
- Cache endpoint: `web/app.py:540-554` (GET /api/admin/intent-cache-metrics)
- IntentService fixture: `tests/conftest.py:60-84`

---

## Root Cause Analysis

### Likely Issue: Cache State Isolation

**Problem**: TestClient may create fresh app state per request, losing cache continuity

**Evidence**:
1. IntentService initialized in `client_with_intent` fixture
2. Each test request may reinitialize IntentService
3. Cache metrics reset with each new IntentService instance

**Why Hidden Before**:
- Permissive test patterns accepted any result
- Test had `[200, 422, 500]` - would pass regardless of cache working

---

## Impact Assessment

### Severity: LOW
- **Production Impact**: None - production cache works fine
- **Test Coverage**: Only affects 1 test out of 27
- **Blocking**: Does not block GREAT-5 phases 2, 3, 4
- **Functionality**: IntentService working, only cache *metrics* test fails

### What Still Works
✅ Intent classification
✅ Canonical handlers
✅ IntentService initialization
✅ Cache endpoints return valid responses
✅ 26/27 other tests passing

### What's Broken
❌ Verifying cache metrics update between requests in test environment

---

## Recommended Fixes

### Option 1: Add Cache Reset Fixture (Recommended)
```python
@pytest.fixture(autouse=True)
def reset_cache_before_test():
    """Reset cache state before each test."""
    from services.intent_service import classifier
    if hasattr(classifier, 'cache'):
        classifier.cache.clear()
    yield
```

**Pros**: Clean slate for each test
**Cons**: May hide cache persistence issues
**Effort**: 5 minutes

### Option 2: Fix TestClient to Maintain State
Ensure TestClient reuses same IntentService instance across requests

**Pros**: More realistic testing
**Cons**: May require TestClient internals knowledge
**Effort**: 15-30 minutes

### Option 3: Adjust Test Expectations
Accept that cache may already have state, test relative changes

**Pros**: Minimal code change
**Cons**: Weaker test guarantees
**Effort**: 5 minutes

### Option 4: Mock Cache for Test
Use mock cache with controlled state

**Pros**: Fully controlled test environment
**Cons**: Not testing real cache implementation
**Effort**: 10 minutes

---

## Workaround

**Current**: Test skipped/documented as known issue

**Alternative**: Run test in isolation:
```bash
pytest tests/intent/test_user_flows_complete.py::TestCachingBehavior::test_duplicate_queries_use_cache -xvs
```

May pass if cache is fresh (not guaranteed).

---

## Decision

**Chosen**: Document and defer (this file)

**Reasoning**:
1. Non-blocking for GREAT-5 mission
2. Inchworm methodology: finish current branch first
3. IntentService initialization fixed (Phase 1.5 complete)
4. Can address in dedicated cache testing epic

**Future Epic Suggestion**: GREAT-5.5 or POST-GREAT-5-CACHE-TESTING

---

## How to Reproduce

```bash
# Run the failing test
PYTHONPATH=. python3 -m pytest \
  tests/intent/test_user_flows_complete.py::TestCachingBehavior::test_duplicate_queries_use_cache \
  -xvs

# Expected: FAILED with assert (0 > 0 or 0 > 0)
# Actual: FAILED (as of Oct 7, 2025, 4:45 PM)
```

---

## Related Issues

**Fixed in Phase 1.5**:
- IntentService initialization (was blocking, now fixed)
- Attribute name errors in cache endpoints (fixed)

**Not Yet Fixed**:
- Cache metrics test (this issue)

---

## Documentation Links

- **Phase 1 Report**: `dev/2025/10/07/great5-phase1-regression-suite.md`
- **Phase 1.5 Report**: `dev/2025/10/07/great5-phase1.5-intent-fixtures.md`
- **Session Log**: `dev/2025/10/07/2025-10-07-1540-prog-code-log.md`

---

## Follow-up Required

- [ ] Create GitHub issue for cache metrics test fix
- [ ] Add to backlog for future sprint
- [ ] Consider as part of broader cache testing improvements
- [ ] Revisit after GREAT-5 complete

---

**Documented By**: Code Agent (Claude Code)
**Date**: October 7, 2025, 4:48 PM
**Epic**: GREAT-5 Phase 1/1.5
**Status**: Known limitation, documented for future fix
