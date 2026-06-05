# UI Functional Audit — June 2026 (#1142)

**Author**: Lead Developer
**Date**: 2026-06-04
**Issue**: #1142 UI-AUDIT-FUNCTIONAL (M3 architectural-cleanup anchor)
**Method**: 3 parallel Explore-agent surveys (route-group A: conversational+data; B: settings+integrations; C: nav reachability + slash-command parity) + Lead Dev reconciliation + spot-verification.
**Scope**: 26 HTML routes in `web/api/routes/ui.py` + 28 templates in `templates/` + slash-command registry (`services/commands/definitions.py`) + `web/api/routes/debug.py`.

---

## PM-readable summary

**The headline correction to the M2-smoke read:** the UI is **less broken than the smoke suggested**, but **less reachable** than anyone realized.

During #1047 M2D-UAT, surfaces appeared "missing" (no lists view) or "isolated" (Insight Journal). The audit shows the real story:

1. **The dominant architecture is sound.** Most pages follow a consistent pattern: the route handler renders a scaffold with user identity, and the template fetches **real domain data from real `/api/v1/*` endpoints client-side** on load. `/lists`, `/todos`, `/insights`, `/transparency`, `/learning`, `/work-items`, `/projects/{id}`, and all 5 integration pages work this way and pull live data. The earlier "STUB" read (handler passes empty array) was a misread of an intentional SPA pattern.

2. **The real problem is reachability, not wiring.** **15 of 26 routes are nav-orphans** — reachable only by typing the URL. This includes `/insights` (the R4 surface we just shipped!), `/transparency`, `/files`, and every `/settings/integrations/*` page. This is why #1047 surfaces "couldn't be found": they exist and work, but nothing links to them.

3. **`/lists` and `/documents` aren't missing — they're trust-gated invisible.** Both nav links are gated to Stage 4+. m1-test is Stage 1 → the links are hidden → PM couldn't reach them during smoke. The pages work; the gating hid them.

4. **One genuinely-stale page**: `/standup` is the legacy "click to generate" UI; the lifecycle-indicator architecture that powers `/todos`/`/projects`/`/work-items` never reached it.

