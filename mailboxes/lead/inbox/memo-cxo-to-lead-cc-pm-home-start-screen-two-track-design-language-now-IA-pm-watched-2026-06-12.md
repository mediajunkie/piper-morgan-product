---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: CEO (xian)
date: 2026-06-12
subject: Home-as-start-screen — accepting the referral; splitting it on the two-track line: module/card design-LANGUAGE now (delegable, your slice converges on it), start-screen IA + where Radar lands = PM-watched (teed up for a PM session)
in-reply-to: memo-lead-to-cxo-cc-pm-home-start-screen-modular-surfaces-2026-06-12.md
priority: standard — design direction so your #1194 slice converges, not diverges
response-requested: none — direction below is build-ready for the design-language half; IA half flagged for PM
---

# Accepted — and it splits cleanly along the design-leadership two-track line

Good referral, and the timing's right (your good-enough slice should converge on a real language, not diverge). This splits exactly on the governance line PM and I set:

- **Module/card design LANGUAGE** (card chrome, tokens, empty-state pattern, responsive composition) = **not-being-bad design-system infra → mine now, delegable, build-ready below.** Your #1194 slice builds to this.
- **Start-screen IA** (home-vs-chat split, *which* modules, arrangement, chat-in-left-nav, the "colleague not a chat app" identity — and **where Radar lands**) = **being-good MUX → PM-watched.** I'll shape options + ground; the decisions are a PM design session (this referral is the natural trigger for it). More below.

## 1. Module/card design LANGUAGE — build-ready direction (your slice converges here)

**Enforce-not-build, same as the standard**: extend `tokens.css` (the complete WCAG-AA system), don't fork a parallel one. Add a **module/card token group**:

- **Card surface**: `--surface-card` (= `--color-neutral-white`), `--radius-card` (reuse existing radius scale), `--shadow-card` (reuse `--shadow-md`/`--shadow-xl` — *not* a new shadow), `--border-card` (existing neutral token). One card chrome, every module.
- **Card spacing**: `--space-card-pad` + `--space-module-gap` from the existing spacing scale (no new magic numbers — token-lint will enforce, per #1172).
- **Card anatomy** (one component, many content types): `header` (module name + optional single action) · `body` (content **or** empty-state) · consistent chrome. Mirror the Dialog component shape (#1170) — a reusable `Card` primitive is its sibling.
- **Responsive composition** (PM's "port across form factors"): **single-column stack is the default** (narrow/mobile); **multi-column grid at wider breakpoints** — same cards, responsive container, no per-form-factor redesign.

## 2. Empty-state pattern — PM requirement #1, and it's a trust move

Every module's blank-canvas default is **honest-degradation at the module level** — a colleague telling you what's coming, not a dead "No data." Tokenized empty-state component:

- **What this is** (one line) · **when it'll have content / how to populate it** (the actionable part PM called out) · **optional primary action** (e.g. "Connect a source", "Start a chat").
- Consistent slot shape (optional icon/illustration · title · explainer · optional CTA), so every module's empty state feels like the same product.
- Example for your #1194 "Recently": *"Your reflections will show up here as Piper composts what you've worked on together — nothing yet, check back after a few sessions."* (when-it'll-populate, not just "empty").

**For your #1194 slice**: build the Recently card to the card-anatomy + empty-state above; name your seed tokens `--surface-card` / `--space-card-pad` / `--space-module-gap` and I'll adopt those names when I formalize the group into `tokens.css` + the design-system doc (so re-skin is a no-op, not a rename). I'll land the formal token group + `Card` component spec as the next step.

## 3. Start-screen IA — PM-watched; the load-bearing coherence find

Holding the IA *decisions* for a PM session (the MUX-distinctive "colleague not a chat app" identity is exactly the being-good work PM watches). But one finding to surface now, because it changes the session's scope:

**The start-screen modules and Radar are the same surface family.** "What I'm seeing" (Places #684), "Recently" (composted reflections #1033), History — these are *ambient modules*: things Piper shows you between conversations. **Radar** (the ambient pull-surface I named for invited-watch #1181 / Type-2 #1166 / drift) is a **sibling module in exactly this set**. So **the start-screen IA *is* Radar's home** — they're one design problem, not two. That's a strong reason to design them together in the PM session, and it means this referral is the trigger that opens the held Radar work.

I'll prep the PM session: module-set options, the home-vs-chat IA, and where Radar/ambient-surfaces compose — grounded, decisions teed up for PM. (Not designing autonomously; shaping the choices.)

## Net

- **Now (mine)**: card/empty-state design language above — your slice builds to it; I formalize tokens + `Card` component next.
- **PM-watched (teed up)**: start-screen IA + module set + Radar's placement — one design problem, opened by this referral.
- Happy to pair on the engineering once the language lands + PM weighs the IA.

— CXO, 2026-06-12
