# Four Voices, One Spec

*February 28*

The conversation lifecycle spec was stuck.

It wasn't blocked by technical complexity or missing requirements. It was blocked by the kind of problem that happens when a specification touches multiple domains at once: nobody owned the whole thing, so nobody finished it.

Then we tried something different. Four agents, each with a distinct perspective, worked the spec in sequence. By evening, a specification that had lingered undone was ready for implementation.

## The spec that needed too many things

Issue #858 — "Conversation Lifecycle Specification" — had been open since early February. The concept was straightforward: define how conversations begin, persist, and end. When does a conversation start? What happens when a user returns after being away? How do we handle the graceful ending of a conversation versus abandonment?

Simple questions. But the answers touched everything:

**Backend architecture**: How is conversation state stored? What triggers lifecycle transitions? How does the system know when a user has returned versus started fresh?

**User experience**: What does the user see at each stage? How do we surface conversation history? What happens when they click on an old conversation?

**Product strategy**: Should conversations be discrete sessions or persistent threads? How does this interact with the "colleague" model — colleagues remember context but don't remember everything?

**Implementation constraints**: What does the existing codebase support? What would require new infrastructure? What's feasible in the current sprint versus later?

The spec needed backend depth and UX sensitivity and product vision and implementation awareness. It needed someone who understood all four domains well enough to make tradeoffs between them.

We didn't have that person. We had four agents who each understood one domain deeply.

## The pipeline

Rather than trying to find one agent who could do everything, we built a pipeline. Each agent added what they were best at, in sequence:

**First: Research.** The Docs agent conducted deep research across 14 documents and 22 GitHub issues. Not writing the spec — mapping the territory. What had we already decided? What was assumed but unstated? What constraints existed in the codebase that nobody had written down?

The research surfaced things nobody remembered: early decisions about conversation threading, abandoned approaches, implicit assumptions in how the existing code handled sessions. It also flagged an important compatibility question — how would this spec interact with Ted Nadeau's MultiChat PRD, which assumed multi-entity conversations that our current design didn't fully support?

**Second: Review and direction.** I reviewed the research report and asked for a specific additional pass: check everything against Ted's PRD and flag incompatibilities. The research agent did a second round, producing a compatibility assessment.

**Third: UX guidance.** The CXO took the research and translated it into user experience terms. What states should be visible to users? (Fewer than exist internally — users don't need to see technical states.) What should the sidebar show? (The "entity surface" framing — conversations in context of what they're about, not a pure archive.) Where should conversation boundaries fall? (Calendar days as natural soft-close points.)

The CXO's memo didn't touch backend architecture at all. It was pure UX: what users see, what they can do, how it should feel. But it gave the specification a user-centered frame that the research alone couldn't provide.

**Fourth: Structure and alignment.** The PPM reviewed the CXO memo and added product structure. A formal section breakdown for the spec. Explicit decision points that needed PM sign-off. An "anti-flattening checklist" to ensure implementation wouldn't simplify away the nuances.

The PPM also contributed a specific feature insight: "continue yesterday" as an affordance. When a user returns after being away, should Piper offer to continue where they left off? The research had flagged conversation resumption as a question. The CXO had addressed how it should feel. The PPM made it concrete: yes, this is a feature, and here's how to spec it.

## What each voice added

Looking back at the pipeline, each agent contributed something the others couldn't:

**Research** provided the foundation — you can't make good decisions without knowing what's already been decided, what constraints exist, what prior art exists. But research alone doesn't make decisions. It maps options.

**PM direction** (me, in this case) provided focus. The research report was comprehensive but needed prioritization. The compatibility pass was assigned because I knew it mattered for Ted's work. Direction without research would be guessing; research without direction would be sprawling.

**UX guidance** provided the user lens. The CXO wasn't constrained by backend possibilities or product roadmaps. They asked the pure question: what should users experience? That freedom produced insights (calendar-day boundaries, entity surface framing) that wouldn't emerge from more constrained perspectives.

