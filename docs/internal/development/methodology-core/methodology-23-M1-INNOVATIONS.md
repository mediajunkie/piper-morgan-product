# Methodology 23: M1-Era Methodology Innovations

*Catalog of methodology changes from the M0-M1 period (Mar 2026). These innovations are already in practice but were not previously documented in methodology-core.*

*Source: CIO methodology audit (Mar 15, 2026), policy updates (Mar 16, 2026)*

---

## 1. Trigger-Based Methodology Audit

**Replaces**: Fixed 6-8 week calendar cadence.

**New rule**: Methodology audit within 2 weeks of each sprint gate closure. 8-week maximum interval as safety net.

**Rationale**: Calendar cadence creates audits disconnected from actual work rhythm. Sprint gates are natural reflection points where methodology gaps are freshest.

**Where documented**: `docs/internal/operations/staggered-audit-calendar-2026.md`, `methodology-audit-policy-updates-2026-03-16.md`

---

## 2. CIO Self-Approval for Emerging Patterns

**Replaces**: PM pre-approval required for all pattern catalog additions.

**New rule**: CIO can commit patterns to the catalog in "Emerging" status without PM pre-approval. PM retains upgrade/revision/removal authority.

**Rationale**: Requiring PM approval for every pattern discovery creates a bottleneck. Most patterns need to be captured quickly while context is fresh, then validated over time. The Emerging→Proven promotion path provides the quality gate.

**Where documented**: `BRIEFING-ESSENTIAL-CIO.md`, `methodology-audit-policy-updates-2026-03-16.md`

---

## 3. Wiring Pass as Sprint Phase

**From**: Pattern-062 (Assembly Assumption)

**Innovation**: The wiring pass — verifying that independently-built components actually connect — is now a planned sprint phase, not an afterthought.

**Rationale**: M1 repeatedly showed that components passing unit tests independently could fail when wired together. The Assembly Assumption (assuming components compose correctly because they work individually) is the root cause. A dedicated wiring pass catches these failures before gate testing.

**Where documented**: `docs/internal/architecture/patterns/pattern-062-assembly-assumption.md`

---

## 4. Floor-First Routing Principle (ADR-060)

**Innovation**: "The LLM is the floor, not the ceiling." Unmatched queries route to the LLM with assembled context rather than deflecting with "I can't do that." Structured handlers enhance above the floor; they don't gatekeep.

**Methodology implication**: Capability handlers extend the conversational floor — they don't replace it. Any query that reaches Piper should get at minimum a thoughtful LLM response. This shifts the quality bar from "did we handle every query?" to "is the floor experience good enough?"

**Where documented**: `docs/internal/architecture/adrs/adr-060.md`

---

## 5. Action Registry as Contract Enforcement

**Innovation**: 34 (category, action) pairs cataloged with `ActionDisposition` enum (CANONICAL, FLOOR, HANDLER, WORKFLOW). Emerged from the "extension without integration" discovery (Mar 16).

**Methodology relevance**: This is the structural fix for the Assembly Assumption at the layer-contract level. Rather than hoping components wire correctly, the Action Registry explicitly maps which intent categories route to which handlers, making the contract visible and testable.

**Where documented**: Pattern-062, `services/shared_types.py` (ActionDisposition enum)

---

## 6. Async Memo-Based Coordination

**Innovation**: The mailbox system and memo conventions have matured to the point where multi-role decisions happen without synchronous PM mediation. Demonstrated by #717 Product Concept resolution (Mar 22-24): Architect validates → CXO recommends → PPM revises → Lead consolidates, all via asynchronous memos over 3 days.

**Methodology relevance**: This changes the multi-agent coordination model from "PM mediates everything" to "agents coordinate directly through structured memos, PM reviews outcomes." Reduces PM bottleneck while maintaining decision quality through the memo audit trail.

**Where documented**: `mailboxes/DIRECTORY.md`, Pattern-029 (multi-agent coordination), methodology-02-AGENT-COORDINATION.md

---

*Created: March 31, 2026*
*Source: CIO methodology audit (Mar 15) + policy updates (Mar 16)*
*Owner: CIO / Documentation Management*
