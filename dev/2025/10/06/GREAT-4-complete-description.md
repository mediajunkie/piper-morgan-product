# GREAT-4: Intent Classification Universal

## Overview
Transform intent classification from optional feature to mandatory universal entry point for ALL user interactions. No bypasses allowed. Remove all direct endpoint access.

## Background (October 5, 2025)
- Plugin architecture complete (GREAT-3 ✅)
- Layer 3 intent access fixed (#172 ✅)
- Intent system exists but is often bypassed
- Multiple CORE tickets need consolidation (#96, #176, #179)
- ADR-032 defines vision but implementation incomplete
- Some endpoints bypass intent classification entirely
- Direct API calls skip intent layer
- CLI commands may not use intent
- Inconsistent user experience across interfaces

## Current State
- Intent classifier exists at `services/intent_service/`
- Some endpoints bypass classification entirely
- Missing intent categories (TEMPORAL, STATUS, PRIORITY)
- Generic/undefined responses from intent handlers
- No universal enforcement mechanism
- Direct service calls still possible from UI
- Command shortcuts bypassing intent exist

## Pre-Work: ADR Review
- [ ] Review ADR-032 (Intent Classification Universal Entry) for requirements
- [ ] Review ADR-003 (Intent Classifier Enhancement) for patterns
- [ ] Review ADR-016 (Ambiguity Driven) for classification strategy
- [ ] Map all current bypass routes
- [ ] Document which interfaces use intent vs direct calls
- [ ] Identify any special cases that might need exemption

## Scope

### Foundation & Categories (4A)
- Add missing intent categories per #96
- Fix pattern loading and classification accuracy
- Establish comprehensive test coverage
- Baseline performance metrics
- Document all intent patterns

### Universal Enforcement (4B)
- Create intent classification middleware
- Route ALL interactions through classifier
- Remove direct endpoint bypasses
- Convert all interfaces to intent-first
- Implement caching for performance

### Quality & Performance (4C)
- Fix generic/undefined responses (#179)
- Optimize processing to <100ms target
- Improve classification accuracy to >80%
- Add context-aware responses
- Implement intent metrics and monitoring

### Validation & Documentation (4D)
- Contract tests for universal coverage
- User flow validation for all paths
- Performance benchmarks
- Update ADR-032 with implementation
- Create intent pattern guide

## Decomposition into Sub-Epics

### GREAT-4A: Foundation & Categories (4-6 hours)
### GREAT-4B: Universal Enforcement (6-8 hours)
### GREAT-4C: Quality & Performance (4-6 hours)
### GREAT-4D: Validation & Documentation (2-3 hours)

(See individual sub-epic descriptions for details)

## Complete Acceptance Criteria

### Foundation (4A)
- [ ] All 3 new categories added and tested (TEMPORAL, STATUS, PRIORITY)
- [ ] Canonical queries classify correctly
- [ ] Pattern loading verified
- [ ] Baseline metrics established
- [ ] All intent patterns documented

### Enforcement (4B)
- [ ] Intent middleware operational
- [ ] 100% of endpoints use classifier
- [ ] Zero bypass routes remain
- [ ] All interfaces converted to intent-first
- [ ] Caching layer functional

### Quality (4C)
- [ ] No undefined responses
- [ ] <100ms processing time
- [ ] >80% accuracy on test set
- [ ] Context-aware responses working
- [ ] Intent metrics dashboard active

### Validation (4D)
- [ ] All user flow tests passing
- [ ] Performance validated
- [ ] Documentation complete
- [ ] Migration guide created
- [ ] ADR-032 updated with implementation

## Entry Point Checklist

### Must Use Intent
- [ ] Web UI chat → intent
- [ ] Web UI buttons → intent
- [ ] CLI commands → intent
- [ ] API endpoints → intent
- [ ] Slack messages → intent
- [ ] Slack commands → intent
- [ ] Webhook calls → intent

### Must Eliminate
- [ ] No direct service calls from UI
- [ ] No direct repository access from API
- [ ] No command shortcuts bypassing intent
- [ ] No admin overrides of intent
- [ ] No emergency bypass routes

## User Flow Validation Tests
- [ ] "Create GitHub issue" → intent → success
- [ ] "Show standup" → intent → success
- [ ] "Upload document" → intent → success
- [ ] "Search knowledge" → intent → success
- [ ] "Send Slack message" → intent → success
- [ ] All CLI commands → intent → success

## Lock Strategy
- Middleware tests prevent bypasses
- Direct endpoints removed from codebase
- Intent required in API gateway
- 100% test coverage for intent routing
- Intent bypass detection in CI
- Coverage reports show 100%
- Performance tests prevent regression

## Dependencies
- ✅ GREAT-3 (Plugin Architecture complete)
- ✅ #172 (Layer 3 access fixed)
- ✅ CORE-PLUG (#173) superseded by GREAT-3

## Success Validation
```bash
# Every user interaction shows intent classification
tail -f logs/app.log | grep "intent_classification"
# Continuous entries for ALL interactions

# No direct routes exist
grep -r "@app.route" . --include="*.py" | grep -v "intent"
# Only intent endpoint shown

# Direct endpoint access fails
curl -X POST http://localhost:8001/api/github/create_issue
# Returns 404 or redirects to intent

# Intent coverage 100%
python measure_intent_coverage.py
# Output: Intent Coverage: 100%

# Performance meets targets
python benchmark_intent.py
# <100ms average

# Accuracy validated
pytest tests/intent/accuracy/ -v
# >80% accuracy
```

## Monitoring & Metrics
- [ ] Intent classification logged
- [ ] Classification confidence tracked
- [ ] Bypass attempts detected
- [ ] Coverage metrics reported
- [ ] Performance impact measured
- [ ] Intent patterns analytics
- [ ] Error rate monitoring

## Issues This Supersedes
When complete, close:
- #96 (CORE-INTENT-CAT) - Categories added in 4A
- #176 (CORE-INTENT-ENFORCE) - Universal enforcement in 4B
- #179 (CORE-INTENT-QUALITY) - Quality fixes in 4C

## Anti-80% Checklist
```
Component    | Found | Fixed | Tested | Enforced | Monitored
------------ | ----- | ----- | ------ | -------- | ---------
Categories   | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Patterns     | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Middleware   | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Web UI       | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
CLI          | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
API          | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Slack        | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Webhooks     | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Caching      | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Accuracy     | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Performance  | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
Monitoring   | [ ]   | [ ]   | [ ]    | [ ]      | [ ]
TOTAL: 0/60 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
16-23 hours (2-3 days based on GREAT-3 velocity)

---

**Note**: This epic follows the Inchworm Protocol - must be 100% complete before moving to GREAT-5
