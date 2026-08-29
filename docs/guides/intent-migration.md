# Intent Classification Migration Guide

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready

## Overview

This guide helps teams migrate to Piper Morgan's intent classification system. The system provides a universal natural language interface across Web, Slack, CLI, and programmatic access.

## Prerequisites

Before migrating to intent classification:
- [ ] Understand the 13 intent categories (see Categories Reference *(proposed; doc TBD)*)
- [ ] Review [Architecture Decision Record (ADR) 032](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-032-intent-classification-universal-entry.md)
- [ ] Read [Intent Classification Guide](./intent-classification-guide.md)

## Migration Scenarios

### Scenario 1: Adding a New Intent Category

**When**: You need a new type of intent not covered by existing 13 categories.

**Steps**:

1. **Define the category** in `services/intent_service/classifier.py`:
```python
class IntentCategory(str, Enum):
    # ... existing categories
    NEW_CATEGORY = "new_category"
```

2. **Create handler** in `services/intent/intent_service.py`:
```python
async def _handle_new_category_intent(
    self,
    intent: Intent,
    session_id: str
) -> IntentResult:
    """Handler for NEW_CATEGORY intents."""
    # Implementation
    return IntentResult(
        success=True,
        message="Result message",
        data={}
    )
```

3. **Add routing** in `IntentService.process_intent()`:
```python
elif intent.category == IntentCategory.NEW_CATEGORY:
    return await self._handle_new_category_intent(intent, session_id)
```

4. **Update classifier** prompts to recognize new category.

5. **Add tests** following GREAT-4E pattern:
   - Direct interface test (1 test)
   - Web/Slack/CLI interface tests (3 tests)
   - Contract tests: performance, accuracy, error, multi-user, bypass (5 tests)
   - Total: 9 tests minimum

6. **Update documentation**:
   - Add to Categories Reference *(proposed; doc TBD)*
   - Update [ADR-032](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-032-intent-classification-universal-entry.md)
   - Update [Pattern-032](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/patterns/pattern-032-intent-pattern-catalog.md)

### Scenario 2: Adding a New Handler to Existing Category

**When**: Extending functionality within an existing category.

**Steps**:

1. **Add new action** to category handler:
```python
async def _handle_execution_intent(self, intent: Intent, session_id: str):
    if intent.action == "create_issue":
        return await self._handle_create_issue(intent, session_id)
    elif intent.action == "new_action":  # NEW
        return await self._handle_new_action(intent, session_id)
```

2. **Implement handler method**:
```python
async def _handle_new_action(self, intent: Intent, session_id: str):
    """Handle new action within EXECUTION category."""
    # Implementation
```

3. **Add tests** for new action.

4. **Update classifier** to recognize new action patterns.

### Scenario 3: Migrating from Direct Service Calls

**When**: Converting existing direct service calls to intent-based routing.

**Before** (Direct service call):
```python
from services.github_service import GitHubService
github_service = GitHubService()
result = await github_service.create_issue(title, body)
```

**After** (Intent-based):
```python
from services.intent.intent_service import IntentService
intent_service = IntentService()
result = await intent_service.process_intent(
    "Create GitHub issue: Fix bug in login",
    session_id="user_123"
)
```

**Benefits**:
- Universal interface across all entry points
- Automatic classification and routing
- Built-in caching and performance optimization
- Bypass prevention and monitoring

### Scenario 4: Adding New Interface Support

**When**: Adding support for a new communication platform (e.g., Discord, Teams).

**Steps**:

1. **Create integration router** in `services/integrations/[platform]/`:
```python
class NewPlatformRouter:
    def __init__(self):
        self.intent_service = IntentService()

    async def handle_message(self, platform_event):
        # Parse platform-specific event
        message = self._extract_message(platform_event)

        # Route through intent service
        result = await self.intent_service.process_intent(
            message,
            session_id=self._get_session_id(platform_event)
        )

        # Format response for platform
        return self._format_response(result)
```

2. **Add interface tests** for all 13 categories through new platform.

3. **Update documentation** with new interface examples.

## Testing Requirements

### Minimum Test Coverage for New Categories

**Per new category, create:**
- 1 direct interface test
- 3 interface tests (Web, Slack, CLI)
- 5 contract tests (performance, accuracy, error, multi-user, bypass)
- **Total**: 9 tests minimum

### Test Templates

Use existing tests as templates:
- `tests/intent/test_direct_interface.py` - Direct testing
- `tests/intent/test_web_interface.py` - Web API testing
- `tests/intent/contracts/test_performance_contracts.py` - Performance testing

### Running Tests

```bash
# Test new category through all interfaces
pytest tests/intent/test_*_interface.py::TestClass::test_your_category -v

# Test all contracts for new category
pytest tests/intent/contracts/ -k "your_category" -v

# Full test suite
pytest tests/intent/ -v
```

## Common Pitfalls

### Pitfall 1: Bypassing Intent Classification

**Wrong**:
```python
# Direct route that bypasses classification
@app.post("/api/v1/github/create-issue")
async def create_issue_endpoint(request):
    return await github_service.create_issue(...)
```

**Right**:
```python
# Route through intent service
@app.post("/api/v1/intent")
async def intent_endpoint(request):
    return await intent_service.process_intent(request.message)
```

### Pitfall 2: Not Adding Tests

**Always add tests** for new categories or handlers. Untested code will fail in production.

### Pitfall 3: Forgetting Documentation

Update all relevant docs:
- ADR-032 (architecture decisions)
- Pattern-032 (pattern catalog)
- Categories Reference (complete list)
- Classification Guide (usage examples)

### Pitfall 4: Incorrect Category Selection

Choose the right category for your intent:
- **EXECUTION**: Actions that change state
- **ANALYSIS**: Data analysis and insights
- **QUERY**: Information retrieval
- **CONVERSATION**: Conversational responses

Refer to Categories Reference *(proposed; doc TBD)* for guidance.

## Performance Considerations

### Fast Path vs Workflow Path

**Fast Path** (Canonical Handlers ~1ms):
- Use for deterministic, simple responses
- Categories: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
- No LLM classification overhead

**Workflow Path** (2000-3000ms):
- Use for complex operations requiring orchestration
- Categories: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING

### Caching

Intent results are automatically cached:
- Cache hit rate: 84.6% (validated)
- Speedup: 7.6x for cached requests
- No action needed - handled by IntentService

## Rollback Procedures

If you need to rollback intent changes, see [Rollback Plan](../operations/intent-rollback-plan.md).

## Support

Questions about migration?
- Check [Intent Classification Guide](./intent-classification-guide.md)
- Review [ADR-032](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-032-intent-classification-universal-entry.md)
- See test examples in `tests/intent/`

---

**Document Status**: ✅ Production Ready
**Test Coverage**: 126 tests passing
**Performance**: Validated under load
**Last Validated**: October 6, 2025 (GREAT-4E)
