# MUX Analysis: What Survives the Floor-First Insight

**Author**: Piper Alpha (PA)
**Date**: April 7, 2026
**Status**: Analysis document for project record
**Context**: Deep dive into MUX (Modeled User Experience) documentation, triggered by backlog review revealing that the project consistently evolved from "code frameworks" to "methodology infrastructure." This analysis asks: given the floor-first insight (ADR-060) and the PA experiment, which MUX concepts are constitutional and which were scaffolding?

---

## The Question

Piper Morgan has accumulated rich UX conceptual work: the object model grammar, five pillars of consciousness, anti-flattening measures, perceptual lenses, composting lifecycle, trust gradient, Radar O'Reilly pattern, semantic gesture mapping, and more. Some of this was designed when the assumption was that Piper would need heavy structured infrastructure (handlers, classifiers, workflow orchestration) for every interaction.

Now we know:
- The LLM floor handles most conversational PM work without structured handlers (ADR-060)
- Tool integrations are commoditized via MCP/plugins — "don't reinvent indoor plumbing" (xian)
- The PA experiment shows a well-briefed LLM with good context methodology can do standup synthesis, triage, memo routing, and analytical writing conversationally
- Intent classification with 19 categories may be over-specified when most categories route to the floor anyway
- The project's most valuable infrastructure is document-based methodology, not code frameworks

**The question isn't "was the MUX work wrong?" — it's "what's constitutional and what was scaffolding?"**

---

## What's Constitutional (Survives Everything)

### 1. The Grammar: "Entities Experience Moments in Places"

This is the project's core intellectual property. It's a decision filter, not a data schema. During MUX-IMPLEMENT, it caught category errors ("Should Insights have lifecycle states?" → "What would BLOCKED insight mean?" → category error, insights are composted output). It will continue to catch errors as long as anyone asks "does this feature make grammatical sense?"

**Why it survives floor-first**: The grammar doesn't require structured handlers. It constrains how the floor *thinks about* PM work. A floor response that says "I noticed a blocker in the sprint" is grammatically correct (Entity observing a Moment in a Place). One that says "Query returned 3 blocked items" is not. The grammar operates at the prompt/context layer, not the handler layer.

**Substrates**: Entities (actors with agency), Places (contexts with atmosphere), Moments (bounded significant occurrences), Situations (the encompassing frame — not a fourth substrate).

