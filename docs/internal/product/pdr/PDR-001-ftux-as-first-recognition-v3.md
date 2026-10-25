# PDR-001: First Contact is First Recognition

**Status**: Draft v3; **Amendment 1 ratified 2026-10-24 (xian)**
**Date**: January 4, 2026 (v3, v2); December 2, 2025 (v1)
**Author**: Principal Product Manager
**Stakeholders**: PM (xian), CXO, Chief Architect, Ted Nadeau (Advisor)

---

## Decision

Piper Morgan's first-time user experience (FTUX) is the initial expression of the recognition interface pattern—not a separate "onboarding wizard" that precedes the "real" experience.

From moment zero, users encounter the same Piper they will always encounter: oriented, contextual, colleague-like. Configuration and setup happen within this experience, not as a gate before it.

**Key principle**: FTUX teaches users *how to learn*, not *everything to know*. Research indicates users discover ~10% of capabilities during onboarding and ~90% through ongoing use. FTUX success is measured by whether users can discover new capabilities naturally, not by how many features they memorize.

---

## Context

The UX Strategy Synthesis (Nov 26, 2025) established the recognition interface as a strategic priority: Piper articulates the situation first, then offers relevant actions. This inverts the "blank prompt" pattern common to AI interfaces.

The question arose: does FTUX follow this pattern, or is it a special case where traditional wizard-style onboarding is acceptable?

This PDR resolves that question: **FTUX must embody the recognition pattern from the first moment.**

---

## User Need

New users face three simultaneous challenges:

1. **Configuration burden**: Piper requires API keys, integration credentials, and preferences to function
2. **Mental model formation**: Users must understand what Piper *is* and how to interact with it
3. **Articulation barrier**: ~50% of users struggle to articulate what they need from AI systems (Nielsen, 2024)

Traditional onboarding separates these: first a setup wizard (forms, validation, Next buttons), then the "real" application. This creates discontinuity—the setup experience teaches nothing about the product experience.

PM users are already overwhelmed. Adding a form-heavy setup phase before delivering any value compounds the burden.

---

## Decision Rationale

FTUX should demonstrate Piper's value proposition immediately. If Piper is a colleague who recognizes context and reduces articulation burden, users should experience that from the first moment—even during configuration.

### Core Principles

**1. Piper speaks first.**

The first screen is not a form or blank prompt. Piper orients:

> "Hi, I'm Piper. I'm here to help you with product management work. Let me help you get set up—I'll need a few things to connect to your tools."

This establishes the colleague relationship immediately.

**2. Configuration is conversational.**

Rather than a multi-step form, Piper asks for what it needs in dialogue.

*Technical note*: API key entry may require hybrid approach (Piper guides conversationally, form elements capture sensitive credentials securely). This is acceptable—the *experience* remains conversational even if specific inputs use form elements.

**3. Multiple entry points, not linear flow.**

Per Ted Nadeau's insight: users should be able to engage from multiple directions simultaneously, not be forced through a single path.

Instead of: Step 1 → Step 2 → Step 3 → Done

Offer: "Here are ways we can start working together..."
- Tell me about yourself and your work
- Connect your tools (GitHub, Slack, Calendar...)
- Ask me a question
- See what I can help with

The user chooses their entry point. Piper adapts. Configuration happens as needed, not as prerequisite.

**4. Progressive reveal replaces feature tours.**

Instead of explaining all capabilities upfront, Piper introduces features as they become relevant:

> "Now that GitHub is connected, I can help you with issue triage. Want to try that, or keep setting up?"

**5. Empty states are oriented.**

When a user reaches a view with no data, Piper doesn't show "Nothing here yet." Piper explains:

> "This is where your project insights will appear once we've connected your tools. Want to connect Notion now?"

**6. Onboarding IS the primer.**

