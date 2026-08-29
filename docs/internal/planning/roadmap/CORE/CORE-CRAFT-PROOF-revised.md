# CORE-CRAFT-PROOF: Documentation & Test Precision (REVISED)

## Context
Following GAP completion, documentation and test precision gaps remain across GREAT-1,2,3,4C,4E,5. GAP revealed documentation drift (claimed 89.3% vs actual 96.55%) and the value of systematic verification.

## Current State Post-GAP
- Documentation claims lag implementation by days/weeks
- Test counts in docs don't match reality
- 2 CI workflows still failing (pre-existing, now visible)
- ADRs incomplete or outdated
- Some tests check structure but not function

## Lessons from GAP to Apply
1. **Phase -1 reconnaissance essential** - Discover hidden issues first
2. **"Push to 100%" finds bugs** - Final 5% often most critical
3. **Documentation drift is real** - 7+ percentage point gap discovered
4. **Follow the smoke** - Surface issues reveal systemic problems
5. **Time Lord philosophy** - Quality determines timeline

## Revised Scope

### PROOF-0: Reconnaissance & Discovery
**NEW - Duration**: 2-3 hours
**Purpose**: Find hidden issues before planning

Using Serena MCP:
- Audit ALL documentation claims vs actual code
- Count actual tests, files, lines
- Identify documentation drift patterns
- Check ADR completion status
- Verify CI/CD workflow status
- **Output**: Complete gap inventory with evidence

### PROOF-1: GREAT-1 Documentation Completion
**Duration**: 1-2 hours
**Gap**: 10%

- Complete architecture.md updates
- ADR-032 revisions for QueryRouter restoration
- Troubleshooting guide completion
- Performance optimization documentation
- Exact line counts and file paths (Serena-verified)

### PROOF-2: GREAT-2 Test Precision
**Duration**: 2-3 hours
**Gap**: 8%

- Spatial intelligence test coverage
- Router test count reconciliation (claimed 92 vs actual)
- ConfigValidator integration verification
- Update exact file inventories
- Make tests stricter (no permissive patterns)

### PROOF-3: GREAT-3 Plugin Polish
**Duration**: 2-4 hours
**Gap**: 10%

- Verify 92 claimed tests vs actual count
- Complete developer guide with working examples
- Validate performance overhead claims
- Plugin documentation accuracy
- Pattern catalog updates

### PROOF-4: GREAT-4C Multi-User Validation
**Duration**: 1-2 hours
**Gap**: 2%

- Multi-user concurrent session testing
- Session isolation under stress
- Load testing documentation
- Edge case validation
- Actual performance metrics

### PROOF-5: GREAT-4E Test Infrastructure
**Duration**: 2-3 hours
**Gap**: 5%

- Reconcile claimed vs actual test counts
- Verify 600K+ req/sec performance claims
- Complete operational documentation
- Test execution time validation
- CI/CD workflow documentation

### PROOF-6: GREAT-5 Final Precision
**Duration**: 1 hour
**Gap**: 5%

- Line count precision in documentation
- Benchmark validation and updates
- CI/CD pipeline time verification (now operational!)
- Quality gate documentation
- Prevention system documentation (NEW from GAP-2)

### PROOF-7: CI/CD Completion
**NEW - Duration**: 3-4 hours
**Gap**: 2 workflows failing

Current failures:
1. Tests workflow - Missing CI API credentials
2. Architecture enforcement - 9 router pattern violations

Options:
- Mock LLM responses for CI testing
- Fix architectural violations
- Document as known technical debt

### PROOF-8: ADR Completion
**NEW - Duration**: 3-4 hours
**Gap**: 6+ ADRs incomplete

From GAP report mentions:
- ADR-032: QueryRouter (needs revision)
- ADR-039: Classification accuracy (exists, needs update)
- Plus 4-6 others identified in earlier tracking

Use Agent Core Charter framework for structure

### PROOF-9: Documentation Synchronization Strategy
**NEW - Duration**: 2-3 hours
**Gap**: Prevent future drift

Establish process for:
- Immediate doc updates after code changes
- Weekly documentation audits
- Automated metrics in docs where possible
- Version tracking between docs and code

## Decomposition Options

### Option A: Single Epic (Recommended for continuity)
Execute PROOF-0 through PROOF-9 in sequence
- Pros: Maintains context, systematic completion
- Cons: 20-30 hours is large scope
- Mitigation: Sub-phases like GAP

### Option B: Three Sub-Epics
1. **PROOF-DOCS** (PROOF-1,3,8,9): Documentation focus
2. **PROOF-TEST** (PROOF-2,4,5,6): Test precision focus
3. **PROOF-INFRA** (PROOF-0,7): Infrastructure focus
- Pros: Clear separation of concerns
- Cons: May lose cross-cutting insights

### Option C: By GREAT Epic
- **PROOF-GREAT-1**: Just GREAT-1 gaps
- **PROOF-GREAT-2**: Just GREAT-2 gaps
- Etc.
- Pros: Clear ownership
- Cons: Inefficient, lots of context switching

## Acceptance Criteria
- [ ] All documentation claims match actual code (Serena-verified)
- [ ] Test counts accurate and verified
- [ ] Line counts and file inventories precise
- [ ] Performance claims validated with evidence
- [ ] No discrepancies between docs and implementation
- [ ] All ADRs correctly referenced and complete
- [ ] CI/CD workflows 9/9 passing (or documented as debt)
- [ ] Documentation sync process established
- [ ] Zero "surprising" discoveries (all gaps found in PROOF-0)

## Verification Method
- Serena MCP systematic audit for each claim
- Automated counting and verification
- Documentation-to-code cross-reference
- Evidence collection for all metrics
- Git blame for documentation staleness analysis
- CI/CD green status verification

## Time Estimate
**Original**: 9-15 hours (PROOF-1 through 6)
**Revised**: 20-30 hours (PROOF-0 through 9)
**Rationale**: GAP showed hidden issues require 2-3x time

## Priority
High - Required for CRAFT completion and alpha readiness

## Dependencies
- Serena MCP for automated verification
- Access to all GREAT epic documentation
- CI/CD access for workflow fixes
- GitHub for ADR updates

## Risk Mitigation
1. **Hidden issues**: PROOF-0 reconnaissance finds them first
2. **Scope creep**: Clear boundaries, defer new discoveries
3. **Documentation drift**: Establish sync process in PROOF-9
4. **CI/CD complexity**: May need separate epic if complex

## STOP Conditions
- If architectural redesign needed
- If test framework requires overhaul
- If documentation structure needs rethink
- If more than 30 hours estimated after PROOF-0

## Success Metrics
- Documentation accuracy: 99%+ (Serena-verified)
- Test precision: No permissive patterns
- CI/CD health: 9/9 workflows or documented
- ADR completion: 100% or documented gaps
- Prevention: Documentation sync process active
