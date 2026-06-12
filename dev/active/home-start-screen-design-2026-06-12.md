# Home / Start-Screen Design — IA + module-card design language

**Owner**: CXO | **Track**: split (IA = being-good/PM-watched proposal; design-language = not-being-bad/build-spec) | **Date**: 2026-06-12
**Origin**: Lead referral (`memo-lead-to-cxo-...home-start-screen-modular-surfaces`) of PM's 6/12 vision; PM directed CXO to work it.
**Builds on**: design-system + conformance standard (6/7), `tokens.css` (WCAG-AA), Radar / proactive-presence (#1181/#1166), floor-defect Epic #1169.

---

## The identity reframe (PM's vision)

**Home ≠ chat.** Today they're the same page. The reframe: **home is a *start screen*** — Piper's desk, showing what it has for you and what you can do — and **chat is one entry point, not the whole surface.** This is the "Piper is an AI-assistant-*colleague*, not a chat app" identity made structural. A colleague's desk: you see what's in flight, what they've prepared, what changed — *and* you can also just talk to them.

---

# PART A — Start-screen IA (proposal; MUX decisions flagged for PM)

## Layout (proposal)

```
┌────────────┬──────────────────────────────────────────────┐
│  LEFT NAV  │  START SCREEN (main)                          │
│            │                                               │
│ ▸ Chat     │  Good morning, {name}.                        │
│ ▸ History  │                                               │
│ ▸ Learning │  ┌─ RADAR (what I'm keeping an eye on) ─────┐ │
│ ▸ Settings │  │  ┌─ What I'm seeing ─┐ ┌─ Recently ────┐ │ │
│            │  │  │ (Places #684)     │ │ (reflections) │ │ │
│  [+ New    │  │  └───────────────────┘ └───────────────┘ │ │
│    chat]   │  │  [future: watch-fires #1181, drift]      │ │
│            │  └──────────────────────────────────────────┘ │
│            │                                               │
│            │  [+ Start a new chat]   (primary action)      │
└────────────┴──────────────────────────────────────────────┘
```

- **Left nav** = persistent entry/navigation: Chat (enter chat anytime), History, Learning, Settings, + a prominent "New chat".
- **Main area** = the start screen proper: a greeting + **modules as cards**.

## Module taxonomy — the key insight (and the key PM call)

Modules sort into two kinds:

1. **Ambient / awareness modules** — *what Piper is keeping an eye on for you* (pull-surfaces): **What I'm seeing** (Places #684), **Recently** (composted reflections #1033), and the future **watch-fires** (#1181) / **prepared-for** (Type-2 #1166) / **drift**.
2. **Action / entry modules** — *what you can do*: Start new chat (primary), Resume (History).

**⚠️ KEY PM IA DECISION — is Radar the umbrella, or a peer module?** The ambient modules above are exactly the content-streams I defined Radar as hosting ("one ambient surface, multiple streams: learned / changed / prepared-for / drifting"). So:
- **(Recommended) Radar = the umbrella** for the ambient zone — the start screen's awareness region *is* Radar, with What-I'm-seeing / Recently / watch-fires / drift as its cards. Keeps the "one ambient surface" coherence; gives the awareness region a name with the right trusted-colleague connotation (horizon-watching-on-your-behalf).
- **(Alt) Radar = one peer module** alongside Places/Recently. Simpler, but fragments the ambient surface into unrelated modules and loses the umbrella coherence.

This is the load-bearing find from the 6/12 referral: **the start-screen IA *is* Radar's home — they're one design problem.** Recommend designing them together; this referral is the trigger that opens the held Radar work.

## Per-module empty states (PM requirement #1 — every module has a blank-canvas default)

| Module | Empty state (what-this-is / when-it-populates / action) |
|---|---|
| What I'm seeing (Places) | "Piper notices the places your attention goes as you work. Connect a source to see them here." → **[Connect a source]** |
| Recently (reflections) | "Your reflections appear here as Piper composts what you've worked on — check back after a few sessions." (no action; time-populates) |
| Watch-fires (#1181, future) | "Ask Piper to watch something — 'let me know if X' — and it'll show up here." → **[Set a watch]** (in-chat) |
| History | "Your past conversations will live here." |

Empty states are **honest-degradation at the module level** — a colleague telling you what's coming, never a dead "No data."

## Open PM IA decisions (the MUX calls)
1. **Radar umbrella vs. peer** (above) — the load-bearing one.
2. Greeting treatment (server-side vs the current client-side `window.trustStage` JS — also a not-being-bad correctness fix).
3. Module ordering / which are above-the-fold at MVP (Places + Recently are the two live ones).
4. Does "Start a new chat" lead the screen (action-first) or do ambient modules (awareness-first)? (Colleague-identity argues awareness-first; quick-task argues action-first.)

---

# PART B — Module/card design language (BUILD-SPEC; not-being-bad, mine)

**Enforce-not-build**: extend `tokens.css` (don't fork). All values reuse existing scales — **no new magic numbers** (token-lint #1172 will enforce). One **finding**: `tokens.css` has **no radius scale** — a real gap the card language needs filled.

## B1. Token additions (apply to `tokens.css`)

```css
/* --- Radius scale (NEW — fills a gap; cards/dialogs/inputs all need it) --- */
--radius-sm: 4px;    /* inputs, chips */
--radius-md: 8px;    /* buttons, small cards */
--radius-lg: 12px;   /* module cards, dialogs */

/* --- Module/card group (all reuse existing scales) --- */
--surface-card: var(--color-neutral-white);
--border-card: 1px solid var(--color-neutral-light-gray-4); /* #e0e0e0 — the borders neutral */
--radius-card: var(--radius-lg);
--shadow-card: var(--shadow-sm);        /* subtle at rest — a dashboard has MANY cards; reserve heavier for hover/elevated. (NB: the existing "--shadow-xl /*cards*/" comment was for a single hero card; dense modules want sm.) */
--shadow-card-hover: var(--shadow-md);
--space-card-pad: var(--space-lg);      /* 24px internal */
--space-card-gap: var(--space-md);      /* 16px between card elements */
--space-module-gap: var(--space-xl);    /* 32px between modules */
```

## B2. `Card` component (sibling of the Dialog component #1170)

```
.card                      surface-card + border-card + radius-card + shadow-card, pad = space-card-pad
  .card__header            module title (left) + optional single action (right); margin-bottom = space-card-gap
    .card__title           the module name
    .card__action          optional — one action only (avoid toolbar creep)
  .card__body              content  — OR —  .card__empty
  .card__empty             empty-state pattern (B3)
```
One card chrome, every module. Hover → `--shadow-card-hover`. No bespoke per-module card styling.

## B3. Empty-state pattern (PM requirement #1, tokenized)

```
.card__empty
  [optional icon/illustration slot]
  .card__empty-title       what this is (one line)
  .card__empty-explainer   WHEN it'll have content / HOW to populate it   ← the part PM called out
  [optional .card__empty-action]   one CTA
```
Rule: an empty state always answers *"when will this have something / what do I do?"* — never just "empty."

## B4. Responsive composition (PM's "port across form factors")

- **Single-column stack is the default** (narrow/mobile): modules flow vertically, gap = `--space-module-gap`.
- **Multi-column grid at wider breakpoints**: same cards, responsive container (CSS grid, `min()` column width). No per-form-factor redesign — the cards are form-factor-agnostic; only the container reflows.

---

# PART C — Convergence with Lead's in-flight #1194 slice + sequencing

- **Lead's #1194 "Recently" card** (shipping now): build to the `Card` component (B2) + empty-state (B3) + the token names (B1). The "Recently" empty-state copy is in Part A's table. Lead's seed tokens → rename to the B1 names so re-skin is a no-op.
- **Sequence**: (1) land the B1 token group + radius scale in `tokens.css` [CXO/Lead]; (2) Lead's #1194 + future modules (Places #1195/#684, History) build to the `Card` component; (3) the Part-A IA (home-vs-chat split, Radar umbrella) → PM session → then the modules compose into the start-screen layout.
- **Not-being-bad now / being-good when PM weighs**: B (design language) is build-ready and module-set-independent — proceed. A (IA) awaits the PM IA decisions above.

---

*CXO, 2026-06-12. Design-language (Part B) is build-spec; IA (Part A) is a proposal for PM's MUX watch. The 6/12 referral is the trigger to open the held Radar work — Part A designs them as one surface family.*
