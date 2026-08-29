# GREAT-4B: Universal Intent Enforcement - SYNTHESIZED

## Context
Second sub-epic of GREAT-4. Makes intent classification mandatory for ALL user interactions by creating/completing middleware and removing bypass routes.

## Background
Currently, many endpoints bypass intent classification, leading to inconsistent behavior. Some interfaces use direct service calls, others use intent. This creates confusion and prevents learning system observation. Based on GREAT-4A findings and the 75% pattern, we expect partial implementation exists.

## Pre-Investigation Expectations
- Intent middleware likely partially exists
- Some endpoints already use intent (estimate 60-75%)
- Clear reasons for bypasses (performance, legacy code)
- Need consistency enforcement more than ground-up building

## Scope

### 1. Discovery & Mapping
- Map ALL entry points before assumptions
- Identify which use intent vs direct calls
- Document bypass reasons
- Check for existing middleware

### 2. Create/Complete Intent Middleware
- FastAPI middleware for web (check if partial exists)
- CLI wrapper for commands
- Slack event interceptor
- API gateway enforcement

### 3. Convert All Interfaces
- Web UI to intent-first
- CLI to intent-first
- API to intent-first
- Slack to intent-first
- Webhooks to intent-first

### 4. Remove Bypass Routes
- Delete direct endpoint routes
- Remove service shortcuts
- Eliminate fallback mechanisms
- Block admin overrides

### 5. Add Caching Layer
- Cache frequent classifications
- Reduce latency impact
- Implement cache invalidation
- Monitor cache hit rates

## Acceptance Criteria
- [ ] All entry points mapped and documented
- [ ] Intent middleware created/completed and active
- [ ] Web UI: 100% interactions through intent
- [ ] CLI: All commands through intent
- [ ] API: All endpoints through intent
- [ ] Slack: All messages through intent
- [ ] Webhooks: All calls through intent
- [ ] Zero direct service calls remaining
- [ ] Zero bypass routes accessible
- [ ] Caching layer operational
- [ ] Cache hit rate >60% for common queries
- [ ] No increase in latency >50ms
- [ ] Intent bypass detection test passing

## Success Validation
```bash
# Map current state first
python scripts/map_intent_usage.py
# Shows baseline: X% using intent

# Verify middleware active
grep "IntentMiddleware" web/app.py
# Should show middleware registered

# Check for bypasses eliminated
grep -r "@app.route" . --include="*.py" | grep -v "intent"
# Should return nothing (only intent routes)

# Test direct access fails
curl -X POST http://localhost:8001/api/github/create_issue -d '{"title":"test"}'
# Should return 404 or redirect

# Verify CLI uses intent
python cli/piper.py create issue --debug
# Should show "Intent classification: CREATE_ISSUE"

# Check cache working
redis-cli KEYS "intent:*" | wc -l
# Should show cached entries

# Run bypass detection
pytest tests/intent/test_no_bypasses.py -v
# All tests pass

# Final verification
python scripts/map_intent_usage.py
# Shows: 100% using intent
```

## Anti-80% Check
```
Interface    | Found | Mapped | Converted | Tested | Blocked | Cached
------------ | ----- | ------ | --------- | ------ | ------- | ------
Web UI       | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
CLI          | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
API          | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Slack        | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Webhooks     | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Middleware   | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
Direct calls | [ ]   | [ ]    | [ ]       | [ ]    | [ ]     | [ ]
TOTAL: 0/42 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
4-6 hours (reduced from 6-8 due to expected partial implementation)

## Key Changes from Original
1. Added discovery phase based on 4A lessons
2. Added "Found" column to Anti-80% checklist
3. Acknowledges middleware likely partial exists
4. Includes baseline measurement before changes
5. Explicit about checking for existing implementation first
