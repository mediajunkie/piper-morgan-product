# Prompt for Code Agent: GREAT-5 Phase 1 - Zero-Tolerance Regression Suite

## Context

GREAT-5 mission: Establish essential quality gates to prevent regression and maintain excellent performance from GREAT-1 through GREAT-4.

**This is Phase 1**: Create zero-tolerance regression suite and fix permissive test patterns.

## Session Log

Continue your existing log and note at this time that we are continuing the Great Refactor with its final epic, GREAT-5.

## Mission

1. Create regression test suite with zero tolerance for critical failures
2. Fix 14 permissive test patterns that accept 500 (server error) as valid outcome

---

## Background from Phase 0 Assessment

**Baseline documented**: `great5-phase0-baseline-assessment.md`

**Current state**:
- 142+ tests exist and passing
- 21 permissive patterns found (`status_code in [...]`)
- ~14 patterns need fixing (accepting 500 as valid)
- ~7 patterns acceptable (error handling, blocked access)

**From GREAT-4 discoveries**:
- Permissive tests hid missing /health endpoint
- Broken imports went undetected
- Need zero-tolerance tests for critical infrastructure

---

## Task 1: Create Zero-Tolerance Regression Suite

**File**: `tests/regression/test_critical_no_mocks.py`

### Structure

```python
"""
Zero-Tolerance Regression Suite

These tests MUST pass 100% - no exceptions, no skips, no permissive assertions.
Purpose: Catch critical infrastructure failures before they reach production.

Based on GREAT-4E-2 Phase 3 discoveries:
- Missing /health endpoint went undetected
- Broken imports (personality_integration) went undetected
- Permissive tests provided false confidence
"""

import pytest
import importlib
from fastapi.testclient import TestClient

class TestCriticalImports:
    """All critical service imports must work - no mocks allowed"""

    def test_web_app_imports(self):
        """Web application must import successfully"""
        try:
            from web import app
            assert app is not None, "web.app module imported but app is None"
        except ImportError as e:
            pytest.fail(f"Failed to import web.app: {e}")

    def test_intent_service_imports(self):
        """Intent service must import successfully"""
        try:
            from services.intent_service import IntentService
            assert IntentService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import IntentService: {e}")

    def test_orchestration_imports(self):
        """Orchestration engine must import successfully"""
        try:
            from services.orchestration.engine import OrchestrationEngine
            assert OrchestrationEngine is not None
        except ImportError as e:
            pytest.fail(f"Failed to import OrchestrationEngine: {e}")

    def test_all_critical_services_importable(self):
        """Verify all critical service modules import"""
        critical_modules = [
            "services.github_service",
            "services.standup_service",
            "services.calendar_service",
            "services.llm.llm_service",
            "web.personality_integration",  # This broke in GREAT-4E-2
        ]

        failed = []
        for module_name in critical_modules:
            try:
                module = importlib.import_module(module_name)
                assert module is not None, f"{module_name} imported but is None"
            except Exception as e:
                failed.append(f"{module_name}: {e}")

        if failed:
            pytest.fail(f"Failed to import critical modules:\n" + "\n".join(failed))


class TestCriticalEndpoints:
    """All critical endpoints must exist and return correct status codes"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from web.app import app
        return TestClient(app)

    def test_health_endpoint_exists(self, client):
        """Health endpoint MUST exist and return 200 - NEVER 404"""
        response = client.get("/health")
        assert response.status_code == 200, (
            f"/health endpoint MUST return 200 (got {response.status_code}). "
            "This endpoint is critical for load balancers and monitoring. "
            "Missing or broken /health will cause service to be removed from rotation."
        )

    def test_health_response_structure(self, client):
        """Health endpoint must return expected structure"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data, "Health response missing 'status' field"
        assert data["status"] == "healthy", f"Health status is '{data['status']}', expected 'healthy'"
        assert "services" in data, "Health response missing 'services' field"

    def test_intent_endpoint_exists(self, client):
        """Intent endpoint must exist"""
        response = client.post("/api/v1/intent", json={"message": "test"})
        # Should return 200 or 422 (validation), but NEVER 404
        assert response.status_code != 404, (
            "/api/v1/intent endpoint does not exist (404). "
            "This is the core entry point for intent classification."
        )

    def test_monitoring_endpoints_exist(self, client):
        """Monitoring endpoints from GREAT-4E-2 must exist"""
        monitoring_endpoints = [
            "/api/admin/intent-monitoring",
            "/api/admin/intent-cache-metrics",
        ]

        for endpoint in monitoring_endpoints:
            response = client.get(endpoint)
            assert response.status_code != 404, (
                f"{endpoint} does not exist (404). "
                "This endpoint is required for production monitoring."
            )


class TestNoBypassRoutes:
    """Verify intent enforcement from GREAT-4B - no routes should bypass intent layer"""

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    def test_direct_service_routes_blocked(self, client):
        """Direct service access routes should not exist"""
        # These routes should NOT exist - all access goes through intent
        blocked_routes = [
            "/github/create-issue",
            "/calendar/get-events",
            "/standup/generate",
        ]

        for route in blocked_routes:
            response = client.post(route, json={})
            assert response.status_code in [404, 405], (
                f"Route {route} should not exist or should reject direct access. "
                f"All service access must go through intent classification layer. "
                f"Got status {response.status_code}"
            )


class TestCanonicalHandlers:
    """Canonical handlers from GREAT-4 must be accessible"""

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    def test_identity_intent_works(self, client):
        """IDENTITY intent must work (canonical handler)"""
        response = client.post("/api/v1/intent", json={"message": "who are you"})
        assert response.status_code == 200, (
            f"IDENTITY intent failed with {response.status_code}. "
            "Canonical handlers must always work."
        )

    def test_temporal_intent_works(self, client):
        """TEMPORAL intent must work (canonical handler)"""
        response = client.post("/api/v1/intent", json={"message": "show my calendar"})
        assert response.status_code in [200, 422], (
            f"TEMPORAL intent failed with {response.status_code}. "
            "Should return 200 or 422 (if calendar not configured)."
        )
```

