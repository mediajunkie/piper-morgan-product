# Prompt for Code Agent: GREAT-4F Phase 1 - QUERY Fallback Implementation

## Context

Phase 0 complete: ADR-043 documents canonical handler pattern.

**This is Phase 1**: Implement QUERY fallback to handle mis-classified canonical intents gracefully.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-0730-prog-code-log.md`

## Mission

Add intelligent QUERY handling to `workflow_factory.py` that detects likely mis-classifications and routes them appropriately, preventing "No workflow type found" timeout errors.

---

## Background

**The Problem**:
- LLM mis-classifies 5-15% of canonical queries as QUERY
- Example: "show my calendar" → mis-classified as QUERY instead of TEMPORAL
- QUERY has no workflow handler → timeout error
- User gets error instead of their calendar

**The Solution**:
- Add QUERY case to workflow_factory.py
- Use smart pattern matching to detect likely canonical intents
- Route to appropriate workflow or fallback to GENERATE_REPORT
- Log mis-classifications for future improvement

---

## Task 1: Locate and Review workflow_factory.py

**File**: `services/orchestration/workflow_factory.py`

Review the existing structure to understand:
- How other categories are handled
- Where to add QUERY handling
- What the return type should be
- How to create workflows for different types

---

## Task 2: Implement QUERY Fallback

Add intelligent QUERY handling after the existing category handlers:

```python
elif intent.category == IntentCategory.QUERY:
    # Smart fallback for likely mis-classified canonical intents
    text_lower = intent.text.lower()

    # TEMPORAL patterns: calendar, schedule, time-related
    temporal_patterns = [
        'calendar', 'schedule', 'meeting', 'appointment',
        'today', 'tomorrow', 'yesterday', 'next week',
        'what time', 'when is', 'what day'
    ]

    # STATUS patterns: work status, standup, current tasks
    status_patterns = [
        'status', 'standup', 'working on', 'current',
        'progress', 'what am i', "what's my"
    ]

    # PRIORITY patterns: importance, focus, priorities
    priority_patterns = [
        'priority', 'priorities', 'important', 'focus',
        'urgent', 'critical', 'top', 'most important'
    ]

    # Check for canonical patterns
    if any(pattern in text_lower for pattern in temporal_patterns):
        # Likely mis-classified TEMPORAL
        logger.warning(
            f"QUERY intent likely mis-classified TEMPORAL: {intent.text}",
            extra={"intent_id": intent.id, "category": "QUERY", "likely": "TEMPORAL"}
        )
        # Route to temporal workflow or canonical handler
        # NOTE: Adjust based on actual workflow creation methods
        return self._create_temporal_workflow(intent)

    elif any(pattern in text_lower for pattern in status_patterns):
        # Likely mis-classified STATUS
        logger.warning(
            f"QUERY intent likely mis-classified STATUS: {intent.text}",
            extra={"intent_id": intent.id, "category": "QUERY", "likely": "STATUS"}
        )
        return self._create_status_workflow(intent)

    elif any(pattern in text_lower for pattern in priority_patterns):
        # Likely mis-classified PRIORITY
        logger.warning(
            f"QUERY intent likely mis-classified PRIORITY: {intent.text}",
            extra={"intent_id": intent.id, "category": "QUERY", "likely": "PRIORITY"}
        )
        return self._create_priority_workflow(intent)

    else:
        # True generic query - use GENERATE_REPORT workflow
        logger.info(
            f"QUERY intent routed to GENERATE_REPORT: {intent.text}",
            extra={"intent_id": intent.id, "category": "QUERY"}
        )
        workflow_type = WorkflowType.GENERATE_REPORT
        return self._create_workflow(workflow_type, intent)
```

**Note**: Adjust method names (`_create_temporal_workflow`, etc.) to match actual implementation in workflow_factory.py. If these methods don't exist, you may need to create them or route differently.

---

## Task 3: Add Helper Methods (If Needed)

If temporal/status/priority workflow creation methods don't exist, add them:

```python
def _create_temporal_workflow(self, intent: Intent) -> Workflow:
    """Create workflow for temporal/calendar queries."""
    # Implementation depends on existing patterns
    workflow_type = WorkflowType.CALENDAR_INTEGRATION  # or appropriate type
    return self._create_workflow(workflow_type, intent)

