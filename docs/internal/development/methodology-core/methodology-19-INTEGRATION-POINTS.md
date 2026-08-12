# Methodology Integration Points

> ⚠️ **Legacy planning doc — numbering resolved 2026-08-12 (CIO, #1584 Part C, Docs-flagged).** This file
> predates the current numbering convention and the `docs/internal/development/` path (it still refers to
> `docs/development/...` throughout). **Slot 19 is canonically THIS file** — `methodology-19-INTEGRATION-POINTS.md`.
> The two placeholder filenames below (`methodology-19-LEARNING-CAPTURE.md`, `methodology-20-FAILURE-ISOLATION.md`)
> were never filed under those numbers and now never can be — both slots are long since taken by other real,
> filed topics (19 = this file; 20 = `methodology-20-OMNIBUS-SESSION-LOGS.md`). They are dead references, not
> open TODOs. `methodology-28-PRE-FILING-SLOT-AVAILABILITY-CHECK.md` is the discipline that now prevents this
> class of drift on new filings.

## Files Requiring Updates for FLY Methodology

### 1. Pattern Catalog Updates

**File**: `docs/architecture/pattern-catalog.md`

**Updates Needed**:

- Add new pattern categories for FLY methodology
- Create "Verification Patterns" section
- Add "Anti-Patterns" section (validation theater, mock fallbacks)
- Include "Coordination Patterns" for multi-agent work
- Add "Error Handling Patterns" for failure isolation

**Categories to Add**:

- **Verification Patterns**: How to validate work properly
- **Coordination Patterns**: Multi-agent collaboration
- **Error Handling**: Graceful degradation vs honest failure
- **Anti-Patterns**: What NOT to do (validation theater, etc.)

### 2. Excellence Flywheel Updates

**File**: `docs/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md`

**Updates Needed**:

- Add failure isolation checkpoint to verification process
- Include pattern capture reminder in multi-agent coordination
- Add circuit breaker patterns to systematic verification
- Update GitHub-first tracking to include methodology patterns

**New Checkpoints**:

- **Failure Isolation Check**: Verify no cascade failures
- **Pattern Capture**: Document learnings from each session
- **Circuit Breaker Validation**: Ensure clear service boundaries

### 3. Cross-Validation Protocol Updates

**File**: `docs/development/methodology-core/methodology-17-CROSS-VALIDATION-PROTOCOL.md`

**Updates Needed**:

- Add methodology pattern validation
- Include failure isolation verification
- Add learning capture validation
- Update validation checklist for FLY patterns

### 4. New Methodology Files Needed

#### FLY-LEARN Integration

**File**: `docs/development/methodology-core/methodology-19-LEARNING-CAPTURE.md`

- Pattern extraction process
- Weekly review integration
- Anti-pattern documentation
- Learning validation protocols

#### FLY-ISOLATE Integration

**File**: `docs/development/methodology-core/methodology-20-FAILURE-ISOLATION.md`

- Service boundary patterns
- Circuit breaker implementation
- Health check protocols
- Failure propagation prevention

### 5. Agent Prompt Templates

**Files**: Need to be created

- `docs/development/agent-prompt-template.md`
- `docs/development/gameplan-template.md`

**Content Needed**:

- Pattern capture reminders
- Failure isolation checkpoints
- Learning validation steps
- Methodology compliance verification

### 6. Testing Integration

**Files**: Various test files

- Add methodology pattern tests
- Include failure isolation tests
- Add learning capture validation
- Update cross-validation tests

## Implementation Priority

### High Priority (Immediate)

1. **Pattern Catalog Updates** - Add new categories
2. **Excellence Flywheel Updates** - Add failure isolation checkpoints
3. **Create Agent Prompt Templates** - Essential for methodology adoption

### Medium Priority (Next Sprint)

1. **Cross-Validation Protocol Updates** - Include FLY patterns
2. **New Methodology Files** - FLY-LEARN and FLY-ISOLATE
3. **Testing Integration** - Validate methodology patterns

### Low Priority (Future)

1. **Advanced Pattern Discovery** - Automated pattern extraction
2. **Methodology Metrics** - Track adoption and effectiveness
3. **Integration with MCP** - Spatial intelligence for patterns

## Success Criteria

- [ ] All methodology files updated with FLY patterns
- [ ] Agent prompts include failure isolation checkpoints
- [ ] Pattern catalog has new categories and anti-patterns
- [ ] Cross-validation includes methodology verification
- [ ] New methodology files created and integrated
- [ ] Testing validates methodology patterns
