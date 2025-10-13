# GREAT-4F: Classifier Accuracy & Canonical Pattern Formalization

## Context
Sixth sub-epic of GREAT-4. Addresses LLM classifier accuracy issues discovered during GREAT-4E load testing and formalizes the undocumented canonical handler pattern.

## Background
GREAT-4E Phase 4 investigation revealed:
- Canonical handlers work correctly when intents classify properly
- ~5-15% of canonical queries mis-classify as QUERY category
- No QUERY workflow exists, causing timeout errors
- Canonical handler pattern exists but lacks ADR documentation
- Dual-path architecture (fast-path vs workflow) is intentional but undocumented

## Scope

### 1. Formalize Canonical Handler Architecture
- Create ADR-043: Canonical Handler Fast-Path Pattern
- Document when to use canonical handlers vs workflows
- Clarify dual-path architecture rationale
- Establish pattern for future simple query handlers

### 2. Add QUERY Fallback Handling
- Map QUERY category to appropriate workflow/handler
- Prevent timeout errors for mis-classified intents
- Provide graceful degradation
- Maintain performance for correctly classified queries

### 3. Improve Classifier Accuracy
- Analyze mis-classification patterns
- Enhance classifier prompts for canonical categories
- Add disambiguation rules for TEMPORAL vs QUERY
- Add disambiguation rules for STATUS vs QUERY
- Test and measure improvement

### 4. Classification Accuracy Testing
- Create comprehensive test suite for classification
- Test 50+ variations per category
- Measure baseline accuracy per category
- Set target: 95% accuracy for canonical categories
- Add to CI/CD pipeline

## Acceptance Criteria
- [ ] ADR-043 created and approved documenting canonical pattern
- [ ] QUERY category has fallback handling (no timeouts)
- [ ] Classifier prompt improved with disambiguation rules
- [ ] Classification accuracy tests created (50+ per category)
- [ ] Canonical categories achieve 95% classification accuracy
- [ ] No "No workflow type found" errors in production logs
- [ ] Documentation updated explaining dual-path architecture
- [ ] CI/CD includes classification accuracy gates

## Success Validation
```bash
# Test classification accuracy
python tests/intent/test_classification_accuracy.py -v
# Should show 95%+ accuracy for canonical categories

# Test QUERY fallback
echo "random query text" | python test_intent.py
# Should not timeout, should return graceful response

# Verify no workflow errors
grep "No workflow type found" logs/production.log
# Should return empty (no errors)

# Check ADR exists
ls docs/adrs/adr-043*
# Should show ADR file

# Run mis-classification tests
for query in "show calendar" "what time" "my status" "priorities"; do
  python classify_intent.py "$query"
done
# Should classify correctly 95% of time
```

## Anti-80% Check
```
Component           | Created | Tested | Documented | Deployed
------------------- | ------- | ------ | ---------- | --------
ADR-043            | [ ]     | N/A    | [ ]        | [ ]
QUERY fallback     | [ ]     | [ ]    | [ ]        | [ ]
Classifier prompts | [ ]     | [ ]    | [ ]        | [ ]
Accuracy tests     | [ ]     | [ ]    | [ ]        | [ ]
95% accuracy       | [ ]     | [ ]    | [ ]        | [ ]
TOTAL: 0/18 checkmarks = 0% (Must reach 100%)
```

## Technical Details

### Canonical Categories Needing Better Classification
- TEMPORAL: Often mis-classified as QUERY
- STATUS: Often mis-classified as QUERY
- PRIORITY: Occasionally mis-classified as QUERY
- IDENTITY: Generally classifies well
- GUIDANCE: Generally classifies well

### Example Mis-classifications to Fix
- "show my calendar" → Should be TEMPORAL, not QUERY
- "what's my status" → Should be STATUS, not QUERY
- "list priorities" → Should be PRIORITY, not QUERY
- "schedule today" → Should be TEMPORAL, not QUERY

### Proposed QUERY Fallback
```python
# In workflow_factory.py
elif intent.category == IntentCategory.QUERY:
    # Check if it might be mis-classified canonical
    if any(term in intent.text.lower() for term in
           ['calendar', 'schedule', 'status', 'priority', 'standup']):
        # Route to appropriate canonical handler
        return self._route_to_canonical(intent)
    else:
        # Generic query handling
        workflow_type = WorkflowType.GENERATE_REPORT
```

## Dependencies
- GREAT-4E must be complete (validation done)
- Access to production logs for error analysis
- Ability to update classifier prompts
- CI/CD pipeline access for accuracy gates

## Time Estimate
2-3 hours (Small-Medium effort)
- ADR creation: 30 minutes
- QUERY fallback: 30 minutes
- Classifier prompt improvements: 1 hour
- Accuracy testing: 1 hour

## Priority
Medium - Improves UX but not blocking core functionality

## Notes
This epic addresses technical debt discovered during GREAT-4 validation. While not blocking, it will significantly improve user experience by eliminating timeout errors and formalizing an important architectural pattern.
