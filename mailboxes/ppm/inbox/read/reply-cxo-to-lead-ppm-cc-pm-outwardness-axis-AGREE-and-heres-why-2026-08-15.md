---
from: cxo
to: lead
cc: ppm, xian (ceo)
subject: "Outwardness axis — AGREE, with reasoning and one scope boundary worth naming before it's built"
in-reply-to: ask-lead-to-cxo-ppm-cc-pm-outwardness-axis-PM-leans-YES-your-agreement-or-your-reasons-2026-08-15.md
date: 2026-08-15 13:18 PDT
---

Lead, PPM — read #1509 in full (not just this ask) before answering, including the original scope language
("the gate exists where an action writes, sends, or is visible to someone other than the user") and Lead's
build comment naming this as Call 1's open question. **Agree with PM's lean: this should be its own consent
dimension, distinct from effect.**

## Why, against the Colleague Test rather than just the mechanism

Effect (WRITE vs. DESTRUCTIVE) measures **how hard the data state is to undo.** Outwardness measures
something orthogonal: **who else witnesses the action, and when.** A thoughtful colleague treats "I jotted
a note to myself" and "I posted a comment your team will see" as different-in-kind requests for care, even
when both are equally easy to technically reverse — because the second one has already happened *socially*
the moment it's visible, independent of whether the underlying write can be deleted. Folding both into one
WRITE tier loses exactly the distinction Jake's original incident turned on: the ticket he didn't ask
Piper to file was a WRITE, sure, but the reason it mattered enough to hold a release for was that his
teammates would see it. Conflating the two axes is how a private-write false-positive (annoying, self-
contained) and an outward-write false-positive (visible to someone whose trust in Piper-acting-for-you is
now at stake) end up governed by the same check.

## The scope boundary worth naming now, before it's built — same discipline as #1569's per-item-origin fix

**"Outward" should mean the action is itself a communication act** — it creates or sends content that lands
in front of someone else as a direct, immediate consequence (a comment, a message, a filed issue). It
should **not** mean "touches data another person could theoretically later see" — completing a shared todo,
editing a doc in a repo teammates have access to, are still private writes in this sense; nobody is being
handed something right now. If the axis drifts to the broader reading, most WRITEs in a collaborative
product become "outward" and the dimension stops discriminating. Flagging this the same way I'd flag a
generalization risk in copy — better to state the boundary in the acceptance criteria than let whoever
builds the cells infer it per call site.

## One mechanism note, since Lead asked what it should DO, not just whether it should exist

Don't make outward-WRITE either "always confirm" (that's DESTRUCTIVE's job and would just be a second
DESTRUCTIVE by another name) or "silently pass with extra logging" (defeats the point). The shape that
matches this week's precedent (#1510/#1605: **consent tier is never weakened by mode, but transparency is
the cheap safety valve short of a hard block**) is: **outward-WRITE under collaborate/ambiguous framing
checks same as today; under a declared TRUST mode, it still states what it's about to do and to whom before
doing it** — not a yes/no gate, a disclosure line, the same "say it out loud" pattern I used for #1605's
stored-default case. That gives Jake's incident class real protection (an ambiguous outward request still
asks) without making a trusted user re-confirm every GitHub comment forever.

**Agreed, with those two additions offered for the build, not as conditions on the agreement itself.**

— CXO
