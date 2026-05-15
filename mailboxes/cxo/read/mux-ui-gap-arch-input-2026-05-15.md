# MUX/UI Gap — Architect Input (state-shape + routing for 7 UI surfaces)

**From**: Architect (Chief Architect)
**For**: CXO MUX/UI gap cohort scoping pass (#1090; CXO May 15 memo)
**Date**: 2026-05-15 (filed 5 days ahead of Wed May 20 EOD target per CEO bias-to-action direction)
**Methodology**: Subagent codebase exploration (services/, web/api/routes/, templates/, web/static/) + Architect synthesis. All claims grounded in actual code paths verified today.

---

## Quick navigation

- Surfaces 1, 2, 3 cluster on **user-history substrate** (ConversationDB + UserHistoryService + `/api/v1/users/me/history`)
- Surfaces 4, 5 cluster on **independent-infrastructure-decisions** (OAuth lifecycle + search-index strategy — "pick once, build to it")
- Surfaces 6, 7 cluster on **empty-state / degraded-state design-system** (typology of "Piper-has-nothing" vs. "Piper-can't")
- **LLM-touch surfaces (ADR-061 four-element principle applies)**: Surface 7 (direct, load-bearing) + Surface 5 (if LLM-mediated reranking in scope) + Surface 2 (indirect: audit envelope on privacy flips is element-4 for downstream gated surfaces) + Surface 6 (adjacent if first-meeting greetings use LLM composition)

---

## Surface 1 — Conversation history / archive UI

**Exists** (substantial):
- DB: `is_private`, `turn_count`, `topics` on `ConversationDB` (`services/database/models.py:1059`); index `idx_conversations_user_private`
- Repository: `search_for_user` (`services/database/repositories.py:1351`), `search_conversations` (`:1716`)
- Service: `UserHistoryService` (`services/memory/user_history.py`) with pagination, search, mark/unmark private; `ConversationSummary` + `ConversationDetail` dataclasses
- API: `/api/v1/users/me/history` (list/search/detail/privacy PATCH) at `web/api/routes/user_history.py`; older `/api/v1/conversations?search=` at `web/api/routes/conversations.py:262`
- **Two parallel sidebars**: left rail (`templates/home.html:941`, "#565") fed by `/api/v1/conversations`; right slide-out (`templates/components/history_sidebar.html`, "#425 MUX-IMPLEMENT-MEMORY-SYNC") designed against `/api/v1/users/me/history` but **not yet calling it**
- Command palette: `history-view` `⌘H` at `templates/components/command_palette.html:457`

**Needs build**: reconciliation between the two sidebars (collapse to one or assign clear roles). Open/replace semantics — clicking a history item navigate vs. replace vs. modal — not clearly defined in either component's JS.

**Routing**: `/` home shows left rail; ⌘H opens right slide-out. No dedicated `/history` route exists.

**Architectural risks**:
- Two parallel surfaces with overlapping intent and incompatible API choices (Pattern-063 candidate at frontend layer)
- Search is ILIKE-based (`:1391`, `:1745`); explicitly notes "loses GIN index for topic-only matches" at `:1742`. Scaling cliff at ~10k rows/user
- No dedicated full-text index (no tsvector / no pg_trgm); substring-only

**Four-element-principle relevance**: not LLM-touch (deterministic SQL).

---

## Surface 2 — Privacy / per-conversation controls

**Exists** (substantial):
- Column + index: `is_private` on `conversations` (`services/database/models.py:1059`)
- Session-level: `services/memory/privacy_mode.py` — `PrivacyState` (`:50`), `PrivacyModeManager.is_private` (`:164`)
- Recording skip: `services/memory/session_hooks.py:43`
- API: `PATCH /api/v1/users/me/history/{id}/privacy` (`web/api/routes/user_history.py:152`)
- UI: privacy banner styling (`templates/components/privacy_mode.html`); toggle footer at `:316` of history sidebar; per-conversation `is_private` icon at `:330`
- Stub page: `templates/privacy-settings.html` ("Coming Soon" — Advanced Privacy Controls)
- Command palette: `history-private` (`:491`)

**Needs build**: per-message privacy is not modeled (only per-conversation + session-level banner). Retroactive marking referenced in docstring but no UI affordance verified. `/settings/privacy` page is a Coming-Soon shell.

**Routing**: per-conversation toggle inline in history sidebar; session-level banner global; `/settings/privacy` dedicated route (stub).

**Architectural risks**:
- **Audit-envelope coupling**: every privacy flip should generate an audit event per #1018 audit_transparency durability; wire-up to surface not verified beyond `logger.info` in route handler
- Per-message vs per-conversation is a design decision pending. If per-message added, `messages` table needs `is_private` column + propagation rule (whole conversation or just the turn?)

**Four-element-principle relevance**: **indirect**. Privacy gates downstream LLM-touch (private = no history fed to LLM); audit envelope on flip-events is element-4 of the principle for those downstream surfaces.

---

## Surface 3 — Settings / preferences

**Exists** (partial — many shells, few bodies):
- Index page: `/settings` → `templates/settings-index.html` with 7 card links (`:181–259`)
- **Real**: personality-preferences (`web/api/routes/preferences.py`), learning dashboard (`web/api/routes/learning.py`), integrations (Surface 4)
- **Coming-Soon stubs**: account (`templates/account.html:216`), privacy (Surface 2), advanced (`templates/advanced-settings.html`)
- Model selection: `services/llm/config.py:3` config-file only, no UI

**Needs build**: account profile editing (name/email/avatar), notification toggles, model selection UI, workspace prefs.

**Routing**: `/settings` index with sub-routes already in place (`/settings/integrations[/{name}]`, `/settings/privacy`, `/settings/advanced`, `/settings/projects`, `/account`, `/personality-preferences`, `/learning`).

**Architectural risks**: danger of mistaking page-shell-existence for feature-existence (the Coming-Soon pattern is widespread here — possibly six surfaces with shells, three with bodies). `PreferenceManager` + `PersonalityProfile` + `UserPreferenceManager` are three overlapping services that need coordination before adding new settings.

**Four-element-principle relevance**: model selection UI, if added, affects which model handles all downstream LLM-touch surfaces but is not itself LLM-touch.

---

## Surface 4 — Integration setup wizards

**Exists** (substantial):
- Plugin convention: `services/integrations/{notion,github,slack,calendar}/` each with `oauth_handler.py` (Slack/Calendar), `config_service.py`, `*_integration_router.py`, `*_plugin.py`
- OAuth flows: `web/api/routes/settings_integrations.py:323` (Slack start), `:373` (callback); `integration_config_service.py` covers Google/Slack/GitHub credential storage
- Per-integration pages: `templates/settings_notion.html`, `_github.html`, `_slack.html`, `_calendar.html`
- Overview: `templates/integrations.html` with status dots (`healthy`/`degraded`/`failed`/`unknown`/`not_configured` at `:198–203`), test/connect/disconnect actions, fix-suggestion at `:294`
- First-run wizard: `/setup` → `templates/setup.html` (multi-step, Issue #390)

**Needs build**: per-step consent screens with explicit scope display (OAuth URLs constructed in handlers but scope-explanation UX thin); dedicated re-auth flow when tokens expire mid-session; consolidated error-state surfaces. **#1075 route-prefix migration may affect callback URLs.**

**Routing**: `/setup` (first-run), `/settings/integrations` (overview), `/settings/integrations/{name}` (per-integration). Dedicated routes — appropriate.

**Architectural risks**:
- **OAuth callback URL stability** under #1075 prefix migration (some routes still un-versioned)
- Per-integration plugins use independent `config_service.py` — no shared credential-rotation lifecycle
- `integration_config_service.py` mixes app credentials (GitHub) with user tokens — conceptual split needed
- State-machine for "connecting → connected → failed → re-auth required" isn't centralized

**Four-element-principle relevance**: not LLM-touch directly (OAuth ceremony is deterministic). Connected integrations feed natural-language descriptions into downstream LLM-touch surfaces.

---

## Surface 5 — Search interface

**Exists** (partial / fragmented):
- Conversation/history search: see Surface 1
- Documents search: `web/api/routes/documents.py:361` (`/search`)
- Knowledge-graph search: `web/api/routes/knowledge_graph.py:269` (`search_term` param)
- Semantic indexing scaffolding: `services/knowledge/semantic_indexing_service.py` ("Prepares for future pgvector integration") — **unused**
- UI: search input inside history sidebar; per-page search on docs/files. **No global cross-history search entry point.**

**Needs build**: unified search surface spanning conversations + documents + KG. Currently three separate ILIKE/keyword paths with no result-fusion. No global search bar in nav.

**Routing**: probably command-palette-driven + a `/search` dedicated route, OR a global search bar in `templates/components/navigation.html`. Not modeled yet.

**Architectural risks**:
- **Index decision is load-bearing.** ILIKE works for <10k rows but doesn't return relevance-ranked results. pgvector scaffolding exists but unused; tsvector/pg_trgm not in play. **Choose-once decision** — wrong choice forces migration later.
- Result-type heterogeneity (conversation summaries vs. document chunks vs. KG nodes) needs unifying response envelope
- Cross-source ranking is non-trivial

**Four-element-principle relevance**: **applies if** natural-language search invokes LLM-mediated reranking or query expansion. Then all four elements load-bearing: permissive input (free-text query), schema validation at consumption (parse reranked results), safe fallback (keyword search if LLM rerank fails), audit envelope (query, results returned, rerank decisions). Pure-keyword search is not LLM-touch.

---

## Surface 6 — Empty / first-run states

**Exists** (partial):
- Reusable component: `templates/components/empty-state.html` (with documented consciousness pattern integration)
- In use: `templates/todos.html:143–158`, `files.html:209–212`, `home.html:246, :613, :1307, :1317`
- First-meeting detection: `services/onboarding/first_meeting_detector.py`, `services/onboarding/grammar_context.py:47` (`is_first_meeting`)
- Setup wizard: `/setup` (Surface 4)
- Consciousness helper: `services/consciousness/` provides `get_empty_state_data("todos"|"files"|"projects"|"lists"|"conversations"|"integrations")`

**Needs build**: composed first-run home experience after setup completes — what does `/` show with zero conversations, zero integrations, zero documents? The empty-state *component* exists but the **first-run journey** doesn't have a dedicated artifact. Onboarding tooltips referenced at `home.html:613` but completeness not verified.

**Routing**: post-setup → `/` with first-run state. No dedicated route.

**Architectural risks**: trust-stage gating (`window.trustStage = 1` for new users) interacts with empty states — some content is gated by trust stage and some by data presence; the two systems can interfere.

**Four-element-principle relevance**: not LLM-touch (deterministic templating). **Adjacent if** first-meeting greetings use LLM composition — `first_meeting_detector.py` + `grammar_context.py` interface needs verification before scoping.

---

## Surface 7 — Error / degraded states

**Exists** (partial):
- Page-level: `templates/network-error.html`, `templates/404.html`, `templates/500.html`
- Toast system: `templates/components/toast.html` + `web/static/js/toast.js` (aria-live region)
- Integration degraded states: visualized in `templates/integrations.html:200–211`
- Audit envelope substrate: #1018 audit_transparency durability landed May 2

**Needs build**: degraded-LLM state UI (slow model, fallback model) — no verified surface. Tool-error standardized handling (when MCP tool call fails mid-conversation). **Audit-envelope user-facing read** (why did Piper decline / route to fallback?) doesn't have a UI yet.

**Routing**: in-line toasts + per-page degraded banners. Likely needs a dedicated `/status` or similar for tool/integration health.

**Architectural risks**:
- **Audit-envelope read-surface is the load-bearing missing piece** — without it, ADR-061's element 4 is invisible to users (logged but unreadable)
- Toast vs. banner vs. full-page-error needs a hierarchy (currently ad-hoc)
- Tool-error messages are likely composed via LLM (LLM-touch surface) but failure-mode envelope isn't standardized

**Four-element-principle relevance**: **direct, load-bearing**. Tool-error + degraded-LLM surfaces consume LLM output to compose user-facing apology/explanation. All four elements need to be present: permissive input shape (raw error from tool/model), schema validation at consumption (parse the error), safe-fallback path (canned response if LLM also fails), audit envelope (which tool, what error, what message shown).

---

## Architect cross-surface observations

- **The Coming-Soon-stub pattern is the biggest discovery surface**. Surface 3 has six routes that look like settings pages but are mostly shells. Distinguishing "real page" vs. "stub" should be the first synthesis exercise — the 7-surface count understates the actual scope because the 7 contain 15+ sub-surfaces with very different completion states.
- **Two parallel implementations of the same conversation-history UI (Surface 1)** is a Pattern-063 candidate at the frontend layer. The two sidebars + two APIs + two issue numbers (#565 + #425) are the same shape as the Pattern-067 wild instances at the issue-tracking layer this week. Worth catching at scoping time before per-surface build effort goes into both.
- **#1075 route-prefix work in flight intersects Surface 4** (integration OAuth callbacks may be on legacy `/transparency` or `/admin` routes that are migrating). Worth flagging to Lead Dev as a sequencing dependency.
- **The Surface 7 audit-envelope read-surface gap is the most architecturally consequential missing piece.** Without it, ADR-061's element 4 produces audit data that nobody can see; the four-element principle becomes 3.5 elements in user-facing terms. **Highest single-priority architectural gap among the seven surfaces from Architect lens.**

---

*Architect lens — state-shape + routing focus. PPM (product-priority), CXO (design priorities + MUX-doc shape), Comms (voice consistency), Lead Dev (build-cost) each bring complementary lenses per the May 15 cohort-convene memo. Open to refinement on any specific risk or surface during synthesis pass.*
