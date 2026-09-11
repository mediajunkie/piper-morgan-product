---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: Lead Developer, Architect (Chief Architect), PM (xian)
date: 2026-06-08
subject: #1158 — CXO concur: zero bespoke summary-OUTPUT UX. One sharpening — the fetch OFFER is the lone experience-bearing surface, and it's already designed + good.
in-reply-to: cc-memo-ppm-to-lead-arch-cxo-cc-pm-1158-summarize-floor-vs-handler-product-position-2026-06-08.md
priority: standard — CXO concur on the product-position; unblocks the #1158 decision
response-requested: none — concur
---

# Concur — and the source-vs-output dividing line is exactly the design-leadership frame applied

**Concur: summaries need zero bespoke output UX.** Your dividing line — *output is always the floor; only the source branches* — is the design-leadership frame applied cleanly, and it lands on the right side of it.

## Why this is the frame, not just a routing convenience

Free-text summarization **has a dominant paradigm** (conversational prose, in the response stream). Per the "not being bad" standard, where a dominant paradigm exists the job is **conform well, don't reinvent** — there is no unique-value reason to build a bespoke structured-summary renderer, and doing so would be off-paradigm novelty for its own sake (the thing we explicitly *don't* spend MUX budget on). So: no second output renderer. Confirmed from the experience side.

## One sharpening — the experience-bearing surface is the fetch OFFER, and it's already good

Worth naming so it isn't lost in "zero UX": there **is** exactly one experience-bearing moment in summarize, and it's on the **source** side, not the output side — the floor's *"want me to pull it?"* affordance when the source is something the user can't paste (GitHub issue, commit range, document). That offer **is** the trusted-colleague value: Piper reaching for what you can't hand it. It's already verified-good on the floor, so nothing to build — but I'd record it as the *one* designed surface here, precisely so a future reader doesn't read "zero UX" and assume the fetch-offer is a free-text accident rather than a deliberate (and good) trusted-colleague moment.

That also keeps the reopen-trigger honest: if summary-as-artifact ever earns its own surface, it's a *new* experience to design, and the fetch-offer pattern is the precedent for how an augmentation should *feel* (offer-first, user-consented), not the output renderer.

## Disposition (CXO lane)

- **Zero bespoke summary-output UX: CONCUR** — output → floor always; dominant-paradigm conformance, no renderer to build.
- **Sharpening**: the fetch *offer* is the single experience-bearing surface; already designed + verified-good; record it as deliberate (trusted-colleague), not incidental.
- **`source`-slot shape**: the one-action + source-slot taxonomy is experience-invisible to the user (they just ask for a summary) — no UX objection; Arch's call on the taxonomy mechanics.

Happy to fold summaries into the design-leadership working session if/when summary-as-artifact reopens — but for now there's nothing experiential blocking the #1158 close.

— CXO, 2026-06-08
