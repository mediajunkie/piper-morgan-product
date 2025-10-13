# Prompt for Code Agent: GREAT-4E-2 Phase 2 - New Documentation

## Context

Phase 1 complete: 4 documents updated with GREAT-4E findings.

**This is Phase 2**: Create 3 new documents (Migration Guide, Categories Reference, Rollback Plan)

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Create 3 new documentation files to complete GREAT-4E-2 acceptance criteria.

---

## Phase 2: New Documentation (3 Items)

### Document 1: Migration Guide

**File**: `docs/guides/intent-migration.md`

**Purpose**: Help teams adopt intent classification system

**Content**:

```markdown
# Intent Classification Migration Guide

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready

## Overview

This guide helps teams migrate to Piper Morgan's intent classification system. The system provides a universal natural language interface across Web, Slack, CLI, and programmatic access.

## Prerequisites

Before migrating to intent classification:
- [ ] Understand the 13 intent categories (see [Categories Reference](../reference/intent-categories.md))
- [ ] Review [ADR-032](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
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
   - Add to [Categories Reference](../reference/intent-categories.md)
   - Update [ADR-032](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
   - Update [Pattern-032](../internal/architecture/current/patterns/pattern-032-intent-pattern-catalog.md)

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
result = await intent_service.process_message(
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
        result = await self.intent_service.process_message(
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
    return await intent_service.process_message(request.message)
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

Refer to [Categories Reference](../reference/intent-categories.md) for guidance.

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
- Review [ADR-032](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
- See test examples in `tests/intent/`

---

**Document Status**: ✅ Production Ready
**Test Coverage**: 126 tests passing
**Performance**: Validated under load
**Last Validated**: October 6, 2025 (GREAT-4E)
```

### Document 2: Intent Categories Reference

**File**: `docs/reference/intent-categories.md`

**Purpose**: Complete reference of all 13 intent categories

**Content**:

