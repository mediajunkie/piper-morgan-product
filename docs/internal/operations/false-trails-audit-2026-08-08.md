# False-trail audit: parallel systems not deprecated, removed, or rewired-around properly

**Directive** (PM, 2026-08-08): "we need to start being more vigilant about parallel systems not being deprecated, removed, or rewired-around properly. Design an audit to scour the codebase for false trails that need to be removed and cauterized. They can make tests pass that shouldn't if left lying around."

**Method & layer (m-43)**: static analysis only — mount/include/fetch/import graphs traced from `main.py` → `web/app.py` → `web/startup.py`; no server run, no DB inspected, no GitHub API (rate-limited during audit). "Live" = statically reachable from the mounted app.

**Denominators**: 31 route modules in `web/api/routes/` (29 mounted, 2 unmounted) + 6 router-bearing `services/` modules outside plugins (1 mounted, 5 unmounted) + 2 dev-gated + 5 plugin routers (conditional, zero-load in default checkout). Templates: 63 (26 pages + 16 components/layouts live; 4 pages + 15 components dead — **48% of components included by nothing**). Static assets: 54 traced, 12 orphaned, + 14 loose dev files at `web/` root. Services: 67 top-level units import-graph swept (sub-package sweep non-exhaustive — first pass, not proof of absence). Capabilities covered: 10 (conversations, chat, todos, standup, insights, settings/integrations, auth, files, projects, places).

The week's five confirmed instances (two sidebars, two standups, four Slack OAuth starts, colliding feedback/todos routers, todos-vs-todo_items table) calibrated the sweep; findings below are additional or sharpened.

---

## Tier 1 — SHIPPING-DARK

