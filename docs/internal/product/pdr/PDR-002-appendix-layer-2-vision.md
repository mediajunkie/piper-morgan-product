# PDR-002 Appendix: Layer 2 Vision (History Sidebar)

**Parent PDR**: [PDR-002: Conversational Glue](../../planning/conversational-glue/PDR-002-conversational-glue-v3.md)
**Version**: 1.0
**Created**: February 6, 2026
**Owner**: CXO

---

## 1. Purpose of Layer 2

Layer 2 is the **User History** layer of the Three-Layer Context Persistence Model. It surfaces accumulated knowledge — not just older conversations, but the entities, work items, and patterns that emerged from those conversations.

**Layer 2 is NOT**:
- A duplicate of the conversation list (Layer 1)
- Just conversations with different styling
- An archive of old chats
- A place to "resume" recent work

**Layer 2 IS**:
- A searchable knowledge base of what Piper has learned about the user's world
- A surface where entities (WorkItems, Documents, People) become visible with lifecycle states
- The user's view into Piper's accumulated understanding
- Oriented toward the past/accumulated ("What have I built up?") rather than present/active ("What am I working on?")

**The core distinction**: Layer 1 answers "What conversation should I continue?" Layer 2 answers "What does Piper know about my work?"

---

## 2. Target State

When Layer 2 is complete, users will see:

### 2.1 Primary Content

- **WorkItems** with lifecycle states (draft → active → done → archived)
- **Documents** Piper has discussed or analyzed, with last-touched dates
- **People/Stakeholders** mentioned across conversations, with relationship context
- **Decisions** made (connected to tracked decisions, if any)
- **Conversations** as secondary context — "which conversations touched this entity?"

Entities are the primary content; conversations are navigation aids to entities.

### 2.2 Interactions

- **Search**: Real search across history, entities, and conversation content
- **Filter**: By entity type, lifecycle state, time period, trust level
- **Drill-down**: Click an entity to see related conversations and cross-references
- **Lifecycle management**: Mark items as archived, update states (at appropriate trust levels)

### 2.3 Trust-Gated Features

| Trust Level | Visible Features |
|-------------|------------------|
| Stage 1-2 | Conversation archive, basic search |
| Stage 3 | WorkItem surfacing, document tracking |
| Stage 4 | Cross-entity relationships, stakeholder mapping |
| Stage 5 | Full lifecycle management, pattern insights |

**Visibility principle**: Features are visible but may show as locked with explanation ("Available after Piper knows your work better"). Hidden features create "Piper can't do X" impressions; visible-but-locked features create "Piper is learning to do X" impressions.

---

## 3. Design Principles

### 3.1 Temporal Orientation

| Layer | Orientation | User Question | Feel |
|-------|-------------|---------------|------|
| Layer 1 (Conversation List) | Present/Future | "What am I working on?" | Active, ephemeral |
| Layer 2 (History Sidebar) | Past/Accumulated | "What have I learned/done?" | Archive, substantial |

This distinction must be felt, not just labeled. Different sort orders, groupings, and visual density reinforce the orientation.

### 3.2 Entities Over Conversations

Conversations are how knowledge enters the system. Entities are what the system knows. Layer 2 surfaces entities; conversations become context for entities.

**Anti-pattern**: Showing conversations as primary content with entity badges.
**Correct pattern**: Showing entities as primary content with conversation links.

### 3.3 Visible Growth

Piper is an "assistant proving themselves." Users should see Piper's knowledge growing over time. This means:
- New entity types unlock visibly (with subtle celebration)
- The sidebar becomes richer as trust increases
- "Coming soon" indicators hint at future capabilities
- Users can see the trajectory, not just the current state

### 3.4 Honest Incompleteness

If a feature isn't ready, show it as "growing" rather than hiding it. Users should understand what Piper is becoming, not just what Piper is.

**Exception**: Broken features (not incomplete, but actually broken) should be hidden until fixed.

---

## 4. Phase Roadmap

| Phase | Scope | Milestone |
|-------|-------|-----------|
| Phase 1 | **Differentiate from conversation list** — wire search, change framing language, archive-oriented grouping | M0 |
| Phase 2 | **WorkItem surfacing** — show WorkItems with basic lifecycle states (draft/active/done) | M1 |
| Phase 3 | **Cross-entity relationships** — "Documents mentioned in WorkItem X", stakeholder mapping | M2 |
| Phase 4 | **Trust-gated depth** — full feature set visible, locked features explained, unlock celebrations | M3 |

**Current phase status**: See [BRIEFING-CURRENT-STATE](../../../briefing/BRIEFING-CURRENT-STATE.md) — do not duplicate status here.

---

## 5. Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| "Just show conversations" | Duplicates Layer 1; misses Layer 2 purpose | Show entities as primary content; conversations as context |
| "Same data, different style" | Users see redundancy, not differentiation | Different content, different temporal orientation, different interactions |
| "Hide incomplete features" | Creates "Piper can't" impression; misses growth narrative | Show features as "growing" with honest framing |
| "Search UI without wiring" | Promises capability that doesn't exist | Either wire it or remove it; no theater |
| "Conversations recent-first" | Mirrors Layer 1 behavior | Archive-oriented grouping (by month, by entity, by project) |

---

## 6. Implementing Issues

Agents working on these issues should read this document first.

| Issue | Title | Phase |
|-------|-------|-------|
| #425 | MUX-IMPLEMENT-MEMORY-SYNC | Origin |
| #706 | MUX-OBJECTS-VIEWS | Phase 2 |
| #785 | History Sidebar differentiation | Phase 1 |
| #735 | History sidebar mounting | Phase 1 (complete) |
| TBD | GLUE-HISTORY-DIFF (if created) | Phase 1 |

**For implementers**: Before starting work on any issue above, ensure you can answer:

> "How does my implementation embody Layer 2's purpose — surfacing accumulated knowledge, not just showing older conversations?"

If you cannot answer this question, consult CXO or PPM before proceeding.

---

## 7. Related Documents

Architecture and implementation details live elsewhere.

| Document | Relationship |
|----------|--------------|
| [PDR-002: Conversational Glue](../../planning/conversational-glue/PDR-002-conversational-glue-v3.md) | Parent PDR defining Three-Layer Model |
| [ADR-054: Cross-Session Memory](../../architecture/current/adrs/adr-054-cross-session-memory-architecture.md) | Technical architecture for memory persistence |
| [ADR-053: Trust Computation](../../architecture/current/adrs/adr-053-trust-computation-architecture.md) | How trust levels are calculated |
| [ADR-045: Object Model](../../architecture/current/adrs/adr-045-object-model.md) | Entity definitions (WorkItem, Feature, etc.) |
| [domain-models.md](../../architecture/current/models/domain-models.md) | Entity lifecycle states |
| [2026-02-history-sidebar-design-archaeology.md](../../design/audits/2026-02-history-sidebar-design-archaeology.md) | Archaeological investigation that prompted this appendix |

---

## Changelog

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-02-06 | CXO | Initial draft based on Lead Dev memo and CIO methodology guidance |

---

*This is a vision document. It describes intent and behavior, not implementation. For technical details, see linked ADRs and issues.*
