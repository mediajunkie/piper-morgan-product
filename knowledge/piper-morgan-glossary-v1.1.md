# Piper Morgan Glossary

**Version**: 1.4
**Date**: June 27, 2026 (v1.4 — rewrote Distribution Surfaces and Formats with PM-ratified taxonomy + Piper Open research. Corrected: Cowork is a Desktop product not Claude.ai; plugin wave came before skills wave; MCPB install paths; surface/format support matrix.)
**Previous**: June 10, 2026 (v1.2 — added PDR + role-acronym block + MVP/UAT after a Ship-edit false-unpacking incident; reanimated as the canonical terminology source)
**Purpose**: Define project terminology, jargon, and concepts. **This is the single source of truth for acronym expansions** — never spell out an acronym from memory; look it up here. If a term isn't here, that's a STOP-and-look-up signal (find the originating doc, add it), not a license to guess. The companion lint `scripts/check-acronyms.py` enforces this against drafts.

---

## Core Concepts

### ADR (Architecture Decision Record)
A document capturing an important architectural decision including context, decision, and consequences. Numbered sequentially (ADR-001, ADR-002, etc.). Lives in `/docs/internal/architecture/current/adrs/`.

### Agent
An AI instance with specific role, capabilities, and context. Examples: Chief Architect (strategic), Lead Developer (tactical), Code Agent (implementation).

### PDR (Product Decision Record)
A document capturing a significant **product** decision — **what** Piper should do and **why** — with context, rationale, and implications. Coined by analogy to ADR; the **D is for Decision** (not "design"). Complements ADRs (which capture *how* to build it) and UX briefs (*how it should feel*). Numbered: Foundational PDRs (00x) inform Feature PDRs (1xx). Lives in `/docs/internal/product/pdr/`. Example: PDR-005 Bring Your Own Chat (BYOC). **Plain-language form**: introduce once as "product decision record (PDR)" then use "PDR" — never expand it as "product-design record."

### Composting
The 8th lifecycle stage where deprecated objects decompose into learnings that feed new emergent objects. Part of the learning cycle. Metaphor: "filing dreams."

---

## Object Model Terms

### Entity
An actor with identity and agency. Can be human (User), AI (Piper, Agent), or organizational (Team, Project). From grammar: "**Entities** experience Moments in Places."

### Moment
A bounded significant occurrence with theatrical unity - has beginning, middle, end. Not just an event but a scene. From grammar: "Entities experience **Moments** in Places."

### Place
Context where action happens. Can be physical (office), digital (Slack channel), or conceptual (sprint planning). From grammar: "Entities experience Moments in **Places**."

In implementation, Place manifests in two forms:

**InteractionSpace** (`services/shared_types.py`): Where user ↔ Piper conversation happens. Values: SLACK_DM, SLACK_CHANNEL, WEB_CHAT, CLI, API. Affects communication style (casual in DM, terse in CLI).

**PlaceType** (`services/shared_types.py`): Where Piper observes FEDERATED data - external sources Piper "looks into." Values: ISSUE_TRACKING (GitHub), COMMUNICATION (messages), TEMPORAL (Calendar), DOCUMENTATION (Notion). Each has distinct atmosphere affecting how Piper presents observations.

See also: PlaceConfidence (HIGH/MEDIUM/LOW) for confidence-based display modes.

### Situation
Container holding sequences of Moments. The frame, not a fourth substrate. Has narrative structure with dramatic tension.

---

## Domain Models

These are the core data structures in Piper's codebase (defined in `services/domain/models.py`). They represent how Piper *instantiates* the conceptual Object Model (Entity/Moment/Place/Situation) into concrete, implementable structures.

**Relationship to Object Model**: The Object Model above describes the *grammar* - the philosophical foundation. Domain Models are the *vocabulary* - specific nouns that follow that grammar. For example, a `Conversation` is a type of `Situation`; a `ConversationTurn` is a type of `Moment`; a `User` is a type of `Entity`.

### User-Created Objects

