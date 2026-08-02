# PDR-004: Piper's Experience Philosophy

**Status**: APPROVED
**Author**: PPM
**Date**: 2026-03-22
**Supersedes**: None (new PDR)
**Related**: PDR-001 (FTUX as First Recognition), ADR-060 (Floor-First Routing), ADR-059 (Workflow Dispatcher)

---

## Context

Between March 13 and March 16, 2026, four product principles emerged from three separate decision processes: the workflow hijack UX sprint (Mar 13), the "Are we doing it backwards?" roundtable (Mar 14), and the floor inversion architecture synthesis (Mar 16). A fifth principle was identified through the CIO's AX testing assessment on March 13.

Each principle was developed, reviewed, and ratified independently. Together they define how Piper behaves in every interaction — not just the first one (which PDR-001 governs) but every subsequent one. They operate at the experience layer: they determine what it feels like to talk to Piper, regardless of what the user is asking about.

These principles were initially tracked as potential addenda to PDR-001, but they operate at a higher level than first-time user experience. PDR-001 remains correct and unchanged — it governs FTUX specifically. PDR-004 governs the ongoing experience.

---

## Decision

Piper's experience is governed by four principles. These are non-negotiable design constraints that apply to every interaction path — structured handlers, conversational floor, guided workflows, error states, and any future interaction mode.

---

### Principle 1: The Session Belongs to the User

**Origin**: Workflow hijack UX sprint, March 13, 2026
**Decision docs**: `memo-ppm-workflow-hijack-direction-2026-03-13.md`, CXO guidance memo (same date)

The user's conversation session is theirs. Workflows, handlers, and processes are guests in the user's session — they have the user's attention only while the user is actively participating. The moment a user redirects, the active process must yield.

**Implications:**
- No workflow may capture a session and refuse to release it
- Explicit escape commands ("cancel," "exit," "stop") must always work, processed by the routing layer before any workflow handler sees the message
- Off-topic detection should recognize when a user has moved on and offer to pause or exit the active workflow
- Timeout mechanisms auto-suspend workflows after inactivity rather than holding the session indefinitely

**What this means in practice:** If a user is in the middle of a standup and asks "What's on my calendar?" — Piper answers the calendar question and offers to resume the standup. It does not force the calendar question through the standup handler. The user's intent takes precedence over the system's process.

---

### Principle 2: Offer-First Activation

**Origin**: Workflow hijack UX sprint, March 13, 2026
**Decision docs**: `memo-ppm-workflow-hijack-direction-2026-03-13.md`, CXO guidance memo (same date)

Guided workflows activate only when the user chooses to enter them. Piper offers; the user decides. Auto-activation is not permitted as a default pattern for any guided workflow.

**Implications:**
- Onboarding is an offer, not a capture: "I can walk you through setting up your workspace — want to do that now, or would you rather just dive in?"
- If the user declines, the workflow never activates and Piper handles whatever the user actually wanted to talk about
- Contextual suggestions for unconfigured integrations are throttled: maximum 1 per session, stop entirely after 3 declined across sessions
- Future guided workflows must follow the offer-first pattern unless there is a specific, documented exception approved by PM

**What this means in practice:** A new user's first interaction with Piper is a welcome that offers help, not a wizard that demands answers. Piper works (with reduced capability) even if the user never configures anything. The user discovers Piper's depth by experiencing it, not by being forced through a setup flow.

**Relationship to PDR-001:** PDR-001 established that FTUX is "first recognition" — Piper demonstrates what it is by being it. Offer-first activation is the mechanism that makes this possible. A captured onboarding flow is the wizard pattern wearing a conversational mask; offer-first is recognition in action.

---

### Principle 3: Piper Coordinates Understanding

**Origin**: CIO AX Testing assessment, March 13, 2026
**Decision docs**: `memo-cio-eta-recommendations-response-2026-03-13.md`

Piper's coordination role extends beyond task routing to context management. Piper's job is not just "I'll route your question to the right handler." It's "I'll make sure every participant in the system — human or agent — knows what it knows, knows what it doesn't know, and knows what changed."

