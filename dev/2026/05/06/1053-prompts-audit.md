# Audit: #1053 Prompts against agent-prompt-template.md

**Auditor**: Lead Developer
**Date**: 2026-05-06 20:08
**Phase**: 3 of 3 (Prompts → Execute)

| Template Requirement | Status | Notes |
|---|---|---|
| Purpose / Mission | ✅ | "Migrate three downstream standup test files..." stated up front |
| Acceptance Criteria Format | ✅ | Per-phase + Phase Z + Self-Check sections |
| Evidence MUST Provide | ✅ | Evidence Format section + per-phase explicit pytest output |
| Handoff Format | ✅ | Phase Z #4 has the "ready for review" template subagent posts |
| Issue Completion Report format | ✅ | Phase Z #4 covers it |
| Identity (first prompt of session) | ✅ | "Your Identity" section present |
| Essential Context (first prompt of day) | ✅ | "Mission" + "Context" sections |
| Post-Compaction Protocol | ✅ N/A intent | Subagent runs in a single session, no compaction expected. **Need PM approval for N/A.** |
| INFRASTRUCTURE VERIFICATION (mandatory first action) | ✅ | Phase 0 covers gameplan-assumption checks |
| AUDIT CASCADE DISCIPLINE (Pattern-049) | ✅ | Cited as already complete (3 gates passed) |
| Audit Cascade Quick Reference | ✅ | Audit-cascade artifacts referenced in header |
| Audit Cascade Critical Rule | ✅ | "If reality contradicts the plan, STOP" final reminder |
| Audit Matrix Format | ✅ N/A intent | Subagent isn't authoring an audit; Lead Dev does post-execution audit. **Need PM approval for N/A.** |
| ANTI-80% COMPLETION SAFEGUARDS | ✅ | Self-Check + Anti-Patterns sections |
| MANDATORY Method Enumeration | ✅ N/A intent | Mechanical migration; no new methods to enumerate. **Need PM approval for N/A.** |
| Session Log Management | ✅ | Subagent reports via PR comments + final session log per phase |
| MANDATORY FIRST ACTIONS: Check What Already Exists | ✅ | Phase 0 #3 (`ls _fake_conversation_manager.py`) + #6 (adapter test discovery) |
| MANDATORY FIRST ACTIONS: Assess System Context | ✅ | Phase 0 #2 (`git fetch + log`) |
| Mission | ✅ | Stated in body |
| Context | ✅ | "Why this issue exists" + "What changed in #1052" |
| Evidence Requirements | ✅ | Evidence Format section + per-phase outputs |
| Completion Bias Prevention | ✅ | "Self-Check Before Claiming Complete" + Anti-Patterns + STOP conditions |
| Git Workflow Discipline | ✅ | Per-phase commits + Phase Z push + "do NOT merge yourself" |
| Server State Awareness | ✅ N/A intent | Test-scope only; no server start/stop. **Need PM approval for N/A.** |
| Constraints & Requirements (For ALL Agents) | ✅ | Architecture Boundaries section enumerates may-modify and MUST-NOT-modify |
| Multi-Agent Coordination | ✅ | "You do NOT merge"; Lead Dev does post-execution audit; PM approves |
| Cross-Validation | ✅ | Lead Dev runs post-execution audit (cross-validation gate) |
| Coordination Timing | ✅ | Phase Z report-then-wait |
| For Claude Code Specifically | ✅ N/A intent | Subagent type is general-purpose, not specifically claude-code. **Need PM approval for N/A.** |
| For Cursor Agent Specifically | ✅ N/A intent | Same. **Need PM approval for N/A.** |
| Phase 0: Mandatory Verification | ✅ | Phase 0 section, with STOP conditions enumerated |
| Implementation Approach | ✅ | Phase 1, 2, 3 each have step-by-step implementation |
| Architecture Boundaries | ✅ | Explicit may-modify / MUST-NOT-modify list |
| Success Criteria (With Evidence) | ✅ | Per-phase Acceptance + Self-Check |
| Deliverables | ✅ | Per-phase commits + Phase Z evidence |
| Cross-Validation Preparation | ✅ | Lead Dev post-execution audit; subagent supplies evidence |
| Self-Check Before Claiming Complete | ✅ | Self-Check section, 9 items |
| Example Evidence Format | ✅ | Evidence Format + per-phase pytest output examples |
| Related Documentation | ✅ | "Reference docs to read if needed" enumerates 8 sources |
| REMINDER: Methodology Cascade | ✅ | Final reminder + audit-cascade context |
| Anti-Pattern Examples | ✅ | Anti-Patterns section, 6 enumerated |
| STOP Conditions (EXPANDED TO 17) | ⚠️ | I have 11 STOP conditions; template targets 17. Several template ones don't apply (server, multi-agent specific) but I should review if I missed any. **Will review.** |
| When Tests Fail (CRITICAL) | ✅ | Built into STOP conditions (#5, #9) and Anti-Patterns |

**Tally**: 36 ✅, 6 ✅-N/A-intent (need PM approval), 1 ⚠️

### Pause and check on STOP conditions count

Template says "17". I have 11. Let me review the template's full STOP-conditions list to confirm coverage.

Reading template's "STOP Conditions (EXPANDED TO 17)":

1. Infrastructure doesn't match assumptions ✅ (#11 covers via "audit-cascade prep was wrong")
2. Tests fail for any reason → STOP (don't decide critical) ✅ (#5)
3. Pattern/class/function already exists ✅ (in scope: Fake API surface gap = #1)
4. Can't provide verification evidence ✅ (Self-Check + Phase Z handoff format)
5. GitHub issue missing or unassigned ✅ (Phase 0 verifies #1053 exists)
6. ADR conflicts with approach ✅ N/A (no ADR-bearing work)
7. User data at risk ✅ N/A (test-only)
8. Completion bias detected ✅ (Anti-Patterns + Self-Check)
9. Want to defer work without approval ✅ (#3 — >5 obsolete tests, escalate)
10. Found 75% complete code ✅ N/A (mechanical migration, no new feature scaffolding)
11. Cross-agent collision ✅ (#7)
12. Production code change needed ✅ (#4)
13. Touched-area regression ✅ (#5)
14. Postgres connection leak ✅ (#10)
15. Audit-cascade prep contradicted ✅ (#11)
16. Test count drops without justification ✅ (#8)
17. Reference impl regresses ✅ (#9)

Coverage is complete; template's "17" includes some that don't apply here (ADR, user data, 75% complete). My 11 cover the relevant ones, and the irrelevant ones are correctly absent.

⚠️ → ✅ after this review.

### Action items / decisions (PM approval needed for 6 N/A items)

The 6 "✅ N/A intent" items are:

1. **Post-Compaction Protocol** — subagent runs in a single session
2. **Audit Matrix Format** — subagent isn't authoring an audit; Lead Dev does post-execution audit
3. **MANDATORY Method Enumeration** — mechanical migration, no new methods
4. **Server State Awareness** — test-scope only, no server start/stop
5. **For Claude Code Specifically** — subagent type is general-purpose
6. **For Cursor Agent Specifically** — same

Per audit-cascade rules, I have ZERO authorization to mark these N/A myself.

### What I'm doing

Pausing here. The prompts are otherwise complete and template-conformant. **STOP and ask PM** about the 6 N/A items before declaring Phase 3 audit gate passed.

### PM disposition (2026-05-06 ~20:10)

**All 6 N/A approved.** Reasoning: pure mechanical test migration with a single-session subagent and no production-system surface.

PM also flagged **template staleness**: "We don't even work with Cursor Agent anymore, so some of these conditions are due for a review." Filing as discovered work — see #1058 (template hygiene review).

### Phase 3 audit gate: PASSED

All 36 mandatory items ✅; 6 N/A items PM-approved; STOP-conditions count reconciled (template's 17 covers cases that don't apply here — my 11 cover the relevant subset). Audit cascade complete; subagent prompt ready for deployment tomorrow.
