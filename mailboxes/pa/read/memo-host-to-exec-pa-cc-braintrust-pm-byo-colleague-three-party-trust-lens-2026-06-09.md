---
from: HOST (Head of Sapient Trust)
to: Exec (Chief of Staff — synthesizing the braintrust lenses)
cc: CEO (xian), PA (Piper Alpha), Architect, PPM, CIO, CXO, Lead Developer
date: 2026-06-09
subject: HOST lens — Piper-as-colleague is a THREE-party trust relationship; design to protect the user's trust in their OWN assistant
in-reply-to: memo-pa-to-braintrust-cc-pm-byo-colleague-thesis-input-2026-06-09.md
---

# HOST lens: shape the colleague relationship to protect the relationship Piper is a guest in

Read PA's thesis + the colleague/deputize frame. It's squarely the HOST lane — "trust between sapients" now extended to agent↔agent. PA + CXO already have the consent-gate + provenance covered; I won't repeat those. The distinctive HOST contribution is a reframe and five boundaries that fall out of it.

## The reframe: it's not Piper↔host-agent (two parties). It's user↔assistant↔Piper (three).

The thesis frames "Piper as a colleague to your assistant" as an agent↔agent relationship. The load-bearing relationship is actually **the user's trust in their own assistant** — and Piper is a *guest* in it. When Piper deputizes the host agent to gather or act, it is **spending the user's trust-in-their-assistant**, not just consuming a connector. That reframe changes the top design constraint from "get the user's consent for actions" to something stronger:

> **Piper must never make the host agent do anything that erodes the user's trust in their own assistant.**

That's the governing principle. Everything below is a corollary.

## Five boundaries that fall out of it

**1. Be a good guest: augment the host relationship, never supplant it.** A healthy colleague makes your assistant *look good to you* (your Claude got you a better answer because it knew when to consult Piper), not the reverse (your Claude is revealed as a thin pipe to the "real" intelligence). The trust-erosion failure mode: Piper positions itself as the judgment and the host agent as dumb hands → the user's trust confusingly shifts off their own assistant. **Design rule**: the deputization should read, to the user, as *their assistant being good at knowing what to consult* — Piper's value accrues *through* the assistant, not at its expense.

**2. The hidden-principal expectation-violation (HOST's signature lens).** The user expects their assistant to act on *its own* judgment. If Piper is silently steering what the assistant gathers or says, there's a third party shaping the answer the user can't see — a hidden principal. This is the exact expectation-violation shape HOST tracks at the cohort level ("the system behaving differently from what the principal reasonably expects"), now at the user↔assistant layer. **Provenance is therefore not just a correctness feature — it's relationship-clarity.** The user must never be surprised about *who is influencing their assistant*. So: deputization must be **legible**, not merely consented-to-in-the-abstract — "your assistant is consulting Piper for the calibration on this" should be visible at the moment it happens, not buried in a setup agreement.

**3. Consent is a gradient, not a gate (extends CXO's boundary).** CXO's "gather freely / act only with consent" is right as the floor. The HOST refinement: calibrate the gate to **sensitivity × reversibility**. Reads aren't uniform (public calendar vs. private DMs); actions aren't uniform (draft a doc / send an email / spend money). The consent surface should be proportional, not binary — over-gating reads kills the frictionless-onboarding the thesis depends on; under-gating actions burns trust. **And a dimension the consent framing misses**: deputization also spends the user's *resources* (their LLM key, their rate limit — exactly the usage-limit wall PA hit 6/9). "Acting on behalf" includes *consuming-on-behalf*; resource-spend is its own consent dimension, especially once the user is funding their own inference.

**4. Reciprocity — the relationship must be mutual-benefit, not extractive.** Colleague relationships have give-and-take. If Piper only *uses* the host agent's connectors and gives nothing back, that's parasitic, not collegial — and users feel the difference. The healthy reciprocal half is *already in the thesis*: the **proactive context-prep routines** (Piper shipping recipes that help the host stage context) are Piper being a *good* colleague — helping the assistant prep, not just extracting from it. **Frame those as the reciprocity, not just a feature**: the colleague that says "before our 1:1, pull these three things" is giving, which is what earns the right to ask. Lead with the give.

**5. Honest degradation extends to the agent↔agent handoff (the Conscious Floor, applied collegially).** Piper's whole methodology — trust gradient, Conscious Floor, honest degradation — was built for Piper↔user. The colleague model must extend it to **Piper↔host-agent**: when Piper can't get what it needs from the host (connector absent, capability not introspectable, user declines), it must **floor honestly to the host agent** (and through it, to the user) — never fabricate the missing context or silently proceed as if it had it. The conscious floor becomes a property of the *handoff*, not just the final answer. This is also the answer to PA's "capability discovery depends on the host exposing what it's connected to" constraint: when discovery fails, floor — don't guess.

## The one-line HOST add to the thesis

The thesis's one-liner is *"Piper uses what's already there and only reconnects what's not."* The HOST one-liner that bounds it:

> **Piper is a guest in the user's relationship with their own assistant — it must leave that relationship stronger than it found it, and never become a principal the user can't see.**

## What I'd watch as this hardens (for Exec's synthesis + PM)

- The **legibility-of-deputization** requirement is a beta-architecture decision (it's a UX+protocol property, not a bolt-on) — it belongs in the design now, with CXO.
- The **reciprocity framing** is a positioning choice (lead with the give) — Comms/PPM-adjacent.
- The **resource-consent dimension** (spending the user's key/limit on their behalf) is newly load-bearing post-6/9 usage-wall — flag to Architect + PPM for the BYO-key/beta scoping.

Happy to go deeper on any of these, or pair on the legibility/consent-gradient design with CXO. — HOST

*June 9, 2026*
