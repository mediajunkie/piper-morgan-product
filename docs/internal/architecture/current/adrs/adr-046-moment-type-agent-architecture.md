# ADR-046: Moment.type Agent Architecture

**Status**: Proposed — DORMANT since 2025-12 (status annotated 2026-08-29)
**Date**: November 30, 2025 (Updated December 1, 2025)
**Author**: Chief Architect, with architectural design by Ted Nadeau

## Change Log
- 2025-12-01: Renamed from "Micro-Format Agent Architecture" to "Moment.type Agent Architecture" to avoid confusion with W3C HTML microformats standard (per Ted Nadeau feedback)

## Context

Through using the advisor mailbox system, Ted Nadeau identified a powerful architectural pattern for agent coordination. His insight: text input should be decomposed into typed "Moments" (Moment.types) that are routed to specialized agent handlers. This emerged from practical experience with async collaboration needs.

Our current architecture uses the grammar "Entities experience Moments in Places" (ADR-045) but lacks granularity in Moment types and processing specialization. The coordination queue works but treats all prompts uniformly. We need more sophisticated routing and handling.

Ted's observation: "There should be many small agents (helps with context, security, division of labor, scaling)."

Note: Ted correctly identified that "microformat" is an established W3C/HTML term. We adopt his suggestion to use "Moment.type" which aligns with our existing object model grammar.

## Decision

Adopt a Moment.type processing pipeline architecture where:

1. **Input text is decomposed** into typed Moments
2. **Each Moment.type** has a specialized listener agent
3. **Processing cascades** through a defined pipeline
4. **Service agents** handle final integration with external systems

### Moment.type Categories (Initial Set with Ted's Templates)

1. **Moment.type.capability**
   - Template: `[User-Type] has the ability to [do|see|change] <X>`
   - Example: "PM has the ability to see conversation history"

2. **Moment.type.epic** (Work hierarchy: Initiative/Epic/Story/Task)
   - Structure: Hierarchical work decomposition
   - Relations: parent-child, blocks, enables

3. **Moment.type.rule** (Constraints: Rule/Requirement/Guideline/Heuristic/Algorithm)
   - Structure: Constraint definition with context
   - Application: Governance and validation

4. **Moment.type.assertion**
   - Structure: Claims requiring validation
   - Workflow: Assert → Research → Validate/Invalidate

5. **Moment.type.question**
   - Template: `Q: [explicit question] A: [draft answer] Related: [Q&A links]`
   - Creates knowledge graph structure

6. **Moment.type.issue**
   - Template: `As <user> within <context> I experienced <X> but expected <Y>`
   - Perfect for trouble reports and gap analysis

7. **Moment.type.permission** (Security/Access control)
   - Structure: Subject-Action-Resource tuples
   - Enforcement: Cryptographic where possible

8. **Moment.type.schema** (Data Model/Structure definitions)
   - Notation: Consider GraphQL SDL per Ted's suggestion
   - Purpose: Type-safe definitions

9. **Moment.type.event** (Workflow/Process definitions)
   - Template: `ON <event-type> DO <set of actions>`
   - Maps to workflow orchestration

10. **Moment.type.function** (Code structures/Objects)
    - Structure: Interface definitions
    - Relations: implements, extends, uses

(Anticipate ~2x more types through discovery)

### Meta-Observation: ADRs as Moment.type

Ted's insight: ADRs themselves are Moment.types:

```javascript
Moment.type.adr = {
  structure: ["context", "decision", "consequences", "status"],
  workflow: ["draft", "review", "accept", "supersede"],
  relationships: ["implements", "supersedes", "depends-on"]
}
```

This validates the recursive nature of the architecture.

### Relationship Model

Moment.types relate through typed connections:
- `blocks` - Prevents progress
- `enables` - Allows capability
- `depends-on` - Requires completion
- `related-to` - Loose association
- `validates` - Confirms assertion
- `invalidates` - Contradicts claim
- `supersedes` - Replaces previous
- `implements` - Realizes design
- `counter-example` - Disproves rule

Note (per Ted): Relationship types themselves have relationships to each other (meta-relationships).

### Processing Architecture

