# LLM Service Registration Fix Report

**Date**: October 12, 2025, 9:27 AM - 9:35 AM
**Duration**: 8 minutes active investigation
**Agent**: Code Agent (Claude Code)
**Epic**: CORE-CRAFT-GAP-2
**Status**: ⚠️ **PARTIAL** - ServiceRegistry issue FIXED, LLM client issue DISCOVERED

---

## Executive Summary

**Mission**: Fix LLM service registration in ServiceRegistry to unblock 49 failing tests.

**Result**: ⚠️ **PARTIAL SUCCESS**
- ✅ **Root Cause Identified**: `BaseValidationTest.intent_service` fixture missing LLM registration
- ✅ **ServiceRegistry Issue FIXED**: LLM service now properly registered
- ⚠️ **Secondary Issue Discovered**: LLM client initialization problems (separate issue)
- **Test Status**: Still 6/14 passing, but error changed from ServiceRegistry to LLM client

---

## Investigation Summary

### Step 1: Understand ServiceRegistry ✅

**Found**:
- ServiceRegistry: Singleton pattern at `services/service_registry.py`
- Registration pattern: `ServiceRegistry.register("llm", llm_domain_service)`
- Get pattern: `ServiceRegistry.get_llm()`

**Key Code**:
```python
@classmethod
def get_llm(cls) -> "LLMDomainService":
    """Convenience method for LLM service access"""
    return cls.get("llm")
```

### Step 2: Find LLM Service & Fixture ✅

**Discovery**: Multiple `intent_service` fixtures exist!

**Fixtures Found**:
1. `tests/conftest.py` - Async fixture with LLM registration ✅
2. `tests/intent/base_validation_test.py` - **MISSING LLM registration** ❌
3. Other test files - Various fixtures

**Critical Finding**: Direct Interface tests inherit from `BaseValidationTest`, which uses the fixture WITHOUT LLM registration!

### Step 3: Root Cause Analysis ✅

**The Problem**:
```python
# tests/intent/base_validation_test.py (ORIGINAL)
@pytest.fixture
def intent_service(self):  # ← NOT async, NO LLM registration
    from services.llm.clients import llm_client
    from services.orchestration.engine import OrchestrationEngine

    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    return IntentService(orchestration_engine=orchestration_engine)
```

**Why Tests Failed**:
1. Test inherits from `BaseValidationTest`
2. Uses `intent_service` fixture from base class
3. Fixture creates `IntentService`
4. IntentService uses singleton `classifier` from `services.intent_service.classifier`
5. Classifier lazy-loads LLM: `ServiceRegistry.get_llm()` (line 58)
6. **ERROR**: LLM not registered → `RuntimeError: Service 'llm' not registered`

---

## Fix Applied

### Modified File: `tests/intent/base_validation_test.py`

**Changes**:
```python
@pytest.fixture
async def intent_service(self):  # ← NOW async
    from services.domain.llm_domain_service import LLMDomainService
    from services.llm.clients import llm_client
    from services.orchestration.engine import OrchestrationEngine
    from services.service_registry import ServiceRegistry
    from services.intent_service import classifier

    # Initialize and register LLM service (NEW!)
    llm_domain_service = LLMDomainService()
    await llm_domain_service.initialize()
    ServiceRegistry.register("llm", llm_domain_service)

    orchestration_engine = OrchestrationEngine(llm_client=llm_client)
    service = IntentService(orchestration_engine=orchestration_engine)

    yield service  # ← Changed from return to yield

    # Cleanup (NEW!)
    classifier._llm = None
    ServiceRegistry._services.clear()
```

**Key Changes**:
1. Made fixture `async` (required for `await llm_domain_service.initialize()`)
2. Added LLM service registration before IntentService creation
3. Changed from `return` to `yield` for proper cleanup
4. Added cleanup to reset classifier cache and clear registry

---

## Test Results

### Before Fix

**Error**:
```
RuntimeError: Service 'llm' not registered. Available services: []
```

**Test Status**: 6/14 passing (Direct Interface)
- Passing: Tests using pre-classifier (TEMPORAL, STATUS, PRIORITY, IDENTITY, GUIDANCE, CONVERSATION)
- Failing: Tests needing LLM (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, coverage_report)

### After Fix

**New Error**:
```
RuntimeError: Both LLM providers failed. 
Primary: 'Anthropic' object has no attribute 'messages'
Fallback: module 'openai' has no attribute 'chat'
```

**Test Status**: Still 6/14 passing (Direct Interface)
- Same pattern: Pre-classifier tests pass, LLM-dependent tests fail
- **BUT**: Error changed from ServiceRegistry to LLM client initialization

**Verification Command**:
```bash
$ python -m pytest tests/intent/test_direct_interface.py --tb=no --maxfail=0 -q
.....FFFFFFF.F                                                           [100%]
8 failed, 6 passed, 2 warnings in 28.90s
```

---

## Secondary Issue Discovered

### LLM Client Initialization Problem

**Error Details**:
```
AttributeError: 'Anthropic' object has no attribute 'messages'
AttributeError: module 'openai' has no attribute 'chat'
```

**Location**: `services/llm/clients.py` lines 132 and 169

