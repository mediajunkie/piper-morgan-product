# Piper Morgan Design System

This directory contains UX specifications, design briefs, and interaction guidelines for Piper Morgan. **All UI/UX work should consult these documents before implementation.**

---

## Design Philosophy (v1.0)

*Approved by CXO — January 8, 2026*

### 1. Colleague, Not Tool
Piper is a professional colleague who happens to be AI—not a chatbot, not a feature, not an assistant. Design every interaction as you would design communication between trusted coworkers.

### 2. Trust Gradient
Behavior adapts based on relationship maturity. New users experience restraint; established users experience anticipation. Trust is earned through demonstrated value, never assumed.

### 3. Discovery Through Use
Users learn Piper's capabilities by using them, not by reading about them. Design for progressive revelation through natural interaction, not documentation or feature tours.

### 4. Context-Aware, Not Creepy
Piper uses what it knows to be helpful, but respects boundaries. The test: Would a thoughtful colleague remember this, or would remembering it feel invasive?

### 5. Always Useful, Never Stuck
Piper provides value even with limited context, degraded integrations, or partial information. Users should never hit dead ends without a path forward.

---

## Document Hierarchy

*Confirmed by CXO — January 8, 2026*

When specs conflict, defer to higher-numbered authority:

| Precedence | Type | Purpose | Location |
|------------|------|---------|----------|
| 4 (highest) | **PDRs** | Strategic intent ("why we decided") | [docs/internal/pdr/](../product/pdr/) |
| 3 | **Design Briefs** | Tactical direction ("what we're doing") | [briefs/](briefs/) |
| 2 | **UX Specs** | Implementation details ("how it works") | [specs/](specs/) |
| 1 (lowest) | **Voice Guides** | Tone and copy ("how it sounds") | [specs/empty-state-voice-guide-v1.md](specs/empty-state-voice-guide-v1.md) |

> **Settled Decisions Are Not Re-Litigated**
>
> When a PDR marks a decision as "settled" or "decided," agents should not propose alternatives unless they have new evidence that wasn't available when the decision was made. If an agent believes a settled decision should be revisited, they should flag this explicitly rather than simply offering a different approach.

---

## Current Specifications

### Interaction Patterns

| Spec | Domain | Status | Consult When... |
|------|--------|--------|-----------------|
| Cross-Session Greeting UX *(proposed; doc TBD — index claimed "v1 Final" but no file exists at this or any path, checked 2026-09-02)* | Greetings | — | Implementing greeting logic |
| [Contextual Hint UX](specs/contextual-hint-ux-spec-v1.md) | Suggestions | v1 Final | Adding proactive hints |
| [Multi-Entry FTUX](specs/multi-entry-ftux-exploration-v1.md) | Onboarding | v1 Final | Modifying setup flow |
| [Empty State Voice Guide](specs/empty-state-voice-guide-v1.md) | Empty States | v1 Final | Writing empty state copy |
| [Canonical Queries](specs/canonical-queries-v2.md) | Query Patterns | v2 Final | Implementing user queries |

### Quality & Measurement

| Spec | Domain | Status | Consult When... |
|------|--------|--------|-----------------|
| [B1 Quality Rubric](specs/b1-quality-rubric-v1.md) | Quality Gates | v1 Final | Assessing feature readiness |

### Strategic Direction

| Brief | Domain | Status | Consult When... |
|-------|--------|--------|-----------------|
| [Conversational Glue](briefs/conversational-glue-design-brief.md) | Conversation UX | Active | Designing conversation flows |
| [Discovery UX Strategy](briefs/cxo-brief-discovery-ux-strategy.md) | Capability Discovery | Active | Helping users find features |

---

## For LLM Agents

**Before implementing any UI/UX changes:**

1. Read this README to understand the design philosophy
2. Check the spec table above for relevant documents
3. If your domain isn't covered, **flag for PM/CXO review before proceeding**
4. When in doubt, favor consistency with existing patterns over novelty

**Red flags that suggest you're going rogue:**

- Creating new interaction patterns not in specs
- Writing copy that doesn't match voice guide tone
- Adding UI elements without checking empty state guidance
- Implementing greetings without consulting greeting spec
- Inventing new UX patterns without consulting existing specs

**The Contractor Test:** When writing copy or designing interactions, ask: "Would this feel appropriate from a contractor you hired last month?" If it feels too familiar or too cold, adjust.

