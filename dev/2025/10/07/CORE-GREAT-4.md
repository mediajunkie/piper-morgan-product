# CORE-GREAT-4: Intent Universalization Epic

## Title
CORE-GREAT-4: Universal Intent Classification - No Bypass

## Labels
epic, refactor, intent, ai, great-refactor

## Description

## Overview
Make intent classification mandatory for all user interactions. Remove all direct endpoint access.

## Background
- Some endpoints bypass intent classification
- Direct API calls skip intent layer
- CLI commands may not use intent
- Inconsistent user experience across interfaces
- ADR-032 (Intent Classification Universal Entry) exists but not fully implemented

## Pre-Work: ADR Review
- [ ] Review ADR-032 (Intent Classification Universal Entry) for requirements
- [ ] Review ADR-003 (Intent Classifier Enhancement) for patterns
- [ ] Review ADR-016 (Ambiguity Driven) for classification strategy
- [ ] Run verification commands to find all endpoints
- [ ] Map all current bypass routes
- [ ] Document which interfaces use intent vs direct calls
- [ ] Identify any special cases that might need exemption
- [ ] Update ADRs based on universalization results

## Acceptance Criteria
- [ ] 100% of user interactions pass through intent classification
- [ ] No direct endpoint calls possible
- [ ] Consistent behavior across all entry points
- [ ] Intent patterns documented
- [ ] Web UI uses intent for all interactions
- [ ] CLI uses intent for all commands
- [ ] Slack uses intent for all messages
- [ ] API endpoints route through intent
- [ ] No bypass routes remain

## Tasks
- [ ] Complete ADR pre-work review
- [ ] **Map all current endpoints**:
  - [ ] Web UI endpoints
  - [ ] CLI command endpoints
  - [ ] API REST endpoints
  - [ ] Slack webhook endpoints
  - [ ] Any other entry points
- [ ] **Route endpoints through intent**:
  - [ ] Convert web UI to intent-first
  - [ ] Convert CLI to intent-first
  - [ ] Convert API to intent-first
  - [ ] Convert Slack to intent-first
- [ ] **Remove direct access**:
  - [ ] Remove direct endpoint routes
  - [ ] Remove bypass mechanisms
  - [ ] Remove fallback direct calls
- [ ] **Test every user flow**:
  - [ ] Test all web UI interactions
  - [ ] Test all CLI commands
  - [ ] Test all API calls
  - [ ] Test all Slack commands
- [ ] Document all intent patterns
- [ ] Add intent classification metrics
- [ ] Create intent bypass detection test
- [ ] Add intent coverage reporting
- [ ] Update ADR-032 with implementation details
- [ ] Create intent pattern guide

## Lock Strategy
- Direct endpoints removed from codebase
- Intent required in API gateway
- 100% test coverage for intent routing
- No bypass routes possible
- Intent bypass detection in CI
- Intent metrics dashboard active
- All related ADRs updated

## Dependencies
- CORE-GREAT-3 must be 100% complete (plugins define intent interface)

## Estimated Duration
1 week

## Success Validation
```bash
# Every user interaction should show intent classification
tail -f logs/app.log | grep "intent_classification"
# Should show continuous entries for ALL interactions

# No direct routes should exist
grep -r "@app.route" . --include="*.py" | grep -v "intent"
# Should only show intent endpoint

# Attempting direct endpoint access should fail
curl -X POST http://localhost:8001/api/github/create_issue
# Should return 404 or redirect to intent

# Intent coverage should be 100%
python measure_intent_coverage.py
# Output: Intent Coverage: 100%
```

## Intent Checklist

### Entry Points
- [ ] Web UI chat → intent
- [ ] Web UI buttons → intent
- [ ] CLI commands → intent
- [ ] API endpoints → intent
- [ ] Slack messages → intent
- [ ] Slack commands → intent
- [ ] Webhook calls → intent

### Bypass Elimination
- [ ] No direct service calls from UI
- [ ] No direct repository access from API
- [ ] No command shortcuts bypassing intent
- [ ] No admin overrides of intent
- [ ] No emergency bypass routes

### Monitoring & Metrics
- [ ] Intent classification logged
- [ ] Classification confidence tracked
- [ ] Bypass attempts detected
- [ ] Coverage metrics reported
- [ ] Performance impact measured

## User Flow Validation
- [ ] "Create GitHub issue" → intent → success
- [ ] "Show standup" → intent → success
- [ ] "Upload document" → intent → success
- [ ] "Search knowledge" → intent → success
- [ ] "Send Slack message" → intent → success
- [ ] All CLI commands → intent → success

---

**Note**: This epic follows the Inchworm Protocol - must be 100% complete before moving to CORE-GREAT-5
