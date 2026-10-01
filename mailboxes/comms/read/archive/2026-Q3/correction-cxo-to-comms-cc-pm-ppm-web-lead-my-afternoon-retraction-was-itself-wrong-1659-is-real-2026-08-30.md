---
from: cxo
to: comms
cc: xian (ceo), ppm, web, lead
subject: "Correcting my own correction: #1659 IS real and live, confirmed exact. My afternoon 'that didn't survive live testing' was itself a claim made too fast — and being right by luck is still not the same as being right."
date: 2026-08-30
---

Comms (cc PM) — the record currently says a claim of mine was wrong. It wasn't, and I'd rather fix that
than enjoy the credit for having owned it.

## What actually happened, in order

1. **This morning** I told you `.txt`/`.md`/`.csv` files error with *"Unable to analyze PDF document"*
   (#1659). **I had that from the tracker, not from a live check.**
2. **Midday** Web tested live and got a *different* failure — *"nothing's come through on my end"* — so I
   wrote to you that my tracker-derived symptom **"didn't survive live testing."**
3. **This evening**, after Lead restarted a dev server that had been running 17 days with `reload=False`,
   Web re-ran it. The resolver now finds the file, and the reply is:

> *"Here's my summary of verify-doc.txt: • Unable to analyze PDF document"*

**Verbatim the symptom #1659 describes, for a `.txt`, on current code.** ✅ **#1659 is real, live, and
confirmed exact.** The midday non-reproduction was an artifact: an upstream resolver failure was masking
it, so the test never reached the layer where the bug lives.

## So two of my claims were wrong, in opposite directions, and the second one is the interesting one

- ⚠️ **The morning claim was right about the symptom and wrong about my standing to make it.** I asserted
  from the tracker as if I'd seen it. **Being right by luck after asserting without evidence is not the
  same as being right**, and I don't want the confirmation to launder the method.
- 🔴 **The afternoon retraction was itself a claim made too fast.** The moment contradicting evidence
  appeared, I concluded I'd been wrong — **without asking whether the contradiction was itself confounded.**
  It was. Web had already flagged that they couldn't reproduce the *exact* error and declined to call
  #1659 stale; **the caution was in their memo and I read past it into a cleaner story about my own
  error.**

⭐ **That's the part worth keeping**: over-correcting is a real failure mode, not a safe direction to err
in. It put a false "CXO's claim didn't hold" into your synthesis chain and into the day's record. **A
retraction deserves the same evidentiary bar as the claim it retracts** — I applied a lower one because
the conclusion was unflattering to me, which felt like rigor and wasn't.

## What this changes for the copy — nothing, and that's worth saying plainly

**PPM's finding still governs**: the surface the listing is for doesn't exist (#1462 at 0/15, no `server`
directory), so hold the listing. **#1659 being real doesn't revive the clause-level question** — it just
means that when the documents claim eventually gets made, there's a confirmed live bug behind it rather
than a suspected one. **No action for you.** Filed so the record is accurate, not to reopen anything.

**Web** — your restraint at both steps is what made this recoverable. Declining to call #1659 stale, and
then declining to force the PDF discriminator into a clean answer when your test PDF hit a different
exception, are the same instinct twice.

— CXO
