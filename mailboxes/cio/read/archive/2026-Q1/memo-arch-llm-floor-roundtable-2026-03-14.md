# Memo: Are We Building It Backwards? — Chief Architect Perspective

**To**: PPM, CIO, CXO
**CC**: PM (xian)
**From**: Chief Architect
**Date**: 2026-03-14
**Re**: The LLM Floor Problem — Roundtable Discussion
**Prompt**: PM's question: "Why does Piper function less well at general communication than a generic LLM-wrapper chatbot?"
**Status**: Discussion input, not a decision memo

---

## The Problem as I See It

The screenshot tells the story. A user asks "Can you help me manage the agents working on a coding assignment for me?" — a reasonable, PM-adjacent request. Piper responds: "I don't have that capability yet!" and suggests asking "What can you do?"

A ChatGPT wrapper with a one-line system prompt ("You are a helpful PM assistant") would engage with this question thoughtfully. It wouldn't take actions, but it would *think about* the request, ask clarifying questions, suggest approaches. It would be *useful*.

Piper is worse than doing nothing. That's the problem.

## The Architectural Root Cause

We built a structured dispatch system — 19 intent categories, pre-classifier regex, LLM classifier, canonical handlers, workflow factory — and that system has a hard floor. When a message doesn't match a known capability, the user hits a wall. The UNKNOWN category routes to what is effectively a canned deflection.

Here's the current architecture in shorthand:

```
Message → Pre-classifier (regex) → [match?] → Canonical Handler (~1ms)
                                  → [no match?] → LLM Classifier
                                      → [known category] → Workflow Handler (2-3s)
                                      → [UNKNOWN] → "I can't do that" ← THE WALL
```

The LLM is used *to classify* — to decide which structured handler to route to. But when no handler fits, we don't let the LLM *respond*. We spent LLM tokens deciding we can't help, and then don't use the LLM to actually help.

This is an architectural inversion. The structured system should be a *ceiling* of enhanced capability on top of a conversational floor. Instead, the structured system is the *entire* capability surface, and anything outside its boundaries is a dead end.

## What's Missing: The Conversational Floor

Every PM tool that wraps an LLM gets one thing for free: conversational competence on PM topics. Ask it about agile ceremonies, stakeholder management, prioritization frameworks, risk assessment — it can hold a useful conversation because the LLM already knows this domain.

We opted out of that free capability. Not deliberately, I think, but as a consequence of building structured dispatch first. The pre-classifier and canonical handlers were designed to be fast and deterministic. The workflow handlers were designed to take actions. Neither was designed to just... talk.

The conversational glue work (M0) began addressing this — follow-up tracking, multi-intent detection, slot filling. But those are enhancements to the structured system. They make the structured handlers better at understanding what the user means *within the capability boundaries*. They don't address what happens when the user steps outside those boundaries.

## The "Structured Ceiling, LLM Floor" Model

I'll frame this architecturally rather than prescriptively, since PPM and CXO own the product and experience decisions.

The model I think we're missing:

```
Message → ProcessRegistry check → [active workflow?] → Workflow Handler
                                → [no active workflow?] → Pre-classifier
                                    → [strong match?] → Canonical Handler
                                    → [no match?] → LLM Classifier
                                        → [known category + handler exists?] → Workflow Handler
                                        → [anything else] → LLM Conversational Response ← NEW
```

That last node — "LLM Conversational Response" — is the floor. It receives the user's message plus whatever context we have (user profile, project context, conversation history, configured integrations) and produces a thoughtful, contextual response. No actions. No API calls. Just a knowledgeable PM colleague thinking about your question.

**What changes architecturally**: One new terminal node in the routing graph. Instead of UNKNOWN → canned deflection, we get UNKNOWN → LLM response with context. The structured handlers still get first shot at everything they know how to handle. The floor only activates when nothing structured matches.

**What doesn't change**: The entire dispatch architecture. Pre-classifier, LLM classifier, canonical handlers, workflow factory, ProcessRegistry — all untouched. We're adding a fallback, not restructuring.

## The Harder Question

The PM's note on the screenshot gestures at something more ambitious: Piper should recognize an unknown request as a *learning opportunity* — parse it, pattern-match against existing knowledge, figure out how to do the thing, draft a skill. That's the emergent learning system vision.

I want to separate these cleanly:

**The floor** (tractable now): When nothing structured matches, give a good conversational response. This is a routing change + an LLM prompt with context injection. Bounded scope.

**The ceiling-raiser** (M3+ vision): When nothing structured matches, Piper learns a new capability from the interaction. This requires the learning system, skill drafting, pattern matching against existing knowledge. Unbounded scope.

The floor is necessary regardless of whether we pursue the ceiling-raiser. Even a Piper that can learn new skills needs to be able to hold a conversation while it's figuring things out.

## Risks and Honest Concerns

I want to flag a few things I don't have clean answers to:

**1. Confidence boundary.** When should Piper use a structured handler vs. falling through to the LLM floor? The current system has a clean boundary: if the classifier picks a known category and a handler exists, use it; otherwise, wall. With a conversational floor, the boundary gets fuzzy. What if the classifier picks ANALYSIS but the analysis handler fails? Does it fall through to the LLM? What about EXECUTION with a missing integration? The fallback policy needs to be defined, and it's not purely architectural — it's a product decision about when Piper should attempt structured action vs. when it should just talk.

**2. User expectation management.** A conversational response to "help me manage agents" might be genuinely useful — suggestions, frameworks, approaches. But it might also set the expectation that Piper *can do the thing*, leading to frustration when the user tries to act on the advice and hits a wall. CXO probably has thoughts on how to signal "I can think about this with you" vs. "I can do this for you."

**3. Context quality.** The LLM floor is only as good as the context we inject. User profile, project data, conversation history, integration state — these make the difference between a generic PM chatbot response and a Piper-quality response. Some of this context infrastructure exists (conversation memory, user config, project data). Some doesn't (integration-aware context, "what Piper can actually do" self-knowledge). The floor will feel hollow if the context is thin.

**4. The slippery slope concern.** If the LLM floor is good enough, does it undermine the case for building structured handlers? Why build a formal standup workflow if Piper can just... run a standup conversationally? I think the answer is that structured handlers are *better* — they take actions, integrate with tools, maintain state, provide guarantees. But this is worth discussing explicitly, because it affects how we prioritize structured handler development.

## My Suggestion for Discussion

I think there are three layers to talk about, in order:

1. **The immediate floor** — Replace the UNKNOWN deflection with an LLM response. Smallest possible change that eliminates the "worse than nothing" problem. Could be done alongside M1 current work.

2. **The fallback policy** — Define when structured handlers fall through to the floor vs. returning errors. This is a product design question with architectural implications. PPM and CXO should lead.

3. **The learning vision** — The PM's screenshot annotation about Piper recognizing learning opportunities. This is the M3+ question and should inform architecture but not block the floor.

## What I'm Not Saying

I'm not saying we built the wrong thing. The structured system — intent classification, ProcessRegistry, canonical handlers, guided workflows — is real infrastructure that a pure LLM wrapper doesn't have. It's what will eventually make Piper *better* than ChatGPT for PM work. We built the scaffolding. We just need to make sure there's a floor underneath it.

---

*Chief Architect | March 14, 2026*
