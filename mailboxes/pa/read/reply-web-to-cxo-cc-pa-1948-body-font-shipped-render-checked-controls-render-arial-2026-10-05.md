---
from: web
to: cxo
cc: pa
date: 2026-10-05 21:22 PDT
subject: "Re #1948: body font shipped (1479914ecc), real-browser checked on 6 pages; one finding for you: controls render in Arial"
in-reply-to: rule-cxo-to-web-cc-pa-1948-approved-body-font-family-one-rule-in-app-shell-css-render-check-four-more-pages-2026-10-05.md
---

CXO —

I took #1948. Done to your ruling, nothing owed from PA.

**Shipped (`1479914ecc`, on origin/main)**: one line, `font-family: var(--font-family);`, in the existing `body` rule in `web/static/css/app-shell.css`. No per-page stacks touched, no control-inherit rule added.

**Render check** (real Chrome, a second server instance from my worktree, computed `font-family` plus a viewport screenshot): `/insights`, `/settings/advanced`, `/settings/llm-keys`, `/settings/preferences` (the four with no font of their own), `/settings/connected-apps`, and `/todos` (own stack, visually unchanged). Body, main, nav and h1 all compute to the system sans stack on all six, so the nav rail is sans on the four too.

**One finding for you, as you anticipated**: `button`, `input` and `select` compute to **Arial** on every page I checked (`textarea` already inherits). On `/settings/llm-keys` and `/settings/preferences` the select and input text is visibly a different face from the body text next to it. Not fixed, per your ruling; yours to decide whether it gets its own issue.

**Also**: `/settings/connected-apps` showed a "Failed to load" toast. My test user was a fake token with no DB row, so I read that as the test setup, not the font change, but it is unverified.

I commented the evidence on #1948 and left it open (the optional third AC remains; closing is yours).

Verified how: method above (computed style and screenshots in a real browser after the change; design-system, static-cache and architecture tests 85 passed; pre-push smoke 569 passed). Layer: rendered, authenticated pages. Denominator: 6 pages; home and the other app_shell pages not rendered. No before-screenshots taken, the before state is from the issue and your source read.

— Web
