# #1269 — Morning standup, reconceived as a skill over connected data — GAMEPLAN

**Author**: Lead Dev · **Date**: 2026-06-18 · **Sprint**: D1 · **Specs (binding)**: CXO experience memo + PPM data-model memo (both 2026-06-18, in lead/read/).

## Problem
The current standup is hollow: `today_priorities` all `source:"fallback"` (hardcoded), `github_activity` empty, vanity metrics (PM's 6/17 screenshot). Reconceive it as a **skill that derives a view over the live entity catalog** — no bespoke data pipeline.

## The two binding decisions (from the specs)
- **PPM (data)**: the standup is a **consumer of the EntitySources**, not a parallel pipeline. Yesterday/Today/Blockers = filtered views (lifecycle_state + recency) over `WorkItemEntitySource` / `DocumentEntitySource` / `ConversationEntitySource` (+ a lightweight calendar pull). "Derive, don't maintain" — it inherits every EntitySource improvement for free.
- **CXO (experience)**: NOT a page/route. A **morning-moment card** in the home center column, above the chat input, on first open before ~10am; dismissable ("Got it") / auto-dismiss at 10am; doesn't reappear till tomorrow. After 10am / any time: on-demand via "give me my standup" in chat (conversational, not the card). Prose narrative (the actual things, not counts), in standup order.

## DDD
- **`StandupSummary`** (domain): three slots — `yesterday: list[StandupItem]`, `today: list[StandupItem]`, `blockers: list[StandupItem]` — each a derived view, + a `to_prose()` rendering (CXO's "say it out loud" framing).
- **`StandupAssembler`** (service): takes the live EntitySources (the SAME ones `_build_feed` wires) + a calendar pull; applies the slot filters; returns a `StandupSummary`. Pure derivation — does **not** read the DB directly.
- **Slot filters** (the PPM derivation rules):
  - **Yesterday** = WorkItem `DONE|RESOLVED|CLOSED` + Document `RATIFIED` + Conversation resolved, all `updated_at > now-24h`.
  - **Today** = WorkItem `IN_PROGRESS|OPEN|ASSIGNED` (attention/near-due first) + Calendar today + Document `IN_PROGRESS`.
  - **Blockers** = WorkItem `BLOCKED|STALLED` + stale `IN_PROGRESS` (>N days no update) + unresolved waiting-threads (lower confidence).

## Key architecture point (avoid duplication)
`_build_feed` (web/api/routes/radar.py) instantiates the EntitySources + providers. The standup must consume the **same** wiring, not re-instantiate/duplicate it. **Phase 1 extracts a shared `build_entity_sources(...)` factory** (or reuse the RadarFeed) that both `_build_feed` and the StandupAssembler call. This is the "one surface, not two" / derive-don't-maintain discipline applied to the source wiring.

## Phases (TDD throughout; real render for the surface, not curl-200)
- **P0 — contract read** (done in this gameplan): EntitySources are callable (WorkItem #1239, Document #1238, Conversation #1021 all in `_build_feed`); lifecycle_state vocab confirmed against each source's `_derive_*_lifecycle`. ⚠️ **Gap to confirm**: the EntitySources emit lifecycle labels (`open/in-review/blocked/closed`, `new/recent/stale`, `active/idle/dormant`) — the PPM filter vocab (`DONE/RESOLVED/CLOSED`, `RATIFIED`, `IN_PROGRESS`) must be **mapped to the actual emitted labels** (a small reconcile, Phase 1).
- **P1 — shared source factory + StandupAssembler** (TDD): extract `build_entity_sources()`; `StandupAssembler.assemble(user_id) -> StandupSummary` with the slot filters; fake EntitySources in tests (don't mock internals — #490). Replaces the hardcoded fallbacks.
- **P2 — calendar pull** (lightweight): the Today slice's calendar events (reuse the calendar connector; graceful-empty if unconfigured, like the WorkItem source).
- **P3 — prose rendering** (`to_prose()`): CXO's narrative shape; honest (only real items; "no items" reads gracefully, not a fabricated "all clear").
- **P4 — the morning-card surface**: center-column card above chat, time-aware (<10am, first-open), dismissable + auto-dismiss-at-10am + once-per-day (localStorage day-key, the #1225 pattern); real render test.
- **P5 — on-demand chat skill**: "give me my standup" → conversational summary (the floor; always callable). Wire via the workflow-dispatcher rail (no new `elif intent.action` — CLAUDE.md).
- **P6 — close**: AC + evidence; retire the hardcoded fallback; close-issue-properly.

## Dependencies / sequencing
- **Hard dep**: #1237 EntitySources callable — **met** (the 3 needed are live; People #1240 is NOT needed for standup — PPM: "People emerge as context, don't list directly").
- Calendar connector exists (places.py uses it).
- No #1240 dependency (good — #1240 is Phase-0-blocked on its source).

## Audit-cascade (GAMEPLAN gate) — self-audit
- Problem statement ✅ · Binding specs cited ✅ · DDD ✅ · Phases w/ TDD ✅ · The duplication-avoidance (shared factory) called out ✅ · The lifecycle-vocab-mapping gap flagged (P0→P1) ✅ · Real-render for the surface ✅ · Dispatcher-rail for the skill ✅ · Close-properly ✅. **Open question for the build**: the staleness threshold N (Blockers) — default 3 days, confirm w/ CXO/PM at P1.

## Not in scope
People-as-a-slot (PPM: emerge as context); insights/learning (Piper's analysis layer, not a real-data summary); attention-scoring (post-MVP — Today ordering uses recency for now).

---

## Phase-0 contract-read FINDINGS (2026-06-18, post-compaction — verify-before-build) ✅

Read the actual source code before writing the assembler. Three findings change the build:

### 1. Lifecycle-vocab reconcile — RESOLVED (the flagged-careful part)
The EntitySources emit ONLY these `lifecycle_state` strings (from `services/radar/sources.py`), plus an `attention` epoch-seconds field on every `RadarEntity` (the parsed `updated_at`/`last_activity` — this IS our recency timestamp; there is no separate datetime):
- **Conversation**: `active` (<24h) · `idle` (<7d) · `dormant` (≥7d)  [recency-derived]
- **Document**: `new` (<24h) · `recent` (<7d) · `stale` (≥7d)  [recency-derived]
- **WorkItem**: `closed` · `blocked` (label~block) · `in-review` (label~review/in-progress) · `open`  [state+label-derived]

The PPM-vocab in the original filters (`DONE/RESOLVED/CLOSED`, `RATIFIED`, `IN_PROGRESS`, `BLOCKED/STALLED`) does **not** exist in the emitted labels. **The honest mapping uses the real labels + `attention`:**
- **Yesterday** (what moved in last ~24h) = Conversation `active` + Document `new`. *(Both are recency-fresh.)*
- **Today** (on my plate) = WorkItem `open` + `in-review` (assigned-to-me via #6) + Document `recent` (+ calendar, P2). *This is what replaces the hardcoded `fallback_priorities`.*
- **Blockers** = WorkItem `blocked` + stale-still-open: WorkItem `open`/`in-review` with `attention` older than N days (N=3 default, confirm w/ CXO/PM).

### 2. ⚠️ Honest gap — WorkItem source is OPEN-ONLY
`WorkItemProvider.list_for_user` calls `router.get_open_issues(...)` → the WorkItem source NEVER emits `closed`. So **"Yesterday = closed work items" is unsatisfiable through the live source.** Yesterday is therefore Conversation+Document recency only (which is honest — we surface what we actually observed moved). A future enhancement (#706/post-MVP) could add a recently-closed-issues pull; out of scope for beta. Documented so the empty-ish Yesterday slot isn't mistaken for a bug.

### 3. Complete-not-duplicate — reuse `StandupItem`, NEW `StandupSummary`
`services/domain/models.py` already has:
- **`StandupItem`** (line 1901) — the line-item value object (`display/source/lifecycle_state/icon` + `to_dict`/`from_dict`/`__str__`), already consumed by `standup.html` (#704). **REUSE it** — the derived items render through the same template path.
- **`StandupPartialCapture`** (line 1956) — three slots `yesterday/today/blockers: List[StandupItem]`. Same SHAPE as our summary, BUT it is the **interactive-capture write-state** (user-authored, persisted with `StandupConversation`, escape/resume). Semantically distinct from a system-**derived** read-model. → Create a NEW `StandupSummary` (derived view + `to_prose()`), reusing `StandupItem`; do NOT overload `StandupPartialCapture`.

`StandupItem.source` for derived items: use the entity_type origin — `"radar:conversation"` / `"radar:document"` / `"radar:work_item"` — so the surface can tell derived-from-observed items apart from captured/commit items. `lifecycle_state` carries the coarse label through.

### 4. The existing hollow standup (what #1269 ultimately retires)
`services/features/morning_standup.py::MorningStandupWorkflow.generate_standup` → `StandupResult`. Its `_get_github_activity` hardcodes `commits: []`, so `yesterday_accomplishments` is always empty, `blockers` is always "No recent GitHub activity detected", `today_priorities` falls to config `fallback_priorities` (the `source:"fallback"` PM saw), and it reports vanity `time_saved_minutes`. The `StandupAssembler` supersedes this as the data source; retiring/rewiring the old workflow + its surfaces (standup.html, MCP skill, consciousness layer) is P5/P6 (surface) — P1b stands up the assembler + domain first. *(Note latent bug for later: `generate_with_documents/issues/calendar` `.append()` plain strings into `List[StandupItem]` — type drift, not #1269's job.)*

### Assembler shape (decided)
`StandupAssembler(sources: list[EntitySource])` — takes the SAME list `build_entity_sources()` returns (DI; tests pass fakes). `async assemble(user_id) -> StandupSummary`: gather all entities with **per-source isolation** (mirror `RadarFeed.assemble`'s try/except — a failing source must never blank the standup), filter to OBSERVED, partition into slots by `(entity_type, lifecycle_state, attention)`. Pure derivation — no DB. `now_epoch` injectable for deterministic tests (default `datetime.now(timezone.utc).timestamp()`).
