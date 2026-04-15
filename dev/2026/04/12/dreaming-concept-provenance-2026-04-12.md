# Dreaming Concept Provenance Brief

**Purpose**: Reference for whoever designs the formal dreaming/memory architecture. Saves re-derivation of concepts that have already been articulated.

**Prepared by**: Docs, April 12, 2026

---

## The Two Types of Dreaming (xian's original concept)

### Type 1: Filing Dreams (consolidation/indexing)
- **Like a baby learning**: processing and organizing experiences, cross-referencing, extracting patterns
- Surfaces as: "Having had some time to reflect, it occurs to me..."
- **Status**: Fully specified in composting architecture. Not implemented.

### Type 2: Anxiety Dreams (threat simulation/risk rehearsal)
- **Like anxiety dreams**: the system imagines failure scenarios to prepare — "what if the floor fabricates again?", "what if the briefing is stale when the gate tester arrives?"
- Surfaces as: proactive risk identification, pre-emptive mitigation
- **Status**: Named once (Nov 26, 2025), then dropped from all subsequent design work. Not specified, not implemented. Janus confirmed (Apr 12, 2026) this concept has no equivalent in any of 20+ surveyed external memory systems — it is genuinely novel.

### The Unihemispheric Extension (added ~6 weeks later)
- **Like a dolphin**: sleeps one hemisphere at a time — never fully offline
- **Problem it solves**: the original dreaming model assumes idle time (user sleeps → Piper dreams). This breaks with power users, multi-timezone teams, dense schedules.
- **Proposal**: partial, rotating dreaming cycles — some components dream while others remain active
- **Key questions** (open): What components are separable? What triggers cycles if not idle time? How does this interact with multi-entity architecture?
- **Status**: Discussed Jan 11, 2026. CIO memo exists but is corrupted. Not yet designed.

---

## Source Artifacts (in chronological order)

### 1. Origin: Nov 26, 2025
**File**: `dev/2025/11/26/piper-morgan-ux-strategy-synthesis.md` (line 159)

> "The **dreaming model** (filing dreams for cross-referencing, anxiety dreams for risk simulation) aligns with research directions but goes further than current implementations."

This is the earliest capture of both types in one sentence. Written during the UX strategy synthesis with CXO.

### 2. Type 1 elaboration: Nov 29 – Dec 1, 2025
**Files**:
- `dev/2025/11/29/issue-MUX-TECH-PHASE4-COMPOSTING.md` — composting as Phase 4 of MUX tech
- `dev/2025/11/29/issue-MUX-VISION-LEARNING-UX.md` — "filing dreams" metaphor formalized
- `docs/internal/architecture/current/composting-learning-architecture.md` — full spec: CompostBin, Decomposer, LearningExtractor, InsightJournal, EmergentCreator. SCHEDULED trigger (2-5 AM quiet hours). Five trigger types: AGE, IRRELEVANCE, MANUAL, SCHEDULED, CONTRADICTION.

Type 2 ("anxiety dreams") is NOT mentioned in any of these. The composting pipeline is purely consolidation/indexing.

### 3. Roadmap integration: Dec 1, 2025
**File**: `knowledge/versions/roadmap-v12.1.md`

Two-layer journal architecture (Session vs Insight), "filing dreams" metaphor, trust gradient for background processing. Type 2 not mentioned.

### 4. Unihemispheric extension: Jan 11, 2026
**File**: `dev/2026/01/11/2026-01-11-1038-cio-opus-log.md` (line 89)

> "**Proposed frame**: Dolphins sleep one hemisphere at a time (unihemispheric sleep). Could Piper's learning architecture support partial, rotating dreaming cycles?"

CIO session with xian. Memo was drafted (`memo-cio-unihemispheric-dreaming-2026-01-11.md`) but the file in mailboxes/cio/read/ is **corrupted** (binary bookmark data, not markdown). xian may have a clean copy.

### 5. Revised memo: Jan 13, 2026
**File**: `docs/omnibus-logs/2026-01-13-omnibus-log.md` (lines 56, 99)

References "Revised unihemispheric dreaming (corrected: real-time learning IS built)" — the Architect corrected the CIO's initial understanding. The revised memo content is not separately preserved.

### 6. Post-floor-first survival: Apr 7, 2026
**File**: `dev/active/mux-analysis-what-survives-floor-first-2026-04-07.md`

PA's analysis preserves composting lifecycle as "constitutional" and the "filing dreams" framing. Does not mention Type 2.

### 7. External validation: Apr 12, 2026
**Files**:
- `mailboxes/docs/read/memo-janus-to-docs-memory-prior-art-response-2026-04-12.md`
- `dev/active/memo-docs-to-janus-memory-prior-art-2026-04-12.md`

Janus's cross-project memory research synthesis confirms Type 2 is absent from all 20+ surveyed external systems. "Genuinely novel."

---

## What Needs to Happen Next

1. **xian**: Check for clean copy of `memo-cio-unihemispheric-dreaming-2026-01-11.md`
2. **xian + PA or CIO**: Conversation to re-articulate Type 2 dreaming (anxiety/threat simulation) and the unihemispheric model. Output: ADR or composting-spec amendment.
3. **Designer**: Consider how Types 1 and 2 interact with the composting trigger mechanisms (AGE, IRRELEVANCE, MANUAL, SCHEDULED, CONTRADICTION). Type 2 may need new triggers: RISK_SIGNAL, GATE_APPROACHING, PATTERN_VIOLATION.
4. **Architect**: Assess whether the unihemispheric model requires changes to the composting-learning-architecture.md spec (written pre-floor-first, Nov 2025).

---

*This brief is research provenance, not a design document. It tells you where the ideas came from so you don't have to re-derive them.*
