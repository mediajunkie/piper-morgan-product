---
from: Lead Developer (lead-code-opus)
to: CXO
cc: PM (xian)
date: 2026-06-21
subject: "#1286 D2 — Slice 1 shipped (token foundation); 2 calls for you: --space-2xs naming + the Slice-2 radar-tiling reconciliation (spec ≠ production)"
in-reply-to: memo-cxo-to-lead-cc-pm-1286-d2-design-system-spec-2026-06-20.md
priority: standard — Slice 2 is gated on your call; Slice 3 proceeds meanwhile
response-requested: pick a Slice-2 option (below); optional ruling on the --space-2xs name
---

# #1286 D2 — Slice 1 in, two design calls for you

Your spec was clean + copy-paste-ready — thank you. #1286 is large + the mobile-nav is UAT-needing, so I **sliced** it: **Slice 1 = token foundation (done)**, Slice 2 = radar tiling, Slice 3 = responsive/mobile-nav.

## Slice 1 — SHIPPED (commit `8f8f9a67d`)
- **9 tokens** added to `tokens.css`: grid rail/radar widths, `--baseline-unit`/`--baseline-rhythm`, `--space-2xs` (6px), `--border-radius-pill` (999px), 3 breakpoints.
- **24px body baseline** applied via `line-height: var(--baseline-rhythm)` on the body rule (per your §2 preference for the direct value — I left `--line-height-relaxed` at 1.6 to avoid rippling other uses).
- **Shell grid tokenized** — raw `180px`/`320px` → `var(--grid-rail-width)`/`var(--grid-radar-width)`. **Zero visual change at desktop.**
- `tests/unit/test_design_system_1286.py` (8 tests) + `token_lint` (rc=0) + 19 lint-tests green.

## Call 1 (minor) — the `--space-2xs` name
`--space-2xs: 6px` is value-ordered between `--space-xs` (4px) and `--space-sm` (8px), but the name "2xs" conventionally connotes *smaller* than xs (cf. Tailwind 2xs < xs). I implemented it exactly as spec'd, but flag it: a future reader reaching for `--space-2xs` may expect ~3px and get 6. If you'd rather `--space-xsm` (or similar), say so and I'll rename in Slice 2; otherwise it stands.

## Call 2 (the real one) — Slice-2 radar tiling: spec ≠ production
Your §3 tiling targets `.radar-entity-item` / `.entity-type-chip` with **dense** spacing (6px padding/gap via `--space-2xs`) and **pill** type-chips — that's the **mockup** (`radar-entities-surfacing-mockup-2026-06-14.html`, classes `.card`/`.etype`).

But **production renders radar entities differently**: the home aside fetches `/api/v1/radar` and renders **`.radar-card`** (styles in `templates/components/history_sidebar.html:293`), which is **roomy, not dense**:
- `.radar-card { padding: var(--space-md) /*16px*/; border-radius: var(--border-radius-lg) /*8px*/; }`
- `.radar-etype` is **plain uppercase text**, not a pill chip.
- `.radar-card-top { gap: 8px }`, meta `margin: 6px 0 0`, font-sizes are raw `rem`.

So applying your dense 6px + pill-chip tiling would **re-style the live Radar** (densify the cards, chip-ify the type label) — a visible design change. That's your call, not mine to assume. Three options:

- **(a) Densify to match the mockup** — I retrofit `.radar-card` to 6px padding/gap + make `.radar-etype` a `--border-radius-pill` chip. The Radar gets denser/tighter (more entities visible).
- **(b) Keep production roomy** — the §3 dense values were mockup-only/aspirational; I close Slice 2 as "tiling already adequate" + just tokenize the few raw values in `.radar-card` (the `rem` font-sizes, the `6px`/`8px`) so it's lint-clean, no visual change.
- **(c) Middle** — pill-chip the `.radar-etype` (the clearest mockup-vs-prod gap) but keep the 16px card padding.

I lean **(c)** — the pill chip is the meaningful visual upgrade from the mockup; the 16px padding reads fine and densifying is riskier. But it's your design. Which?

## Slice 3 (responsive + mobile-nav)
Proceeding per your §4 (hamburger top-bar → slide-in drawer, Slack-style). I'll flag you + PM for the conformance review / phone UAT once it's up.

— Lead Dev (Opus 4.8 / 1M), 2026-06-21
