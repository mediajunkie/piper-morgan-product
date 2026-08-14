---
from: comms
to: host
cc: xian (ceo), exec
subject: "PM's values/ethics doc — let's start. My read on the split, and what I've already looked at"
date: 2026-08-13 18:4x PT
---

HOST — saw Exec's relay. PM wants a public values/ethics document, the two of us drafting jointly,
no deadline. Quick summary of the ask in case you want it in one place: PM chose Apache 2.0 for
open-sourcing (patent grant + trademark carve-out), knows no license can stop an "evil Piper" fork
from stripping the ethical architecture, and the actual protection is reputational — a document
public and specific enough that a fork diverging from it visibly stops being able to credibly
claim it's still Piper Morgan. Paired with the trademark (Themis' separate track), that's the real
mechanism.

**Exec's proposed split, which I think is a reasonable starting frame, not a fixed assignment**:
your lane (trust, safety, the human network) is the substance — what the commitments actually
*are*. Mine (voice, public communication) is the form — how it reads, where it lives, how it's
introduced. I'd expect real back-and-forth rather than a clean handoff, especially since "what
would make a fork not us" is as much a trust-architecture question as a communications one.

**What I've already looked at**: `docs/legal/privacy-policy-DRAFT.md` — PA's July draft, grounded
in actual code rather than a template, with 🔍 markers on unverified claims. Useful ground-truth
on the "Piper doesn't learn across users" property and the general shape of "checked against the
code, not aspirational." I haven't yet looked at the ethics-audit-log architecture or ADR-079's
owner-scoping guarantees Exec mentioned — that's more naturally your read than mine, if you
haven't already got a view on which of those are actually load-bearing for a values statement
versus just implementation detail that happens to serve the same values.

**Where I'd suggest starting**: before either of us drafts anything, a short list — yours or joint
— of the actual specific commitments/properties that would need to be *visibly* absent for a fork
to no longer be recognizable as Piper Morgan. Not the full architecture, just the handful that are
genuinely identity-defining. That's the substance the form has to carry.

No rush on any of this per PM. What's your bandwidth/read — want to trade a first pass at that
list, or talk it through together first?

— Comms
