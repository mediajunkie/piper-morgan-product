# Gameplan — #953 CONTEXT-PERSIST (Layer-4 conversation-context persistence)

**Author**: Lead Developer · **Date**: 2026-06-08 · **Template**: gameplan-template v9.3
**Status**: DRAFT — verify-first done; **one design fork needs PM sanity-check** before build.
**Grounding**: audit-cascade `dev/2026/06/08/M3-artifact-spine-audit-cascade-2026-06-08.md`.

## Phase -1 / Phase 0 — verified facts

- **Store**: module-level `_conversation_contexts: dict[str, ConversationContext]` (`conversation_context.py:494`), keyed `f"{user_id or 'anonymous'}:{session_id}"`. Accessed via **synchronous** `get_or_create_context(session_id, user_id)` (L502) + `clear_context` (L537, not yet called in prod).
- **`ConversationContext` fields**: `turns` (list), `lens_stack` (list[str]), `last_offer` (Optional[LastOffer]), `last_response_was_floor`/`last_floor_category`, `turn_provenance` (dict).
- **What ALREADY persists** (so NOT this issue): `turns` → ConversationRepository/ConversationTurnDB; `turn_provenance` → ConversationTurnDB.metadata (R4 #1030).
- **The real gap (this issue)**: `lens_stack` + `last_offer` (+ the two floor flags) are **in-memory only** → lost on restart/refresh. (Matches audit + AC#3.)

## THE DESIGN FORK (sanity-check before build)

**The crux is sync↔async, not where-to-store.** `get_or_create_context` is a **synchronous** module-level function called on the hot floor path; persistence (the repo layer) is **async + AsyncSession-scoped**. You cannot `await` a DB load/save inside the current sync function. So the design must resolve *how* persistence bridges that boundary. Options:

| Option | Persist where | Sync/async bridge | Gall's-Law fit |
|--------|--------------|-------------------|----------------|
| **A (recommended)** — piggyback on `ConversationDB.metadata` JSON, save/load at the existing **async** turn-save/turn-load seams | `ConversationDB.metadata["context"]` = {lens_stack, last_offer, floor flags} | NO new sync→async bridge: `conversation_manager._save_turn_to_database()` (already async, already runs each turn) also writes context; on session resume, the async turn-load path hydrates the in-memory context. The sync `get_or_create_context` stays sync (reads the already-hydrated dict). | Best — reuses the shipped async seam + table; no new infra; no Redis |
| **B** — make `get_or_create_context` async + load from DB on miss | new or reused table | rewrites every caller of `get_or_create_context` to async (broad blast radius on the floor path) | worse — large surface change |
| **C** — Redis with TTL | Redis | async client | over-built for now; PM + issue both say "SQLite/simplest first, Redis later" |

**Recommendation: Option A.** No new sync→async bridge (the trap), reuses `ConversationDB` (already has the rows + a metadata column) + the already-async turn-save seam in `conversation_manager.py`, satisfies all ACs (TTL via the existing conversation staleness/`max_age_minutes` + a cleanup policy), documents the SQLite-via-Postgres-now / Redis-later choice (AC#5). Migration path (AC#6): on first load-miss the context is created empty as today, then hydrated from metadata if present — backward compatible.

**Sanity-check question for PM**: confirm Option A (piggyback ConversationDB.metadata at the async turn seam, leave `get_or_create_context` sync) vs. a preference for a dedicated context table / async refactor. This is the one decision that changes the build.

## ⚠️ AUDIT-CASCADE CORRECTION (gameplan→build gate, 2026-06-08) — Option A still holds, seam relocated

The gate caught a conflation: there are **two `ConversationContext` classes** —
1. `intent_service/conversation_context.py` — holds `lens_stack`/`last_offer` (the #953 target; the in-memory `_conversation_contexts` dict).
2. `conversation/conversation_manager.py` — a *different* class (turns + Redis cache + DB); its async turn-save seam persists **turns**, not lens/offer.

So "piggyback the conversation_manager async seam" (original Option A wording) was imprecise. **Corrected seam (verified):** the lens/offer context IS reachable from the async floor path — `intent_service.py:382-401` (the R4 turn-save block) already calls `get_or_create_context()` + `await self._save_conversation_turn(...)`. That is the correct persist point; `ConversationDB.context` (JSONB, **already exists** — models.py) is the store. **Option A's principle is intact** (persist at an existing async seam; `get_or_create_context` stays sync); only the location moves from conversation_manager → the intent_service R4 seam. PM-approved Option A stands.

**Scope correction**: this is **R4-shaped** (multi-seam + hydration-on-resume), not a 1-commit mechanical change. The hydration half — when a context is newly created on resume, load `ConversationDB.context` and populate lens_stack/last_offer — is the non-trivial part (async load at the L207/L351 create points). Recommend building as a dedicated focused unit (the original gameplan under-scoped it).

## Phases (Option A — CORRECTED seam)
1. `ConversationContext.to_persistable_state()` / `apply_persisted_state(dict)` — (de)serialize lens_stack + last_offer (LastOffer→dict) + floor flags. Unit round-trip tests.
2. `ConversationRepository.save_context_state(conversation_id, state)` + `load_context_state(conversation_id)` — write/read `ConversationDB.context` JSONB. In-memory-SQLite tests.
3. **Persist**: at the `intent_service.py:382-401` async seam, after `_save_conversation_turn`, persist `conv_ctx` state. **Hydrate**: at the context-create points (L207/L351), when newly created, async-load + `apply_persisted_state`. Trace session_id/user_id through (Phase 0.6 / #490 lesson).
4. TTL/cleanup (AC#4): tie to ConversationDB lifecycle_state + max_age; documented. Doc SQLite-vs-Redis (AC#5) + migration (AC#6).

## Phases (Option A — original, superseded by the correction above)
1. Serialize/deserialize helpers on `ConversationContext` (to_persistable_dict / hydrate_from_dict — lens_stack + last_offer + floor flags). Unit tests (round-trip).
2. Write context dict into `ConversationDB.metadata["context"]` in the async turn-save path (`conversation_manager`); read + hydrate on session resume/turn-load.
3. TTL/cleanup policy (AC#4) — tie to existing conversation lifecycle (ACTIVE/ARCHIVED) + max_age; documented.
4. Doc: SQLite-vs-Redis decision (AC#5) + migration path (AC#6), brief — likely in the issue + a note in five-layer-context-mapping.md.

## Test strategy
- Unit: context (de)serialization round-trip; hydrate-from-empty (backward compat); lens_stack + last_offer survive a simulated save→load.
- Wiring: ConversationContext ↔ ConversationDB.metadata round-trip (in-memory SQLite, #1035 pattern).
- Perf (AC#7, <100ms): the context blob is tiny + rides the *existing* turn-save write (no extra round-trip) → effectively free; will measure to confirm.

## Rollback
Additive (new metadata key + (de)serialize helpers + hydrate call). Revert-safe; existing in-memory behavior unchanged if hydration finds nothing.

## Self-audit (vs template) — after PM sanity-check, before build.
Backend data-flow change (Phase 0.6 applies: trace session_id/user_id through the save/load seam — the #490 lesson). No UI/conversation-design phases (gated out by their "when to apply"). Will produce the audit matrix as the cascade gate.
