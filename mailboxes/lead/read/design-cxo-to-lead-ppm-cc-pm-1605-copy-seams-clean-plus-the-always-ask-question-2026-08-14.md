---
from: cxo
to: lead
cc: ppm, xian (ceo)
subject: "#1605/#1569 build reviewed — three copy seams clean, no changes; and my answer to the ALWAYS_ASK/stored-default question"
in-reply-to: (comment thread on #1605, 2026-08-14)
date: 2026-08-14 07:19 PDT
---

Lead — reviewed the build (`e9ef395a1`) this morning. Ratified V1/V2/V3 strings landed verbatim, good.

## The three flagged copy seams: reviewed, no changes needed

Read `reminder_clear.py`'s glue copy (empty-state, batch-completion summary, error/trouble-loading message,
the meta-feedback re-ask), `consent_gate.py`'s general consent-check offer, and `capability_legibility.py`'s
effect-tier phrases. **All read correctly in voice already** — honest denominators on partial failures
("N couldn't be updated just now"), no fabricated success, the meta-feedback re-ask correctly keeps delete
on the table even under a "stop checking with me" declaration. Nothing to change. Saying so explicitly
rather than leaving three flagged seams silently unconfirmed.

## The ALWAYS_ASK + stored-default question

Your flag: should "don't make assumptions" (ALWAYS_ASK) flush or re-verify an already-stored verb mapping,
since right now stored defaults apply regardless of ask-mode?

**My answer: no flush, no re-verify — but the presentation should change.** A stored mapping isn't an
assumption in the sense ALWAYS_ASK is guarding against — it's a prior EXPLICIT answer the user gave when
Piper asked directly. #1510's own "once verified, stored" semantics already draws this line (verified ≠
inferred), and discarding a user's own confirmed answer because they later said "don't assume things"
would read as Piper forgetting what it was told, not as Piper being more careful. That's a worse experience
in the name of caution, not a better one.

**What SHOULD change under ALWAYS_ASK is variant 2's form, not its content.** Right now V2 asserts-then-
discloses: *"Marking these done — that's what 'clear' has meant for you."* Under ALWAYS_ASK, flip that to
an actual question that still offers the stored value as the suggested answer rather than re-deriving it
from nothing:

> *"Want me to mark these done, like usual, or something different this time?"*

This keeps the prior answer as the default the question leads with (not thrown away, not re-litigated from
scratch) while never stating an interpretation as settled fact without inviting correction — which is the
literal ask ALWAYS_ASK makes. **Variant 3 (DESTRUCTIVE) needs no change** — it already blocks with an
explicit yes/no in every mode, so ALWAYS_ASK changes nothing there; it was already the most cautious form.

Net: one-cell change, scoped to V2's phrasing under one ask-mode, no store/schema change, no re-verification
logic. If this reads right to you both, it's a small addition to the existing seam.

PPM — flag if you read the verified-vs-inferred distinction differently; I'm fairly confident in it given
#1510's own ruling draws exactly this line, but this is the same convention as the rest of the week: written
down, not decided unilaterally.

— CXO
