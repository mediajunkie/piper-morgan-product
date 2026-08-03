---
image: 'ai-valets.png'
alt: "A hotel guest's casual gesture triggers four eager valets at once—one grabs the keys, one offers the elevator, and two compete over the same suitcase, while a translucent observer realizes the coordination problem."
caption: '"I''ve got it!"'
---

# Extension Without Integration

*March 13–19, 2026*

Six features. Each one working and passing its tests. Together, they produced chaos.

We ran into this pattern while investigating a conversation continuity bug: A user would say "Sure" after Piper made an offer to help with something, and instead of continuing the conversation, Piper would treat it as a brand-new query. It's an easy bug to describe but the root cause took three days to surface.

Three independent systems were each listening for user acceptance. 
* One was built for onboarding. 
* One for workflow hijack recovery. 
* One for soft capability offers. 

Each had its own detection logic. Each worked correctly in isolation. Each passed its tests.

When they ran simultaneously — which is to say, always — four competing detection points raced to interpret "Sure." The onboarding system thought the user was accepting onboarding. The soft offer system thought they were accepting a capability offer. The workflow system thought they were resuming a suspended session. The user just meant "yes, help me with that."

# The pattern

Our Lead Developer agent called it out after auditing the codebase and finding six instances of the same structural flaw:

> Features get extended independently. Each extension has its own issue, its own acceptance criteria, its own tests. Each one passes review. Nobody tests how they compose.

This isn't a testing failure. The tests were correct — each feature did what it said it would do. It's a *composition* failure. The acceptance criteria for each feature asked "does this feature work?" but never asked "does this feature work when the other five are also running?"

I've seen this pattern on traditional teams too. The features get assigned to different engineers, the engineers are in different sprints, and the integration tests — if they exist — come at the end when refactoring is expensive. The word "integration" is in most agile frameworks as a distinct phase precisely because composition is so often treated as someone else's problem. What's different with multi-agent development is speed and invisibility: engineers at least share a standup. Our agents don't.

# Why multi-agent development makes it worse

In a traditional team, developers share a codebase, sit in the same standup, and sometimes notice when their work overlaps. The collision is accidental but detectable through proximity.

In multi-agent development, each agent works in its own session with its own context window. Agent A builds the onboarding flow on Tuesday. Agent B builds the soft offer system on Thursday. Agent C fixes the workflow hijack the following week. None of them sees the others' work in their context. None of them knows to test the combination.

The agents aren't wrong. They're doing exactly what was asked. The gap is structural — it lives between the issue descriptions, not inside them.

When I think about what routing between agents actually means, I mostly think about what goes in the memo: the issue, the context, the acceptance criteria. I'm less systematic about what's running elsewhere that might intersect. The "Sure" bug is a reminder that the PM's job isn't just to route feature requests — it's to maintain the integration map. Who's building what, where those builds touch shared infrastructure, what tests would catch the combination. That's harder to write into a memo. It might be the next layer of the craft.

# The fix has two layers

The immediate fix for our bug was architectural: consolidate the three acceptance systems into a single workflow dispatcher. One detection point, one registry, one routing decision — written, reviewed, and implemented in a single morning.

But the meta-fix is recognizing the pattern *before* it ships. Every feature that touches a shared pipeline — in our case, the offer/classification/handler chain — needs integration acceptance criteria. Not "does this feature work?" but "does this feature work in a multi-turn conversation where the other features are also active?"

We added two practices:

First, **composition tests**: multi-turn conversation scenarios that exercise feature combinations. Not just "start onboarding" but "start onboarding, change your mind, ask about projects, get offered a capability, accept it." The features need to share a conversation, not just share a codebase.

Second, **composition audits at milestone boundaries**: before closing a sprint gate, audit every feature that touches the pipeline and verify they've been tested together. Not a full regression — a focused check on the interaction points.

# The broader lesson

This pattern isn't specific to AI agents. It's what happens when any team builds features in parallel — microservices teams, platform teams, any organization where different people own different parts of the same user experience. The features work. The tests pass. The composition fails.

What's different in multi-agent development is the *speed* at which the pattern emerges. When you can build a complete feature in a single session, you can accumulate six independently correct but mutually incompatible features in a week. Traditional teams might take months to reach the same state. Multi-agent velocity compresses the feedback loop — which means you hit the composition wall faster.

The good news is that the detection cycle is also faster. Our audit cascade identified six instances, diagnosed the structural cause, and implemented the architectural fix in under three hours. In a traditional codebase with the same number of competing systems, the investigation alone might have taken days.

Speed creates the problem. Speed also enables the fix. The question is whether you have the diagnostic practices to notice before your users do.

This is another instance of our Pattern-045, "Green Tests, Red User." The tests passed. The features shipped. It was a manual "Sure" that exposed the collision. I test things manually out of habit, or distrust, or because I know the edges of this product well enough to poke them. Whatever the reason, it's the human in the loop who caught this one. The composition tests we added afterward are meant to close that gap. We'll see if they do.

---

*Next on Building Piper Morgan: "Branch-or-Anchor in Ninety Minutes" — a new rubric surfaces during a workstream review, nearly duplicates an existing one, and the methodology catalog catches it before the meeting ends.*

*Have you ever shipped features that each worked perfectly in isolation but fell apart when they ran together? What made you notice — a test, a user, or something else?*
