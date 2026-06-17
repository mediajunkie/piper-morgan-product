---
from: Lead Developer
to: CXO (Chief Experience Officer)
cc: CEO (xian)
date: 2026-06-16
subject: F2 #1171 — shell + insights SHIPPED; Phase-0 found 27 standalone pages (not ~6) → 4 cohorting/scope decisions to confirm before the mass migration
in-reply-to: design-floor-F2-page-shell-spec-2026-06-16.md
response-requested: the 4 confirms below (cohort list, item-2 scope, nav-component scope, aside default) — at your cadence; the migration cohort waits on the cohort confirm
---

# F2 built to your spec — shell + first page on main

Your spec was clean to build to. Shipped + on `origin/main` (793 template tests green):
- **`layouts/app_shell.html` + `web/static/css/app-shell.css`** — the standalone shell. Chrome (nav include + footer) is shell-owned, **not page-overridable** — proven by a test (a page overriding `header`/`nav`/`footer` blocks has zero effect; the chrome always renders). Token-only (no inline styles). 5 real-render tests.
- **`insights.html` migrated** onto it (the proof-of-pattern): re-pointed base→app_shell; the #1251 item-1 per-page nav include is retired (the shell owns the chrome now, exactly as that include's own comment predicted); **#1251 item-3 done** ("Correct" → "Correct this"). Real-render test confirms nav+footer+content render via the shell.

# Phase-0 scope finding: it's **27 standalone pages, not ~6**

That changes the migration from a quick pass to a cohorted effort. **4 decisions before I mass-migrate** (I'll build to whatever you confirm):

1. **Cohort confirm** — proposed split:
   - **MIGRATE to app_shell (~21 app pages)**: home, account, documents, files, lists, projects, project_detail, todos, work_items, learning-dashboard, standup, transparency, integrations, settings-index, settings_calendar, settings_github, settings_notion, settings_projects, settings_slack, advanced-settings, personality-preferences, privacy-settings.
   - **STAY standalone-by-design (~5)**: login, setup (pre-auth — no app-nav before login), 404, 500, network-error (error states — minimal chrome). A future minimal auth/error shell is out of F2 scope. **Confirm this split?**

2. **#1251 item-2 (inline CSS → tokens) scope** — `insights.html`'s `<head>` is **242 lines of CSS**, and each app page has its own inline CSS too. I recommend: **structural migration first** (re-point + chrome, per page), **CSS tokenization as a focused follow-on** (its own increment), rather than one giant per-page pass. **Agree, or fold CSS into each page's migration?**

3. **nav-component CSS** — `components/navigation.html` itself carries **~500 lines of inline hardcoded-hex `<style>`** (drift *inside* the chrome). Your spec wants chrome token-only; the shell's own CSS is token-clean, but the nav component isn't. That's a sizable token migration. **F2 scope, or a separate F3-adjacent item?** (I recommend separate.)

4. **aside default** — your spec said the Radar aside defaults **on**; I shipped it **opt-in (`show_radar=false` default)** for v1 to keep the shell decoupled from #1236 Radar (still behind `?radar=1` / UAT-pending). Flip to default-on when Radar UAT passes? **Confirm v1 default-off is OK.**

On your cohort confirm I'll migrate the ~21 as per-page green increments (a real `template.render()` per page, per the UI-fix discipline). Gameplan + audit: `dev/2026/06/16/1171-F2-*.md`.

— Lead, 2026-06-16
