# Prompt for Code Agent: GREAT-4E Phase 0 - Test Infrastructure Setup

## Context

Phase -1 confirmed:
- 13 intent categories exist and have handlers
- 4 interfaces exist (Web, Slack, CLI, Direct)
- Scope: 52 interface tests + 65 contract tests + 6 documents
- Estimated: 4-6 hours total

**This is Phase 0**: Set up test infrastructure before validation begins

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Create test framework for systematic validation of all 13 intent categories through all 4 interfaces.

---

## Phase 0: Test Infrastructure Setup

### Task 1: Create Test Constants

Create: `tests/intent/test_constants.py`

```python
"""Test constants for GREAT-4E validation"""

# All 13 intent categories - ENUMERATE EXPLICITLY
INTENT_CATEGORIES = [
    "TEMPORAL",
    "STATUS",
    "PRIORITY",
    "IDENTITY",
    "GUIDANCE",
    "EXECUTION",
    "ANALYSIS",
    "SYNTHESIS",
    "STRATEGY",
    "LEARNING",
    "UNKNOWN",
    "QUERY",
    "CONVERSATION",
]

# All 4 interfaces - ENUMERATE EXPLICITLY
INTERFACES = [
    "web",
    "slack",
    "cli",
    "direct",
]

# Expected test counts
CATEGORY_COUNT = 13
INTERFACE_COUNT = 4
INTERFACE_TESTS = CATEGORY_COUNT * INTERFACE_COUNT  # 52
CONTRACT_TESTS = CATEGORY_COUNT * 5  # 65 (5 contracts per category)
TOTAL_TESTS = INTERFACE_TESTS + CONTRACT_TESTS  # 117

# Example queries for each category
CATEGORY_EXAMPLES = {
    "TEMPORAL": "What's on my calendar today?",
    "STATUS": "Show me my current standup status",
    "PRIORITY": "What's my top priority right now?",
    "IDENTITY": "Who are you and what do you do?",
    "GUIDANCE": "What should I focus on next?",
    "EXECUTION": "Create a GitHub issue about testing",
    "ANALYSIS": "Analyze recent commits in the repo",
    "SYNTHESIS": "Generate a summary of this document",
    "STRATEGY": "Help me plan the next sprint",
    "LEARNING": "What patterns do you see in my work?",
    "UNKNOWN": "Blarghhh fuzzbucket",
    "QUERY": "What's the weather in San Francisco?",
    "CONVERSATION": "Hey, how's it going?",
}

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    "max_response_time_ms": 100,
    "min_classification_accuracy": 0.90,
    "min_cache_hit_rate": 0.80,
}
```

### Task 2: Create Coverage Tracker

Create: `tests/intent/coverage_tracker.py`

```python
"""Track test coverage for GREAT-4E validation"""
from typing import Dict, Set
from dataclasses import dataclass
from test_constants import CATEGORY_COUNT, INTERFACE_COUNT, INTERFACE_TESTS, CONTRACT_TESTS

@dataclass
class CoverageStats:
    categories_tested: Set[str]
    interfaces_tested: Set[str]
    interface_tests_passed: int
    contract_tests_passed: int

    @property
    def category_coverage(self) -> float:
        return len(self.categories_tested) / CATEGORY_COUNT

    @property
    def interface_coverage(self) -> float:
        return len(self.interfaces_tested) / INTERFACE_COUNT

    @property
    def interface_test_coverage(self) -> float:
        return self.interface_tests_passed / INTERFACE_TESTS

    @property
    def contract_test_coverage(self) -> float:
        return self.contract_tests_passed / CONTRACT_TESTS

    @property
    def total_coverage(self) -> float:
        total_possible = INTERFACE_TESTS + CONTRACT_TESTS
        total_passed = self.interface_tests_passed + self.contract_tests_passed
        return total_passed / total_possible

    def report(self) -> str:
        """Generate coverage report."""
        return f"""
GREAT-4E Coverage Report
========================
Categories:    {len(self.categories_tested)}/{CATEGORY_COUNT} ({self.category_coverage:.0%})
Interfaces:    {len(self.interfaces_tested)}/{INTERFACE_COUNT} ({self.interface_coverage:.0%})
Interface Tests: {self.interface_tests_passed}/{INTERFACE_TESTS} ({self.interface_test_coverage:.0%})
Contract Tests:  {self.contract_tests_passed}/{CONTRACT_TESTS} ({self.contract_test_coverage:.0%})
TOTAL:         {self.interface_tests_passed + self.contract_tests_passed}/{INTERFACE_TESTS + CONTRACT_TESTS} ({self.total_coverage:.0%})
"""

# Global tracker instance
coverage = CoverageStats(
    categories_tested=set(),
    interfaces_tested=set(),
    interface_tests_passed=0,
    contract_tests_passed=0,
)
```

### Task 3: Create Base Test Class

Create: `tests/intent/base_validation_test.py`