### Verification

After creating tests:

```bash
# Run regression suite
pytest tests/regression/test_critical_no_mocks.py -v --tb=short

# Should show multiple tests passing
# If any fail, critical infrastructure is broken
```

---

## Task 2: Fix Permissive Test Patterns

### Patterns to Fix (14 instances)

Based on Phase 0 assessment, these files have problematic patterns:

1. **tests/intent/test_integration_complete.py** (1 instance)
2. **tests/intent/test_user_flows_complete.py** (8 instances)
3. **tests/intent/test_no_web_bypasses.py** (1 instance - /docs)
4. **tests/intent/test_bypass_prevention.py** (1 instance)
5. **tests/intent/test_enforcement_integration.py** (2 instances)
6. **tests/regression/test_critical_no_mocks.py** (1 instance - if exists)

### Analysis Required

For each permissive pattern, determine:

**1. Is 500 (server error) actually acceptable?**
- NO for: Health checks, canonical handlers, critical paths
- MAYBE for: Error handling tests, edge case tests

**2. What should the assertion be?**
```python
# BEFORE (permissive)
assert response.status_code in [200, 422, 500]

# AFTER (strict) - if endpoint should work
assert response.status_code == 200, "Endpoint must return success"

# AFTER (strict) - if validation expected
assert response.status_code in [200, 422], "Should succeed or validate, not error"
```

### Fix Strategy

**Step 1**: Review each file and understand test context

**Step 2**: Fix patterns by category:

**Category A: Critical Endpoints** (STRICT)
```python
# Health checks, monitoring, canonical handlers
assert response.status_code == 200
```

**Category B: User Input Validation** (MODERATE)
```python
# May have validation errors but should not crash
assert response.status_code in [200, 422]
# 200 = success, 422 = validation error
# NOT 500 = server crash
```

**Category C: Error Handling Tests** (PERMISSIVE - OK)
```python
# Tests that specifically test error conditions
assert response.status_code in [400, 422, 500]
# This is OK - testing error handling explicitly
```

**Step 3**: Document changes in summary file

---

## Task 3: Document Changes

Create: `dev/2025/10/07/great5-phase1-regression-suite.md`

Include:
- Regression test suite created (test count, coverage)
- Permissive patterns fixed (count, files affected)
- Analysis of each change (why it's now stricter)
- Test results (all regression tests passing)
- Impact (what failures would now be caught)

---

## Success Criteria

- [ ] Regression suite created with 10+ zero-tolerance tests
- [ ] All critical imports tested (web.app, services, orchestration)
- [ ] All critical endpoints tested (/health, /api/v1/intent, monitoring)
- [ ] Intent enforcement verified (no bypass routes)
- [ ] Canonical handlers validated (IDENTITY, TEMPORAL work)
- [ ] 14 permissive patterns fixed or justified
- [ ] All regression tests passing (100%)
- [ ] Changes documented
- [ ] Session log updated

---

## Critical Notes

- **Zero tolerance**: Regression tests MUST pass 100% - no skips, no permissive assertions
- **No mocks**: Use real system to catch real failures (learned from GREAT-4E-2)
- **Be strict**: Only accept 500 if test explicitly testing error handling
- **Document reasoning**: Explain why each pattern changed
- **Test first**: Run regression suite before fixing patterns to see current state

---

## STOP Conditions

- If regression suite reveals currently broken infrastructure, document and ask PM
- If >20 permissive patterns found (Phase 0 found 14), document scope and ask PM
- If tests can't run without major refactoring, document and ask PM

---

**Effort**: Medium (~1-1.5 hours)
**Priority**: HIGH (foundation for quality gates)
**Deliverable**: Zero-tolerance regression suite + fixed permissive tests
