# The Planning Caucus

*January 19*

[alt text: Four specialists in a relay race, each passing a baton to the next]
Caption: "Each runner handing off cleanly"

One issue. Four meetings. One subagent. 101 tests by end of day.

That's the shape of January 19th—the day we launched the MUX track with what I'm calling a "planning caucus": a deliberate sequence of specialized consultations before any code was written.

## The issue

Issue #399: MUX Object Model Implementation.

This wasn't a bug fix or a quick feature. This was foundational work—turning our conceptual object model ("Entities experience Moments in Places") into actual running code. Eight months of thinking were about to become infrastructure.

The risk of getting it wrong was high. The cost of rework would be weeks, not hours. So instead of diving straight into implementation, I tried something different.

## The caucus

I scheduled four planning sessions, each with a different specialist agent.

At 9:28 AM, the CXO tackled the first question: What does "experience" actually mean in our grammar? The design philosophy that emerged centered on three principles: awareness not data (entities perceive, they don't just store), atmosphere not contents (places have character, not just items), and weight not sequence (some moments matter more than order). The key insight was that "experience" is the verb that needs the most attention—it's what makes Piper Morgan different from a database with a chat interface.

At 9:58 AM, the Principal PM addressed the second question: How do we translate design into implementation phases? The PPM took the CXO's philosophy and turned it into actionable guidance. They added Phase 4.5 for canonical query tagging with lens mapping, revised the estimate from 20 to 31-32 hours, established success metrics at three tiers, and assigned Pattern-051 to the Lead Developer. The key insight: "Cathedral work, not velocity work—40 hours done right beats 20 hours flattened."

At 11:16 AM, the Chief Architect provided technical direction. Use Protocols for role fluidity, not inheritance. Build lenses on the existing 8-dimensional spatial framework. Treat Situation as context manager, not data model. Cross-reference ADR-054 for persistence boundaries. The key insight: the infrastructure we need already partially exists—build on it, don't rebuild it.

At 12:28 PM, the Lead Developer absorbed all the guidance and began execution. By 1:37 PM, seven child issues were spec'd (#612-#618). By 3:45 PM, Phase 0 investigation was complete. By 4:20 PM, a subagent was deployed for Phase 1.

## The subagent

Here's where it gets interesting.

The subagent deployed at 4:20 PM completed Phase 1 in 15 minutes. Not 15 hours. Fifteen minutes.

Delivered: 15 source files (protocols, situations, perception models), 8 lens implementations, 17 test files, and 101 passing tests. All template requirements met.

How is that possible?

Because by the time the subagent started, every decision had already been made. The design philosophy was clear. The implementation pattern was specified. The success criteria were defined. The architectural constraints were documented.

The subagent's job wasn't to figure anything out. It was to execute a precisely specified plan.

[PM PLACEHOLDER: The 15-minute P1 completion—what was your reaction when that came back done?]

## Why this worked

I've run plenty of sessions where I go straight to the Lead Developer with "Here's the issue, figure it out." Sometimes that works. Often it doesn't—there's thrashing, rework, architectural drift, and the creeping suspicion that we're building the wrong thing.

The planning caucus inverted that pattern. The old way goes implementation, then discovery, then correction, then more implementation. The caucus way goes discovery, then alignment, then specification, then implementation.

The four meetings took about 3 hours total. The actual implementation (once we started) took 15 minutes for P1. Even accounting for P0 investigation time, the total time to working code was faster than "just start building" would have been.

More importantly, the confidence was higher. We weren't hoping the implementation was right. We knew it was right because we'd validated the approach from three different angles before writing a single line of production code.

## The structure

For future reference, here's the caucus structure that worked. The CXO goes first with "What does this mean?" and outputs design principles. The PPM goes second with "How do we phase this?" and outputs implementation guidance. The Architect goes third with "What pattern do we use?" and outputs technical direction. The Lead Developer goes fourth to execute, outputting decomposition and deployment.

Each agent has a distinct lens. The CXO brings user experience and design philosophy. The PPM brings product priorities and success criteria. The Architect brings technical patterns and infrastructure. The Lead Developer brings execution and coordination.

The sequence matters. Design philosophy informs product phases. Product phases inform technical patterns. Technical patterns inform execution. Reversing the order leads to solutions looking for problems.

## When to use it

The planning caucus is probably overkill for bug fixes, small features, well-understood domains, and time-sensitive work.

It's valuable for foundational infrastructure, work that will be hard to change later, domains where the team has different mental models, and anything where "getting it right" matters more than "getting it done."

The MUX object model qualified on all four counts. We'll be building on this foundation for months. A few hours of alignment now prevents weeks of rework later.

## The unspoken part

I should admit something: I was prepared to facilitate back-and-forth. Disagreements between agents. Clarification requests. Maybe even a second round of consultations.

None of that happened.

Each agent took the previous memos seriously, built on them, and added their layer. The CXO didn't contradict the existing object model work. The PPM didn't override the design philosophy. The Architect didn't ignore the product guidance.

[PM PLACEHOLDER: Your experience of the day—was there a moment where you expected friction and didn't get it?]

I don't know if that's because the structured sequence forced coherence, or because we got lucky, or because the agents are better at synthesis than I expected. But the result was a planning session that felt less like a meeting and more like a relay race—each runner handing off the baton cleanly, the final runner crossing the finish line.

---

*Next on Building Piper Morgan: The Leadership Caucus, where a disagreement between advisors became a feature, not a bug.*

*Have you ever tried sequencing specialist consultations before implementation? What order worked for you?*
