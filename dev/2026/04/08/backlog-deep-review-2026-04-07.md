# Backlog Deep Review — 16 Potentially Superseded Issues

**Author**: Piper Alpha (PA)
**Date**: April 7, 2026
**Status**: Draft for PM review and discussion
**Purpose**: Audit each issue for remaining value, not just closure. "Squeeze every drop before discarding."

---

## The Dominant Pattern

Across all 16 issues, one pattern recurs: **the project evolved from "build code frameworks to enforce X" to "establish methodology and process infrastructure that achieves X."**

The FLY-VERIFY trilogy assumed Python classes would enforce verification. The INFR-AGENT issue assumed shell scripts would deploy multi-agent coordination. The CONV-MCP-* issues assumed a "Skills" framework would solve capability extension. In every case, the project found a different and better answer:

- Verification → Completion Discipline Triad (Patterns 045-047) + audit-cascade + gate verification
- Multi-agent coordination → CLAUDE.md roles + mailbox system + session logs + PM-mediated handoffs
- Capability extension → ADR-060 floor-first routing + MCP tools + workflow handlers

**This pattern is itself a product insight**: Piper Morgan's MVP may need less structured code infrastructure and more methodology tooling than the original backlog assumed. The floor-first principle (ADR-060) is the architectural expression of this learning.

---

## Recommendations Summary

| Issue | Title | Rec | Remaining Edge |
|-------|-------|-----|----------------|
| #167 | INFR-TEST: Regression testing gaps | CLOSE | API contract testing (future concern, not MVP) |
| #191 | POST-TEST-E2E: Web UI E2E Testing | CLOSE | Visual regression testing (post-MVP, if UI grows complex) |
| #273 | TEST-SMOKE: Smoke test epic | CLOSE | Empty stub; work lives in #927 |
| #276 | TEST-SMOKE-CI: Smoke tests in CI | CLOSE | Fold any residual smoke tests into #930 |
| #241 | CORE-ETHICS-TUNE: Post-Alpha Ethics | CLOSE | Ethics tuning with real users — refile when beta users exist |
| #310 | CONV-UX-QUICK: Settings & Startup | REVISE | Settings index page + loading states remain valid as post-MVP UX polish |
| #146 | FLY-VERIFY: Three-Tier Verification | CLOSE | Solved by methodology, not code framework |
| #147 | FLY-VERIFY-HAND: Handoff Protocol | CLOSE | Solved by mailbox/memo infrastructure |
| #148 | FLY-VERIFY-CONFIG: Configuration | CLOSE | Depends on #147; entire FLY-VERIFY trilogy superseded |
| #302 | CONV-MCP-DOCS: Document Processing | REVISE | Real need, wrong framing — strip "Skills" abstraction, scope to actual MCP architecture |
| #309 | CONV-MCP-PROTO: DocumentAnalysisSkill | CLOSE | Prototype for unadopted framework |
| #315 | CONV-MCP-LIBRARY: Core Skills Library | CLOSE | "Skills" framework not adopted |
| #312 | CONV-UX-DESIGN: Unified Design System | REVISE | Demote to post-MVP; scope to design tokens + dark mode |
| #313 | CONV-UX-DOCS: File Browser & Docs UI | CLOSE | #355 (DOCS-STOPGAP) is the right-sized version |
| #355 | DOCS-STOPGAP: Artifact Persistence | KEEP | Well-scoped, still relevant. MVP or Fast Follow decision needed. |
| #118 | INFR-AGENT: Multi-Agent Coordinator | CLOSE | Coordination operational via methodology, not software |

**Totals**: 12 close, 3 revise, 1 keep

---

## Detailed Analysis

### Group 1: Testing (Superseded by #927-930 E2E/AAXT Track)

**#167 INFR-TEST** (Sep 2025): Reacted to personality enhancement regressions. The pipeline it was concerned with (PersonalityEnhancer + formatting) no longer exists in the ADR-060 architecture. The E2E/AAXT track (#927-930) provides architecturally-aligned testing. **Edge**: API contract testing between frontend and API routes is not covered by #927-930 — file fresh if needed when UI evolves.

**#191 POST-TEST-E2E** (Sep 2025): Proposed Playwright browser automation. The project discovered ASGI-transport pytest gives equivalent coverage without browser overhead — and post-ADR-060, user journeys are conversational, not navigational. **Edge**: Visual regression testing if UI gains complexity beyond chat.

**#273 TEST-SMOKE** (Oct 2025): Empty stub epic. No content to preserve.

