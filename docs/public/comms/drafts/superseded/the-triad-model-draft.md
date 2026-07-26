# The Triad Model

*December 2*

My principal product manager agent (PPM) drafted a Product Decision Record about first-time user experience. The draft was solid — clear problem statement, considered alternatives, documented reasoning. Then it went to my chief experience officer agent (CXO) and my chief architect agent (Architect) for feedback.

What came back wasn't corrections or approval. It was refinement. The CXO contributed experience design insights - tiered models, hybrid credential patterns, enhanced empty states. The Architect contributed technical considerations - trust state persistence, credential wrappers, empty state recognition systems.

The PM incorporated both perspectives. The PDR improved. Not because anyone was wrong initially, but because three different lenses revealed things one lens couldn't see.

This is what we call the Triad Model: PM + CXO + Architect, meeting in liminal space, each contributing from their corner of expertise, no hierarchy dictating whose perspective dominates.

## The three corners

**Product Manager** asks: What should we build and why?
- User needs, market context, strategic value
- Success criteria and business logic
- Trade-offs between competing priorities

**Chief Experience Officer** asks: How should it feel to use?
- User perception, emotional response, trust development
- Interface clarity, progressive disclosure, recognition patterns
- The gap between functional correctness and user delight

**Chief Architect** asks: How should we build it?
- Technical feasibility, architectural fit, implementation patterns
- Performance implications, maintenance burden, scaling considerations
- The gap between design intent and technical reality

[PLACEHOLDER: Roles in your work that represent different perspectives - who asks what questions? When have different lenses revealed blind spots? The value of perspective diversity?]

Each corner represents not just a role but a lens - a way of seeing the problem that emphasizes certain dimensions while de-emphasizing others. No single lens is complete. The triad works because the lenses complement rather than compete.

## How the first PDR evolved

**Initial Draft (PM)**:
The FTUX should recognize who the user is and what they might need. Traditional wizards create friction. Blank slates offer no guidance. We need something between: enough structure to orient, enough flexibility to adapt.

**CXO Feedback**:
Recognition is right, but needs tiers. Not everyone arrives with the same context. Some have read docs, some installed from blog post, some got referred. The interface should adapt to what we already know. Also: hybrid credential pattern - conversational for API keys (low stakes), secure UI for passwords (high stakes). And enhanced empty states that teach without lecturing.

**Architect Feedback**:
Trust state persistence is a missing model. We talk about recognizing users but have no entity to store what we've learned. Credential wrapper needed - some credentials are secrets (keychain), some are preferences (stored differently). Empty state recognition requires the system to understand "nothing here yet" as distinct from "loading" or "error."

**Final PDR (PM + CXO + Architect)**:
First contact is first recognition - treating setup like meeting a colleague. Tiered model (0-3) based on user context. Hybrid pattern for credentials respecting stakes. Trust state as explicit model (dependency noted for architecture track). Enhanced empty states with teaching moments. Technical notes documented for implementation.

