# PDR-002: Conversational Glue

**Status**: Draft v2
**Date**: January 4, 2026
**Author**: Principal Product Manager
**Stakeholders**: PM (xian), CXO, Chief Architect

---

## Decision

Conversational continuity is a **first-class product feature**, not an infrastructure detail. The connective tissue between Piper's capabilities—how conversations flow, how context persists, how discovery happens—is as important as the capabilities themselves.

Piper's value proposition depends on this glue working seamlessly. A feature that exists but cannot be discovered, or that breaks conversational flow to be invoked, fails the colleague test.

---

## Context

The CXO UX Strategy work (Nov 2025 - Jan 2026) revealed a critical insight: Piper's features are largely built, but users struggle to discover and use them naturally. The gap isn't capability—it's continuity.

This manifests as:
- Users don't know what Piper can do until they ask the right question
- Transitions between tasks feel abrupt rather than conversational
- Context from previous interactions doesn't inform current ones
- Proactive suggestions feel random rather than situationally appropriate

Traditional product thinking treats these as UX polish—nice to have after core features work. This PDR establishes the opposite: **conversational glue is core functionality**.

---

## The Problem

### Capability Without Discovery is Invisible Capability

Piper can perform standup synthesis, issue triage, calendar analysis, document intelligence, and more. But if a user doesn't know to ask, these capabilities might as well not exist.

The blank prompt pattern ("What can I help you with?") places full articulation burden on users. Research shows ~50% of users struggle to articulate what they need from AI systems (Nielsen, 2024). These users will never discover Piper's value—not because Piper can't help, but because they can't ask.

### Context Loss Breaks the Colleague Metaphor

A colleague remembers what you discussed yesterday. A colleague notices patterns in your work. A colleague offers relevant help without being asked.

If Piper forgets context between sessions, treats each conversation as isolated, and only helps when explicitly requested—Piper isn't a colleague. Piper is a tool with a chat interface.

### Proactive Help Without Trust is Annoyance

Unsolicited suggestions can be helpful or annoying depending on:
- Whether the suggestion is relevant
- Whether the timing is appropriate
- Whether the user trusts the suggester's judgment

Piper must earn the right to be proactive. This requires a trust model that governs when and how suggestions surface.

---

## Decision Rationale

### Conversational Glue Has Three Components

**1. Discovery Glue**: How users learn what Piper can do
**2. Context Glue**: How information persists and connects across interactions
**3. Proactivity Glue**: How Piper offers help without being asked

Each component requires explicit product design, not just technical implementation.

---

## Component 1: Discovery Glue

### The Recognition Interface Pattern

Piper articulates the situation first, then offers relevant actions. This inverts the typical AI pattern where users must know what to ask.

**Instead of**: Blank prompt waiting for user input

**Do this**: Piper observes context and offers:
> "You have 3 GitHub issues that changed overnight and a standup in 2 hours. Want me to summarize the issues, or help you prep for standup?"

### Contextual Capability Hints

After successful task completion, Piper may surface one related capability the user hasn't used.

**Throttling rules** (prevent annoyance):
- Maximum 2 suggestions per 5 successful interactions
- Stop suggesting if user ignores 2 suggestions in a session
- Never interrupt flow—only suggest at natural pause points
- Respect "don't show me this again" for specific capabilities

**Example**:
> User completes issue triage
> Piper: "Nice work. By the way, I can also generate release notes from closed issues if that's ever useful."

### "What Can You Help With?" Response Quality

When users explicitly ask what Piper can do, the response must be:
- **Contextual**: Based on connected integrations and current project state
- **Prioritized**: Most relevant capabilities first, not alphabetical feature list
- **Actionable**: Each capability includes "want to try it?" option

**Anti-pattern**: Generic feature list that reads like marketing copy

### Dead-End Recovery

When Piper can't help with a request, the response includes alternative paths:

**Instead of**: "I can't do that."

**Do this**: "I can't access your email directly, but I could help you draft a response if you paste the thread, or summarize your calendar to help you find time to respond."

