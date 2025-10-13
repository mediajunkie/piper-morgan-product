# Gameplan: GREAT-4F - Classifier Accuracy & Canonical Pattern

**Date**: October 7, 2025
**Epic**: GREAT-4F (Sixth and final sub-epic of GREAT-4)
**Context**: Improve classifier accuracy and formalize canonical pattern
**Effort**: Small-Medium (2-3 hours)

## Mission

Address the 5-15% mis-classification rate for canonical intents discovered during GREAT-4E load testing. Formalize the canonical handler pattern with ADR documentation and add QUERY fallback to prevent timeout errors.

## Background

GREAT-4E revealed:
- Canonical handlers work perfectly when classification is correct
- ~5-15% of TEMPORAL/STATUS/PRIORITY queries mis-classify as QUERY
- No QUERY workflow exists → timeout errors
- Canonical pattern undocumented (no ADR)
- Tests have permissive assertions hiding failures

## Phase -1: Current State Verification
**Lead Developer WITH PM - MANDATORY**

### Verify Baseline
```bash
# Check current mis-classification examples
python3 -c "
from services.intent_service import IntentService
queries = [
    'show my calendar',  # Should be TEMPORAL
    'what is my status',  # Should be STATUS
    'list priorities'     # Should be PRIORITY
]
for q in queries:
    # Test classification
    print(f'{q}: {classify(q)}')
"

# Check for existing QUERY handling
grep -n "IntentCategory.QUERY" services/orchestration/workflow_factory.py

# Find permissive test assertions
grep -r "status_code in \[200, 404\]" tests/
```

### Questions for PM
1. Any specific mis-classification examples from users?
2. Should QUERY fallback try re-classification or just handle gracefully?
3. Priority of fixing permissive tests?

## Phase 0: ADR Documentation
**Code Agent - Small effort**

### Create ADR-043
`docs/adrs/adr-043-canonical-handler-pattern.md`:

Structure:
- **Title**: Canonical Handler Fast-Path Pattern
- **Status**: Approved
- **Context**: Need for fast simple query handling
- **Decision**: Dual-path architecture
  - Canonical: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
  - Workflow: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, etc.
- **Consequences**: Faster responses for simple queries
- **Implementation**: Line 123-131 in intent_service.py

## Phase 1: QUERY Fallback Implementation
**Code Agent - Small effort**

### In workflow_factory.py

Add intelligent QUERY handling:
```python
elif intent.category == IntentCategory.QUERY:
    # Smart fallback - check if likely mis-classified
    text_lower = intent.text.lower()

    # Pattern matching for likely canonical intents
    if any(pattern in text_lower for pattern in
           ['calendar', 'schedule', 'today', 'tomorrow']):
        # Likely TEMPORAL
        return self._create_temporal_workflow(intent)
    elif any(pattern in text_lower for pattern in
             ['status', 'standup', 'working on']):
        # Likely STATUS
        return self._create_status_workflow(intent)
    elif any(pattern in text_lower for pattern in
             ['priority', 'priorities', 'focus']):
        # Likely PRIORITY
        return self._create_priority_workflow(intent)
    else:
        # True generic query
        workflow_type = WorkflowType.GENERATE_REPORT
```

## Phase 2: Classifier Prompt Enhancement
**Cursor Agent - Medium effort**

### Find and Update Classifier Prompts

Location likely in:
- `services/llm/prompts/intent_classifier.py`
- Or embedded in IntentClassifier

Add disambiguation rules:
```python
# Add to classifier prompt
DISAMBIGUATION_RULES = """
TEMPORAL vs QUERY:
- If asking about time, dates, calendar, schedule → TEMPORAL
- If asking for general information → QUERY

STATUS vs QUERY:
- If asking about current work, standup, projects → STATUS
- If asking for general information → QUERY

PRIORITY vs QUERY:
- If asking about priorities, focus, importance → PRIORITY
- If asking for general rankings → QUERY
"""
```

