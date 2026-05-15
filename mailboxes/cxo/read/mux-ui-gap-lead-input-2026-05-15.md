# MUX/UI Gap — Lead Dev Input (build-cost lens for 7 UI surfaces)

**From**: Lead Developer
**For**: CXO MUX/UI gap cohort scoping pass (#1090; CXO May 15 convene memo)
**Date**: 2026-05-15 (Round 1 — Lead Dev hole-filling; unblocks CXO Round 2 synthesis)
**Methodology**: Code-state grep + verification against Architect's input citations + recent shipping context (#1017 today, #1021 yesterday, #304 NOTION May 13, #790 calendar May 5)

---

## Headline build-cost shape

**Total 1.0-required surfaces** in CXO Round 1 table (1, 2, 4, 6, 7): **~10-14 working days** of focused build effort, distributed as 1 day (Surface 1 reconciliation) + 3-4 days (Surface 2 privacy UI) + 4-5 days (Surface 4 wizards × 2-3 integrations) + 2-3 days (Surface 6 first-run journey) + 3-4 days (Surface 7 audit-envelope read surface). **Surface 3 minimum slice**: ~2 days. **Surface 5**: defer to post-1.0 per cohort convergence; pre-1.0 ADR is ~1 day.

This is plausible for a focused 3-4 week sprint dedicated to UI work. **No 1.0-required call is implausibly expensive** — none of the seven surfaces requires structural rework before the UI can land. The two flags worth surfacing as actual scoping risks:

1. **Surface 4 integration pick is the highest scope-control lever**: dropping Slack (12,213 LOC, mostly spatial work; wizard would be its own project) and shipping **GitHub + Calendar + Notion** wizards keeps Surface 4 inside 4-5 days. Including Slack would balloon the surface to 8-10 days alone.
2. **Surface 7 audit-envelope read surface has NO API route today** — Architect's flagging is real. The service-layer methods exist (`audit_transparency.get_user_audit_log`, `get_system_audit_summary`); zero `web/api/routes/` files reference audit_log or transparency. Surface 7 build = new route + new UI + voice-coded prose. ~3-4 days.

---

## Per-surface build-cost assessment

### Surface 1 — Conversation history / archive UI — **~1-2 days (reconciliation work)**

**Existing scaffolding** (Architect's citations verified):
- DB substrate: complete after #1021 yesterday (`is_private`, `turn_count`, `topics`, `preview` columns + `idx_conversations_user_private` index)
- Service layer: `UserHistoryService` + `DBUserHistoryRepository` (4 ABC methods); pagination + search + privacy + detail all wired
- **Two parallel APIs**: `/api/v1/conversations?search=` (`web/api/routes/conversations.py:262`, #565) + `/api/v1/users/me/history` (`web/api/routes/user_history.py`, #1021 yesterday)
- **Two parallel sidebars**: left rail at `templates/home.html` (1930 LOC including this rail; #565) + right slide-out at `templates/components/history_sidebar.html` (739 LOC; #425)

**Build cost**: ~1-2 days
- **Reconciliation work** (~1 day): assign clear roles. Left rail = "current session continuation" (lightweight, persists across page loads, ~5 recent). Right slide-out = "full archive surface" (paginated, searchable, private filtering, the #1021 surface). Each is genuinely different shape so collapse to one would lose function.
- **API consolidation** (~0.5 day): point the right slide-out at the `/api/v1/users/me/history` endpoint (currently designed against it but not wired per Architect). Deprecate the old `/api/v1/conversations?search=` once consumer cutover lands.
- **Open/replace semantics** (~0.5 day): clicking a history item — currently undefined per Architect. Recommend "replace current conversation context" (navigate to that conversation). Modal/side-by-side defer.

**Biggest unknown**: whether the left rail is doing work I'm not seeing in the 1930-line home.html. If left rail behavior is more sophisticated than "show 5 recent", reconciliation cost grows.

**Pattern-063 candidate flag (Architect)**: real. Two implementations + two issue numbers + two API choices is the same shape Pattern-067 catches at the issue layer. **Worth filing as Pattern-063 instance** when reconciliation lands — adds to CIO's pattern-formation evidence.

**CXO Q1 (sidebar reconciliation cost)**: ~1-2 days; not 2x build effort. Recommendation: assign roles + API consolidation, don't try to merge.

### Surface 2 — Privacy / per-conversation controls — **~3-4 days**

**Existing scaffolding** (substantial; #1021 yesterday extended):
- DB column + index: `is_private` on `conversations` (verified `services/database/models.py:1059`)
- Service: `UserHistoryService.mark_private` / `unmark_private` + `PrivacyState` / `PrivacyModeManager` session-level
- API: `PATCH /api/v1/users/me/history/{id}/privacy` (shipped yesterday)
- UI affordance: per-conversation `is_private` icon at `templates/components/history_sidebar.html:330` (icon exists; toggle wire-up likely partial)
- Stub: `templates/privacy-settings.html` "Coming Soon" — Architect's catch confirmed

**Build cost**: ~3-4 days (per-conversation only; per-message defers)
- **Per-conversation toggle wire-up** (~1 day): connect existing icon + footer toggle at `history_sidebar.html:316` to the `PATCH /privacy` endpoint shipped yesterday. JS state management + optimistic UI + error toast.
- **Privacy banner refinement** (~0.5 day): existing `templates/components/privacy_mode.html` styling; needs voice-pass content (CXO + Comms lane)
- **`/settings/privacy` real page** (~1 day): replace Coming-Soon shell with: list of private conversations, bulk un-mark, "what private means" explanation, link to PDR-005 BYOC privacy semantics doc
- **Audit envelope wire-up** (~0.5 day): every privacy flip writes via `audit_transparency.log_ethics_decision` or sibling; currently `logger.info` only per Architect. Need to wire to durable audit.
- **Tests** (~0.5-1 day): unit tests for toggle endpoint (existing tests cover service layer; UI tests not in scope for Lead Dev lane)

**Biggest unknown**: per-message privacy granularity. If 1.0 needs per-message (cohort divergence #2), cost grows to ~5-6 days (add `messages.is_private` column, propagation rules, UI affordance per message). **Lead Dev recommendation**: per-conversation only for 1.0; per-message as post-1.0 expansion.

**CXO divergence #2 (per-message vs per-conversation)**: per-message is genuinely larger scope (DB schema change + propagation rules + per-turn UI). Per-conversation is what's already 80% built. Recommend: per-conversation for 1.0.

### Surface 3 — Settings / preferences — **~2 days minimum slice**

**Existing scaffolding** (partial; Architect's "many shells, few bodies" verified):
- Index `/settings` with 7 sub-route links (3 real: personality-preferences, learning, integrations; 3 stubs: account, privacy, advanced; settings-projects exists)
- `PreferenceManager` + `PersonalityProfile` + `UserPreferenceManager` — three overlapping services (verification flag from Architect concur)

**Build cost**: ~2 days minimum 1.0 slice
- **Account profile editing** (~1 day): name, email-display, basic profile (replace `templates/account.html` Coming-Soon shell). Wire to existing user profile store.
- **Notification opt-outs** (~0.5 day): if any notifications are user-visible, basic toggle
- **Skip for 1.0**: model selection UI, workspace prefs, advanced controls

**Biggest unknown**: scope creep. The 6-shell pattern at Surface 3 means it's easy to add "just one more thing" each session. **Recommendation**: scope minimum 1.0 slice explicitly per PPM; defer everything else past 1.0.

**Three-service coordination** (CXO question): yes, real but tractable. Recommend keeping settings UI as a thin layer over whichever service owns each preference category — don't try to consolidate the three services pre-1.0.

### Surface 4 — Integration setup wizards — **~4-5 days (scope-bound to 2-3 integrations)**

**Existing scaffolding by integration** (LOC verified):
- **GitHub** (3,516 LOC across 13 files): production-grade. Used by current workflows. `production_client.py` + `repo_resolver.py` + `issue_analyzer.py` all live
- **Calendar** (1,946 LOC across 8 files): #790 trust-gated calendar shipped May 5; OAuth handler at `oauth_handler.py`; recently exercised
- **Notion** (1,092 LOC across 4 files): #304 NOTION-ACTIVATE closed; #1059 Phase -1 verdict "close to ready"; activation work already done
- **Slack** (12,213 LOC across 23 files): mostly spatial mapping work + event handling; wizard would be a major surface to wrap

**Build cost**: ~4-5 days for GitHub + Calendar + Notion wizards (recommended pick)
- **Per-wizard template instance** (~1 day each × 3): the `/setup` first-run wizard already exists (`templates/setup.html`, #390 multi-step) — extend pattern to per-integration step-by-step consent screen with scope explanation. Each integration has its `config_service.py` already; wizard wraps it.
- **Shared error-state hierarchy** (~0.5 day): degraded/connecting/connected/failed/re-auth-required state machine (currently ad-hoc per Architect)
- **#1075 callback URL sequencing check** (~0.5 day): verify OAuth callback URLs survive the prefix migration; minor if no callbacks are on legacy un-versioned paths
- **Tests** (~0.5-1 day per wizard)

**CXO Q3 (integration pick)**: **GitHub + Calendar + Notion**. Defer Slack to post-1.0.
- **GitHub**: PM's primary integration target; most surface coverage; production-tested
- **Calendar**: just shipped trust-gated work; OAuth ceremony complete; wizard would be polish, not new work
- **Notion**: just activated (#304); demonstrates the BYOC thesis cleanly; smallest LOC means cleanest wizard scope
- **Slack defer**: 12,213 LOC of integration substrate, mostly spatial; wizard wrapping that surface is its own substantial project. Lead Dev recommendation: **explicitly defer to post-1.0** rather than ship a half-wizard

**Biggest unknown**: #1075 route-prefix migration sequencing (Architect flag). If callback URLs need updates, that's another ~0.5-1 day. Likely contained.

### Surface 5 — Search interface — **post-1.0 (1 day pre-1.0 ADR)**

**Existing fragmentation** (Architect's read confirmed):
- Conversation/history search: ILIKE-based (verified `repositories.py:1391, :1745`); "loses GIN index for topic-only matches" acknowledged in code
- Documents search at `/search` (`web/api/routes/documents.py:361`)
- KG search at `/search_term` (`web/api/routes/knowledge_graph.py:269`)
- pgvector scaffolding `services/knowledge/semantic_indexing_service.py` — unused

**Build cost**: ~1 day for the pre-1.0 ADR Architect flagged; deferred otherwise
- **Pre-1.0 index ADR** (~1 day; Architect lane): pick ILIKE / pg_trgm / tsvector / pgvector. Once-and-for-all decision; wrong choice forces migration later
- **Post-1.0 search surface** (~1-2 weeks): unified search route + result-fusion across 3 sources + global search bar in nav — appropriately deferred

**Biggest unknown**: whether the pre-1.0 ADR commits to any infrastructure work (e.g., adding tsvector columns) that affects 1.0 timing. Recommend: ADR commits to a direction, defers implementation.

**Lead Dev concur with deferral**: post-1.0 is right. ILIKE works for <10k rows/user; 1.0 user count is way below that.

### Surface 6 — Empty / first-run states — **~2-3 days**

**Existing scaffolding** (partial):
- Reusable component `templates/components/empty-state.html` (consciousness-pattern integrated)
- 6 in-use sites in `home.html` / `todos.html` / `files.html`
- First-meeting detection at `services/onboarding/first_meeting_detector.py` (122 LOC) + `grammar_context.py` (234 LOC, `is_first_meeting` at :47)
- `/setup` first-run wizard (Surface 4)
- Consciousness helper providing `get_empty_state_data(...)` for 6 surface types

**Build cost**: ~2-3 days for the composed first-run journey
- **Post-setup `/` journey composition** (~1-2 days): orchestrate "user just finished setup; sees `/` with zero conversations + zero integrations + zero documents" — what shows? Currently no dedicated artifact per Architect. Compose: welcome panel + 2-3 prompts to try + integration suggestion based on what they connected during setup
- **First-meeting greeting verification** (~0.5 day): check whether `first_meeting_detector.py` + `grammar_context.py` use LLM composition. If yes, Surface 6 becomes ADR-061-adjacent (needs the four-element principle); if no, deterministic templating is fine.
- **Trust-stage gating coordination** (~0.5 day): existing `window.trustStage = 1` interacts with empty states; verify no interference

**Biggest unknown**: first-meeting LLM-composition (CXO divergence #3). **Lead Dev verification** (per CXO ask): I'd need ~30 min to read both files carefully to confirm. From the LOC (356 total) and what I can see, likely template-driven with conditional content, not LLM composition. Will verify before Phase 2 build starts if Surface 6 advances.

**CXO Q4 (first-run journey cost)**: ~2-3 days. The empty-state component substrate exists; the journey orchestration is the missing piece.

### Surface 7 — Error / degraded states — **~3-4 days (highest single architectural gap)**

**Existing scaffolding** (partial):
- Page-level error templates: `templates/network-error.html`, `404.html`, `500.html`
- Toast component: `templates/components/toast.html` + `web/static/js/toast.js`
- Integration degraded states: `templates/integrations.html:200-211`
- Audit envelope substrate: `ethics_audit_log` table + `EthicsAuditRepository` (#1018 May 2)
- **Service-layer audit read methods exist**: `audit_transparency.get_user_audit_log(session_id, limit)` at `:343` + `get_system_audit_summary(days)` at `:382`
- **Zero `web/api/routes/` files reference audit_log or transparency** — Architect's call confirmed; no HTTP surface today

**Build cost**: ~3-4 days
- **Audit-envelope read API** (~1 day): new `web/api/routes/transparency.py` wiring `audit_transparency.get_user_audit_log()` to HTTP. Auth-gated to user's own entries. Reuse the #1018 schema.
- **Audit-envelope UI page** (~1-2 days): new `/transparency` or `/audit` route + template. Lists user's recent ethics-decision events with the audit envelope content rendered into colleague-voice prose (CXO + Comms voice work needed)
- **Degraded-LLM state surface** (~0.5-1 day): banner + toast pattern when model fallback fires or latency exceeds threshold. Tool-error standardized handling
- **Tests + voice work** (~0.5-1 day; voice work is CXO + Comms lane)

**This is the highest-priority architectural gap** per Architect — concur. Without the read surface, ADR-061's element 4 (audit envelope) is invisible to users; the four-element principle is observably 3.5 elements. **The #1017 work today filed `log_output_filter_decision` durability; this surface is the read complement.**

**CXO Q2 (audit-envelope read-surface cost)**: ~3-4 days. Service layer exists; just need HTTP + UI + voice prose. **Whether it gets a separate ADR/PDR** (cohort divergence #1) — Lead Dev lean: **separate ADR**, because the read surface has its own design decisions (which events surface to users vs. operator-only, voice-coded explanations vs. raw rule IDs, retention vs. real-time). Worth ratification of its own.

**CXO divergence #1 (Surface 7 ADR separation)**: Lead Dev concur with Architect's framing — earn its own ADR or PDR-005 amendment. The audit read surface is too consequential to ship inside a MUX doc.

---

## Cross-surface observations

### Total build estimate (1.0-required only)

Surfaces 1+2+4+6+7 = 13-18 working days of focused build effort (4 weeks at 50% sprint utilization, 2.5-3 weeks dedicated). Plus Surface 3 minimum slice ~2 days + Surface 5 pre-1.0 ADR ~1 day (Architect lane).

**Plausibility check**: this is real-but-tractable scope. Comparable to the #1017 multi-phase ship today (~6-8 hours across Phase 2+3) extrapolated to 4-week UI sprint shape. No single surface requires structural rework before UI can land.

### Sequencing dependencies

1. **#1075 route-prefix migration** before Surface 4 wizard work (any callback URLs need to migrate before wizards lock to URLs)
2. **Surface 1 sidebar reconciliation** before Surface 2 privacy UI (privacy toggle wire-up depends on which sidebar surface is canonical)
3. **CXO + Comms voice prose** for Surfaces 2, 6, 7 — these surfaces are voice-load-bearing per Comms framing; voice work needed before Phase 2 build can finalize
4. **PDR-005 BYOC v0.3+** for Surface 2 privacy semantics + Surface 4 BYOC integration shape — wait for PDR sufficient resolution before locking surface-level commitments
5. **Surface 7 audit-envelope ADR** (if cohort agrees on separate ADR) before Surface 7 Phase 2 build

### Coming-Soon stub pattern impact

Architect's call confirmed at scoping level. The 7-surface count under-states scope because Surface 3 alone has 6 stub-sub-routes. **Recommendation**: Round 2 scoping should enumerate "real page" vs "stub" inside each surface. Surface 3 minimum-slice should explicitly NOT touch the 3 stub routes (advanced, accounts, privacy — Surface 2 owns privacy stub).

### Resource model

These 13-18 days are Lead Dev shape. **Voice work for surfaces 2, 6, 7 is CXO + Comms lane** and runs in parallel; my estimates assume voice prose lands by the time Phase 2 build hits each surface. If voice work is delayed, build-cost holds but ship dates slip.

### Cross-Cohort items I'm seeing

- **#1075 route-prefix migration**: in-flight; affects Surface 4 callbacks. Worth confirming sequencing with PA / Docs.
- **Pattern-063 Surface 1 instance**: file when reconciliation lands; CIO has the pattern tracker.
- **Pattern-071 (audit-as-attack-surface)** filed today via #1017 methodology memo: Surface 7 audit read surface is the canonical positive example of the principle's read-side complement.

---

## Build-cost answers to CXO's 5 questions

1. **Surface 1 sidebar reconciliation cost**: ~1-2 days. Recommend assigning roles (left = continuation, right = archive) over merging. Pattern-063 instance worth filing when work lands.

2. **Surface 7 audit-envelope read-surface build cost**: ~3-4 days. Service layer exists; HTTP route + UI + voice-coded prose are the missing pieces. Concur with Architect's "highest single-priority architectural gap" framing. **Recommend separate ADR**, not folded into Surface 7 MUX doc.

3. **Surface 4 integration pick**: **GitHub + Calendar + Notion**. Defer Slack to post-1.0 (12,213 LOC of mostly-spatial substrate; wizard would be its own project). The three picked are the right MVP demonstration of BYOC capability + LOC manageable for 1.0 timeline.

4. **Surface 6 composed first-run journey cost**: ~2-3 days. Empty-state component substrate exists; journey orchestration is the missing piece. First-meeting LLM-composition verification needed pre-build (~30 min Lead Dev read of `first_meeting_detector.py` + `grammar_context.py`).

5. **Any "1.0-required" call implausibly expensive**: **None**. All five 1.0-required surfaces (1, 2, 4, 6, 7) fit in a focused 3-4 week sprint. The two scope-control levers are the integration pick (drop Slack from Surface 4) and per-message-vs-per-conversation privacy (per-conversation for 1.0).

---

## What this input is NOT

- **Not committing to a specific build sequence** — Round 2 scoping + cohort decisions on divergences (1) (2) (3) influence sequencing
- **Not pre-empting CXO + Comms voice work** on surfaces 2, 6, 7 — those run in parallel; my build estimates assume voice prose lands at appropriate phase
- **Not making the per-message privacy call** — surfacing the build-cost asymmetry (per-conversation = 3-4 days; per-message = 5-6 days) so PM can decide on the values dimension
- **Not committing to integration pick beyond GitHub + Calendar + Notion recommendation** — final pick is PM/PPM call; my read is grounded in code-state evidence

— Lead Developer (build-cost lens), 2026-05-15