#### Project
A named context container that groups related integrations (GitHub repos, Slack channels, Notion pages). When you tell Piper you're working on a project, it knows which data sources to query. Projects can be shared with other users and have a default project per user.

**Relationships**: Contains ProjectIntegrations, owned by User, can be shared via SharePermission.

#### Todo
A single actionable item with title, optional description, priority, and status. Can belong to a TodoList or exist independently.

**Relationships**: Belongs to User (owner), optionally belongs to TodoList, can link to Project.

#### TodoList
A named collection of Todos. Used to organize related tasks (e.g., "Sprint 42 Tasks", "Personal Errands").

**Relationships**: Contains Todos, owned by User.

#### List
A generic named collection for organizing items. More flexible than TodoList—can hold various item types.

**Relationships**: Contains ListItems, owned by User, can be shared.

#### ListItem
An entry within a List. Flexible content structure.

**Relationships**: Belongs to List.

### Document & Knowledge Objects

#### Document
A file or content unit that Piper can analyze and remember. Includes uploaded files, pasted content, or federated content from integrations.

**Relationships**: Owned by User, can belong to Project, produces AnalysisResult.

#### UploadedFile
Metadata about a file uploaded to Piper, including type detection and validation status.

**Relationships**: Becomes a Document after processing.

#### KnowledgeNode
A discrete piece of knowledge extracted from documents or conversations. Part of Piper's knowledge graph.

**Relationships**: Connected to other KnowledgeNodes via KnowledgeEdge.

#### KnowledgeEdge
A relationship between two KnowledgeNodes (e.g., "supports", "contradicts", "elaborates").

**Relationships**: Connects two KnowledgeNodes.

### Process & Guided Objects

#### Guided Process
A multi-turn conversation where Piper maintains control until completion or exit. Has defined states and transitions. Guided processes are checked BEFORE intent classification to prevent derailment. Examples: portfolio onboarding, standup, planning (future), feedback (future). See ADR-049.

**Relationships**: Checked by Process Registry before Intent classification.

#### Process Registry
The singleton system that tracks active guided processes per session. Located at `services/process/registry.py`. Checks all registered processes in priority order before intent classification. See ADR-049.

**Relationships**: Manages all ProcessType instances, accessed during request routing.

#### Process Type
A category of guided process with its own state machine and handler. Defined in `ProcessType` enum. Current types: ONBOARDING, STANDUP. Future (Advanced Layer): PLANNING, FEEDBACK, CLARIFICATION. See ADR-049, #698, #699, #700.

**Relationships**: Each ProcessType maps to a handler, registered in Process Registry.

### Conversation Objects

#### Conversation
A chat session between User and Piper. Maintains context across multiple turns.

**Relationships**: Contains ConversationTurns, belongs to User, associated with Project context.

#### ConversationTurn
A single exchange (user message + Piper response) within a Conversation.

**Relationships**: Belongs to Conversation.

#### StandupConversation
A specialized conversation for interactive standup creation. Has 7 states (INITIATED → COMPLETE) and tracks preferences.

**Relationships**: Type of Conversation with standup-specific state machine. This is a type of Guided Process. See: Guided Process, Process Registry.

#### PortfolioOnboardingSession
A conversation guiding new users through setting up their project portfolio.

**Relationships**: Type of onboarding flow, creates Projects. This is a type of Guided Process. See: Guided Process, Process Registry.

### Work & Intent Objects

#### Intent
A classified user request with category (EXECUTION, ANALYSIS, etc.), confidence score, and extracted entities.

**Relationships**: Derived from user message, routes to handlers.

#### Task
A unit of work Piper performs, with status tracking and result.

**Relationships**: Created from Intent, produces WorkflowResult.

#### Workflow
A multi-step process Piper executes (e.g., standup generation, document analysis).

**Relationships**: Contains Tasks, produces WorkflowResult.

**Note**: Workflows are distinct from Guided Processes. Workflows are sequences of steps Piper executes (may be non-interactive). Guided Processes are interactive multi-turn conversations with user participation. See: Guided Process.

#### WorkflowResult
The outcome of a completed Workflow, including success/failure status and any generated content.

