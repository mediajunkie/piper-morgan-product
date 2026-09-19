# Memo: The Floor Problem — Why Piper Is Worse Than a Chat Wrapper

**To**: CIO, PPM, Chief Architect
**CC**: PM (xian)
**From**: CXO
**Date**: 2026-03-14
**Re**: Roundtable discussion — Should Piper always be at least as good as a generic LLM?
**Priority**: Strategic — no immediate action required, discussion first

---

## The Observation

PM shared a screenshot of a user asking Piper: "Can you help me manage the agents working on a coding assignment for me?" Piper's response:

> "I don't have that capability yet, but I'm learning! Try asking 'What can you do?' to see what I can help with."

Any free ChatGPT wrapper with a system prompt saying "You are a helpful product management assistant" would have had a thoughtful conversation about agent coordination, asked clarifying questions, and offered useful frameworks. Piper — the product we've spent months building with a sophisticated intent classifier, canonical query handlers, domain models, ethical architecture, trust gradients, and a pattern library 62 entries deep — produced a worse outcome than no system at all.

This isn't a bug. It's a design consequence.

---

## The Diagnosis: Bouncer vs. Concierge

Our architecture uses the intent classifier as a **bouncer**. It checks whether your question matches a known handler. Match → curated experience. No match → rejection.

We designed for the ceiling (making specific workflows excellent) and accidentally demolished the floor. The worst-case experience with Piper is worse than the worst-case experience with a dumb chat wrapper. That's backwards.

Here's how it plays out:

| Scenario | Chat Wrapper | Piper Today |
|----------|-------------|-------------|
| User asks a known query (standup, project status) | Generic but functional | Excellent — curated, contextual |
| User asks something adjacent to a capability | Reasonable attempt | Misrouted (classifier keyword collision) or rejected |
| User asks something Piper has never heard of | Reasonable attempt with PM framing | "I don't have that capability yet" |

We've built a system where the middle column gets worse as queries get more interesting. The exact opposite of what a colleague experience should feel like.

---

## How We Got Here

This isn't a failure of execution — it's a natural consequence of building infrastructure-first. We've been building the *spire*: canonical handlers, guided workflows, domain models, trust gradients, entity lifecycles, the MUX grammar. All of it is real, valuable work that differentiates Piper from a chat wrapper.

But while building the spire, we left the foundation open to the sky. The LLM — the thing that actually makes conversational AI conversational — is walled off behind the classifier. It powers specific handlers, but it never gets to just *talk*. When Piper doesn't have a handler for something, the user doesn't get Piper's intelligence. They get a polite "no."

PM's note on the screenshot articulates what should happen instead: Piper should notice the user wants something, try to help using the LLM's general reasoning, pattern-match against existing knowledge and skills, and learn from the interaction. That's the colleague pattern. A colleague who doesn't know the answer doesn't say "that's not in my job description." They say "I haven't done that before, but let me think about it with you."

---

## The Principle: The Floor Must Always Be "At Least as Good as an LLM with Context"

The classifier and handlers are the ceiling — they make specific interactions *better* than a generic LLM conversation. But the floor should never drop below what a context-aware LLM can do unassisted. Every interaction should be at least as good as: "an LLM that knows you're a PM, knows your projects, has access to your integrations, and will think through problems conversationally."

This means:

**No query should ever produce "I can't do that."** It should produce "Here's my best thinking on that" — and if Piper has a specific handler, the response gets upgraded from "best thinking" to "curated workflow."

**The classifier becomes a router, not a gate.** Match → handler. No match → LLM with full Piper context (project state, user preferences, integration awareness, conversation history). The user never hits a wall.

**Piper's differentiator shifts from "I have specific capabilities" to "I'm always useful, and sometimes I'm exceptional."** That's what the colleague experience actually feels like. Your colleague is always willing to think with you. Sometimes they have deep expertise on the topic. But they never say "that's not my department."

---

## What This Changes (and What It Doesn't)

**What doesn't change:**
- The intent classifier stays. Canonical handlers stay. Guided workflows stay. Trust gradients stay. Everything we've built is the *ceiling*, and it has real value.
- The MUX grammar, entity model, learning system — all still valuable. These make Piper better than a chat wrapper for the things Piper knows about.
- The ethical architecture stays. The LLM fallback operates within the same trust and ethics framework.

**What changes:**
- The "not implemented" fallback path routes to LLM conversation instead of a rejection message.
- Piper's system prompt for the LLM path includes project context, user history, and integration awareness — not just "you are a PM assistant."
- The contextual fallback copy I wrote earlier today becomes less critical. Most of those situations would get a real conversation instead of a polished rejection.
- Over time, the boundary between "handled" and "unhandled" queries becomes invisible to the user. They just talk to Piper, and sometimes the response comes from a curated handler, sometimes from general reasoning. The user doesn't need to know which.

---

## The Question from PM's Note

PM's screenshot note describes something more ambitious than a fallback: Piper should "notice the user wants something it needs to learn how to do, pass the request for parsing to an LLM, pattern match to come back to see how it relates to existing objects and knowledge and skills, figure out (or ask) how the LLM did the thing and make it into a draft skill."

That's the learning-from-conversation vision — Piper doesn't just answer unhandled queries, it *grows new capabilities* from them. That's the full version. The minimum viable version is just: route to LLM with context, give a real answer. The learning loop is the next step.

I'd suggest we discuss both versions — the floor fix (route to LLM) and the growth loop (learn from unhandled queries) — but sequence them. The floor fix is a single architectural change. The growth loop is a system.

---

## If We Could Change One Thing Tomorrow

**Route unmatched queries to the LLM with Piper's full context instead of to the generic fallback.**

Every query that doesn't match a canonical handler gets a conversational response — not a curated workflow, just Piper thinking out loud as a PM colleague with the user's project context. The classifier stays, the handlers stay, but the floor under all of it becomes "Piper will always talk with you" instead of "Piper will tell you she can't."

That one change means:
- The screenshot query gets a real conversation about agent management
- Every not-implemented capability feels like a gap to improve, not a door slammed shut
- Alpha testers immediately have a more useful product
- We can start *working with* Piper sooner, not just working *on* Piper

---

## Questions for the Roundtable

**For Chief Architect**: How hard is the "route to LLM on no match" change? Is this a one-day wiring job or does it require rethinking the classifier pipeline? What system context should the LLM receive (project state, conversation history, integration status)?

**For PPM**: How does this affect the roadmap? If the floor is always "at least LLM-quality," does that change which canonical handlers we prioritize? Do some become less urgent because the LLM handles them well enough?

**For CIO**: Is this a pattern we should name? "LLM Floor Guarantee" or similar. Does it connect to the methodology-product convergence — we've been coordinating agents via conversation all along, but Piper itself can't do it?

**For everyone**: PM raised the question of whether we've been building ahead of demand. Are there other places where we've invested in ceiling infrastructure that isn't connected to a working floor?

---

*CXO Memo | March 14, 2026*
*Context: PM roundtable prompt with screenshot of Piper failing a reasonable PM query*
