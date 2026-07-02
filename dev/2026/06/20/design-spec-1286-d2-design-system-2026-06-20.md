# Design Spec: D2 Design-System Foundation (#1286)

**Issue**: [#1286 D2 Design-system foundation](https://github.com/mediajunkie/piper-morgan-product/issues/1286)
**Author**: CXO | **Date**: 2026-06-20 | **Status**: DRAFT — for Lead review
**Binding reference**: `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` + `web/static/css/tokens.css`

---

## Scope

Four areas per PM direction (#1286):
1. **Grid layout** — shell grid tokens + content column structure
2. **Typographic baseline rhythm** — vertical rhythm aligned to the 8px grid
3. **Padding / margin / tiling rules** — principled spacing; closes #1251 annotation gaps
4. **Mobile-first + progressive rendering** — responsive breakpoints and layout strategy

**Not in scope**: color tokens (locked), shadow tokens (current `tokens.css` values stand), nav-rail dark-surface tokens (locked in #1280).

---

## 1. Grid layout

### Shell grid tokens (add to `tokens.css`)

```css
/* Shell layout grid — #1286 D2 (CXO spec 2026-06-20) */
--grid-rail-width: 180px;      /* left nav rail */
--grid-radar-width: 320px;     /* Radar panel (home only) */
```

These are already used as raw values in `app-shell.css`. Tokenizing them makes the three-surface constraint explicit and prevents drift.

### Shell grid definitions

```
Home page:   grid-template-columns: var(--grid-rail-width) 1fr var(--grid-radar-width)
Other pages: grid-template-columns: var(--grid-rail-width) 1fr
```

(Already correct per #1280 v2 spec — this formalizes it as token-referenced.)

### Content column

No max-width cap on the center (`1fr`) column — the chat interface is full-width within its column. If future content density requires capping (e.g., reading-width articles), add a `--grid-content-max: 720px` token then. Don't add it speculatively.

### Gutter

No explicit gutter between shell columns — column boundaries are defined by surface backgrounds (dark rail, light content, light Radar). Whitespace is provided by component-level padding inside each column, not by grid gap.

---

## 2. Typographic baseline rhythm

**Baseline unit**: 8px (aligns with existing `--space-sm`).
**Baseline rhythm**: 24px (3 × 8px) — chosen because body text at 14px achieves this with `line-height: 24px` (ratio 1.714). This is the canonical line-height for the body; all other text sizes snap to multiples of 8px.

### Token additions (add to `tokens.css`)

```css
/* Baseline rhythm — #1286 D2 */
--baseline-unit: 8px;          /* = --space-sm, the 8px grid base */
--baseline-rhythm: 24px;       /* 3 × 8px: body line-height target */
```

### Typography scale (aligned to 24px baseline)

| Role | Font size | Line height | Baseline multiple |
|---|---|---|---|
| Micro (nav footer, chips) | `--font-size-xs` (12px) | 16px | 2 units |
| Label (section headers, metadata) | `--font-size-sm` (13px) | 16px | 2 units |
| Body (chat messages, card content) | `--font-size-base` (14px) | 24px | 3 units (canonical baseline) |
| UI text (form fields, entity titles) | `--font-size-md` (15px) | 24px | 3 units |
| Heading-sm (panel titles) | `--font-size-lg` (16px) | 24px | 3 units |
| Heading-md (page titles) | `--font-size-2xl` (20px) | 24px | 3 units |
| Heading-lg (section titles) | `--font-size-3xl` (24px) | 32px | 4 units |

**Current `--line-height-relaxed: 1.6` produces 22.4px for 14px text** — 1.6px short of the 24px baseline. Update to `--line-height-relaxed: 1.714` (rounds to 24px) or specify `line-height: var(--baseline-rhythm)` directly in the body rule. Either achieves the 24px snap; prefer the direct value on the body rule for legibility.

### Apply to body rule

```css
body {
  font-size: var(--font-size-base);   /* 14px */
  line-height: var(--baseline-rhythm); /* 24px — 3 × 8px grid */
  font-family: var(--font-family);
}
```

Heading and label line-heights: use 16px (2 units) for small text (12–13px), 24px (3 units) for 14–16px text, 32px (4 units) for 20–24px text. These are not new tokens — specify inline in component CSS rules.

---

## 3. Padding / margin / tiling rules

### Token gap: micro-spacing `--space-2xs`

The Radar panel uses `gap: 6px` and `padding: 6px` for entity items — a tight spacing that the current 8px grid doesn't cover cleanly. The options were: round to 4px (too tight), round to 8px (noticeably looser), or introduce a `6px` micro-spacing step.

**Decision**: Add `--space-2xs: 6px` as the micro-spacing token. Rationale: 6px is a documented, intentional value in the Radar panel design (flagged as non-annotated in #1251). Rounding it to 4px or 8px changes the visual density. The 8px grid is a discipline, not an absolute rule — a single 6px step for dense entity surfaces is justified.

```css
/* Add to tokens.css spacing section — between --space-xs and --space-sm */
--space-2xs: 6px;   /* micro-spacing for dense entity surfaces (Radar items, chips) */
```

### Token gap: pill border radius

```css
/* Add to tokens.css border radius section */
--border-radius-pill: 999px;   /* pill shape for entity type tags, chips */
```

The existing `--border-radius-full: 50%` produces circles. For rectangular elements that should be pill-shaped (entity type badges), `999px` is the correct approach.

### Tiling rules for Radar entity items

These close the #1251 non-annotated items. All values from the mockup, now tokenized:

| Property | Token | Value |
|---|---|---|
| Item padding (vertical) | `--space-2xs` | 6px |
| Item padding (horizontal) | `--space-sm` | 8px |
| Item gap (between items in a section) | `--space-2xs` | 6px |
| Item border-radius | `--border-radius-md` | 6px |
| Entity type chip border-radius | `--border-radius-pill` | 999px |
| Body text | `--line-height-relaxed` (updated to 24px) | per §2 |

```css
/* Canonical Radar entity item rule (from mockup) */
.radar-entity-item {
  padding: var(--space-2xs) var(--space-sm);   /* 6px 8px */
  border-radius: var(--border-radius-md);       /* 6px */
  display: flex;
  align-items: center;
  gap: var(--space-2xs);                        /* 6px between icon and label */
}

.entity-type-chip {
  border-radius: var(--border-radius-pill);     /* pill */
  padding: 2px var(--space-xs);                 /* 2px 4px */
  font-size: var(--font-size-xs);               /* 12px */
  line-height: 16px;                            /* 2 baseline units */
}
```

### Card-level spacing

Existing card tokens from `tokens.css` stand — they are correct for card-level tiling:
- `--space-card-pad: var(--space-lg)` = 24px internal padding ✓
- `--space-card-gap: var(--space-md)` = 16px between card elements ✓
- `--space-module-gap: var(--space-xl)` = 32px between modules ✓

### Content column padding

```css
.content-column {
  padding: var(--space-md) var(--space-lg);  /* 16px top/bottom, 24px left/right */
}
```

Consistent for all non-home pages. Home page: chat input has its own padding; no column-level wrapper padding (the chat interface handles its own insets).

---

## 4. Mobile-first + progressive rendering

### Breakpoints

```css
/* Add to tokens.css or a new breakpoints.css */
--breakpoint-mobile: 480px;    /* single-column floor */
--breakpoint-tablet: 768px;    /* two-column: rail + content */
--breakpoint-desktop: 1024px;  /* full shell: rail + content (+ Radar on home) */
```

**Note**: breakpoints are non-responsive custom properties — they're used as media query values in the CSS, not as applied tokens. Documenting them here as the canonical source of truth.

### Mobile-first layout strategy

All CSS is written for mobile first, with wider layouts added via `min-width` media queries.

**Mobile (<768px)**:
- Single-column layout: `grid-template-columns: 1fr`
- Rail: hidden. Navigation via hamburger button in a top bar (or bottom navigation strip — design TBD, below)
- Radar: not displayed on home; accessible via a "View Radar" button or link in the chat interface
- Home page: full-width chat interface, no side panels

**Tablet (768px–1023px)**:
- Two-column: `grid-template-columns: var(--grid-rail-width) 1fr`
- Rail: visible. Same content model as desktop (conversations + footer).
- Radar: not persistent; accessible via a toggle in the home page (button above or below the chat area). Could be a drawer or inline expandable.
- Other pages: `grid-template-columns: var(--grid-rail-width) 1fr` (same as desktop, no change needed)

**Desktop (≥1024px)**:
- Home: `grid-template-columns: var(--grid-rail-width) 1fr var(--grid-radar-width)`
- Other: `grid-template-columns: var(--grid-rail-width) 1fr`

```css
/* app-shell.css — mobile-first shell grid */
.app-shell {
  display: grid;
  grid-template-columns: 1fr;   /* mobile: single column */
}

.nav-rail {
  display: none;   /* mobile: hidden */
}

@media (min-width: 768px) {
  .app-shell {
    grid-template-columns: var(--grid-rail-width) 1fr;
  }
  .nav-rail {
    display: flex;
  }
}

@media (min-width: 1024px) {
  .app-shell.home-page {
    grid-template-columns: var(--grid-rail-width) 1fr var(--grid-radar-width);
  }
}
```

### Mobile navigation — deferred design decision

The mobile nav pattern (hamburger + top bar vs. bottom tab strip) is a **deferred decision** — not enough context yet about which surfaces are most used on mobile. For D2, implement mobile as: **collapsed rail + top bar with hamburger → slide-in drawer**. This is the simplest pattern and consistent with Slack-style mobile navigation. Post-D2, revisit if analytics show different usage patterns.

```
Mobile top bar (48px height):
  [≡ hamburger]  Piper Morgan  [avatar]
  
Slide-in rail (same content model as desktop rail):
  [Logo] Piper Morgan  [×]
  CHATS
    Recent conv 1..8
  [+ New chat]
  ————————————————————
  Check in · Insights · Learning · Settings
  [Avatar] Name ▸
```

The `--touch-target-min: 48px` token (already in `tokens.css`) applies to all mobile touch targets.

---

## Conformance review against mockup

#1286 subsumes the #1236 conformance-review-against-the-mock. The binding reference is `dev/active/radar-entities-surfacing-mockup-2026-06-14.html`.

**Conformance pass order** (after Lead implements D2):
1. Spacing: verify Radar items use `var(--space-2xs)` gap/padding, not raw 6px
2. Typography: verify body text is 14px/24px
3. Grid: verify shell grid at all three breakpoints
4. Pill radius: verify entity type chips use `var(--border-radius-pill)`
5. Mobile: verify nav collapses to hamburger drawer at <768px

CXO will run this conformance review after Lead ships the D2 implementation.

---

## Summary of token additions

Add to `tokens.css`:

```css
/* Grid tokens — #1286 D2 */
--grid-rail-width: 180px;
--grid-radar-width: 320px;

/* Baseline rhythm — #1286 D2 */
--baseline-unit: 8px;
--baseline-rhythm: 24px;

/* Micro-spacing for dense entity surfaces — #1286 D2 */
--space-2xs: 6px;

/* Pill border radius — #1286 D2 */
--border-radius-pill: 999px;

/* Breakpoints (documentation only — use in media queries) — #1286 D2 */
--breakpoint-mobile: 480px;
--breakpoint-tablet: 768px;
--breakpoint-desktop: 1024px;
```

**Total net new tokens**: 7 (grid ×2, baseline ×2, spacing ×1, radius ×1, breakpoints ×3).
**Modified token**: `--line-height-relaxed` body application → target `24px` (via `line-height: var(--baseline-rhythm)` in body rule).

---

## Lead implementation notes

1. Start with `tokens.css` additions (the 7 tokens) — they're the foundation.
2. Update `app-shell.css` for the mobile-first grid (the CSS block in §4 is copy-paste-ready with minor customization for your template variable names).
3. Update the body rule in whatever the global CSS is (likely `tokens.css` or `app-shell.css`).
4. Add `.radar-entity-item` and `.entity-type-chip` rules to `radar.css` (or wherever radar entity rendering lives).
5. Run `token_lint` to confirm no raw hex or raw px values remain in new CSS.
6. CXO conformance review after implementation — I'll do a code-review pass against the mockup and this spec.

If any implementation decision conflicts with a constraint I haven't seen (template variable naming, server-side rendering limitations, etc.), flag me — I'll resolve quickly.