**Implications:**
- When a user returns after an absence, Piper's job is to orient them: what happened, what changed, what needs attention
- When an agent enters a new session, Piper's job is to brief them: what's current, what's pending, what to watch for
- Context quality is first-class infrastructure, not a nice-to-have. The Context Assembler (ADR-060) is the architectural expression of this principle
- The gap between what a participant *thinks* it knows and what is *actually true* is the most dangerous failure mode in multi-agent coordination. Piper's job is to close that gap proactively

**What this means in practice:** Piper is not a tool you query. It's a colleague who maintains situational awareness across the team and ensures nobody is operating on stale or false assumptions. This applies to Piper's own agent team (development workflow), to Piper's LLM calls (floor context assembly), to Piper's users' agent workflows (the product vision), and to Piper helping users think through context management as a PM problem.

---

### Principle 4: The LLM Floor Guarantee

**Origin**: "Are we doing it backwards?" roundtable, March 14, 2026
**Decision docs**: `memo-ppm-roundtable-synthesis-2026-03-14.md` (ratified), ADR-060 (formalized)

**Piper is always at least as good as a well-prompted LLM with the user's context. Structured handlers make it better, not different.**

The LLM conversational floor is Piper's baseline experience. Every interaction must be at least as useful as what a context-aware LLM would produce unassisted. Structured handlers (canonical routing, workflow automation, integration actions) are the ceiling — they make specific interactions *better* than the floor. But no interaction should ever fall *below* the floor.

**Implications:**
- No query may produce "I don't have that capability yet" or any equivalent deflection. Piper always engages conversationally.
- The intent classifier is a router, not a gate. Match → structured handler (better experience). No match → LLM with context (baseline experience). The user never hits a wall.
- The floor operates within the same ethics and trust pipeline as structured handlers. It is not a bypass.
- The floor reasons conversationally — it does not take actions or call integrations. Structured handlers handle side effects. The floor handles thinking.

**Voice guidance for floor responses:**
- Engage directly with what the user asked
- Use available project context to make responses specific
- Offer concrete actions Piper can actually perform
- Never apologize for not having a feature. Never say "I can't help with that." Just help.
- If an action requires a capability Piper doesn't have, suggest an alternative naturally — without highlighting the limitation

**What this means in practice:** A user who asks "Can you help me manage the agents working on a coding assignment?" gets a thoughtful conversation about agent coordination, task decomposition, and interface contracts — with an offer to create issues for tracking. They do not get "I don't have that capability yet, but I'm learning!"

**The ethical boundary distinction:** "Never say I can't" applies to Piper's conversational capability. It does not override ethical boundaries. When a request crosses an ethical line, Piper declines with professional judgment and tact — like a colleague exercising discretion, not a system returning an error. The three response modes are: capability (floor default — always engage), ethical boundary (professional decline with explanation), and action limitation (suggest alternatives naturally).

---

## Relationship Between Principles

These four principles are not independent — they form a coherent experience philosophy:

**Principles 1 and 2** govern the relationship between Piper and the user's agency. The user controls the session (1) and chooses what to engage with (2). Piper serves the user's intent, not its own processes.

**Principle 3** governs what Piper's role is — not just a task router but a context coordinator. This is the "what" of Piper's value proposition.

**Principle 4** governs the minimum bar for how Piper delivers on that role. Whatever Piper does, it does at least as well as a well-prompted LLM with context. This is the "how" — the floor beneath everything.

Together: Piper is a colleague who respects your autonomy (1, 2), maintains shared understanding across the team (3), and always engages thoughtfully with whatever you bring to it (4).

---

## What This PDR Does Not Cover

- **FTUX specifics**: PDR-001 governs first-time user experience. PDR-004 governs every interaction.
- **Entity model**: PDR-003 governs entity concepts. PDR-004 is about experience, not data modeling.
- **Architectural implementation**: ADR-060 (floor-first routing) and ADR-059 (workflow dispatcher) are the architectural expressions of these principles. PDR-004 governs the *why*; the ADRs govern the *how*.
- **Specific voice/personality design**: The CXO's voice guidance (formality calibration, Colleague Test rubric, PA voice card) operates downstream of these principles. PDR-004 establishes the constraints; voice design works within them.

---

## ⚠️ Amendment A (PROPOSED, 2026-07-30, CXO) — the experience gate binds

**Status: PROPOSED. Not ratified. PPM and PM hold the ratification call.**

### What this amends

PDR-004 places voice design *"downstream of these principles"* and explicitly out of its own scope
(see "What This PDR Does Not Cover", above). That was correct — but it left a gap that only became
visible when the machinery downstream grew teeth:

**DoD Layer B** (`docs/internal/development/experience-verification-dod-layer-b.md`) states that
*"a user-facing surface is not Done until its delivered experience passes the Colleague Test (or the
surface's branched verification rubric) and conforms to the experience intent specified in its MUX
doc."* That gate is **treated as binding** and is used to block Done.

**Nothing ratified says it binds.** Someone disputing a Layer-B failure has nothing in the decision
corpus to appeal to. The instruments are documented and versioned; the *authority* is not recorded.

### The decision

> **A user-facing surface is not Done until its delivered experience passes the Colleague Test, or
> the branched verification rubric appropriate to that surface, and conforms to the experience intent
> its MUX doc specifies.**
>
> **The rubrics are CXO-owned, versioned instruments.** This decision binds **the gate**, not any
> particular version of any instrument. Rubrics may be revised, re-tuned, and branched without
> re-ratification; what is ratified is that a rubric failure can block Done.

### Why the instrument stays out of the corpus

Diagnosed by PPM (2026-07-30), and it corrects the question CXO originally asked — which was whether
to promote the *rubric* to ratified status:

**Under m-38 the corpus records decisions, not instruments.** A rubric is a measuring device; it gets
versioned, amended, and re-tuned, which is exactly what it must stay free to do. Putting a live
instrument in the ratified corpus is a category error with a practical cost: **every rubric revision
would drag a re-ratification behind it, and revision would stop.** The Colleague Test rubric is at
v2.3.2 with a further branch opening for the PDR-006 plugin surface — precisely the case that would
have raised the tier question a second time.

**So: ratify the decision; leave the instrument where it lives.**

### Scope — what this covers, deliberately including surfaces we don't render

Per PM's 2026-07-30 ruling that experience decisions are PM + CXO **"across all the surfaces"**, the
gate applies to every user-facing surface, including ones where Piper does not control the final
rendering:

| Surface | Instrument |
|---|---|
| Chat / floor responses, declines, error paths | Colleague Test rubric (R/C/T) |
| UI-rendering surfaces (lifecycle, staleness, status) | UI Lifecycle Verification Rubric |
| **Hosted-MCP / plugin tool responses (PDR-006)** | **Branch open, not yet specified — see below** |
| New surface type with no fitting rubric | Branch a new instrument per Branch-or-Anchor; **naming the absence is itself a Layer-B finding** |

⚠️ **Open, and named rather than assumed**: under PDR-006 the client LLM composes what the user
actually reads from our tool output, so R/C/T no longer scores what the user sees. A rubric branch is
**opened** (CXO, 2026-07-30) and its dimensions are not yet settled. The load-bearing unknown is
**honesty-under-recomposition** — our honest-decline discipline is a property of text we control, and
whether a hedge survives another model paraphrasing it has never been tested. A Phase-0 probe (PA)
runs before the branch is specified, because a negative result moves the fix out of the rubric
entirely and into the tool output format.

### Provenance

Raised by CXO as *"does the Colleague Test warrant PDR status?"*; reframed by PPM — **the unratified
thing is the decision, not the instrument** — which is the form recorded here. Originating context:
the Jake Krajewski alpha FTUX review, where the Colleague Test was applied to a new surface (the FTUX)
and the question of its standing surfaced.

---

## Review History

| Date | Event |
|------|-------|
| 2026-03-13 | Principles 1, 2, 3 emerged from hijack UX sprint and CIO AX assessment |
| 2026-03-14 | Principle 4 emerged from roundtable (4/4 unanimous) |
| 2026-03-14 | PPM synthesis ratified by PM with revisions from CIO, Architect, CXO |
| 2026-03-16 | All four principles referenced in floor inversion synthesis as binding direction |
| 2026-03-19 | ADR-060 formalized floor-first routing as architectural expression of Principle 4 |
| 2026-03-22 | PDR-004 created, consolidating all four principles into single product decision record |
| 2026-07-30 | **Amendment A PROPOSED (CXO)** — ratifies that the experience gate (DoD Layer B) binds, while keeping the rubrics as unratified CXO-owned instruments. Awaiting PPM + PM. |

---

*PDR-004 | Created March 22, 2026*
*Author: PPM | Approved: PM (xian)*
