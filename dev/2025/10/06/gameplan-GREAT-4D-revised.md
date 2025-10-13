# Gameplan: GREAT-4D - EXECUTION/ANALYSIS Handlers (REVISED)

**Date**: October 6, 2025
**Epic**: GREAT-4D (Fourth sub-epic of GREAT-4)
**Context**: Follow QUERY pattern to implement missing handlers
**Effort**: Small-Medium (2-4 hours)

## Mission

Remove placeholder blocking EXECUTION/ANALYSIS intents and implement handlers following the proven QUERY pattern that already works for STATUS/TEMPORAL/PRIORITY intents.

## Background from Investigation

Code's investigation (12:18 PM) revealed:
- QUERY intents work perfectly via domain services
- EXECUTION/ANALYSIS blocked by placeholder: "requires full orchestration workflow"
- Solution: Follow QUERY pattern, not complex workflow orchestration

## Phase 0: Current State Verification
**Both Agents - Small effort**

### Verify Investigation Findings
```bash
# Confirm placeholder location
grep -n "full orchestration workflow" services/intent/intent_service.py

# Check QUERY pattern for reference
grep -n "_handle_query_intent" services/intent/intent_service.py

# Verify GitHubService methods available
grep "def create" services/github_service/*.py
```

### Document Pattern
Study how `_handle_query_intent()` works and routes to services.

## Phase 1: Remove Placeholder & Add Routing
**Code Agent - Small effort**

### In `services/intent/intent_service.py`

Remove generic handler and add specific routing:
```python
# Find and modify _handle_generic_intent
# Replace with:
async def _handle_execution_intent(self, intent, context):
    # Route to appropriate service based on intent

async def _handle_analysis_intent(self, intent, context):
    # Route to appropriate service based on intent
```

Update main routing:
```python
# In process() or equivalent routing method
elif intent.category == IntentCategory.EXECUTION:
    return await self._handle_execution_intent(intent, context)
elif intent.category == IntentCategory.ANALYSIS:
    return await self._handle_analysis_intent(intent, context)
```

## Phase 2: Implement EXECUTION Handler
**Code Agent - Medium effort**

### Follow QUERY Pattern
Look at how QUERY routes to services, do similar for EXECUTION:

```python
async def _handle_execution_intent(self, intent, context):
    # Parse what needs to be executed
    if "issue" in intent.text.lower() or "ticket" in intent.text.lower():
        # Use GitHubService
        github_service = self.service_locator.get(GitHubService)
        # Extract title and description from intent
        # Call service method
        result = await github_service.create_issue(...)
        return {"status": "success", "result": result}
```

## Phase 3: Implement ANALYSIS Handler
**Cursor Agent - Medium effort**

### Follow QUERY Pattern
Similar approach for ANALYSIS:

```python
async def _handle_analysis_intent(self, intent, context):
    # Determine analysis type
    if "commit" in intent.text.lower():
        # Analyze commits
        analysis_service = self.service_locator.get(AnalysisService)
        # Or use existing service
        result = await analysis_service.analyze_commits(...)
    elif "report" in intent.text.lower():
        # Generate report
        result = await self.report_service.generate(...)

    return {"status": "success", "analysis": result}
```

## Phase 4: Testing
**Cursor Agent - Small effort**

### Create Handler Tests
`tests/intent/test_execution_analysis_handlers.py`:

```python
async def test_execution_creates_issue():
    # Test that EXECUTION intent creates actual GitHub issue

async def test_analysis_generates_report():
    # Test that ANALYSIS intent returns actual analysis

async def test_no_placeholder_remains():
    # Verify no "Phase 3" message returned
```

### Integration Test
Test end-to-end flow from intent to actual result.

## Phase Z: Validation
**Both Agents**

### Verify Success
```bash
# No placeholders remain
grep -r "Phase 3\|full orchestration" services/intent/
# Should be empty

# Test actual functionality
python dev/2025/10/06/test_execution_analysis_behavior.py
# Should show success, not placeholder
```

### Update Documentation
- Remove any "Phase 3" references
- Document new handlers

## Success Criteria

- [ ] Placeholder removed (PM will validate)
- [ ] EXECUTION creates GitHub issues (PM will validate)
- [ ] ANALYSIS returns actual analysis (PM will validate)
- [ ] Tests passing (PM will validate)
- [ ] No "Phase 3" references (PM will validate)
- [ ] Follows QUERY pattern (PM will validate)

## Agent Division

**Code Agent** - Phases 1, 2
- Remove placeholder
- Implement EXECUTION handler
- Follow QUERY pattern

**Cursor Agent** - Phases 3, 4
- Implement ANALYSIS handler
- Create tests
- Validate implementation

## Critical Notes

- Follow QUERY pattern exactly - it's proven to work
- Don't build workflow orchestration - too complex
- Use existing services - they already work
- Simple is better - direct routing like QUERY

## STOP Conditions

- If QUERY pattern unclear
- If services don't have needed methods
- If complexity exceeds pattern

---

*Ready to implement simple, proven solution!*