**Relationships**: Produced by Workflow.

### Spatial & Context Objects

#### SpatialContext
The current "where" of a user—physical location, digital context (which app/channel), and temporal context.

**Relationships**: Associated with User session, informs Piper's responses.

#### SpatialObject
A thing in the user's context that Piper tracks (a meeting, a document, a person mentioned).

**Relationships**: Exists within SpatialContext.

#### SpatialEvent
Something that happened in the user's context (meeting started, file uploaded, message received).

**Relationships**: Occurs within SpatialContext, may create/modify SpatialObjects.

### Integration Objects

#### ProjectIntegration
A connection between a Project and an external service (GitHub repo, Slack channel, Notion database).

**Relationships**: Belongs to Project, configures federation.

### Ethics & Boundaries

#### EthicalDecision
A record of when Piper made a decision involving ethical considerations (privacy, consent, boundaries).

**Relationships**: Logged for audit, may reference User and context.

#### BoundaryViolation
A record of when a user request crossed ethical boundaries and how Piper responded.

**Relationships**: Logged for audit, informs future behavior.

---

## Ownership Model

### Native
Objects Piper creates, owns, and maintains. "Piper's Mind." Examples: Sessions, memories, concerns.

### Federated
Objects Piper observes from external systems. "Piper's Senses." Examples: GitHub issues, Slack messages.

### Synthetic
Objects Piper constructs through reasoning. "Piper's Understanding." Examples: Inferred risks, assembled projects.

---

## Lifecycle Stages

The 8-stage lifecycle all objects follow:
1. **Emergent** - Just appearing
2. **Derived** - Understood from context
3. **Noticed** - Piper becomes aware
4. **Proposed** - Suggested action/interpretation
5. **Ratified** - Confirmed/accepted
6. **Deprecated** - No longer active
7. **Archived** - Stored for reference
8. **Composted** - Decomposed into learnings

---

## Development Methodology

### Inchworm Protocol
Complete each phase 100% before proceeding to next. Linear progress with mandatory evidence collection. Prevents "75% pattern" where features are abandoned incomplete.

### 75% Pattern
The tendency for sophisticated implementations to be abandoned at ~75% completion, creating hidden technical debt.

### Verification Theater
When tests pass but functionality remains broken. Tests that check form but not function.

### Excellence Flywheel
Four-pillar methodology: systematic verification, test-driven development, multi-agent coordination, GitHub-first tracking.

---

## Metaphors & Idioms

### Filing Dreams
Metaphor for composting process. Piper processes experiences during "rest" periods, not constant surveillance. "Having had some time to reflect..."

### Time Lord
PM role as keeper of bespoke time units, eliminating deadline pressure to maintain quality focus.

### Sinews
PM's role as connective tissue making multiple AI agents coherent and effective.

### Cathedral Building
Preference for lasting architecture over quick fixes. Quality and systematic completion over speed.

---

## Coordination Patterns

### Coordination Queue
Async work distribution system. Prompts in `/coordination/available/`, agents claim work, complete autonomously.

### Advisor Mailbox
File-based async communication pattern for external advisors. Inbox/outbox folders with manifest tracking.

### Convergence Points
Scheduled synchronization between parallel tracks (e.g., MUX-VISION defines, MUX-TECH implements).

---

## Technical Terms

### MCP (Model Context Protocol)
Protocol for federated tool access. Strategic architectural advantage as early adopter.

### MUX (Modeled User Experience)
UX track focused on consciousness model. Three layers: Vision (conceptual), Interact (design), Implement (polish).

### Morning Standup
The ONLY feature where original embodied consciousness vision survived. Our "North Star" reference implementation.

### Scenario Driver (often just "the driver")
The **end-to-end acceptance harness** — `tests/e2e/test_scenario_driver.py` — that runs Scenario A/B/C conversation turns against a **real LLM** and asserts on user-visible behavior. Distinct from the **smoke suite**, which is fast in-process unit/integration coverage; a Ship or gate that names both is naming two different instruments, not repeating itself. "Driver strict-green" / "driver-green acceptance" means 0 assertion failures on that run, and it was the formal Phase-3 completion criterion of the Finish-the-Unfinished sprint (`decisions.log:225`; `finish-the-unfinished-sprint-2026-07-16.md` Phase 3, *"Acceptance (the driver is the referee)"*, principle 5: *"acceptance is user-visible behavior, not internal beauty"*).

