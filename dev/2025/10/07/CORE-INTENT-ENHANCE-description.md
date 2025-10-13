# CORE-INTENT-ENHANCE: Classification Accuracy & Pre-Classifier Optimization

## Context
Follow-up to GREAT-4F. While core categories achieved 95%+ accuracy, IDENTITY and GUIDANCE remain at ~76%. Additionally, pre-classifier could handle more patterns for faster responses.

## Current State (Post-GREAT-4F)
- PRIORITY: 100% accuracy ✅
- TEMPORAL: 96.7% accuracy ✅
- STATUS: 96.7% accuracy ✅
- IDENTITY: 76% accuracy ⚠️
- GUIDANCE: 76.7% accuracy ⚠️
- Pre-classifier: ~1% hit rate (mostly just "help")
- QUERY fallback: Working, prevents timeouts

## Scope

### 1. IDENTITY Classification Enhancement (76% → 90%+)
**Problem**: Capability questions often mis-classify as QUERY
- "What can you do?" → QUERY (should be IDENTITY)
- "What are your features?" → QUERY (should be IDENTITY)
- "Tell me about yourself" → Sometimes CONVERSATION

**Solution**:
- Add capability/feature keyword patterns to classifier prompt
- Emphasize "can you", "what can", "your capabilities", "your features"
- Add examples of IDENTITY vs QUERY disambiguation
- Test with 50+ capability question variants

### 2. GUIDANCE Classification Enhancement (76.7% → 90%+)
**Problem**: Advice requests mis-classify as CONVERSATION or STRATEGY
- "How should I approach this?" → varies unpredictably
- "What's the best way to..." → Sometimes STRATEGY
- "Can you guide me..." → Sometimes CONVERSATION

**Solution**:
- Strengthen GUIDANCE vs STRATEGY disambiguation
- Add "how-to", "best way", "should I" patterns
- Emphasize advice/recommendation signals
- Test with 50+ guidance question variants

### 3. Pre-Classifier Pattern Expansion (~1% → 10%+ hit rate)
**Current**: Only catches "help" and a few others

**Add Pattern Sets**:

**TEMPORAL patterns** (instant recognition):
```python
TEMPORAL_PATTERNS = [
    r'\b(calendar|schedule|appointment|meeting)\b',
    r'\b(today|tomorrow|this week|next week)\b',
    r'\bwhat.{0,10}(day|date|time)\b',
    r'\bwhen is\b',
    # ... more patterns
]
```

**STATUS patterns** (instant recognition):
```python
STATUS_PATTERNS = [
    r'\b(standup|stand-up|status)\b',
    r'\bworking on\b',
    r'\bcurrent (task|project|work)\b',
    r'\bmy progress\b',
    # ... more patterns
]
```

**PRIORITY patterns** (instant recognition):
```python
PRIORITY_PATTERNS = [
    r'\b(priority|priorities)\b',
    r'\b(urgent|important|critical)\b',
    r'\bfocus on\b',
    r'\btop items?\b',
    # ... more patterns
]
```

## Acceptance Criteria

- [ ] IDENTITY accuracy ≥ 90% (50+ test queries)
- [ ] GUIDANCE accuracy ≥ 90% (50+ test queries)
- [ ] Pre-classifier hit rate ≥ 10% on common queries
- [ ] Pre-classifier patterns for TEMPORAL working
- [ ] Pre-classifier patterns for STATUS working
- [ ] Pre-classifier patterns for PRIORITY working
- [ ] No regression in other categories (all stay >75%)
- [ ] Performance maintained (<100ms for pre-classifier)
- [ ] Documentation updated with new patterns

## Success Validation
```bash
# Test IDENTITY accuracy
python tests/intent/test_classification_accuracy.py::test_identity_accuracy -v
# Should show ≥90% accuracy

# Test GUIDANCE accuracy
python tests/intent/test_classification_accuracy.py::test_guidance_accuracy -v
# Should show ≥90% accuracy

# Test pre-classifier hit rate
python tests/intent/test_pre_classifier.py -v
# Should show ≥10% hit rate on common queries

# Verify no regression
python tests/intent/test_classification_accuracy.py -v
# All categories should maintain or improve accuracy

# Performance check
python benchmark_pre_classifier.py
# Should maintain <100ms (likely <10ms) for pattern matching
```

## Implementation Strategy

### Phase 1: IDENTITY Enhancement
1. Analyze current mis-classifications
2. Identify capability/feature keywords
3. Update classifier prompt
4. Test with 50+ variants
5. Iterate until ≥90%

### Phase 2: GUIDANCE Enhancement
1. Analyze GUIDANCE vs STRATEGY confusion
2. Identify advice/recommendation signals
3. Update classifier prompt
4. Test with 50+ variants
5. Iterate until ≥90%

### Phase 3: Pre-Classifier Expansion
1. Add TEMPORAL pattern set
2. Add STATUS pattern set
3. Add PRIORITY pattern set
4. Test hit rate on real queries
5. Optimize patterns for coverage vs false positives

### Phase 4: Validation
1. Run full accuracy suite
2. Verify no regressions
3. Update documentation
4. Create pattern guide

## Technical Details

### Files to Modify
- `services/llm/prompts/intent_classifier.py` (or embedded prompts)
- `services/intent_service/pre_classifier.py`
- `tests/intent/test_classification_accuracy.py`
- `docs/guides/intent-classification-guide.md`

### Test Data Needed
- 50+ IDENTITY queries covering capability questions
- 50+ GUIDANCE queries covering advice requests
- 100+ common queries for pre-classifier hit rate testing
- Regression test set for all 13 categories

## Risk Mitigation
- QUERY fallback remains as safety net
- Test all categories to prevent regression
- Keep pattern matching simple for performance
- Document all pattern changes

## Time Estimate
4-6 hours total:
- IDENTITY enhancement: 1-2 hours
- GUIDANCE enhancement: 1-2 hours
- Pre-classifier patterns: 1-2 hours
- Testing and documentation: 1 hour

## Priority
Medium - Valuable but not blocking:
- System works at current accuracy levels
- QUERY fallback prevents failures
- This is optimization, not critical fix

## Success Metrics
- IDENTITY: 76% → 90%+ (14+ point improvement)
- GUIDANCE: 76.7% → 90%+ (13.3+ point improvement)
- Pre-classifier: ~1% → 10%+ hit rate (10x improvement)
- Overall canonical accuracy: 89.3% → 94%+
- User experience: Fewer mis-classifications, faster responses

## Notes
This enhancement builds on GREAT-4F discoveries. While not critical for alpha/production, these improvements will significantly enhance user experience by reducing mis-classifications and speeding up common queries through pre-classifier optimization.