**Ownership modes**: Native (Piper's Mind — sessions, memories, concerns), Federated (Piper's Senses — GitHub issues, Slack messages), Synthetic (Piper's Understanding — assembled projects, inferred risks). These determine storage, updating, and trust levels.

### 2. The Five Pillars of Consciousness

Identity Awareness, Time Consciousness, Spatial Awareness, Agency Recognition, Predictive Modeling. These aren't features to build — they're qualities that every Piper response must exhibit. They're *constraints on how the floor speaks*.

- **Identity**: "I found 3 tasks" not "Query returned 3 results"
- **Time**: "Earlier this afternoon" not "14:32:07 UTC"
- **Spatial**: "Over in GitHub" not "Source: github.com/api/v3"
- **Agency**: "Would you like me to..." not silent action
- **Prediction**: "I'm noticing a pattern" not "Alert: threshold exceeded"

**Why they survive**: These are implemented through the floor's system prompt and context assembly, not through handler code. They constrain *voice*, not *routing*.

### 3. Anti-Flattening as Ongoing Discipline

Consciousness degrades through well-intentioned optimization. Each cut is defensible; the cumulative effect is death by a thousand cuts. The project's own history proves this: consciousness was designed into the architecture but survived intact only in the Morning Standup, because that's where someone cared about the output layer, not just the data layer.

The UAT (April 3) proved anti-flattening is still needed: Pattern-045 (Green Tests, Red User) is an anti-flattening pattern. 23 tests passed for todo completion but the user couldn't complete a todo. The consciousness rubric ("does this feel like Piper?") catches what tests miss.

**Warning signs of flattening** (from the MUX docs):
- Language: Third-person instead of first-person, no uncertainty expressions, timestamps without context
- Structure: IDs instead of names, config strings instead of place names
- Process: Tests only check function not feeling, performance prioritized over personality

**Why it survives**: Anti-flattening is a quality discipline, not code. It operates through review, rubrics, and the Colleague Test — all methodology-layer tools.

### 4. The Lifecycle with Composting

Eight stages: Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted. The key insight: composted objects decompose into learnings that feed new emergent objects. Nothing truly disappears.

The "filing dreams" metaphor: composting surfaces as colleague reflection ("Having had some time to reflect, it occurs to me..."), not surveillance ("While you were away, I was watching...").

**Why it survives**: This is the experience model for artifact persistence — the "bathing experience" on top of the "indoor plumbing" of file storage. It answers "what happens to conversation outputs that need to outlive the conversation?" with a richer model than just "save to disk." The lifecycle is how Piper's understanding accumulates over time, which is the core product promise.

### 5. The Trust Gradient as Experience Design

Four-stage earned proactivity (New → Building → Established → Trusted). Trust is invisible to users but its effects are noticeable. Users don't see "Trust Level: Established" — they experience Piper getting more helpful over time.

**Why it survives**: Trust graduation is a UX principle, not a code system. The floor can implement it through context ("this user has had 50 successful interactions; be more proactive") without a dedicated TrustComputationService. The *design* is what matters — the implementation can be lighter than ADR-053 specified.

### 6. The Radar O'Reilly Pattern

Piper shows up where you are, doesn't ask you to visit. The mobile insight generalized: "the user is mobile, not the app." Piper's MVP doesn't need a dedicated mobile app — it needs to show up intelligently in existing surfaces (Slack, email, CLI, IDE).

**Why it survives**: This is a distribution and integration philosophy, not a feature. It aligns perfectly with the MCP/plugin model — Piper as a service that manifests through existing tools, not as a destination.

### 7. Recognition Over Articulation

"Piper articulates, user recognizes." Address the articulation barrier — users shouldn't need to know the right words. When someone says "what's on my plate?" Piper recognizes the intent (overwhelmed, need focus) rather than executing a literal query.

**Why it survives**: This is what the floor *already does well*. LLMs are naturally good at intent recognition from natural language. The design principle validates the floor-first approach — structured intent classification may actually be worse at recognition than letting the LLM understand naturally.

---

## What Was Scaffolding (Served Its Purpose, Not MVP)

### 1. Detailed Warmth Calibration Values

The warmth_levels dict with specific thresholds (0.2, 0.4, 0.6, 0.8) mapping to specific praise phrases ("Outstanding!", "Great!", "Good progress"). This is engineering a feeling instead of expressing one. The floor can calibrate tone with simpler guidance in the system prompt: "Match formality to the user's style. Be warmer when they seem stressed."

**What to keep**: The *idea* that Piper adjusts warmth based on context. **What to drop**: The specific numerical thresholds and phrase tables.

### 2. Consciousness Attribute Layering (Enums)

AwarenessLevel, EmotionalState, EntityRole as separate enums with specific values. This is a code framework for something that the floor handles through prompt engineering. A system prompt instruction like "you are currently in focused mode helping with sprint planning" achieves the same effect as setting `awareness_level=FOCUSED, emotional_state=CURIOUS, role=ANALYST`.

**What to keep**: The *concept* that Piper's mode shifts based on context. **What to drop**: The enum-based implementation.

### 3. Four-Wave Consciousness Rollout Plan

A detailed wave-by-wave plan for retrofitting consciousness across all features (Wave 1: Todos/Conversations/Loading/Errors, Wave 2: Standup/Intent/CLI, etc.). This assumed consciousness would be added feature-by-feature to existing structured handlers.

**Why it's scaffolding**: Floor-first routing means most responses are LLM-generated. Consciousness doesn't need to be retrofitted per-feature — it needs to be built into the floor's system prompt and context assembly once. The Morning Standup proved consciousness works when it's in the output layer. The floor IS the output layer now.

**What to keep**: The insight that consciousness degrades and needs active maintenance. **What to drop**: The per-feature rollout plan.

### 4. Specific Confidence Thresholds for Learning Types

Pattern confidence 0.6-0.9, Insight confidence 0.5-0.8, Correction confidence 0.8-1.0, etc., with trust-level gates for surfacing. Right concept (learnings have varying confidence, surfacing should be graduated), premature precision (we don't have real users yet to calibrate against).

**What to keep**: The learning type taxonomy and trust-graduated surfacing concept. **What to drop**: The specific numerical thresholds until we have real usage data.

### 5. PersonalityProfile as Dedicated Service

The personality_profile.py with adjust_for_context(), warmth calibration, confidence presentation style, action orientation, technical depth — as a separate service in the response pipeline. The floor's system prompt can incorporate these as instructions rather than as a code service that transforms output.

**What to keep**: User preferences that persist and influence responses. **What to drop**: The dedicated personality service as middleware. Preferences are better handled like Claude's memory model — user-correctable inferences stored as context, not as a parameterized transformation pipeline.

### 6. The 19-Category Intent Classification System

EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW, LEARNING, QUERY, CONVERSATION, IDENTITY, DISCOVERY, TEMPORAL, STATUS, PRIORITY, GUIDANCE, TRUST, MEMORY, PORTFOLIO, UNKNOWN. If most categories route to the floor anyway, the classifier may be solving the wrong problem at the wrong time.

**What to keep**: The action gate test — "does this require a side effect?" If yes, route to a handler. If no, floor. **What to drop**: The granular 19-category taxonomy as a routing mechanism. A simpler "action vs conversation" binary (with maybe 3-4 specific action types: GitHub, Calendar, Todo, Slack) may be sufficient.

---

## What This Means for MVP

### The Differentiator Stack

MVP = **Context Methodology + Conscious Floor + Artifact Persistence + Trust-Graduated Experience**

1. **Context Methodology** (the five-layer model, operationalized): What makes "just Claude with context" into a product. The methodology for assembling, maintaining, and transferring context is the core IP. Nobody else has operationalized this at this level.

2. **Conscious Floor** (grammar + five pillars + anti-flattening): The LLM floor speaks as Piper — with identity, temporal awareness, spatial awareness, agency, and prediction. Not through a personality service, but through carefully crafted system prompts and context assembly that embody the grammar.

3. **Artifact Persistence** (composting lifecycle): Conversation outputs that outlive the conversation. The lifecycle model (Emergent → ... → Composted → new Emergent) is the experience design. The implementation can start simple (#355-sized: save, browse, retrieve) but the design should know where it's going.

4. **Trust-Graduated Experience**: Piper earns the right to be proactive. Implementation can be lightweight (context-based rather than a dedicated computation service), but the design principle is non-negotiable.

### What MVP Doesn't Need

- A 19-category intent classifier (simpler action gate suffices)
- A dedicated personality service (floor prompt handles this)
- Bespoke tool integrations (MCP/plugins for plumbing)
- A four-wave consciousness rollout (consciousness lives in the floor prompt)
- Detailed warmth calibration code (prompt instruction suffices)
- Workflow orchestration engine (for the few action handlers that exist, direct dispatch is fine)

### The Indoor Plumbing vs. Bathing Experience Distinction

**Indoor plumbing** (commoditized, use existing solutions):
- GitHub, Slack, Calendar, Notion integrations → MCP plugins
- File storage → filesystem or simple database
- Reminders/todos → existing task management patterns
- Authentication → standard OAuth/session patterns

**Bathing experience** (Piper's differentiator):
- How context accumulates across sessions (five-layer model)
- How the assistant speaks (consciousness grammar + anti-flattening)
- How artifacts emerge, mature, and feed new understanding (composting lifecycle)
- How proactivity graduates based on trust (earned, not configured)
- How the assistant shows up where you already are (Radar O'Reilly)
- How the assistant recognizes intent from natural language (recognition over articulation)

---

## Relationship to Other Documents

- **Vision V2** (`docs/internal/planning/current/vision-v2-draft.md`): Needs revision to reflect this analysis. The "Three Horizons" model should emphasize methodology layer as Horizon 1 differentiator, not structured handlers.
- **Backlog Deep Review** (`dev/active/backlog-deep-review-2026-04-07.md`): This analysis provides the conceptual foundation for the MVP scope recommendations in that document.
- **Five-Layer Context Mapping** (`docs/internal/architecture/current/five-layer-context-mapping.md`): The context methodology pillar of MVP. This document describes the current state; the MUX analysis describes what it should feel like.
- **Roadmap Refresh Prep** (`dev/active/roadmap-refresh-prep-2026-04-02.md`): Needs significant revision once the MVP scope conversation concludes.

---

## The Sentence

If forced to say it in one sentence:

**Piper Morgan's MVP is a conscious conversational floor with good context methodology, artifact persistence, and trust-graduated experience — using commodity plumbing for tool integrations and focusing its differentiation on the methodology that makes an LLM feel like a colleague who remembers, learns, and grows.**

---

*Analysis document for project record. Captures the reasoning behind MVP scope decisions informed by the MUX deep dive and the April 7 product strategy conversation with PM.*
