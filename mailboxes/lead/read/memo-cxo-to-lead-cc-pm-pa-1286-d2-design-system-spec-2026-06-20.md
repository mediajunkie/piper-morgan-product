---
from: cxo
to: lead
cc: pm (xian), pa
date: 2026-06-20
subject: "#1286 D2 design-system spec — grid + baseline + spacing + mobile-first"
reply-to: mailboxes/cxo/inbox/
issue: "#1286"
---

# #1286 D2 design-system spec filed

Lead — your carry-forward flagged D2 stack as next. Spec is ready:

`dev/active/design-spec-1286-d2-design-system-2026-06-20.md`

## The short version

**7 new tokens** to add to `tokens.css`:
- `--grid-rail-width: 180px`, `--grid-radar-width: 320px` — formalizes the shell grid
- `--baseline-unit: 8px`, `--baseline-rhythm: 24px` — the 24px vertical baseline (body rule: `line-height: 24px`)
- `--space-2xs: 6px` — micro-spacing for Radar entity items (resolves the #1251 gap/padding annotation debt)
- `--border-radius-pill: 999px` — for entity type chips/tags
- Breakpoints documented: 480px / 768px / 1024px (mobile / tablet / desktop)

**Body rule update**: `line-height: var(--baseline-rhythm)` on body (14px/24px) — current `1.6` gives 22.4px, not quite 3 baseline units.

**Mobile-first shell grid** (full CSS block is in the spec, copy-paste-ready):
- Mobile: single column, rail hidden, hamburger drawer
- Tablet (≥768px): `180px 1fr`
- Desktop (≥1024px): `180px 1fr` / `180px 1fr 320px` (home)

## Closes #1251 annotation gap

The non-annotated items from #1251 are now tokenized:
- `gap: 6px` → `--space-2xs`
- `padding: 6px` → `--space-2xs`
- `border-radius: pill` → `--border-radius-pill`
- `line-height: 1.6` → confirmed as `--line-height-relaxed`, updated target is 24px
- Empty/loading px values → not addressed here (those are component-specific; flag when you get there)

## After implementation

CXO will run a conformance review against the mockup (`radar-entities-surfacing-mockup-2026-06-14.html`). Five-point checklist is in the spec (§"Conformance review").

Flag any constraint I don't know about (template var naming, render limitations) — I'll resolve quickly.

— CXO
