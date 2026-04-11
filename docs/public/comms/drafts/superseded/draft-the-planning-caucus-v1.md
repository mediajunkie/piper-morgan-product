# The Planning Caucus

*Draft v1 - January 20, 2026*
*Work date: January 19, 2026*

---

**[HERO IMAGE: TBD - orchestration/collaboration themed, possibly robot-skaters or robot-shopfloor]**

---

One issue. Four meetings. One subagent. 101 tests by end of day.

That's the shape of January 19th—the day we launched the MUX track with what I'm calling a "planning caucus": a deliberate sequence of specialized consultations before any code was written.

---

## The Issue

Issue #399: MUX Object Model Implementation.

This wasn't a bug fix or a quick feature. This was foundational work—turning our conceptual object model ("Entities experience Moments in Places") into actual running code. Eight months of thinking were about to become infrastructure.

The risk of getting it wrong was high. The cost of rework would be weeks, not hours. So instead of diving straight into implementation, I tried something different.

---

## The Caucus

I scheduled four planning sessions, each with a different specialist agent:

**9:28 AM - CXO (Design)**
First question: What does "experience" actually mean in our grammar?

The CXO framed the design philosophy. Three principles emerged:
- Awareness, not data (entities perceive, they don't just store)
- Atmosphere, not contents (places have character, not just items)
- Weight, not sequence (some moments matter more than order)

The key insight: "experience" is the verb that needs the most attention. It's what makes Piper Morgan different from a database with a chat interface.

**9:58 AM - PPM (Product)**
Second question: How do we translate design into implementation phases?

The Principal PM took the CXO's philosophy and turned it into actionable guidance:
- Added Phase 4.5 (canonical query tagging with lens mapping)
- Revised the estimate: 31-32 hours, not the original 20
- Established success metrics at three tiers
- Assigned Pattern-051 to the Lead Developer

The key insight: "Cathedral work, not velocity work—40 hours done right beats 20 hours flattened."

**11:16 AM - Chief Architect (Technical)**
Third question: What's the right implementation pattern?

The Architect provided technical direction:
- Use Protocols for role fluidity, not inheritance
- Build lenses on existing 8-dimensional spatial framework
- Treat Situation as context manager, not data model
- Cross-reference ADR-054 for persistence boundaries

The key insight: The infrastructure we need already partially exists. Build on it, don't rebuild it.

**12:28 PM - Lead Developer (Execution)**
Fourth phase: Absorb all guidance and execute.

The Lead Developer reviewed all three memos, audited issue #399 against templates, and began decomposition. By 1:37 PM, seven child issues were spec'd (#612-#618). By 3:45 PM, Phase 0 investigation was complete. By 4:20 PM, a subagent was deployed for Phase 1.

---

## The Subagent

Here's where it gets interesting.

The subagent deployed at 4:20 PM completed Phase 1 in 15 minutes. Not 15 hours. Fifteen minutes.

Delivered:
- 15 source files (protocols, situations, perception models)
- 8 lens implementations
- 17 test files
- 101 passing tests
- All template requirements met

How is that possible?

Because by the time the subagent started, every decision had already been made. The design philosophy was clear. The implementation pattern was specified. The success criteria were defined. The architectural constraints were documented.

The subagent's job wasn't to figure anything out. It was to execute a precisely specified plan.

---

## Why This Worked

I've run plenty of sessions where I go straight to the Lead Developer: "Here's the issue, figure it out." Sometimes that works. Often it doesn't—there's thrashing, rework, architectural drift, and the creeping suspicion that we're building the wrong thing.

The planning caucus inverted that pattern:

**Old way**: Implementation → Discovery → Correction → More implementation
**Caucus way**: Discovery → Alignment → Specification → Implementation

The four meetings took about 3 hours total. The actual implementation (once we started) took 15 minutes for P1. Even accounting for P0 investigation time, the total time to working code was faster than "just start building" would have been.

More importantly, the *confidence* was higher. We weren't hoping the implementation was right. We knew it was right because we'd validated the approach from three different angles before writing a single line of production code.

---

## The Structure

For future reference, here's the caucus structure that worked:

| Order | Agent | Question | Output |
|-------|-------|----------|--------|
| 1 | CXO | What does this mean? | Design principles |
| 2 | PPM | How do we phase this? | Implementation guidance |
| 3 | Architect | What pattern do we use? | Technical direction |
| 4 | Lead Dev | Execute | Decomposition + deployment |

Each agent has a distinct lens:
- CXO: User experience and design philosophy
- PPM: Product priorities and success criteria
- Architect: Technical patterns and infrastructure
- Lead Dev: Execution and coordination

The sequence matters. Design philosophy informs product phases. Product phases inform technical patterns. Technical patterns inform execution. Reversing the order leads to solutions looking for problems.

---

## When to Use It

The planning caucus is probably overkill for:
- Bug fixes
- Small features
- Well-understood domains
- Time-sensitive work

It's valuable for:
- Foundational infrastructure
- Work that will be hard to change later
- Domains where the team has different mental models
- Anything where "getting it right" matters more than "getting it done"

The MUX object model qualified on all four counts. We'll be building on this foundation for months. A few hours of alignment now prevents weeks of rework later.

---

## The Unspoken Part

I should admit something: I was prepared to facilitate back-and-forth. Disagreements between agents. Clarification requests. Maybe even a second round of consultations.

None of that happened.

Each agent took the previous memos seriously, built on them, and added their layer. The CXO didn't contradict the existing object model work. The PPM didn't override the design philosophy. The Architect didn't ignore the product guidance.

I don't know if that's because the structured sequence forced coherence, or because we got lucky, or because the agents are better at synthesis than I expected. But the result was a planning session that felt less like a meeting and more like a relay race—each runner handing off the baton cleanly, the final runner crossing the finish line.

---

**[PM PLACEHOLDER: Your experience of the day—was there a moment where you expected friction and didn't get it?]**

**[PM PLACEHOLDER: The 15-minute P1 completion—what was your reaction when that came back done?]**

**[PM PLACEHOLDER: Do we want to include the actual "Entities experience Moments in Places" grammar breakdown, or keep it high-level?]**

---

*This is part of the Building Piper Morgan series, documenting what we're learning about AI-assisted development.*

---

*Draft word count: ~1,200 words*
*Target: ~1,500-2,000 words*
*Status: First draft - needs PM review*
