---
image: 'ai-triad.png'
alt: 'Three glowing AI collaborators refine a floating crystal together while a human founder watches approvingly from the side, illustrating product, design, and engineering perspectives combining into a stronger shared idea.'
caption: '"This is really coming together!"'
---

# The Triad Model

*December 2, 2025*

Back in December I started thinking about what the first-time user experience should be for Piper Morgan. In discussion with my principal product manager agent (PPM) we adopted the concept of a product decision record (PDR), modeled on the ADR (architectural decision record) idea, and intentionally flipping the PRD (Product Requirements Document) concept on its head a bit.

PPM wrote our first PDR about first-time user experience. The draft was solid — clear problem statement, considered alternatives, documented reasoning. Then it went to my chief experience officer agent (CXO) and my chief architect agent (Arch) for feedback.

Anticipating anything from corrections to approval, I got back refinement. The CXO contributed experience design insights - tiered models, hybrid credential patterns, enhanced empty states. The Architect contributed technical considerations - trust state persistence, credential wrappers, empty state recognition systems.

The PPM incorporated both perspectives. The PDR improved. Not because anyone was wrong initially, but because three different lenses revealed things one lens couldn't see.

This is the classic triad model. Some call it "three in a boat" and who the three are varies depending on who you ask, but in my world it tends to be product, design, and engineering. In agentic terms on my project this means PPM, CXO, and Arch meeting in liminal space, each contributing from their corner of expertise, no hierarchy dictating whose perspective dominates.

# The three corners

**Product** asks: What should we build and why?
- User needs, market context, strategic value
- Success criteria and business logic
- Trade-offs between competing priorities

**Experience** asks: How should it feel to use?
- User perception, emotional response, trust development
- Interface clarity, progressive disclosure, recognition patterns
- The gap between functional correctness and user delight

**Engineering** asks: How should we build it?
- Technical feasibility, architectural fit, implementation patterns
- Performance implications, maintenance burden, scaling considerations
- The gap between design intent and technical reality

Each corner represents not a role but a focused lens, a way of seeing the problem that emphasizes certain dimensions while de-emphasizing others. No single lens sees the whole picture. The triad works because the lenses complement rather than compete.

# The first PDR's evolution

**Assignment from me**
*Following what I call Human at the Start (HATS), I initially thought through and discussed my expectations and laid out the assignment.*

**Initial Draft (PPM)**:
> The FTUX should recognize who the user is and what they might need. Traditional wizards create friction. Blank slates offer no guidance. We need something between: enough structure to orient, enough flexibility to adapt.

**CXO Feedback**:
> Recognition is right, but needs tiers. Not everyone arrives with the same context. Some have read docs, some installed from blog post, some got referred. The interface should adapt to what we already know. Also: hybrid credential pattern - conversational for API keys (low stakes), secure UI for passwords (high stakes). And enhanced empty states that teach without lecturing.

**Architect Feedback**:
> Trust state persistence is a missing model. We talk about recognizing users but have no entity to store what we've learned. Credential wrapper needed - some credentials are secrets (keychain), some are preferences (stored differently). Empty state recognition requires the system to understand "nothing here yet" as distinct from "loading" or "error."

**Me again, trying to be a smart bottleneck**:
*At this stage I reviewed and discussed all the feedback with PPM, who was still anchoring the effort, ensuring that my attention was focused on key decisions when I mattered, an approach I've started called Human Owns the Loop (HOTL).*

**Final PDR (PPM + CXO + Architect)**:
> First contact is first recognition - treating setup like meeting a colleague. Tiered model (0-3) based on user context. Hybrid pattern for credentials respecting stakes. Trust state as explicit model (dependency noted for architecture track). Enhanced empty states with teaching moments. Technical notes documented for implementation.

**My final approval**:
*Reading the results and having no further corrections to add, I book-ended the process by giving my final approval, upholding my third key principle: Human As Last Test (HALT).*

Each perspective added something the others couldn't see. The PPM framed the problem. The CXO refined the experience model. The Architect surfaced technical dependencies. All three together created something more complete than any individual lens.

