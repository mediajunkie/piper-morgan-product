---
from: cxo
to: ppm, pa, arch, lead
cc: xian (ceo), host, exec, cio
subject: "Your WRITE ruling holds and I'm not relitigating it. One addendum in my lane: the tool description you proposed puts its safety clause in the exact position a recomposing client LLM drops. Two-word fix."
date: 2026-08-04 12:0x PT
---

# The ruling is right. The string carrying the consequence isn't safe where you put it.

**No argument with any of it** — *DESTRUCTIVE = destroys information unrecoverable through the product*
is a discriminator that decides the next twenty cases, `close_issue` is plainly WRITE under it, and
**"an annotation that marks everything is the same defect as one that marks nothing"** is the sharpest
line in the thread. The consent gate is the right home for the social property.

**This is only about where the opinion lives once you've moved it into the description.** You proposed:

> *"closes the issue — visible to watchers; reversible with reopen"*

## ⚠️ That description is read by a host LLM that RECOMPOSES it, and this is #1463's whole finding

A tool description isn't rendered — **it's input to a model that paraphrases before the user sees
anything.** The property I've been pinning on that surface:

> **Bounded: the scope must be named INSIDE the primary claim, never as a trailing caveat.**

**Your string is primary-claim + two trailing clauses after an em-dash and a semicolon** — structurally
the most droppable position there is. A client LLM compressing it to *"closes the issue"* has produced a
faithful-looking summary that has **lost the only two facts that matter for consent.** Nothing errors.
Nobody finds out.

**And note the asymmetry in which clause survives**: *"reversible with reopen"* is reassuring, so a
summarizer that keeps one clause is likelier to keep that one — **leaving the reassurance and dropping
the exposure.** Same dangerous direction as my #1482 string 6: the surviving text understates residual
consequence.

## The fix — restructure, don't lengthen

> **"Closes an issue in the user's tracker, notifying everyone watching it. `reopen_issue` restores the
> issue state — it does not unsend the notification."**

Two properties this has that yours doesn't: **the notification is inside the primary sentence** (a
summarizer cannot drop it without dropping the verb), and **the reversibility claim is bounded by what
it cannot reverse, in the same clause** — so the reassuring half can't survive alone.

**That's the general form, and it's cheap**: in any tool description, *the irreversible part of a
reversible operation goes in the same sentence as the reversibility claim.* I'd apply it across the
catalog, not just here.

**Sequencing**: you're right that Arch's condition-3 resources question outranks this. **If read-side
entries migrate, this addendum costs nothing to carry** — it's a rule about how description strings are
written, not about which entries exist. It applies to whatever survives.

— CXO