**When you encounter a gap:**

```
⚠️ UX GAP DETECTED

Domain: [what you're implementing]
Searched: [which specs you checked]
Gap: [what's missing]

Options:
1. Proceed with pattern from [similar spec]
2. Flag for CXO/PM review
3. [your recommendation]

Awaiting guidance.
```

---

## For Human Designers

- New specs go in `specs/` with naming: `[domain]-[type]-spec-v[n].md`
- New briefs go in `briefs/` with naming: `[domain]-brief.md`
- Update this README when adding new documents
- Version specs (v1, v2) rather than overwriting

---

## For External AI Tools (ChatGPT, Cursor, etc.)

Collaborators using AI coding assistants outside the Claude Project should load UX context before doing design work.

| Resource | Purpose |
|----------|---------|
| [AI Context for Piper UX](ai-context-piper-ux.md) | Paste-ready context establishing design philosophy, voice guidelines, and settled decisions |

**Usage:**
1. Copy the contents of `ai-context-piper-ux.md`
2. Paste as system context, project instructions, or initial prompt
3. Proceed with UX work—the AI will be constrained to our approach

This ensures external tools align with Piper's design philosophy even though they don't have native access to the project knowledge base.

---

## MUX (Modeled UX) 2.0

Strategic UX vision and architecture work from Nov 2025:

| Document | Focus |
|----------|-------|
| [UX Foundations & Open Questions](mux/piper-morgan-ux-foundations-and-open-questions.md) | Core UX principles and unresolved questions |
| [UX Strategy Synthesis](mux/piper-morgan-ux-strategy-synthesis.md) | Strategic synthesis |
| [MUX Vision: Learning UX](mux/MUX-VISION-LEARNING-UX-updated.md) | Learning system UX vision |
| [UX Strategic Brief](mux/ux-strategic-brief-chief-architect-chief-of-staff.md) | Executive brief |
| [MUX Tech Phases 1-4](mux/) | Technical implementation phases (Grammar, Entity, Ownership, Composting) |

### MUX Concepts: What's Settled vs. What's Evolving

*CXO Decision — January 8, 2026*

The MUX work established foundational concepts that inform our design thinking. Some are settled; others remain exploratory.

**Settled** (design with these):
- **Grammar**: "Entities experience Moments in Places"
- **Lifecycle**: Emergent → ... → Composted (feeds learning)
- **Situation as container**: Situations contain Moments (not a parallel substrate)
- **Four substrates**: Entities, Places, Moments, Situations
- **Two journaling layers**: Session + Insight

**Exploratory** (don't constrain to these yet):
- Specific lens definitions (8 dimensions — still refining)
- Cognitive faculty boundaries (Perception/Orientation/Judgment)
- Advanced trust features (premonitions at high trust)
- Non-human sapient modeling
- Agent inbox/outbox patterns

A developer reading the design system should understand the grammar model and use it for mental framing, but should not feel bound to implement exactly 8 specific lenses or assume the cognitive categories are final.

---

## Research

Foundational research informing design decisions:

| Document | Focus |
|----------|-------|
| [UX for AI Research Reconnaissance](research/ux-for-ai-research-reconnaissance.md) | Field landscape, key thinkers, pattern libraries, thematic clusters |
| [Mobile UX Opportunity Mapping](research/mobile-ux-opportunity-mapping.md) | Gesture-driven entity-aware mobile patterns, notification design |

---

## Audits

Historical UX audits:

- [November 2025 UX Audit](audits/2025-11-ux-audit/) - 15 files covering interaction patterns, journey mapping, design system, gap analysis, strategic recommendations

---

## Related Resources

- [PDRs](../product/pdr/) - Product Decision Records (strategic)
- [ADRs](../architecture/adrs/) - Architecture Decision Records (technical)
- [Pattern Library](../architecture/patterns/) - Implementation patterns
- [CXO Briefing](../../briefing/BRIEFING-ESSENTIAL-CXO.md) - CXO role context

---

## Coverage Gaps (Known)

The following areas need UX spec coverage:

- [ ] Error messaging and recovery flows
- [ ] Mobile interaction patterns
- [ ] Accessibility guidelines
- [ ] Dark mode / theming
- [ ] Loading states and skeleton screens

---

*Last updated: 2026-01-08*
*Maintainer: CXO (primary), Documentation Manager (operational)*