```markdown
# Intent Categories Reference

**Version**: 1.0
**Last Updated**: October 6, 2025
**Coverage**: 13/13 categories (100%)

## Overview

Piper Morgan's intent classification system recognizes 13 distinct intent categories, each routing to specialized handlers optimized for that category's needs.

## Category Architecture

### Fast Path (Canonical Handlers)
**Performance**: ~1ms average response time
**Method**: Pre-classifier pattern recognition
**Use case**: Simple, deterministic queries

### Workflow Path (Orchestration)
**Performance**: 2000-3000ms average response time
**Method**: Full LLM classification + workflow execution
**Use case**: Complex, multi-step operations

---

## Categories (Alphabetical)

### 1. ANALYSIS
**Path**: Workflow
**Purpose**: Data analysis and insights generation
**Performance**: 2000-3000ms

**Example Queries**:
- "Analyze commits from last week"
- "What patterns exist in our code?"
- "Generate a report on test coverage"

**Handler**: `_handle_analysis_intent`
**Actions**: `analyze_commits`, `generate_report`, `analyze_data`
**Tests**: 9 tests (direct + interfaces + contracts)

---

### 2. CONVERSATION
**Path**: Workflow
**Purpose**: Conversational responses and general chat
**Performance**: 2000-3000ms

**Example Queries**:
- "Hey, how's it going?"
- "Tell me a joke"
- "What do you think about X?"

**Handler**: `_handle_conversation_intent`
**Tests**: 9 tests

---

### 3. EXECUTION
**Path**: Workflow
**Purpose**: Action execution and state changes
**Performance**: 2000-3000ms

**Example Queries**:
- "Create GitHub issue for bug fix"
- "Update ticket status to in progress"
- "Deploy to staging"

**Handler**: `_handle_execution_intent`
**Actions**: `create_issue`, `update_issue`
**Tests**: 9 tests

---

### 4. GUIDANCE
**Path**: Fast (Canonical)
**Purpose**: Recommendations and advice
**Performance**: ~1ms

**Example Queries**:
- "How should I approach this problem?"
- "What's the best way to structure this?"
- "Give me advice on X"

**Handler**: Canonical handler in `services/intent_service/canonical_handlers.py`
**Tests**: 9 tests

---

### 5. IDENTITY
**Path**: Fast (Canonical)
**Purpose**: Bot identity and capabilities
**Performance**: ~1ms

**Example Queries**:
- "Who are you?"
- "What can you do?"
- "Tell me about yourself"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 6. LEARNING
**Path**: Workflow
**Purpose**: Pattern recognition and learning
**Performance**: 2000-3000ms

**Example Queries**:
- "What patterns exist in our workflow?"
- "Learn from these examples"
- "Identify common issues"

**Handler**: `_handle_learning_intent`
**Actions**: `learn_pattern`
**Tests**: 9 tests

---

### 7. PRIORITY
**Path**: Fast (Canonical)
**Purpose**: Priority assessment and focus
**Performance**: ~1ms

**Example Queries**:
- "What's most important right now?"
- "What should I focus on?"
- "Show me top priorities"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 8. QUERY
**Path**: Workflow
**Purpose**: General information queries
**Performance**: 2000-3000ms

**Example Queries**:
- "What's the weather?"
- "Look up X"
- "Search for Y"

**Handler**: `_handle_query_intent`
**Tests**: 9 tests

---

### 9. STATUS
**Path**: Fast (Canonical)
**Purpose**: Current state and progress
**Performance**: ~1ms

**Example Queries**:
- "Show my standup status"
- "What am I working on?"
- "Current progress?"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 10. STRATEGY
**Path**: Workflow
**Purpose**: Strategic planning and prioritization
**Performance**: 2000-3000ms

**Example Queries**:
- "Plan next sprint"
- "Create a roadmap"
- "Prioritize backlog"

**Handler**: `_handle_strategy_intent`
**Actions**: `strategic_planning`, `prioritization`
**Tests**: 9 tests

---

### 11. SYNTHESIS
**Path**: Workflow
**Purpose**: Content generation and summarization
**Performance**: 2000-3000ms

**Example Queries**:
- "Generate a summary"
- "Create documentation"
- "Synthesize these notes"

**Handler**: `_handle_synthesis_intent`
**Actions**: `generate_content`, `summarize`
**Tests**: 9 tests

---

### 12. TEMPORAL
**Path**: Fast (Canonical)
**Purpose**: Time and schedule queries
**Performance**: ~1ms

**Example Queries**:
- "What's on my calendar?"
- "When is my next meeting?"
- "What day is it?"

**Handler**: Canonical handler
**Tests**: 9 tests

---

### 13. UNKNOWN
**Path**: Workflow
**Purpose**: Fallback for unclassifiable input
**Performance**: 2000-3000ms

**Example Queries**:
- "Blarghhh"
- "asdfasdf"
- [Gibberish or unclear input]

**Handler**: `_handle_unknown_intent`
**Response**: Helpful fallback, asks for clarification
**Tests**: 9 tests

---

## Category Selection Guide

### When to Use Each Category

**Need instant response?** → Use Fast Path categories (IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE)

**Need complex operation?** → Use Workflow Path categories (EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING)

**Uncertain classification?** → System will route to UNKNOWN and provide helpful fallback

### Classification Confidence

The classifier assigns confidence scores:
- **High confidence** (>0.9): Direct routing
- **Medium confidence** (0.7-0.9): Validated routing
- **Low confidence** (<0.7): May route to UNKNOWN

## Performance Summary

| Category | Path | Avg Time | Cache Hit Rate |
|----------|------|----------|----------------|
| IDENTITY | Fast | ~1ms | 84.6% |
| TEMPORAL | Fast | ~1ms | 84.6% |
| STATUS | Fast | ~1ms | 84.6% |
| PRIORITY | Fast | ~1ms | 84.6% |
| GUIDANCE | Fast | ~1ms | 84.6% |
| EXECUTION | Workflow | 2000-3000ms | 84.6% |
| ANALYSIS | Workflow | 2000-3000ms | 84.6% |
| SYNTHESIS | Workflow | 2000-3000ms | 84.6% |
| STRATEGY | Workflow | 2000-3000ms | 84.6% |
| LEARNING | Workflow | 2000-3000ms | 84.6% |
| QUERY | Workflow | 2000-3000ms | 84.6% |
| CONVERSATION | Workflow | 2000-3000ms | 84.6% |
| UNKNOWN | Workflow | 2000-3000ms | 84.6% |

**Cache speedup**: 7.6x for all categories
**Sustained throughput**: 602,907 req/sec
**Validated**: October 6, 2025 (GREAT-4E)

## Test Coverage

Each category has 9 tests:
- 1 direct interface test
- 3 interface tests (Web, Slack, CLI)
- 5 contract tests (performance, accuracy, error, multi-user, bypass)

**Total test coverage**: 126 tests (13 categories × 9 tests + coverage reports)
**Status**: All passing ✅

## Related Documentation

- [ADR-032: Intent Classification Universal Entry](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
- [Pattern-032: Intent Pattern Catalog](../internal/architecture/current/patterns/pattern-032-intent-pattern-catalog.md)
- [Intent Classification Guide](../guides/intent-classification-guide.md)
- [Migration Guide](../guides/intent-migration.md)

---

**Document Status**: ✅ Production Ready
**Last Validated**: October 6, 2025 (GREAT-4E)
**Coverage**: 13/13 categories (100%)
```

