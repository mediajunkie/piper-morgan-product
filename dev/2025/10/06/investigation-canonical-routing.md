# Investigation: Canonical Handler Routing Trace

## Context
GREAT-4E Phase 4 load testing revealed "No workflow type found" errors for IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE categories. Yet all tests pass. We need to understand the actual execution flow.

## Your Task
Trace the complete execution path for canonical intents to understand why tests pass but errors appear in logs.

## Investigation Requirements

### 1. Find the Canonical Handler Integration Point

Look in `services/intent/intent_service.py` for:
```python
# We found this comment but need the actual code:
# Handle canonical intents (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)
if self.canonical_handlers.can_handle(intent):
    canonical_result = await self.canonical_handlers.handle(intent, session_id)
```

Document:
- What line number is this at?
- Is it BEFORE or AFTER the main routing logic (lines 118-165)?
- Does it return immediately or continue processing?

### 2. Trace a PRIORITY Intent End-to-End

Create a test script:
```python
# dev/2025/10/06/trace_canonical_routing.py
import asyncio
import logging
from services.intent_service import IntentService

logging.basicConfig(level=logging.DEBUG)

async def trace_priority_intent():
    """Trace how PRIORITY intent flows through the system"""

    service = IntentService()
    text = "What is my top priority today?"

    print(f"\n=== Tracing: {text} ===\n")

    # Add debug logging to see the flow
    result = await service.process_intent(text, "test-session")

    print(f"\nResult type: {type(result)}")
    print(f"Result content: {result}")

    # Check for errors
    if isinstance(result, dict):
        if "error" in result:
            print(f"ERROR FOUND: {result['error']}")
        if "workflow" in result:
            print(f"WORKFLOW: {result['workflow']}")

    return result

asyncio.run(trace_priority_intent())
```

Run it and document:
1. Does it succeed or fail?
2. What's the actual response?
3. Any error messages in logs?

### 3. Understand the Dual Path Problem

Check if there are TWO paths that canonical intents can take:

**Path A**: Through canonical handlers (working)
```
Intent → PreClassifier → CanonicalHandlers.handle() → Response
```

**Path B**: Through main routing (failing)
```
Intent → IntentService.process_intent() → No handler found → Workflow attempt → Error
```

Find evidence:
- Are both paths active?
- Which path do tests use?
- Which path does production use?
- Why do both exist?

### 4. Locate the "No workflow type found" Error

Find where this error is generated:
```bash
grep -n "No workflow type found" services/ -r
```

Then trace back:
- What conditions trigger this error?
- Can canonical intents reach this code path?
- If yes, why aren't they handled before reaching it?

### 5. Verify Test vs Production Behavior

Compare how tests execute vs production:

**Test execution**:
```python
# How do the GREAT-4E tests call canonical intents?
# Check tests/intent/test_category_validation.py or similar
```

**Production execution**:
```python
# How does the actual web API call them?
# Check web/app.py or web/middleware/
```

Document any differences in the execution paths.

### 6. Check for Multiple IntentService Instances

Are there different IntentService configurations?
```python
# Check if canonical handlers are initialized differently
grep -n "IntentService()" . -r
grep -n "canonical_handlers" services/intent/ -r
```

Could some instances have canonical handlers wired and others not?

## Deliverables

1. **Execution Flow Diagram** showing both paths (if two exist)
2. **Line-by-line trace** of a PRIORITY intent through the system
3. **Explanation** of why tests pass but errors appear
4. **Root cause** of "No workflow type found" for canonical categories
5. **Recommendation**:
   - Is this a real bug or just noisy logging?
   - Should we create GREAT-4F to fix it?
   - Or can we mark GREAT-4E complete?

## Success Criteria

- Clear understanding of canonical handler routing
- Explanation of test success despite error messages
- Definitive answer on whether this blocks GREAT-4E completion

---

*Time estimate: 30-45 minutes investigation*