---

## Component 2: Context Glue

### Session Context Persistence

Within a session, Piper maintains full context:
- What the user asked
- What Piper provided
- What decisions were made
- What tasks remain

This is table stakes—most chat interfaces do this.

### Cross-Session Memory

Between sessions, Piper maintains relevant context:
- User preferences (communication style, technical depth, etc.)
- Project state (active integrations, recent activity)
- Conversation history (what was discussed, what was decided)
- Trust level (earned through interaction history)

**Cross-session greeting** follows context-aware pattern (per PDR-001):

| Condition | Greeting Approach |
|-----------|-------------------|
| Same day, recent session | Reference specific work: "Back already! We were working on [X]—continue?" |
| Next day, active project | Light reference: "Yesterday we discussed [X]. Continue, or different focus?" |
| Week+ gap | Offer choice: "It's been a bit! Want to pick up where we left off, or start fresh?" |
| Month+ gap | Gentle reorientation: "Welcome back! Want me to catch you up, or start fresh?" |
| Previous session trivial | No reference: "What can I help with?" |

**Key principle**: Always offer the pivot. Never trap users in previous context.

### Entity Continuity

When users reference entities (projects, issues, people, documents), Piper resolves references across the conversation:

- "The issue we discussed" → resolves to specific GitHub issue
- "My standup" → resolves to user's recurring standup
- "That document" → resolves to most recently referenced document

This requires anaphoric reference resolution—understanding what "it," "that," and "the thing" refer to.

---

## Component 3: Proactivity Glue

### The Trust Gradient Model

Piper's proactivity is governed by earned trust, not user preference. Users cannot simply enable "maximum proactivity"—trust must be demonstrated through competent behavior over time.

| Trust Stage | Piper Behavior | How Earned |
|-------------|----------------|------------|
| Stage 1 (New) | Responds to queries; no unsolicited help | Default for new users |
| Stage 2 (Building) | Offers related capabilities after task completion | ~10 successful interactions |
| Stage 3 (Established) | Proactive suggestions based on observed context | ~50 interactions + pattern recognition |
| Stage 4 (Trusted) | Anticipates needs; "I'll do X unless you stop me" | Extended history + explicit user comfort |

**Trust can decrease**: If Piper makes poor suggestions, misunderstands context repeatedly, or causes user to lose trust, proactivity level regresses.

> 🔴 **OPEN QUESTION (PPM, 2026-08-01) — the gradient's denominator may not exist on the plugin surface.**
> **This trust gradient is denominated in interactions** (~10 → Stage 2, ~50 → Stage 3), which assumes
> **Piper owns the surface and can count them.** **PDR-006** (hosted MCP + plugin distribution,
> ratified 2026-07-31) means we do not: the user is inside Claude or ChatGPT, and the host LLM decides
> when to call us and mediates everything the user sees. **What counts as "an interaction" when the
> client LLM may invoke three tools in one user turn, or none?**
> **Not a blocker for first contact** — a cold account is Stage 1 either way, and Stage 1 is where it
> starts regardless of how interactions are counted. **It bites at stage TRANSITIONS**, which are
> currently unimplementable-as-specified on the plugin path.
> Surfaced while adjudicating whether the first-contact design spec conflicts with Stage 1; recorded
> here rather than left in mail. **Needs a product decision before any stage-transition logic is
> built for the plugin surface** — not before beta.

