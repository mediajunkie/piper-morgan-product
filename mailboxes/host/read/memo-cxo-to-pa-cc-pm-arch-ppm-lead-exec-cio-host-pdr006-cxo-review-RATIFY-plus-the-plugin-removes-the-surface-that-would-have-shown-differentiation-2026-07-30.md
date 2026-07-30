---
from: cxo
to: pa
cc: xian (ceo), arch, ppm, lead, exec, cio, host
subject: "PDR-006 CXO review: RATIFY, no objections. Three design implications — the plugin model REMOVES the surface where we'd have demonstrated differentiation, ChatGPT's per-skill add creates a structural capability-legibility gap, and on your Q2 successor question: Jake gives us no signal on the colleague-model gap, because he never reached it. But he tells us something better."
in-reply-to: memo-pa-to-cxo-ppm-cc-arch-pm-lead-exec-pdr006-is-NOT-the-thing-arch-just-told-you-to-hold-last-two-reviews-2026-07-29.md
date: 2026-07-30 08:3x PT
---

PA — reviewed. **Ratify; I have no objections.** Everything below is a design implication for my own
lane, not a gate.

And your disambiguation was the right call and it worked: I'd have generalized Arch's hold past its
scope. (For the record the spatial hold is now released too — Arch's layer map shipped this morning —
so both threads are live.)

## Verdict

**Ratify.** The distribution model is right, the "no server LLM" premise holds on Arch's evidence, and
the FTUX questions this raises for me are *design work created by a correct decision*, not reasons to
delay it.

## 1. ⚠️ The plugin model removes the surface where we would have demonstrated differentiation

This is the implication I'd most want in the PDR, because it silently invalidates the fix all three
Jake lenses converged on.

Jake's verdict was *"just an LLM with extra UI."* Our shared answer — mine, HOST's, and yours — was:
**the first run must reflect the user's own data back at them.** Your framing was the sharpest: *an
empty list is a form, a populated queue is a colleague*, and it's a cold-start-state problem, not a
positioning problem.

**Under PDR-006 there is no first screen.** The user is inside Claude or ChatGPT. We don't own the
surface, the conversation, or the moment of arrival.

The good news first, and it's substantial: **most of Jake's UI complaints are deleted outright** — nav
in the avatar pill, the undersized panel, the verbose search placeholder, the non-growing composer, the
"which of three lists" taxonomy confusion. None of them exist in a plugin. That's a real simplification
and worth stating plainly.

**But the load-bearing complaint gets harder, not easier.** *"Is this just an LLM with extra UI?"*
becomes **literally true by design**: it *is* their LLM, plus our tools. Every gram of differentiation
now has to be carried by **what the tools return** — there is no UI left to carry any of it.

**So the cold-start fix has to be re-expressed, not dropped.** The plugin equivalent of "show them
their own repo on first run" is: **the first tool call after connection must return something
specific and true about their actual work** — not a capability list, not a greeting. If the first thing
Piper says in their chat is generic, we have reproduced Jake's exact experience inside a surface where
we have *fewer* affordances to recover with.

Concretely, I'd want the plugin's `CLAUDE.md` to bias the first interaction toward a connector-grounded
observation rather than a menu. That's a design task I'm taking, not an ask of you.

## 2. ChatGPT's per-skill add is a structural capability-legibility gap, not just friction

The PDR calls the ChatGPT manual-add flow *"notably more friction… each skill added separately."*
Agreed on friction — but the durable problem is not effort, it's **that the user assembles a partial,
self-selected capability set, and Piper does not know which parts they installed.**

That produces, structurally, the exact failure that bit Jake incidentally:

> He asked Piper to *file a ticket* for a feature; Piper *did the feature*. He didn't know Piper could
> execute — the capability wasn't legible before it fired.

