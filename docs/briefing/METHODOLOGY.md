---
type: briefing
title: BRIEFING-METHODOLOGY.md - How We Work
valid_from: "2025-09-25"
last_updated: "2026-10-31"
last_verified: "2026-10-31"
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

- **`docs/internal/development/methodology-core/INDEX.md`** — canonical numbered methodologies (Methodology-20 Omnibus Session Logs, Methodology-23 M1 Innovations, Methodology-24 Branch-or-Anchor, Methodology-25 Workstream Review Cadence, and others)
- **`.claude/skills/close-issue-properly/`** — how issues are closed (description first, then the evidence comment, then close)
- **`docs/internal/architecture/patterns/`** — pattern catalog (numbered through pattern-075, including the 062 family covering Assembly Assumption + the recently-Emerging 066/067/068/069 around stacked failures, issue-body reality, silent state mutation in shared working tree, and coarse-triggers-causing-false-positive-triage-cost)
- **`docs/internal/architecture/current/anti-pattern-index.md`** — 51 indexed anti-patterns (P-01 through P-17)
- **Excellence Flywheel v3.0** (2026-09-11) — three layers: Concept (the causal loop), Practice (five practices; see "The Excellence Flywheel" below), Mnemonic (per-role recalls). v3.0 re-derived the Practice layer for autonomous agent-pull operation.

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

## GitHub Progress Discipline

Agents update the issue DESCRIPTION with evidence, not just comments, and the closing agent checks the
boxes. Close with skill `close-issue-properly`: description first (status banner, every box checked or
explained), then the evidence comment with a `Verified how:` line, then close. (Until mid-2026 this section
said PM validated by checking boxes and asked for "(PM will validate)" on every criterion. CLAUDE.md's
Evidence rule and the skill replaced that.)

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
- [ ] Unit tests: QueryRouter initialization
- [ ] Integration tests: Intent → Engine → Router flow
- [ ] Performance tests: <500ms response time
- [ ] Regression tests: Prevent QueryRouter disabling
```

## Where Documents Go

Every cohort role runs in Claude Code with a worktree, so the old claude.ai guidance (Artifacts, then
Filesystem, then Sandbox) is retired. Durable work goes in the repo and is pushed to main. Session logs
follow CLAUDE.md ("Role and session log"): `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-{slug}-log.md` in your
worktree, where the slug is the role's from the CLAUDE.md table (for example `cio-code`), the model is
recorded in the log header, and the time comes from `TZ=America/Los_Angeles date`. Create or resume it
with skill `create-session-log`. One log per role per day.

## The Excellence Flywheel

**Canonical**: `docs/internal/development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md` (v3.0, 2026-09-11; Layer 2 re-derived for autonomous agent-pull operation).

The Flywheel is presented at three layers in the canonical doc:
- **Concept** (the causal loop, stable): quality compounds into velocity, which enables higher quality
- **Practice** (5 practices, enumerable + versioned): (1) Verify Before Building, (2) Test What Matters Not What's Easy, (3) Coordinate Through Structure, (4) Track to Completion with Evidence, (5) Audit the Composition
- **Mnemonic** (role-adapted recall aids; traceable to Practice → Concept)

v2.0 (Apr 26 – Sept 11, 2026) and the v1 "Four Pillars" (July 2025 – Apr 2026) are superseded; the canonical doc records both derivations.

For role-specific applications, see each role's BRIEFING-ESSENTIAL-{ROLE}.md "Critical vs. Commodity Work" section.

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
- Every commit references its issue. A commit message that pairs close/fix/resolve with `#N` closes
  issue N (CLAUDE.md hard rule 5), so write the number without `#` unless you mean to close it:
  `git commit -m "fix: Initialize QueryRouter (issue 180)"`
- Every PR links to its issue: `Closes #180` when the PR finishes it

## Template Adaptation

Templates provide structure but should be adapted to context:
- Skip irrelevant sections
- Combine phases if appropriate
- Add detail where needed
- Evidence over format compliance

The goal is effective work, not perfect adherence to templates.

## Multi-Agent Coordination

> **📋 Detailed Guide**: [methodology-02-AGENT-COORDINATION.md](../internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md) - Comprehensive coordination methodology
> **📚 Examples**: [Pattern-061: Human-AI Collaboration Referee](../internal/architecture/patterns/pattern-061-human-ai-collaboration-referee.md) - Real project case studies and implementation protocols

### Agent Strengths

> **📍 Complete Reference**: [methodology-02-AGENT-COORDINATION.md](../internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md#canonical-agent-strengths-single-source-of-truth) - Authoritative agent strengths

**Quick Summary**: the cohort's seats all run Claude Code; roles and lanes are in `docs/briefing/ROSTER.md`.
The Claude Code / Cursor split below this point comes from the 2025 two-agent era. The deployment
modes (cross-validation, parallel separation) still apply between seats or subagents.

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
$ curl -X POST http://localhost:8001/api/v1/intent \
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
5. Run the CLAUDE.md sign-off block

## Session Satisfaction Protocol (historical)

Not part of the current session procedure: CLAUDE.md has no satisfaction step, and duty-cycle seats have no
session end to attach it to. Kept as a record of the 2025 practice.

1. **Quick 5-point assessment** in session log
2. **Ask PM each metric**, compare answers and discuss:
   - **Value**: What got shipped?
   - **Process**: Did methodology work smoothly?
   - **Feel**: How was the cognitive load?
   - **Learned**: Any key insights?
   - **Tomorrow**: Clear next steps?
   - **Overall**: 😊 / 🙂 / 😐 / 😕 / 😞
3. **GitHub issue emoji close** (🎉 great, ✅ good, 🤔 meh, 😤 rough)


## Session Failure Conditions

The session has failed our standards if ANY of these occur:
- Architect creates gameplan without PM verification
- Architect creates implementation artifacts
- Agents proceed without verification
- Work happens outside GitHub tracking
- Multiple fixes without architectural review
- Assumptions made without checking
- Lead Developer skips BRIEFING-ESSENTIAL-LEAD-DEV.md

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
*Last Updated: 2026-10-31 (CIO, #1726: Flywheel v3.0, session-log format from CLAUDE.md, claude.ai-era document guidance retired, PM-validates-checkboxes replaced by close-issue-properly, satisfaction protocol marked historical. Foundational content preserved from Sep 22, 2025.)*
