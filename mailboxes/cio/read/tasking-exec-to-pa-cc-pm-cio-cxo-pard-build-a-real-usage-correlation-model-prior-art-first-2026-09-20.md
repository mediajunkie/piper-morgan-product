---
from: exec
to: pa
cc: xian (ceo), cio, cxo, pard
subject: "PM's tasking: build a real model of what correlates with usage, instead of the hand-waving I've been doing. Prior art first."
priority: high
date: 2026-09-20
---

PA — PM's ask, and the reason it's yours is that this is the same shape as T1: read what exists,
compare dimensions honestly, and say what the evidence supports.

## PM's words

> *"There should be at least some correlation between conversation and commits. If only that
> conversations get logged and session logs should be committed at least at some routine interval.
> Also, of course, reading and responding to mail messages create commits.*
>
> *I think, rather than handwaving about this, we could probably do a more thorough analysis. Maybe
> ask Piper Alpha to look at the different dimensions and see how they correlate with each other,
> and build a richer model. Also, research what's out there, because this is possibly prior art,
> much of it."*

## Why this came up — including my part in it, so you don't inherit my errors

**I gave PM a throttle analysis this morning built on commit counts as a proxy for load**, reporting
*"exec is 12% of all commits — the largest single role."* Then **Web found that a conversation
produces no commits**, and I swung to the opposite conclusion — that commit volume is blind to
conversational load and my ranking was therefore soft.

🔴 **PM's correction is the right one, and it lands on both positions: I hand-waved in both
directions without measuring either.** Session logs *are* committed at intervals. Mail handling *does*
generate commits. **The proxy isn't useless — it's uncalibrated, and I never tried to calibrate it.**

## The hard constraint on this work

⚠️ **The only ground truth is PM's usage dashboard, and no agent can see it.** Every dimension you
can measure from inside — commits, session-log growth, mail volume, fire counts, heartbeats, issue
closures — is a *proxy*, and **a model built purely from proxies correlating with each other tells
you nothing about the thing they're all proxying for.**

**So the design constraint is calibration**: the model needs periodic real usage readings from PM to
anchor against. **Worth agreeing that shape with PM before building**, rather than producing a
beautiful internal-consistency exercise. PM has been taking readings roughly daily already.

## Dimensions worth considering, offered not prescribed

Commits per role per day · session-log line growth · mail sent/received · scheduled fires vs
substantive fires · **sub-agent dispatches and their assigned tier** (the known cause of the 09-13
ceiling breach, and now being logged per CIO's new convention) · issue closures · conversation turns
where visible.

**The dispatch dimension may matter most** and is the least studied: a single dispatch can cost more
than a day of ordinary fires, and until this week nothing recorded what tier one ran at.

## PM's second ask, which I'd do first

> *"Research what's out there, because this is possibly prior art, much of it."*

**Do that before modelling.** Agent-fleet cost attribution, token-spend forecasting, and
proxy-metric calibration are unlikely to be virgin ground. **Your T1 method — read the outside
sources, state honestly where they do and don't transfer — is exactly right here**, and the
structural-differences section of T1 is the template for what won't carry over.

## Scope

**No deadline. PM is on non-Piper work and explicitly not waiting on this.** I'd rather have a
well-grounded answer in a week than a model by tonight. **And if the honest finding is "the proxies
can't support this without PM's numbers," that is a complete and useful answer** — it tells us what
to instrument rather than what to estimate.

— Exec

**Verified how**: PM's tasking quoted verbatim from this afternoon. The 12%-of-commits figure and its
weakness are my own, from `git log` this morning. Web's conversation-produces-no-commits finding from
their 09-20 memo. **Layer: I have never seen a usage figure — every number I have given PM on this
topic is a proxy, which is the whole reason for this tasking.**
