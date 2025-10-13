# Investigation: Testing Regime Blind Spots & Import Failures

## Context
GREAT-4E-2 Phase 3 revealed critical testing gaps:
- Broken imports didn't fail tests
- Missing /health endpoint went undetected
- Tests allow 404 for critical endpoints
- No recent commits explain these issues

## Your Task
Conduct thorough investigation of testing blind spots and create action plan for comprehensive regression testing.

## Investigation Requirements

### 1. Test Execution Audit

**Check actual test execution with PYTHONPATH**:
```bash
# Use the ACTUAL test command pattern from our codebase
PYTHONPATH=. python -m pytest tests/intent/ -v 2>&1 | tee test_output.log

# Check for import errors that pytest might hide
grep -i "error\|import\|fail" test_output.log

# Check pytest collection summary
grep "collected" test_output.log

# Look for skipped tests
grep -i "skip" test_output.log
```

Document:
- How many tests actually run vs exist
- Any hidden import errors
- Any silently skipped tests

### 2. Import Error Detection

**Test if pytest catches import errors**:
```python
# Create intentionally broken test file
# dev/2025/10/06/test_import_detection.py
import sys
sys.path.insert(0, '.')

# Test 1: Can we import web.app?
try:
    from web.app import app
    print("✅ web.app imports successfully")
except ImportError as e:
    print(f"❌ web.app import fails: {e}")

# Test 2: Do tests actually use web.app?
import subprocess
result = subprocess.run(
    ["grep", "-r", "from web.app import", "tests/"],
    capture_output=True, text=True
)
print(f"Tests importing web.app:\n{result.stdout}")
```

### 3. Health Endpoint Mystery

**Find when /health disappeared**:
```bash
# Check entire git history for /health endpoint
git log -p --all -S "@app.get\(\"/health\"\)" -- "*.py"

# Find when it was removed (if ever existed)
git log --diff-filter=D --summary | grep -B 10 "health"

# Check if it exists elsewhere
find . -name "*.py" -exec grep -l "@app.get.*health" {} \;
```

**Investigate why tests accept 404**:
```bash
# Find all tests that check /health
grep -r "/health" tests/ --include="*.py" -A 2 -B 2

# Find tests that allow 404
grep -r "\[200, 404\]\|404.*200" tests/ --include="*.py"
```

Document:
- When /health last existed (if ever)
- Why tests were written to accept 404
- Whether this pattern exists for other endpoints

### 4. Mock Usage Audit

**Identify over-mocking that hides issues**:
```bash
# Find all mock usage
grep -r "mock\|Mock\|patch" tests/ --include="*.py" | wc -l

# Find mocked imports
grep -r "@patch\|mock.*import" tests/ --include="*.py"

# Find mocked web.app
grep -r "mock.*web\.app\|patch.*web\.app" tests/ --include="*.py"
```

Create list of:
- Tests that mock critical imports
- Tests that mock web.app
- Tests that might pass regardless of actual code

### 5. Silent Failure Patterns

**Identify tests that can't fail**:
```python
# Search for anti-patterns
patterns = [
    "except.*pass",  # Silently swallowing exceptions
    "assert.*or.*True",  # Always-true assertions
    "if.*else.*pass",  # Conditional passes
    "try.*except.*continue",  # Skipping on error
    "pytest.skip",  # Skipped tests
]

for pattern in patterns:
    print(f"\n=== {pattern} ===")
    # grep for each pattern
```

### 6. Regression Test Plan

Create comprehensive test plan that:
- Runs with NO mocks for critical paths
- Fails immediately on import errors
- Validates all endpoints exist
- Has no "acceptable failure" states

**Template for new regression suite**:
```python
# tests/regression/test_no_mocks.py
"""Regression tests that use NO mocks and NO silent failures"""

import pytest
import sys
import importlib

def test_critical_imports():
    """All critical imports must work"""
    critical_modules = [
        "web.app",
        "services.intent_service",
        "services.orchestration.engine",
    ]

    for module in critical_modules:
        try:
            importlib.import_module(module)
        except ImportError as e:
            pytest.fail(f"Critical import failed: {module} - {e}")

def test_all_endpoints_exist():
    """All documented endpoints must exist"""
    from web.app import app

    required_endpoints = [
        ("/health", "GET"),
        ("/api/v1/intent", "POST"),
        # ... complete list
    ]

    routes = {(r.path, list(r.methods)[0]) for r in app.routes}

    for endpoint, method in required_endpoints:
        assert (endpoint, method) in routes, f"Missing: {method} {endpoint}"

def test_health_endpoint_returns_200():
    """Health check must return 200, never 404"""
    from fastapi.testclient import TestClient
    from web.app import app

    client = TestClient(app)
    response = client.get("/health")

    # NO allowing 404!
    assert response.status_code == 200, "Health check must return 200"
```

## Deliverables

1. **Testing Blind Spots Report**
   - List all identified gaps
   - Explain why tests passed despite issues
   - Count of affected tests

2. **Import Error Analysis**
   - Can pytest detect import errors?
   - Are import errors being hidden?
   - How to make them visible

3. **Historical Timeline**
   - When /health disappeared
   - Why tests allow 404
   - Other missing endpoints

4. **Regression Test Suite Design**
   - No mocks for critical paths
   - No silent failures
   - No "acceptable" error states
   - Clear pass/fail criteria

5. **Recommendations for GREAT-5**
   - Complete regression testing epic
   - Fix all blind spots
   - Implement proper test gates

## Success Criteria

- Understand why import errors didn't fail tests
- Know when /health was removed
- Have plan to prevent future blind spots
- Design regression suite with zero tolerance for failures

---

*Time estimate: 1-2 hours investigation*
