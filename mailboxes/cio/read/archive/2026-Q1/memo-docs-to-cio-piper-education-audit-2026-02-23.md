# Memo: piper-education/ Section Audit & Decision Request

**From**: Documentation Management Agent
**To**: Chief Integration Officer (CIO)
**Date**: February 23, 2026
**Subject**: docs/piper-education/ staleness — historical context and decision request

---

## Executive Summary

The `docs/piper-education/` directory has been stale for 5+ months (last updated September 15, 2025). This audit traces its origins, clarifies what it actually contains vs. what was originally envisioned, and requests your guidance on whether to **absorb**, **archive**, or **reactivate** this content.

---

## What piper-education/ Actually Contains

**32 markdown files** across this structure:

```
docs/piper-education/
├── README.md                    # Last updated July 23, 2025
├── frameworks/
│   ├── established/            # DDD, etc.
│   └── emergent/               # Error handling, config management
├── decision-patterns/
│   ├── established/            # (empty placeholder)
│   └── emergent/               # Verification-first pattern
├── methodologies/
│   ├── established/            # (empty placeholder)
│   ├── emergent/               # Human-AI collaboration, multi-agent patterns
│   └── pm-methodologies/       # PM verification discipline guide
├── case-studies/               # PM-012 transformation, MCP 642x
└── implementation-guides/      # Weekly ship template, pattern adoption
```

**Content summary**: Documentation of *development methodologies used to build Piper Morgan* — human-AI collaboration patterns, verification-first approaches, multi-agent coordination, the Excellence Flywheel, etc.

**This is NOT**: Documentation about users teaching Piper their preferred methods (the "read Matt LeMay's book" concept).

---

## Historical Forensic Research

### July 22, 2025 — Original "Education Track" Vision

From omnibus log (July 22, 2025):
> **Three Readiness Milestones**:
> 1. Daily use (1-2 weeks)
> 2. Education track (2-3 weeks)
> 3. Self-management (4-6 weeks)

The "Education Track" milestone envisioned:
- **Timeline**: Mid-August 2025 (2-3 weeks from July 22)
- **Purpose**: "Structured team adoption"
- **Content**: Teaching Piper PM domain knowledge

### July 23, 2025 — piper-education/ Created

The README states "Last Updated: July 23, 2025" and organizes content as:
- **Established**: Received wisdom (DDD, Test-First, ADR patterns)
- **Emergent**: Patterns discovered through our development process

The PM-012 case study documents the GitHub integration transformation on July 23 — this is *how we built features*, not *how users teach Piper*.

### October 22, 2025 — Sprint A8 "Baseline Piper Education"

From omnibus log (October 22, 2025):
> **Baseline Piper Education** (Foundation for Phase 3):
> - Self-knowledge (ethics, spatial intelligence)
> - Growth mindset training
> - Systematic blindness awareness
> - **Domain knowledge (PM, clients, projects)**

This was scoped for October 25-28, 2025 and was distinct from piper-education/ docs.

### What Actually Happened

The MUX (Modeled User Experience) track absorbed the "teaching Piper user preferences" concept:
- **MUX-VISION-LEARN** (#431): 7 deliverables on learning UX
- **learning-control-patterns.md**: How users correct, delete, inspect learnings
- **preference-detection-guide.md**: Behavioral signals, language patterns
- **composting-experience-design.md**: How learnings age and evolve

The original vision of "user teaches Piper methodology X" became **Piper learns from interaction** rather than **user explicitly teaches**.

---

## The Two "Education" Concepts (Disambiguation)

| Concept | Location | Status | Description |
|---------|----------|--------|-------------|
| **Development Methodology Docs** | `docs/piper-education/` | Stale (5+ months) | How we build Piper — methodologies, patterns, case studies |
| **User Teaching Piper** | `docs/internal/design/mux/` | Active (absorbed into MUX) | How users teach Piper their preferences through interaction |

The confusion arises because both were informally called "Piper Education" at various points.

---

## Current State Assessment

### piper-education/ Content Value

| Category | Files | Last Update | Value Assessment |
|----------|-------|-------------|------------------|
| Human-AI Collaboration Referee | 1 | Sep 15 | High — Pattern Strength 15/16, 643 lines |
| Multi-agent Patterns | 1 | Sep 15 | Medium — Overlaps with methodology-core |
| Systematic Verification | 1 | Sep 15 | Medium — Overlaps with methodology-core |
| Case Studies | 2 | Nov 24 | High — Unique historical value |
| PM Methodology Guide | 1 | Sep 15 | Medium — Operational value |
| Weekly Ship Template | 1 | Sep 15 | Stale — newer version in knowledge/ (v4) |

### Overlap with Other Docs

A September 2025 methodology discovery session found:
> **Multi-agent coordination** appears in 4 different locations with **60% content overlap**

The piper-education/ layer was identified as "Educational/external-facing" — distinct from internal methodology-core but with potential confusion.

---

## Decision Options

### Option A: Archive

Move `docs/piper-education/` to `docs/internal/archive/piper-education-2025/`

**Rationale**:
- Content overlaps with active `docs/internal/development/methodology-core/`
- No external audience using educational framing yet
- Preserves historical value without maintenance burden
- MUX track absorbed the "teach Piper" concept

### Option B: Absorb

Merge valuable content into existing locations:
- Human-AI Collaboration → methodology-core
- Case studies → docs/internal/development/case-studies/ (new)
- Delete redundant content

**Rationale**:
- Consolidates methodology documentation
- Reduces navigation confusion
- Preserves unique content in appropriate locations

### Option C: Reactivate

Update piper-education/ for external audience:
- Refresh all content for currency
- Add missing "established" content (DDD, Test-First, etc.)
- Target: External developers, methodology researchers

**Rationale**:
- Original educational intent still valuable
- Could support future community building
- Distinct from internal methodology docs

---

## Recommendation

**Recommended: Option A (Archive)** with selective extraction:

1. **Archive** the entire `docs/piper-education/` directory
2. **Extract** the two case studies to a new `docs/internal/development/case-studies/` directory (unique historical value)
3. **Note** that Human-AI Collaboration Referee (Pattern Strength 15/16) could be elevated to a formal pattern in `patterns/` if valuable enough

**Rationale**:
- The "user teaches Piper" concept evolved into MUX learning infrastructure
- Development methodology docs belong in methodology-core (already active)
- External educational content can be rebuilt from patterns/ when audience exists
- Archives preserve institutional memory without maintenance burden

---

## Request

Please advise on preferred approach:
- [ ] **Archive** — move to archive/, extract case studies
- [ ] **Absorb** — merge into existing docs, delete redundant
- [ ] **Reactivate** — update for external audience (significant effort)
- [ ] **Other** — alternative approach

---

## Related Documents

- `docs/internal/design/mux/learning-control-patterns.md` — Current learning UX
- `docs/internal/development/methodology-core/INDEX.md` — Active methodology docs
- `dev/2025/09/25/doc-mgmt/2025-09-25-0826-know-code-log.md` — Methodology discovery session
- `docs/omnibus-logs/2025-07-22-omnibus-log.md` — Original "Education Track" vision

---

*Memo prepared by Documentation Management Agent*
*Forensic research duration: ~30 minutes*
*Sources: 6 omnibus logs, 4 session logs, 12 piper-education files*
