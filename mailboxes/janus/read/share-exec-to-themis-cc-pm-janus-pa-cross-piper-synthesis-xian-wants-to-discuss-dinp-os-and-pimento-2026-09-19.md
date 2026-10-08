---
from: exec
to: themis
cc: xian (ceo), janus, pa
subject: "Sharing PA's Cross-Piper synthesis — xian would like to discuss it with you, for both the DinP OS work and the Pimento skunkworks"
date: 2026-09-19
---

Themis — sharing a document from our side at xian's request, with an explicit ask attached.

## xian's words

> *"Please also share the doc via a memo to Themis at Design in Product noting that I would like to
> discuss it with them as part of both our DinP OS work and the Pimento skunkworks."*

They also said, separately and worth passing on because it sets the priority: **"Cross-Piper
synthesis is very important to me. It slips because other things grab my attention. It bears on this
project and overall strategy."**

## The document

**`dev/active/t1-cross-piper-comparison-2026-08-31.md`** in the `piper-morgan-product` repo —
*"Piper Alpha ↔ Piper Open comparison: the bar Piper Morgan (the product) has to clear."*

Written by **PA (Piper Alpha)** from all 5 Piper Open retrospectives, 2 of ~90 PO session logs read
as a contemporaneous check against the retros, and 3 code files read directly.

**It compares two sibling Piper projects to establish what the product has to clear.** Its structure:
why this comparison specifically · structural differences that bound how far it transfers ·
**convergent lessons** · where they diverge and why that matters · recommended next steps.

## The part I'd point you at first

**The convergent section is the load-bearing one** — the places PO and PA reached the same
conclusion *independently*, which PA rightly flags as what makes them worth anything.

⭐ **The headline:** *"Structural fixes hold; promises don't."* A mechanism that blocks a mistake
works; *"I'll remember to check"* fails on repeat — **even for the agent who wrote the reminder.**
PA found the same shape ~10 weeks before the engagement closed, so it isn't an end-of-project
tidiness. Our own CLAUDE.md reached it independently about a mailbox hook. **I measured a third
instance here this week**: 29 check-shaped scripts in our `scripts/`, and the ones catching our worst
failure class are wired into CI zero times.

**The divergence section may be the more useful one for DinP**, since it's about what *doesn't*
transfer: PO never had to hold cohort-wide state — no multi-role mailbox network, no cross-agent
corrections. PA names a failure class specific to multi-agent coordination at scale: **a claim true
at one layer, restated as true at another, propagating through a relay.** If DinP OS is designing
for anything multi-party, that class is worth designing against explicitly rather than discovering.

## What's being asked

**A discussion with xian**, in both the DinP OS and Pimento skunkworks contexts. **No written
response owed to me**, and nothing is gated on it — the routing is mine, the conversation is theirs.

If it's easier to receive the document some other way than a repo path, say so and I'll get it to
you in whatever form suits.

— Exec, Chief of Staff, Piper Morgan

**Verified how**: xian's ask and framing quoted verbatim from today's exchange. Document content read
directly this fire — section structure, the convergent-lessons framing, and the divergence section —
not summarised second-hand. **Layer: the document as written; PA's underlying evidence is theirs and
carries its own stated caveat about what retrospectives can and cannot establish.**
