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

---

## ✅ CXO RATIFIED the content-model (2026-06-18) — build-ready

CXO ratified ("build it") with these resolutions to the 5 gaps:
1. **Brand** → top of the left rail (compact). ✓
2. **Global search** → Radar panel on home; **NO non-home search affordance** (avoid the false-promise of a search box that can't search; defer cross-page search to #1236). Resolves gap 2.
3. **User-menu** → left-rail footer (`margin-top:auto`), below the utility links. ✓
4. **Command palette** → **⌘K-only, no visible rail button** (keyboard-invoked); trust-gated nav items live in the footer when visible. Resolves gap 4.
5. **Non-home content** → **conversation list EVERYWHERE** (Slack-style — chats always reachable), not page-context nav. Resolves gap 5.

The rail (all pages): **[brand top] · [conversation-list body] · [+ New chat CTA] · [footer: utility links (History·Learning·Settings) + trust-gated items + user-menu]**.

## Build specifics (shell investigation, 2026-06-18)
- **The shell** (`templates/layouts/app_shell.html`): top-nav include at **L48** (`{% include 'components/navigation.html' %}`) + `.app-shell-body` = `.app-shell-main` + optional `.app-shell-aside` (Radar, behind `show_radar`). **The flip** = replace the top-nav include with a left-rail include + restructure `.app-shell-body` into a grid: base `180px 1fr`; home adds the `320px` Radar aside → `180px 1fr 320px`.
- **⚠️ The conversation list is DYNAMIC JS**, not a static include — it lives in `home.html` + `web/static/js/chat.js` (conversation load/render) + the `history_sidebar.html` slide-out. So the rail's conv-list **reuses/integrates the existing chat.js conversation-loading** — NOT a static-render-testable partial. The static rail chrome (brand/CTA/footer/user-menu) IS server-render-testable; the conv-list behavior needs the **jest harness (#1248) or PM UAT** (per the real-render-test discipline — a server render test won't exercise the JS).
- **Tokens** (the 7 `--color-nav-*`) landed (`d107d013c`).

## Revised phased plan (rail-alongside → flip)
1. ✅ Tokens.
2. **Build the left-rail component** — static chrome (brand · New chat CTA · footer: utility + trust-gated links + user-menu) render-tested (template.render asserts structure + token-only colors, mirror the F2 app-shell tests) **+ integrate the dynamic conv-list** (reuse chat.js loading) jest/UAT-verified. Build **rail-alongside** (not yet wired into app_shell) = zero regression.
3. **Flip `app_shell.html`** — top-nav include → rail include; `.app-shell-body` → grid; **all 22 pages at once** (shared shell). Per-page real-render tests (home 3-col, /insights, /documents, /settings); retire the top `.global-nav` CSS.
4. **token-lint clean** + cross-page render verification + PM UAT + close-issue-properly.

**STATUS: build-ready; teed up for a focused fire.** The build is a substantial 22-page re-architecture with a JS conv-list integration (warrants fresh focus + the jest-or-UAT verification path, not a rushed tail-of-fire build). Next fire executes Phase 2.
