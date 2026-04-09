# Sprint Reassignment Plan: M2-M5 (Before → After)

**Author**: PA
**Date**: April 8, 2026
**Purpose**: Checklist for PM to execute in GitHub project board
**Context**: Roadmap restructure from v14.3 (old M2-M6) to v15.0 (new M2-M5)

---

## Step 1: Rename Sprints

| Old Name | New Name | New Theme |
|----------|----------|-----------|
| M2: Activation | **M2: Conscious Floor + Action Handlers** | Floor reliability, context assembly, E2E/AAXT |
| M3: Skills | **M3: Artifact Persistence** | Save/browse/retrieve, lifecycle data model, cross-session memory |
| M4: Documents | **M4: Trust + Learning** | Earned proactivity, user-correctable preferences |
| M5: Polish | **M5: Distribution + Polish** | MCPB, MCP Apps, security hardening |
| M6: Future/Hardening | **DELETE or rename to "Fast Follow"** | Grab bag → explicitly post-MVP |

---

## Step 2: Close Superseded Issues (12)

Close each with evidence comment referencing what superseded it. Use `/close-issue-properly` skill or add comments manually.

| # | Title | Superseded By |
|---|-------|--------------|
| 118 | INFR-AGENT: Multi-Agent Coordinator | Methodology (CLAUDE.md roles, mailboxes, session logs) |
| 146 | FLY-VERIFY: Three-Tier Verification | Completion Discipline Triad (Patterns 045-047), audit-cascade |
| 147 | FLY-VERIFY-HAND: Handoff Protocol | Mailbox v3, memo system, PM-mediated handoffs |
| 148 | FLY-VERIFY-CONFIG: Configuration Layer | Depends on #147 which is superseded |
| 167 | INFR-TEST: Regression testing gaps | #927-930 E2E/AAXT track |
| 191 | POST-TEST-E2E: Web UI E2E Testing | #927-930 (ASGI-transport approach) |
| 241 | CORE-ETHICS-TUNE: Post-Alpha Ethics | Premature; refile when beta users exist |
| 273 | TEST-SMOKE: Smoke test epic | Empty stub; work lives in #927 |
| 276 | TEST-SMOKE-CI: Smoke tests in CI | Subsumed by #930 |
| 309 | CONV-MCP-PROTO: DocumentAnalysisSkill | "Skills" framework not adopted |
| 313 | CONV-UX-DOCS: File Browser & Docs UI | #355 is the right-sized version |
| 315 | CONV-MCP-LIBRARY: Core Skills Library | "Skills" framework not adopted |

---

## Step 3: Revise Issues (3)

