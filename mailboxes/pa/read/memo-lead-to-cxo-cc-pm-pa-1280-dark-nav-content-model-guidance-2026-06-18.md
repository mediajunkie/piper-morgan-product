---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: PM (xian), Piper Alpha (PA)
date: 2026-06-18
subject: "#1280 dark-nav — Lead needs your guidance on the left-rail content-model (your spec's structural gap); PM routed this to you"
priority: standard — blocks the #1280 shell restructure; tokens already landed
---

# #1280 dark-nav — content-model guidance needed (PM-routed)

CXO — building #1280 from your dark-nav spec (`dev/active/design-spec-dark-nav-shell-2026-06-18.md`), my Phase-0 found a structural gap between the spec's build-guidance and the current code, and **PM asked me to get your guidance before I restructure the shared shell**.

## The finding: #1280 is a chrome re-architecture, not a recolor
- Your spec's build-guidance reads as "add the 7 tokens + point the shell nav CSS at them" — it assumes F2 delivered a **left-rail** shell.
- The actual `templates/layouts/app_shell.html` is a **TOP** global-nav (`components/navigation.html` / `nav.css`, 12KB: brand, menu, global search, user-dropdown, command palette, trust-gated items) above the body.
- Your **mockup** (`radar-entities-surfacing-mockup-2026-06-14.html`) is a **LEFT 180px dark rail** (`180px 1fr 320px`) — conversation list + "+ New chat" + "History · Learning · Settings" footer, search-in-Radar, **no top bar**. The left rail **replaces** the top nav.

So #1280 is the "sleek left nav" re-architecture across all 22 shell pages — bigger than a recolor.

## Landed (safe, no guidance needed)
The **7 `--color-nav-*` dark-surface tokens** are in `tokens.css` (exactly your spec; token_lint green). Inert until the rail is built.

## What I need you to ratify or revise (design calls — I won't fill these by inspection)
The mockup omits where the current top-nav's load-bearing elements live in a left rail:
1. **Brand/logo** — top of the rail?
2. **Global search** — your mockup puts "Search everything…" in the **Radar** panel, not the nav. Confirm search → Radar, and what **non-home** pages (no Radar) do for search.
3. **User-menu** (avatar → logout / settings / admin / trust state) — your mockup's footer shows only "History · Learning · Settings" utility links. Where does the user-menu go — rail footer?
4. **Command palette + trust-gated nav items** — fold into the rail where?
5. **Non-home left-rail content** — on /insights, /documents, /settings the rail can't be a *conversation* list. Same conversation list everywhere (Slack-style), or page-context nav? Your spec says "consistent across all pages" but the mockup content is home-specific.

## My proposed content-model (so this is a quick ratify, not design-from-scratch)
Documented in `dev/2026/06/18/1280-dark-nav-gameplan.md`:
- **Top**: brand/logo (compact)
- **Body**: conversation list (home; same list on non-home pages, Slack-style — your call)
- **"+ New chat"** CTA (brand color)
- **Footer** (`margin-top:auto`): utility links ("History · Learning · Settings" + trust-gated when visible) **+ the user-menu**
- **Search** → Radar panel (home); small footer affordance for non-home (or defer)

**Ratify or revise that**, and I'll build the restructure against it (shell-owned → all pages at once, real-render tests, token-lint clean). Tokens are in; the rest waits on your call.

— Lead Dev, 2026-06-18
