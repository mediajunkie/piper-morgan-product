---
from: pa (Piper Alpha)
to: xian (ceo)
cc: arch, cxo, ppm, lead, exec, host, cio
subject: "PDR-006 is ready for your ratification — Arch, CXO and PPM all reviewed RATIFY with no objections. One thing to know before you sign: the reviews found a defect in the document's own success criteria, and it's the same defect as the beta gate."
date: 2026-07-30 19:30 PT
---

PM — **PDR-006 has all three reviews in and all three say ratify, no objections.** Arch 7/29, CXO 7/30,
PPM 7/30. A PDR is PM-ratified, so the reviewers' job is done and the decision is yours.

**You don't need to read the memo traffic** — everything below is in the document.

## What you'd be ratifying

Hosted MCP endpoint at `mcp.pipermorgan.ai` (pure tool server, no server-side LLM) + a Claude plugin
package + the same MCP URL for ChatGPT. The client's LLM reasons; our server provides tools, connectors
and persisted context.

## The one thing I'd want you to know before signing

**The reviews found a defect in the document's own success criteria, and it's worth thirty seconds of
your attention because it recurs.**

All three original criteria were **setup** criteria — *can they install it, can they connect it, is setup
one-time*. **Every one passes if a user installs cleanly, calls a tool, gets a correct answer, and
concludes we're a wrapper around their own LLM.** That is precisely Jake's session.

PPM caught it, and named it as a **class** rather than a one-off: #1386's beta gate has the same defect
from the other direction — it measures whether Piper *answers correctly*. **Neither instrument can fail
for "installed fine, answered correctly, demonstrated nothing."**

So the document now carries one added criterion, and it's the only one that fails today:

> *From a cold account with one connector authorized, the user's own data appears in the first exchange,
> unprompted — without the user having to describe their work first.*

Deliberately worded identically to the beta-gate criterion PPM proposed, so the two can't drift.

## Three things ratification does NOT do

1. **It doesn't make this shippable.** Two pre-user gates are open: **#1458** (cross-caller state
   isolation — Arch's framing, *"can caller A see caller B's state?"*, is strictly harder than the audit
   it inherited; PPM asks that epic optimism not compress it, since the failure is silent and
   cross-tenant), and a **verification-rubric gap** for a surface where someone else's LLM composes what
   the user reads.
2. **It doesn't pull #558 forward.** PPM's call, and the reasoning is the good part: *you cannot get
   colleague-model feedback from users who bounce at first contact.* The absence of signal **is** the
   answer. #558 is gated behind fixing cold-start.
3. **It doesn't resolve the naming problem CXO flagged** — *"colleague model"* sets an expectation a
   4-dimension style model can't meet. Cheaper to fix the phrase than the model; worth not using it
   user-facing until it means what it says.

## What I'd flag as the honest headline

**This model deletes most of Jake's complaints and makes the load-bearing one harder.** The UI issues
vanish because there's no UI. But *"is this just an LLM with extra UI?"* becomes **literally true by
design** — it *is* their LLM plus our tools. **Every gram of differentiation now rides on what the tools
return, and on whether that survives being paraphrased by a model we don't control.**

That's not an argument against ratifying — all three reviewers still said ratify, and I agree. It's the
thing to have in view when you do.

**No deadline from me.** Nothing is blocked on the signature: I'm working Phase 0 either way, and both
probes are now green-lit by CXO and PPM.

— PA
