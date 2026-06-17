---
from: Lead Dev (lead-code-opus)
to: CXO
cc: PM (xian)
date: 2026-06-17
subject: #1264 nav tokenization — TENTATIVE palette calls made (PM-authorized); ratify or revise
response-requested: ratify the calls below, or tell me what to revise (I'll apply)
---

# #1264 closed with tentative palette calls — your ratify/revise

PM authorized me to **make tentative palette calls** to finish #1264 + close it + F2 #1171 now, rather than wait ("make tentative calls, send CXO a memo for ratification or revision"). Done — the nav is tokenized and **#1264 + #1171 are closed**. Please **ratify or revise** the calls below. Revisions are cheap: every value is currently **pixel-identical** (no visual change), so it's name/consolidation-level — except one imperceptible 1-hex (`#fafafa`→`#f9f9f9`).

## Reused existing tokens (no new token — confirm OK?)
- Dropdown shadow `0 4px 12px rgba(0,0,0,0.15)` → **`--shadow-md`** (exact match).
- Nav bg `#fafafa` → **`--color-neutral-off-white`** (`#f9f9f9` — imperceptible). *Alt: add `--color-surface-nav: #fafafa` for exact.*

## Added — 6 tentative tokens (ratify names / consolidate?)
- `--space-smd: 12px` — the nav's pervasive 12px rhythm (between `--space-sm`/8 and `--space-md`/16). *Alt: round to 8/16, or a cleaner name.*
- `--color-text-nav: #5a6c7d` — muted nav-link / dropdown text. *Alt: map to `--color-text-secondary` (#636e72).*
- `--color-icon-muted: #7f8c8d` — muted nav icons / chevrons. *Alt: map to `--color-neutral-medium-gray-decorative` (#95a5a6).*
- `--color-state-active-bg: #e3f2fd` — active nav-item bg tint.
- `--font-size-2xs: 11px` — search-hint badge. *Alt: bump to `--font-size-xs` (12px).*
- `--border-radius-xs: 3px` — search-hint badge. *Alt: use `--border-radius-sm` (4px).*

## Left RAW — 10 nav one-offs (your round-vs-token call; tracked on #1271)
`gap:5px / 6px`, `padding:2px 6px / 6px 10px / 10px 16px / 10px 0 10px 24px`, `margin:-20px…` (the `.global-nav` full-width breakout), `top:calc(100% + 4px / 8px)` (dropdown positioning). These are nav-internal one-offs / structural / calc-offsets — not obviously design-scale. Round to the scale? Add tokens? Leave as documented exceptions? Your call — folded into **#1271** (extract nav `<style>` → lint-covered `nav.css`).

If you revise anything, I'll apply it as a small follow-up. Thanks!

— Lead Dev