def _create_status_workflow(self, intent: Intent) -> Workflow:
    """Create workflow for status queries."""
    workflow_type = WorkflowType.STATUS_CHECK  # or appropriate type
    return self._create_workflow(workflow_type, intent)

def _create_priority_workflow(self, intent: Intent) -> Workflow:
    """Create workflow for priority queries."""
    workflow_type = WorkflowType.PRIORITY_ANALYSIS  # or appropriate type
    return self._create_workflow(workflow_type, intent)
```

**IMPORTANT**: Only add these if they don't already exist. Check the file first.

---

## Task 4: Add Logging Import (If Missing)

Ensure logging is imported at the top of the file:

```python
import logging

logger = logging.getLogger(__name__)
```

---

## Task 5: Test the Implementation

Create simple test to verify QUERY fallback works:

**File**: `tests/intent/test_query_fallback.py`

```python
"""Test QUERY fallback routing for mis-classified intents."""

import pytest
from services.intent.intent_service import IntentService
from services.intent.models import Intent, IntentCategory

class TestQueryFallback:
    """Test QUERY intent fallback handling."""

    @pytest.fixture
    def intent_service(self):
        return IntentService()

    @pytest.mark.asyncio
    async def test_query_temporal_fallback(self, intent_service):
        """QUERY with temporal keywords should not timeout."""
        intent = Intent(
            text="show my calendar",
            category=IntentCategory.QUERY,  # Mis-classified
            confidence=0.85
        )

        # Should not raise "No workflow type found" error
        result = await intent_service.process_intent(intent, "test_session")

        assert result is not None
        assert result.success or "calendar" in result.message.lower()

    @pytest.mark.asyncio
    async def test_query_status_fallback(self, intent_service):
        """QUERY with status keywords should not timeout."""
        intent = Intent(
            text="what is my status",
            category=IntentCategory.QUERY,
            confidence=0.85
        )

        result = await intent_service.process_intent(intent, "test_session")

        assert result is not None
        assert result.success or "status" in result.message.lower()

    @pytest.mark.asyncio
    async def test_query_generic_fallback(self, intent_service):
        """Generic QUERY should route to GENERATE_REPORT."""
        intent = Intent(
            text="what is the weather in Paris",
            category=IntentCategory.QUERY,
            confidence=0.95
        )

        result = await intent_service.process_intent(intent, "test_session")

        assert result is not None
        # Should not timeout, should handle gracefully

    @pytest.mark.asyncio
    async def test_no_workflow_error_prevented(self, intent_service):
        """QUERY should never cause 'No workflow type found' error."""
        queries = [
            "show calendar",
            "my status",
            "what's important",
            "random query"
        ]

        for query_text in queries:
            intent = Intent(
                text=query_text,
                category=IntentCategory.QUERY,
                confidence=0.85
            )

            # None of these should raise errors
            result = await intent_service.process_intent(intent, "test_session")
            assert result is not None, f"Query failed: {query_text}"
```

---

## Verification

After implementation:

```bash
# Verify QUERY handling exists
grep -n "IntentCategory.QUERY" services/orchestration/workflow_factory.py

# Should show the new QUERY case

# Run tests
pytest tests/intent/test_query_fallback.py -v

# Should pass without timeout errors

# Check for "No workflow type found" in logs
# (After running some test queries)
tail -100 logs/app.log | grep "No workflow type found"
# Should be empty or greatly reduced
```

---

## Success Criteria

- [ ] QUERY case added to workflow_factory.py
- [ ] Pattern matching implemented for temporal/status/priority
- [ ] Logging added for mis-classification tracking
- [ ] Fallback to GENERATE_REPORT for generic queries
- [ ] Test file created with 4+ test cases
- [ ] Tests pass without timeout errors
- [ ] "No workflow type found" errors eliminated for QUERY
- [ ] Session log updated

---

## Critical Notes

- **Don't break existing functionality** - only add QUERY case
- **Match existing code style** - follow patterns in workflow_factory.py
- **Test thoroughly** - QUERY fallback is critical for user experience
- **Log mis-classifications** - data helps improve classifier later
- **Be defensive** - assume pattern lists may need expansion

---

**Effort**: Small (~30-40 minutes including tests)
**Priority**: HIGH (prevents user-facing timeout errors)
**Deliverable**: QUERY fallback handling + tests
