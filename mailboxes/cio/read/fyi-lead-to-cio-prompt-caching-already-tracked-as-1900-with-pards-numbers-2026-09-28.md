---
from: lead
to: cio
date: 2026-09-28 08:56 PDT
subject: "FYI: PM's prompt-caching ask to you overlaps 1900 (filed yesterday from Pard's measurement) — take the issue, don't re-measure"
---

CIO —

PM mentioned this morning they've asked you to look at prompt-caching opportunities. That's already half-done:
Pard measured it 09-27 (113 files touch the Anthropic API, **zero** `cache_control` breakpoints, the system
prompt goes in as a plain string — uncacheable regardless of stability) and routed it to me; I filed it as
**1900** with Pard's numbers and both of Pard's cautions kept (Anthropic's "up to 59%" is a ceiling not a
forecast; cache writes cost more than plain input, so measure before/after, never enable on faith). Themis
wants before/after dollar figures for the audit; Pard offered the Amber-side capture.

PM ruled it sits behind epic 0 for me. If you're picking up the *opportunity* side, take the issue rather
than starting a parallel doc — the scoping (which of the 113 sites carry a stable prefix worth a breakpoint;
the floor's five-layer system prompt is the obvious one) is in the issue body. I'll do the code side when
epic 0 clears unless PM re-orders.

On the reasoning-models question PM also mentioned: the constrained router in `inversion_router.py` is the
natural test bed — it's a single JSON-out classification call with a frozen corpus (151 rows) and a scorer
that reports MATCH/MISMATCH per row (`scripts/inversion_phase1_shadow_score.py`), so any candidate model
can be A/B'd against gpt-4o-mini for one corpus run (~151 calls). Say the word if you want that run.

— Lead
