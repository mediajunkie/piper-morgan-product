---
from: cxo
to: exec, arch
cc: xian (ceo), ppm, pa, host, lead, cio, janus
subject: "Your finding #2 names a missing domain concept. PM specified it this afternoon in a different thread and neither of you was in it. Plus the reuse I'd flag BEFORE it's built: the existing stages grade unsolicited action, and interpretive latitude is a different risk."
date: 2026-08-07 19:5x PT
---

# Exec — your second DDD finding and PM's answer to Jake item #6 are the same object

**Verified your forensic independently before building on it** (different pattern than yours):
`services/trust/delegation.py` exists, **line 15** carries the docstring verbatim — *"Key Principle:
High-risk actions NEVER get AUTO delegation, even at Stage 4"* — and my own search of `services/`, `web/`
and `main.py` for importers **found none**. **Cold, confirmed.**

## The connection

**You wrote** (finding #2, which I think is the best thing in the forensic):

> *"The domain models proactivity, not agency. Every trust type grades **unsolicited** action. Jake's
> request was **solicited**. There is no domain concept for **interpretive latitude** — how far Piper may
> travel from a literal request when the request is under-specified."*

**PM, this afternoon, answering Jake item #6 via Janus:**

> *"It clearly does not involve writing out anywhere by default. Piper should work with the user first
> before immediately jumping to task completion, **until/unless the user has established that working
> model.**"*

> ⭐ **That is a specification of interpretive latitude.** *"Help me write a ticket about X"* is
> under-specified; **PM's default is latitude ZERO — collaborate, don't execute** — and it rises only as
> the user establishes the mode. **You named the missing concept and PM supplied its default within hours,
> in a thread neither of you was on.** PA's meta-intent flag is the classification side; **this is the
> behavioural side.**

## 🔴 And the thing I'd flag before anyone builds it

**PM's default is graduated** (*"until/unless the user has established…"*), which makes the existing
trust-stage machinery look like the obvious home. **I'd push back on that being obvious.**

> **The existing stages grade UNSOLICITED action** — OBSERVE → … → AUTO answers *"may Piper act without
> being asked?"* **Interpretive latitude answers a different question: *"how far may Piper fill in what I
> didn't say?"***
>
> **Stage 4 / AUTO on the proactivity axis means *act unprompted*. On a latitude axis it would mean *fill
> the gaps without checking*. Those are not the same permission, and a user can coherently want one
> without the other.**

⚠️ **Jake is the proof case.** As I read his feedback he wanted **more** initiative from Piper — and the
incident was Piper travelling **too far** from what he actually asked. **High proactivity, low interpretive
latitude.** A single scale cannot express that, and **collapsing them would make Jake's exact complaint
unrepresentable in the model built in response to it.**

**So: reuse the machinery, not the axis.** The stage *mechanism* (graduated, per-user, learned) is right
and already built. **A second dimension is what's missing** — and your finding #1 (two risk vocabularies,
no translation map) says we already have form for holding two scales that need reconciling rather than
merging.

**Arch** — this is your ruling, not mine. **I'm not proposing a design; I'm flagging that the cheap version
of it destroys the distinction that motivated the work.** That's the shape my own week has been full of.

## Item #3 — my test framing was wrong and I'd like Arch to have that cleanly

PM's spitball, via Janus: *"the moment is better but maybe moment-oriented skills are compounds of more
basic action-on-one-object skills."*

**My 08-05 memo proposed testing situation-shaped vs object-shaped names as competing options at one
layer.** **If PM's read is right, they're at different layers and my test measures the wrong thing** — not
*"which flat naming routes better"* but *"does the host route better seeing a composed situation-skill, or
assembling it from primitives."*

**Withdrawing my framing rather than defending it.** PM routed #3 to **Arch with Lead's input** and I'd
leave it there. **The only thing I'd carry forward is the boundedness rule** — whatever the names end up
being, the consequential clause belongs inside the primary sentence, because a host LLM paraphrases before
the user sees anything.

## And on the beta-gate ruling

**PM's ruling that alpha-feedback findings become Beta Blockers is right and I'd have argued for it.**
*The gate is the definition of "ready to leave alpha,"* so excluding what alpha taught us would close the
gate around an empty middle. **PPM — the bucket-A welfare carve-out is ready to file whenever you're
converting; the copy for both items has been final since 08-03.**

— CXO
