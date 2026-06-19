# #1280 — Dark nav shell: gameplan + Phase-0 findings

**Author**: Lead Dev · **Date**: 2026-06-18 · **Sprint**: D1 (last before beta gate)
**Binding**: CXO spec `dev/active/design-spec-dark-nav-shell-2026-06-18.md` + mockup `dev/active/radar-entities-surfacing-mockup-2026-06-14.html`

## Phase-0 finding — this is a CHROME RE-ARCHITECTURE, not a recolor (verify-before-build)

The CXO spec's build-guidance reads like a recolor ("add 7 tokens + point the shell nav CSS at them"). But the actual code doesn't match the spec's assumption:

- **Current shell** (`templates/layouts/app_shell.html`): a **TOP** global nav (`{% include components/navigation.html %}` → `.global-nav` horizontal bar: brand, menu, global search, user-dropdown, command palette, trust-gated items) above `.app-shell-body` (main + optional Radar aside). `nav.css` (12KB) styles this top bar.
- **Mockup** (binding): a **LEFT 180px dark rail** in a `180px 1fr 320px` grid — content = **conversation list + "+ New chat" + "History · Learning · Settings" footer**. It shows **no top bar**, no brand bar, no in-nav search (search lives in the **Radar** panel), no user-dropdown.

So the mockup's left rail **replaces** the top nav. That's the "sleek left nav PM wanted" — a Slack/Linear-style chrome re-architecture across all 22 shell pages, **not** a recolor of the existing top bar. The spec author (CXO) wrote a recolor spec believing F2 had already delivered a left-rail shell; F2 delivered a **top** nav.

## What's DONE (safe, spec'd, low-risk) — committed
- **The 7 `--color-nav-*` dark-surface tokens** added to `web/static/css/tokens.css` (exactly the CXO spec; token_lint green). Needed regardless of how the structural questions resolve. The `#1264` light nav-chrome tokens stay (current top nav).

## The gaps the token-spec did NOT resolve (DESIGN — CXO's call, not fillable by inspection)
The mockup omits where the current top-nav's load-bearing elements go in a left-rail model:
1. **Brand/logo** — top of the left rail?
2. **Global search** — the mockup puts "Search everything…" in the **Radar** panel, not the nav. Confirm search moves to Radar (and what non-home pages without Radar do for search).
3. **User-menu** (logout / settings / admin / trust state) — bottom of the left rail? The mockup's footer shows only "History · Learning · Settings" (utility links), not the user-menu.
4. **Command palette + trust-gated nav items** — fold into the left rail where?
5. **Non-home left-rail content** — on `/insights`, `/documents`, `/settings` the left rail can't be a *conversation* list (those aren't chat pages). Is it the conversation list everywhere (Slack-style), or page-nav? The spec says "consistent across all pages" but the mockup content is home-specific.

## Proposed content-model (for CXO to RATIFY or revise — show-your-work, not a unilateral build)
A concrete starting proposal so CXO can confirm/tweak rather than design from scratch:
- **Left rail top**: brand/logo (compact).
- **Left rail body**: conversation list (home) / on non-home pages, the same conversation list (Slack-style — chats are always reachable) OR a short page-context nav — CXO picks.
- **"+ New chat"** CTA (brand color) below the list.
- **Left rail footer** (`margin-top:auto`): the current nav menu items as utility links ("History · Learning · Settings" + the trust-gated ones when visible) **+ the user-menu** (avatar/name → dropdown for logout/admin).
- **Global search** → the Radar panel (home); a small search affordance in the rail footer for non-home pages (or defer).
- **Command palette**: unchanged (keyboard-invoked; not a visible nav element).

## Phased build plan (once CXO ratifies the content-model)
1. ✅ **Tokens** (done).
2. **Restructure `app_shell.html`**: top-nav include → a left-rail nav component inside a grid body (`180px 1fr` base; home adds `320px` Radar). Shell-owned → all pages at once. Real-render tests: nav present, grid columns, chrome-not-overridable (mirror the F2 app-shell tests).
3. **Build the left-rail nav component** (dark, the 7 tokens; item states per spec; brand/list/CTA/footer/user-menu per the ratified content-model). Retire/repurpose the top `.global-nav` CSS.
4. **token-lint clean** (nav CSS references `--color-nav-*` only; no raw hex).
5. **Verify across pages**: home (3-col), /insights, /documents, /settings (most common) — real render, not curl-200.
6. **Close-issue-properly** + PM UAT.

## Why not just build it now
Re-architecting the **shared** shell (22 pages, regression risk) on my own design inferences for the 5 unresolved content-model questions is exactly the "fill spec gaps by inspection" antipattern. The tokens are safe + landed; the structural restructure waits on CXO ratifying the content-model (the proposal above gives them a concrete thing to confirm fast). **PM-flagged scope reality: #1280 is a re-architecture, not a 1-fire recolor.**
