# Roadmap Restructure Proposal: v14.3 → v15.0

**Author**: Piper Alpha (PA)
**Date**: April 8, 2026
**Status**: DRAFT — for PM, PPM, CXO, and Architect review
**Context**: Product strategy conversation (Apr 7) + MUX analysis + backlog deep review + MCPB feasibility research

---

## Why a Restructure, Not Just a Refresh

The v14.3 roadmap was designed before:
- The floor-first insight (ADR-060) — most interactions don't need structured handlers
- The MUX analysis — consciousness is voice constraints, not code infrastructure
- The backlog review — 12 issues superseded, methodology consistently beat code frameworks
- The MCPB discovery — distribution via MCP bundle could eliminate the bespoke web UI from MVP
- The PA experiment — a well-briefed LLM with good context methodology handles most PM work conversationally

The M2-M6 sprint decomposition assumed a structured product with 19 intent categories, handler-per-feature architecture, dedicated personality services, and a bespoke web UI. That's no longer what we're building.

**We're not cutting scope for timeline reasons.** We're refocusing on what makes Piper Piper: the differentiator stack.

---

## The Differentiator Stack (What MVP Must Deliver)

1. **Context Methodology** — Five-layer model operationalized. How context assembles, persists, transfers, stays fresh.
2. **Conscious Floor** — LLM responses that embody the grammar, Five Pillars, and anti-flattening discipline.
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with lifecycle awareness.
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value.

**Indoor plumbing** (use commodity solutions): GitHub, Slack, Calendar, Notion via MCP plugins. File storage via SQLite/filesystem. Auth via standard patterns.

---

## Proposed Sprint Structure

### M1 — Foundation ✅ GATE VERIFICATION

**Status**: All 30 issues closed. Gates 3-4 verified. Gates 1-2 blocked on floor LLM connectivity (UAT rounds 1-2 failed, diagnostic in progress). 6,309 tests passing.