## Phase 3: Classification Accuracy Testing
**Cursor Agent - Medium effort**

### Create Accuracy Test Suite

`tests/intent/test_classification_accuracy.py`:

```python
class TestCanonicalAccuracy:
    """Test canonical categories achieve 95% accuracy"""

    TEMPORAL_VARIANTS = [
        "what's on my calendar",
        "show my schedule",
        "calendar for today",
        "what time is my meeting",
        # ... 50+ variants
    ]

    def test_temporal_accuracy(self):
        correct = 0
        for query in self.TEMPORAL_VARIANTS:
            result = classify(query)
            if result.category == IntentCategory.TEMPORAL:
                correct += 1

        accuracy = correct / len(self.TEMPORAL_VARIANTS)
        assert accuracy >= 0.95, f"TEMPORAL accuracy {accuracy} < 95%"
```

## Phase 4: Fix Permissive Tests
**Code Agent - Small effort**

### Update Tests with Strict Assertions

Files to fix (from yesterday's investigation):
1. `tests/intent/test_user_flows_complete.py:150`
2. `tests/integration/test_no_web_bypasses.py:44`
3. `tests/integration/test_no_web_bypasses.py:89`

Change:
```python
# BEFORE (permissive)
assert response.status_code in [200, 404]

# AFTER (strict)
assert response.status_code == 200, "Health check MUST return 200"
```

## Phase Z: Validation & Metrics
**Both Agents**

### Measure Improvement
```bash
# Test classification accuracy
python tests/intent/test_classification_accuracy.py -v
# Target: 95%+ for canonical categories

# Test QUERY fallback
echo "show my calendar" | python test_intent.py
# Should not timeout

# Verify no workflow errors
tail -n 1000 logs/app.log | grep "No workflow type found"
# Should be empty or greatly reduced

# Verify tests are strict
grep -r "in \[200, 404\]" tests/
# Should return nothing
```

### Update Documentation
- Update Pattern-032 with accuracy metrics
- Document QUERY fallback strategy
- Add classification tips to developer guide

## Success Criteria

- [ ] ADR-043 created documenting canonical pattern (PM will validate)
- [ ] QUERY fallback implemented and tested (PM will validate)
- [ ] Classifier prompts enhanced with disambiguation (PM will validate)
- [ ] Accuracy tests show 95%+ for canonical categories (PM will validate)
- [ ] 3 permissive tests fixed to strict assertions (PM will validate)
- [ ] No timeout errors for mis-classified queries (PM will validate)
- [ ] Documentation updated (PM will validate)

## Anti-80% Check
```
Component        | Implemented | Tested | Documented | Verified
---------------- | ----------- | ------ | ---------- | --------
ADR-043          | [ ]         | N/A    | [ ]        | [ ]
QUERY fallback   | [ ]         | [ ]    | [ ]        | [ ]
Prompt enhance   | [ ]         | [ ]    | [ ]        | [ ]
Accuracy tests   | [ ]         | [ ]    | [ ]        | [ ]
Test fixes       | [ ]         | [ ]    | [ ]        | [ ]
95% accuracy     | [ ]         | [ ]    | [ ]        | [ ]
```

## Agent Division

**Code Agent** - Phases 0, 1, 4
- ADR creation
- QUERY fallback implementation
- Fix permissive tests

**Cursor Agent** - Phases 2, 3
- Classifier prompt enhancement
- Accuracy test creation
- Accuracy measurement

**Both** - Phase Z
- Final validation
- Documentation updates

## STOP Conditions

- If classifier prompts not found where expected
- If QUERY fallback causes performance issues
- If accuracy cannot reach 95% with prompt changes alone
- If more than 3 tests have permissive patterns

## Critical Notes

- QUERY fallback should be smart, not just keyword matching
- Test fixes are critical for preventing future issues
- ADR should explain WHY dual-path exists
- Accuracy testing should cover edge cases

---

*Ready to complete GREAT-4 epic!*
