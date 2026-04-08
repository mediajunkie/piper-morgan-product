# Piper Morgan Vision v2.2 — DRAFT

**Status**: Draft for leadership review (PPM, CXO, Architect)
**Author**: Piper Alpha, incorporating 10 months of project learning
**Date**: April 8, 2026
**Supersedes**: vision.md (June 21, 2025) — preserved as founding vision
**Informed by**: MUX analysis, backlog deep review, MCPB feasibility research, product strategy conversations (Apr 7-8)

---

## What Changed Since the Founding Vision

The June 2025 vision described three phases: intern → associate → advisor. That trajectory still holds directionally, but ten months of building taught us things the founding vision couldn't know:

1. **The LLM is the floor, not the ceiling.** Piper should always be at least as good as a well-prompted LLM with the user's context. Structured handlers make it *better*, not *different*. (ADR-060, March 2026)

2. **Entities experience Moments in Places.** The object model isn't a data schema — it's a constitutional grammar that resolves design disputes and catches category errors before they become technical debt. (ADR-045, November 2025)

3. **Consciousness is architecture, not decoration.** The Five Pillars (Identity, Time, Space, Agency, Prediction) aren't features to build — they're qualities every response must exhibit. Anti-flattening is an ongoing discipline, not a one-time retrofit. (MUX analysis, November 2025 – April 2026)

4. **Methodology beats code frameworks.** The project consistently evolved from "build code to enforce X" to "build methodology that achieves X." Verification, multi-agent coordination, and capability extension all work better as process infrastructure (CLAUDE.md, mailboxes, session logs) than as Python classes. (Backlog analysis, April 2026)

5. **Tool integrations are commoditized.** GitHub, Slack, Calendar, Notion — these are indoor plumbing. Available as MCP plugins and standard integrations. Piper's value isn't in connecting to these tools; it's in the *experience* of using them through a colleague who understands context. (MCP ecosystem, March 2026)

6. **The PA experiment proved the floor is high.** Piper Alpha — a well-briefed Claude agent — handles standup synthesis, issue triage, backlog analysis, strategic document drafting, and cross-project awareness conversationally, with no structured handlers. The floor is higher than we assumed. (PA Phase 1, March–April 2026)

---

## The Problem (Unchanged, Better Understood)

Product managers spend 40-60% of their time on routine knowledge management. The founding vision named this correctly. What we understand better now:

- The problem isn't just time spent on mechanics — it's **context fragmentation**. PMs carry the "why" in their heads because no tool captures it structurally.
- Execution tools (Jira, Linear, Asana) are excellent repositories for the *output* of PM thinking but don't support the *process* of PM thinking. Piper sits upstream.
- The discovery problem is real: features that work technically but can't be found by users deliver zero value. (Pattern-045: Green Tests, Red User)
- **No existing product combines context methodology with conscious experience design.** Tools have pieces (integrations, AI features, chat interfaces). Nobody has operationalized the methodology layer that makes it feel like working with a colleague.

---

## The Vision: Colleague, Not Tool

Piper Morgan is an AI-powered PM colleague that inhabits your existing workspace and helps with the upstream product work that execution tools don't address.

### What Makes Piper a Colleague, Not Just a Chatbot

The difference isn't features — it's **consciousness architecture**:

- **"I found 3 tasks that need attention"** not "Query returned 3 results" (Identity)
- **"Earlier this afternoon, when you were reviewing the PR"** not "At 14:32 UTC" (Time)
- **"Over in GitHub, in the sprint board"** not "Source: api.github.com" (Space)
- **"Would you like me to close that?"** not silent action (Agency)
- **"I'm noticing several PRs waiting — might be worth a nudge"** not "Alert: PR count > threshold" (Prediction)

These Five Pillars are implemented through the floor's system prompt and context assembly, not through a personality service or consciousness middleware. Consciousness is enforced at the voice layer — every response passes through the grammar ("Entities experience Moments in Places") and the Colleague Test.

