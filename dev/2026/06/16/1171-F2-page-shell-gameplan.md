# Gameplan — F2 #1171 Page-Shell

**Issue**: #1171 (F2 page-shell) · parent #1169 design-floor
**Binding spec**: `dev/active/design-floor-F2-page-shell-spec-2026-06-16.md` (CXO) — treated as the ISSUE-gate artifact.
**Author**: Lead Developer · 2026-06-16 · template v9.6 · Execution SOLO.

## The property F2 guarantees (CXO §0)
A page **cannot drift off-chrome, structurally** — it declares only its content; header/nav/footer are the shell's and are **not page-overridable blocks**. Structure, not discipline, retires the Insight-Journal-isolation defect class.

## Phase -1: Infra (verified empirically)
Jinja2Templates (lenient Undefined); `templates/layouts/base.html` = thin base (head + token CSS + `{% block content %}`, NO nav); `templates/components/navigation.html` = global nav (currently a large **inline `<style>` of hardcoded hex** — drift inside the chrome); `web/static/css/tokens.css` exists; F3 token-lint live. pytest + `template.render()` for UI tests.

## Phase 0: Investigation (done) — the scope finding
- **27 standalone pages declare their own `<html>`/`<!DOCTYPE>`** (CXO spec estimated "~6"). Only `insights.html` extends a base today.
- **⚠️ SCOPE-DISCOVERY → cohorting needed** (not a blind sweep):
  - **Migrate to `app_shell` (app-page cohort, ~22)**: insights (first — already on base), home, account, documents, files, lists, projects, project_detail, todos, work_items, learning-dashboard, standup, transparency, integrations, settings-index, settings_calendar, settings_github, settings_notion, settings_projects, settings_slack, advanced-settings, personality-preferences, privacy-settings.
  - **Stay standalone-by-design (~5)**: login, setup (pre-auth — no app-nav), 404, 500, network-error (error states — minimal chrome). **→ surface to CXO/PM to confirm** (a future minimal auth/error shell is out of F2 scope).

## Phase 0.5: Frontend contract (the block contract IS the contract — CXO §2)
| block | who | purpose |
|---|---|---|
| `page_title` | page | `<title>` text |
| `head_extra` | page | page `<head>`: meta, page CSS link, preloads |
| `main` | page | **THE content — the one block every page overrides** |
| `aside` | page (opt) | Radar/Layer-2 aside; suppress via `{% block aside %}{% endblock %}` / `show_radar=false` |
| `scripts` | page | end-of-body page scripts |
| **header/nav/footer** | **SHELL ONLY — not a block** | the F2 guarantee |

## Phase 0.5 (static-file): verify `app-shell.css` is served
New CSS at `web/static/css/app-shell.css` → served at `/static/css/app-shell.css` (same dir as tokens.css, which base.html links as `/static/css/tokens.css`). Confirm the StaticFiles mount covers it (it covers the existing token/dialog/etc. CSS, so a sibling file is served by the same mount) — verify by the render test asserting the `<link>` href + a served-path check.

## Design decisions
1. **`app_shell.html` = standalone full shell** (own DOCTYPE+head+chrome+blocks), **NOT** `{% extends base.html %}`. Rationale: matches CXO's block names exactly; avoids base's title/head/content/scripts nested re-exposure puzzle; `base.html` stays for now (retire later when nothing extends it).
2. **Chrome = `{% include 'components/navigation.html' %}` + a footer, both shell-owned (no blocks)** → pages physically cannot override → the guarantee. A test asserts no migrated page defines `<html>`/nav.
3. **Token-only chrome via new `web/static/css/app-shell.css`** (zero inline styles — F3-clean). The nav component's existing inline-hex `<style>` is **pre-existing drift**; cleaning navigation.html → tokens is a flagged follow-on sub-item (not blocking the shell; noted for "chrome uses tokens exclusively").
4. **`aside` default = empty in v1** (the slot exists; pages opt into the Radar aside). Rationale: #1236 Radar is behind `?radar=1` + UAT-pending — don't couple the shell to un-UATed Radar. The slot is ready; Radar fills it where enabled (home already wires it). Revisit when Radar UAT passes.
5. CSS load order: `tokens.css` first (per base.html's note).

## Phases (Inchworm — green + commit + push per increment)
- **P1** — Build `app_shell.html` + `app-shell.css` (token-based: content max-width+centered, `--space-lg` padding, `--color-neutral-off-white` bg, `--surface-card`; aside fixed-width + `--border-card`; minimal footer). **TDD**: shell renders; `page_title`/`head_extra`/`main`/`aside`/`scripts` overridable; **header/nav/footer NOT overridable** (a child template overriding a bogus `header` block leaves chrome intact); nav include present; token-only (no inline `style=`).
- **P2** — Migrate `insights.html` → `app_shell` (re-point from base; content → `{% block main %}`); fold in **#1251 item-2** (inline styles→tokens; bespoke→Part-B Card/Dialog) + **item-3** ("Correct"→"Correct this"). **Real `template.render()` test** (not curl-200): asserts nav present, content rendered, "Correct this" label, no raw `<html>` double-wrap.
- **P3** — Surface the 27-vs-6 cohorting to CXO/PM (memo). On confirm, migrate the app-page cohort as **per-page green increments** (each a real-render test).
- **PZ** — Close #1171 properly when the cohort renders inside the shell (a grep/test confirms no app-page defines its own `<html>`/nav).

## Test scope
- [ ] Unit: shell block contract (overridable vs shell-only); token-only chrome.
- [ ] **Real-render** (per page): `template.render(realistic_context)` asserts nav + content + no double-`<html>` (UI-fix discipline — NOT curl-200).
- [ ] Regression: existing template suite stays green (insights re-point doesn't break its tests; the 784 template tests).
- [ ] Performance: shell adds one include + one CSS link per page — negligible; the structural win (no per-page nav dup) reduces template surface.

## STOP conditions
27-vs-6 surfaced (done — cohorting is a CXO/PM call before mass-migrate); if a "standalone-by-design" page (login/error) turns out to need chrome → re-cohort with CXO; if app-shell.css token gaps (a needed token missing) → flag to CXO (F3 lane), don't hardcode.

## Tonight's increment
P1 (shell + css + TDD) + P2 (insights migration + #1251 items) + the P3 surface-memo. The ~22-page cohort migration proceeds as increments after cohorting is confirmed.
