# CORE-CRAFT-VALID: Verification & Validation

## Context
Final verification that all GREAT refactor work is genuinely complete and functional. Uses Serena MCP for systematic audit plus comprehensive integration testing.

## Current State
- No systematic verification performed yet
- Integration tests check structure more than function
- Evidence collection ad-hoc
- Completion claims unverified

## Scope

### VALID-1: Serena-Powered Final Audit
**Duration**: 3-5 hours

**Systematic Verification**:
- Extract all completion claims from GREAT documentation
- Use Serena to verify each claim against actual code
- Count actual files, lines, tests, patterns
- Identify any remaining placeholders
- Generate discrepancy report

**Audit Coverage**:
```python
# For each GREAT epic
for epic in ["GREAT-1", "GREAT-2", "GREAT-3", "GREAT-4*", "GREAT-5"]:
    - Claimed completion percentage
    - Actual completion (Serena-verified)
    - Specific gaps identified
    - Evidence collected
```

### VALID-2: Integration Testing
**Duration**: 5-8 hours

**End-to-End Workflow Validation**:
- User story: "Create GitHub issue about bug"
  - Intent classification → Routing → Handler → API → Confirmation
- User story: "What's my schedule today?"
  - Intent → Calendar integration → Response formatting
- User story: "Analyze last week's commits"
  - Intent → Git integration → Analysis → Report generation
- User story: "Generate standup report"
  - Multi-service orchestration → Content generation → Formatting

**Performance Validation**:
- Verify 602K req/sec claims
- Validate <1ms pre-classifier performance
- Confirm 7.6x cache speedup
- Test multi-user isolation

**Integration Points**:
- All 9 plugins functional
- Service-to-service communication
- Error recovery and retry logic
- State management across requests

## Acceptance Criteria
- [ ] Serena audit complete with full report
- [ ] All discrepancies documented and resolved
- [ ] Integration tests pass with real data (no mocks)
- [ ] Performance benchmarks validated
- [ ] Evidence package compiled (screenshots, logs, terminal output)
- [ ] Final completion percentage: 95%+ verified

## Evidence Requirements
- Serena audit report with line-by-line verification
- Terminal output for all integration tests
- Performance benchmark results
- Screenshots of working workflows
- API call logs showing real integrations

## Verification Standards
Every "complete" claim must have:
1. Structural validation (code exists)
2. Functional validation (feature works)
3. Evidence (terminal output/screenshots)
4. Serena verification (objective count)

## Time Estimate
8-13 hours total
- VALID-1: 3-5 hours
- VALID-2: 5-8 hours

## Priority
Medium - Final quality assurance

## Dependencies
- CORE-CRAFT-GAP complete (placeholders replaced)
- CORE-CRAFT-PROOF complete (documentation accurate)
- Serena MCP operational

## Success Metrics
- Zero sophisticated placeholders found
- All integration tests use real data
- Performance within 10% of claims
- Documentation 100% accurate to code

## Deliverables
1. Serena audit report (markdown)
2. Integration test results (terminal logs)
3. Performance benchmark report
4. Evidence package (screenshots/videos)
5. Final completion certification