```
Input Layer: Text Analysis
    ↓
Extraction Layer: Moment.type identification
    ↓
Routing Layer: Type-specific distribution
    ↓
Processing Layer: Specialized handlers (ON EVENT new-X DO)
    ↓
Service Layer: External system integration
```

### Evolution Path

1. **Phase 1**: File-based (current coordination queue)
2. **Phase 2**: Repository-backed with relationships
3. **Phase 3**: Message-based with routing
4. **Phase 4**: Workflow orchestration

### Formal Specification Approach

Per Ted's suggestion, consider GraphQL Schema Definition Language (SDL) for formal type definitions:

```graphql
type Capability {
  id: ID!
  userType: String!
  action: ActionType!
  target: String!
  enabled: Boolean!
}

enum ActionType {
  DO
  SEE
  CHANGE
}
```

## Consequences

### Positive

- **Specialization**: Each agent focuses on one Moment.type
- **Scalability**: Add new types without disrupting existing ones
- **Security**: Agents have minimal context/permissions
- **Traceability**: Clear path from input to action
- **Composability**: Moment.types combine into larger structures
- **Evolution**: Natural path from files to workflows
- **Self-hosting**: Architecture can describe itself (ADRs as Moment.type)

### Negative

- **Complexity**: More moving parts than monolithic processing
- **Coordination**: Inter-agent communication overhead
- **Discovery**: Need to identify Moment.types through use
- **Training**: Each agent type needs specific capabilities

### Neutral

- Changes our Moment model from generic to typed
- Requires routing layer infrastructure
- Shifts from single agent to multi-agent coordination
- Creates dependency on Moment.type extraction accuracy

## Implementation Strategy

### Pilot Approach (December 2025)

1. Test Ted's 3 template types (capability, question, issue) in coordination queue
2. Measure extraction accuracy and routing effectiveness
3. Implement specialized handlers for pilot types
4. Gather metrics on processing improvement

### Full Implementation (Q1 2026)

1. Build extraction layer with LLM-based classification
2. Implement routing infrastructure
3. Create specialized agent templates
4. Connect to service layer (GitHub, Slack, etc.)
5. Consider GraphQL SDL for formal specifications

## Relationship to Existing Architecture

### Maps to Object Model (ADR-045)
- Moment.types are specialized **Moment** subtypes
- Listener agents are specialized **Entity** processors
- Service layer represents **Places** where actions manifest
- Relationships create **Situation** containers

### Extends Coordination Queue
- Queue evolves from generic to typed prompts
- Routing becomes intelligent rather than claimed
- Specialization improves processing quality

## Validation

Ted's architecture emerged from actual use of our systems, not theoretical design. This bottom-up discovery validates the pattern through experience.

## References

- Ted's advisor mailbox responses (November 30 - December 1, 2025)
- ADR-045: Object Model (Entities, Moments, Places)
- Coordination Queue pilot results
- MUX-TECH implementation phases
- W3C Microformats specification (naming conflict avoided)
- Apollo GraphQL SDL Tutorial (suggested notation)

## Decision Outcome

**Accepted** - Will pilot with Ted's 3 template types (capability, question, issue) in December 2025, then expand based on results.

## Notes

This architecture represents a convergence between our build methodology (how we coordinate agents) and Piper's architecture (how Piper processes information). The recursive elegance is that we'll use Moment.type processing to build the Moment.type processor.

Ted's insight about "write-flow vs read-and-work-update flow" suggests different pipelines for different operations - creation versus modification patterns.

The fact that our collaboration with Ted is itself generating Moment.types (questions, agreements, issues) that need handling demonstrates the pattern's universality.

---

*Attribution: Core architectural design by Ted Nadeau, formalized by Chief Architect. Naming correction by Ted Nadeau (avoiding collision with W3C microformats).*
---

## Status annotation (2026-08-29, Chief Architect — Architectural Review 2026, mechanical win #4)

**Still Proposed; annotated DORMANT rather than unilaterally withdrawn.** Never ratified, never
formally declined; no decisions.log engagement since filing. PDR-004 subsequently assumed
experience governance without referencing it. Disposition (absorb / archive / revive) belongs to
the review's corpus-disposition pass (phase 4/7), not to a status edit — this annotation exists so
the dormancy is visible instead of ambient.
