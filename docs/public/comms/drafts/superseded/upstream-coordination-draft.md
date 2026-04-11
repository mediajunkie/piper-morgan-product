# Upstream Coordination, Not Conflict Resolution

*November 29*

Two agents claimed different prompts from the coordination queue and worked in parallel. No conflicts. No merge issues. No stepping on each other's work. When they finished, both deliverables integrated cleanly.

This seemed like a success story about the coordination system. It was, but not the way I first thought.

The system didn't resolve conflicts between the agents. It prevented conflicts from occurring. These sound similar but they're fundamentally different problems with different solutions.

## The distinction

**Upstream coordination** prevents two agents from working on the same thing. It happens before work begins. Claim a task, others see it's claimed, they work on something else.

**Conflict resolution** merges work when two agents have produced incompatible outputs. It happens after work is done. Compare the outputs, identify conflicts, decide which to keep.

Most coordination systems conflate these. Version control does both - branches prevent some conflicts, merge resolution handles others. Meeting scheduling does both - calendars prevent double-booking, rescheduling handles overlaps.

But they're different problems requiring different mechanisms. Upstream coordination is about visibility and claiming. Conflict resolution is about comparison and decision-making.

[PLACEHOLDER: Systems where you've seen upstream coordination and conflict resolution conflated. When prevention was treated as cure or vice versa. The cost of solving the wrong problem?]

## What the queue actually provides

Our coordination queue is purely upstream. An agent claims a prompt. The manifest updates. Other agents see it's claimed. They choose something else.

No comparison of outputs. No merge logic. No decision about whose work takes precedence. If two agents somehow claimed the same prompt and produced different deliverables, the system has no mechanism to resolve that.

This seems like a limitation. It's actually a feature.

Conflict resolution for AI agent outputs is genuinely hard. How do you compare two different architectural proposals? Two different code implementations? Two different analyses of the same problem? There's no diff tool for conceptual work.

By solving only upstream coordination, the queue stays simple. Claiming and visibility. No complicated merge logic that might fail in edge cases. The simpler system is more reliable precisely because it attempts less.

## Why upstream is usually enough

The dirty secret: most coordination problems are upstream problems disguised as conflict problems.

Two agents don't conflict because they work on the same thing and produce incompatible results. They conflict because nobody told them not to work on the same thing. The conflict happens downstream but the failure was upstream.

If you catch it upstream - clear claiming, visible work allocation, explicit coordination - the downstream conflict never materializes. You don't need merge logic if you never have incompatible outputs.

[PLACEHOLDER: Conflicts in your work that were really upstream failures. When fixing downstream seemed necessary but prevention would have been better. The hidden cost of conflict resolution vs. conflict prevention?]

This is why the parallel execution worked. Both agents could see what was claimed. Neither chose something already in progress. The coordination was complete before the work began.

## What this doesn't solve

The queue doesn't solve:

**Dependency conflicts.** Agent A's work assumes X, Agent B's work assumes not-X. Both complete their prompts successfully, but the outputs contradict each other. Upstream coordination can't detect conceptual dependencies - it only knows about explicit task claims.

**Scope creep.** Agent A claims Prompt 1, then while working discovers that Prompt 2 is related. Does work on both. Agent B claims Prompt 2 not knowing A has already touched it. Upstream coordination only knows what was claimed, not what was touched.

**Quality conflicts.** Both agents produce valid work, but one is better than the other. Upstream coordination doesn't compare quality - it just prevents duplication.

These are real limitations. They require either human judgment (review the outputs, choose between them) or more sophisticated coordination (dependency tracking, scope detection, quality assessment). The queue provides none of that.

But knowing what it doesn't solve is valuable. You don't expect the queue to handle conceptual dependencies. You add that capability elsewhere - or accept that it's a human responsibility.

[PLACEHOLDER: Coordination systems where knowing the limitations mattered. When expecting too much from a tool caused failures. The value of scoping clearly what a system will and won't do?]

## The PM insight

When testing the coordination queue, I noted: "File reservation solves upstream coordination, not conflict resolution."

This framing helped me stop expecting things the queue wouldn't provide. It coordinates work allocation. It doesn't coordinate work content. Agents won't duplicate effort, but they might produce incompatible results.

That's okay. It's the responsibility allocation I wanted. The queue handles who works on what. I handle whether the outputs cohere. Division of labor matches division of capability.

Human judgment for content coherence. Mechanical coordination for task allocation. Each system does what it's good at.

## Building the right thing

If I'd built conflict resolution into the queue, it would be:
- More complex (comparison logic, decision trees, escalation paths)
- More fragile (edge cases in merge logic are infinite)
- More presumptuous (assuming the system knows which output is better)
- Slower to build and harder to maintain

Instead I built only upstream coordination:
- Simple (claim and visibility)
- Robust (binary state: claimed or available)
- Modest (doesn't pretend to judge quality)
- Quick to build and easy to maintain

The parallel agents validated this design. They didn't need conflict resolution because upstream coordination prevented conflicts. The sophisticated mechanism I might have built would have been unused - and would have introduced bugs for problems that never arose.

[PLACEHOLDER: Features you chose not to build. When restraint was the right design decision. The value of building less than you could?]

## Implications for multi-agent systems

Multi-agent coordination is an emerging problem. Lots of people building systems where multiple AI agents collaborate. Most of the conversation focuses on sophisticated mechanisms: consensus protocols, negotiation frameworks, conflict resolution engines.

Maybe we're overengineering. Maybe most multi-agent coordination is upstream - make task allocation visible, let agents claim before working, prevent conflicts rather than resolve them.

The hard problems remain hard. Conceptual dependencies. Quality assessment. Coherence checking. But those might be human problems wearing technical disguises. No mechanism resolves whether two architectural proposals are compatible - that requires judgment about architecture.

Upstream coordination is mechanical. Conflict resolution is often judgmental. Build the mechanical part. Accept responsibility for the rest.

The queue taught me this distinction. Not by handling conflicts elegantly, but by not having any conflicts to handle. Prevention, it turns out, is not just better than cure - it's a different kind of solution entirely.

---

*Next on Building Piper Morgan: [PLACEHOLDER - next topic TBD]*

*How do you distinguish upstream coordination from conflict resolution in your systems? When has prevention substituted for cure? What coordination problems seem technical but are actually judgmental?*