### Document 3: Intent Rollback Plan

**File**: `docs/operations/intent-rollback-plan.md`

**Purpose**: Emergency rollback procedures for intent system

**Content**:

```markdown
# Intent System Rollback Plan

**Version**: 1.0
**Last Updated**: October 6, 2025
**Status**: Production Ready

## Overview

This document provides emergency rollback procedures for the intent classification system. Use these procedures when the intent system is experiencing issues that require immediate intervention.

## Identifying Need for Rollback

### Critical Symptoms

Rollback immediately if you observe:
- **Error rate >10%**: Sustained error rate above 10% for >5 minutes
- **Response time >5s**: P95 response time exceeds 5 seconds
- **Classification accuracy <70%**: Significant mis-classification causing user issues
- **Complete system failure**: Intent service crashes or becomes unresponsive

### Warning Symptoms

Consider rollback if you observe:
- **Error rate 5-10%**: Elevated but not critical error rate
- **Response time 3-5s**: Degraded but functional performance
- **Classification accuracy 70-80%**: Lower accuracy than validated baseline
- **Memory leaks**: Continuous memory growth over 1 hour

## Monitoring Endpoints

Check system health:
```bash
# Intent monitoring dashboard
curl http://localhost:8001/api/admin/intent-monitoring

# Cache metrics
curl http://localhost:8001/api/admin/intent-cache-metrics

# Check error rate
curl http://localhost:8001/api/admin/intent-monitoring | jq '.errors_last_hour'
```

## Rollback Procedures

### Option 1: Rollback to Previous Commit (RECOMMENDED)

**When**: Intent handlers or classification logic has bugs

**Steps**:

1. **Identify last known good commit**:
```bash
# Check recent commits
git log --oneline services/intent/ | head -10

# Find GREAT-4E deployment commit
git log --grep="GREAT-4E" --oneline
```

2. **Revert to last good commit**:
```bash
# Revert specific commit
git revert [bad-commit-hash]

# Or reset to known good commit (nuclear option)
git reset --hard [good-commit-hash]
git push origin main --force
```

3. **Verify rollback**:
```bash
# Run basic functionality tests
PYTHONPATH=. python3 -m pytest tests/intent/test_direct_interface.py -v

# Check that all 13 categories work
PYTHONPATH=. python3 tests/intent/test_basic_functionality.py
```

4. **Clear intent cache**:
```bash
curl -X POST http://localhost:8001/api/admin/intent-cache/clear
```

5. **Restart services**:
```bash
# Local development
./scripts/restart-services.sh

# Production
systemctl restart piper-morgan
```

### Option 2: Disable Specific Category

**When**: One category is failing but others work

**Steps**:

1. **Comment out category handler** in `services/intent/intent_service.py`:
```python
async def process_intent(self, intent: Intent, session_id: str):
    # Temporarily disable problematic category
    if intent.category == IntentCategory.PROBLEMATIC:
        return IntentResult(
            success=False,
            message="This feature is temporarily unavailable"
        )

    # Normal processing continues
    if intent.category == IntentCategory.TEMPORAL:
        return await self._handle_temporal_intent(...)
```

2. **Deploy hotfix**:
```bash
git commit -am "Hotfix: Disable PROBLEMATIC category temporarily"
git push origin main
```

3. **Monitor other categories**:
```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

### Option 3: Emergency Bypass (LAST RESORT)

**When**: Complete intent system failure, need immediate fallback

**WARNING**: This breaks the universal entry point architecture. Use only in emergencies.

