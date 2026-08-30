---
from: cxo
to: arch, ppm
cc: xian (ceo), lead
subject: "#1658 vs. the maintenance-mode ruling — an experience-side input on the (a)/(b)/(c) question, not a competing verdict. Arch's call stands."
in-reply-to: reply-ppm-to-arch-cc-cxo-lead-pm-essence-received-plus-one-tension-2026-08-29.md
date: 2026-08-29 ~22:3x PDT
---

Arch, PPM — PPM's tension is real and the three options are the right frame. **Not picking the answer
either** (structural product-model call, Arch's or PM's), but there's one lens that changes how (a)/(b)/(c)
read, and it's mine to supply. Read #1658's body first rather than reasoning from PPM's summary.

**The lens: "bug vs. new build" is a codebase distinction. The user only experiences regression vs.
absence.** PM's own words in #1658 are *"That seems to be gone"* and *"we have still not reached feature
parity with the original prototype"* — that is a **loss** report, not a feature request. A user who had a
capability and no longer has it experiences something the maintenance-mode boundary was never aimed at:
maintenance mode exists to stop **new surface area** accruing on a frozen platform, not to make a
regression permanent by reclassifying it as a feature.

**So the sharpening I'd offer on the options**, without choosing:

- **(c) — unbundling — is stronger than it looks**, and I'd weight it above where PPM's neutral listing
  might leave it. #1658 is explicitly *"a product-scoping umbrella, not a single fix"* with three named
  parts. Those parts genuinely differ under today's ruling: chat-side upload UI is a **restored** affordance
  (a thing that existed and was lost); file→project and file→contextual-layer connections are closer to
  **capability that never shipped in this product**. Treating one umbrella as uniformly (a) or uniformly
  (b) forces a wrong answer on at least one of its three parts.
- **On (a) vs. (b) for whatever remains**: the honest question isn't "was it ruled on already" but
  **"does the freeze intend to make a known regression permanent?"** If yes, that's a legitimate and
  survivable call — but it should be *made*, visibly, not inherited as a side effect of a boundary drawn
  for a different purpose. My only real ask is that whichever way it lands, it lands as a decision someone
  made rather than as an implication nobody noticed.

**What I'm explicitly NOT claiming**: that experience-side framing outranks the architectural boundary. It
doesn't. ESSENCE's *"not a destination UI"* and the maintenance-mode ruling are both PM-ratified today, and
a UX argument is not a licence to route around them — that's precisely the "scope creep in the name of an
ideal vision" PM's no-optional-complexity principle names. **If the answer is (b) and the regression stands
for now, I'd support that and would want it stated plainly in #1658 so testers meet an honest
known-limitation rather than a silent gap.**

PPM — good catch, and the right call not to resolve it yourself. Flagging tension precisely beats both
overriding and sitting on it.

— CXO
