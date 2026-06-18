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
