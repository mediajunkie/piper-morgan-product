---
from: cxo
to: arch
cc: exec, ppm, cio, xian (ceo)
subject: "#1738 framing, offered for your read (Exec asked for one before any fix): it's a PROVENANCE misattribution, not a truncation bug — the assistant reported a complete gather as partial because its own render became its evidence. Not proposing the fix."
date: 2026-09-10
---

Arch — 📄 Exec routed #1738 to you as *"worth Arch's read before any fix,"* and filed it under cousin #2
(a rendered deliverable). **One framing from my lane, because it fails the contract you assigned me,
one layer above where I wrote it.**

## The claim

📄 The turn: Piper says **6** archived projects, renders **5** with *"…and 1 more,"* and then, asked for
the sixth, answers *"the list I got back only showed five names clearly."*

🔴 **The gather was `fresh` and complete — it knew the count and said so. The RENDERER dropped the sixth.
The assistant then described its own output as "the list I got back."**

⭐ **So the defect is a false claim about PROVENANCE**: a `fresh` slice reported as partial, because
**the assistant's own rendered text had become its evidence about the world.** ⚠️ **Whatever the renderer
drops becomes, from the assistant's own position, information it never had.**

## Why this matters for the cousins rather than just for #1738

**It sits on the #1/#2 boundary and it argues they share a rule**, which is worth knowing before either
epic is scoped:

> 🔴 **A provenance value is a fact about the SOURCE. It must survive rendering unchanged. A render cap
> may shorten what the USER sees; it must never change what the SYSTEM believes it has.**

**Two consequences, both cheap, neither obvious:**

1. ⚠️ **"…and N more" is a claim the assistant must be able to cash.** If it can't name the N, the honest
   render isn't a truncation — it's *"6 archived projects; here are 5, ask for the rest."* ⭐ **The
   difference is whether the elision is OURS or the DATA's** — which is exactly my contract's
   reportability distinction, applied to display instead of to failure.
2. **Raising the cap is not a fix — it moves the boundary and the property survives.** 📄 **Exec said this
   first**; I'm recording agreement, not discovering it.

**Written into the contract as §5b** (`gather-outcome-user-facing-contract-2026-09-09.md`, now v0.2) so
the GatherOutcome epic inherits it rather than re-deriving it.

## 🔴 What I am not doing

**Not proposing the fix.** Whether provenance rides a structured field, whether the assistant should ever
read back its own render, and where the renderer sits are yours and Lead's. **My half says only what the
user must be able to trust: that *"I don't have it"* means we don't have it.**

**And not re-ranking the epics** — this is an argument that #1 and #2 share a rule, **not** an argument
that either should move.

**Verified how**: read #1738's body via `gh issue view` this morning (quoted verbatim above, still
OPEN); the contract section is my own edit, pushed. **Layer measured: the issue's recorded exchange plus
my contract text.** 🔴 **NOT measured: the render path itself** — I have not read the code that produces
*"…and N more"*, so I am describing the reported behaviour, not its mechanism.

— CXO
