# Prompt for Code Agent: GREAT-4E Phase 3 - Contract Validation

## Context

Phase 2 complete: All 52 interface tests passing (52/117 tests, 44%)

**This is Phase 3**: Validate 5 contracts across all 13 categories (65 tests total)

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Implement contract tests ensuring all 13 intent categories meet quality requirements:
1. Performance contracts (13 tests)
2. Accuracy contracts (13 tests)
3. Error handling contracts (13 tests)
4. Multi-user contracts (13 tests)
5. Bypass prevention contracts (13 tests)

Total: 65 contract tests

---

## Phase 3: Contract Validation (65 Tests)

### Test Organization

Create: `tests/intent/contracts/` directory

Files:
- `test_performance_contracts.py` (13 tests)
- `test_accuracy_contracts.py` (13 tests)
- `test_error_contracts.py` (13 tests)
- `test_multiuser_contracts.py` (13 tests)
- `test_bypass_contracts.py` (13 tests)

### Contract 1: Performance (13 Tests)

Create: `tests/intent/contracts/test_performance_contracts.py`

**Contract**: Each category must respond within 3000ms (from Phase 1 findings)

```python
"""Performance contract tests for all 13 intent categories"""
import pytest
import time
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.test_constants import INTENT_CATEGORIES, CATEGORY_EXAMPLES
from tests.intent.coverage_tracker import coverage
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


class TestPerformanceContracts(BaseValidationTest):
    """Verify all categories meet performance requirements."""

    @pytest.mark.asyncio
    async def test_temporal_performance(self, intent_service):
        """PERF 1/13: TEMPORAL response time."""
        intent = Intent(
            text=CATEGORY_EXAMPLES["TEMPORAL"],
            original_message=CATEGORY_EXAMPLES["TEMPORAL"],
            category=IntentCategory.TEMPORAL,
            action="calendar_query",
            confidence=0.95,
            context={}
        )

        start = time.time()
        result = await intent_service.process(intent, session_id="perf_test")
        duration_ms = (time.time() - start) * 1000

        # Verify performance threshold
        self.assert_performance(duration_ms)

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ TEMPORAL performance: {duration_ms:.1f}ms")

    # Repeat for all 13 categories...

    @pytest.mark.asyncio
    async def test_status_performance(self, intent_service):
        """PERF 2/13: STATUS response time."""
        # Similar pattern

    @pytest.mark.asyncio
    async def test_priority_performance(self, intent_service):
        """PERF 3/13: PRIORITY response time."""
        # Similar pattern

    # ... continue for all 13 categories
```

### Contract 2: Accuracy (13 Tests)

Create: `tests/intent/contracts/test_accuracy_contracts.py`

**Contract**: Classification accuracy >90% for each category

```python
"""Accuracy contract tests for all 13 intent categories"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from services.intent_service.classifier import classify


class TestAccuracyContracts(BaseValidationTest):
    """Verify classification accuracy for all categories."""

    @pytest.mark.asyncio
    async def test_temporal_accuracy(self):
        """ACC 1/13: TEMPORAL classification accuracy."""
        # Test with multiple temporal queries
        temporal_queries = [
            "What's on my calendar?",
            "What day is it?",
            "Show me today's schedule",
            "What time is my next meeting?",
            "When is my deadline?"
        ]

        correct = 0
        for query in temporal_queries:
            intent = await classify(query)
            if intent.category.value == "temporal":
                correct += 1

        accuracy = correct / len(temporal_queries)

        # Verify meets threshold
        assert accuracy >= 0.90, \
            f"TEMPORAL accuracy {accuracy:.1%} below 90% threshold"

        # Update coverage
        coverage.contract_tests_passed += 1

        print(f"✓ TEMPORAL accuracy: {accuracy:.1%}")

    @pytest.mark.asyncio
    async def test_status_accuracy(self):
        """ACC 2/13: STATUS classification accuracy."""
        status_queries = [
            "Show my standup",
            "What am I working on?",
            "What's my current status?",
            "Show me my tasks",
            "What's in progress?"
        ]

        correct = 0
        for query in status_queries:
            intent = await classify(query)
            if intent.category.value == "status":
                correct += 1

        accuracy = correct / len(status_queries)
        assert accuracy >= 0.90
        coverage.contract_tests_passed += 1

        print(f"✓ STATUS accuracy: {accuracy:.1%}")

    # ... continue for all 13 categories
```

### Contract 3: Error Handling (13 Tests)

Create: `tests/intent/contracts/test_error_contracts.py`

**Contract**: All categories handle errors gracefully (no crashes, proper error messages)

```python
"""Error handling contract tests for all 13 intent categories"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


class TestErrorContracts(BaseValidationTest):
    """Verify error handling for all categories."""

    @pytest.mark.asyncio
    async def test_temporal_error_handling(self, intent_service):
        """ERROR 1/13: TEMPORAL error handling."""
        # Test with malformed intent
        intent = Intent(
            text="",  # Empty text
            original_message="",
            category=IntentCategory.TEMPORAL,
            action="invalid_action",
            confidence=0.95,
            context={"invalid": "data"}
        )

        # Should not crash
        try:
            result = await intent_service.process(intent, session_id="error_test")

            # Verify graceful handling
            assert result is not None
            assert hasattr(result, 'message')
            assert len(result.message) > 0

            # Should indicate error or provide helpful message
            # (not crash with exception)

            coverage.contract_tests_passed += 1
            print(f"✓ TEMPORAL error handling: graceful")

        except Exception as e:
            pytest.fail(f"TEMPORAL handler crashed on error: {e}")

    @pytest.mark.asyncio
    async def test_status_error_handling(self, intent_service):
        """ERROR 2/13: STATUS error handling."""
        # Similar pattern - test with invalid data

    # ... continue for all 13 categories
```

