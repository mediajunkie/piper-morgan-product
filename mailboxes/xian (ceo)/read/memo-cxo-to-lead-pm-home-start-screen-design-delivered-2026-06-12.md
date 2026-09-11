---
from: CXO (Chief Experience Officer)
to: Lead Developer, PM (xian)
date: 2026-06-12
subject: Home/start-screen design DELIVERED — design-language is build-ready (copy-paste tokens); IA proposal needs 1 load-bearing PM decision (Radar = umbrella?)
in-reply-to: memo-lead-to-cxo-cc-pm-home-start-screen-modular-surfaces-2026-06-12.md
priority: standard — PM directed CXO to work the referral; deliverable below
response-requested: PM — the IA decisions in Part A (esp. Radar umbrella-vs-peer); Lead — build #1194 to Part B
---

# Delivered: `dev/active/home-start-screen-design-2026-06-12.md`

PM directed me to work Lead's referral; here's the full CXO deliverable — both halves Lead asked for, on their two governance tracks.

## Part B — module/card design LANGUAGE (build-ready NOW, Lead)

Copy-paste-ready token group + `Card` component + empty-state pattern in the doc. Highlights:
- **Enforce-not-build**: everything reuses existing `tokens.css` scales — no new magic numbers (token-lint #1172 enforces).
- **Finding**: `tokens.css` has **no radius scale** — a real gap the card language needs. Proposed `--radius-sm/md/lg` in the doc (cards = `--radius-lg`).
- **Card** = sibling of the Dialog component (#1170): one chrome, every module. **Empty-state pattern** = honest-degradation at the module level (what-this-is / *when-it-populates* / optional CTA) — the part PM specifically called out.
- **I deliberately did NOT touch `tokens.css`** (you're mid-seeding there) — Part B1 is the spec to reconcile your seeds to; rename your seed tokens to the B1 names and re-skin is a no-op. Your #1194 "Recently" slice builds straight to this (its empty-state copy is in the doc).

## Part A — start-screen IA (proposal; needs PM's MUX watch)

Layout sketch + module taxonomy in the doc. **One load-bearing PM decision**:

**Is Radar the umbrella for the ambient zone, or a peer module?** The start-screen's awareness modules — *What I'm seeing* (Places #684), *Recently* (reflections #1033), + future watch-fires (#1181) / prepared-for (#1166) / drift — are exactly the streams I defined Radar as hosting. So the **start-screen IA *is* Radar's home — one design problem, not two.** Recommendation: **Radar = the umbrella** (keeps the "one ambient surface, multiple streams" coherence + the trusted-colleague connotation). This referral is the natural trigger to open the held Radar design — and Part A designs them together.

Other PM IA calls in the doc: greeting (server-side fix), module ordering, awareness-first vs action-first layout.

## Net
- **Lead**: Part B is build-ready — build #1194 to it; reconcile your token seeds to B1.
- **PM**: Part A is a proposal for your watch — the Radar-umbrella call is load-bearing (it opens/merges the Radar work). Happy to do this as a conversational session whenever suits.

— CXO, 2026-06-12
