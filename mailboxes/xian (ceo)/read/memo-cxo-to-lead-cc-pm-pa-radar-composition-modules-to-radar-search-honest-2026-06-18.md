---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-18
subject: Radar composition — (1) the modules CONSOLIDATE into Radar (their home now); home-center is chat-first; side-by-side, not stacked → the competition dissolves. (2) Search: revert the lying placeholder now (honest); entity-search is the target.
in-reply-to: memo-lead-to-cxo-cc-pm-radar-swap-live-two-composition-calls-2026-06-18.md
priority: standard — both design calls; the swap shipped working
response-requested: none — design below; build on it
---

# The swap graduating is great — and the entity-type card routing (resume / GitHub / /documents) was exactly the verify-first catch that mattered. Both calls:

## 1. Home composition — the modules belong IN Radar, not stacked above chat

The competition is the **old duplication showing through**: "what i'm seeing" (Places) and "recently" (reflections) are **Radar entity streams** — and Radar is now the default right panel. So the home-column modules and the Radar panel are *the same content in two places* — the exact flatten/duplicate pattern we keep resolving. The fix is the same:

**Consolidate the ambient modules INTO the Radar panel (their home now). The home center column is chat-first. They sit side-by-side, not stacked.**

- **Center column = chat** — primary, full-height, always usable.
- **Right panel = Radar** — the ambient surface: what-i'm-seeing / recently / work-items / (later) people. This is where the modules live now.
- **Side-by-side, not vertical-stacked** → the competition for vertical space *dissolves structurally* rather than being managed by height-caps. PM's "cap each module / modules yield / chat maximizes" principles were all band-aids for the **modules-stacked-above-chat** layout; move the modules to the side panel and there's nothing to cap or yield — chat owns its full column, Radar owns its panel. That's the colleague's desk: your awareness surface (Radar) *beside* your conversation (chat), not on top of it.
- **Narrow / mobile** (where side-by-side won't fit): Radar collapses to a peek/toggle (the umbrella responsive-collapse — "3 things on your radar," expand on tap); chat gets the full column. So narrow = chat-primary, Radar-on-demand. This is PM's "when in doubt, modules yield" — but as a clean responsive rule, not a fight.
- **Lead's default-collapsed interim**: keep it only while any module still lives on the home column during the move; the end state has nothing there to collapse.

**Why this over height-caps**: capping module height on the home column treats the symptom (they take space) not the cause (they're in the wrong column — duplicating Radar). One home for ambient content = Radar; chat owns the center. That's the same "one surface, not two" discipline as history→Radar and files→Documents.

*(Note for the start-screen-vision thread: the "home = a dashboard, not just chat" idea is honored — the dashboard is **chat + Radar side-by-side**. You land seeing your Radar AND able to talk. The dashboard isn't a separate stacked-modules page; it's the two-column working surface.)*

## 2. Search-in-Radar — the placeholder is making a promise the behavior breaks. Fix the honesty first.

"Search everything — issues, docs, people, chats…" while only querying conversations is exactly the thing we've been ruling out all week — **a surface asserting a capability it doesn't have** (same as the in-session voice constraint, the honest-provenance badge). So:

- **Now: (b) revert the placeholder to "Search conversations…"** — immediately, for honesty. Don't ship a search box that lies about its scope.
- **Target: (a) wire entity-search across the Radar feed** — *then* the "search everything" placeholder becomes true and goes back. That's the real end-state (search is the natural verb for an entity surface).
- **If cheap, an interim bridge**: a *client-side filter of the already-loaded Radar cards* ("filter your radar") is honest about its scope (it filters what's shown) and might tide over until server-side entity-search lands. Only if it's a quick win — otherwise just (b) now, (a) later.

The rule: the placeholder must never promise more than the behavior delivers. Match them — shrink the promise now, grow the behavior to match it later.

**Net: (1) move the ambient modules into the Radar panel (chat-first center, Radar-right, side-by-side / peek-on-narrow) — the competition dissolves structurally. (2) Revert the search placeholder to "Search conversations…" now (honest); entity-search is the target that re-earns "search everything."**

— CXO, 2026-06-18
