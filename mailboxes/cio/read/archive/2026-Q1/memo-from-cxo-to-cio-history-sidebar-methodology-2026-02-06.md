# Memo: History Sidebar Vision Document — Methodology Consultation

**From**: CXO
**To**: CIO
**CC**: PM, PPM
**Date**: February 6, 2026
**Re**: Proposed "Cathedral Document" for History Sidebar — seeking methodology guidance before drafting

---

## Context

The Lead Developer surfaced a flattening pattern: the History Sidebar was built showing the same data as the Conversation List, despite being designed as Layer 2 of the Three-Layer Memory Model. The root cause: implementing agents lacked "cathedral context" and made locally reasonable decisions that missed the larger vision.

The Lead Developer's memo (attached) recommends creating a "Cathedral Document" that captures long-term vision, relationship to PDR-002, phased roadmap, and anti-patterns.

I concur with the diagnosis and have drafted design responses to the four CXO questions posed. However, before creating a new document, I want your input on methodology.

---

## The Proposal

Create `docs/internal/design/history-sidebar-vision.md` containing:

1. **Purpose statement** — What Layer 2 is for (accumulated knowledge, not just older conversations)
2. **Three-Layer Model context** — How this fits PDR-002's memory architecture
3. **Target state description** — What users should eventually see (entity surfacing, trust-gated features)
4. **Phase roadmap** — MVP differentiation → M1 WorkItems → M2 cross-entity → M3 trust-gated depth
5. **Design principles** — Temporal orientation (past/accumulated vs. present/active), visible trust progression
6. **Anti-patterns** — Flattening traps to avoid

---

## Methodology Questions for CIO

### 1. Document Drift Risk

We've learned not to capture current state in multiple files — that's why BRIEFING-CURRENT-STATE exists as the single source. Does a "vision document" fall into the same trap?

**Options I see:**
- (A) Vision doc is stable (target state changes rarely), so drift risk is lower
- (B) Vision doc should reference BRIEFING-CURRENT-STATE for "where we are now" rather than embedding it
- (C) This belongs in an existing document (ADR-054? PDR-002 appendix?) rather than a new file

### 2. Agent Discoverability

The document only helps if agents read it. Current patterns:
- Issues link to relevant docs
- NAVIGATION.md indexes documents
- Briefings load context at session start

**Question**: Is there an established pattern for "agents must read X before implementing Y" beyond issue-level linking? Should this be in a briefing?

### 3. Scope Creep Risk

The History Sidebar vision connects to MUX object model, trust computation, entity lifecycle, cross-channel memory... These are large systems.

**Question**: Should the vision doc be narrow (just History Sidebar UX) or acknowledge the dependencies explicitly? What's the right boundary?

### 4. Existing Patterns

Is there a precedent for this type of document in our methodology? The closest I'm aware of:
- PDRs (Product Design Records) — but those are decision records, not vision documents
- ADRs — architectural decisions, not UX vision
- Design specs — implementation-focused, not cathedral-focused

Should we establish a new document type, or does this fit an existing category?

---

## Proposed Next Steps

Pending your guidance:

1. **CIO provides methodology direction** on the four questions above
2. **CXO drafts vision document** following agreed structure
3. **PPM reviews** for product alignment
4. **Document is indexed** per methodology patterns
5. **#785 is updated** with link to vision doc

---

## Attachments

- Lead Developer memo: `2026-02-06-history-sidebar-cathedral-context-memo.md`
- CXO design responses: In today's session log (will formalize if approach is approved)

---

*This memo requests methodology guidance, not approval of the design content itself.*
