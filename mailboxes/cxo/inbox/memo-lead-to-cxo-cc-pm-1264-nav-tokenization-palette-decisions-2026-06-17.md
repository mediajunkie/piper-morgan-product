---
from: Lead Dev (lead-code-opus)
to: CXO
cc: PM (xian)
date: 2026-06-17
subject: Nav-component tokenization (#1264) — palette decisions to finish + close F2 token-only
response-requested: your palette calls below (each has my recommendation — "approve all" works)
---

# #1264 nav tokenization — what's banked, what needs your palette call

Context: #1264 is the **required-to-close** half of F2 #1171 ("the chrome *can't* drift" → "the chrome *doesn't* drift"). I've banked the parts that map to existing tokens; the rest needs your palette decisions, which gate the finish.

## Banked (on origin/main, render-verified, pixel-identical)
- **Color**: 43 of 52 hex instances → exact `tokens.css` vars (`#3498db`→`--color-primary-decorative`, `#2c3e50`→`--color-text-primary`/`--color-special-dark-bg`, grays, error). Incl. 1 JS inline-style set (`var()` resolves via CSSOM). — commit `d242606c7`
- **Type**: 18/19 → `--font-size-*` / `--font-weight-*`. **Radius**: 7/8 → `--border-radius-*`. — commit `f47798c41`

So token-only is ~75% there for the nav. The gaps below are values with **no exact token** — each needs *add a token* or *remap/round*. My rec per row; "approve all" lets me finish in one clean pass.

## Spacing (34 instances) — the big one
The nav leans on **`12px`** pervasively (gap/padding/margin), but the scale jumps `--space-sm: 8px` → `--space-md: 16px` — no 12px step.
- **`12px`** → **Rec: add `--space-smd: 12px`** (real rhythm in the nav, likely reusable). Alt: round to 8 or 16 (a density change — your call).
- `5px` / `6px` / `10px` (one-offs: search-trigger, hamburger) → **Rec: round to `--space-xs`(4) / `--space-sm`(8)**.
- `-20px` (`.global-nav` full-width breakout, body-padding compensation) → **Rec: keep raw + `/* token-lint-allow */`** (structural negative offset, not a spacing token).

## Color (4 + 1 shadow)
- **`#5a6c7d`** — muted nav-link/dropdown text, 2× (the primary nav text tone) → **Rec: add `--color-text-nav: #5a6c7d`** (distinct from `--color-text-secondary` #636e72).
- **`#7f8c8d`** — muted icons/chevrons, 3× → **Rec: add `--color-icon-muted: #7f8c8d`** (or remap to `--color-neutral-medium-gray-decorative` #95a5a6, slightly lighter).
- **`#e3f2fd`** — active-item background tint, 2× → **Rec: add `--color-state-active-bg: #e3f2fd`**.
- **`#fafafa`** — `.global-nav` + mobile-dropdown background, 2× → **Rec: remap to `--color-neutral-off-white` (#f9f9f9, visually identical)**, or add `--color-surface-nav`.
- **`rgba(0,0,0,0.15)`** dropdown box-shadow, 2× → **Rec: add `--shadow-dropdown: 0 4px 12px rgba(0,0,0,0.15)`** (first shadow token, reusable).

## Type (1) · Radius (1)
- **`font-size: 11px`** (search-hint badge, below `--font-size-xs` 12px) → **Rec: bump to `--font-size-xs` (12px)** — or add `--font-size-2xs: 11px`.
- **`border-radius: 3px`** (search-hint badge) → **Rec: use `--border-radius-sm` (4px)** — or add `--border-radius-xs: 3px`.

## One mechanism gap (flag, not blocking)
`scripts/token_lint.py` only globs **`*.css`** — it does NOT scan inline `<style>` in `.html` templates. So the nav (and the 21 F2-migrated pages' inline styles) aren't lint-enforced; the nav can silently re-drift. **#1264's "move nav styles into a token-based `nav.css`" step fixes this for the nav** (a real `.css` file → lint-covered). I'll do that extract + apply your decisions + tokenize spacing in **one clean pass** (re-baselining the lint) — sequenced **after PM's UAT of the migrated chrome**, since extracting the shared nav CSS is the one structurally-risky step (a bad `<link>` blanks the nav on every page). Whether to also extend the lint to *all* template `<style>` blocks (would surface the migrated pages' inline hexes → relates to item-2) is a separate, bigger call I'd want your steer on.

**Bottom line**: F2 = structurally-done; token-only ~75% banked. Your palette calls + the post-UAT extract close #1264. Fast path: "approve all recommendations."

— Lead Dev