> ✅ **RESOLVED (PPM read, 2026-08-01) — first contact after connector authorization is Stage-1 legal.**
> Two components, two grounds, and they are different:
> - **The reading** (returning a specific view of the user's own work) is **not "unsolicited help"** —
>   it is the *result of the authorization*, bounded to exactly what was authorized. **The
>   authorization is the solicitation.**
> - **The attached offer** ("want me to draft those?") clears Stage 2's *"offers **related**
>   capabilities"* threshold not by meeting it but by **not being that behavior**: Stage 2 governs
>   *adjacent* capability discovery (this doc's own example: *"by the way, I can also generate release
>   notes"*) — a cross-sell into an unused capability. A first-contact offer to act on **the thing just
>   read, inside the scope just authorized** is continuation, not cross-sell.
>
> **Scope note on throttling**: the max-2-per-5 rule sits under *Contextual Capability Hints* and is
> scoped to *"after successful task completion… a related capability the user hasn't used."* First
> contact is neither, so **it does not spend a suggestion** unless we decide it should.

### Trust Computation Framework

*Added v2 from CXO feedback—this needs architectural implementation (flag for ADR).*

**Interaction Outcomes**:

| Outcome | Trust Effect | Signal |
|---------|--------------|--------|
| **Successful** | +1 toward next stage | User acted on response (clicked, executed, continued meaningfully) |
| **Neutral** | No change | User acknowledged but didn't act, or conversation ended naturally |
| **Negative** | -1 (with floor) | User explicitly rejected, expressed frustration, abandoned mid-task |

**Stage Thresholds** (calibration needed—starting point):
- Stage 1 → 2: ~10 successful interactions
- Stage 2 → 3: ~50 successful + evidence of pattern recognition value
- Stage 3 → 4: Extended history + explicit user comfort signal

**Regression Rules**:
- 3 consecutive negative interactions: drop one stage
- 90-day inactivity: drop one stage (Stage 4→3 or 3→2 only; never below Stage 2 once earned)
- Explicit user complaint about proactivity: immediate drop to Stage 2

**Visibility Decision**: Trust level is invisible—no "Your trust level: Established" display. But effects should be noticeable enough that users feel progression. If user asks "Why did you just do that without asking?", Piper can explain: "Based on our history, I thought this was something you'd want me to handle. Should I check first next time?"

This makes trust *discussable* without being *displayed*. Colleagues don't announce trust scores, but they do explain their assumptions when questioned.

**Architectural implication**: Trust needs to be computed, stored, and queryable—but not surfaced in UI. Flag for Chief Architect ADR.

### Proactivity Triggers

At Trust Stage 3+, Piper may initiate based on:

| Trigger | Example Proactive Behavior |
|---------|---------------------------|
| Calendar event approaching | "Your standup is in 30 minutes. Want me to prep your notes?" |
| GitHub activity spike | "12 new comments on issues you own overnight. Summary?" |
| Document staleness | "Your roadmap doc hasn't been updated in 2 weeks. Review time?" |
| Pattern recognition | "You usually check PRs on Monday mornings. 3 await your review." |

### Proactivity Guardrails

**Never proactive about**:
- Sensitive personal information
- Actions that can't be undone
- Anything the user has dismissed twice

**Always ask before**:
- Taking action on behalf of user (until Trust Stage 4)
- Sharing information with others
- Modifying external systems

---

## Success Criteria

### Discovery Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Unprompted capability discovery (30-day) | ≥3 features per user | Users finding capabilities without explicit instruction |
| "What can you help with?" satisfaction | >4/5 rating | Response quality when explicitly asked |
| Dead-end recovery success | >60% continue conversation | Users don't abandon after hitting limits |
| Feature tour skip rate | N/A | No feature tour exists; discovery is conversational |

### Context Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Cross-session reference accuracy | >90% | When user references "what we discussed," Piper resolves correctly |
| Anaphoric resolution success | >85% | "It," "that," "the thing" resolved correctly |
| Context-aware greeting relevance | >80% user acceptance | Users don't immediately redirect after greeting |

### Proactivity Glue Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Proactive suggestion acceptance | >30% at Stage 2, >50% at Stage 3 | Suggestions are relevant enough to act on |
| Proactive suggestion annoyance | <10% "don't show again" | Not annoying users |
| Trust progression | 50% reach Stage 2 within 30 days | Users earning trust through natural use |

---

## The B2 Quality Gate

From the CXO UX synthesis: **"B2" represents the threshold where conversational glue works well enough that users experience Piper as a colleague, not a chatbot.**

B2 is not a feature checklist. B2 is a qualitative assessment:
- Does conversation feel natural or stilted?
- Does Piper remember what matters?
- Are proactive suggestions helpful or annoying?
- Can users discover capabilities without reading documentation?

**B2 is a release criterion**: Features that work technically but fail the B2 conversational test are not ready for users.

---

## Alternatives Rejected

### Explicit Feature Discovery (Tours, Tips, Badges)
**Rejected because**: Foreign to colleague metaphor. Colleagues don't give you achievement badges for discovering they can help with spreadsheets.

### User-Controlled Proactivity Settings
**Rejected because**: Users don't know what proactivity level is appropriate until they experience it. Trust-based progression is more natural than preference toggles.

### Session Isolation (Fresh Start Each Time)
**Rejected because**: Destroys the colleague relationship. Valuable for privacy-conscious users as an option, but not the default.

### Maximum Context Retention (Remember Everything)
**Rejected because**: Creepy. Users should feel Piper remembers what's relevant, not that Piper is surveillance. Selective memory is more human.

---

## Implications

**For CXO**:
- Design recognition interface patterns for each major capability
- Specify contextual capability hint UX (when, where, how to dismiss)
- Design cross-session greeting variations
- Define "B2 quality" assessment criteria

**For Chief Architect**:
- Cross-session memory architecture (what persists, how long, how retrieved)
- Trust level computation and persistence
- Anaphoric reference resolution system
- Proactivity trigger infrastructure

**For Implementation**:
- Discovery glue is not separate from features—each feature needs discovery design
- Context glue requires UserContextService enhancements
- Proactivity glue requires trust computation (may be new system)

---

## Relationship to Other PDRs

**PDR-001 (First Contact is First Recognition)**: FTUX is the first expression of conversational glue. The principles established there (Piper speaks first, multiple entry points, onboarding as primer) are specific applications of the glue patterns defined here.

**PDR-003 (Multi-Entity Chat)** [Pending]: Multi-entity conversations will require extended glue—how context persists when multiple participants are involved, how proactivity works in group settings.

---

## Open Questions

1. **Memory boundaries**: How much cross-session context is helpful vs. creepy? What's the retention policy? CXO "thoughtful colleague" test: remember work context and stated preferences; don't remember casual asides or inferred personal details.

2. ~~**Trust computation specifics**~~: **Resolved v2** — Framework established above (interaction outcomes, stage thresholds, regression rules). Needs architectural ADR for implementation.

3. **Privacy mode**: Should there be an explicit "don't remember this session" option? How does it interact with trust levels?

4. **Multi-device continuity**: If a user switches from desktop to mobile mid-task, how does context transfer?

---

## References

- CXO UX Strategy Synthesis (Nov 26, 2025) — Recognition interface, trust gradient origins
- CXO UX Summary Report (Jan 3, 2026) — B2 quality gate, discovery patterns, proactivity rules
- PDR-001: First Contact is First Recognition — FTUX as glue expression
- Nielsen research on articulation barrier (2024)
- Ethics-First Architecture — Trust gradient foundations
- Personalization Technical Assessment (Jan 4, 2026) — Adaptive detection infrastructure

---

## Changelog

**v2 (January 4, 2026)**:
- Added Trust Computation Framework (CXO feedback)
- Added interaction outcomes table (+1 successful, 0 neutral, -1 negative)
- Added stage thresholds and regression rules
- Established visibility decision: invisible computation, visible effects, discussable on request
- Modified inactivity regression: 90 days (gentler than 30), never below Stage 2 once earned
- Added memory boundaries guidance ("thoughtful colleague" test)
- Flagged trust computation for Chief Architect ADR

**v1 (January 4, 2026)**:
- Initial draft establishing conversational glue as first-class product concern
- Defined three glue components: Discovery, Context, Proactivity
- Established trust gradient as proactivity governor
- Defined B2 quality gate
- Connected to PDR-001 and upcoming PDR-003

---

*PDR-002 | Draft v2 | January 4, 2026*