5. **One real bug**: `/documents` reads `window.trustStage` but its handler never server-renders it (unlike `/insights`, which #1132 fixed). Trust-gate fails silently unless the user visited home first.

6. **Five genuine placeholders**: `/account`, `/settings/privacy`, `/settings/advanced`, `/settings/projects`, `/personality-preferences` are "Coming Soon" / un-pre-populated form scaffolds.

**Bottom line for testability** (the #1142 raison d'être): once we (a) wire the orphan pages into nav and (b) fix the `/documents` trust_stage bug, the UI becomes UAT-navigable for a normal user. The M3 testability prerequisite is mostly a **navigation + reachability** fix, not a rebuild.

---

## Catalog

Verdict legend: **WIRED** (template fetches real data from working API) · **STALE-UI** (predates architecture) · **PLACEHOLDER** (coming-soon / no backend) · **BUG** (defect) · nav: **LINKED** / **ORPHAN** (URL-only) / **GATED** (nav link trust-gated).

| Route | Handler | Template | Verdict | Nav | Notes |
|---|---|---|---|---|---|
| `/` home | ui.py:114 | home.html | WIRED | LINKED | trust_stage server-rendered; adaptive greeting |
| `/standup` | ui.py:282 | standup.html | **STALE-UI** | LINKED ("Check in") | legacy generate-button; no lifecycle indicators (#1047 Surface 1) |
| `/learning` | ui.py:300 | learning-dashboard.html | WIRED | LINKED | client-fetch /api/v1/learning |
| `/transparency` | ui.py:328 | transparency.html | WIRED | **ORPHAN** | client-fetch conversations + audit-log; ADR-063 |
| `/insights` | ui.py:365 | insights.html | WIRED | **ORPHAN** | R4 + #1132 fixes verified; **the surface we just shipped has no nav link** |
| `/lists` | ui.py:484 | lists.html | WIRED | **GATED** (Stage 4+) | real /api/v1/lists CRUD; hidden from Stage-1 (#1047 Surface 2 reconciled) |
| `/todos` | ui.py:495 | todos.html | WIRED* | LINKED | client-fetch /api/v1/todos; *edit/delete are TODO stubs in template |
| `/projects` | ui.py:506 | projects.html | WIRED* | LINKED | client-fetch /api/v1/projects; *edit/delete TODO stubs |
| `/projects/{id}` | ui.py:517 | project_detail.html | WIRED | ORPHAN (linked from /projects) | real project + work-items fetch; lifecycle rendering |
| `/work-items` | ui.py:528 | work_items.html | WIRED | LINKED | client-fetch /api/v1/work-items; lifecycle indicators |
| `/files` | ui.py:344 | files.html | WIRED | **ORPHAN** | client-fetch /api/v1/files/list; CRUD wired |
| `/documents` | ui.py:352 | documents.html | **BUG** | GATED (Stage 4+) | handler doesn't pass trust_stage → window.trustStage undefined; gate fails silently |
| `/settings` | ui.py:310 | settings-index.html | WIRED (hub) | LINKED | nav card grid; no domain data needed |
| `/account` | ui.py:320 | account.html | **PLACEHOLDER** | LINKED | "Coming Soon" scaffold |
| `/personality-preferences` | ui.py:290 | personality-preferences.html | **PLACEHOLDER** | **ORPHAN** | form not pre-populated from prefs service |
| `/settings/integrations` | ui.py:424 | integrations.html | WIRED | **ORPHAN** | client-fetch /api/v1/integrations/health (real status) |
| `/settings/integrations/notion` | ui.py:434 | settings_notion.html | WIRED | **ORPHAN** | real connection status + live DB enumeration |
| `/settings/integrations/github` | ui.py:444 | settings_github.html | WIRED | **ORPHAN** | real connection status + live repo enumeration |
| `/settings/integrations/slack` | ui.py:454 | settings_slack.html | WIRED | **ORPHAN** | real OAuth/credentials status + channel enumeration |
| `/settings/integrations/calendar` | ui.py:464 | settings_calendar.html | WIRED | **ORPHAN** | real Google Calendar OAuth status |
| `/settings/projects` | ui.py:474 | settings_projects.html | **PLACEHOLDER** | **ORPHAN** | form scaffold, no project data |
| `/settings/privacy` | ui.py:536 | privacy-settings.html | **PLACEHOLDER** | **ORPHAN** | pure "Coming Soon" |
| `/settings/advanced` | ui.py:546 | advanced-settings.html | **PLACEHOLDER** | **ORPHAN** | pure "Coming Soon" |
| `/login` | ui.py:230 | login.html | WIRED (auth) | ORPHAN (entry) | redirects authed→home, no-users→setup |
| `/setup` | ui.py:270 | setup.html | WIRED (onboarding) | ORPHAN (entry) | fresh-install wizard |
| `/debug-markdown` | debug.py:24 | (inline) | **DEV-ONLY** | ORPHAN | markdown-renderer test page; NOT auth-gated — verify not registered in prod |

\* WIRED* = page loads real data but has incomplete CRUD (edit/delete TODO markers in template).

---

## Slash-command parity

Slash commands (`services/commands/definitions.py`): `standup`, `calendar_today`, `calendar_week`, `identity`, `discovery`, `status`, `priority`, `help` (8 total).

- **Routes WITH a matching slash command**: only `/standup`.
- **Routes WITHOUT a slash command**: all other 25 UI routes.
- **Slash commands WITHOUT a UI route**: `calendar_today/week`, `identity`, `discovery`, `status`, `priority`, `help` — these are chat-native actions, not page-shaped. Reverse-parity is expected here (not every chat command needs a page).

**Assessment**: PM's "every /keyword URL maps to a slash command and vice versa" principle is **aspirational, not currently honored**. Most page-routes have no slash equivalent. This is a design-decision surface, not a straightforward fix — many page-routes (settings, integrations) don't have a natural chat-command form. Recommend treating slash-parity as a **deliberate per-surface decision**, not a blanket mandate (file as design question, low priority).

---

## Key findings → recommended dispositions

1. **NAV-ORPHAN-PAGES (the big one)** — 15 of 26 routes have no nav link, including the freshly-shipped `/insights` (R4), `/transparency`, `/files`, and all integration pages. **This generalizes #1134** (which was Insight-Journal-specific). Recommend: **one consolidated issue** to wire orphan pages into nav (or deliberately decide which stay URL-only/programmatic). M3, medium-high — it's the core testability blocker.
2. **`/documents` trust_stage BUG** — handler doesn't server-render trust_stage (the exact bug #1132 fixed for `/insights`). Same fix pattern. Recommend: small fix, fold into the #1132 follow-up or file as a quick M3 bug.
3. **`/standup` STALE-UI** — already tracked via #1047 Surface 1 + #704. Confirm it lands in M3 UI work.
4. **Trust-gating-vs-reachability** — `/lists` + `/documents` Stage-4-gating made them invisible during Stage-1 smoke. Not a bug per se (gating is intentional), but **a UAT-methodology finding**: testing as a Stage-1 user can't reach Stage-4 surfaces. Recommend: seed a Stage-4 test user for UAT, OR a dev affordance to bump test-user stage (relates to #1143 composting-trigger-style test infrastructure).
5. **5 PLACEHOLDER pages** — `/account`, `/settings/privacy`, `/settings/advanced`, `/settings/projects`, `/personality-preferences`. Genuinely unbuilt. Recommend: confirm these are intended-future (not regressions) + ensure they're not nav-linked as if functional (`/account` IS nav-linked but is "Coming Soon" — mild Pattern-064 felt-shape risk).
6. **CRUD-incomplete**: `/todos` + `/projects` edit/delete are TODO stubs. Recommend: small completion tickets, M3 or M5.
7. **`/debug-markdown` not auth-gated** — verify `debug.py` router is dev-only / not registered in production. Quick security-hygiene check.

---

## Disposition recommendation for PM

The #1142 audit reframes the M2-smoke findings: **the architecture is wired; the navigation isn't.** The single highest-leverage M3 fix is **wiring orphan pages into nav + fixing the /documents trust_stage bug** — after that, the UI is UAT-navigable and the remaining items (placeholders, CRUD completion, slash-parity) are normal backlog.

Suggested issue spin-offs (pending PM nod):
- **NAV-WIRE-ORPHAN-PAGES** (M3, med-high) — finding #1
- **/documents trust_stage fix** (M3, small) — finding #2
- **UAT-test-user-stage affordance** (M3, small; pairs with #1143) — finding #4
- **debug.py prod-exposure check** (M3/M5, quick) — finding #7
- existing #704/#1047 covers standup (#3); #1134 folds into NAV-WIRE (#1)

---

## Method note

Three Explore agents ran in parallel with a shared rubric. The two route-group agents initially disagreed on the handler-scaffold + client-fetch pattern (one called it STUB, one WIRED); Lead Dev reconciled by verifying `/api/v1/lists` is a real CRUD router with DB sessions → confirmed the pattern is intentional SPA architecture, normalizing the verdict to WIRED-where-the-endpoint-is-real. Verdicts marked WIRED are high-confidence on the architecture pattern; per-endpoint data-correctness (does each `/api/v1/*` return *correct* data) was not exhaustively re-verified and is a deeper follow-up if needed.