### Bring Your Own Chat

Piper doesn't ask you to use a new app. **Piper shows up inside the AI conversation you're already having.**

Distributed as an MCP server, Piper's tools, context, and persistence are available to any MCP-compatible client — Claude Desktop, ChatGPT, Gemini, VS Code, and the growing ecosystem. The user picks their preferred LLM and client. Piper enhances it with PM-specific context methodology, artifact persistence, and trust-graduated experience.

This is the Radar O'Reilly pattern realized through distribution architecture: Piper appears where you already are and anticipates what you need. You never "go to" Piper. The mobile insight generalized: the user is mobile, not the app.

**"Bring Your Own Chat" solves two problems at once:**

1. **Discovery**: In a static UI, users must find features. In an MCP-powered conversation, the agent offers capabilities contextually. The user says "help me prep for tomorrow's sprint review" and the agent discovers what Piper tools are available, assembles context, and uses them. No navigation, no menus.

2. **Dynamic troubleshooting**: When an MCP tool returns unexpected results, the agent can inspect the error, adjust, and retry — all within the conversation. A static UI would show an error message and wait for a developer. The agent *debugs its own tools in real time*.

### Recognition Over Articulation

Users shouldn't need to know the right words. When someone says "what's on my plate?" Piper recognizes the intent — overwhelmed, need focus — rather than executing a literal query. The LLM floor is naturally good at this. Structured intent classification with 19 categories may actually be worse at recognition than letting the LLM understand naturally.

---

## The Differentiator Stack

**What Piper MVP offers is the methodology layer.** Not tools (commoditized), not LLM reasoning (commoditized), not individual integrations (available as plugins). The differentiation:

### 1. Context Methodology (The Five-Layer Model)

The five-layer context model — Kit Briefing, Project Instructions, Project Memory, Channel Addendum, Entity Prompt — operationalized as a practiced discipline. This is how context assembles, persists, transfers, and stays fresh. Nobody else has mapped this systematically, tested it through agent migrations, or published the results.

The proof: we migrated every agent to new infrastructure without losing one beat. That's not a feature — it's the product of a context methodology that nobody else has at this level.

### 2. Conscious Floor (Grammar + Five Pillars + Anti-Flattening)

The LLM floor speaks as Piper — with identity, temporal awareness, spatial awareness, agency, and prediction. Not through a personality service, but through carefully crafted system prompts and context assembly that embody the grammar. Anti-flattening is the ongoing discipline that prevents consciousness from degrading to mechanical behavior.

### 3. Artifact Persistence (Composting Lifecycle)

Conversation outputs that outlive the conversation. The lifecycle model (Emergent → Derived → Noticed → Proposed → Ratified → Deprecated → Archived → Composted → feeds new Emergent) is the experience design. Composted objects decompose into learnings that feed new understanding. Nothing truly disappears.

Implementation can start simple (save, browse, retrieve) but the design knows where it's going: artifacts have ownership levels, lifecycle states, and contribute to Piper's cumulative understanding. The "filing dreams" metaphor — composting surfaces as colleague reflection, not surveillance.

### 4. Trust-Graduated Experience

Piper earns the right to be proactive through demonstrated value:
- Stage 1 (New): Respond only
- Stage 2 (Building): Offer related capabilities after success
- Stage 3 (Established): Proactive suggestions based on context
- Stage 4 (Trusted): Anticipate needs

Trust is invisible to users but its effects are noticeable. Implementation can be lightweight (context-based prompting, not a dedicated computation service), but the design principle is non-negotiable.

### What's Indoor Plumbing (Use Existing Solutions)

- GitHub, Slack, Calendar, Notion integrations → MCP plugins
- File storage → filesystem or simple database
- Reminders/todos → existing task management patterns
- Authentication → standard OAuth/session patterns
- LLM provider management → adapter pattern, bring your own key

---

## Three Horizons (Revised)

### Horizon 1: Conscious Conversational Floor (Current Focus)

