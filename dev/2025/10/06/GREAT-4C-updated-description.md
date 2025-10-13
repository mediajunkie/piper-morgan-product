# GREAT-4C: Handler Architecture Fixes - UPDATED

## Context
Third sub-epic of GREAT-4. Fixes critical architectural issues in the 5 canonical handlers, particularly hardcoded single-user assumptions.

## Background (Updated October 5, 2025)
Investigation revealed:
- Only 5 canonical handlers exist (not 219 - that was Slack handlers)
- Critical: Hardcoded "VA/Kind Systems" user context (single-user hack)
- Spatial intelligence patterns not integrated (violates ADRs)
- Missing error handling for service failures
- No caching for PIPER.md reads
- Performance already excellent (<1ms)

## Scope (Revised)

### 1. Remove Hardcoded User Context (CRITICAL)
- Eliminate hardcoded "VA/Kind Systems" string matching
- Implement proper user context service
- Enable multi-user support
- **Blocking for alpha release**

### 2. Integrate Spatial Intelligence
- Apply spatial patterns from ADRs
- Use appropriate pattern per handler
- Ensure architectural compliance

### 3. Add Error Handling
- Handle calendar service failures gracefully
- Handle missing PIPER.md files
- Provide helpful fallback responses
- Log failures for monitoring

### 4. Implement PIPER.md Caching
- Cache config reads (5-minute TTL)
- Reduce file I/O overhead
- Improve performance under load

### 5. Defer: Enhanced PIPER.md Parsing
- Create issue for structured parsing
- Current basic parsing works
- Enhancement can wait

## Acceptance Criteria
- [ ] Zero hardcoded user references
- [ ] Multi-user context service operational
- [ ] Spatial intelligence patterns applied
- [ ] All service failures handled gracefully
- [ ] PIPER.md caching implemented
- [ ] Enhancement issue created for parsing
- [ ] All handlers tested with multiple users
- [ ] No regression in performance (<1ms maintained)

## Success Validation
```bash
# Verify no hardcoded users
grep -r "VA\|Kind Systems" services/intent_service/
# Should return nothing

# Test multi-user support
python tests/intent/test_multi_user.py
# Different users get different contexts

# Test error handling
python tests/intent/test_handler_failures.py
# Graceful degradation confirmed

# Verify caching
python tests/intent/test_piper_cache.py
# Cache hits reduce file reads

# Performance maintained
python benchmark_intent.py
# Still <1ms average
```

## Anti-80% Check
```
Component     | Found | Fixed | Tested | Documented
------------- | ----- | ----- | ------ | ----------
Hardcoded     | [ ]   | [ ]   | [ ]    | [ ]
Multi-user    | [ ]   | [ ]   | [ ]    | [ ]
Spatial       | [ ]   | [ ]   | [ ]    | [ ]
Error Handle  | [ ]   | [ ]   | [ ]    | [ ]
Caching       | [ ]   | [ ]   | [ ]    | [ ]
TOTAL: 0/20 checkmarks = 0% (Must reach 100%)
```

## Priority Ranking
1. **CRITICAL**: Hardcoded context (blocks multi-user)
2. **HIGH**: Spatial intelligence (architectural violation)
3. **MEDIUM**: Error handling (UX impact)
4. **MEDIUM**: Caching (performance)
5. **DEFER**: PIPER.md parsing (works now)

## Time Estimate
2-3 hours (focused on critical/high priority items)
