# Piper Morgan Roadmap v14.3

**Date**: March 10, 2026
**Author**: Documentation Agent (updated from v14.2)
**Status**: Active - M0 COMPLETE (v0.8.6), M1 Sprint Next

---

## Executive Summary

**Current state**: M0 (Conversational Glue) shipped as v0.8.6 on March 4, 2026. 27 issues total (5 planned + 22 discovered via Assembly Assumption). Sprint executed in 3 days vs 13-22 day estimate. All quality gates passed. PM taking deliberate pause before M1.

**Key Changes from v14.2**:
- M0 COMPLETE — gate #779 closed, epic #762 closed, v0.8.6 released
- 56-commit merge to main, production push
- Inchworm position advanced: 4.4.1 → 4.4.2
- M0 sprint summary updated with final totals
- Ship #033 "The Cathedral Ships" drafted
- GitHub wiki published
- Branch protection enabled on main

---

## Current Position

```
Inchworm Position: 4.4.2 (M0 Complete, M1 Next)

1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.5.1)
4. 🎯 Complete build of MVP
   4.1. ✅ B1 - Beta Enablers (v0.8.3.x) - COMPLETE Jan 11
   4.2. ✅ A20 - Alpha Testing round 2 (v0.8.4.x) - COMPLETE Jan 18
   4.3. ✅ MUX: Modeled User Experience - COMPLETE Jan 27
   4.4. 🎯 MVP Sprints (M0-M6) ← CURRENT
        ✅ M0: Conversational Glue — COMPLETE (v0.8.6, Mar 4)
        ○ M1: Foundation (47% cherry-picked) ← NEXT
        ○ M2: Activation (4%)
        ○ M3: Skills (30%)
        ○ M4: Documents (0%)
        ○ M5: Polish (0%)
        ○ M6: Future/Hardening (18%)
   4.5. ○ DIST: Distribution Packaging (after M6)
5. Beta testing on 0.9
6. Launch 1.0
```

---

## MVP Sprint Status (March 10, 2026)

### M0 — Conversational Glue ✅ COMPLETE

**Status**: COMPLETE — v0.8.6 shipped March 4, 2026
**Theme**: Natural conversation flow — "The sheet music for the orchestra"
**Epic**: #762 (GLUE - Conversational Glue Implementation) — CLOSED
**Gate**: #779 (M0-GLUE Sprint Completion Gate) — CLOSED

**Final Totals**: 27 issues (5 planned + 22 discovered via Assembly Assumption)
- Sprint executed in 3 days (Feb 17-19) vs 13-22 day estimate
- 56-commit merge to main, production release
- All B2 quality gate criteria resolved
- #858 Conversation Lifecycle Spec approved (4 reviewers, same-day)
- #715 full lifecycle implementation (27 tests)

**Lesson Learned**: 5 planned issues expanded to 27 total. Assembly Assumption pattern (Pattern-049) — individually correct components ≠ correct composition. B2 testing revealed the gap between "tests pass" and "users succeed" (Pattern-045).

---

### M1 — MVP Foundation (47% cherry-picked)

**Status**: 14/30 done — cherry-picked during MUX and alpha testing
**Theme**: Security + Testing foundation

**Done (14 issues)**:
#239, #245, #275, #301, #305, #306, #307, #308, #316, #317, #332, #385, #696, #697

**Blocked (1 issue)**:
- #358 SEC-ENCRYPT-ATREST (blocked on expert consultation → M6)

**Remaining (15 issues)**:
| Category | Issues |
|----------|--------|
| Testing | #190, #247, #352, #472, #738, #739 |
| Security | #470 (RBAC epic), #482, #542 |
| Architecture | #557 (WebSocket) |
| MUX follow-up | #705, #706, #717 |
| Learning | #372 |
| QA | #375 |

---

### M2 — MVP Activation (4%)

**Status**: 1/23 done
**Theme**: MUX Wiring + Infrastructure

**Done (1 issue)**: #298 AUTH-PASSWORD-CHANGE