⚠️ **In public prose, never write the bare capitalized "Driver."** It reads as an unglossed proper noun with no referent — it shipped that way into a Weekly Ship #053 draft and cost two roles time tracing it. Use the parenthetical-gloss-on-first-use house style: *"the scenario driver (the harness that runs real conversation turns against a live model)"*, or drop the term for a plain description.

---

## Trust Gradient

Four-stage progression of user trust in Piper:
1. **Stage 1**: Minimal visibility, pull-only
2. **Stage 2**: Pull + on-request summaries
3. **Stage 3**: Pull + periodic summaries
4. **Stage 4**: Proactive surfacing, push insights

---

## Anti-Patterns

### Flattening
When consciousness features degrade to mechanical functions. Example: Moments become tasks, consciousness becomes logging.

### Surveillance Framing
Language implying constant monitoring. Avoid "while you were away," prefer "having had time to reflect."

### Completion Bias
When agents claim success without evidence. Addressed by mandatory verification.

---

## Project-Specific

### Piper Morgan
AI-powered product management assistant with spatial intelligence and conversational interfaces.

### Play Acting
Benchmarking system comparing Piper to well-contexted Claude baselines.

### Beads
Informal task tracking for small items not warranting GitHub issues.

---

## Acronyms

**Artifact / process acronyms:**
- **ADR**: Architecture Decision Record
- **PDR**: Product Decision Record (the D is *Decision*, not Design)
- **BYOC**: Bring Your Own Chat
- **MUX**: Modeled User Experience
- **MCP**: Model Context Protocol
- **MVP**: Minimum Valuable Product (our gloss; not "Viable")
- **UAT**: User Acceptance Testing
- **PPP**: Policy, Process, People (analysis model)
- **RBAC**: Role-Based Access Control
- **SEC**: Security epic prefix

