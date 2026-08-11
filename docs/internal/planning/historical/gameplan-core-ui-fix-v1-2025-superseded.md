# Gameplan: CORE-UI Fix Layer 3 Intent Processing Pipeline

## Context
- **Issue**: Bug #166 child - CORE-UI Layer 3 investigation
- **Complexity**: High (architectural issue affecting multiple layers)
- **Lead Developer**: Tomorrow morning session
- **Agents**: Claude Code (investigation) + Cursor (UI validation)

## Phase -1: MANDATORY Infrastructure Verification

### Part A: What I Think Exists
Based on today's architectural review:
1. **Intent system exists**: Full `services/intent_service/` directory
2. **Web framework**: FastAPI at `web/app.py`
3. **Port**: 8001 for local development
4. **Current issue**: Layer 3 intent→handler→response disconnection
5. **Multiple prompts affected**: Not just standup

### Part B: PM Verification Required
```bash
# Verify intent service structure
ls -la services/intent_service/
cat services/intent_service/__init__.py

# Check web app endpoints
grep -A 10 "@app.post" web/app.py
grep -A 10 "@app.get" web/app.py

# Look for intent routing
grep -r "intent_classifier" web/ --include="*.py"
grep -r "process_intent" web/ --include="*.py"

# Check if server is running
ps aux | grep python
curl http://localhost:8001/health -v
```

### Part C: Proceed/Revise Decision
- [ ] PROCEED if intent service structure matches expectations
- [ ] REVISE if architecture different than expected
- [ ] CLARIFY if intent→handler wiring unclear

## Phase 0: Investigation & GitHub Setup (MANDATORY)

### All Agents Must
1. Verify GitHub issue #166 exists and read full context
2. Create child issue CORE-UI as specified
3. Search for Layer 3 patterns in codebase
4. Document current pipeline flow

```bash
# GitHub verification
gh issue view 166

# Pattern search
grep -r "Layer 3" . --include="*.md"
grep -r "intent.*handler" services/ --include="*.py"
grep -r "response.*transform" services/ --include="*.py"

# Map the pipeline
find . -name "*intent*.py" -type f
find . -name "*handler*.py" -type f
find . -name "*response*.py" -type f
```

## Phase 1: Pipeline Mapping & Diagnosis

### Multi-Agent Division
**Claude Code** - Backend Investigation
- Map complete intent→handler flow
- Identify disconnection points
- Test intent classifier directly
- Check response transformation

**Cursor Agent** - UI Symptom Documentation
- Document all affected prompts
- Capture browser console errors
- Test various input patterns
- Screenshot hanging states

### Coordination Points
- Share findings after mapping complete
- Cross-reference backend issues with UI symptoms
- Identify pattern in failures

## Phase 2: Fix Implementation

### Critical Areas to Check
1. **Intent Classifier Wiring**
   ```python
   # services/intent_service/intent_classifier.py
   # Check if all endpoints use this
   ```

2. **Handler Registration**
   ```python
   # Where handlers register with intents
   # May be in application layer
   ```

3. **Response Pipeline**
   ```python
   # How responses get back to UI
   # Check for transformation failures
   ```

### Implementation Approach
- Fix one endpoint first as proof of concept
- Validate fix with that endpoint
- Apply pattern to all affected endpoints
- Ensure no direct bypasses remain

## Phase 3: Validation & Testing

### Cross-Validation Protocol
**Code Tests**:
- Unit tests for intent→handler connection
- Integration tests for full pipeline
- Performance tests (<100ms)

**Cursor Tests**:
- All previously hanging prompts work
- No UI freezes or timeouts
- Console errors eliminated
- User experience smooth

## STOP Conditions
- Intent service architecture different than expected → STOP
- Cannot reproduce the hang → STOP, need more info
- Fix affects other working features → STOP, architectural review needed
- Performance degrades significantly → STOP

## Success Criteria
- [ ] All hanging prompts identified
- [ ] Root cause in Layer 3 documented
- [ ] Fix implemented and tested
- [ ] No regressions introduced
- [ ] Performance maintained (<100ms)
- [ ] Browser testing confirms resolution
- [ ] GitHub issue updated with evidence

## Time Estimate
- Phase 0: 30 minutes (investigation)
- Phase 1: 60 minutes (mapping & diagnosis)
- Phase 2: 90 minutes (fix implementation)
- Phase 3: 60 minutes (validation)
- Total: ~4 hours

## Evidence Requirements
- Pipeline flow diagram
- Before/after terminal output
- Browser screenshots showing fix
- Test results with timing
- Git commits with clear messages

## Notes for Lead Developer

### Known Context
- Previous Layer 1 & 2 fixes completed
- Layer 3 specifically identified as issue
- Multiple prompts affected (not standup-specific)
- Intent system exists but may not be fully wired

### Architecture References
- Intent service: `services/intent_service/`
- Web app: `web/app.py`
- Spatial patterns: `services/integrations/spatial/`

### Critical Success Factor
This blocks ALL further development. Fixing this unblocks:
- Testing of all features
- Plugin architecture work
- Intent classification universalization
- Learning implementation

---
*Gameplan Version: 1.0*
*Issue: CORE-UI (child of #166)*
*Priority: CRITICAL - Blocking all development*