**Remaining (22 issues)**:
| Category | Issues |
|----------|--------|
| WIRE-* (MUX wiring) | #683, #690, #691, #692, #693, #694, #695 |
| MUX Lifecycle | #703 (epic 25%), #707, #714, #715 |
| Testing | #167, #191, #273 (75%), #276 |
| Infrastructure | #304 (Notion quick win), #309, #310, #366, #371, #471 |
| Feature | #790 (Trust-gated calendar) |

---

### M3 — MVP Skills (30%)

**Status**: 3/10 done
**Theme**: Canonical queries + Core skills

**Done (3 issues)**: #143, #248, #303

**Remaining (7 issues)**:
| Issue | Title |
|-------|-------|
| #118 | INFR-AGENT: Multi-Agent Coordinator |
| #312 | CONV-UX-DESIGN: Unified Design System |
| #315 | CONV-MCP-LIBRARY: Core Skills Library |
| #496 | CANONICAL-#9: Priority queries |
| #497 | CANONICAL-#10: Focus guidance synthesis |
| #704 | MUX-LIFECYCLE-UI-A: Morning Standup lifecycle |
| #716 | MUX-FEATURES-VIEW |

---

### M4 — MVP Document Revolution (0%)

**Status**: 0/5 done
**Theme**: Document processing (coherent, focused)

| Issue | Title |
|-------|-------|
| #302 | CONV-MCP-DOCS: Unified Document Processing |
| #313 | CONV-UX-DOCS: File Browser & Document Management UI |
| #355 | DOCS-STOPGAP: Basic Artifact Persistence |
| #712 | MUX-DOCUMENT-VIEWER |
| #713 | MUX-DOCUMENTS-LIFECYCLE-UI |

---

### M5 — MVP Polish (0%)

**Status**: 0/11 done
**Theme**: Auth polish, Slack, remaining features

| Issue | Title | Category |
|-------|-------|----------|
| #100 | CONV-FEAT-PROJ: Project Portfolio Awareness | Feature |
| #101 | CONV-FEAT-TIME: Temporal Context System | Feature |
| #103 | CONV-FEAT-PRIOR: Priority Calculation Engine | Feature |
| #146 | FLY-VERIFY: Three-Tier Verification Pyramid | Infrastructure |
| #147 | FLY-VERIFY-HAND: Mandatory Handoff Protocol | Infrastructure |
| #148 | FLY-VERIFY-CONFIG: Configuration Layer | Infrastructure |
| #244 | CONV-UX-SLACK: Interactive Slack Standup | Feature |
| #272 | RESEARCH-TOKENS-THINKING | Research |
| #338 | INFRA-MIGRATION-ROLLBACK | Infrastructure |
| #441 | CORE-UX-AUTH-PHASE2 | Auth |
| #463 | FLY-COORD-TREES: Git Worktrees | Infrastructure |

---

### M6 — MVP Future/Hardening (18%)

**Status**: 2/11 done
**Theme**: Security hardening + future features

**Done (2 issues)**: #270, #450

**Remaining (9 issues)**:
| Issue | Title | Category |
|-------|-------|----------|
| #104 | CONV-FEAT-ALLOC: Time Allocation Analysis | Feature |
| #106 | CONV-FEAT-STRAT: Strategic Recommendations | Feature |
| #241 | CORE-ETHICS-TUNE: Post-Alpha Ethics | Ethics |
| #465 | FLY-COORD-TREES-2: Phase 3-5 Python | Infrastructure |
| #546 | TECH-DEBT: Alternate issue providers | Tech Debt |
| #558 | MUX-STANDUP-CONVERSE: LLM preference extraction | MUX |
| #568 | MUX-CORE-PORTFOLIO-ACROSS | MUX |
| #669 | COMPOSTING-HYBRID-TRIGGER | Learning |
| #760 | TECH-DEBT: slack_workspaces table | Tech Debt |