**What it is**: Piper as a conscious PM colleague powered by the LLM floor with assembled context, artifact persistence, and trust-graduated experience. Tool integrations via commodity MCP plugins.

**What's being built now**:
- Floor-first routing confirmed working (ADR-060, verified via UAT April 2026)
- Context assembly that grounds floor responses in real project state
- Artifact persistence (composting lifecycle, starting with save/browse/retrieve)
- Trust graduation through context, not dedicated services
- Action handlers only for side-effect operations (GitHub write, Calendar create, Todo persist)
- MCP-native distribution (MCPB format for Claude Desktop)

**What we've learned to drop**:
- 19-category intent classification → simpler action gate ("does this need a side effect?")
- Dedicated personality service → floor prompt with user preferences
- Code-based verification enforcement → methodology (audit-cascade, gate verification, Colleague Test)
- Bespoke tool integrations → MCP plugins for plumbing
- Four-wave consciousness rollout → consciousness lives in the floor prompt once

**The action gate test**: "Does this intent require an operation the LLM cannot perform within a floor response?" If yes → handler. If no → floor with context. This probably means 4-5 action handlers, not 19 classified categories.

### Horizon 2: Learning and Cumulative Understanding (Next)

**What it is**: Piper that genuinely learns — preferences, patterns, corrections — and accumulates understanding across sessions. The composting lifecycle becomes operational: observations decompose into insights that inform future behavior.

**Key capabilities**:
- User preferences that update from observed behavior (not just database-stored static values)
- Cross-session pattern recognition (your standups always run long → offer to help)
- Learning surfaced through trust gradient (low trust: factual patterns only; high trust: observations and suggestions)
- User control: correct, delete, inspect, reset what Piper has learned

**What we know already**: Layer 5 (behavioral calibration) is the hardest transfer problem. Klatch's Agent Traditions concept and Calliope's externalization pilot are the most promising approaches. The five-layer model gives us the diagnostic framework; Horizon 2 builds the solution.

### Horizon 3: Analytical Partnership (Future)

**What it is**: Piper as a genuine analytical partner — proactive insights, cross-project synthesis, predictive PM.

**Shaped by Horizon 2 learning, not by speculation.** Cross-project synthesis may be more achievable than we thought (the cross-pollination brief system demonstrates it today, conversationally). Predictive capabilities require data accumulation from sustained production usage.

---

## Architectural Principles (Evolved)

### 1. The LLM Is the Floor, Not the Ceiling
Every interaction at least as good as a well-prompted LLM with context. Handlers enhance; they don't replace.

### 2. Entities Experience Moments in Places
Constitutional grammar. Decision filter. Category error detector. Not a data schema.

### 3. Consciousness Is Architecture, Not Decoration
The Five Pillars constrain how Piper speaks. Anti-flattening prevents degradation. The Colleague Test is the quality gate. This is enforced at the prompt/context layer, not through middleware.

### 4. Don't Reinvent Indoor Plumbing
Use commodity solutions for tool integrations. Focus differentiation on the bathing experience — how context accumulates, how artifacts persist, how trust graduates, how the assistant feels like a colleague.

### 5. Completion Over Velocity
The Inchworm Protocol. The Pledge. Gall's Law: start with the simplest working system, extend only when it's rock-solid.

### 6. Trust Is Earned, Not Configured
Graduated proactivity through demonstrated value. Invisible to users; noticeable in effects.

### 7. Bring Your Own Chat (Evolved from "Bring Your Own Key")
LLM-agnostic MCP server. Users bring their preferred AI client — Claude, ChatGPT, Gemini, VS Code — and Piper enhances it. No new app to learn. The persona layer adapts per platform (Claude Project instructions, Custom GPT instructions, Gem instructions); the MCP server stays the same. Development optimizes for Claude Desktop via MCPB; the server works anywhere MCP does.

---

## The Methodology as Product

The founding vision described the *product* without the *process*. Ten months later, the methodology is itself a product-level asset:

- **Five-Layer Context Model**: How context assembles, persists, and transfers — the core IP
- **Excellence Flywheel**: Foundation-first → Systematic Verification → Multi-Agent Coordination → Accelerated Delivery
- **Completion Discipline Triad**: Green Tests Red User, Beads, Time Lord Alert
- **Building in Public**: 260+ blog posts; the methodology is the marketing
- **Ethics as Information Architecture**: Structural constraints, not policy afterthoughts (IAC talk, April 17, 2026)

The dominant pattern from the backlog review: the project consistently evolved from code frameworks to methodology infrastructure, and the methodology approach won every time. This is itself a product insight — Piper's MVP needs less structured code and more methodology tooling than the original backlog assumed.

---

## Success Looks Like

### For Individual PMs (Horizon 1-2)

A PM asks Piper, in Slack or the web UI, to help clarify the rationale for an initiative. Piper draws on assembled context — GitHub issues, meeting notes, previous conversations — and responds as a colleague who remembers the project's history. The PM spends 5 minutes refining rather than 30 minutes drafting from scratch. The output persists as an artifact that matures through the composting lifecycle. Over time, Piper learns the PM's style and applies it without being asked.

### For PM Teams (Horizon 3)

Quarterly planning includes Piper synthesizing cross-project signals, surfacing composted patterns from past quarters, and identifying capability gaps from the data. The PM still makes the call — informed by systematically assembled context rather than selective recall.

### For the Practice of PM

Piper Morgan demonstrates that AI product development can be thoughtful, transparent, and humane. The methodology is transferable. The building-in-public narrative serves as proof that ethical architecture produces better systems, not constrained ones.

---

## What Remains True from June 2025

- **The problem statement**: Context fragmentation and knowledge management overhead are real
- **The three-phase trajectory**: Task automation → analytical intelligence → strategic partnership
- **Domain-first architecture**: PM concepts drive technical decisions
- **Knowledge amplification over replacement**: Augment human judgment, don't substitute for it
- **Ethical AI partnership**: Transparency, human oversight, clear boundaries

## What the Founding Vision Didn't Know

- That the LLM floor would be high enough to handle most PM work without structured handlers
- That tool integrations would be commoditized through MCP before we shipped v1.0
- That consciousness architecture would survive and matter more than workflow orchestration
- That methodology infrastructure would consistently beat code frameworks
- That artifact persistence with lifecycle is the bridge between "good conversation" and "useful PM tool"
- That the object model would emerge from hand sketching, not AI-assisted design
- That a 14-agent team coordinated through async memos would work as well as it does
- That building the process of building the product would be as valuable as the product itself
- That the Phase 2 timeline was optimistic by roughly 12-18 months

---

*Draft v2.2 — April 8, 2026*
*Prepared by: Piper Alpha*
*Informed by: MUX analysis, backlog deep review, product strategy conversations with PM, MCPB feasibility research*
*For leadership review (PPM, CXO, Architect) alongside roadmap restructure proposal*

## Revision Log

- **June 21, 2025**: Founding vision (v1.0) — three-phase evolution, architectural principles, success scenarios
- **March 31, 2026**: Draft v2.0 — incorporates ALL STOP, Inchworm Protocol, object model, floor-first routing, PA experiment findings, distribution strategy, methodology-as-product framing
- **April 7, 2026**: Draft v2.1 — incorporates MUX deep dive (consciousness as architecture, Five Pillars as voice constraints, anti-flattening as discipline), backlog analysis (methodology > code frameworks), differentiator stack (context methodology + conscious floor + artifact persistence + trust graduation), "indoor plumbing vs bathing experience" distinction, revised Horizon 1 scope (conscious conversational floor with commodity plumbing)
- **April 8, 2026**: Draft v2.2 — adds "Bring Your Own Chat" (evolved from "Bring Your Own Key"), MCPB distribution as primary path, MCP Apps for artifact canvas, cross-platform portability via MCP standard, dynamic troubleshooting insight, discovery problem reframed through MCP