**What remains**:
- Fix floor LLM call (the #940 fix deployed but floor still not generating responses — active investigation)
- Todo completion + input parsing fixes
- Pass 14 UAT scenarios
- Canonical retest ≥85%

**No structural changes to M1.** The gate criteria are sound; the product just needs to meet them.

---

### M2 — Conscious Floor + Action Handlers [RESTRUCTURED]

**Theme**: Get the conscious floor working reliably and wire the few action handlers that perform side effects.

**Old M2 was**: "Activation" — WIRE-* wiring, MUX lifecycle UI, old testing issues.
**New M2 is**: Make the differentiator stack's first two pillars operational.

| Issue | Title | Category | Status |
|-------|-------|----------|--------|
| #925 | Floor inversion Phase 3-4 (STATUS, PRIORITY routing) | Floor | Open |
| #927 | E2E: Task lifecycle smoke tests | Testing | Open (assigned M2) |
| #928 | E2E: Automated canonical suite | Testing | Open (assigned M2) |
| #929 | AAXT: Golden scenarios with DeepEval | Testing | Open (assigned M2) |
| #930 | CI: E2E + AAXT nightly | Testing | Open (assigned M2) |
| NEW | Simplify intent routing to action gate (binary: side-effect vs conversation) | Architecture | **OPEN QUESTION** — scope TBD |
| NEW | Floor system prompt with Five Pillars + grammar + anti-flattening guidance | Consciousness | To file |
| NEW | Context assembler for all floor-routed categories (not just FLOOR-NATIVE) | Floor | To file |

**Moved out of M2**:
- #167, #191, #273, #276 — superseded by #927-930 (CLOSE)
- WIRE-* issues (#690-695) — **OPEN QUESTION**: how much wiring is needed if floor handles most interactions? Review each against action gate test.
- #304, #309, #310, #366, #371, #471 — review individually; most are either superseded or defer to Fast Follow

**Open question**: Should the action gate simplification (replacing 19-category classifier with a simpler binary) be M2 or a later refinement? The current classifier works; simplifying it is an optimization, not a fix.

---

### M3 — Artifact Persistence + Cross-Session Memory [RESTRUCTURED]

**Theme**: Conversation outputs that outlive the conversation. The bridge between "good conversation" and "useful PM tool."

**Old M3 was**: "Skills" — canonical queries, multi-agent coordinator, design system, skills library.
**New M3 is**: The third differentiator pillar — persistence with lifecycle awareness.

| Issue | Title | Category | Status |
|-------|-------|----------|--------|
| #355 | DOCS-STOPGAP: Basic Artifact Persistence (save, browse, retrieve) | Persistence | Open — PROMOTED to centerpiece |
| NEW | Artifact data model with lifecycle states (Emergent→Ratified→Archived→Composted) | Design | To file — design with composting in view, implement simple |
| NEW | Cross-session memory persistence (Redis or SQLite backing for conversation context) | Infrastructure | To file — fixes the Layer 4 gap |
| #669 | COMPOSTING-HYBRID-TRIGGER | Learning | Open — review for fit; may be Horizon 2 |

**Moved out of M3**:
- #118 (Multi-Agent Coordinator) — CLOSE, superseded by methodology
- #312 (Unified Design System) — REVISE, demote to Fast Follow (design tokens + dark mode)
- #315 (Core Skills Library) — CLOSE, "Skills" framework not adopted
- #496, #497 (canonical queries) — **OPEN QUESTION**: are these floor context shapes now? If so, they're part of context assembler work in M2, not separate "skills."
- #704, #716 (MUX lifecycle/features UI) — **OPEN QUESTION**: needed if MCPB + MCP Apps replaces bespoke web UI?

---

### M4 — Trust + Learning [RESTRUCTURED]

**Theme**: Earned proactivity and cumulative understanding. The fourth differentiator pillar.

**Old M4 was**: "Document Revolution" — document processing, file browser, document viewer.
**New M4 is**: The trust/learning experience that makes Piper grow with the user.

| Issue | Title | Category | Status |
|-------|-------|----------|--------|
| NEW | Trust graduation via context (lightweight, not dedicated TrustComputationService) | Experience | To file |
| NEW | User-correctable preferences (Claude memory model — infer, store, let user correct) | Experience | To file |
| NEW | Learning surfaced through trust gradient (low trust: facts only; high trust: suggestions) | Experience | To file |
| #558 | MUX-STANDUP-CONVERSE: LLM preference extraction | MUX | Open — fits naturally here |

**Moved out of old M4**:
- #302 (Document Processing) — REVISE, strip "Skills" framing; core need absorbed into M3 artifact persistence
- #313 (File Browser UI) — CLOSE, #355 is the right scope
- #712, #713 (Document viewer/lifecycle UI) — **OPEN QUESTION**: MCP Apps canvas or bespoke UI?

---

### M5 — Distribution + Polish [RESTRUCTURED]

**Theme**: Get Piper into users' hands. No point polishing what nobody can install.

**Old M5 was**: "Polish" — auth, Slack, FLY-VERIFY trilogy, thinking tokens, migration rollback.
**New M5 is**: Distribution first, polish alongside.

| Issue | Title | Category | Status |
|-------|-------|----------|--------|
| #829 | DIST-MCP-PACKAGE: Package Piper as MCP server | Distribution | Open |
| #830 | DIST-MCP-DOCS: Integration documentation | Distribution | Open |
| #831 | DIST-MCP-REGISTRY: Publish to registries | Distribution | Open |
| #832 | DIST-MCP-TEST: Integration testing | Distribution | Open |
| NEW | MCPB packaging with manifest, permissions, install UX | Distribution | To file — research complete |
| NEW | Claude Project template for Piper persona (hybrid MCPB + Project approach) | Distribution | To file |
| NEW | MCP Apps: artifact canvas / project dashboard | Distribution | To file — feasibility confirmed |
| #921 | FastAPI/Starlette upgrade | Infrastructure | Open (assigned M5) |
| #932 | SEC: HIBP stub | Security | Open (assigned M5) |
| #933 | SEC: API key validation | Security | Open (assigned M5) |
| #935 | TECH-DEBT: BudgetManager persistence | Tech Debt | Open (assigned M5) |
| #936 | TECH-DEBT: UserService persistence | Tech Debt | Open (assigned M5) |
| #441 | CORE-UX-AUTH-PHASE2 | Auth | Open |

**Moved out of old M5**:
- #146, #147, #148 (FLY-VERIFY trilogy) — CLOSE, superseded by methodology
- #272 (thinking tokens research) — defer to Fast Follow
- #338 (migration rollback) — defer to Fast Follow
- #463 (git worktrees) — defer to Fast Follow

**DIST Desktop Phase (old #833-837)**: Moved to Fast Follow. MCPB-first; standalone desktop app only if demand warrants.

---

### Deferred to Fast Follow (Post-MVP)

Issues moved from MVP that have residual value but aren't differentiator-stack work:

| Issue | Title | Reason for Deferral |
|-------|-------|-------------------|
| #100 | CONV-FEAT-PROJ: Project Portfolio | Review — may be floor-with-context |
| #101 | CONV-FEAT-TIME: Temporal Context | Review — may be floor-with-context |
| #103 | CONV-FEAT-PRIOR: Priority Engine | Review — may be floor-with-context |
| #104 | CONV-FEAT-ALLOC: Time Allocation | Horizon 2 |
| #106 | CONV-FEAT-STRAT: Strategic Recs | Horizon 2 |
| #244 | CONV-UX-SLACK: Interactive Standup | Commodity integration path |
| #272 | RESEARCH-TOKENS-THINKING | Research, not MVP |
| #312 | CONV-UX-DESIGN: Design System | Post-MVP polish (tokens + dark mode) |
| #338 | INFRA-MIGRATION-ROLLBACK | Infrastructure, not user-facing |
| #463 | FLY-COORD-TREES | Infrastructure, not user-facing |
| #546 | TECH-DEBT: Alternate issue providers | Post-MVP |
| #833-837 | DIST Desktop Phase 2 | After MCPB validates demand |
| WIRE-* | Various wiring issues | Review against action gate test |
| MUX-* lifecycle UI | Various UI issues | Review — MCP Apps may replace |

**Issues to CLOSE** (12 from backlog deep review):
#167, #191, #273, #276, #241, #146, #147, #148, #309, #315, #313, #118

**Issues to REVISE** (3 from backlog deep review):
#310 (demote to post-MVP UX polish), #302 (strip "Skills" framing), #312 (demote to design tokens + dark mode)

---

## Revised Sprint Summary

| Sprint | Theme | Focus | Status |
|--------|-------|-------|--------|
| **M1** | Foundation | Floor-first routing, security, testing | 🎯 GATE VERIFICATION |
| **M2** | Conscious Floor + Action Handlers | Floor reliability, action gate, E2E/AAXT | Next |
| **M3** | Artifact Persistence | Save/browse/retrieve, lifecycle data model, cross-session memory | — |
| **M4** | Trust + Learning | Earned proactivity, user-correctable preferences, composting | — |
| **M5** | Distribution + Polish | MCPB, MCP Apps canvas, security hardening, auth | — |

---

## Revised Timeline

```
April 2026
- [ ] M1 gate closure (floor fix + UAT round 3)
- [ ] M2 sprint begin
- [ ] IAC presentation (Apr 17, Philadelphia)
- [ ] Close 12 superseded issues
- [ ] File new issues for M2-M5 restructured scope

May 2026
- [ ] M2 complete (conscious floor operational + E2E/AAXT)
- [ ] M3 begin (artifact persistence)
- [ ] MCPB prototype (can start in parallel with M3)

June 2026
- [ ] M3 complete (artifacts persist, lifecycle data model in place)
- [ ] M4 begin (trust + learning)
- [ ] MCPB beta (early testers via .mcpb download)

July+ 2026
- [ ] M4 complete
- [ ] M5 execution (distribution polish, registry publish, security)
- [ ] Beta via MCPB
```

**Note**: These are not deadlines. We are time lords. The inchworm moves forward when each phase is complete, not when the calendar says so. Discovery work will expand scope (M0 went 5→27, M1 went 15→30+). Plan for it.

---

## Open Questions (For Leadership Review)

1. **Action gate simplification**: Replace 19-category classifier with binary (side-effect vs conversation)? Or keep classifier for analytics/learning while routing most to floor?

2. **WIRE-* issues**: How many need structured wiring if most interactions are floor-routed? Review each against "does this need a handler?"

3. **MUX lifecycle UI**: If MCPB + MCP Apps replaces the bespoke web UI, which MUX UI issues are still relevant? The artifact canvas via MCP Apps is confirmed feasible.

4. **CONV-FEAT cluster (#100, #101, #103)**: Are these floor-with-context or do they genuinely need structured code? Review together.

5. **MCPB persona gap**: The hybrid approach (MCPB for tools + Claude Project for persona) resolves the system prompt limitation. Does the Architect see risks in this architecture?

6. **Canonical queries (#496, #497)**: Are these now "context shapes for the floor" rather than separate skills? If so, they fold into M2 context assembler work.

7. **Composting (#669)**: Is composting M3 (persistence foundations) or M4 (learning)? The data model should be designed in M3 even if the composting engine is M4.

---

## Relationship to Other Documents

- **Vision V2.1** (`docs/internal/planning/current/vision-v2-draft.md`): Aligned. The differentiator stack maps to the Vision's four pillars.
- **MUX Analysis** (`dev/active/mux-analysis-what-survives-floor-first-2026-04-07.md`): Provides the conceptual foundation for the sprint restructuring.
- **Backlog Deep Review** (`dev/active/backlog-deep-review-2026-04-07.md`): Identifies the 12 closures, 3 revisions, and the "methodology beats code" insight.
- **MCPB Feasibility** (`dev/active/mcpb-feasibility-2026-04-08.md`): Confirms distribution path and MCP Apps opportunity.

---

*DRAFT — This is a proposal, not a decision. Requires PM authorization and leadership review (PPM, CXO, Architect) before replacing the current roadmap.*