```python
"""Base test class for GREAT-4E validation"""
import pytest
from typing import Dict, Any
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory
from test_constants import CATEGORY_EXAMPLES, PERFORMANCE_THRESHOLDS
from coverage_tracker import coverage


class BaseValidationTest:
    """Base class for intent validation tests."""

    @pytest.fixture
    def intent_service(self):
        return IntentService()

    async def validate_category(
        self,
        category: str,
        interface: str,
        intent_service: IntentService
    ) -> Dict[str, Any]:
        """
        Validate a category through a specific interface.

        Returns validation results.
        """
        example_query = CATEGORY_EXAMPLES[category]

        # Track coverage
        coverage.categories_tested.add(category)
        coverage.interfaces_tested.add(interface)

        # Test will be implemented by subclass
        return {
            "category": category,
            "interface": interface,
            "example": example_query,
            "tested": True,
        }

    def assert_no_placeholder(self, message: str):
        """Verify no placeholder messages."""
        assert "Phase 3" not in message
        assert "full orchestration workflow" not in message
        assert "placeholder" not in message.lower()

    def assert_performance(self, duration_ms: float):
        """Verify performance threshold."""
        threshold = PERFORMANCE_THRESHOLDS["max_response_time_ms"]
        assert duration_ms < threshold, \
            f"Response time {duration_ms}ms exceeds threshold {threshold}ms"
```

### Task 4: Create Test Stub Generator

Create: `dev/2025/10/06/generate_test_stubs.py`

```python
"""Generate test stubs for all 52 interface tests"""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.intent.test_constants import INTENT_CATEGORIES, INTERFACES


def generate_interface_test_stubs():
    """Generate test file stubs for each interface."""

    for interface in INTERFACES:
        filename = f"tests/intent/test_{interface}_interface.py"

        content = f'''"""
Test {interface.upper()} interface for all 13 intent categories - GREAT-4E
"""
import pytest
from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.test_constants import INTENT_CATEGORIES
from tests.intent.coverage_tracker import coverage


class Test{interface.title()}Interface(BaseValidationTest):
    """Test all 13 categories through {interface.upper()} interface."""
'''

        for i, category in enumerate(INTENT_CATEGORIES, 1):
            content += f'''
    @pytest.mark.asyncio
    async def test_{category.lower()}_{interface}(self, intent_service):
        """{interface.upper()} {i}/13: {category} category."""
        result = await self.validate_category(
            "{category}",
            "{interface}",
            intent_service
        )

        # Verify no placeholder
        # Verify proper routing
        # Verify response valid

        # Update coverage
        coverage.interface_tests_passed += 1

        assert result["tested"] is True
'''

        print(f"Generated: {filename}")
        print(f"  Tests: {len(INTENT_CATEGORIES)}")

    print(f"\nTotal interface tests: {len(INTERFACES) * len(INTENT_CATEGORIES)}")


if __name__ == "__main__":
    generate_interface_test_stubs()
```

Run generator:
```bash
PYTHONPATH=. python3 dev/2025/10/06/generate_test_stubs.py
```

### Task 5: Document Test Plan

Create: `dev/2025/10/06/great4e-test-plan.md`

```markdown
# GREAT-4E Test Plan

## Test Coverage Matrix

| Category | Web | Slack | CLI | Direct | Total |
|----------|-----|-------|-----|--------|-------|
| TEMPORAL | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| STATUS   | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| PRIORITY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| IDENTITY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| GUIDANCE | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| EXECUTION| [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| ANALYSIS | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| SYNTHESIS| [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| STRATEGY | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| LEARNING | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| UNKNOWN  | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| QUERY    | [ ] | [ ]   | [ ] | [ ]    | 0/4   |
| CONVERSATION | [ ] | [ ] | [ ] | [ ]  | 0/4   |
| **TOTAL**| 0/13| 0/13  | 0/13| 0/13   | **0/52** |

## Contract Test Matrix

| Category | Perf | Accuracy | Error | Multi-User | Bypass | Total |
|----------|------|----------|-------|------------|--------|-------|
| TEMPORAL | [ ]  | [ ]      | [ ]   | [ ]        | [ ]    | 0/5   |
| [... all 13 categories]
| **TOTAL**|0/13  |0/13      |0/13   |0/13        |0/13    |**0/65**|

## Test Execution Order

1. Phase 1: Category validation (13 tests)
2. Phase 2: Interface validation (52 tests)
3. Phase 3: Contract validation (65 tests)
4. Phase 4: Load testing (5 benchmarks)
5. Phase 5: Documentation (6 documents)

Total: 135 items + 6 documents = 141 items

## Stop Conditions

- Any category fails validation
- Coverage <100% at any checkpoint
- Performance regression detected
- Documentation incomplete
```

---

## Success Criteria

- [ ] Test constants created with all 13 categories enumerated
- [ ] Coverage tracker implemented
- [ ] Base test class created
- [ ] Test stub generator created and run
- [ ] Test plan documented with coverage matrix
- [ ] Session log updated

---

**Effort**: Small (~30 minutes)
**Priority**: HIGH (foundation for all validation)
**Deliverables**: Test infrastructure ready for Phase 1
