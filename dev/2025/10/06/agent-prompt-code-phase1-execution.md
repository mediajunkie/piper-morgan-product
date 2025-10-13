# Prompt for Code Agent: GREAT-4D Phase 1 - EXECUTION Handler Implementation

## Context

Phase 0 confirmed the blocking placeholder in `services/intent/intent_service.py` line 346.

**Target file**: `services/intent/intent_service.py` (NOT services/intent_service/)
**Pattern to follow**: `_handle_query_intent()` method (lines 206-228)
**Task**: Replace placeholder with working EXECUTION handler

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Remove `_handle_generic_intent` placeholder and implement `_handle_execution_intent` following the proven QUERY pattern.

---

## Phase 1: EXECUTION Handler Implementation

### Step 1: Study the QUERY Pattern

The pattern in `services/intent/intent_service.py`:

```python
async def _handle_query_intent(self, intent, workflow, session_id):
    """Routes to appropriate domain service based on intent action."""

    if intent.action in ["show_standup", "get_standup"]:
        return await self._handle_standup_query(intent, workflow.id, session_id)
    elif intent.action in ["list_projects", "show_projects"]:
        return await self._handle_projects_query(intent, workflow.id)
    else:
        # Generic query handler using QueryRouter
        return await self._handle_generic_query(intent, workflow.id)
```

**Key pattern elements**:
1. Check for specific actions
2. Route to specific handlers
3. Fall back to generic handler
4. Pass workflow.id consistently
5. Return IntentProcessingResult

### Step 2: Check Where to Route EXECUTION Intents

Find the main routing logic in `services/intent/intent_service.py`:

```bash
# Find where QUERY gets routed
grep -B 5 -A 10 "IntentCategory.QUERY" services/intent/intent_service.py

# Check if EXECUTION/ANALYSIS routing exists
grep -B 5 -A 10 "IntentCategory.EXECUTION\|IntentCategory.ANALYSIS" services/intent/intent_service.py
```

Document current routing and where to add EXECUTION/ANALYSIS cases.

### Step 3: Implement _handle_execution_intent

Edit: `services/intent/intent_service.py`

Replace the placeholder `_handle_generic_intent` with:

```python
async def _handle_execution_intent(
    self, intent: Intent, workflow, session_id: str
) -> IntentProcessingResult:
    """
    Handle EXECUTION category intents.

    Routes to appropriate domain service based on intent action.
    Follows QUERY pattern for consistency.
    """
    self.logger.info(f"Processing EXECUTION intent: {intent.action}")

    # Route based on action
    if intent.action in ["create_issue", "create_ticket"]:
        return await self._handle_create_issue(intent, workflow.id, session_id)

    elif intent.action in ["update_issue", "update_ticket"]:
        return await self._handle_update_issue(intent, workflow.id)

    else:
        # Generic execution handler - route to orchestration
        self.logger.info(f"Routing generic EXECUTION to orchestration: {intent.action}")
        try:
            result = await self.orchestration_engine.handle_execution_intent(intent)
            return IntentProcessingResult(
                success=True,
                message=f"Execution processed: {intent.action}",
                intent_data={
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                },
                workflow_id=workflow.id,
                requires_clarification=False,
            )
        except Exception as e:
            self.logger.error(f"Execution handler error: {e}")
            return IntentProcessingResult(
                success=False,
                message=f"Failed to execute: {str(e)}",
                workflow_id=workflow.id,
                error=str(e),
                error_type="ExecutionError",
            )
```

### Step 4: Implement _handle_create_issue

Add specific handler for issue creation:

