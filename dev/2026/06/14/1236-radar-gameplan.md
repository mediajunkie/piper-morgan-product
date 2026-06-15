# Gameplan — #1236 RADAR entities-surfacing slot-swap

**Template**: `knowledge/gameplan-template.md` v9.4 · **Issue**: #1236 (child of #1090 epic) · **Sprint**: D1 · **Author**: Lead Dev · 2026-06-14
**Binding spec**: `dev/active/radar-entities-surfacing-mockup-2026-06-14.html` (CXO)

---

## Phase -1: Infrastructure Verification (recon done + PM nod)
- **Web**: FastAPI; Jinja2 templates under `templates/`; static under `web/static/` (per app.py StaticFiles). **DB**: PostgreSQL (5433). **Tests**: pytest (asyncio_mode=auto, `--import-mode=importlib`).
- **Exists**: `templates/components/history_sidebar.html` (the slot, 739L); `web/api/routes/user_history.py` (#1021 — conversations source); `web/static/css/cards.css` + `templates/components/insight_card.html` (Part-B Card); `place_window.html`/`insight_card.html`/`lifecycle_*` (home Radar modules).
- **Missing**: entity-catalog backend (#706, PPM-owned); the Radar render.
- **Worktree**: already in the ephemeral session worktree → SKIP extra worktree (single agent, sequential).
- **PM verification**: PM nodded the plan (carve #1236 + run the flywheel). Proceed.

## Phase 0: GitHub Investigation (done)
- #1236 created (child of #1090, the scoping tracker). Mockup = the spec. #706 entity-catalog absent → build the surface + wire conversations (#1021); slot richer types as PPM lands the model.

## Phase 0.5: Frontend–Backend Contract Verification (MANDATORY — UI work) — **gate at build start**
- **Backend**: `GET /api/v1/users/me/history` (`user_history.py`, #1021) is the Conversation source. **ACTION (do first in Phase 1)**: read `user_history.py` + `history_sidebar.html` to capture (a) the #1021 response field shape (id/title/preview/topics/lifecycle/updated_at?) and (b) whether the sidebar renders **server-side (Jinja)** or **client-fetch (JS)** — the Radar render matches the existing pattern.
- **Static**: `web/static/` → `/static/`; `cards.css` present.
- **STOP** if #1021 lacks fields the cards need (lifecycle/provenance) → that's a backend-extension scope decision → escalate to PM before extending.

## Phase 0.6: Data Flow & Integration (user_id propagation)
- The Radar feed is **per-user** → needs `user_id`. #1021 is user-scoped (`get_current_user`). Verify the sidebar render path carries `user_id` (rendered inside an authed page).
- **State**: entities sourced **live** (no new persistence) — #1021 (conversations) now; entity catalog later. Provenance/`is_seed` comes from the entity's data (#1214/#1216), applied as a filter, not stored here.

## DDD Domain Model (the core design — the abstraction PPM's types slot into)
- **`RadarEntity`** (value object): `entity_type` (Conversation | WorkItem | Person | Document), `title`, `lifecycle_state` (blocked | active | in_review | in_design | awaiting_reply | done …), `provenance` (observed | example | seed), `meta`, `attention` (score / last_activity → ordering), `ref` (link).
- **`EntitySource`** (protocol): `fetch(user_id) -> list[RadarEntity]`. First impl: **`ConversationEntitySource`** (wraps #1021 `user_history`). Future: `WorkItem/Person/DocumentEntitySource` register as #706 lands — **slot-in, no surface change.**
- **`RadarFeed`** (domain service): `assemble(user_id) -> RadarView` — gathers from registered sources, **filters provenance** (observed-only in default), **orders attention-first** (types mixed), **selects state** (empty vs populated).
- **Provenance rule**: default = `[e for e in entities if e.provenance == observed]`; empty-state when none. Seed never rendered as observed.

## Phases 1–N: Development (TDD, progressive bookending)
### Phase 1 — Domain + ConversationSource (backend, TDD)
- **Tests first**: `RadarEntity`; `RadarFeed.assemble` (attention-first ordering · provenance filter · empty/populated selection); `ConversationEntitySource` (#1021 → RadarEntity mapping).
- Implement `services/radar/` (entity, source protocol, conversation source, feed). DDD — domain logic, no template concerns.
- Evidence: unit tests green.
### Phase 2 — The surface (slot-swap render, TDD)
- Render the Radar surface in `history_sidebar.html` — entity cards via Part-B `.card` (type label · title · lifecycle badge · provenance · meta); attention-first; **two states** (default real-only / empty explainer + one `○ example`). **Behind a feature flag** (rollback = existing conversation-list).
- **Real `template.render()` tests** (realistic `RadarView` context) for default + empty (per the UI-fix discipline — not curl-200).
- **Wiring test**: render path carries `user_id` → `RadarFeed` → cards (real objects, minimal mocking — per the #490 learning).
### Phase 3 — Entity-search + richer types (gated, non-blocking)
- Entity-search box spanning types (subsumes chat-search; conversations one facet). Wire WorkItem/Person/Document as #706 lands (register sources).

## Phase Z: Handoff
- All AC + evidence; **CXO conformance review** (#1169-style); close-properly with the **Layer-2 closure gate** (cite PDR-002 + the mockup); session log.

## Test Strategy
- **Unit (TDD)**: RadarEntity; RadarFeed (ordering / provenance / two-state); ConversationEntitySource mapping.
- **Render**: real `template.render()` — default + empty.
- **Wiring**: `user_id` → RadarFeed → render (no mocked internals).
- **Regression**: chat-nav (Layer-1) still works; flag-off = prior behavior.

## Rollback
- Feature-flag the Radar render in `history_sidebar.html` (e.g. `RADAR_SIDEBAR`); off → the existing conversation-list. Fully reversible.

## STOP Conditions
- #1021 lacks needed fields (lifecycle/provenance) → escalate (backend-extension scope).
- PPM entity-model conflicts with the mockup → escalate.
- Slot-swap regresses the chat-nav → stop.
- **Closure gate**: do NOT close until it surfaces entities (Layer 2), cite PDR-002 + the mockup.

## Five-Whys (root cause of the 3× recurrence)
History flattens to a chat-list → the slot defaults to the easy conversation-list → no binding spec for the entity surface → entity-model/Layer-2 was never designed (MUX deferred it) → recurs because there's **no closure gate**. **Fix**: build to the mockup (binding spec) + enforce the Layer-2 closure gate (CXO's anti-recurrence).

---

## Gameplan audit (self, vs template v9.4) — the audit-cascade gameplan gate
| Template phase/section | Status | Note |
|---|---|---|
| Phase -1 Infra | ✅ | from recon + PM nod |
| Phase 0 Investigation | ✅ | #1236 + mockup + #706-absent |
| Phase 0.5 FE/BE contract | ✅ | gate flagged; #1021 shape + render-pattern read is the first Phase-1 action |
| Phase 0.6 Data flow | ✅ | user_id propagation + live-source (no new state) |
| Phase 0.7 Conversation design | ⏭️ | template-sanctioned skip — not a conversational feature ("skip this phase") |
| Phase 0.8 Post-completion | ⏭️ | template-sanctioned skip — read-only surface ("skip this phase") |
| Phases 1–N dev | ✅ | 3 phases, TDD, progressive |
| Phase Z handoff | ✅ | CXO conformance + close-properly |
| Test strategy (unit/render/**wiring**/regression) | ✅ | wiring test per #490; render test per UI-fix discipline |
| Rollback | ✅ | feature-flag |
| STOP conditions | ✅ | incl. closure gate + escalation triggers |
| DDD model | ✅ | RadarEntity/EntitySource/RadarFeed — the slot-in abstraction |

**Gate verdict**: complete for build. The two ⏭️ skips are the template's own "skip this phase" rules for this feature type (NOT a unilateral N/A — if PM disagrees, flag). Ready to execute Phase 1 (TDD domain).