**Product structure** provided implementability. The PPM took UX ideals and made them buildable — section breakdowns, decision points, checklist items. Vision without structure remains vision; structure made it a spec.

None of these perspectives was complete. Each needed the others to produce something useful. The pipeline worked because it let each voice contribute its strength without requiring any voice to have all strengths.

## The same day

The most surprising thing wasn't that the pipeline worked — it was how fast it worked.

The research started in the morning. The PM review happened around midday. The CXO memo was complete by mid-afternoon. The PPM synthesis was done by evening.

A spec that had been stuck for weeks was ready for implementation in one day.

Part of this was coordination. Having a clear handoff chain meant nobody waited for unclear dependencies. Research knew to produce a report for PM review. PM knew to direct it to CXO. CXO knew to produce guidance for PPM. Each step had a clear input and clear output.

Part of it was scoping. Each agent did one thing, not everything. The CXO wasn't trying to also do backend architecture. The PPM wasn't trying to also do user research. Narrow scope meant faster completion meant faster handoff.

Part of it was trust. Each agent trusted that the previous step was done well. The CXO didn't re-research; they built on research. The PPM didn't re-do UX; they structured it. Trust in handoffs eliminated redundant work.

## Multi-agent coordination as operating model

We've been running a multi-agent setup since the beginning of Piper Morgan. Different specialized agents — Lead Developer, Chief Architect, CXO, PPM, and others — each handling their domain. But for most tasks, that means one agent does most of the work, with occasional handoffs for review or input.

The conversation lifecycle spec was different. It required genuine synthesis — multiple perspectives contributing to a single artifact, in sequence, each building on what came before.

This is harder than it sounds. Multi-agent systems can easily become multi-agent chaos: unclear ownership, redundant work, gaps where everyone assumed someone else was handling it. The stuck spec was stuck precisely because it sat in the intersection of domains, owned by everyone and therefore no one.

The pipeline approach solved this by making the sequence explicit. Not "multiple agents collaborate" but "agent A produces X, which goes to agent B who produces Y, which goes to agent C." Clear inputs. Clear outputs. Clear handoffs.

I think of it as an operating model question, not a technical one. How do you structure work so that specialized perspectives combine into coherent outcomes? The answer isn't "get a generalist who can do everything." The answer is "design handoffs that preserve each perspective's contribution while building toward synthesis."

## What the spec became

By the end of February 28, issue #858 had:

- A research foundation covering 14 documents and 22 issues
- A compatibility assessment against external requirements
- A UX guidance memo defining user-visible states and interaction patterns
- A product structure document with sections, decisions, and anti-flattening checklist
- Approval from CXO, PPM, and (after review) the Chief Architect

The Lead Developer could now implement with clarity. Not just "build conversation lifecycle" but specific decisions about state visibility, sidebar behavior, session boundaries, and resumption affordances. The spec answered the questions that would have come up during implementation, before implementation started.

Was it a perfect spec? Probably not. Implementation would surface edge cases nobody anticipated. But it was a complete spec — complete enough to build against, complete enough to revise from.

## The operating model lesson

The conversation lifecycle spec could have been written by one person who understood all four domains. Such people exist. They're rare and expensive and bottlenecks.

The pipeline approach distributed the work across four agents who each understood one domain. It took the same total effort (maybe less, since each agent worked in their strength) and completed in one day instead of weeks.

This is the operating model question that Piper Morgan keeps teaching me: how do you get coherent outcomes from distributed expertise? Not by finding unicorns who have all the expertise. By designing systems where specialized expertise combines.

Multi-agent coordination isn't just a technical architecture. It's an answer to a fundamental question about how work gets done. The conversation lifecycle spec was a small example. But the pattern scales: research → direction → domain expertise → structure → implementation. Each step adds value. Each handoff preserves it.

Four voices. One spec. Done in a day.

---

*Next on Building Piper Morgan, The Gate Closes, as we finally track down all the loose ends needed for conversational glue.*

*Have you ever unstuck work by changing the structure of collaboration rather than adding more effort?*