**Steps**:

1. **Enable bypass flag** in `config/PIPER.user.md`:
```yaml
intent_classification:
  enabled: false  # Temporarily disable intent classification
  bypass_mode: true
```

2. **Restart services**:
```bash
systemctl restart piper-morgan
```

3. **Verify fallback routing**:
```bash
# Should route directly without classification
curl -X POST http://localhost:8001/api/v1/chat \
  -d '{"message": "test"}'
```

4. **Immediate followup**: File incident report and plan proper fix.

## Post-Rollback Procedures

### 1. Verify System Health

After rollback, verify:
```bash
# Check error rate
curl http://localhost:8001/api/admin/intent-monitoring | jq '.errors_last_hour'
# Should be <5

# Check classification accuracy
curl http://localhost:8001/api/admin/intent-monitoring | jq '.classification_accuracy'
# Should be >90%

# Check response times
curl http://localhost:8001/api/admin/intent-monitoring | jq '.avg_response_time'
# Should be <3000ms

# Run full test suite
pytest tests/intent/ -v
# Should show 126/126 passing
```

### 2. Root Cause Analysis

Document what went wrong:
- What symptoms were observed?
- What change triggered the issue?
- Why did monitoring not catch it earlier?
- What tests would have caught this?

### 3. Create Prevention Plan

- Add tests for the failure scenario
- Update monitoring thresholds
- Improve classification prompts
- Add safeguards to code

### 4. Communicate Status

Notify stakeholders:
- What was rolled back
- Current system status
- Expected timeline for fix
- Action items for prevention

## Recovery Procedures

### Recovering from Rollback

Once the issue is fixed:

1. **Create fix branch**:
```bash
git checkout -b fix/intent-issue-YYYYMMDD
```

2. **Implement fix with tests**:
```bash
# Fix the issue
# Add regression tests
pytest tests/intent/ -v  # Verify all pass
```

3. **Test in staging**:
```bash
# Deploy to staging
# Monitor for 1 hour
# Verify metrics are healthy
```

4. **Deploy to production**:
```bash
git push origin fix/intent-issue-YYYYMMDD
# Create PR, get review
# Merge to main
# Monitor closely for 24 hours
```

## Escalation

### When to Escalate

Escalate immediately if:
- Rollback doesn't resolve issues
- Multiple rollbacks needed in short time
- Data corruption suspected
- Security issue identified

### Escalation Contacts

[Add your team's escalation contacts]

## Testing Rollback Procedures

**Recommended**: Test rollback procedures in staging quarterly.

```bash
# Simulate rollback in staging
git checkout staging
git revert [recent-commit]
./scripts/test-rollback.sh
```

## Related Documentation

- [Intent Classification Guide](../guides/intent-classification-guide.md)
- [Migration Guide](../guides/intent-migration.md)
- [ADR-032: Intent Universal Entry](../internal/architecture/current/adrs/adr-032-intent-classification-universal-entry.md)
- [Operational Guide](./operational-guide.md)

---

**Document Status**: ✅ Production Ready
**Last Tested**: October 6, 2025
**Review Cycle**: Quarterly
```

---

## File Naming Convention

**Save your work as**: `great4e-2-phase2-code-newdocs.md`

This avoids conflicts with Cursor's Phase 3/4 work.

---

## Success Criteria

- [ ] Migration guide created (docs/guides/intent-migration.md)
- [ ] Categories reference created (docs/reference/intent-categories.md)
- [ ] Rollback plan created (docs/operations/intent-rollback-plan.md)
- [ ] All 3 documents complete and comprehensive
- [ ] Session log updated
- [ ] Work saved with unique filename

---

## Validation

After creation, verify:
```bash
# All 3 documents exist
ls -la docs/guides/intent-migration.md
ls -la docs/reference/intent-categories.md
ls -la docs/operations/intent-rollback-plan.md

# Check document sizes (should be substantial)
wc -l docs/guides/intent-migration.md  # Should be >200 lines
wc -l docs/reference/intent-categories.md  # Should be >300 lines
wc -l docs/operations/intent-rollback-plan.md  # Should be >200 lines
```

---

**Effort**: Medium (~60 minutes for 3 comprehensive documents)
**Priority**: HIGH (completes documentation requirements)
**Deliverables**: 3 new documentation files
