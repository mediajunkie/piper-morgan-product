# #1574 build design — UserPreferenceManager gets a real store (Audit Cluster 1 head)

**Status**: design for a fresh-session build (Lead, scoped 2026-09-22 evening; deliberately not
built at day's end — the named quality-banking trigger). Parent: #1828. Unblocks the tz-consumption
family (#1556/#1575/#1576/#1577/#1588) which needs `get_timezone` to stop being a facade.

## The measured facts (fresh census tonight)

- `services/domain/user_preference_manager.py` (1,110 lines): in-memory dicts only; every
  preference lost per restart; tz always returns the America/Los_Angeles default (audit F6).
- **Real production consumers exist and are the reason this matters**: `preference_handler`
  (set_preference / apply_preference_pattern — user-visible "remember that I…" flows),
  `canonical_handlers` (calendar-setup-offer state — resets every deploy, so the offer re-nags),
  reminder_* family, learning flags, context_format.
- **The real store already exists and has conventions**: `users.preferences` JSONB (#1422),
  read by `user_context_service` (#280 keys), written by `standup_preferences` (#1510
  verified-inference store). These existing keys MUST NOT be clobbered.

## The design (API-preserving; the fix lives inside the manager)

1. **User-scoped preferences become read-through/write-through to `users.preferences`** under
   ONE namespaced sub-key: `"upm"` — `{"upm": {"<pref_key>": <PreferenceItem.to_dict()>}}`.
   `PreferenceItem.to_dict/from_dict` already exist; versioning + expiry serialize for free.
   Namespacing means zero collision with #280/#1510 keys and a trivial rollback (delete the key).
2. **Session-scoped preferences stay in-memory** — session lifetime is the correct lifetime;
   the existing ConversationSession bridge (update/load_from_session_context) is unchanged.
3. **Write path**: set_preference persists synchronously in the same call (async DB write via
   session_scope_fresh; the manager already holds per-key asyncio locks — they become the
   read-modify-write guard on the JSONB merge). No write-behind, no cache-invalidation problem:
   process-local cache + write-through, DB wins on cold read (the #1808 shape).
4. **Read path**: get_preference checks the in-process cache, falls to a JSONB read on miss,
   caches. `get_all_preferences`/`merge_preferences` compose from the same two layers.
5. **No data migration exists to run** — in-memory means nothing durable predates this. The only
   "migration" is the empty namespaced key appearing on first write.
6. **Multi-process honesty**: alpha runs one app machine today; cross-process staleness is
   bounded by cold-read-wins + short cache. If Fly ever scales machines, the cache needs a TTL —
   note in code, don't build it now (m-43: name the layer the guarantee covers).

## Order of work (fresh session)

1. Storage adapter inside the manager (JSONB merge helpers + locks) — with red-first tests:
   restart-survival (new manager instance, same DB → same prefs), collision-safety (#280/#1510
   keys untouched — read them before/after), expiry/version round-trip.
2. Flip user-scope get/set to the adapter; session scope untouched.
3. Live verify: set a pref via the real `/api/v1/preferences` route, bounce the local server,
   read it back (the audit's own falsifying test).
4. Then the cluster's consumption fixes (#1556 etc.) become real work against a real store.

## Explicitly out of scope

Deleting the manager in favor of direct JSONB calls everywhere (the #1510 agent's route-around):
17 consumer files say the facade earns its keep once it's honest; false-trails cleanup of any
consumers that duplicated storage goes to the per-issue fixes in the cluster.
