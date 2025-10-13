# Gameplan: GREAT-4D - Missing Handler Implementation

**Date**: October 6, 2025
**Epic**: GREAT-4D (Fourth sub-epic of GREAT-4)
**Context**: EXECUTION and ANALYSIS handlers return placeholder messages

## Mission

Implement missing EXECUTION and ANALYSIS intent handlers that currently return "Phase 3C will implement" placeholder messages.

## Background

Investigation revealed two intent categories with placeholder implementations. Intents classify correctly but handlers are missing. This unfinished work must be completed per Great Refactor mission.

## Phase -1: Infrastructure Verification
**Lead Developer WITH PM - MANDATORY**

### Current Understanding
Based on GREAT-4C findings:
- Intent classification exists and works
- 5 canonical handlers implemented
- EXECUTION and ANALYSIS return placeholders
- Services exist for GitHub, Notion, etc.

### PM Verification Required
Please run these commands to verify:
```bash
# Check for EXECUTION/ANALYSIS placeholders
grep -r "Phase 3C" services/intent_service/ --include="*.py"
grep -r "EXECUTION\|ANALYSIS" services/intent_service/ --include="*.py"

# Check for existing services we can use
ls -la services/github_service/
ls -la services/notion_service/
ls -la services/

# Check intent routing structure
grep -r "def route\|def handle" services/intent_service/ --include="*.py"
```

### Questions for PM
1. Do GitHub/Notion services have methods for create/update operations?
2. What services exist for ANALYSIS operations?
3. Are there existing patterns for handler implementation?
4. Any known issues with EXECUTION/ANALYSIS?

If infrastructure differs significantly, STOP and revise gameplan.

## Phase 0: Discovery & Investigation
**Both Agents - Small effort**

### Investigate Current State
Agents should discover:
- Exact placeholder messages
- How intents route to handlers
- Available service methods
- Existing handler patterns from the 5 working handlers

### Document Findings
Create `dev/2025/10/06/handler-discovery.md` with:
- Services available for EXECUTION
- Services available for ANALYSIS
- Handler pattern to follow
- Specific intents needing handlers

## Phase 1: EXECUTION Handler Implementation
**Code Agent - Large effort**

### Handler Structure
Following pattern from existing handlers:
- Check existing handler patterns
- Implement similar structure
- Connect to appropriate services
- Apply multi-user context from 4C
- Add error handling from 4C patterns

### Expected EXECUTION Operations
Based on investigation, implement handlers for:
- CREATE operations (issues, documents, etc.)
- UPDATE operations (modify existing items)
- DELETE operations (with confirmation)

Note: Exact methods depend on Phase 0 discovery

## Phase 2: ANALYSIS Handler Implementation
**Cursor Agent - Large effort**

### Handler Structure
Following discovered patterns:
- Implement analysis handlers
- Connect to data services
- Apply spatial intelligence where relevant
- Cache expensive operations if needed

### Expected ANALYSIS Operations
Based on investigation, implement handlers for:
- Data analysis operations
- Report generation
- Metric evaluation
- Comparison operations

Note: Exact methods depend on Phase 0 discovery

## Phase 3: Integration & Routing
**Code Agent - Medium effort**

### Wire Handlers
- Connect new handlers to intent router
- Remove placeholder responses
- Ensure proper routing
- Test intent flow

### Verify Integration
- Each intent routes correctly
- Services properly initialized
- Error handling works
- Multi-user context applied

## Phase 4: Testing
**Cursor Agent - Medium effort**

### Create Handler Tests
- Unit tests for each handler
- Integration tests for routing
- Error case tests
- Multi-user tests

### Test Coverage
- All EXECUTION operations tested
- All ANALYSIS operations tested
- Error scenarios handled
- Performance verified

## Phase Z: Documentation & Validation
**Both Agents**

### Remove Placeholders
```bash
# Verify no placeholders remain
grep -r "Phase 3C" . --include="*.py"
# Should return nothing
```

### Update Documentation
- Update handler documentation
- Document new capabilities
- Update relevant ADRs if needed

### Final Validation
- All tests passing
- Performance <100ms
- No placeholders remain
- GitHub issue updated

## Success Criteria

- [ ] All EXECUTION intents have working handlers (PM will validate)
- [ ] All ANALYSIS intents have working handlers (PM will validate)
- [ ] Zero "Phase 3C" references remain (PM will validate)
- [ ] Tests created and passing (PM will validate)
- [ ] Integration verified (PM will validate)
- [ ] Documentation updated (PM will validate)
- [ ] Performance maintained <100ms (PM will validate)

## Anti-80% Check

Agents should track completion:
```
Component    | Found | Implemented | Tested | Integrated
------------ | ----- | ----------- | ------ | ----------
EXECUTION    | [ ]   | [ ]         | [ ]    | [ ]
ANALYSIS     | [ ]   | [ ]         | [ ]    | [ ]
Routing      | [ ]   | [ ]         | [ ]    | [ ]
Placeholders | [ ]   | [ ]         | [ ]    | [ ]
```

## Effort Indicators

- Phase -1: Infrastructure verification (with PM)
- Phase 0: Discovery (small)
- Phase 1: EXECUTION handlers (large)
- Phase 2: ANALYSIS handlers (large)
- Phase 3: Integration (medium)
- Phase 4: Testing (medium)
- Phase Z: Documentation (small)

## Agent Division

**Claude Code** - Phases 0, 1, 3
- Discovery and investigation
- EXECUTION handler implementation
- Integration and routing

**Cursor Agent** - Phases 2, 4, Z (partial)
- ANALYSIS handler implementation
- Test creation and execution
- Cross-validation of Code's work

## Critical Notes

- Do NOT assume handler structure - discover from existing patterns
- Do NOT hardcode service methods - use what exists
- Follow multi-user patterns from GREAT-4C
- Apply error handling patterns from GREAT-4C
- Verify all "Phase 3C" placeholders removed

## STOP Conditions

- Infrastructure doesn't match expectations
- Services don't have needed methods
- Pattern unclear from existing code
- Performance degrades below 100ms

---

*Ready to complete missing handler implementation*
