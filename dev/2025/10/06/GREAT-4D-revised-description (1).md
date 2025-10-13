# GREAT-4D: EXECUTION/ANALYSIS Handler Implementation (REVISED)

## Context
Fourth sub-epic of GREAT-4. Implements EXECUTION and ANALYSIS intent handlers following the proven QUERY pattern.

## Background (Updated from Investigation)
Investigation revealed two parallel systems:
- **QueryRouter system** (QUERY intents) - Working perfectly via domain services
- **Workflow system** (EXECUTION/ANALYSIS) - Never built, intentional placeholder

EXECUTION/ANALYSIS intents currently return: "requires full orchestration workflow. This is being restored in Phase 3"

The simple solution: Route EXECUTION/ANALYSIS to domain services like QUERY intents do.

## Scope (Simplified)

### 1. Remove Placeholder
- Remove `_handle_generic_intent()` placeholder response
- Stop blocking EXECUTION/ANALYSIS intents

### 2. Implement EXECUTION Handler
Following QUERY pattern:
- Route to GitHubService for issue operations
- Route to appropriate services for other operations
- Use existing service methods (already proven to work)

### 3. Implement ANALYSIS Handler
Following QUERY pattern:
- Route to data services for analysis
- Use existing report generation capabilities
- Leverage proven service integrations

### 4. Testing
- Verify intents route correctly
- Confirm operations complete
- No placeholder messages remain

## Acceptance Criteria
- [ ] Placeholder removed from `_handle_generic_intent()`
- [ ] EXECUTION intents create actual GitHub issues
- [ ] ANALYSIS intents generate actual reports/analysis
- [ ] Tests prove end-to-end functionality
- [ ] No "Phase 3" references remain
- [ ] Response time <100ms maintained
- [ ] Follows QUERY pattern consistently

## Success Validation
```bash
# Test EXECUTION
echo "Create a GitHub issue about the login bug" | python test_intent.py
# Should create actual issue, not return placeholder

# Test ANALYSIS
echo "Analyze last week's commits" | python test_intent.py
# Should return analysis, not placeholder

# Verify no placeholders
grep -r "Phase 3\|full orchestration workflow" services/
# Should return nothing

# Run tests
pytest tests/intent/test_execution_handler.py -v
pytest tests/intent/test_analysis_handler.py -v
```

## Anti-80% Check
```
Task         | Found | Fixed | Tested | Integrated
------------ | ----- | ----- | ------ | ----------
Placeholder  | ✓     | [ ]   | [ ]    | [ ]
EXECUTION    | ✓     | [ ]   | [ ]    | [ ]
ANALYSIS     | ✓     | [ ]   | [ ]    | [ ]
Tests        | [ ]   | [ ]   | [ ]    | [ ]
```

## Time Estimate
2-4 hours (Small-Medium effort) - Following proven patterns, not building new architecture

## Why Simple Now
- Not building workflow orchestration (complex)
- Following QUERY pattern (proven)
- Using existing services (GitHubService, etc.)
- Direct routing like successful handlers