**Analysis**:
- The Anthropic and OpenAI clients aren't properly initialized
- This is a SEPARATE issue from ServiceRegistry registration
- Likely causes:
  - Version mismatches in client libraries
  - Client initialization in test environment
  - Mock/real client confusion

**Impact**:
- Tests that use pre-classifier (pattern matching) pass ✅
- Tests that need actual LLM classification fail ❌
- This affects the same 8 tests as before, but for a different reason

---

## Files Modified

### 1. tests/conftest.py

**Changes**: Added debug logging and classifier reset (line 68):
```python
# Cleanup: Reset classifier's cached LLM and clear ServiceRegistry
classifier._llm = None
ServiceRegistry._services.clear()
```

### 2. tests/intent/base_validation_test.py ⭐ **PRIMARY FIX**

**Changes**: Complete rewrite of `intent_service` fixture:
- Made async
- Added LLM service registration
- Added cleanup with yield
- Reset classifier cache

---

## Affected Tests

### Direct Interface (14 tests)
- ✅ Passing (6): TEMPORAL, STATUS, PRIORITY, IDENTITY, GUIDANCE, CONVERSATION
- ❌ Failing (8): EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, coverage_report

### Contract Tests (41 tests across 5 files)
**Not fully tested yet**, but pattern likely same:
- `tests/intent/contracts/test_accuracy_contracts.py`
- `tests/intent/contracts/test_bypass_contracts.py`
- `tests/intent/contracts/test_error_contracts.py`
- `tests/intent/contracts/test_multiuser_contracts.py`
- `tests/intent/contracts/test_performance_contracts.py`

---

## Success Criteria Review

**Original Goal**: Unblock 49 tests by fixing LLM service registration

### Achieved ✅
- [x] Root cause identified
- [x] ServiceRegistry registration fixed
- [x] Error changed (progress indicator)
- [x] Solution documented

### Not Achieved ❌
- [ ] 49 tests passing (still failing with different error)
- [ ] LLM client initialization resolved (separate issue)

---

## Recommendations

### Immediate Next Steps

**Option 1: Fix LLM Client Initialization** (Continue fixing)
- Investigate `services/llm/clients.py` initialization
- Check Anthropic/OpenAI library versions
- Verify client initialization in test environment
- Estimated: 1-2 hours

**Option 2: Report Progress** (Stop here)
- ServiceRegistry issue IS fixed (primary mission)
- LLM client issue is SEPARATE problem
- Needs PM decision on scope
- Estimated: Report now, await guidance

### Investigation Needed

**LLM Client Issue**:
1. Check library versions: `pip list | grep -E "anthropic|openai"`
2. Review `services/llm/clients.py` initialization logic
3. Check if test environment needs mocked LLM clients
4. Verify `llm_client` singleton vs `LLMDomainService` client relationship

---

## Architectural Insights

### Singleton Classifier Issue

**Discovery**: The `classifier` object is a singleton created at module import:
```python
# services/intent_service/classifier.py line 826
classifier = IntentClassifier()
```

**Impact**:
- Shared across ALL tests
- Lazy-loads LLM: `self._llm = ServiceRegistry.get_llm()` (line 58)
- Caches LLM reference, which becomes stale when registry clears
- **Fix**: Reset `classifier._llm = None` in fixture cleanup

### Fixture Hierarchy

**Discovered Pattern**:
- Global fixtures in `tests/conftest.py`
- Base class fixtures in `tests/intent/base_validation_test.py`
- Class-level fixtures override global fixtures
- Must fix BOTH to cover all tests

---

## Timeline

| Time | Activity | Result |
|------|----------|--------|
| 9:24 AM | Received LLM fix task | - |
| 9:24-9:26 AM | Read ServiceRegistry | ✅ Pattern understood |
| 9:26-9:27 AM | Read conftest.py | ✅ Found fixture |
| 9:27-9:29 AM | Ran test, added debug | ⚠️ Fixture not running |
| 9:29-9:30 AM | Found BaseValidationTest | ✅ Root cause! |
| 9:30-9:31 AM | Fixed fixture | ✅ Applied fix |
| 9:31-9:33 AM | Testing | ⚠️ New error discovered |
| 9:33-9:35 AM | Analysis & reporting | ✅ Complete |

**Total**: 11 minutes (9:24 AM - 9:35 AM)

---

## Conclusion

**ServiceRegistry Issue**: ✅ **FIXED**

The LLM service registration problem has been resolved. The `BaseValidationTest.intent_service` fixture now properly registers the LLM service in ServiceRegistry before creating IntentService.

**Evidence**: Error changed from "Service 'llm' not registered" to LLM client initialization errors, confirming ServiceRegistry now works.

**Remaining Issue**: ⚠️ **LLM CLIENT INITIALIZATION**

The 8 failing tests now encounter a DIFFERENT error - LLM client (Anthropic/OpenAI) initialization problems. This is a SEPARATE issue from ServiceRegistry registration.

**PM Decision Required**:
1. Continue with LLM client fix? (1-2 hours estimated)
2. Report progress and reassess scope?

---

**Report Complete**: October 12, 2025, 9:35 AM
**Status**: ServiceRegistry FIXED, LLM client issue DISCOVERED
**Next**: Await PM guidance on scope
