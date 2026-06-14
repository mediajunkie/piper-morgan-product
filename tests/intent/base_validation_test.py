"""Base test class for GREAT-4E validation.

#1204: restored after #1094 deleted it — collateral to the OrchestrationEngine
removal, since its old ``intent_service`` fixture constructed the now-deleted
``OrchestrationEngine``. Deleting it left SIX intent-contract test files
uncollectable (``ModuleNotFoundError: tests.intent.base_validation_test``):
test_error_contracts, test_performance_contracts, test_bypass_contracts,
test_accuracy_contracts, test_multiuser_contracts, and test_direct_interface.

The broken fixture is dropped; those classes now inherit the shared
``intent_service`` fixture from ``tests/conftest.py`` (the current,
non-orchestration construction — they define no fixture of their own). Only the
generic, orchestration-free helpers remain here.
"""

from typing import Any, Dict

from tests.intent.coverage_tracker import coverage
from tests.intent.test_constants import CATEGORY_EXAMPLES, PERFORMANCE_THRESHOLDS


class BaseValidationTest:
    """Base class for intent validation tests.

    Note: the ``intent_service`` fixture is provided by ``tests/conftest.py``
    (inherited), not here — see #1204.
    """

    async def validate_category(self, category: str, interface: str, intent_service) -> Dict[str, Any]:
        """Validate a category through a specific interface. Returns results."""
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
        assert (
            duration_ms < threshold
        ), f"Response time {duration_ms}ms exceeds threshold {threshold}ms"
