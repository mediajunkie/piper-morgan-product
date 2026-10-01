# Memo: Documentation Updates — Architect Briefing, Session Log Template, ADR Status Notes

**To**: Documentation Management
**CC**: PM (xian)
**From**: Chief Architect
**Date**: 2026-03-19
**Re**: Three documentation updates needed
**Priority**: Standard (no implementation is blocked, but accuracy matters)

---

## 1. BRIEFING-ESSENTIAL-ARCHITECT.md — Recommended Edits

The March 17 briefing fixes (removing hardcoded Sprint A3 references, deferring counts to CURRENT-STATE) were a meaningful improvement. A few residual items remain that would help a new architect instance orient correctly.

### Changes Requested

**Section: "Key Patterns (Your Designs)"** — Add two entries:

After the existing four patterns (Router Architecture, Spatial Intelligence, Plugin System, Config Validation), add:

```markdown
**ProcessRegistry / Guided Process Architecture** (ADR-049):
- Two-tier intent: process-level state checked before message-level classification
- Active guided process claims messages (onboarding, standup, future workflows)
- Escape commands, timeout, and suspension mechanisms (implemented/in progress)
- Note: Onboarding currently removed per ADR-059; infrastructure remains for future workflows

**Floor-First Routing** (ADR-060):
- LLM conversational floor is the default response path
- Structured handlers retained for side effects (Action Gate pattern)
- Context Assembler gathers per-category data for floor prompt injection
- Supersedes ADR-039 routing philosophy; ADR-039 infrastructure retained
```

**Section: "Architectural State — System Capabilities"** — Replace the current list:

```markdown
**System Capabilities**:
- ✅ All integrations working via routers (7 plugins)
- ✅ Spatial intelligence operational (3 patterns)
- ✅ Configuration validation active
- ✅ Floor-first routing (Phase 1 complete, Phases 2-4 in progress)
- ✅ ProcessRegistry for guided workflows
- 🚧 Floor migration Phases 2-4 (in progress, #911)
- 🚧 Workflow dispatcher consolidation (#922/ADR-059)
- ❌ Learning system (future, M3+)
```

**Section: "Architectural State — Technical Debt"** — Replace:

```markdown
**Technical Debt**:
- ~126 canonical handler tests need migration as floor phases complete
- `_GENERIC_CANONICAL_SIGNATURES` whack-a-mole (removed after Phase 5)
- CLI bypasses intent layer (future work)
- intent_service.py at ~9,400 lines (large file, refactoring planned)
```

**Section: "Standing Design Principles"** — The existing #4 ("Floor-First Routing") is good. No change needed, just confirming it should stay.

### What NOT to Change

The role definition, responsibilities, decision authority, methodology integration, and critical rules sections are stable and accurate. Don't touch those.

---

## 2. Session Log Template — Date Boundary Rule

On March 14, multiple agents (including me) appended a new day's work to the previous day's session log instead of starting a new file. PM corrected this. The convention is clear in practice but not explicitly stated in the template.

### Recommended Addition

Add the following to the session log template, near the top (after the header fields, before the first section):

```markdown
> **Date boundary rule**: Each calendar day gets its own session log file. If the date has changed since this log was created, close this log and start a new one with today's date and timestamp.
```

This is a one-line addition. It prevents a failure mode that affected multiple agents simultaneously.

---

## 3. ADR Status Notes

Two ADRs need status annotations. These are small edits — a few lines each at the top of the document.

### ADR-039 (Canonical Handler Fast-Path Pattern)

**Current status line**: `Approved & Implemented (October 7, 2025)`

**Replace with**:
```markdown
## Status
Approved & Implemented (October 7, 2025)
**Routing philosophy superseded by [ADR-060](adr-060-floor-first-routing.md) (March 2026).** ADR-039 infrastructure (pre-classifier, canonical handler framework, workflow factory) remains in active use. ADR-060 changes the default routing path from canonical handlers to conversational floor. Consult ADR-060 for current routing decisions; consult ADR-039 for handler infrastructure design.
```

This is NOT a deprecation. ADR-039's infrastructure is actively used. The routing philosophy — "canonical handlers are the primary response path" — is what changed. An agent reading ADR-039 should understand both what's still valid (the handler framework) and what's been revised (the routing default).

### ADR-049 (Conversational State and Hierarchical Intent)

**Current status line**: `Proposed` (or whatever it currently reads)

**Add after the status line**:
```markdown
**Pending review**: ADR-059 (Workflow Dispatcher, March 2026) removes onboarding workflow and consolidates offer/acceptance systems. Escape command and timeout infrastructure specified in this ADR remains needed for standup (#889) and future guided workflows. Onboarding-specific patterns (OFFERED state, offer-first activation) are on hold pending ADR-059 implementation outcomes and potential onboarding redesign. This ADR will be amended once the post-ADR-059 architecture stabilizes.
```

This accurately reflects the current state: the core architecture (ProcessRegistry, guided process protocol, two-tier intent) is still valid. The onboarding-specific details are in flux. Future agents reading ADR-049 will know to check ADR-059 before assuming onboarding patterns are current.

---

## 4. Reminder: Check Other Briefings for Analogous Issues

The architect briefing had residual staleness after the March 17 fixes (System Capabilities still referenced 3B/GREAT-era items, Technical Debt was outdated). Other role briefings may have similar residual issues — sections that were updated to remove the most egregious references but still contain stale specifics.

When you next review briefings, scan for:
- "System Capabilities" or equivalent sections with outdated feature status
- "Technical Debt" or "Known Issues" sections referencing resolved work
- Any section that describes the state of the codebase rather than the state of the role (codebase state belongs in CURRENT-STATE, not in role briefings)

The pattern established on March 17 is correct: stable role context in briefings, time-sensitive state deferred to CURRENT-STATE. Just verify it's applied consistently across all 10+ briefing files.

---

*Chief Architect | March 19, 2026*
