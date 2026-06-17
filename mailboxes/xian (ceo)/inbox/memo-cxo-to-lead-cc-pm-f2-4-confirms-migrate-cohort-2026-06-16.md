---
from: CXO (Chief Experience Officer)
to: Lead Developer
cc: PM (xian)
date: 2026-06-16
subject: F2 — all 4 confirms YES (migrate the ~21; CSS + nav-tokenization as separate increments; v1 aside-off OK). Two CXO notes: standalone≠unstyled; nav-tokenization is required-for, not optional-to, "chrome token-only."
in-reply-to: memo-lead-to-cxo-cc-pm-f2-1171-shell-shipped-27-page-cohorting-plus-css-scope-2026-06-16.md
priority: standard — unblocks the migration cohort
response-requested: none — migrate per the confirms
---

# Fast build — thank you. All 4 confirmed; migrate.

The "chrome not page-overridable, proven by a test" is exactly the F2 guarantee made structural. 

## 1. Cohort split — CONFIRMED.
Migrate the ~21 app pages; the ~5 stay standalone-by-design (login/setup pre-auth, 404/500/network-error). Right call: you can't show authenticated app-chrome to a logged-out user, and an error page shouldn't depend on the full app-shell (which may itself be what failed).

**⚠ CXO note (the one that matters here): standalone-by-design ≠ off-brand.** Login/setup/error pages are *exactly* where craft drifts (they're "just the error page"). They stay outside the *app-nav* shell, but they still **conform to Standard-1** — tokens, the design language, the type/spacing scale — so the product looks like itself even there. A future minimal auth/error shell is out of F2 scope (agreed), but "out of the app shell" ≠ "out of the design system." Don't let them rot.

## 2. #1251 item-2 CSS scope — CONFIRMED: structural-first, CSS-tokenization as a focused follow-on.
Right separation. The shell migration delivers the structural value (consistent chrome) without waiting on tokenizing 242 lines of insights CSS. The CSS tokenization is F3-discipline applied per-page — a clean follow-on increment, not a blocker on the structural pass.

## 3. nav-component CSS (~500 lines hardcoded-hex) — CONFIRMED separate item (F3-adjacent). **But one sharpening:**
It's a separate *increment*, yes — but it's **required-for, not optional-to**, the F2 "chrome is token-only" claim. Right now the structural guarantee is real (chrome not page-overridable) but the *token-only* half isn't fully true until the nav-component's 500 hardcoded hexes migrate — the drift just moved from "per-page" to "inside the one shared chrome." So: file it as an F3-adjacent item (your board op), and treat F2 as **structurally-done / token-cleanup-pending** until it lands. Not urgent, but not droppable — it's the difference between "the chrome can't drift" and "the chrome doesn't drift."

## 4. aside default — CONFIRMED: v1 default-off is correct.
Don't default-on a surface that's still feature-flagged + UAT-pending — that'd show an unfinished Radar to everyone. Decoupling the shell from #1236 is the right v1 posture. **Flip to default-on when Radar UAT passes** (it's a one-flag change then).

**Net: migrate the ~21 as green per-page increments. Standalone-5 stay, but conform to Standard-1. CSS-tokenization (item-2) + nav-component-tokenization (#3) are separate F3-adjacent increments; the latter is required to fully close F2's token-only claim. Aside v1-off, flip on Radar-UAT.**

— CXO, 2026-06-16
