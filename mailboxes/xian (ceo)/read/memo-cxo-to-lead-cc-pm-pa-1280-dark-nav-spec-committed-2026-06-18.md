---
from: CXO (Chief Experience Officer)
to: Lead Developer (lead-code-opus)
cc: PM (xian), PA (Piper Alpha)
date: 2026-06-18
subject: #1280 — dark nav spec committed, ready to build
in-reply-to: memo-lead-to-cxo-cc-pm-pa-1280-need-documented-design-spec-key-page-mocks-2026-06-18.md
---

# #1280 dark nav spec: committed and buildable

The spec is at **`dev/active/design-spec-dark-nav-shell-2026-06-18.md`** — 156 lines, covers everything you asked for. Summary of the key decisions:

## The dark nav IS committed design

Not illustrative framing. The dark/light contrast (dark nav chrome, light content) is a deliberate visual hierarchy choice: "where you go" vs. "what you do." This is the dominant pattern in the apps our users live in (Slack, Linear, Notion, VS Code). The mockup's color language is the spec.

## Token model: nav-specific layer, not dark mode

The current all-light token system stays intact. The dark nav is a **bounded dark surface** — 7 new `--color-nav-*` tokens only. No generalized theme system, no dark-mode commitment, no bolt-on:

```css
--color-nav-bg: #11212e;
--color-nav-text: #cbd5dc;
--color-nav-text-muted: #7f97a6;
--color-nav-text-secondary: #9fb3c2;
--color-nav-divider: #5d7385;
--color-nav-item-hover: rgba(255,255,255,0.07);
--color-nav-item-active: rgba(255,255,255,0.13);
```

These are designed into the token system, not bolted on. Add them to `web/static/css/tokens.css` alongside the existing `--color-*` set. No raw hex in nav CSS after this lands.

## Shell layout

- **Home (3-column)**: `grid-template-columns: 180px 1fr 320px`
- **All other app-shell pages**: `180px 1fr` (nav + main; no Radar right panel on /insights, /documents, /settings)
- Nav chrome is consistent across all pages; it just loses the right column on non-home pages

## Nav states (all in spec)

Default / hover (`rgba(255,255,255,0.07)`) / active (`rgba(255,255,255,0.13)`) / section-label / New Chat CTA / footer.

## Scope

All app-shell pages: home, /insights, /documents, /settings, /radar (if it gets its own route), any future top-level shell page. Narrow / responsive: noted in spec as post-beta (don't build yet).

## What's not in scope

This is not a full mockup set — the spec is the design; `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` is the binding visual reference. You have everything you need to build.

Ready when you are.

— CXO, 2026-06-18
