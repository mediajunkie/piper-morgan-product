# Prompt for Code Agent: GREAT-5 Phase 3 - Integration Tests for Critical Flows

## Context

GREAT-5 mission: Establish essential quality gates to prevent regression and maintain excellent performance from GREAT-1 through GREAT-4.

**This is Phase 3**: Create integration tests for critical user flows, testing end-to-end functionality.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-1535-prog-code-log.md`

## Mission

Create integration tests for the most critical user flows:
1. Intent classification flow (all 13 categories)
2. Multi-user context isolation
3. Error recovery and graceful degradation
4. End-to-end canonical handler flows

---

## Background

**From GREAT-4**: Intent system has 13 categories, 4 interfaces, complex orchestration

**Current test coverage**:
- 142+ tests for intent system
- 10 zero-tolerance regression tests (Phase 1)
- 4 performance benchmarks (Phase 2)

**Gap**: No comprehensive end-to-end integration tests for critical user flows

**Goal**: Alpha-appropriate integration tests (not exhaustive, focus on critical paths)

---

## Task 1: Create Integration Test Suite

### File Structure

Create: `tests/integration/test_critical_flows.py`

### Test Categories

**1. Intent Classification Flow** (Priority: HIGH)
- User input → Intent classification → Handler selection → Response
- Test all 13 intent categories at least once
- Verify correct handler invoked
- Verify response structure valid

**2. Multi-User Context Isolation** (Priority: HIGH)
- User A and User B make requests
- Verify User A's context doesn't leak to User B
- Verify session isolation working

**3. Error Recovery** (Priority: MEDIUM)
- Invalid input → Graceful error response
- Service unavailable → Fallback behavior
- Timeout → Proper error message

**4. Canonical Handler Flows** (Priority: HIGH)
- IDENTITY: "who are you" → bot identity response
- TEMPORAL: "show my calendar" → calendar response or proper error
- STATUS: "what's my status" → status response or proper error
- PRIORITY: "my priorities" → priority response or proper error
- GUIDANCE: "how do I..." → guidance response

---

## Task 2: Implement Integration Tests

### Template Structure

```python
"""
Integration Tests for Critical User Flows

Tests end-to-end functionality of the most important user paths.
Alpha-appropriate scope - covers critical flows without over-engineering.

Based on:
- GREAT-4 intent system (13 categories, 4 interfaces)
- GREAT-4E validation (142+ tests)
- GREAT-5 quality gates (zero-tolerance, performance)
"""

import pytest
from fastapi.testclient import TestClient

