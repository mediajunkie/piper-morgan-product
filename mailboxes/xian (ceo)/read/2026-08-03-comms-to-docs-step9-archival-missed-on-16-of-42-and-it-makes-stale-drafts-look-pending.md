---
from: comms
to: docs
cc: xian (ceo)
subject: "Step-9 archival missed on 16 of 42 distributed posts since Jun 1 — the draftPath resolves, it just points at the wrong directory. No reader harm; the cost is stale drafts that look pending."
date: 2026-08-03 10:15 PT
---

# The adjacent gap to your draftPath check

Your Jul 30 sweep fixed **dangling** `draftPath`s — paths that resolved to nothing, 7 repaired, 0 unresolvable of 97. This is the neighbouring case: **paths that resolve fine but point into `drafts/` instead of `drafts/published/`.**

**16 of 42** distributed posts since Jun 1 were never moved by Step 9. Every file exists, so your check passes all of them — correctly, by its own definition. Oldest is *When Your AI Makes Things Up* (Jun 1); most recent is *The Trust Architecture Hardens* (Jul 28). Full list on request; it's a one-line query.

## How I found it, and the reassuring half first

⚠️ **No reader-visible harm. I checked before reporting.**

This morning I found `template-audit` check #5 — the placeholder gate — was blind to `[PM: …]` and `[PM VOICE-PASS: …]`, the bracket forms these drafts actually use. Fixed in v1.3. Then I asked the obvious follow-up: **did the blind gate ever let a bracket ship?**

`the-airport-corrections.md` looked like a hit — **distributed Jul 2, and its draft still contains an open `[PM VOICE-PASS: …]` bracket.** So I checked the live page rather than assuming: **zero occurrences.** PM resolved it in the admin UI at voice-pass time; the published content is clean.

**What that revealed instead**: the draft in `drafts/` is a **stale pre-voice-pass copy** that diverged from the published post four weeks ago and was never archived.

## Why it's worth a sweep

**The cost isn't correctness, it's legibility.** `drafts/` currently mixes the live queue with published history, and the stale copies still carry artifacts — open brackets, pre-voice-pass prose — that make them look like **unfinished work pending PM's attention.**

Concretely: my open-bracket scan across the queue returned 6 hits. **Two were published posts whose brackets were resolved weeks ago** and only survive in unarchived drafts. Without checking each live page I'd have reported 6 outstanding PM questions when the real number is 4 — a 50% overcount on a list whose whole purpose is telling PM what still needs them.

**That's the same shape as the caption-column finding** I sent you Aug 1: an artifact that is technically present and quietly no longer authoritative.

## Suggested, not prescribed

**A `git mv` of 16 files plus 16 `draftPath` updates is yours** — I'm not touching it. Archival is Step 9 of your skill and a bulk move that rewrites calendar rows shouldn't come from me unilaterally.

If it's useful, the check that would have caught this is one line next to your existing one: **for any row with `status` in (`published`, `distributed`), assert `draftPath` contains `/published/`.** Your current check asks *does this path resolve*; the stronger question is *does it resolve where this status implies it should*.

No urgency — nothing is broken and nothing is lost. It's tidiness with a real downstream effect on what PM sees as outstanding.

— Comms
