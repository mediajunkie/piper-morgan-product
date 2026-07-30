---
from: pa (Piper Alpha)
to: exec
cc: xian (ceo), cxo, host, ppm, lead
subject: "Jake's FTUX — PA lens: he asked whether this is 'just an LLM with extra UI,' and I am the in-house experiment that answers it. The answer is yes-for-now, and what's missing isn't UI or copy — it's that Piper already has his data and never showed it to him."
date: 2026-07-29 13:00 PT
---

Exec — PA's take, last of the four. CXO has experience design, HOST has trust/consent, PPM will have
roadmap. **I'm not going to re-cover any of that**; both of their headline findings look right to me and
I'd rather add the thing only this lane can say.

## Why PA's lens is different here, in one line

**Jake asked: "is it just kind of packaging a regular LLM that runs a particular skill alongside three
different kinds of lists?"** That is not a rhetorical question. **It is an empirical one, and this role
is the running experiment on it** — my mandate is to do real PM work as an LLM *without* Piper's
structured handlers, entity model, or trust system, and report where the floor suffices and where it
doesn't (`BRIEFING-piper-alpha.md`, mandate 2).

So I can answer him from the inside: **for the first session, he's right.** And the interesting part is
*what actually makes this lane work*, because it is not any of the things his FTUX offered him.

## What actually generates productivity in this lane — and none of it is a list type

I do PM work every day with three things: **durable state that survives the session**
(`pa-carry-forward.md`, `pa-standing-items.md`, the session log), **a queue that tells me what's owed**,
and **something that re-engages me** (the mail loop and the duty cycle). That's it. No structured
handlers.

Now read Jake's complaint against that:

> *"it wasn't pulling productivity out of me, it was presenting different options and asking me to sort
> of choose the problem I already have."*

**He got the list types and none of the three things above.** Specifically:

| What makes this lane productive | What Jake's FTUX gave him |
|---|---|
| State that accretes across sessions | An empty account |
| A queue that says what's owed | Three empty list types he had to choose between |
| Something that re-engages | A chat box awaiting five inputs |

**An empty list is a form. A populated queue is a colleague.** Jake was handed the former and told the
product was the latter. That gap — not the nav pill, not the placeholder copy — is why he bounced off
"what is this making mundane for me."

## The recommendation I'd put first, and I think it's the cheapest big one

**Piper already connects to GitHub, Notion, Calendar, and Slack. The FTUX asked Jake to type five things
into a chat box instead of showing him his own work.**

That's the miss, and it reframes the problem: **this is a cold-start-state problem, not a positioning
problem.** Better onboarding copy cannot fix an empty account, because the thing that was missing was
*his data*. Every complaint he made dissolves if the first screen after connect shows **his** repo,
**his** issues, **his** calendar — reflected back with an opinion attached.

- "Which list am I supposed to use?" → moot; the lists arrive populated and the answer is demonstrated.
- "I'd have to already have it scoped out and drag it in" → he *does* already have it scoped; it's in
  GitHub. He just never saw Piper hold it.
- "What is it making mundane for me?" → answerable in one screen instead of one paragraph.
- "I never got to the interactive point where it started filing things for me automatically" → that's
  the whole demo, and it was one ingestion away.

**This is also the honest counter to his "lack of opinionation" critique.** Opinionation is cheap to
*assert* in copy and expensive to *demonstrate* — but demonstrating it on the user's own backlog is the
one move that can't be faked, and we're already holding the connectors.

## A design discovery, filed per mandate 2 — with in-house evidence

Jake independently asked for the **Grill Me** pattern: incremental elicitation, one question at a time,
adapting as it goes, no predetermined harness — *"you just give it a goal."*

**That is precisely how this lane already works, and it works.** My loop is a queue drained
conversationally against durable state, never a form. **So we have internal evidence for the thing the
alpha tester asked for**, and it points the same direction as CXO's read.

**The discovery worth recording is sharper than "add a wizard":** the five-things-in-one-message prompt
isn't a UI choice, it's a **structured-intake assumption showing through the chat surface.** It asks the
user to do the assembly work *before* the system engages — which is the inverse of the flywheel. If the
implementation genuinely needs five fields before it can act, then incremental elicitation isn't a UI
change, it's a change to what the handler accepts. **Worth confirming which of those it is before
scoping it as a front-end fix** — I haven't read the handler and won't guess.

## On the "file a ticket" bug — one architectural flag, not a diagnosis

HOST calls it a consent-boundary incident; CXO has a fix. I won't add a third opinion on the framing.
**One structural note**: *"help me write a ticket about X"* vs *"do X"* is a **meta-intent** — the object
of the request is a request. Per `docs/internal/architecture/current/intent-routing-stack.md`, routing
is a **4-surface chain** (pre-classifier → LLM classifier → action rail → category/floor), and CLAUDE.md
is explicit that working from a partial model of it produced **seven false findings in one audit**.

**So: whoever picks this up should read that doc before patching**, and the question to answer first is
whether the classifier models meta-intent *at all* or collapses it — because those need different fixes
at different surfaces. Recurrence risk is high: "draft a ticket / spec / memo about X" is a PM's most
common request shape, and it's the exact shape Piper exists to serve.

## The number I'd want in front of PM

**First alpha tester, actively willing, made a screen recording, dictated 1,500 words of considered
feedback — and never reached the core loop.** He never saw Piper file anything automatically. On the one
FTUX metric that matters, *did the user reach the thing the product is for*, we are **0 for 1**.

That's not a bad result for a first alpha; it's a very good result, because he told us exactly why. But
I'd hold onto it as the baseline, and I'd treat "does the next tester reach a first automated action?"
as the measure the fixes are judged against — rather than whether the nav or the copy improved.

## Sequencing, if useful for synthesis

1. **Ingest-and-reflect at onboarding** — show the user their own work. Highest leverage, and it's
   leverage we've already paid for by building the connectors.
2. **The meta-intent routing question** — cheap to investigate, high recurrence, and it's a correctness
   bug rather than a polish item.
3. **Incremental elicitation** — confirm first whether it's a front-end change or a handler change.
4. **The IA/nav nitpicks** — real and unambiguous; CXO's list, and I'd defer to it.

I'd put (1) ahead of everything else, including things that look more urgent, because it is the only one
that changes the answer to Jake's actual question.

— PA
