# LLM Service Registration Fix

**Date**: October 12, 2025, 9:24 AM  
**Agent**: Code Agent  
**Epic**: CORE-CRAFT-GAP-2  
**Task**: Fix LLM service registration in ServiceRegistry

---

## Mission

Register LLM service in ServiceRegistry for test environment to unblock 49 tests currently failing with LLM service registration errors.

**Context**: Phase 0 found 49 test failures with same root cause:
```
IntentProcessingError: Intent processing failed: API Error [INTENT_CLASSIFICATION_FAILED]
```

**Root Cause**: ServiceRegistry does not have LLM service registered during tests

---

## Problem Analysis

### Affected Tests (49 total)

**Direct Interface Tests** (8 tests):
- `tests/intent/test_direct_interface.py`
- Tests failing due to missing LLM service

**Contract Tests** (41 tests):
- `tests/intent/contracts/test_accuracy_contracts.py` (7 tests)
- `tests/intent/contracts/test_bypass_contracts.py` (7 tests)
- `tests/intent/contracts/test_error_contracts.py` (13 tests)
- `tests/intent/contracts/test_multiuser_contracts.py` (7 tests)
- `tests/intent/contracts/test_performance_contracts.py` (7 tests)

### Error Pattern

```python
IntentProcessingError: Intent processing failed: API Error [INTENT_CLASSIFICATION_FAILED]
```

This indicates:
- IntentService trying to use LLM service
- LLM service not registered in ServiceRegistry
- Test environment setup incomplete

---

## Investigation Steps

### Step 1: Understand ServiceRegistry (15-20 min)

**Find ServiceRegistry**:
```bash
# Locate ServiceRegistry implementation
find . -name "*service*registry*" -type f | grep -v __pycache__

# Or search for ServiceRegistry class
grep -r "class ServiceRegistry" --include="*.py"
```

**Study registration pattern**:
- How are services registered?
- Where does registration happen?
- What's the pattern for test vs production?

### Step 2: Find LLM Service (10-15 min)

**Locate LLM service implementation**:
```bash
# Find LLM service
find services/ -name "*llm*" -type f | grep -v __pycache__

# Or search for LLM class
grep -r "class.*LLM" services/ --include="*.py"
```

**Understand LLM service**:
- What's the class name?
- What interface does it implement?
- How is it used by IntentService?

### Step 3: Find Working Examples (10-15 min)

**Look for services that ARE registered**:
```bash
# Search for service registration examples
grep -r "register.*service" --include="*.py" | head -20

# Find test fixtures that register services
grep -r "@pytest.fixture" tests/ --include="*.py" -A 5 | grep -i service
```

**Study pattern**:
- How do other services get registered in tests?
- Where is registration code?
- What's the pattern to follow?

---

## Implementation Approach

### Option 1: Test Fixture Approach

**If services registered via fixtures**:

1. **Find or create fixture file**:
   - Look for `tests/conftest.py` (pytest global fixtures)
   - Or `tests/intent/conftest.py` (local fixtures)

2. **Add LLM service fixture**:
   ```python
   @pytest.fixture(autouse=True)
   def register_llm_service():
       """Register LLM service for tests."""
       from services.service_registry import ServiceRegistry
       from services.llm_service import LLMService  # Adjust import
       
       registry = ServiceRegistry.get_instance()
       llm_service = LLMService()  # Or Mock if needed
       registry.register("llm_service", llm_service)
       
       yield
       
       # Cleanup if needed
       registry.unregister("llm_service")
   ```

3. **Verify fixture scope**:
   - Use `autouse=True` for automatic application
   - Or apply to specific test files

### Option 2: ServiceRegistry Setup

**If registration happens in ServiceRegistry init**:

1. **Modify ServiceRegistry**:
   - Add LLM service to default registrations
   - Ensure test environment gets LLM service

2. **Or create test-specific registry**:
   - `tests/test_service_registry.py`
   - Pre-configure for tests

### Option 3: Mock LLM Service

**If real LLM service not needed in tests**:

1. **Create mock LLM service**:
   ```python
   class MockLLMService:
       async def classify(self, text):
           return {"category": "QUERY", "confidence": 1.0}
   ```

2. **Register mock in fixtures**:
   - Same fixture approach as Option 1
   - Use mock instead of real service

---

## Testing Strategy

### After Implementation

1. **Run previously failing tests**:
   ```bash
   # Direct interface tests
   pytest tests/intent/test_direct_interface.py -v
   
   # Contract tests
   pytest tests/intent/contracts/ -v
   ```

2. **Verify all 49 tests now pass**:
   ```bash
   # Count should be 49/49
   pytest tests/intent/test_direct_interface.py tests/intent/contracts/ --tb=no -q
   ```

3. **Ensure no regression**:
   ```bash
   # All intent tests
   pytest tests/intent/ -v
   ```

### Success Criteria

- [ ] 8 Direct Interface tests pass (was 6/14, should be 14/14)
- [ ] 41 Contract tests pass (was 29/70, should be 70/70)
- [ ] Total: 49 additional tests passing
- [ ] No regression in other tests
- [ ] Solution documented

---

## Deliverables

### Code Changes

**Files to Modify** (likely):
- `tests/conftest.py` (or create if doesn't exist)
- OR `tests/intent/conftest.py`
- OR `services/service_registry.py`

### Documentation

**Create**: `dev/2025/10/12/llm-service-registration-fix.md`

**Contents**:
- Problem description
- Root cause analysis
- Solution implemented
- Test results (before/after)
- Registration pattern documented

---

## Duration Estimate (For PM Planning Only)

**Estimated Duration**: 1-2 hours
- Investigation: 30-45 minutes
- Implementation: 20-30 minutes
- Testing: 15-30 minutes
- Documentation: 15-20 minutes

**Important**: Planning estimate only, not a constraint. Quality takes as long as quality takes.

---

## Progress Milestones

**Report to PM after**:
- Investigation complete (understanding achieved)
- Implementation complete (code ready)
- Tests passing (49 tests unblocked)
- Issues (if any complications discovered)

---

## STOP Conditions

**Stop and report to PM if**:
- ServiceRegistry architecture unclear
- LLM service location uncertain
- Registration pattern not obvious
- Solution requires architectural changes
- Tests still failing after reasonable attempts

**Don't stop for**:
- Need time to study codebase
- Testing taking time to verify
- Multiple approaches to evaluate
- Documentation thoroughness

---

## Notes

### Why This Matters

**These 49 tests validate**:
- Accuracy contracts (classification working)
- Bypass contracts (enforcement working)
- Error contracts (error handling working)
- Multiuser contracts (user context working)
- Performance contracts (benchmarks met)

**Without LLM service**, these contracts can't be verified.

### Quality Standards

- Follow existing patterns (don't invent new approaches)
- Understand before implementing
- Test thoroughly
- Document clearly
- No shortcuts

---

**LLM Registration Fix Prompt Created**: October 12, 2025, 9:24 AM  
**Agent**: Code Agent authorized to proceed  
**Goal**: 143/143 tests passing (100%)  
**Next**: Phase 2 (Evidence Collection) after LLM fix complete
