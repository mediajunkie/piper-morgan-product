# #984 CONTEXT-CACHE Redis TTL — Phase 0 audit

**Issue**: [#984](https://github.com/mediajunkie/piper-morgan-product/issues/984) — CONTEXT-CACHE: Redis TTL caching for ContextAssembler external calls
**Scope**: M2f-E pre-work (precedes #985 CONTEXT-SPRINT + #986 CONTEXT-ACTIVITY)
**Phase**: 0 — audit-cascade investigation
**Author**: Lead Developer
**Date**: 2026-05-11

---

## Pattern-067 check

**Header docstring** (`services/intent_service/context_assembler.py:11`):

> *Cache-ready — design for Redis TTL caching later (not implemented yet)*

**Conclusion**: NEGATIVE. The premise is accurate — no cache exists. Confirmed by exhaustive grep: zero `redis_scope` / `setex` / `cache` references inside `context_assembler.py`. Body's framing matches codebase reality.

---

## Inventory of external/expensive calls in ContextAssembler

| Gather method | External / expensive calls | Type | Hot path? |
|---|---|---|---|
| `_gather_identity_context` | `workflow_dispatcher.get_registered_workflows`; `plugin_registry.get_status_all`; `user_context_service.get_user_context`; `conversation_context.get_or_create_context` | in-process | every IDENTITY/DISCOVERY query |
| `_gather_trust_context` | `UserTrustProfileRepository.get_by_user_id` | **DB** | every TRUST query |
| `_gather_memory_context` | `conversation_context` (in-memory); `UserHistoryService.get_history_summary` | DB / in-memory | every MEMORY query |
| `_gather_reminder_context` | `TodoIntentHandlers.get_due_reminders` | **DB** | every CONVERSATION query (greetings!) |
| `_gather_temporal_context` | calls `_gather_calendar_context`; `todo_svc.list_todos` (called **twice** — once with `include_completed=False`, once with `True`); raw SQL `SELECT … FROM projects`; `conversation_context` | **DB + external** | every TEMPORAL query |
| `_gather_status_priority_context` | calls `_gather_calendar_context`; `user_context_service`; `todo_svc.list_todos`; `plugin_registry.get_status_all` | **DB + external** | every STATUS/PRIORITY query + every UNKNOWN-fallback |
| `_gather_calendar_context` | **`CalendarIntegrationRouter.get_temporal_summary`** | **external API** (Google Calendar / MS Graph) | every TEMPORAL + STATUS + PRIORITY + UNKNOWN-fallback |

### The hot calls

- **Calendar** is the only call genuinely hitting an external API (Google/MS Graph). Called from TEMPORAL, STATUS, PRIORITY, and the UNKNOWN-fallback path (line 122) — i.e. *most* floor queries that involve user context.
- **`todo_svc.list_todos`** is called twice inside `_gather_temporal_context` (lines 387 + 396), once for pending, once for completed. Two DB round-trips per TEMPORAL query.
- **Raw projects SQL** (line 417) — separate DB call each TEMPORAL query.
- **User trust profile** + **user_context_service** — separate DB calls each TRUST or STATUS query.

The body's framing "External API hits" understates the real surface — there are also redundant DB hits we can collapse with the same cache.

### GitHub note

#984 body says "External calls (calendar, GitHub, and future sprint/activity assemblers)". In *current* codebase GitHub is **not** directly called from `context_assembler` — only `plugin_registry.get_status_all().get("github")` to check `configured`/`active`. The real GitHub API hits will land when **#985 CONTEXT-SPRINT** and **#986 CONTEXT-ACTIVITY** introduce sprint/activity gatherers. So this is appropriately pre-work: bake the cache pattern now, and #985/#986 plug into it.

---

## Existing cache infrastructure in repo

### `services/cache/redis_factory.py` (69 lines)

- `RedisFactory.initialize()` — singleton pool init (max 20 connections, retry_on_timeout, decode_responses=False)
- `RedisFactory.create_client()` — returns `redis.Redis`, also pings to record health
- `RedisFactory.redis_scope()` — async context manager (`async with` pattern)
- `RedisFactory.close_pool()` — shutdown cleanup
- ENV: `REDIS_URL` (default `redis://localhost:6379`)

### Working examples to mirror

- **`services/auth/token_blacklist.py:97-129`** — the cleanest pattern in the codebase: `redis = await self.redis_factory.create_client()` → `await redis.setex(key, ttl, value)` with structured logging. Has a `_redis_available` flag that flips to in-memory fallback on connection failure. This is exactly the graceful-degradation shape #984 AC asks for.
- **`services/feedback/capture.py:43`** — `await self.redis.setex(key, 86400 * 7, json.dumps(...))` — JSON serialization pattern.
- **`services/intent_service/cache.py`** — `IntentCache` (intent-classification cache, NOT Redis — in-process LRU with TTL). Demonstrates the per-method TTL surface in this codebase already.

### Pattern that does NOT exist yet

- No general-purpose cached-async-function decorator anywhere in the codebase. token_blacklist uses explicit get/set calls.

---

## Audit against gameplan-template.md (Phase 0 outputs)

| Phase 0 requirement | Status | Notes |
|---|---|---|
| Issue number referenced | ✅ | #984 |
| Pattern-067 check | ✅ | NEGATIVE — docstring confirms not-yet-implemented |
| Body-vs-reality inventory | ✅ | calendar/GitHub framing accurate but understates DB-call surface |
| Existing infra mapped | ✅ | RedisFactory + token_blacklist pattern available |
| External-call sites inventoried | ✅ | 7 gather methods surveyed; calendar is the only true external API today |
| Scope-ambiguity questions surfaced | ⚠️ | See **Open design questions** below — PM input needed before Phase 1 |
| Risk assessment | ✅ | See **Risk surfaces** below |

---

## Open design questions (PM input requested before gameplan)

The AC items in the #984 body all surface real choices. Listed in roughly the order they need decisions:

### Q1 — Caching scope and key shape

Three options:
- **(a) Per-method per-user**: separate cache key per `_gather_*` method per user — `cache:context:calendar:{user_id}`, `cache:context:trust:{user_id}`, etc. Cleanest TTL story (different TTLs per data type). Composability poor — invalidation requires knowing the key prefix.
- **(b) Composite per-user**: one big context blob per user keyed `cache:context:{user_id}` with a unified TTL. Simpler key surface but loses the per-data-type TTL flexibility the body asks for.
- **(c) Per-method, ALSO per-category**: key includes the calling intent category — `cache:context:calendar:{user_id}:{category}`. Lets STATUS-derived calendar context evict independently of TEMPORAL-derived. Probably over-engineered.

**Recommendation**: (a). The body's TTL examples ("calendar ~60s, GitHub ~5min, trust_profile ~1h") only make sense with per-method keys.

### Q2 — TTL defaults

Suggested per data type (open to PM tuning):

| Method / data | Suggested TTL | Rationale |
|---|---|---|
| calendar | 60s | User clicks around in a short window; want freshness |
| pending_todos | 30s | User creates/completes todos frequently; want them to appear fast |
| completed_todos | 5min | Less volatile (already done) |
| projects (list) | 5min | Slow-changing |
| trust_profile | 1h | Very slow-changing (trust-stage transitions are rare events) |
| user_context (projects+orgs from user_context_service) | 5min | Slow-changing |
| conversation_history (in-memory already) | n/a | Don't cache — already in-process |
| capabilities / integrations (plugin_registry) | n/a | In-process — caching adds no value |
| GitHub (future, #985+) | 5min per body suggestion | External rate limits |

### Q3 — Invalidation strategy

TTL-based primary (#984 AC ✓). Eager-invalidation hooks needed?

- **Trust-stage change** → invalidate `cache:context:trust:{user_id}` (AC mentions this)
- **Project add/remove** → invalidate `cache:context:projects:{user_id}` + `cache:context:user_context:{user_id}` (AC mentions this)
- **Todo CRUD** (create/edit/complete) → invalidate `cache:context:pending_todos:{user_id}` + `cache:context:completed_todos:{user_id}` (AC silent — but freshness matters here, esp. for "I just added a todo, is it on my agenda?")
- **OAuth disconnect** → invalidate `cache:context:calendar:{user_id}` (AC silent)

**Trade-off**: eager invalidation is correctness-improving but adds plumbing at many entry points (every todo-create site, every trust-stage updater). TTL-only is simpler but creates 30–60s stale windows.

**Decision needed**: TTL-only (smaller scope) vs. TTL + targeted invalidations (correctness-improving, more code).

### Q4 — Implementation pattern (decorator vs. explicit)

Two viable shapes:

- **(a) Decorator**: `@cached_in_redis(ttl=60, key=lambda self, user_id: f"context:calendar:{user_id}")` on each gather method. Clean, but obscures the cache layer and makes selective invalidation (Q3) harder to wire.
- **(b) Explicit get/set inside the method**: pattern from `token_blacklist.py` — check cache → return on hit; on miss, call source, write to cache. More boilerplate but transparent failure paths, easier to express the "stale-on-error vs. fail-graceful" behavior, easier to add invalidation hooks.
- **(c) Helper class + explicit calls**: extract `ContextCache` class with `get_or_compute(key, ttl, async_fn)` method; gather methods become 2-line cached versions. Hybrid that keeps boilerplate down without hiding the cache layer.

**Recommendation**: (c). Matches the `RedisFactory` / `token_blacklist` pattern in this codebase and keeps the eager-invalidation surface explicit. If PM picks "TTL-only" on Q3, (a) is also fine and saves boilerplate.

### Q5 — Scope minimum vs. complete

Three sizing options:

- **(I) Minimum viable cache** (~2 hr): TTL-only, no eager invalidation, single helper class, the two hottest methods (`_gather_calendar_context` + the doubled todo calls in `_gather_temporal_context`). Unblocks the pattern for #985/#986. Defers eager invalidation to a follow-up if real user feedback shows staleness pain.
- **(II) Full pattern, TTL-only** (~3 hr): same as I but all 7 gather methods wrapped. Still no eager invalidation.
- **(III) Full pattern + targeted invalidation** (~4-5 hr): II + eager-invalidation hooks at trust/project/todo/oauth boundaries. Matches the #984 AC closest.

**Recommendation**: (I) for fastest unblock of #985/#986. (III) is the eventual end state but doesn't need to land in this issue if #984 establishes the pattern.

### Q6 — Cache key namespace prefix

`cache:context:` is what I've assumed above. Existing patterns: `blacklist:jwt:` (token_blacklist), no clear convention. Suggest `context:` as the top-level prefix to leave space for `cache:` to mean different things if needed. **Recommendation**: `context:{method}:{user_id}` (drop the `cache:` prefix; the connection is Redis-only so namespace clash is small).

---

## Risk surfaces (non-design, raised here for visibility)

1. **Cache as a fabrication vector**: if stale cached data is presented as current, the floor LLM will compose around it without knowing. Mitigation: TTLs short enough that user-perceived staleness is rare; PM-decision on whether to surface "as of N seconds ago" in the context. *Not adding this in initial impl unless PM wants it.*
2. **Cross-tenant leakage**: if `user_id` is ever empty, key becomes `context:calendar:None`. Mitigation: guard at top of each cached method — if `user_id` is None, skip cache entirely. (`_gather_calendar_context:541` already early-returns on `if not user_id`, so this is naturally already-handled there. Need to replicate for other methods.)
3. **Test environment Redis**: tests will need to either mock the cache layer or run against a real Redis (dev port 6379 per CLAUDE.md). Suggest: mock by default, but include one integration test that hits real Redis to validate the round-trip.
4. **Health-monitor pollution**: token_blacklist's pattern records every Redis call in `health_monitor`. If the context cache hits Redis ~5x per floor query, health_monitor calls multiply. Need to check if health-monitor's "5.0 ms cost" is per call or amortized.

---

## Suggested gameplan shape (pending PM decisions on Q1–Q5)

Conditional on PM picking **Q1=(a), Q3=TTL-only, Q4=(c), Q5=(I)**:

- **Phase 1** (~45 min): build `ContextCache` helper class at `services/intent_service/context_cache.py` with `get_or_compute(key: str, ttl: int, fn: Callable[[], Awaitable[T]]) -> T`. Graceful fallback on Redis unavailable.
- **Phase 2** (~30 min): wrap `_gather_calendar_context` + collapse the double `todo_svc.list_todos` call.
- **Phase 3** (~45 min): unit tests for hit/miss/error paths (mock Redis).
- **Phase 4** (~30 min): integration smoke test (real Redis).
- **Phase 5** (~15 min): merge, close issue, evidence.

Total: ~2.5 hr.

If PM picks **Q5=(III)**: add Phase 6 (~90 min) for trust/project/todo invalidation hooks.

---

## STOP — awaiting PM decision

Per audit-cascade discipline, I'm pausing here. Q1–Q5 each have real trade-offs and the priority label (`priority: low`) suggests this isn't a "build the most thorough thing" situation. I'll proceed to Phase 1 implementation once PM picks shape on each question.

— Lead Developer