**Deferred to M6**: #358 SEC-ENCRYPT-ATREST (from M1, blocked on expert consultation)

---

### DIST — Distribution Packaging (NEW)

**Status**: 0/10 — Issues created Feb 21, 2026
**Theme**: MCP-native + Desktop distribution
**Epic**: #828 (DIST — Distribution Packaging)
**Placement**: After M6, before Beta

**Strategic rationale**: MCP-native first positions us for fluid UI surfaces while being the lightest distribution path. Desktop follows for standalone experience. Hosted deferred unless demand warrants.

**Phase 1 — MCP-Native (2-3 weeks)**:
| Issue | Title | Priority |
|-------|-------|----------|
| #829 | DIST-MCP-PACKAGE: Package Piper as MCP server | P0 |
| #830 | DIST-MCP-DOCS: Integration documentation | P0 |
| #831 | DIST-MCP-REGISTRY: Publish to registries | P1 |
| #832 | DIST-MCP-TEST: Integration testing | P1 |

**Phase 2 — Desktop (3-5 weeks)**:
| Issue | Title | Priority |
|-------|-------|----------|
| #833 | DIST-SQLITE: SQLite adapter | P0 |
| #834 | DIST-WRAPPER: Desktop application wrapper | P0 |
| #835 | DIST-UPDATE: Auto-update mechanism | P1 |
| #836 | DIST-INSTALLER: Platform installers | P1 |
| #837 | DIST-FIRST-RUN: First-run experience | P1 |

**Open Questions**:
1. Package name: `piper-morgan`? Check PyPI/npm availability
2. Electron vs Tauri: Needs investigation
3. Python bundling: Bundle runtime or require system Python?
4. Signing certificates: Apple ($99/yr), Windows ($200-400/yr)

---

## Sprint Summary

| Sprint | Theme | Total | Done | Remaining | % | Status |
|--------|-------|-------|------|-----------|---|--------|
| **M0** | Conversational Glue | 27 | 27 | 0 | 100% | ✅ COMPLETE (v0.8.6) |
| **M1** | MVP Foundation | 31 | 14 | 17 | 45% | ○ NEXT |
| **M2** | MVP Activation | 23 | 1 | 22 | 4% | — |
| **M3** | MVP Skills | 10 | 3 | 7 | 30% | — |
| **M4** | Document Revolution | 5 | 0 | 5 | 0% | — |
| **M5** | MVP Polish | 11 | 0 | 11 | 0% | — |
| **M6** | Future/Hardening | 11 | 2 | 9 | 18% | — |
| **DIST** | Distribution | 10 | 0 | 10 | 0% | — |
| **Total** | | **128** | **47** | **81** | **37%** | — |

---

## Timeline (Revised March 2026)

### February 2026
- [x] M0 sprint execution (Feb 16-18: 3 days vs 13-22 day estimate)
- [x] M0 bug fixes and quality gate resolution (Feb 19 - Mar 2)

### March 2026
- [x] M0 gate closure + v0.8.6 release (Mar 4)
- [ ] M1 sprint begin
- [ ] M1-M2 complete
- [ ] Security bugs resolved
- [ ] MUX wiring operational

### April 2026
- [ ] M3-M4 complete
- [ ] Skills + Documents operational
- [ ] MVP feature-complete approaching

### May 2026
- [ ] M5-M6 complete
- [ ] Security hardening
- [ ] v0.9 beta preparation

### June 2026
- [ ] DIST Phase 1 (MCP-native)
- [ ] Beta release

### July 2026
- [ ] DIST Phase 2 (Desktop)
- [ ] v1.0 launch preparation

---

## B2 Quality Gate (from PDR-002 v3)

**Definition**: "B2" represents the threshold where conversational glue works well enough that users experience Piper as a colleague, not a chatbot.

