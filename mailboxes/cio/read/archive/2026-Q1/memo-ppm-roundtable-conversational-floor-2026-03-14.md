# Memo: PPM Perspective — "Are We Doing It Backwards?"

**To**: CIO, Chief Architect, CXO
**From**: PPM
**Date**: 2026-03-14
**Re**: PM's roundtable question — Why is Piper worse than a generic wrapper at basic conversation?
**Context**: PM screenshot showing Piper refusing a request to help manage coding agents — a core PM task — with "I don't have that capability yet"

---

## The Problem

A user asks Piper: "Can you help me manage the agents working on a coding assignment for me?" Piper responds: "I don't have that capability yet! Try asking 'What can you do?'"

A generic ChatGPT wrapper with a one-line system prompt ("You are a helpful PM assistant") would have engaged with this request. It would have asked clarifying questions, suggested a framework, offered to brainstorm. It might not have done it brilliantly, but it would have *tried*.

Piper — the AI-powered PM assistant we've spent months building — refused to try. That's not a missing feature. That's a fundamental product failure.

---

## Why This Happens

Piper's architecture routes user messages through intent classification to structured handlers. When a message matches a handler (GitHub queries, standup, status checks), the experience can be quite good — better than a generic wrapper. When nothing matches, the user hits a wall.

This design embeds an assumption: that we can anticipate user needs in advance and build handlers for them. For a PM tool, that assumption is structurally wrong. Product management is defined by ambiguity, novel situations, and questions nobody has scripted answers for. A system that only responds to pre-anticipated queries is architecturally unsuited to its target user.

The M0 conversational glue work improved *how* Piper handles conversation flow — context persistence, multi-intent recognition, soft invocations. But it didn't address *what happens when no handler matches*. We made the routing smarter without fixing the dead end that unrouted queries reach.

---

## The Layer Inversion

I believe we have the experience layers in the wrong order. A conversational AI assistant should work like this:

**Layer 0 — Conversational floor.** The LLM engages with any PM-relevant topic using its native language capabilities, the user's context, and Piper's personality. This is the minimum viable experience. It should never be worse than a generic wrapper.

**Layer 1 — Structured handlers.** When Piper has a specific capability (GitHub integration, standup, issue triage), the structured handler provides a *better* experience than Layer 0 alone. Handlers are enhancements, not gatekeepers.

**Layer 2 — Learning and adaptation.** The gap between what users ask for (hitting Layer 0) and what Layer 1 can handle becomes the signal for what to build next. This is the emergent learning system described in PM's screenshot note.

**We built Layer 1 without Layer 0.** The structured handlers work well when they match, but the absence of a conversational floor means every miss is catastrophic — not graceful degradation, but a wall. Users who encounter the wall will not come back to discover the structured handlers.

Layer 2 (learning) is the long-term vision, and PM's screenshot note describes it well. But Layer 2 requires users to stay long enough to generate signal. Without Layer 0, they won't.

---

## What This Means for What We've Built

I want to be clear: this is not "throw it all out." The intent classification, the ethics framework, the structured handlers, the conversational glue — all of that is valuable infrastructure. The handlers are genuinely better than raw LLM conversation for the tasks they cover.

The problem is that we treated structured handling as the *only* path rather than as an *enhancement* over a conversational baseline. The fix is additive, not subtractive: add the floor beneath the structure that already exists.

This also reframes some of our architectural decisions. The spec pipeline, the ProcessRegistry, the handler system — those become the mechanism by which Piper gets *better* at specific tasks over time. But the LLM conversation is what makes Piper useful on day one, with zero configuration, for any PM question.

---

## Product Implications

**First impression.** Every new user will eventually ask something we haven't built a handler for. If Piper's response is "I can't do that," the user forms a permanent impression: Piper is limited. If Piper's response is a thoughtful attempt to help, the user forms a different impression: Piper is a capable collaborator that's getting better.

**Alpha tester retention.** Our alpha testers are sophisticated users. They'll forgive rough edges on specific features. They will not forgive an AI assistant that's less helpful than ChatGPT at basic conversation.

**The "wrapper with a prompt" comparison.** PM's framing is precise: Piper should always be *at least* as good as a ChatGPT wrapper. That's the floor, not the ceiling. Our structured handlers are the ceiling — they make Piper better than a wrapper for specific tasks. But we need the floor first.

**Learning signal.** If Layer 0 exists, every conversation where Piper engages conversationally (rather than via a handler) is a signal about what handlers to build next. Without Layer 0, those users just leave, and we never learn what they wanted.

---

## One Thing Tomorrow

**Add an LLM conversational fallback to the intent classification pipeline.**

When no structured handler matches a user's message, instead of "I don't have that capability," Piper should engage conversationally — using its underlying LLM, its PM-focused system prompt, whatever context it has about the user and their projects, and Piper's established personality and voice.

The framing should be natural, not apologetic. Not "Sorry, I can't do that, but let me try anyway." Just... help. The way a human PM colleague would if you asked them something outside their specific expertise. They'd think about it, draw on their experience, and give you their best take.

This is likely a bounded engineering task — the `_handle_generic_query` path probably exists or is close to existing. The change is making it *good* rather than making it a dead end.

If this is the right direction, it arguably should jump ahead of M1 Phase 2 epics. A conversational floor that makes Piper usable for any PM conversation is higher-impact than any individual structured handler improvement.

---

## Questions for the Roundtable

1. **For Chief Architect**: Is the `_handle_generic_query` path viable as the LLM fallback, or does the architecture require something different? What's the real engineering scope?

2. **For CXO**: How does a conversational fallback interact with Piper's personality and voice system? Does the current Piper persona work well in open-ended conversation, or does it need tuning for non-structured contexts?

3. **For CIO**: Does this reframing connect to the "Piper coordinates understanding" principle from the AX testing work? The conversational floor is arguably Piper doing coordination through dialogue rather than through structured routing.

4. **For everyone**: PM asked "are we doing it backwards?" — I've said "partly, yes, the layers are inverted." Do you agree with that framing, or is there a different diagnosis?

---

*PPM Roundtable Memo | March 14, 2026*