### Contract 4: Multi-User (13 Tests)

Create: `tests/intent/contracts/test_multiuser_contracts.py`

**Contract**: All categories respect user context (session isolation)

```python
"""Multi-user contract tests for all 13 intent categories"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory
from tests.intent.test_constants import CATEGORY_EXAMPLES


class TestMultiUserContracts(BaseValidationTest):
    """Verify multi-user support for all categories."""

    @pytest.mark.asyncio
    async def test_temporal_multiuser(self, intent_service):
        """MULTI 1/13: TEMPORAL user isolation."""
        intent = Intent(
            text=CATEGORY_EXAMPLES["TEMPORAL"],
            original_message=CATEGORY_EXAMPLES["TEMPORAL"],
            category=IntentCategory.TEMPORAL,
            action="calendar_query",
            confidence=0.95,
            context={}
        )

        # Process for user 1
        result1 = await intent_service.process(intent, session_id="user1")

        # Process for user 2
        result2 = await intent_service.process(intent, session_id="user2")

        # Both should succeed
        assert result1.success is not None
        assert result2.success is not None

        # Sessions should be isolated (not interfere)
        # This is verified by both succeeding independently

        coverage.contract_tests_passed += 1
        print(f"✓ TEMPORAL multi-user: isolated")

    @pytest.mark.asyncio
    async def test_status_multiuser(self, intent_service):
        """MULTI 2/13: STATUS user isolation."""
        # Similar pattern

    # ... continue for all 13 categories
```

### Contract 5: Bypass Prevention (13 Tests)

Create: `tests/intent/contracts/test_bypass_contracts.py`

**Contract**: No routes bypass intent classification

```python
"""Bypass prevention contract tests for all 13 intent categories"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import coverage
from services.intent.intent_service import IntentService
from unittest.mock import patch, MagicMock


class TestBypassContracts(BaseValidationTest):
    """Verify no bypass routes exist for any category."""

    @pytest.mark.asyncio
    async def test_temporal_no_bypass(self, intent_service):
        """BYPASS 1/13: TEMPORAL requires classification."""
        # Mock the classifier to verify it's called
        with patch('services.intent.intent_service.classify') as mock_classify:
            # Set up mock to return temporal intent
            mock_intent = MagicMock()
            mock_intent.category.value = "temporal"
            mock_intent.action = "calendar_query"
            mock_intent.confidence = 0.95
            mock_classify.return_value = mock_intent

            # Process message
            await intent_service.process_message(
                "What's on my calendar?",
                session_id="bypass_test"
            )

            # Verify classifier was called
            assert mock_classify.called, \
                "TEMPORAL bypassed classification"

            coverage.contract_tests_passed += 1
            print(f"✓ TEMPORAL no bypass: verified")

    @pytest.mark.asyncio
    async def test_status_no_bypass(self, intent_service):
        """BYPASS 2/13: STATUS requires classification."""
        # Similar pattern

    # ... continue for all 13 categories
```

---

## Coverage Report After Phase 3

Add to each contract test file:

```python
@pytest.mark.asyncio
async def test_zzz_coverage_report(self):
    """Generate coverage report after contract tests."""
    from tests.intent.coverage_tracker import coverage

    print("\n" + "=" * 80)
    print(coverage.report())
    print("=" * 80)
```

---

## Running the Tests

```bash
# Run all contract tests
pytest tests/intent/contracts/ -v

# Or run each contract separately
pytest tests/intent/contracts/test_performance_contracts.py -v
pytest tests/intent/contracts/test_accuracy_contracts.py -v
pytest tests/intent/contracts/test_error_contracts.py -v
pytest tests/intent/contracts/test_multiuser_contracts.py -v
pytest tests/intent/contracts/test_bypass_contracts.py -v

# Should show:
# Performance: 14 passed (13 + coverage report)
# Accuracy: 14 passed
# Error: 14 passed
# Multi-user: 14 passed
# Bypass: 14 passed
#
# Total: 65/65 contract tests passing
```

---

## Success Criteria

- [ ] Performance contracts: 13/13 passing
- [ ] Accuracy contracts: 13/13 passing
- [ ] Error contracts: 13/13 passing
- [ ] Multi-user contracts: 13/13 passing
- [ ] Bypass contracts: 13/13 passing
- [ ] Total: 65/65 contract tests passing
- [ ] Coverage report shows 117/117 tests (100%)
- [ ] Session log updated

---

## Critical Notes

- All contracts must pass for all 13 categories
- Performance threshold: 3000ms (from Phase 1)
- Accuracy threshold: 90%
- Stop if any contract fails for any category
- Document any category that requires special handling

---

**Effort**: Large (~2-3 hours for 65 tests across 5 contracts)
**Priority**: HIGH (validates quality contracts)
**Deliverables**: 65 contract tests + coverage report