**S1. `home.html` still carries the legacy conversation-item renderer** (CSS ~179–260, JS renderer ~1386–1416 with archive/delete buttons) alongside the live rail (`components/nav_rail.html`, #1280, populated by `static/js/nav.js`) and `components/history_sidebar.html`'s own third renderer (~493/696). Three conversation renderers in one page's reachable path + a fourth fully-dead one (`components/navigation.html`). Until excised, the next conversation fix can land in dead markup again (this week's incident, still armed). Excision requires a real `template.render()` test.

**S2. Places API: mounted route + serializer feeding a component that renders nowhere.** `web/api/routes/places.py` mounted at `/api/v1/places`, zero fetch callers; docstring advertises home's "What I'm seeing" panel via `components/place_window.html` (included by nothing — panel consolidated into Radar in #1236/`b8c1bba52`, whose `services/radar/sources.py` `PlaceProvider` "mirrors the /api/v1/places route"). Place logic exists twice; the mounted-but-uncalled copy is the documented one.

**S3. `services/api/health/staging_health.py` — documented ops contract that 404s.** `web-routes-conventions.md` (+ CLAUDE.md pointer) presents `/health/liveness`, `/readiness`, `/metrics` as the live ops exception; the router is imported by nothing. Any monitor pointed at documented `/health` paths is dark (live surface: `web/api/routes/health.py` at `/api/v1/health`). Same doc lists `loading_demo`/`conversation_context_demo` as live — both unmounted. Mount or cauterize + rewrite the exceptions doc; today it is affirmatively misleading.

## Tier 2 — COLLISION-ARMED

**C1. `/api/v1/todos` twins + a comment pointing at the wrong one.** Mounted `web/api/routes/todos.py` vs unmounted `services/api/todo_management.py` (identical prefix). The #1427 comment in `web/app.py` (~255) sits two lines above the LIVE mount — readable as either being the dead one. Hazard: live chat path (`todo_handlers.py`) imports `TodoCreateRequest`/`TodoUpdateRequest` **from the dead module** — model move required before deletion.

**C2. `/api/v1/feedback` twins — and the mounted one has no UI caller either.** `services/api/feedback_api.py`: zero importers incl. tests → delete outright. No template/JS fetches `/api/v1/feedback` at all; `services/feedback/` is the live machinery. Decide if the mounted REST surface is API-first-by-design or a third trail.

**C3. `/api/v1/slack` unmounted monitoring router (8 endpoints)** — only prod importer of `services/debugging/` (slack_inspector), a diagnostics package alive only through a dead chain.

**C4. Slack OAuth initiation four-way** (precise coordinates): `settings_integrations.py` connect ~347 / authorize ~412; `setup.py` oauth/start ~1283 + slack-credentials ~791; `webhook_router.py` HTTP router (never mounted; class live via socket runner — half-alive module) + committed 857-line `webhook_router.py.security-fix-backup`.

**C5. Stale full pages URL-reachable in prod NOW**: `web/assets/standup.html` + `personality-preferences.html` served verbatim at `/assets/*` (unconditional StaticFiles mount) beside live `/standup` + `/personality-preferences` — old links resurrect pre-refactor UI without current auth/UX.

**C6. Five message-renderer files, one live**: live `web/assets/bot-message-renderer.js` (home.html); trails: `markdown-renderer.js` (debug page only), `-v2.js`, `-v3.js` (nothing), stale root `web/bot-message-renderer.js` (same name, unserved).

**C7. Documents API mounted; its only fetch callers are dead templates** (`documents.html`, `components/document_window.html`); live browser is `files.py`/`files.html` (#1270 redirect). Upload fixes have a mounted, plausible, uncalled twin.

**C8/C9. Dead chrome twins**: `components/navigation.html` (+orphan `nav.css`, still includes chat-widget) vs live nav_rail; `layouts/base.html` (nothing extends) vs live `layouts/app_shell.html` (24 pages).

## Tier 3 — MISLEADS-AUDITS ("tests that pass that shouldn't")

| Dead code | Passing tests pinning it |
|---|---|
| `services/api/todo_management.py` (C1) | `tests/integration/test_todo_management_persistence.py`; `test_todo_full_stack.py` (its item/todo_service chain) |
| `services/queries/` (ConversationQueryService, zero prod importers) | `test_temporal_context_standalone.py`, `test_temporal_context_integration.py` |
| `services/persistence/` (second persistence layer: ActionHumanizationDB; zero prod importers) | `tests/security/test_schema_reconciled_1312.py`, `test_humanized_workflow_messages.py` |
| `services/config_validator.py` ("stub for CI") | `tests/performance/test_config_performance.py` |
| Slack webhook HTTP surface (C4) | `test_webhook_oauth_url_1339.py`, `test_ngrok_webhook_flow.py` — green tests on URLs no route serves |

**M-extra 1**: `services/persistence` ships migration `8ef0aa7cbc90` (+ merge-head `3659cb18c317`) — `action_humanizations` table exists in every DB, read/written by zero prod code (live `action_humanizer.py` runs uncached). Same class as the standup-interview tables and `todos` table.
**M-extra 2 (m-44)**: `pytest.ini` `--ignore=services/integrations/*/tests` — every test there **never runs**; existence reads as coverage and isn't.

## Tier 4 — INERT (opportunistic removal)

I1 root Next.js scaffold (package.json "site", Next 15, no app/ — cannot build; biggest "wrong repo?" trail) · I2 unwired error pages (404/500/network-error + error-page.css; #283 handler returns JSON — wire-or-delete is a product call) · I3 `home-modules.js/css` (loads removed in #1236, files left) · I4 15 dead components/layouts (insight_card, insight_controls, place_window, document_window, greeting_context, channel_continuity, lifecycle_*, preference_suggestion, privacy_mode, reflection_summary, skeleton+css, spinner, navigation, base) · I5 zero-importer services (`service_registry.py` — dead twin of live `container.py`; `version.py`; `editorial/`; `analytics/` (empty); `user/` (self-documented shell); `api/middleware.py`; `api/health/mcp_health.py`) · I6 committed backups (`web/app.py.backup-personality`, slack `webhook_router.py.security-fix-backup`, `requirements.txt.bak`, `config/PIPER.md.backup-20251101`, 4× `backup_before_phase2_*.sql`) · I7 `web/` root debris (11 ad-hoc test-*.js, debug files, REFACTOR_TODOs, `ba.sh`, `git.sh` → dead branch) · I8 unmounted demo routes documented live · I9 `MultiAgentWorkflowProgress.jsx` in a Jinja app · I10 orphan `static/admin/compose.js/css`. Noted, not dead: `services/config/` AND `services/configuration/` both live — naming hazard, not a cauterization target.

## Proposed cauterization order

1. **Disarm fix-magnets in live files**: excise home.html legacy renderer (render-test-gated); fix the #1427 comment placement; fix or supersede places.py docstring.
2. **Same-prefix unmounted routers** via delete-module-safely, one family per commit, Tier-3 tests deleted in the SAME commit: todo_management (move request models to `services/todo/` first), feedback_api, slack_monitoring (+ decide `services/debugging/`), staging_health + mcp_health or mount them — either way rewrite the conventions doc.
3. **Decide Places** (wire a caller or unmount + delete place_window; Radar becomes sole impl). Same decision for documents vs files (C7).
4. **Kill URL-reachable stale pages + renderer clones** (C5, C6).
5. **Dead template/component/CSS batch** (C8/C9/I2–I4) — one grep-gated commit; PM/CXO makes the 404/500 wire-or-delete call.
6. **Tier-3 test deletions ride with their modules** (never one without the other). Decide `services/persistence` + `action_humanizations`: wire the cache or add a drop migration.
7. **INERT sweep** (I1, I5–I10).
8. **Ratchet so the class can't regrow** (the durable fix, mirroring TestPreFloorDispatchSiteRatchet): architecture-enforcement test asserting (a) every APIRouter is mounted or allowlisted-with-reason; (b) every template reachable from a render/include graph or allowlisted; (c) every static js/css referenced or allowlisted; (d) no `*.bak`/`*.backup*` under web/, services/, config/. Allowlist entries are visible, reviewed false trails instead of invisible ones.

*Read-only static pass, 2026-08-08. Runtime verification is the step-8 ratchet's job; services sub-package sweep non-exhaustive.*
