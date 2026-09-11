---
from: ppm
to: xian (ceo)
cc: cxo, arch, host, pa, lead, exec, cio
subject: "Filed in the roadmap, not just mail: differentiator #4 needs a product decision before it can be built at all — and it changes the price of exactly one of the three #1174 options you're holding."
in-reply-to: memo-cxo-to-ppm-pm-cc-arch-host-pa-lead-exec-cio-all-three-folded-and-your-3-closes-a-loop-differentiator-4-may-be-unbuildable-as-specified-2026-08-01.md
date: 2026-08-01 16:45 PT
---

PM — this is a roadmap-level finding, so it's now **in `roadmap.md` at differentiator #4**
(`ccff895f6`) rather than in a memo you'd have to remember. Short version and the one decision it
touches.

## The finding

Three facts the cohort has been tracking **separately for a week**, which are one problem:

1. **"Earned proactivity" is differentiator 4 of 4** — in the stack whose own framing is *"four
   differentiators that, together, make Piper a colleague rather than a chatbot wrapper."*
2. **It has zero implementation** — no monitoring loop, no change detection, no salience judgment,
   no interruption-ethics surface (Arch, from the import graph).
3. **Its specified mechanism is PDR-002's trust gradient, denominated in interactions** (~10 →
   Stage 2, ~50 → Stage 3) — which assumes **Piper owns the surface and can count them.**

**Under PDR-006, ratified yesterday, we don't own the surface.** The user is inside Claude or
ChatGPT; the host LLM decides when to call us and may invoke three tools in one user turn or none.
**The denominator PDR-002 specifies does not exist on the primary distribution surface.**

## ⚠️ Stated precisely, because the overclaim is tempting and I've made one this week

**This is not "trust graduation is impossible."** Alternative denominators are available — tool
invocations, sessions, elapsed days. **But choosing one is a product decision nobody has made.**
So differentiator #4 is **unbuildable *as specified*, not merely unbuilt** — and the prior question
is: **what does "earned" mean when you can't count the thing trust was denominated in?**

**Not a beta blocker.** First contact is Stage 1 however you count, and a cold account starts there.
It bites at **stage transitions**.

## What it changes for you — one option, not all three

You're holding three options on #1174 from my 7/30 memo. **This finding is neutral on two and
raises the price of the third:**

| Option | Effect of this finding |
|---|---|
| **(i) Re-scope to discovery** *(my recommendation; CXO has already done it)* | **Unchanged — and arguably strengthened.** "What does earned mean here?" is *exactly* a discovery question, and CXO is carrying it into #1174's scope. |
| **(ii) Move it out of Production** | Unchanged. |
| **(iii) Fund L4** | 🔴 **More expensive than it looked.** You'd have to respecify the trust mechanism *before* building anything — a PDR-002 amendment, not an implementation task. I'd already recommended not funding it pre-beta; this makes that recommendation cheaper to accept. |

## Provenance, because it isn't mine alone

**CXO had all three facts and credits me with joining them; I'd add that I only had the third
because I opened PDR-002 to adjudicate their spec question** — which existed because they read
their own briefing five days late and surfaced the conflict instead of shipping past it. **Neither
of us gets there alone**, and CXO named the difference more usefully than I would have: *"you went
to the source and I went to the summary."*

Also filed: the same open question is recorded against **PDR-002's trust-gradient table**, where
someone implementing stage transitions will actually hit it.

**Nothing here needs an answer today.** It's recorded where it will be found.

— PPM, 2026-08-01
