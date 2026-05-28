---
type: briefing
title: BRIEFING-METHODOLOGY.md - How We Work
valid_from: "2025-09-25"
last_updated: "2026-05-12"
---

# BRIEFING-METHODOLOGY.md - How We Work

## Core Principle: Visible Collaboration

**Always check and discuss an ambiguity rather than guessing and moving forward silently.**

We need visibility into difficult choices. We don't expect silent perfection. We welcome messy discussion and collaborating to find paths none of us might find alone.

When in doubt:
- STOP and ask
- Document the ambiguity
- Propose options
- Discuss tradeoffs
- Decide together

## Documentation Navigation
For complete documentation structure and navigation, see: **docs/NAVIGATION.md**
This file maps all documentation locations and purposes.

## Current Methodology Corpus (Pointer Index)

This briefing captures foundational principles that have been stable since 2025. For the live methodology corpus, consult:

- **`docs/internal/development/methodology-core/INDEX.md`** — canonical numbered methodologies (Methodology-20 Omnibus Session Logs, Methodology-23 close-issue-properly, Methodology-24 Branch-or-Anchor, Methodology-25 Workstream Review Cadence, and others)
- **`docs/internal/architecture/current/patterns/`** — pattern catalog (70 patterns as of 2026-05-12, including the 062 family covering Assembly Assumption + the recently-Emerging 066/067/068/069 around stacked failures, issue-body reality, silent state mutation in shared working tree, and coarse-triggers-causing-false-positive-triage-cost)
- **`docs/internal/architecture/current/anti-pattern-index.md`** — 51 indexed anti-patterns (P-01 through P-17)
- **Excellence Flywheel v2.0** — reformulated 2026-04-17 (CIO M1 methodology audit) into three layers: Concept (the causal loop), Practices (5 currently: TDD/Verify-before-build/Audit-cascade/Branch-or-anchor/**Audit the composition** added 2026-04-17 from Pattern-062), Mnemonics (per-role compact recalls)

The foundational principles below remain canonical regardless of catalog evolution.

## The Inchworm Protocol (ADR-035)

We complete work sequentially and thoroughly. Like an inchworm, each movement is complete before the next begins.

### The Five Steps (Required for Every Epic)

1. **Fix** - Solve the actual problem, not work around it
2. **Test** - Prove it works with comprehensive tests
3. **Lock** - Add tests that prevent regression
4. **Document** - Update docs to reflect reality
5. **Verify** - Confirm with the North Star test (GitHub issue creation)

### Definition of "Done"

A task is only complete when:
- ✅ All acceptance criteria met
- ✅ All tests passing
- ✅ Lock mechanisms in place
- ✅ Documentation updated
- ✅ No TODO comments without issue numbers
- ✅ No workarounds present
- ✅ Evidence provided for all claims

**Not Done**: "It should work" / "It's mostly complete" / "Just needs cleanup"
**Done**: "Here's the test proving it works, the lock preventing regression, and the updated docs"

## GitHub Progress Discipline (MANDATORY)

### PM Validates Checkboxes
This is critical methodology:
- **Agents UPDATE** progress descriptions with evidence
- **PM VALIDATES** by checking boxes
- **Include "(PM will validate)"** in all acceptance criteria
- **Evidence required** before PM checks any box

### Format for Issues
```markdown
## Acceptance Criteria
- [ ] Task description with clear completion definition (PM will validate)
- [ ] Another task with evidence requirement (PM will validate)
  - Evidence: [terminal output or test results will go here]
```

### Progress Updates
Agents update in issue DESCRIPTION (not comments):
```markdown
## Progress
- [ ] Investigation complete
  - Found root cause: session management issue
  - Evidence: [link to specific line in engine.py]
- [ ] Fix implemented
  - Changed initialization in commit abc123
  - Tests passing: see output below
```

## Test Scope Specification

All acceptance criteria must specify test types:

### Required Test Categories
- **Unit tests**: Individual component functionality
- **Integration tests**: Component interaction and flow
- **Performance tests**: Speed and resource metrics
- **Regression tests**: Prevent specific failures from recurring

### Example Format
```markdown
## Testing Requirements
- [ ] Unit tests: QueryRouter initialization (PM will validate)
- [ ] Integration tests: Intent → Engine → Router flow (PM will validate)
- [ ] Performance tests: <500ms response time (PM will validate)
- [ ] Regression tests: Prevent QueryRouter disabling (PM will validate)
```

## Document Creation Guidelines

### Use Artifacts When:
- Creating prompts for agents
- Creating final deliverables for PM
- Creating reusable templates
- Want it visible in project artifacts

### Use Filesystem When:
- Creating session logs
- Creating working documents
- Need permanent record
- Multiple files in sequence

### Use Sandbox When:
- Quick temporary calculations
- Testing code snippets
- Throwaway explorations

### Documentation Location Priority When in Doubt (Use First Available)

1. **Artifacts** (when reliable)
   - Pros: Attached to project, versioning, easy navigation
   - Cons: Intermittent bugs, download naming issues
   - Backup: Download periodically with -HHMM timestamp

2. **Filesystem** (when available)
   - Pros: Secure, real-time, repository integration
   - Cons: Not available in standard Claude.ai (only Desktop)
   - Path: `/Users/xian/Development/piper-morgan/dev/YYYY/MM/DD/`

3. **Sandbox** (fallback)
   - Pros: Usually available
   - Cons: Update failures, no project attachment
   - Backup: Download with -HHMM timestamps

### Verification Discipline
After EVERY file write:
- Run: `tail -5 [filename]` to verify
- Report failures immediately
- Fall back to next location if failed

## Session Log Standard v2

### Framework and instructions

**If in Claude.ai or Claude Desktop with access to project knowledge**
* session-log-framework.md
* session-log-instructions.md

**If access you have access to the local filesystem**
* `User/xian/Development/piper-morgan/docs/internal/development/tools/session-log-framework.md`
* `User/xian/Development/piper-morgan/docs/internal/development/tools/session-log-instructions.md`

### Format
```
YYYY-MM-DD-HHMM-[role]-[product]-log.md
```

### Standard Slugs
**Roles**:
- `exec` (Chief of Staff)
- `arch` (Chief Architect)
- `lead` (Lead Developer)
- `prog` (Programmer)

**Products**:
- `opus` (Claude Opus)
- `sonnet` (Claude Sonnet)
- `code` (Claude Code)
- `cursor` (Cursor Agent)

### Examples
```
2025-09-22-0816-arch-opus-log.md
2025-09-22-1046-lead-sonnet-log.md
2025-09-22-1400-prog-code-log.md
```

### Creation Command
```bash
# Generic format (replace [role] and [product])
mkdir -p dev/$(date +%Y)/$(date +%m)/$(date +%d)
echo "# Session Log - $(date +%Y-%m-%d %H:%M)" > dev/$(date +%Y)/$(date +%m)/$(date +%d)/$(date +%Y-%m-%d-%H%M)-[role]-[product]-log.md
```

## The Excellence Flywheel

**Canonical**: `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (v2.0 three-layer reformulation, Apr 2026).

The Flywheel is presented at three layers in the canonical doc:
- **Concept** (the causal loop, stable): quality compounds into velocity, which enables higher quality
- **Practice** (5 practices, enumerable + versioned): (1) Verify Before Building, (2) Test What Matters Not What's Easy, (3) Coordinate Through Structure, (4) Track to Completion with Evidence, (5) Audit the Composition
- **Mnemonic** (role-adapted recall aids; traceable to Practice → Concept)

The pre-v2 "Four Pillars" formulation (July 2025 → April 2026) is superseded; canonical doc explains the v1 → v2 derivation.

For role-specific applications, see each role's BRIEFING-ESSENTIAL-{ROLE}.md "Load-Bearing vs. Commodity Work" section.

## GitHub Discipline

Every piece of work must be tracked:

### Issue-First Development
1. **GitHub issue exists** before work starts
2. **Issue assigned** to track ownership
3. **Issue description** contains acceptance criteria
4. **Updates go in description** via checkbox edits (not just comments)
5. **Evidence provided** for each completed checkbox

### Linking Everything
- Every TODO has an issue: `# TODO(#184): Fix this`
- Every commit references issue: `git commit -m "fix: Initialize QueryRouter (#180)"`
- Every PR links to issue: `Closes #180`

## Template Adaptation

Templates provide structure but should be adapted to context:
- Skip irrelevant sections
- Combine phases if appropriate
- Add detail where needed
- Evidence over format compliance

The goal is effective work, not perfect adherence to templates.

## Multi-Agent Coordination

> **📋 Detailed Guide**: [methodology-02-AGENT-COORDINATION.md](../internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md) - Comprehensive coordination methodology
> **📚 Examples**: [Pattern-061: Human-AI Collaboration Referee](../internal/architecture/current/patterns/pattern-061-human-ai-collaboration-referee.md) - Real project case studies and implementation protocols

### Agent Strengths

> **📍 Complete Reference**: [methodology-02-AGENT-COORDINATION.md](../internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md#canonical-agent-strengths-single-source-of-truth) - Authoritative agent strengths

**Quick Summary**:
- **Claude Code**: Multi-file implementations, architecture design, subagent coordination
- **Cursor**: API endpoints, testing, documentation, UI/UX implementation

### Deployment Patterns

> **🎯 Decision Guide**: [Validation Approaches](../internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md#validation-approaches-when-to-use-each-method) - When to use cross-validation vs parallel separation

**Cross-Validation Mode**: Both agents work same high-risk task, compare approaches
**Parallel Separation Mode**: Agents work different domains, coordinate at interfaces
**Single Agent**: Only with explicit justification for simple tasks

### Quick Decision Framework
- **High risk + complex** → Cross-validation
- **Clear domains + time critical** → Parallel separation
- **Uncertain territory** → Start cross-validation, evolve to parallel

### Multi-Agent Quick Start Checklist

**Pre-Deployment** (2 minutes):
- [ ] Task complexity justifies multi-agent approach
- [ ] Clear separation of concerns identified OR overlap planned for cross-validation
- [ ] Integration points defined (API, domain models, test interfaces)

**Deployment** (30 seconds):
- [ ] Both agents briefed with agent-specific prompts
- [ ] GitHub issue created for coordination
- [ ] Initial sync point scheduled (15-30 minutes)

**Execution** (ongoing):
- [ ] Regular progress updates in shared GitHub issue
- [ ] Coordination checkpoints every 15-30 minutes
- [ ] Integration validation before completion claims

**Quality Gates**:
- [ ] Both agents verify final integration
- [ ] Evidence provided for all claims
- [ ] Cross-validation performed for critical components

### Common Pitfalls to Avoid
- **Duplicate work** without coordination
- **Interface conflicts** from lack of upfront agreement
- **Uneven progress** without sync checkpoints
- **Integration debt** from deferred coordination

## Evidence Requirements

No claims without proof:

### What Counts as Evidence
✅ **Terminal output** showing success
✅ **Test results** passing
✅ **Performance metrics** meeting targets
✅ **File diffs** showing changes
✅ **Screenshots** of working features
✅ **Logs** demonstrating behavior

❌ **Not Evidence**: "Should work" / "Probably fixed" / "Seems right"

### Evidence Examples
```bash
# Good: Show the test passing
$ pytest tests/test_orchestration.py -xvs
...
tests/test_orchestration.py::test_github_issue_creation PASSED

# Good: Show the performance
$ python benchmark.py
Average response time: 247ms (target: <500ms) ✓

# Good: Show it actually works
$ curl -X POST http://localhost:8001/api/intent \
    -d '{"message": "create github issue about login bug"}'
{"status": "success", "issue_url": "github.com/..."}
```

## STOP Conditions (Red Flags)

Stop immediately and ask for help when:

### Infrastructure Mismatches
- File structure different than expected
- Ports not matching documentation
- Missing dependencies

### Pattern Confusion
- Multiple ways to do same thing
- Conflicting patterns in codebase
- ADR contradicts code

### Test Failures
- ANY test failing after changes
- Performance degradation
- Unexpected behavior

### Assumption Moments
- About to guess configuration value
- Unsure which pattern to follow
- Don't understand why something was done

### The Questions to Ask
1. "I expected X but found Y - should I proceed?"
2. "There are two patterns here - which is correct?"
3. "This seems broken but has TODO - fix or skip?"
4. "I don't understand why - can you explain?"

## Collaboration Over Perfection

We value:
- **Visible struggle** over silent suffering
- **Asking questions** over wrong assumptions
- **Sharing confusion** over hiding ignorance
- **Proposing options** over picking blindly
- **Learning together** over knowing alone

## Daily Rhythm

Start each session:
1. Check current epic status
2. Review relevant ADRs
3. Verify infrastructure matches expectations
4. Plan work with clear deliverables
5. Set evidence targets

End each session:
1. Document what was completed (with evidence)
2. Update GitHub issues
3. Note any discoveries or surprises
4. Flag any blockers for next session
5. Complete satisfaction assessment (see below)

## Session Satisfaction Protocol

Before ending any session, complete satisfaction check:

1. **Quick 5-point assessment** in session log
2. **Ask PM each metric**, compare answers and discuss:
   - **Value**: What got shipped?
   - **Process**: Did methodology work smoothly?
   - **Feel**: How was the cognitive load?
   - **Learned**: Any key insights?
   - **Tomorrow**: Clear next steps?
   - **Overall**: 😊 / 🙂 / 😐 / 😕 / 😞
3. **GitHub issue emoji close** (🎉 great, ✅ good, 🤔 meh, 😤 rough)

This is MANDATORY for session completion. The satisfaction data helps improve our processes and prevent burnout.

Reference: session-log-instructions.md

## Session Failure Conditions

The session has failed our standards if ANY of these occur:
- Architect creates gameplan without PM verification
- Architect creates implementation artifacts
- Agents proceed without verification
- Work happens outside GitHub tracking
- Multiple fixes without architectural review
- Assumptions made without checking
- Lead Developer skips 00-START-HERE-LEAD-DEV

When failure conditions occur, stop and reset methodology compliance.

## Success Metrics

### Per Session
- Setup time: <15 minutes (from ~1 hour baseline)
- Infrastructure verification: 100%
- GitHub tracking: 100% complete
- Manual reminders needed: <5
- Verification theater: 0 instances

### Per Week
- Methodology compliance: >90%
- Cross-validation performed: 100%
- Documentation current: Always
- Cognitive load: Significantly reduced
- Wrong gameplans avoided: Target 100%

## The "Simpler Than Expected" Pattern

Often, we assume complexity where simplicity exists:
- QueryRouter issue: Session management, not dependency chain
- Bug fixes: Often configuration, not architecture
- Performance: Often caching, not algorithm

**Approach**: Start with simple checks before complex investigation.

## Remember

The path none of us would find alone is the one we discover together through visible collaboration, systematic verification, and complete execution.

When you find yourself guessing - STOP. That's the moment to engage, not push through.

---

*Excellence comes from completion, not perfection.*
*Last Updated: 2026-05-12 (foundational content preserved from Sep 22, 2025; Current Methodology Corpus pointer index added to track post-2025 corpus evolution)*