| Criterion | Test | Pass Condition |
|-----------|------|----------------|
| **Naturalness** | "Does this feel like talking to a colleague?" | Alpha testers agree ≥4/5 |
| **Memory** | "Does Piper remember what matters?" | Context references resolve >85% |
| **Proactivity** | "Are suggestions helpful or annoying?" | Acceptance >30%, annoyance <10% |
| **Discovery** | "Can I discover capabilities without docs?" | ≥3 features discovered/30 days |
| **Recovery** | "When things go wrong, does Piper help?" | >60% continue after hitting limits |
| **Flow** | "Can I accomplish goals naturally?" | No explicit command required |

---

## Version History

| Version | Date | Key Features |
|---------|------|--------------|
| v0.8.6 | Mar 4, 2026 | M0 Conversational Glue — 27 issues, 56-commit merge |
| v0.8.5.3 | Feb 11, 2026 | Windows compat, setup UX, 14 issues |
| v0.8.5.2 | Feb 6, 2026 | Alpha bug fixes, timezone alignment |
| v0.8.5.1 | Jan 31, 2026 | Alpha testing stabilization |
| v0.8.5 | Jan 27, 2026 | MUX-IMPLEMENT complete |
| v0.8.4.3 | Jan 18, 2026 | Fresh install fixes |
| v0.8.4 | Jan 12, 2026 | Sprint B1 Complete |

---

## Risk Mitigation

### Technical Risks
- **M0 expansion pattern**: 5 planned → 23 actual. Expect similar expansion in M1-M6
- **Assembly Assumption**: Wiring passes now standard practice post-sprint
- **Distribution complexity**: Phase 1 (MCP) is lightweight; Phase 2 (Desktop) has more unknowns

### Process Risks
- **75% pattern**: Mitigated by Beads Discipline (Pattern-046)
- **Vision flattening**: Anti-flattening safeguards in implementation guide
- **Scope creep**: Clear P0/P1/P2 prioritization per sprint

---

## Patterns Applied

- **Pattern-045**: Green Tests, Red User — M0 discovered 17 integration gaps
- **Pattern-046**: Beads Completion Discipline — Gate #779 enforces 100%
- **Pattern-047**: Time Lord Alert — Uncertainty signaling
- **Pattern-049**: Assembly Assumption — Wiring pass validates composition

---

## Change Log

### v14.3 (March 10, 2026)
- M0 COMPLETE — gate #779 closed, epic #762 closed, v0.8.6 released Mar 4
- 56-commit merge, 27 total issues (5 planned + 22 discovered)
- Inchworm position: 4.4.1 → 4.4.2
- Sprint summary updated: M0 100%, total 37% (47/128)
- Timeline updated through March
- Version history updated (v0.8.5.2, v0.8.5.3, v0.8.6)

### v14.2 (February 23, 2026)
- B2 quality gate assessment: NOT READY (CXO Feb 22 testing)
- #767 GLUE-SOFTINVOKE: Tests pass but users fail (Pattern-045)
- #763 GLUE-FOLLOWUP: Blocked by calendar query infrastructure issue
- #813 closed (coroutine mock bug fixed)
- #814 deferred from M0 to M1
- Sprint summary updated with B2 status column
- Total: 124 issues (40 done, 84 remaining = 32%)

### v14.1 (February 21, 2026)
- M0 actual status: 23 issues (18 done, 4 blocking gate, 1 gate issue)
- M1-M6 sprint data refreshed from GitHub exports
- DIST sprint created: Epic #828 + 9 children (#829-837)
- Sprint summary table with completion percentages
- Distribution consensus documented: MCP-native → Desktop → Hosted
- Timeline revised through July 2026
- Assembly Assumption pattern lesson captured
- Total MVP scope: 123 issues (38 done, 85 remaining)

### v14.0 (February 1, 2026)
- Added M0 (Conversational Glue Sprint) as critical path
- Updated inchworm position to 4.4.0
- PDR-002 updated to v3 with implementation guide
- Backlog freshness audit: 4 deferred, 1 merged, 1 closed
- B2 quality gate formalized

---

*Roadmap v14.3 — M0 COMPLETE (v0.8.6), M1 Next*