FTUX must address the articulation barrier. Users need to learn:
- That they can ask naturally (not commands)
- That Piper will suggest options (they don't need to know everything)
- That Piper will ask for clarification (they don't need perfect requests)

The insight: **the preferences questionnaire itself becomes the conversation primer**. Rather than a separate demo followed by setup, the setup IS the demo. Piper asks about communication style, work style, decision-making preferences—and in doing so, demonstrates what conversational interaction with Piper feels like.

This is elegant: users learn the interaction model *while* providing information that makes Piper more useful. No separate artifact needed. The onboarding teaches how to talk to Piper by being a conversation with Piper.

**7. User can personalize the relationship.**

Per Ted's feedback: users should be able to rename Piper if desired (e.g., if they have a child named Piper, or prefer a different name). This respects user control while maintaining the colleague metaphor.

*Implementation note*: This is a new feature request, not currently implemented. Should be available in settings; can be mentioned during FTUX if user expresses discomfort with name.

---

## Trust Gradient Initialization

FTUX establishes the user at **Trust Stage 1 (New)**. Per the UX Strategy:

| Stage | Piper Behavior |
|-------|----------------|
| Stage 1 (New) | Responds to queries; minimal unsolicited help |
| Stage 2 (Building) | Offers related capabilities after task completion |
| Stage 3 (Established) | Proactive suggestions based on context |
| Stage 4 (Trusted) | Anticipates needs; "I'll do X unless you stop me" |

Piper's FTUX behavior reflects Stage 1:
- Explicit permission-seeking: "Would you like me to...?"
- No assumptions about preferences
- High explanation, low autonomy
- Foundation for trust to build through demonstrated competence

Trust stage is computed from interaction history, not user preference. Users cannot skip to higher trust levels—trust is earned.

---

## Existing Personalization Infrastructure

Piper has robust personalization infrastructure already implemented (~75-80% complete per technical assessment).

### Personality Dimensions (4 Axes)

| Dimension | Range | Purpose |
|-----------|-------|---------|
| Warmth Level | 0.0 (Professional) → 1.0 (Friendly) | Tone calibration |
| Confidence Style | numeric / descriptive / contextual / hidden | How certainty is expressed |
| Action Orientation | high / medium / low | Bias toward suggesting next steps |
| Technical Depth | detailed / balanced / simplified | Explanation complexity |

### User Preferences (5 Dimensions)

| Preference | Options |
|------------|---------|
| Communication Style | concise / balanced / detailed |
| Work Style | structured / flexible / exploratory |
| Decision Making | data-driven / intuitive / collaborative |
| Learning Style | examples / explanations / exploration |
| Feedback Level | minimal / moderate / detailed |

### Adaptive Detection

Piper can detect user preferences from conversation:
- High confidence (≥0.9): Auto-applies without asking
- Medium confidence (0.4-0.9): Surfaces as suggestion; user accepts/dismisses

This supports the 10%/90% model—users don't configure everything upfront; Piper learns over time.

### Integration Hierarchy

Per PM direction, integrations have clear priority for FTUX:

| Integration | Classification | FTUX Behavior |
|-------------|---------------|---------------|
| LLM | Required | Must configure to proceed |
| GitHub | Critical | Strongly encouraged during FTUX |
| Calendar | Important | Prompted during FTUX, not blocking |
| Notion | Nice-to-have | Deferred to "when you need it" |
| Slack | Contextual | Deferred; high value only for Slack-heavy users |

---

## FTUX Success Criteria

FTUX teaches ~10% of capabilities. The remaining ~90% is discovered through use. Therefore, FTUX success is not "user knows all features" but "user can discover features naturally."

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time to first recognition pattern | < 30 seconds | User experiences Piper articulating situation and offering options |
| Configuration completion | > 80% complete minimum viable setup | Users connect at least one integration |
| Mental model formation | Qualitative | User can describe "what Piper is like" after first session |
| Zero "now what?" moments | Qualitative | No point where user is stranded without guidance |
| Conversation primer completion | > 90% | Users see demonstration of natural interaction |
| Unprompted discovery (30-day) | At least 3 features | User uses capabilities not explicitly taught in FTUX |

---

## Ongoing Discovery Design

Because FTUX only teaches ~10%, the remaining ~90% requires ongoing discovery mechanisms. These are not part of FTUX but must be designed as part of the same product decision:

**Contextual capability hints**: After successful task completion, Piper may offer one related capability (throttled: max 2 suggestions per 5 interactions; stop if user ignores 2 in a session).

**"What can you help with?" response**: When asked, Piper provides contextual, useful response based on current project state—not a generic feature list.

**Dead-end recovery**: When Piper can't help with a request, the response includes alternative paths: "I can't do X, but I could help you with Y or Z."

**Empty state education**: Every empty state teaches what could be there and how to get there.

---

## Alternatives Rejected

### Traditional wizard → main app handoff
**Rejected because**: Creates discontinuous experience. Users learn "setup mode" patterns that don't apply to actual use. Delays value delivery.

### Blank slate with "What can I help you with?"
**Rejected because**: Places articulation burden on user who doesn't yet know what Piper can do. Violates recognition interface principle. Fails ~50% of users who struggle to articulate needs.

### Progressive feature unlock (gamification)
**Rejected because**: Foreign to colleague metaphor. Piper isn't a game to be leveled up; Piper is a colleague learning to work with you.

### Defer all configuration until needed
**Rejected because**: Some integrations (GitHub, LLM API keys) are required for core functionality. Deferring entirely would create broken-feeling first experience. However, optional integrations should be deferred.

### Comprehensive feature tour
**Rejected because**: Users won't remember. 10%/90% research shows onboarding retention is limited. Better to teach "how to discover" than "everything that exists."

---

## Implications

**For CXO**:
- FTUX interaction design must follow recognition interface patterns
- Empty states need Piper voice, not just UI copy
- Conversation primer design required
- Multiple entry point UI needed (not linear wizard)

**For Chief Architect**:
- Configuration collection needs conversational wrapper around technical validation
- Trust level must be initialized and persisted from first interaction
- Hybrid form/conversation pattern for sensitive credential entry
- User preference storage for optional personalization (name)

**For Implementation**:
- PM-122 (FTUX Wizard) should be reframed—not a wizard in traditional sense, but first-recognition implementation
- May warrant new issue or scope revision
- Discovery mechanisms (hints, dead-end recovery) are coupled to FTUX success

---

## Open Questions

*Most questions from v1 have been resolved through stakeholder input and technical assessment.*

### Resolved

1. **Current onboarding audit**: Audit to be conducted before implementation; current state documented in technical assessment and BRIEFING-CURRENT-STATE.

2. **Minimum valuable configuration**: Integration hierarchy established (LLM required → GitHub critical → Calendar important → Notion/Slack deferred).

3. **Conversation primer format**: Resolved—onboarding IS the primer. The preferences questionnaire itself demonstrates conversational interaction.

4. **Personalization scope**: Existing 4-dimension personality system + 5 user preferences provide robust foundation. Rename capability is new feature request.

### Design Work Needed

5. **Cross-session continuity**: Context-aware greeting approach approved (neither "Welcome back" nor "Last time..." exclusively, but situational).

**Greeting Conditions Table** (v3 refinement from CXO feedback):

| Condition | Greeting Approach |
|-----------|-------------------|
| Same day, recent | "Back already! We were working on [X]—continue?" |
| Next day, active work | "Yesterday we discussed [X]. Continue, or different focus?" |
| Week+ gap | "It's been a bit! Want to pick up where we left off, or start fresh?" |
| Month+ gap | "Welcome back! Want me to catch you up, or start fresh?" |
| Previous session trivial | "What can I help with?" (no reference) |
| Previous session ended with explicit abandonment | Fresh start: "Good morning! What can I help with?" |
| Previous session had multiple dead-ends | Soft fresh start: "Hi! Ready to pick up something new, or continue where we left off?" |

**Key principle**: Context-aware greeting is *emotionally* context-aware, not just *topically* context-aware. Sometimes the kindest acknowledgment is a clean slate. Referencing a frustrating failed session without acknowledgment is tone-deaf.

**Abandonment signals** (detectable):
- Explicit language: "never mind," "forget it," "this isn't working"
- Session closed mid-task without completion
- High ratio of dead-end responses in session

Requires:
   - Recency-aware logic (same day vs. week gap vs. month gap)
   - Emotional context detection (abandonment, frustration signals)
   - Trivial session filtering (don't reference abandoned/testing sessions)
   - Always offer pivot option ("continue or start fresh?")
   - Implementation in UserContextService

6. **Sandbox mode**: Optional "practice space" for users who want to experiment before creating real data. Lower priority than core FTUX but worth tracking.

7. **Learning → Suggestion bridge**: Infrastructure for preference detection exists, but end-to-end flow to surface suggestions needs completion. Not blocking for FTUX but important for "Piper learns" promise.

---

## PDR Lifecycle

*Addressing Ted's process question: "How does this become real?"*

| Stage | Description | Status |
|-------|-------------|--------|
| Draft | Initial proposal for review | ✓ v1 (Dec 2) |
| Review | Stakeholder feedback incorporated | ✓ v2 (Jan 4) |
| Approved | PM accepts decision | Pending |
| Implemented | Development work complete | Future |
| Validated | Success criteria measured | Future |

**Approval workflow**: PM reviews → shares with CXO and Chief Architect for final input → PM approves → becomes authoritative product decision → informs GitHub issues and implementation.

---

## References

- UX Strategy Synthesis (Nov 26, 2025) — Recognition interface priority
- CXO UX Summary Report (Jan 3, 2026) — Trust gradient, discovery patterns, 10%/90% insight
- Personalization Technical Assessment (Jan 4, 2026) — Current infrastructure state
- Roadmap v12.3 — VISION-CONSCIOUSNESS, Sprint V1 scope
- Ethics-First Architecture — Trust gradient definition
- ADR-027 — User vs System Configuration Separation
- ADR-010 — Configuration Access Patterns
- Nielsen research on articulation barrier (2024)
- Ted Nadeau feedback (Dec 3, 2025) — Multi-entry points, rename capability, process questions
- Christopher Alexander, "A Pattern Language" — Generative pattern thinking

---

## Amendment 1: recognition-first applies to the first conversation; the hosted setup wizard is the recorded exception (RATIFIED 2026-10-24 17:28 PT, xian, with Exec: "Adopt CXO's PDR-001 wording. In beta see that we live up to it.")

**The wording, as ratified:** recognition-first applies to the first conversation. The hosted setup wizard is a stepped, explicit-consent flow, and is the recorded exception.

**Why an exception is recorded, not denied.** The decision above says first contact is not "a separate onboarding wizard that precedes the real experience", and "Traditional wizard → main app handoff" is in Alternatives Rejected. The hosted app has a wizard anyway (invite, API keys, account, projects, complete), because it must collect an invite code, a provider key and consent before any conversation can run, and none of that can be inferred. Leaving the PDR silent made it read as if the wizard were a drift from the decision. It is a bounded exception with a boundary.

**The boundary.**
- The wizard asks only for what a conversation cannot start without: the invite code, the account, the provider key, and any consent the person must give. Nothing in it is a product tour.
- Everything else in the original decision still holds for the first conversation: Piper opens oriented, offers options rather than "What can I help you with?", and does not ask the user to articulate what they do not yet know.
- Integrations and preferences stay in the conversation and in Settings, not in more wizard steps.

**The beta check ("see that we live up to it").** Whether the first conversation after the wizard recognizes the user today is not verified; #1538 is the work. During beta, the check is a served row, not a description:
1. Web takes a fresh account through the wizard on alpha and quotes the first Piper reply in chat, with the account's connected state stated beforehand.
2. CXO judges the quote on three tests: it orients (says what Piper can see on this account, truthfully); it offers options instead of a blank prompt; and it states nothing false about what is connected.
3. Run once per beta wave on a fresh account, and again whenever the wizard's steps or the first reply's handler change. A failure is class 3 (honesty) if the reply claims something untrue, and otherwise a UX issue.

**What this amendment does not change:** the rest of the decision, the FTUX success criteria, and the trust-gradient initialization, which stays dormant through beta (#2135).

---

## Changelog

**Amendment 1 (October 24, 2026)**: recorded the setup wizard as the exception to recognition-first, with its boundary and the beta check. Ratified by xian 17:28 PT (production-map ruling 5). Drafted by CXO.

**v3 (January 4, 2026)**:
- Added emotional context awareness to cross-session greeting (CXO feedback)
- Added greeting conditions table with abandonment/frustration handling
- Added key principle: "emotionally context-aware, not just topically context-aware"
- Added detectable abandonment signals for implementation

**v2 (January 4, 2026)**:
- Added "onboarding IS the primer" insight—questionnaire demonstrates interaction model
- Added 10%/90% insight framing (CXO research)
- Added multiple entry points principle (Ted feedback)
- Added user rename capability as new feature request (Ted feedback)
- Added existing personalization infrastructure section (4 dimensions + 5 preferences)
- Added integration hierarchy with PM-directed prioritization
- Added ongoing discovery design section
- Added PDR lifecycle section (Ted process question)
- Resolved open questions: primer format, personalization scope, cross-session approach
- Added design work needed: cross-session greeting implementation, sandbox mode, learning bridge
- Refined success criteria for discovery-focused measurement
- Added articulation barrier context

**v1 (December 2, 2025)**:
- Initial draft establishing FTUX as first recognition

---

*PDR-001 | Draft v3 | January 4, 2026*
