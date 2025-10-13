# Prompt for Code Agent: GREAT-4F Phase 4 - Fix Permissive Tests

## Context

GREAT-4F mission: Fix permissive test assertions that accept 404 as valid response for health checks.

**This is Phase 4**: Fix tests that incorrectly accept `status_code in [200, 404]` for critical endpoints like `/health`.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-0730-prog-code-log.md`

## Mission

Find and fix all tests with permissive assertions that accept 404 as a valid response for endpoints that should ALWAYS return 200 (especially health checks).

---

## Background from Yesterday

**Discovery**: During GREAT-4E-2 Phase 3, found `/health` endpoint was missing entirely. Tests passed because they accepted `status_code in [200, 404]` as valid.

**PM Guidance**: "HUGE PROBLEMS - why would you accept 404 as a 'good' result from a health check endpoint?"

**Identified yesterday**:
1. `tests/intent/test_user_flows_complete.py:150`
2. `tests/integration/test_no_web_bypasses.py:44`
3. `tests/integration/test_no_web_bypasses.py:89`

**Gameplan STOP condition**: "More than 3 tests" with permissive patterns

---

## Task 1: Find All Permissive Tests

Search for problematic patterns:

```bash
# Find all permissive status code checks
grep -rn "status_code in \[200, 404\]" tests/
grep -rn "in \[200, 404\]" tests/

# Also check for variations
grep -rn "status.*200.*404" tests/
grep -rn "404.*acceptable\|404.*valid\|404.*ok" tests/
```

**Expected**: Should find the 3 tests identified yesterday, possibly others

**STOP if**: More than 3 tests found (gameplan condition) - document and ask PM

---

## Task 2: Analyze Each Permissive Test

For each test found, determine:

1. **What endpoint is being tested?**
   - Health checks → MUST be 200
   - Documentation endpoints → MIGHT accept 404
   - API endpoints → MUST be 200 or explicit error codes

2. **Why was 404 acceptable?**
   - Oversight?
   - Endpoint was optional at time of writing?
   - Test written before endpoint existed?

3. **What should the assertion be?**
   - Health checks: `assert response.status_code == 200`
   - Critical endpoints: `assert response.status_code == 200`
   - Optional endpoints: Document why 404 is acceptable OR make endpoint required

---

## Task 3: Fix Critical Tests

### Health Check Tests (HIGHEST PRIORITY)

For `/health` endpoint tests:

```python
# BEFORE (WRONG)
response = client.get("/health")
assert response.status_code in [200, 404]

# AFTER (CORRECT)
response = client.get("/health")
assert response.status_code == 200, "/health endpoint MUST return 200 for monitoring"
```

### Other Critical Endpoints

For any endpoint that should always exist:

```python
# BEFORE (WRONG)
response = client.get("/api/endpoint")
assert response.status_code in [200, 404]

# AFTER (CORRECT)
response = client.get("/api/endpoint")
assert response.status_code == 200, "Critical endpoint must always be available"
```

---

## Task 4: Verify Endpoints Exist

Before changing assertions, verify the endpoints actually exist:

```bash
# Check for /health endpoint
grep -n "def health" web/app.py
grep -n "@app.get.*health" web/app.py

# Check for other endpoints in tests
grep -n "def [endpoint_name]" web/app.py
```

**If endpoint doesn't exist**: DO NOT change test - document as separate issue for PM

---

## Task 5: Run Fixed Tests

After fixing assertions:

```bash
# Run the fixed tests
pytest tests/intent/test_user_flows_complete.py -v
pytest tests/integration/test_no_web_bypasses.py -v

# All should pass (endpoints exist and return 200)
```

**If tests fail**: Endpoint might not exist or not return 200 - document and ask PM

---

## Task 6: Document Changes

Create: `dev/2025/10/07/permissive-tests-fixed.md`

Include:
- How many tests had permissive assertions
- Which endpoints were affected
- What assertions were changed
- Why these changes are critical (monitoring, production readiness)
- Test results after fixes

---

## Success Criteria

- [ ] All permissive test patterns found (should be ≤3 per gameplan)
- [ ] Each test analyzed (endpoint type, why permissive, correct assertion)
- [ ] Health check tests fixed with strict `== 200` assertions
- [ ] Other critical endpoint tests fixed
- [ ] Endpoints verified to exist before changing tests
- [ ] All fixed tests passing
- [ ] Changes documented
- [ ] Session log updated

---

## Expected Fixes

Based on yesterday's investigation:

### 1. tests/intent/test_user_flows_complete.py:150
```python
# Likely testing exempt paths including /health
exempt_paths = [("/health", [200, 404]), ...]

# Fix to:
exempt_paths = [("/health", [200]), ...]  # Health must return 200
```

### 2. tests/integration/test_no_web_bypasses.py:44
```python
# Likely testing /health endpoint
response = client.get("/health")
assert response.status_code in [200, 404]

# Fix to:
response = client.get("/health")
assert response.status_code == 200, "/health must return 200"
```

### 3. tests/integration/test_no_web_bypasses.py:89
```python
# Similar pattern, possibly different endpoint
# Fix based on endpoint criticality
```

---

## Critical Notes

- Health checks MUST return 200 always (load balancers, monitoring depend on this)
- Don't change tests for endpoints that don't exist yet
- Permissive tests hide real problems (like missing /health endpoint yesterday)
- This is a production reliability fix, not just test cleanup

---

## STOP Conditions

- If >3 tests found with permissive patterns, document count and ask PM
- If endpoints don't exist for tests being fixed, document and ask PM
- If test changes cause failures, document and ask PM

---

**Effort**: Small (~15-30 minutes)
**Priority**: HIGH (production reliability)
**Deliverable**: Fixed tests with strict assertions for critical endpoints