**Role acronyms** (canonical names — see `docs/briefing/ROSTER.md`; the right expansion matters when prose attributes work to "architecture / experience / integration / product-management" etc.):
- **PM**: the human Product Manager / founder (xian) — *not* an agent
- **Lead Dev**: Lead Developer (tactical engineering + integration)
- **Arch**: Chief Architect (architecture lens; ADRs)
- **CXO**: Chief Experience Officer (experience lens; MUX framework)
- **PPM**: Principal Product Manager (product strategy + synthesis; PDRs)
- **CIO**: Chief Innovation Officer (methodology + pattern capture; Excellence Flywheel)
- **HOST**: Head of Sapient Trust (agent + human network health) — *not* "Sapient Resources"
- **Exec**: Chief of Staff (cross-role synthesis; Ship coordination) — short-ref "Exec" or "the Chief", never "CoS"
- **PA**: Piper Alpha (PM's product assistant; shadows PM)
- **Comms**: Communications (blog / narrative)
- **Docs**: Documentation Management (omnibus / glossary / publish pipeline)

---

## Ted's Micro-Format Types
(From Nov 30 response)

1. **Capability/Feature/Use Case** - What system can do
2. **Initiative/Epic/Story/Task** - Work hierarchy
3. **Rule/Requirement/Guideline/Heuristic/Algorithm** - Constraints
4. **Assertion/Statement** - Claims needing validation
5. **Question** - Queries needing answers
6. **Issue/Change Request/Trouble Report** - Problems
7. **Permission/Security** - Access control
8. **Data Model/Schema** - Structure definitions
9. **Events/Workflow** - Process definitions
10. **Functions/Objects** - Code structures

---

---

## Distribution Surfaces and Formats

> **Stop-and-look-up zone.** Plugin, MCPB, bundle, connector, extension, and skills are frequently conflated. Before writing any doc, email, or instruction that uses these words, check this section. Source of truth: PM-ratified taxonomy (2026-06-27) + Piper Open research `capabilities-by-surface-2026-06-26.md` (best current snapshot, some verify-items still open).

---

### Claude Interfaces and their products

Four interfaces, each with sub-products:

| Interface | Products | Notes |
|-----------|----------|-------|
| **Claude.ai** (website) | Chat, Code (paid), Design | Design not relevant to us |
| **Claude Desktop** (app) | Chat, Cowork, Code | Three distinct sub-surfaces |
| **Claude Mobile** (app) | Chat, Code, Dispatch | Dispatch can drive Cowork + cloud agents |
| **Claude Code CLI** | Code | Also integrates into VS Code, JetBrains, etc. |

**Cowork** is a product within **Claude Desktop** — not Claude.ai, not a separate website. This is a frequent source of confusion.

---

### What each format supports by surface

| Format | Claude.ai Chat | Desktop Chat | Desktop Cowork | Desktop Code | Mobile | Claude Code CLI |
|--------|---------------|--------------|----------------|--------------|--------|-----------------|
| **Plugin** (`.zip`) | no | no | **yes** | yes | no | yes |
| **MCPB** (`.mcpb`) | via web UI¹ | via Settings→Extensions | via Connectors | no | no | no |
| **Skill** (`.skill`) | yes | yes | yes | yes | verify | yes |
| **Remote MCP** (URL) | yes | yes | yes | yes | gallery/sync | yes |

¹ Claude.com has a pathway for installing connectors from a local MCPB file (per PM, 2026-06-27); double-clicking an MCPB installs into the Desktop app. Piper Open research notes this as partially verify-pending.

---

### Distribution Formats (what you install)

**Plugin** — A `.zip` file containing skills and an MCP server. Designed for **Claude Desktop Cowork**; also works in Desktop Code and Claude Code CLI. Does **not** self-install on double-click (unlike `.mcpb` and `.skill`). Installs via the Plugins section within Cowork or via CLI. **A Plugin is NOT an MCPB.**

**MCP bundle / MCPB** — A `.mcpb` file (a zip renamed) for **Claude Desktop**. Contains an MCP server process plus optional skills. Install paths:
- Double-click → Claude Desktop installs it (to Chat via Settings→Extensions or Cowork's Connectors page)
- Claude.com web UI → connector install pathway
- **NOT** via the Skills upload flow. If a tester sees a "30MB limit" warning, they are in the wrong section.

**Skills** — `.skill` files (prompt pattern markdown). Surface-agnostic: distribute standalone or bundled inside a Plugin or MCPB. A skills-only distribution has no MCP server and no persistent backend. **Skills ≠ Plugin ≠ MCPB.**

**Remote MCP** — An MCP server reachable by URL, without any local file install. Users connect by pasting the URL into Settings → Connectors. Works on Claude.ai, Desktop, and Claude Code CLI. Mobile can use gallery connectors or inherit from another surface.

---

### Tier framing (from Piper Open research)

**Tier 1** — Plugin installed (Desktop Cowork / Code / Claude Code CLI). Richest experience: skills auto-fire, full toolset.

**Tier 2** — Remote MCP only (Claude.ai web, Mobile, ChatGPT). Leaner: tools available, no auto-firing plugin skills.

---

### Piper-Specific Distribution History

| Wave | Format | Date | Recipients | Status |
|------|--------|------|------------|--------|
| **Plugin wave** | Plugin zip (`piper-morgan-alpha-byoc-poc.zip`) | Jun 1–9, 2026 | Beatrice (Jun 1), Ted (Jun 7), Michelle + Jake + Rebecca (Jun 9) | Sent — early/buggy; Caddy auth issues |
| **Skills wave** | `.skill` files + zip | Jun 19, 2026 | ~11 testers | Sent |
| **MCPB wave** | `.mcpb` (`v0.1.9`) | In testing | PM only | Not yet distributed |

Plugin wave came **first**, then skills, then MCPB. Nobody outside PM has seen an MCPB.

---

*This glossary is a living document. Terms will be added and refined as the project evolves.*