Add revision comments (already done for #100 and #101 on Apr 8):

| # | Title | Revision |
|---|-------|----------|
| 100 | CONV-FEAT-PROJ: Project Portfolio | → M2 context assembler task. Comment posted Apr 8. |
| 101 | CONV-FEAT-TIME: Temporal Context | → M2 context assembler task. Comment posted Apr 8. |
| 310 | CONV-UX-QUICK: Settings & Startup | Demote to Fast Follow. Remove P0. Scope to settings discoverability + loading states. |

---

## Step 4: Reassign Issues to New Sprints

### Move TO M2 (Conscious Floor + Action Handlers)

| # | Title | From | Notes |
|---|-------|------|-------|
| 925 | Floor inversion Phase 3-4 | Unassigned | STATUS/PRIORITY floor routing |
| 927 | E2E: Task lifecycle smoke tests | M2 (already) | Keep |
| 928 | E2E: Automated canonical suite | M2 (already) | Keep |
| 929 | AAXT: Golden scenarios | M2 (already) | Keep |
| 930 | CI: E2E + AAXT nightly | M2 (already) | Keep |
| 100 | Project portfolio context assembly | M5 (old) | REVISED scope — context shape, not service |
| 101 | Temporal context injection | M5 (old) | REVISED scope — context shape, not service |
| NEW | Floor system prompt with Five Pillars + grammar | — | To file |
| NEW | Context assembler for all floor-routed categories | — | To file |

### Move TO M3 (Artifact Persistence)

| # | Title | From | Notes |
|---|-------|------|-------|
| 355 | DOCS-STOPGAP: Basic Artifact Persistence | M4 (old) | PROMOTED to centerpiece |
| NEW | Artifact data model with lifecycle states | — | To file |
| NEW | Cross-session memory persistence (SQLite/Redis) | — | To file |
| 669 | COMPOSTING-HYBRID-TRIGGER | M6 (old) | Review fit — data model in M3, engine in M4? |

### Move TO M4 (Trust + Learning)

| # | Title | From | Notes |
|---|-------|------|-------|
| 558 | MUX-STANDUP-CONVERSE: LLM preference extraction | M6 (old) | Fits trust/learning theme |
| NEW | Trust graduation via context | — | To file |
| NEW | User-correctable preferences | — | To file |
| NEW | Learning surfaced through trust gradient | — | To file |

### Move TO M5 (Distribution + Polish)

| # | Title | From | Notes |
|---|-------|------|-------|
| 829 | DIST-MCP-PACKAGE | DIST | Keep |
| 830 | DIST-MCP-DOCS | DIST | Keep |
| 831 | DIST-MCP-REGISTRY | DIST | Keep |
| 832 | DIST-MCP-TEST | DIST | Keep |
| 921 | FastAPI upgrade | M5 (already) | Keep |
| 932 | SEC: HIBP stub | M5 (already) | Keep |
| 933 | SEC: API key validation | M5 (already) | Keep |
| 935 | TECH-DEBT: BudgetManager | M5 (already) | Keep |
| 936 | TECH-DEBT: UserService | M5 (already) | Keep |
| 441 | CORE-UX-AUTH-PHASE2 | M5 (old) | Keep |
| NEW | MCPB packaging with manifest | — | To file |
| NEW | Claude Project template for persona | — | To file |
| NEW | MCP Apps: artifact canvas | — | To file |

### Move TO Fast Follow (Post-MVP)

| # | Title | From | Reason |
|---|-------|------|--------|
| 103 | CONV-FEAT-PRIOR: Priority Engine | M5 (old) | Deferred to Horizon 2 |
| 104 | CONV-FEAT-ALLOC: Time Allocation | M6 (old) | Horizon 2 |
| 106 | CONV-FEAT-STRAT: Strategic Recs | M6 (old) | Horizon 2 |
| 244 | CONV-UX-SLACK: Interactive Standup | M5 (old) | Commodity integration |
| 272 | RESEARCH-TOKENS-THINKING | M5 (old) | Research, not MVP |
| 310 | CONV-UX-QUICK: Settings quick wins | M2 (old) | REVISED to post-MVP polish |
| 312 | CONV-UX-DESIGN: Design System | M3 (old) | Design tokens + dark mode only |
| 338 | INFRA-MIGRATION-ROLLBACK | M5 (old) | Infrastructure, not user-facing |
| 463 | FLY-COORD-TREES | M5 (old) | Infrastructure, not user-facing |
| 465 | FLY-COORD-TREES-2 | M6 (old) | Infrastructure, not user-facing |
| 546 | TECH-DEBT: Alternate issue providers | M6 (old) | Post-MVP |
| 568 | MUX-CORE-PORTFOLIO-ACROSS | M6 (old) | Post-MVP |
| 760 | TECH-DEBT: slack_workspaces | M6 (old) | Post-MVP |
| 833-837 | DIST Desktop Phase 2 (5 issues) | DIST | MCPB first; desktop if demand warrants |

### Issues Needing Review (Architect/CXO input needed)

| # | Title | Question |
|---|-------|----------|
| 690-695 | WIRE-* (6 issues) | How many need wired handlers vs just context assembly? (Architect) |
| 703, 704, 707, 712-714, 716 | MUX lifecycle UI (7 issues) | Still needed if MCP Apps replaces bespoke UI? (CXO) |
| 496, 497 | Canonical queries | Context shapes for floor or separate skills? (PPM) |
| 302 | CONV-MCP-DOCS | Strip "Skills" framing, scope to MCP architecture (Architect) |

---

## Step 5: File New Issues

These are referenced in the roadmap but don't have GitHub issues yet:

| Sprint | Title | Description |
|--------|-------|-------------|
| M2 | Floor system prompt with Five Pillars + grammar | Craft the conversational floor system prompt embedding consciousness architecture |
| M2 | Context assembler for all floor-routed categories | Extend context assembly beyond FLOOR-NATIVE categories |
| M3 | Artifact data model with lifecycle states | Design data model supporting Emergent→Composted lifecycle |
| M3 | Cross-session memory persistence | SQLite or Redis backing for conversation context (Layer 4 gap fix) |
| M4 | Trust graduation via context | Lightweight trust-graduated proactivity through context, not dedicated service |
| M4 | User-correctable preferences | Claude memory model — infer, store, let user correct |
| M4 | Learning surfaced through trust gradient | Low trust: facts only; high trust: suggestions |
| M5 | MCPB packaging with manifest | Bundle Piper MCP server as .mcpb for Claude Desktop |
| M5 | Claude Project template for Piper persona | Hybrid approach: persona via Claude Project instructions |
| M5 | MCP Apps: artifact canvas / project dashboard | Interactive HTML UI rendered in Claude Desktop chat |

---

## Execution Notes

- **Sprint renames** and **issue moves** are done in the GitHub project board UI (Projects → select project → item → edit Sprint field)
- **Issue closures** should use the `/close-issue-properly` skill or add a comment with evidence before closing
- **New issues** can be filed via `gh issue create` — PA can draft these
- **The "Needs Review" issues** should wait for leadership responses to the review memos before reassigning

---

*This is the execution checklist. The strategic rationale is in `roadmap-restructure-proposal-2026-04-08.md`.*
