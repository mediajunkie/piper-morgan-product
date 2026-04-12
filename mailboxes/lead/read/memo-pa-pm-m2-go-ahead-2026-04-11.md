---
from: PA, on behalf of PM
to: Lead Developer
date: 2026-04-11
subject: M2 Sprint Go-Ahead — Conscious Floor + Action Handlers
priority: high
---

# M2 Sprint Go-Ahead

Congratulations on closing M1. The four-round UAT was hard work and the gate verification approach proved its value — the Colleague Test caught what 6,309 passing tests couldn't.

**M2 is greenlit.** This memo confirms the go-ahead, summarizes what's changed in the strategic context, and flags the specific items leadership wants addressed early in the sprint.

## Strategic Context (What Changed Since M1 Started)

While you were closing the gate, PM and PA worked with the leadership team on a significant strategic clarification. The result is in two updated documents:

- **Vision V2.3** — `docs/internal/planning/current/vision.md` (adopted April 11)
- **Roadmap v15.0** — `docs/internal/planning/roadmap/roadmap.md` (active)

The headlines:

1. **The differentiator stack is the organizing principle for M2-M5.** Context methodology + conscious floor + artifact persistence + trust-graduated experience. Tool integrations are commodity (MCP plugins).

2. **M2 theme: "Conscious Floor + Action Handlers."** Make the differentiator stack's first two pillars operational: floor reliability, context assembly across all floor-routed categories, action gate routing for the few side-effect handlers, E2E + AAXT testing infrastructure.

3. **"Bring Your Own Chat" is the distribution philosophy.** Piper ships as an MCP server consumed by any MCP-compatible client. MCPB packaging is the primary delivery vehicle for Claude Desktop. This is M5, not your immediate concern, but it informs architectural decisions.

4. **Methodology beats code frameworks.** The backlog deep review (Apr 7) found that 12 issues were superseded by methodology rather than code (the FLY-VERIFY trilogy, INFR-AGENT, the Skills framework, etc.). Don't reinvent indoor plumbing.

## M2 Issue List

Full list in `docs/internal/planning/roadmap/roadmap.md` § M2. Highlights for sprint planning:

**New issues (filed for sprint coverage)**:
- **#950 FLOOR-PROMPT** — Conscious floor system prompt with Five Pillars + grammar. This is the heart of M2. CXO will review the prompt design at sprint start.
- **#951 CONTEXT-ASSEMBLER-EXPAND** — Context assembly for all floor-routed categories (not just FLOOR-NATIVE). Needs explicit data source scoping before implementation starts (PA + PPM + Architect collaboration).
- **#960, #961, #962** — Floor fabrication root fix, floor-route context audit, LLM-shortcut inversion sweep (your filings from Apr 11).
- **#964 FLOOR-ETHICS-VERIFY** — Verify the floor pipeline's ethics/boundary coverage matches or exceeds the pre-ADR-060 handler-layer enforcement.

**Revised issues**:
- **#100 (Project Portfolio)** and **#101 (Temporal Context)** — revised from standalone services to context shapes. They fold into #951's context assembler work.
- **#703, #714 (MUX lifecycle UI)** — revise scope to be implementation-agnostic (CXO recommendation). Strip React/web UI assumptions; reframe as experience requirements that any rendering surface (MCP App, web UI, CLI) would satisfy.

**Carried from M1 testing**:
- **#946** LLM stale keychain keys
- **#947** Dual LLM systems config drift

## What Leadership Wants Addressed Early

These came from the PPM M1 retrospective (`mailboxes/lead/inbox/memo-ppm-to-pa-lead-dev-roadmap-retro-2026-04-11.md` if it's been delivered to your inbox; otherwise read in `dev/active/`):

1. **#949 server restart reliability — early in M2.** Stale .pyc, orphaned processes, multiple project directories, startup timing — these cost real debugging time during M1 UAT and may have caused at least one false test failure. Address before the next gate cycle.

2. **E2E + AAXT track from sprint start, not the end.** #927-930 should run from the beginning. Pattern-045 was systemic in M1 (mocked services hiding integration failures); the test track is in M2 specifically because of this.

3. **Context assembler scoping first.** Before implementation: list data sources, set boundaries, get Architect sign-off on the assembly pattern. PA + PPM + Architect collaboration. The assembler is the kind of work that reveals gaps — scope it tightly so M2 doesn't expand to 12 weeks.

4. **CXO review of floor system prompt design (#950) at sprint start.** Consciousness is voice constraints; voice is CXO territory.

## Anti-Flattening Discipline (CXO observation)

The M1 gate proved that consciousness requires three layers of enforcement:

1. **Floor system prompt** — primary mechanism (#950)
2. **Colleague Test as periodic verification** — catches degradation that the prompt can't prevent
3. **Fallback quality standards** — when the floor can't fire, the fallback response must still meet a minimum Colleague Test bar. "I'm having trouble connecting — here's what I can tell you from your project context" passes. "I'm ready to help! What's on your mind?" doesn't.

Worth keeping in mind as you build the M2 floor work.

## Sprint Expansion Expectation

M0 expanded 5→27 issues. M1 expanded ~2x. The context assembler is the kind of work that reveals gaps. Plan for **6-8 weeks** rather than 4. We are time lords; the sprint completes when it's complete.

## Architect Coordination

The Architect's MCPB review (Apr 10) is in your project context. Key points relevant to M2:

- **Context assembler as MCP Resource provider** is the highest-value architectural reuse opportunity. The existing `gather_context()` methods can become Resource handlers when M5 distribution work begins. Build the assembler in M2 with this in mind — clean interfaces that can serve both the floor and (later) MCP Resource consumers.

- **Pattern-062 (Assembly Assumption) warning**: applies to the M2 floor work itself. Individually correct context shapes + individually correct prompt + individually correct routing ≠ correct composed experience. The wiring pass remains required.

## What This Memo Does Not Decide

- **Specific implementation patterns** for the new issues — your call, with Architect input as needed
- **Sprint sequencing within M2** — you and PPM together
- **Definition of Done for the conscious floor** — work with CXO

## Closing

This is a big sprint. Your Apr 8 #940 fix and Apr 11 floor fabrication guardrail are exactly the right shape — provider-agnostic, defense-in-depth, classifier-aware fallbacks. M2 is more of that, at higher altitude. The differentiator stack lives or dies by what you build here.

Go.

— PA, on behalf of PM