class TestIntentClassificationFlow:
    """
    Test complete intent classification flow for all 13 categories.

    Flow: User input → Classification → Handler → Response
    """

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    # Canonical categories (5)

    def test_identity_flow(self, client):
        """IDENTITY: who are you → bot identity"""
        response = client.post("/api/v1/intent", json={"message": "who are you"})
        assert response.status_code == 200
        data = response.json()
        assert "category" in data or "response" in data
        # Verify identity-related response

    def test_temporal_flow(self, client):
        """TEMPORAL: show my calendar → calendar response"""
        response = client.post("/api/v1/intent", json={"message": "show my calendar"})
        assert response.status_code in [200, 422]  # 422 if calendar not configured
        # Not 500 - must handle gracefully

    def test_status_flow(self, client):
        """STATUS: what's my status → status response"""
        response = client.post("/api/v1/intent", json={"message": "what's my status"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_priority_flow(self, client):
        """PRIORITY: my priorities → priority response"""
        response = client.post("/api/v1/intent", json={"message": "show my priorities"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_guidance_flow(self, client):
        """GUIDANCE: how do I... → guidance response"""
        response = client.post("/api/v1/intent", json={"message": "how do I create a PR"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    # Workflow categories (8)

    def test_execution_flow(self, client):
        """EXECUTION: create issue → execution workflow"""
        response = client.post("/api/v1/intent", json={"message": "create a github issue"})
        assert response.status_code in [200, 422]
        # May require auth/config, but should not crash

    def test_analysis_flow(self, client):
        """ANALYSIS: analyze project → analysis workflow"""
        response = client.post("/api/v1/intent", json={"message": "analyze our project status"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_synthesis_flow(self, client):
        """SYNTHESIS: summarize → synthesis workflow"""
        response = client.post("/api/v1/intent", json={"message": "summarize recent updates"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_strategy_flow(self, client):
        """STRATEGY: planning query → strategy workflow"""
        response = client.post("/api/v1/intent", json={"message": "plan our next sprint"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_learning_flow(self, client):
        """LEARNING: teach/explain → learning workflow"""
        response = client.post("/api/v1/intent", json={"message": "explain how caching works"})
        assert response.status_code in [200, 422]
        # Not 500 - must handle gracefully

    def test_conversation_flow(self, client):
        """CONVERSATION: casual chat → conversation workflow"""
        response = client.post("/api/v1/intent", json={"message": "how are you doing"})
        assert response.status_code == 200
        # Conversation should always work

    def test_query_flow(self, client):
        """QUERY: generic question → query workflow (fallback)"""
        response = client.post("/api/v1/intent", json={"message": "what is the meaning of life"})
        assert response.status_code in [200, 422]
        # QUERY has fallback from GREAT-4F - should not timeout

    def test_unknown_flow(self, client):
        """UNKNOWN: unclear input → unknown workflow"""
        response = client.post("/api/v1/intent", json={"message": "asdfghjkl"})
        assert response.status_code in [200, 422]
        # Should handle gracefully even if unclear


class TestMultiUserIsolation:
    """
    Test that multi-user context isolation works correctly.

    From GREAT-4C: Multi-user context support implemented.
    Verify User A's context doesn't leak to User B.
    """

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    def test_session_isolation(self, client):
        """Different sessions should have isolated context"""
        # User A request
        response_a = client.post(
            "/api/v1/intent",
            json={"message": "my name is Alice"},
            headers={"X-Session-ID": "session-a"}
        )
        assert response_a.status_code in [200, 422]

        # User B request
        response_b = client.post(
            "/api/v1/intent",
            json={"message": "what is my name"},
            headers={"X-Session-ID": "session-b"}
        )
        assert response_b.status_code in [200, 422]

        # User B should NOT know Alice's name
        # (This is basic isolation test - full testing would require mocks)

    def test_concurrent_users(self, client):
        """Multiple users can use system concurrently"""
        # Send requests from 3 different users
        for user_id in ["user-1", "user-2", "user-3"]:
            response = client.post(
                "/api/v1/intent",
                json={"message": "who are you"},
                headers={"X-Session-ID": user_id}
            )
            assert response.status_code == 200
            # All should get valid responses independently


class TestErrorRecovery:
    """
    Test graceful error handling and recovery.

    System should degrade gracefully, never crash.
    """

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    def test_invalid_json(self, client):
        """Invalid JSON should return 422, not 500"""
        response = client.post(
            "/api/v1/intent",
            data="not valid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
        # Validation error, not server crash

    def test_missing_message(self, client):
        """Missing message field should return 422"""
        response = client.post("/api/v1/intent", json={})
        assert response.status_code == 422
        # Validation error, not server crash

    def test_empty_message(self, client):
        """Empty message should be handled gracefully"""
        response = client.post("/api/v1/intent", json={"message": ""})
        assert response.status_code in [200, 422]
        # Either handle empty or validate, but don't crash

    def test_very_long_message(self, client):
        """Very long message should be handled gracefully"""
        long_message = "word " * 10000  # 50K characters
        response = client.post("/api/v1/intent", json={"message": long_message})
        assert response.status_code in [200, 422]
        # Either process or reject, but don't crash


class TestCanonicalHandlerIntegration:
    """
    Test canonical handlers end-to-end.

    From GREAT-4F: Canonical handlers are fast-path (1ms, 600K+ req/sec).
    Verify they work correctly in integration.
    """

    @pytest.fixture
    def client(self):
        from web.app import app
        return TestClient(app)

    def test_identity_handler_response(self, client):
        """IDENTITY handler returns valid bot identity"""
        response = client.post("/api/v1/intent", json={"message": "what can you do"})
        assert response.status_code == 200

        data = response.json()
        # Should contain bot identity/capabilities info
        # Exact structure may vary, just verify it's a valid response
        assert data is not None
        assert isinstance(data, dict)

    def test_temporal_handler_response(self, client):
        """TEMPORAL handler provides calendar info or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "what's on my schedule today"})
        assert response.status_code in [200, 422]

        # If 422, should explain calendar not configured
        # If 200, should return calendar data

    def test_status_handler_response(self, client):
        """STATUS handler provides work status or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "show my standup"})
        assert response.status_code in [200, 422]

        # Should either provide status or explain not configured

    def test_priority_handler_response(self, client):
        """PRIORITY handler provides priorities or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "what should I focus on"})
        assert response.status_code in [200, 422]

        # Should either provide priorities or explain not configured
```

---

## Task 3: Run Integration Tests

### Execute Tests

```bash
# Run new integration tests
pytest tests/integration/test_critical_flows.py -v

# Expected: Most tests pass
# Some may be 422 if services not fully configured in test env
# None should be 500 (server crash)
```

### Document Results

Record:
- Total tests created
- Tests passing
- Tests failing (with reasons)
- Any 500 errors found (these are bugs!)

---

## Task 4: Document Integration Test Coverage

Create: `dev/2025/10/07/great5-phase3-integration-tests.md`

Include:
- Integration test suite created
- Critical flows covered
- Test results (pass/fail breakdown)
- Coverage by category (all 13 intents tested)
- Multi-user isolation verified
- Error recovery validated
- Any issues found and fixed

---

## Success Criteria

- [ ] Integration test suite created (`tests/integration/test_critical_flows.py`)
- [ ] All 13 intent categories tested (at least once each)
- [ ] Multi-user isolation tested (2+ test cases)
- [ ] Error recovery tested (4+ test cases)
- [ ] Canonical handlers tested (5 handlers)
- [ ] All tests run successfully (0 crashes/500 errors)
- [ ] Results documented
- [ ] Session log updated

---

## Critical Notes

- **Alpha-appropriate**: One test per category is sufficient, not exhaustive
- **Focus on crashes**: 500 errors are bugs, 422 validation errors are OK
- **Graceful degradation**: Services may not be configured, tests should handle this
- **No mocks needed**: Use TestClient with real system (integration test approach)
- **Document issues**: Any 500 errors found should be documented as bugs

---

## STOP Conditions

- If >3 categories return 500 errors, document and ask PM (integration broken)
- If multi-user isolation fails, document and ask PM (GREAT-4C regression)
- If tests can't run due to missing dependencies, document and ask PM

---

**Effort**: Medium (~45-60 minutes)
**Priority**: HIGH (validates critical flows)
**Deliverable**: Integration test suite covering all critical user flows
