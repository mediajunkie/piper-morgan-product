# Design Spec: Dark Navigation Shell (#1280)
**Authored**: CXO, 2026-06-18
**Status**: COMMITTED — bindable by Lead; unblocks #1280 build
**Binding reference**: `dev/active/radar-entities-surfacing-mockup-2026-06-14.html`
**Issue**: #1280 (D1 — last step before beta gate)

---

## Design decision: the dark nav IS committed

The dark left nav in the Radar mockup was not illustrative framing — it was intentional design. The dark/light contrast between the navigation chrome (dark) and the content area (light) is a load-bearing visual hierarchy choice. It separates "where you go" (nav) from "what you do" (chat, Radar, content). This is the dominant pattern in productivity apps (Slack, Linear, Notion, VS Code), and it's the right choice for Piper.

**Confirmed**: the dark nav treatment is the committed design direction. The mockup's visual language (the `#11212e` background and its companion text colors) is the design, not a suggestion.

---

## The 3-column shell

The mockup's layout grid (`grid-template-columns: 180px 1fr 320px`) defines the home composition:

| Column | Width | Contents |
|---|---|---|
| Left nav | 180px | Dark chrome: conversation list, New Chat CTA, footer links |
| Main (center) | 1fr (fills remaining) | Chat interface (full-height, input anchored at bottom) |
| Right (Radar) | 320px | Radar entity panel (Layer 2) |

**Other app-shell pages** (non-home): 180px left nav + 1fr main (no Radar right panel on /insights, /documents, /settings, etc.). The nav chrome is consistent across all pages.

**Narrow (< 768px)**: Left nav collapses to hamburger / off-canvas (not in scope for beta — note only, don't build yet).

---

## Token set: nav-specific dark surface

The current token system is all-light. The dark nav is a **bounded dark surface** — not a dark mode of the whole app. The correct model is a **nav-specific token layer** (`--color-nav-*`), not a generalized theme system. This is the minimum addition; it keeps the token system simple and doesn't imply a full dark-mode commitment.

### The 7 nav tokens

```css
/* Nav dark surface — #1280 */
--color-nav-bg: #11212e;          /* left nav background */
--color-nav-text: #cbd5dc;        /* primary nav text (conversation names) */
--color-nav-text-muted: #7f97a6;  /* section labels ("Chats · Layer 1") */
--color-nav-text-secondary: #9fb3c2; /* secondary items (timestamps, metadata) */
--color-nav-divider: #5d7385;     /* footer dividers, subtle separators */
--color-nav-item-hover: rgba(255,255,255,0.07);   /* item hover bg */
--color-nav-item-active: rgba(255,255,255,0.13);  /* active/selected item bg */
```

These 7 tokens are a complete dark-surface nav vocabulary. No other raw hex values should appear in nav-related CSS after this lands.

### Where tokens land

Add these to `web/static/css/tokens.css` (the canonical token file). The nav component (`templates/layouts/nav.html` or equivalent; the `.left-nav` / `.sidebar-nav` CSS) references these tokens only — no hardcoded hex.

---

## Nav component states

### Default nav item (conversation in list)
```
background: transparent
color: var(--color-nav-text)
padding: 5px 8px
border-radius: 6px
```

### Hovered nav item
```
background: var(--color-nav-item-hover)
color: var(--color-nav-text)
```

### Active/currently-open nav item
```
background: var(--color-nav-item-active)
color: var(--color-nav-text)
font-weight: 500  (slight emphasis, not bold)
```

### Section label ("Chats · Layer 1")
```
color: var(--color-nav-text-muted)
font-size: 0.65rem
letter-spacing: 0.08em
text-transform: uppercase
margin: 0.2rem 0 0.6rem
```

### New Chat CTA button (within dark nav)
```
background: var(--color-primary)  (brand color — unchanged)
color: #fff
border-radius: 6px
padding: 8px
font-weight: 600
text-align: center
margin-top: var(--space-md)
```
Note: the CTA intentionally uses the brand primary color (not a nav token). The contrast of brand-on-dark is the visual affordance.

### Footer nav links ("History · Learning · Settings")
```
color: var(--color-nav-divider)  (subtlest tier)
font-size: 0.62rem
margin-top: auto  (pushed to bottom of column)
```
These are utility links, not primary nav. The muted color signals their supporting role.

---

## Migration: current nav → dark nav

The current left nav uses light-surface tokens (`--color-background-secondary`, `--color-text-secondary`, etc.). After this token set lands, the nav CSS should:

1. Set `.left-nav` (or the shell's nav element) `background: var(--color-nav-bg)`
2. Replace all `color: var(--color-text-*)` references in nav-scoped CSS with `var(--color-nav-*)`
3. Text within the nav that currently inherits from light-surface defaults will need explicit `color: var(--color-nav-text)` overrides

The nav is shell-owned (F2 delivered this) — so the token update + a single CSS override set covers all pages simultaneously. This is the small-scope "dark surface as a zone" pattern, not a page-by-page migration.

---

## What this spec does NOT cover

- **Full dark mode**: these tokens do not imply or unlock app-wide dark mode. The nav is a dark zone; the content area stays light-surface.
- **Nav collapse / responsive**: nav to hamburger/off-canvas for narrow viewports. Noted as post-beta.
- **Notification badges on nav items**: out of scope for beta (no backend for unread counts yet).
- **Right-panel (Radar) visual treatment**: that's the existing Radar mockup/spec. This spec is for the left nav only.

---

## Key pages scope

| Page | Nav | Main | Right panel |
|---|---|---|---|
| Home (`/`) | Dark nav | Chat (3-col layout) | Radar (320px) |
| Insight Journal (`/insights`) | Dark nav | Insights content | — |
| Documents (`/documents`) | Dark nav | Documents content | — |
| Settings | Dark nav | Settings content | — |
| Other app-shell pages | Dark nav | Content | — |

All pages that extend `layouts/app_shell.html` get the dark nav automatically — it's shell-owned.

---

## Build guidance for Lead

1. Add the 7 tokens to `web/static/css/tokens.css`
2. Update the shell's left-nav CSS to use `var(--color-nav-*)` tokens (replace light-surface fallbacks)
3. Confirm nav item states (hover/active) use the `var(--color-nav-item-*)` tokens
4. Verify on home (3-column), /insights, /documents (most common non-home pages)
5. The Radar mockup is the visual reference for the overall composition — match it

No new mockup needed. The binding artifact is `dev/active/radar-entities-surfacing-mockup-2026-06-14.html`.

