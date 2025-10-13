# Deferred: Cache Test Infrastructure Issue

**Date**: October 9, 2025 (Sprint A1)
**Issue**: #216 - Cache test using wrong JSON key and weak assertions
**Deferred To**: #190 (MVP-TEST-QUALITY)
**Status**: Test fix implemented but infrastructure issue remains
**Decision**: Defer to test quality epic - not blocking Alpha

---

## Summary

Cache test `test_duplicate_queries_use_cache` fails to validate cache behavior due to TestClient lifecycle issue. Production cache works perfectly (84.6% hit rate), but test shows 0 hits/0 misses despite fixing the JSON key bug.

## What Was Fixed

✅ **JSON Key Bug** (lines 74, 78, 89):
- Changed `{"text": "..."}` to `{"message": "..."}`
- Strengthened assertions (200 only, not 422)
- Test now sends correct payload to API

✅ **pytest.ini**:
- Fixed duplicate `markers =` declaration

## What Remains Broken

❌ **Cache Metrics Still Zero**:
```bash
FAILED tests/intent/test_user_flows_complete.py::TestCachingBehavior::test_duplicate_queries_use_cache
assert (final_hits > initial_hits) or (final_misses > initial_misses)
E   assert (0 > 0 or 0 > 0)
```

## Root Cause Analysis

### Evidence

1. **Cache Works in Isolation**:
   ```python
   cache = IntentCache(ttl=3600)
   cache.set('query', data)  # Works
   result = cache.get('query')  # Works - metrics increment correctly
   ```

2. **Global Classifier Has Cache**:
   ```python
   from services.intent_service import classifier
   print(classifier.cache.get_metrics())  # Returns valid metrics structure
   ```

3. **Test Shows Zero Metrics**:
   - First request: hits=0, misses=0
   - Second request: hits=0, misses=0
   - Never increments despite correct JSON key

### Hypothesis: TestClient Lifecycle Issue

**Suspected Problem**:
1. TestClient triggers `web/app.py` lifespan context manager
2. Lifespan creates NEW IntentService (lines 112-119)
3. Test fixture ALSO creates IntentService (`conftest.py:78-82`)
4. Multiple IntentService instances OR cache being cleared between requests
5. Metrics endpoint may read from different cache than classification uses

**Files Involved**:
- `tests/conftest.py:60-85` - client_with_intent fixture
- `web/app.py:46-203` - lifespan context manager
- `web/app.py:113-119` - IntentService initialization

## Production Status

✅ **Cache Works in Production**:
- Hit rate: 84.6% (from gameplan Sprint A1)
- Functionality proven
- No production issues

## Why Deferred

1. **Not Blocking Alpha**: Production cache works perfectly
2. **Test Infrastructure Issue**: Belongs in MVP-TEST-QUALITY (#190)
3. **Time Box Exceeded**: Phase 0 investigation (3 parts) + Phase 1 fix = 72 minutes
4. **Clear Ownership**: #190 specifically targets test quality improvements

## Investigation Summary

### Phase 0 Part 1: Locate Test (8:50 AM - 9:00 AM)
- ✅ Found test at `tests/intent/test_user_flows_complete.py:72-100`
- ✅ Identified companion test at same location

### Phase 0 Part 2: Cache Bypass Investigation (9:00 AM - 9:10 AM)
- ❌ Initial hypothesis: Cache eligibility not met (INCORRECT)
- ✅ Found: Same cache instance in test and production
- ❌ Missed: JSON key issue (found in Part 3)

### Phase 0 Part 3: Cache Eligibility Analysis (9:04 AM - 9:15 AM)
- ✅ Found root cause: `{"text": "..."}` vs `{"message": "..."}`
- ✅ Documented cache eligibility rules
- ✅ Proposed fix with expected behavior

### PM Clarification (9:20 AM - 9:25 AM)
- ✅ Reconciled Part 2 vs Part 3 findings
- ✅ Confirmed Part 2 diagnosis was incorrect
- ✅ Traced full execution path with evidence

### Phase 1: Implementation (9:29 AM - 9:31 AM)
- ✅ Fixed JSON key: `"text"` → `"message"`
- ✅ Strengthened assertions: 200 only (not 422)
- ✅ Fixed pytest.ini duplicate markers
- ❌ Test still fails: cache metrics = 0
- 🛑 STOP CONDITION: Deeper infrastructure issue

## Next Steps (for #190)

**Option A**: Add debug logging to trace IntentService instances
- Log which instance handles each request
- Verify same cache instance used throughout

**Option B**: Modify test to bypass TestClient
- Call IntentService directly
- Eliminate TestClient lifecycle concerns

**Option C**: Investigate cache clearing behavior
- Check if cache cleared between requests
- Verify no cache.clear() calls in test fixtures

**Option D**: Fix TestClient/lifespan interaction
- Prevent lifespan from creating NEW IntentService
- Ensure test fixture's IntentService is used

## Technical Details

### Test Location
- **File**: `tests/intent/test_user_flows_complete.py`
- **Class**: `TestCachingBehavior`
- **Method**: `test_duplicate_queries_use_cache` (lines 72-100)

### Changes Made
```python
# Line 74: Fixed JSON key
query = {"message": "What day is it?"}  # Was: {"text": "..."}

# Line 78: Strengthened assertion
assert response1.status_code == 200  # Was: in [200, 422]

# Line 89: Strengthened assertion
assert response2.status_code == 200  # Was: in [200, 422]
```

### Cache Eligibility Rules
```python
cache_eligible = (
    use_cache=True AND
    context=None AND
    session=None AND
    spatial_context=None
)
```

## Files Modified

1. `tests/intent/test_user_flows_complete.py` - Fixed test JSON key and assertions
2. `pytest.ini` - Fixed duplicate markers declaration
3. `dev/2025/10/09/deferred-cache-test-infrastructure.md` - This document

## Related Issues

- #216 - Original cache test issue (CLOSED as duplicate)
- #190 - MVP-TEST-QUALITY (target epic)
- Sprint A1 Phase 1 - Where this work occurred

## Session Log

Full investigation details: `dev/active/2025-10-09-0843-prog-code-log.md`
- Lines 32-147: Phase 0 Part 1 (test location)
- Lines 158-316: Phase 0 Part 2 (cache bypass investigation)
- Lines 321-503: Phase 0 Part 3 (cache eligibility analysis)
- Lines 508-671: PM clarification (execution trace)
- Lines 676-749: Phase 1 implementation (STOP condition)

---

**Deferred**: October 9, 2025, 9:41 AM
**Reason**: Test infrastructure issue, not production feature
**Target**: MVP-TEST-QUALITY (#190)