```python
async def _handle_create_issue(
    self, intent: Intent, workflow_id: str, session_id: str
) -> IntentProcessingResult:
    """
    Handle create_issue/create_ticket action.

    Creates GitHub issue using domain service.
    """
    try:
        from services.domain.github_domain_service import GitHubDomainService

        github_service = GitHubDomainService()

        # Extract issue details from intent
        title = intent.context.get("title") or f"Issue: {intent.text[:50]}"
        description = intent.context.get("description") or intent.text
        repository = intent.context.get("repository")

        # Create issue
        issue = await github_service.create_issue(
            title=title,
            body=description,
            repository=repository,
            labels=intent.context.get("labels", [])
        )

        return IntentProcessingResult(
            success=True,
            message=f"Created issue #{issue.number}: {issue.title}",
            intent_data={
                "category": intent.category.value,
                "action": intent.action,
                "issue_number": issue.number,
                "issue_url": issue.html_url,
            },
            workflow_id=workflow_id,
            requires_clarification=False,
        )

    except Exception as e:
        self.logger.error(f"Failed to create issue: {e}")
        return IntentProcessingResult(
            success=False,
            message=f"Failed to create issue: {str(e)}",
            workflow_id=workflow_id,
            error=str(e),
            error_type="GitHubError",
        )
```

### Step 5: Update Main Routing

Find the main `process()` or routing method and add EXECUTION case:

```python
# In main routing logic (find this pattern)
if intent.category == IntentCategory.QUERY:
    return await self._handle_query_intent(intent, workflow, session_id)

# Add after QUERY:
elif intent.category == IntentCategory.EXECUTION:
    return await self._handle_execution_intent(intent, workflow, session_id)
```

**Remove or update the old call to `_handle_generic_intent`**.

### Step 6: Test EXECUTION Handler

Create: `dev/2025/10/06/test_execution_handler.py`

```python
"""Test EXECUTION intent handler - GREAT-4D Phase 1"""
import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService
from services.intent_service import classifier


async def test_execution_handler():
    """Test that EXECUTION intents work, not placeholder."""

    print("=" * 80)
    print("EXECUTION HANDLER TEST - GREAT-4D Phase 1")
    print("=" * 80)

    intent_service = IntentService()

    # Test create issue intent
    print("\n1. Testing create_issue intent:")
    intent = await classifier.classify("create an issue about testing execution handlers")
    print(f"   Category: {intent.category.value}")
    print(f"   Action: {intent.action}")

    result = await intent_service.process(intent, session_id="test_session")
    print(f"   Success: {result.success}")
    print(f"   Message: {result.message}")

    # Check for placeholder message
    if "Phase 3" in result.message or "full orchestration workflow" in result.message:
        print("   ❌ FAILED - Still returning placeholder message")
        return False
    else:
        print("   ✅ PASSED - No placeholder message")

    # Verify it attempted to do work
    if result.success or "issue" in result.message.lower():
        print("   ✅ PASSED - Handler attempted execution")
    else:
        print("   ⚠️  WARNING - Handler may not have executed")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_execution_handler())
    if success:
        print("\n✅ EXECUTION handler working - placeholder removed!")
    else:
        print("\n❌ EXECUTION handler still has issues")
```

Run test:
```bash
PYTHONPATH=. python3 dev/2025/10/06/test_execution_handler.py
```

---

## Success Criteria

- [ ] `_handle_generic_intent` placeholder removed
- [ ] `_handle_execution_intent` implemented following QUERY pattern
- [ ] `_handle_create_issue` implemented for issue creation
- [ ] Main routing updated to call EXECUTION handler
- [ ] Test shows no "Phase 3" placeholder message
- [ ] Test shows handler attempts execution
- [ ] Session log updated

---

## Evidence Format

```bash
$ PYTHONPATH=. python3 dev/2025/10/06/test_execution_handler.py
=== EXECUTION HANDLER TEST ===

1. Testing create_issue intent:
   Category: EXECUTION
   Action: create_issue
   Success: True
   Message: Created issue #123: Issue: create an issue about testing
   ✅ PASSED - No placeholder message
   ✅ PASSED - Handler attempted execution

✅ EXECUTION handler working - placeholder removed!
```

---

**Effort**: Small-Medium (~1 hour)
**Priority**: HIGH (removes blocker)
**Pattern**: Follow QUERY exactly - proven to work