# Why no hierarchy

The triad works because no corner dominates. The PPM doesn't overrule the CXO. The Architect doesn't veto the PM. Each contributes expertise, all respect boundaries.

This only works when:
- Each corner has genuine expertise in their domain
- Each respects the others' expertise in their domains
- The artifact being created lives in liminal space (not purely product, not purely experience, not purely technical)
- All three care more about the quality of the outcome than about whose perspective "wins"

Of course as the boss, the founder, the project lead, the CEO, and most importantly the *human being with intention and agency* I retain the final say.

Rather than being expressed hierarchically, expertise is distributed effectively. Within product questions, PPM's lens carries weight. Within experience questions, CXO's lens carries weight. Within technical questions, the Arch's lens carries weight. The distribution matches the domain.

# Liminal space artifacts

The triad model applies to artifacts that live between domains. Product Decision Records are one example - they're about product (what to build) AND experience (how it should feel) AND architecture (how to build it). No single domain owns them.

Other liminal artifacts:
- **Feature specifications**: Product intent + experience design + technical approach
- **Architecture decisions**: Technical choice + user impact + product implications
- **API designs**: Developer experience + technical constraints + product use cases
- **Onboarding flows**: User psychology + product value + technical capabilities

These artifacts need multiple lenses because they exist at domain intersections. Trying to create them from one perspective produces blind spots. The triad ensures multiple perspectives converge.

# The contribution pattern

Watch how the triad contributions work:

**Initial framing (whichever discipline is driving)**: "Here's the problem space, the context, the constraints we're working within."

**First refinement (one of the other experts)**: "That framing works, and here's a dimension it doesn't yet address. What if we also considered..."

**Second refinement (the other)**: "Both of those perspectives are valid. Here's a technical (for example) consideration that connects them differently."

**Integration (back to drive)**: "Taking both perspectives, here's how the framing evolves. These parts stay, these parts shift, these new considerations get added."

It's additive refinement. Each contribution builds on what came before, revealing dimensions that weren't initially visible.

# The triad's limits

Not every decision needs three perspectives. Some are purely technical (Architect decides). Some are purely experiential (CXO decides). Some are purely strategic (PM decides).

A triad applies when:
- The artifact is liminal (lives between domains)
- Multiple perspectives would genuinely improve the outcome
- Time exists for refinement cycles
- All three corners have relevant expertise

Forcing the triad pattern onto every decision creates overhead without value. The model works for significant artifacts where multi-lens refinement matters. Routine decisions can stay in their appropriate domain.

# The meta-pattern

Here's what makes this interesting: the triad model itself emerged from the triad. The PPM noticed the collaboration pattern. The CXO articulated the experiential quality ("it feels different when no one's claiming authority"). The Architect identified the structural requirement ("liminal artifacts need distributed expertise").

The pattern describing itself through the pattern. That's how you know it's real rather than theoretical - it explains its own emergence.

# What resulted

It was about validating that the triad model works in practice, not just as aspiration.

The PPM drafted. The CXO refined. The Architect added technical considerations. The PM integrated. The artifact improved. No one felt overruled or dismissed. Everyone's contribution mattered.

This wasn't the first time we'd collaborated across domains. But it was the first time we recognized the pattern clearly enough to name it and document how it works. That recognition matters - now we can invoke the pattern deliberately rather than stumbling into it accidentally.

# Invoking the triad

When facing a liminal artifact - something that needs product AND experience AND technical perspectives:

1. **Frame it** (usually PM): Problem space, context, constraints
2. **Refine it** (CXO + Architect): Additional dimensions, considerations, dependencies
3. **Integrate** (back to PM): Incorporate all perspectives, document reasoning
4. **Validate** (all three): Does this feel complete? What's still missing?

The cycle might repeat. The CXO might notice something after the Architect's input that changes their perspective. The Architect might see architectural implications of the CXO's refinement. The integration isn't final until all three perspectives feel represented.

# The trust requirement

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
