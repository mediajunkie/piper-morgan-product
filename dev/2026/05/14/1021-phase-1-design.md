# #1021 — Phase 1 Design Memo

**Issue**: [#1021](https://github.com/mediajunkie/piper-morgan-product/issues/1021) — UserHistoryService Layer 3 DB backend
**Path**: A (build) per PM disposition 2026-05-14
**Phase**: 1 — Design ratification (Architect estimated 1-2 days; surfaced as a single design pass + PM ratification)
**Date**: 2026-05-14

---

## Major discovery: most of the schema already exists

Architect's Apr 27 framing assumed we'd build **net-new** `conversation_summaries` + `conversation_details` tables. Verified today: we already have **ConversationDB + ConversationTurnDB** persisted via the existing `ConversationRepository`.

### What's already in the database

`services/database/models.py:1037` — `ConversationDB` (table `conversations`):

| Column | Type | Notes |
|---|---|---|
| id | String PK | conversation_id |
| user_id | String | owner |
| session_id | String | session reference |
| title | String | display title |
| context | JSONB | per-conversation context blob |
| lifecycle_state | String(20) | active / archived / deleted (#715) |
| archived_at, deleted_at | TimestampTZ | soft-delete timestamps |
| created_at, updated_at | TimestampTZ | standard |
| **last_activity_at** | TimestampTZ | ✅ already there — perfect for sort ordering |

`services/database/models.py:1100` — `ConversationTurnDB` (table `conversation_turns`):

| Column | Type | Notes |
|---|---|---|
| id | String PK | turn_id |
| conversation_id | String | FK to conversations |
| turn_number | Integer | order within conversation |
| user_message | Text | the user's message |
| assistant_response | Text | Piper's response |
| intent, entities, references, context_used, metadata | various | rich annotation |
| processing_time | Float | telemetry |
| created_at | TimestampTZ | per-turn timestamp |

### What's missing for the `UserHistoryRepository` ABC contract

Comparing the existing tables against the `ConversationSummary` / `ConversationDetail` domain shapes from `services/memory/user_history.py:27-95`:

| Domain field | Source |
|---|---|
| `conversation_id` | ✅ `ConversationDB.id` |
| `title` | ✅ `ConversationDB.title` |
| `started_at` | ✅ `ConversationDB.created_at` |
| `last_activity` | ✅ `ConversationDB.last_activity_at` |
| `turn_count` | ⚠️ derive at query time: `COUNT(*)` on conversation_turns WHERE conversation_id = X |
| `topics` | ❌ **missing** — list of topic strings; not stored anywhere today |
| `preview` | ⚠️ derive at query time: first user_message of first turn |
| `is_private` | ❌ **missing** — boolean per-conversation; not stored |
| `turns` (in ConversationDetail) | ✅ join on conversation_turns |

**Gap: 2 fields (`topics`, `is_private`); 2 derivable fields (`turn_count`, `preview`).**

This is a much smaller schema problem than Architect's body framed.

---

## Three design options

### Option α — Projection over existing tables (smallest scope)

Build `DBUserHistoryRepository` as a **read-only projection** over `ConversationDB` + `ConversationTurnDB`. Derive `turn_count` and `preview` at query time. For `topics` and `is_private`:
- **Option α1 — Skip these fields**: return `topics=[]` and `is_private=False` always. Honest about today's state; surfaces the data-gap as future work.
- **Option α2 — Add columns to ConversationDB**: Alembic migration adds `topics JSONB` + `is_private BOOLEAN` columns. Maintain via the conversation-create / turn-save paths.

**Cost (α1)**: ~1 day (repository impl + tests + container wiring + integration with context_assembler.py:393 fix).
**Cost (α2)**: ~1.5 days (above + migration + maintenance hooks).

**Pro**: smallest blast radius; no new tables.
**Con (α1)**: PDR-002 adaptive greetings without `topics` is limited — "It's been a while" works on last_activity, but "you were working on X" needs topics.
**Con (α2)**: maintenance burden — topics need to be derived/refreshed; is_private needs UI hook.

### Option β — Denormalized cache table (Architect's prescribed)

New `conversation_summaries` table that caches the projected fields. Background refresh or on-write maintenance.

**Cost**: ~3-4 days per Architect's original framing.
**Pro**: fast reads regardless of conversation length; isolation from turn-table churn.
**Con**: duplicate state; refresh strategy adds complexity; data drift risk.

### Option γ — Extend ConversationDB + use existing infrastructure

Add `topics JSONB`, `preview TEXT`, `is_private BOOLEAN` directly to `ConversationDB`. Compute `turn_count` lazily at query time (or denormalize as `turn_count INTEGER` for performance). Build `DBUserHistoryRepository` querying the extended ConversationDB directly.

**Cost**: ~1.5-2 days (migration + maintenance hooks + repo impl + tests + integration).
**Pro**: extends existing infrastructure rather than building parallel system; single source of truth.
**Con**: ConversationDB grows wider; need conversation-create/turn-save hooks to maintain the new columns.

---

## Recommendation

**Option γ — Extend ConversationDB**.

Rationale:
1. The existing `ConversationDB` is already the right place for these fields — `is_private` is per-conversation; `topics` summarizes the conversation; `preview` is conversation-shaped. Splitting into a parallel `conversation_summaries` table (β) creates a sync problem we don't need.
2. Storage cost is small — 1 boolean + 1 short text + 1 JSONB array per conversation. Hundreds of bytes.
3. Maintenance: `topics` can update at turn-save time (extract from intent + entities); `preview` updates on first-turn; `is_private` is a user action.
4. Avoids the α1 "honest-but-limited" trap where PDR-002 adaptive greetings can't reference topics.
5. ~1.5-2 days vs. 3-4 days for β.

α1 (skip the missing fields) is the **fastest** option (~1 day) if PM wants to ship the DB backend ASAP and treat topics + is_private as a follow-up feature. Honest framing: PDR-002 adaptive greetings work partially (last-activity-based "It's been a while" works; topic-based "you were working on X" doesn't).

---

## Open design questions for PM

### Q1 — α/β/γ shape

Recommendation: γ.

### Q2 — Maintenance strategy for `topics`

If γ or α2:
- **(a) LLM-extraction at conversation end** (when conversation transitions to archived state): one LLM call extracts 3-5 topic strings; relatively cheap; topic data is stable
- **(b) Heuristic from intents + entities**: aggregate the `intent` field + `entities` JSONB across turns; deterministic; no LLM cost; may produce less semantically-meaningful topics
- **(c) Defer topics entirely**: ship with empty topics list; file a follow-up for the topic-extraction feature

**Recommendation**: **(b) heuristic**. Cheap, deterministic, runnable on existing data. Can be upgraded to LLM-based later.

### Q3 — Maintenance strategy for `preview`

If γ or α2:
- **(a) Set on first turn**: write conversation_db.preview = turn.user_message at turn 1 save time. Never updated. Simple.
- **(b) Always reflect first turn**: triggers/queries always read the FIRST turn's user_message dynamically. More dynamic.

**Recommendation**: **(a)** — set once, simple. Previews are display-only.

### Q4 — `is_private` UX surface

If γ or α2:
- **(a) Ship the column + repo support; defer UI**: API surface (`UserHistoryService.mark_private`) works; no UI to flip the flag yet. Architecturally complete; user-visible deferred.
- **(b) Ship column + UI together**: include a /api/v1/conversations/{id}/privacy endpoint + frontend toggle

**Recommendation**: **(a)** for this phase. UI is separate concern; can ship later under a UX-focused issue.

### Q5 — `get_history_summary` latent bug at context_assembler.py:393

The method doesn't exist on `UserHistoryService`. Three options:
- **(a) Add it to UserHistoryService**: new method that combines get_conversations(limit=5) into a short text summary suitable for floor prompt inclusion
- **(b) Fix the caller**: change context_assembler to call `search_history()` with a different shape
- **(c) Remove the broken call entirely**: delete the try/except block; ship the rest of #1021 without persistent_memory floor context

**Recommendation**: **(a)** — adding `get_history_summary` is the natural method-shape for what the caller wants. It would return e.g. "User has had 3 prior conversations; most recent 2 hours ago about topic X" suitable for prompt injection. Honors PDR-002 adaptive greetings.

### Q6 — Migration scope

For γ: one Alembic migration adds 3-4 columns to `conversations` table. Should also add indexes:
- `idx_conversations_user_last_activity` (user_id, last_activity_at DESC) — for `get_conversations` pagination
- `idx_conversations_user_private` (user_id, is_private) — for filtering
- GIN index on `topics` — for `search_conversations`

**Recommendation**: ship indexes with the migration; cost is small.

### Q7 — Test fixture migration

`InMemoryUserHistoryRepository` stays in `user_history.py` for tests per Architect's body. Existing test file `tests/unit/services/memory/test_user_history.py` tests against the in-memory impl; new integration tests added for the DB impl (write → restart → read).

**Recommendation**: keep in-memory for unit tests; add DB integration test in `tests/integration/` exercising the round-trip.

---

## Suggested Phase 2 gameplan (conditional on PM ratifying γ + recommendations)

Once Q1–Q7 are ratified:

- **Phase 2.1** (~30 min): Alembic migration adding `topics JSONB DEFAULT '[]'`, `preview TEXT DEFAULT ''`, `is_private BOOLEAN DEFAULT false`, optional `turn_count INTEGER DEFAULT 0` to `conversations` table; 3 indexes
- **Phase 2.2** (~1-2 hr): `DBUserHistoryRepository` in `services/database/repositories.py` implementing the 4 ABC methods (`get_conversations`, `search_conversations`, `set_private`, `get_detail`). Reuse `BaseRepository` patterns where possible.
- **Phase 2.3** (~45 min): heuristic topic-extraction helper (Q2=b); preview-set hook (Q3=a); container wiring to use DBUserHistoryRepository by default
- **Phase 2.4** (~30 min): add `get_history_summary` method to UserHistoryService (Q5=a)
- **Phase 2.5** (~1 hr): tests — unit (repository CRUD against test DB) + integration (write → restart → read end-to-end)
- **Phase 2.6** (~30 min): fix `context_assembler.py:393` to actually populate `persistent_memory` field; verify MEMORY-category queries now include history context

**Phase 2 total**: ~5-7 hours (one focused session). Down from Architect's 2-3 day estimate because the schema discovery shrunk scope.

**Phase 3** (~1 day per Architect): wire memory audit trail sibling to #1018; the `context_assembler` fix above covers most of Phase 3 already.

**Revised total**: ~2-3 days vs Architect's 4-6 days. The schema-discovery is the cost saver.

---

## STOP — awaiting PM ratification on Q1–Q7

Most consequential: **Q1 (α/β/γ)** — picks the schema shape; everything else is tactical.

— Lead Developer, 2026-05-14