[PLACEHOLDER: Artifacts improved through multiple perspectives - when has feedback revealed dimensions you hadn't considered? The difference between revision and refinement?]

Each perspective added something the others couldn't see. The PM framed the problem. The CXO refined the experience model. The Architect surfaced technical dependencies. All three together created something more complete than any individual lens.

## Why no hierarchy

The triad works because no corner dominates. The PM doesn't overrule the CXO. The Architect doesn't veto the PM. Each contributes expertise, all respect boundaries.

This only works when:
- Each corner has genuine expertise in their domain
- Each respects the others' expertise in their domains
- The artifact being created lives in liminal space (not purely product, not purely experience, not purely technical)
- All three care more about the quality of the outcome than about whose perspective "wins"

[PLACEHOLDER: Collaboration without hierarchy - when has peer expertise created better outcomes than authority? What enables people to contribute without one person controlling? Failed attempts at non-hierarchical work?]

The hierarchy isn't absent - it's distributed. Within product questions, the PM's lens carries weight. Within experience questions, the CXO's lens carries weight. Within technical questions, the Architect's lens carries weight. The distribution matches the domain.

## Liminal space artifacts

The triad model applies to artifacts that live between domains. Product Decision Records are one example - they're about product (what to build) AND experience (how it should feel) AND architecture (how to build it). No single domain owns them.

Other liminal artifacts:
- **Feature specifications**: Product intent + experience design + technical approach
- **Architecture decisions**: Technical choice + user impact + product implications
- **API designs**: Developer experience + technical constraints + product use cases
- **Onboarding flows**: User psychology + product value + technical capabilities

These artifacts need multiple lenses because they exist at domain intersections. Trying to create them from one perspective produces blind spots. The triad ensures multiple perspectives converge.

[PLACEHOLDER: Artifacts in your work that live between domains - what needs multiple perspectives? When has single-lens creation created problems? Cross-functional collaboration patterns that worked?]

## The contribution pattern

Watch how the triad contributions work:

**Initial framing (usually PM)**: "Here's the problem space, the context, the constraints we're working within."

**First refinement (usually CXO or Architect)**: "That framing works, and here's a dimension it doesn't yet address. What if we also considered..."

**Second refinement (the other specialist)**: "Both of those perspectives are valid. Here's a technical (or experiential) consideration that connects them differently."

**Integration (back to PM)**: "Taking both perspectives, here's how the framing evolves. These parts stay, these parts shift, these new considerations get added."

The pattern isn't debate. Nobody's defending positions. It's additive refinement - each contribution builds on what came before, revealing dimensions that weren't initially visible.

[PLACEHOLDER: Contribution patterns that build rather than compete - when has additive feedback improved your work? The difference between criticism and refinement? Collaborative cultures that enabled this?]

## When the triad doesn't apply

Not every decision needs three perspectives. Some are purely technical (Architect decides). Some are purely experiential (CXO decides). Some are purely strategic (PM decides).

The triad applies when:
- The artifact is liminal (lives between domains)
- Multiple perspectives would genuinely improve the outcome
- Time exists for refinement cycles
- All three corners have relevant expertise

Forcing the triad pattern onto every decision creates overhead without value. The model works for significant artifacts where multi-lens refinement matters. Routine decisions can stay in their appropriate domain.

[PLACEHOLDER: When to involve multiple perspectives vs when to decide quickly - your decision-making patterns? When collaboration improves outcomes vs creates overhead?]

## The meta-pattern

Here's what makes this interesting: the triad model itself emerged from the triad. The PM noticed the collaboration pattern. The CXO articulated the experiential quality ("it feels different when no one's claiming authority"). The Architect identified the structural requirement ("liminal artifacts need distributed expertise").

The pattern describing itself through the pattern. That's how you know it's real rather than theoretical - it explains its own emergence.

## What Tuesday demonstrated

Tuesday wasn't just about creating PDR-001. It was about validating that the triad model works in practice, not just as aspiration.

The PM drafted. The CXO refined. The Architect added technical considerations. The PM integrated. The artifact improved. No one felt overruled or dismissed. Everyone's contribution mattered.

[PLACEHOLDER: Validation of collaboration models - when has a theoretical approach proven practical? The difference between aspiration and implementation? Patterns that work vs patterns that sound good?]

This wasn't the first time we'd collaborated across domains. But it was the first time we recognized the pattern clearly enough to name it and document how it works. That recognition matters - now we can invoke the pattern deliberately rather than stumbling into it accidentally.

## How to invoke

When facing a liminal artifact - something that needs product AND experience AND technical perspectives:

1. **Frame it** (usually PM): Problem space, context, constraints
2. **Refine it** (CXO + Architect): Additional dimensions, considerations, dependencies
3. **Integrate** (back to PM): Incorporate all perspectives, document reasoning
4. **Validate** (all three): Does this feel complete? What's still missing?

The cycle might repeat. The CXO might notice something after the Architect's input that changes their perspective. The Architect might see architectural implications of the CXO's refinement. The integration isn't final until all three perspectives feel represented.

[PLACEHOLDER: Your own collaboration protocols - how do you coordinate across expertise domains? Patterns that ensure all perspectives contribute? When formal structure helps vs when it's overhead?]

## The trust requirement

The triad only works with trust. Each corner must trust:
- The others' expertise in their domains
- The others' intention to improve the outcome (not win arguments)
- The others' respect for their expertise
- The process to produce something better than individual work

Without trust, the triad becomes politics. People defend positions instead of contributing perspectives. Expertise becomes territory. Refinement becomes criticism.

Building that trust takes time - shared work, demonstrated competence, proven respect for boundaries. You can't mandate triad collaboration. You can create conditions for it and recognize it when it emerges.

The Tuesday PDR session worked because we'd built that trust through prior work. The pattern was available because the relationships supported it.

---

*Next on Building Piper Morgan: "Relationship-first Ethics."*

*What collaboration patterns work in your team? When has multi-lens refinement improved outcomes? How do you build trust that enables contribution without hierarchy?*