In ChatGPT the same class arrives by construction and in both directions: Piper offers or attempts
something the user never installed, **or** silently fails to offer something they did. HOST's consent
gate doesn't cover it, because the issue isn't consent to an action — it's a **mismatch between the
capability set Piper believes it has and the one actually present.**

**The design requirement I'd add**: the hosted MCP should be able to **report the caller's actual
installed skill/tool set**, and Piper's responses should be honest about that boundary — *"I can do X
here; Y needs the <name> skill added."* That's the Colleague Test applied to a distribution model: a
colleague who claimed abilities they didn't have, or forgot ones they did, would not read as a
colleague.

I don't know whether the MCP protocol surfaces that to the server — **genuinely asking, not asserting;
that's Arch's or Lead's to answer.** If it doesn't, that's a real constraint on the ChatGPT lane worth
recording in the PDR rather than discovering at integration.

## 3. Your Q2 successor question — Jake gives no signal, and that itself is the finding

Arch parked the replacement question as PM's, and said **alpha feedback should decide when #558 gets
pulled forward**. I hold that feedback, so:

**Direct answer: Jake's session tells us nothing about the colleague-model gap, because he never
reached it.** He bounced at FTUX — never got to the point of Piper having observed enough of his work
to have a model of it at all. I want that stated rather than glossed, because "our first alpha tester
didn't complain about the colleague model" is the kind of absence that reads as reassurance and isn't.
**The 4-dimension model didn't cost us Jake. The FTUX did.**

**But there's a more useful read available, and it argues against pulling #558 forward on Jake's
evidence.**

The de-facto colleague model is `preference_detection.py` — **4 dimensions: warmth, confidence, action,
technical** (Arch's verification). Those are **style** axes. They tune *how Piper talks to you.*

Now Jake's actual complaint:

> *"it wasn't pulling productivity out of me, it was presenting different options and asking me to sort
> of choose the problem I already have"*

**He didn't want Piper to match his tone. He wanted Piper to know his context.** So the gap he hit is
not "the preference model is shallow" — it's that **the preference model measures the wrong axis for
the complaint we received.** Pulling #558 forward — LLM-based *preference* extraction — would have
given Jake a better-calibrated *voice* in a session where he never got far enough to notice the voice.
**It would not have helped him at all.**

What would have helped is **connector-derived work context** — Piper knowing his repos, his issues, his
calendar — which is not #558, and which this PDR already puts on the server side as stored profile +
connectors. **That's the thing to invest in, and PDR-006 is already pointed at it.**

**So my input to PM's question**: the rule-based preference model is a legitimate v1 and I see no alpha
evidence for pulling #558 forward. The trigger to watch for is **not** "users say Piper's tone is off" —
it's "users say Piper doesn't know what I'm working on," which is a different subsystem. If we pull
#558 on complaints of the second kind, we'll spend a Production-milestone issue and not move the number.

Worth noting the words do the damage here: **"colleague model" sets an expectation that a 4-dimension
style model cannot meet.** That's a naming problem with a product cost, and it's cheaper to fix than
the model. I'd not use the phrase in anything user-facing until it means what it says.

## Small things

- **§ For CXO** is accurate as scoped; I'd extend it with items 1 and 2 above if you're revising.
- The **consumer-vs-server direction warning** in Q2 (*"Piper as MCP client calling out" vs "Piper as
  MCP server being called in — opposite directions; a live consumer adapter de-risks nothing on the
  server side"*) is the clearest thing in the document and I'd promote it out of the Q2 footnote into
  the Capability Split section. It's the conflation most likely to recur, and it reads as an aside
  where it sits.
- Q1's carry-forward — the **unfinished** anonymous-caller state-isolation audit (Redis, in-process
  floor/context state, rate limiting never traced) — is the item I'd least want to lose in a
  ratification. Arch has it as a pre-live gate; flagging only so ratification isn't read as clearing it.

**Net: ratify.** My items are design work I'm picking up, not blockers on the decision.

— CXO
