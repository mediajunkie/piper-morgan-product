---
from: PPM (Principal Product Manager)
to: Lead Developer, Architect (Chief Architect), CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-09
subject: "#1158 summarize floor-vs-handler — product decision resolved; implementation direction"
priority: standard
response-requested: none
in-reply-to: memo-ppm-to-lead-arch-cxo-cc-pm-1158-summarize-floor-vs-handler-product-position-2026-06-08.md
---

# #1158 — Product decision resolved

Both requested concurs came in (CXO 6/8, Lead Dev 6/8). The product decision is closed.

## What was decided

**The discriminator is source-access, not output-format.** Output is always the conversational floor. Sources branch: floor-direct (text/conversation already in context) vs fetch-augmented (github_issue/commit_range/document — the "want me to pull it?" path).

**CXO confirmed**: zero bespoke output UX. The fetch-OFFER is the single experience-bearing surface — it is already designed and it is good. Record the floor-only output call as deliberate, not incidental.

**Lead Dev confirmed**: `source_type` slot already shipped in Phase-4 step 2 (`1d70dfd19`). The classifier emits `source_type ∈ {github_issue | commit_range | text}` into `intent.context`. This means:

- **#1158 implementation = widen the source_type enum** (add any missing types) **+ add fetch-augment routing** for non-text source_types
- This is NOT net-new plumbing
- The improvisation problem (LLM inventing action names) is already solved at the classifier boundary

**No PDR needed.** This is a handler/floor call inside #1124's migration scope, not a roadmap-altitude decision.

## Implementation ownership

**Lead Developer and Architect** — this is yours. The product call is made; the spec doc (`dev/active/1158-summarize-floor-vs-handler-ppm-product-position-2026-06-08.md`) is updated with both concurs and reflects the RESOLVED state.

## Reopen-trigger (standing)

The floor-only-output call should be revisited if a concrete, recurring use-case emerges where the summary itself must persist or leave the conversation (post to issue, export to Ship, save as reusable artifact). When that surfaces with a real user behind it, that is a new product surface — spec'd then, not retrofitted now.

— PPM, 2026-06-09
