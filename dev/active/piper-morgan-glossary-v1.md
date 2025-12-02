# Piper Morgan Glossary

**Version**: 1.0
**Date**: November 30, 2025
**Purpose**: Define project terminology, jargon, and concepts
**Invocation Question(s)**: "What are the terms in use at Piper Morgan that are necessary to understand or have a specific meaning in this context? Especially any terms that there might be some confusion about."

---

## Core Concepts

### ADR (Architecture Decision Record)
A document capturing an important architectural decision including context, decision, and consequences. Numbered sequentially (ADR-001, ADR-002, etc.). Lives in `/docs/internal/architecture/current/adrs/`.

### Agent
An AI instance with specific role, capabilities, and context. Examples: Chief Architect (strategic), Lead Developer (tactical), Code Agent (implementation).
Ted: add 'restrictions'

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

### Situation
Container holding sequences of Moments. The frame, not a fourth substrate. Has narrative structure with dramatic tension.

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

- **ADR**: Architecture Decision Record
- **MCP**: Model Context Protocol
- **MUX**: Modeled User Experience
- **PM**: Product Manager (xian's role)
- **PPP**: Policy, Process, People (analysis model)
- **RBAC**: Role-Based Access Control
- **SEC**: Security epic prefix

---

## Ted's Micro-Format Types
(From Nov 30 response)

1. **Capability/Feature/Use Case** - What the system can do
1.1 - Benefits ( why )
1.2 - Cost / Effort
2. **Initiative/Epic/Story/Task** - Work-Issue hierarchy
3. **Rule/Requirement/Guideline** - Constraints, business rules, technical rules
4. **Assertion/Statement** - Claims needing validation
5. **Inquiry/Question** - Queries needing answers
6. **Issue/Change Request/Trouble Report** - Problems, things that are non-optimal
7. **Permission/Security** - Access control
7.1 GRANT priviledge-type-group ON object-group TO grantee-user-group
8. **Data Model/Schema/Class/Data-Object** - Data Structure (persistence) definitions
8.1 See UML Class diagram
9. **Events/Workflow/Activity** - Process definitions
9.1 Workitem, Workstep
9.2 ON <event> DO <action(s)>
9.3 See UML State diagram
10. **Component/Functions/Procedures/Class/Code-Object** - Code structures
Ted adds:
11. **Plan/Methodology/Heuristic/Algorithm/Recipe/Tutorial** - related to getting things done (GTD)
12. **Canonical Query** - The set of base questions or requests that a user has that the system should service
13. **Report / View** - Typically an output that is the answer to an implied or stated question.
14. **Conversation / Dialog / Monolog / Musings** - shared thinking about topics.
15. **Reaction / Response**
16. **Model / View**
17. **Strategy/Tatic**

Ted: These micro-formats are generated from sub-regions of text/experience/conversations/presentations as part of Reaction-Flow
0) each speaker-presenter has context & goals & each listener has context & goals
1) the listener recognize/perceive/understand the presentation-stream
 1a) & might ask for clarification or validation as to their understanding
2) the listener 'reacts' to the presentation-stream
 2a) often this might be: 1) attention / emotional ( approach-avoid,... )
 2b) description / labeling / judging
3) some portion of the reaction-stream are labeled as micro-formats ( that is a <x-microformat> )
4) these microformats imply downstream responses / actions based on pre-defined skill-microformat-responses
---

*This glossary is a living document. Terms will be added and refined as the project evolves.*

task: Some terms to be added (above) (reason:) as they are specifically meaningful in this Piper-Morgan context:
Piper Morgan
Product Management
Project Management
AI-Assisted Integrated Development Environment ( IDE )
Computer-Assisted Software Engineering ( CASE )
Event-Driving Programming - ON event DO actions
Capability Maturity Model ( CMM )
Machine-Augmented Reasoning ( MAR )
**Conceptual Model** - An easily understood shared understanding of how things work & why, differentiated from implementation layers of 'logical model' and 'physical model'
**Architecture**