**#276 TEST-SMOKE-CI** (Oct 2025): Add existing smoke tests to CI. #930 defines more architecturally relevant CI jobs. **Edge**: Fold any remaining value (13 Slack component smoke tests) into #930 as sub-task.

### Group 2: Ethics and UX (Partially Superseded)

**#241 CORE-ETHICS-TUNE** (Oct 2025): Planned 4-week monitoring and tuning of ethics enforcement with real alpha users. The project still doesn't have real users — this is anticipatory planning for a situation that hasn't arisen. When beta users exist, the actual tuning needs will be different. **Edge**: Ethics tuning IS needed eventually, but should be filed fresh against the actual architecture and user base that exists at that point.

**#310 CONV-UX-QUICK** (Nov 2025): Bundle of UX quick wins. Startup welcome message addressed by floor-first routing. Settings index page and loading states/skeletons remain valid UX improvements. **Edge**: Settings discoverability and loading states — revise as post-MVP UX polish, remove P0 designation.

### Group 3: FLY-VERIFY Trilogy (Methodology Superseded Code)

**#146, #147, #148** (Sep 2025): Proposed Python classes (`ThreeTierVerification`, `MandatoryHandoffProtocol`, configuration layer) to enforce verification and handoff discipline. The project discovered verification is a methodology problem, not a code problem. The Completion Discipline Triad, audit-cascade, mailbox system, and PM-mediated coordination solve these concerns more effectively than automated enforcement would. **Edge**: None meaningful — the methodology approach is genuinely better.

**What this tells us**: The assumption that "agents need programmatic guardrails to prevent cutting corners" was wrong. What they actually need is clear process (session logs, evidence requirements, gate verification) and PM review. This is relevant to the MVP scope question — we don't need to build enforcement code.

### Group 4: CONV-MCP / Skills Framework (Framework Not Adopted)

**#302, #309, #315** (Nov 2025): Built on the "Skills" execution framework concept — a separate layer for capability extension with token reduction as the organizing principle. The project adopted MCP tools (ADR-052) and workflow handlers instead. The "Skills" abstraction was speculative architecture that didn't survive contact with implementation priorities.

**#302 edge**: Document processing is a real user need. Strip the "Skills" framing and scope to actual MCP/handler architecture. Consider whether #355 (DOCS-STOPGAP) is the right-sized version.

**#313 CONV-UX-DOCS** (Nov 2025): Comprehensive file browser. Way too much scope. #355 is the right-sized version.

**What this tells us**: The "Skills" framework was the CONV era's version of a premature abstraction. The project has learned (per Gall's Law) to build concrete capabilities first, then abstract if patterns emerge. This is directly relevant to the "what is MVP" question — don't build frameworks, build features.

### Group 5: Architecture Evolution

**#118 INFR-AGENT** (Aug 2025): Proposed deploying the Multi-Agent Coordinator via automation scripts with coordination accuracy metrics and latency targets. The actual multi-agent system is CLAUDE.md roles + mailboxes + session logs + PM mediation — document infrastructure, not software infrastructure.

**What this tells us**: The most successful infrastructure in the project (mailbox system, session logs, briefing architecture) is all document-based. The code infrastructure that was planned (agent coordinator, verification enforcement, skills framework) was never built because the document approach worked better. This is a fundamental insight for MVP scoping.

---

## Implications for "What Is MVP?"

Three themes emerge from this review:

### 1. Methodology Infrastructure > Code Infrastructure
The project's most valuable infrastructure is document-based (CLAUDE.md, briefings, mailboxes, session logs, omnibus logs, audit-cascade). The code infrastructure that was planned but never built (FLY-VERIFY, INFR-AGENT, Skills framework) was superseded by methodology. **Implication**: MVP should invest in methodology tooling (skills that help humans use the system) rather than enforcement code (systems that constrain agent behavior).

### 2. The Floor Handles More Than We Assumed
ADR-060 (floor-first routing) means the LLM handles most user interactions. Structured handlers are enhancements for specific side-effect operations. Many backlog issues assumed structured handlers were needed for capabilities the floor can handle conversationally. **Implication**: MVP scope should be filtered through the question "does this need a handler, or does the floor handle it?"

### 3. Gall's Law Keeps Winning
#355 (DOCS-STOPGAP) vs #313 (full file browser). #927-930 (focused E2E tests) vs #191 (Playwright framework). The right-sized, concrete approach consistently wins over the ambitious, abstract one. **Implication**: MVP should prefer small, concrete capabilities over ambitious frameworks. "Save as file" beats "document management system."

---

*Draft for PM review. Issues should be closed with proper evidence and audit-cascade per project convention.*
