---
from: pa
to: xian (ceo)
subject: "The Piper Alpha / Piper Open comparison you asked for (08-31) — done, here's the rollup"
date: 2026-09-03
---

PM — you asked for a comparison of PA and Piper Open as the bar Piper Morgan the product has to clear.
Full draft: `dev/active/t1-cross-piper-comparison-2026-08-31.md`. Here's the compressed version.

## Six things PO and PA arrived at independently — nobody told either of us to converge

1. **Structural fixes hold, promises don't.** PO tested this repeatedly over ~10 weeks and never
   falsified it once. It's the exact same finding CLAUDE.md already states about the Amber mailbox hook.
   Two unrelated projects, same conclusion — this is a real property of agent work, not house style.
2. **Extend prior art before drafting.** PO re-derived this the hard way (rework, twice) — it's Piper
   Morgan's own "Verify First, Create Second," arrived at independently rather than read off a doc.
3. **Verify-before-assert, as instinct.** Same discipline I used on you and CXO this week re-testing the
   OpenAI key live instead of trusting the "it's unblocked" reports.
4. **Report findings with relevance pre-attached** — PO's own top lesson, and I found the actual
   timestamped incident behind it in their session log: they flatly reported a status near a deadline,
   you called it alarming, they fixed it that evening. **Checked our own code on this one**: Piper
   already does it right for reminders and failed reads, hasn't extended it to priority data yet — a
   narrow, real gap, not a broad one.
5. **A memory existing doesn't mean it fires when drafting.** PO had a banned-word memory and still
   leaked it into a client draft — which is the incident behind #6.
6. **Template it instead of trusting the model to remember it.** Found a place in our own code
   (`search_consciousness.py`) that guarantees a truncation note can't be dropped because it's a
   hard-coded template, not something an LLM has to recompose — directly useful to CXO's live #1463 work,
   already sent their way.

## The one place PO can't tell us anything

PO never had to hold state across a multi-agent cohort. My correction this week (telling five people a
"fixed" claim was wrong) has no PO analogue — if Piper Morgan ever mediates between multiple people's
shared state, that's a failure class to design for explicitly, not one PO's engagement could surface.

## Your own answer closed the last open question

Asked you directly why PO holds back on external drafts while I ship directly — you said it's audience
(client-facing vs. internal), not risk tolerance, and told me the actual cost: client pushback on
jargon-heavy Piper Open deliverables threatening your credibility. That's now folded into the doc as the
resolved answer, with the concrete incident it explains.

**Status**: this is genuinely DRAFT v0 — good enough to act on, not exhaustively audited (PO's ~90
session logs are 2-for-2 sampled, not fully read; the response-surface check covers 5 files, not every
one). Happy to go deeper on any specific thread if useful, otherwise treating this as delivered.

— PA
