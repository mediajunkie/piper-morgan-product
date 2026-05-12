# #984 CONTEXT-CACHE Redis TTL — gameplan

**Issue**: [#984](https://github.com/mediajunkie/piper-morgan-product/issues/984)
**Phase 0 audit**: `dev/2026/05/11/984-issue-audit.md`
**PM decisions** (2026-05-12):
- Q1 key shape: **per-method per-user**
- Q2 TTLs: **proposed table approved** (calendar 60s, pending_todos 30s, completed_todos 5min, projects 5min, trust_profile 1h, user_context 5min)
- Q3 invalidation: **(c) hybrid** — eager on todos + trust-stage; TTL-only on projects/calendar/user_context
- Q4 pattern: **helper class** (`ContextCache`)
- Q5 scope: **III** (full pattern) — but reduced because Q3=(c) limits eager-invalidation surface
- Q6 namespace: **`context:{method}:{user_id}`**

**Branch**: `claude/984-context-cache-redis-ttl` (worktree at `piper-morgan-product-984`)

---

## Phase -1: Infrastructure verification

Done in Phase 0 audit. Summary:
- `services/cache/redis_factory.py` exists (69 lines). `RedisFactory.create_client()` returns connection-pooled `redis.Redis`. Connection: `REDIS_URL` env (default `redis://localhost:6379`).
- Existing Redis callers: `services/auth/token_blacklist.py` (cleanest pattern — `setex` + JSON serialization + graceful fallback), `services/feedback/capture.py`.
- `services/intent_service/context_assembler.py` has 7 gather methods; calendar is the only true external API today.
- Test infra: pytest + mocking is established convention; integration tests against real Redis are acceptable when dev Redis is up.

No PM verification needed — infrastructure matches Phase 0 understanding.

---

## Problem statement

`ContextAssembler` (`services/intent_service/context_assembler.py`) calls expensive data sources on every floor query: external calendar APIs (Google/MS Graph), redundant DB queries (todos called twice in `_gather_temporal_context`), and per-query trust-profile lookups. With #985 + #986 about to add GitHub + activity-feed gatherers, this will compound. Body's `Cache-ready — design for Redis TTL caching later (not implemented yet)` docstring note (line 11) confirms this was anticipated.

## Five-whys

1. **Why cache?** External API + DB hits on every floor query are wasteful and rate-limit-risky.
2. **Why is that a problem?** User clicks around in a short window → repeated identical fetches → slow UX + risk of hitting Google Calendar rate limits.
3. **Why now?** #985/#986 will add GitHub + activity gatherers; pattern needs to exist before those land.
4. **Why these specific TTLs?** Match data volatility — calendar 60s (fast-changing), trust 1h (rare transitions), pending_todos 30s (user creates/completes frequently).
5. **Why hybrid invalidation (Q3=c)?** Eager invalidation has hidden-bug risk (forgotten site → unbounded staleness). TTL-only loses "I just did that" responsiveness. Hybrid keeps eager where users notice (todos, trust) and bounded-stale fallback elsewhere.

## Success criteria (= #984 AC mapped to decisions)

- [ ] Caching scope: **per-method per-user** (Q1 ✓)
- [ ] TTL defaults per data type: **table from Phase 0 audit** (Q2 ✓)
- [ ] Graceful fallback when Redis unavailable: cache layer returns `None` on Redis error; gather methods fall through to source (Q4: helper class abstracts this)
- [ ] Cache invalidation strategy: **eager on todos (any CRUD) + trust-stage transitions; TTL-only elsewhere** (Q3=c ✓)
- [ ] Unit tests cover cache hit, cache miss, cache error paths
- [ ] No behavioral change for users — transparent speedup

Additional self-imposed criteria:
- [ ] PII never logged at WARNING+ (cache keys may contain user_id, OK; cached values may contain PII data, never log raw cached values)
- [ ] Invalidation sites audit-loggable (structured log on each invalidation event for debugging)

## Test strategy

- **Unit tests for `ContextCache`** (~6 tests): hit, miss, error-on-get, error-on-set, expiry semantics, prefix-invalidation
- **Unit tests for context_assembler caching** (~4 tests): one per cached gather method — assert cache is consulted, populated, and second call hits cache
- **Unit tests for eager invalidation** (~4 tests): todo create/update/complete/delete each invalidate; trust-stage transition invalidates
- **Integration test** (optional, 1 test): real Redis round-trip — skipped if Redis not available in test env

Target: ~15 tests added, all pass. No regressions in existing context_assembler tests.

---

## Phases

### Phase 1: Build `ContextCache` helper class (~45 min)

**Location**: `services/intent_service/context_cache.py` (new file)

**Public API**:

```python
class ContextCache:
    """TTL cache for context_assembler gather methods.
    
    Graceful fallback: any Redis error → returns None (cache miss).
    Caller must handle None by computing the value from source.
    """
    
    def __init__(self, redis_factory: Optional[RedisFactory] = None): ...
    
    async def get(self, key: str) -> Optional[Any]: ...
    
    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool: ...
    
    async def get_or_compute(
        self,
        key: str,
        ttl_seconds: int,
        compute_fn: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Cache-aside helper. Returns cached value if hit, else computes,
        stores, returns. On cache error, calls compute_fn and returns its
        result (no cache write attempted)."""
        ...
    
    async def invalidate(self, key: str) -> bool: ...
    
    async def invalidate_prefix(self, prefix: str) -> int:
        """Delete all keys matching prefix*. Used for cross-key invalidation
        like 'context:pending_todos:{user_id}' + 'context:completed_todos:{user_id}'
        when a todo mutation happens."""
        ...
```

**Internals**:
- Use `RedisFactory.create_client()` to acquire a client. Treat redis-pool init failure as "cache unavailable" — log once at WARN, fall through silently thereafter.
- Serialize values via `json.dumps` (callers responsible for serializable input).
- Key namespace: caller provides full key including `context:` prefix.
- Mirror `token_blacklist.py:97-129` for the graceful-fallback pattern.

**Tests (in `tests/intent_service/test_context_cache.py`)**:
- `test_get_returns_none_on_miss`
- `test_set_then_get_returns_value`
- `test_get_returns_none_on_redis_error`
- `test_set_returns_false_on_redis_error_no_exception`
- `test_get_or_compute_calls_compute_on_miss_caches_result`
- `test_get_or_compute_returns_cached_on_hit_does_not_call_compute`
- `test_get_or_compute_returns_compute_result_on_redis_error`
- `test_invalidate_removes_key`
- `test_invalidate_prefix_removes_all_matching_keys`

### Phase 2: Wrap gather methods in `context_assembler.py` (~60 min)

**Add to `ContextAssembler.__init__`**: `self.cache = ContextCache()`

**Per-method wraps** (use `cache.get_or_compute`):

| Method | Cache key | TTL | Notes |
|---|---|---|---|
| `_gather_calendar_context` | `context:calendar:{user_id}` | 60s | Skip cache if `user_id is None` |
| `_gather_trust_context` | `context:trust:{user_id}` | 3600s (1h) | Skip cache if `user_id is None` |
| `_gather_reminder_context` | `context:reminders:{user_id}` | 30s | Skip cache if `user_id is None` |
| `_gather_temporal_context` — todos | `context:pending_todos:{user_id}` + `context:completed_todos:{user_id}` | 30s / 300s | Cache the **lists** separately; collapse the existing double `list_todos` calls into one and split |
| `_gather_temporal_context` — projects | `context:projects:{user_id}` | 300s | Skip cache if `user_id is None` |
| `_gather_status_priority_context` — user_context | `context:user_context:{user_id}` | 300s | |
| `_gather_status_priority_context` — todos | `context:pending_todos:{user_id}` | 30s | **Shares key with temporal** so invalidation works |

**NOT cached** (in-process or trivial):
- `_gather_identity_context`'s `workflow_dispatcher.get_registered_workflows` (in-process)
- `plugin_registry.get_status_all` (in-process)
- `conversation_context.get_or_create_context` (in-memory already)
- `user_history_service.get_history_summary` (only called from MEMORY, low frequency)

**Implementation shape per method**:

```python
async def _gather_calendar_context(self, user_id: str = None) -> Dict[str, Any]:
    if not user_id:
        return {}
    
    key = f"context:calendar:{user_id}"
    return await self.cache.get_or_compute(
        key=key,
        ttl_seconds=60,
        compute_fn=lambda: self._compute_calendar_context(user_id),
    )

async def _compute_calendar_context(self, user_id: str) -> Dict[str, Any]:
    # existing body of _gather_calendar_context (lines 540-583) goes here
    ...
```

(Same pattern for the other 5 methods.)

**Tests** (extend `tests/intent_service/test_context_assembler.py`):
- `test_calendar_context_uses_cache_on_second_call`
- `test_trust_context_uses_cache_on_second_call`
- `test_reminder_context_uses_cache_on_second_call`
- `test_temporal_todos_uses_cache_on_second_call`

### Phase 3: Eager invalidation on todos + trust (~45 min)

**Subagent-amenable**: yes — well-bounded scoping.

**Todo invalidation** — wrap mutations in `services/todo/todo_management_service.py`:

Find every method that mutates todo state. Likely:
- `create_todo` (or equivalent)
- `update_todo`
- `complete_todo` / `mark_complete`
- `delete_todo`

After successful mutation, call:
```python
await self.cache.invalidate_prefix(f"context:pending_todos:{user_id}")
await self.cache.invalidate_prefix(f"context:completed_todos:{user_id}")
await self.cache.invalidate_prefix(f"context:reminders:{user_id}")
```

(`invalidate_prefix` chosen over per-key for forgiveness — even if a method later adds another todo-derived key, the prefix catches it.)

**Trust-stage invalidation** — find every place where trust_stage transitions. Likely in `services/repositories/user_trust_profile_repository.py` or a trust service. After `trust_stage` update:
```python
await self.cache.invalidate(f"context:trust:{user_id}")
```

**Logging**: add structured log on every invalidation:
```python
logger.info("context_cache_invalidated", method="pending_todos", user_id=user_id, reason="todo_create")
```

**Tests** (in `tests/intent_service/test_context_cache_invalidation.py`):
- `test_todo_create_invalidates_pending_todos_cache`
- `test_todo_complete_invalidates_both_pending_and_completed_caches`
- `test_todo_delete_invalidates_caches`
- `test_trust_stage_transition_invalidates_trust_cache`

### Phase 4: Integration smoke test + verification (~20 min)

- Run full context_assembler test suite — assert no regressions
- One integration test against real Redis (skip if Redis unavailable): write/read/invalidate round-trip
- Verify the canonical retest hasn't regressed on TEMPORAL / STATUS / PRIORITY queries (sample a few from the corpus)

### Phase 5: Merge + close issue (~10 min)

- Merge `claude/984-context-cache-redis-ttl` → `main`
- Close #984 with evidence (commits, test counts, files touched)
- Clean up worktree
- Update session log

**Total estimate**: ~3 hr (less than Q5=III estimate because Q3=c reduces eager-invalidation surface from ~8-12 sites to ~4-5 sites).

---

## Rollback plan

The cache layer is **additive**: if `ContextCache.get_or_compute` returns `None` from a Redis failure, it falls through to `compute_fn`, which is the original gather logic. **The system works the same with Redis down as it does today** — just slower.

If a critical bug emerges:
1. **Immediate**: set `REDIS_URL` to an invalid value in env — `ContextCache` will fail-graceful on every call, behaving exactly like pre-#984.
2. **Surgical**: revert the wrap commits (Phase 2 + Phase 3). Phase 1 (the helper class) can stay — it has no callers if unwrapped.
3. **Full**: revert the entire branch merge.

No feature flag added — the graceful-fallback pattern IS the safety net.

---

## Dependencies

- **None blocking**: Redis already running (port 6379), RedisFactory exists, no new package dependencies.
- **#985 + #986 will consume this** once Phase 5 ships — they'll add `_gather_sprint_context` and `_gather_activity_context` and follow the same wrap pattern.

---

## Risks (carried forward from Phase 0 audit)

1. **Cache as fabrication vector**: addressed by short TTLs (30-60s on user-mutable data) + eager invalidation on todos/trust. Worst-case staleness on slower-changing data is 5min (projects, user_context).
2. **Cross-tenant leakage**: addressed by `user_id` guards at top of every cached method — `if not user_id: return ...` skips cache entirely.
3. **Test environment Redis**: addressed by mocking by default + one optional integration test.
4. **Health-monitor pollution**: each Redis call records into health_monitor. Need to verify this is amortized; if not, may need to suppress for cache-layer calls.

---

## Audit-cascade Phase 1 gate

Gameplan audit will run against `knowledge/gameplan-template.md` after I finish drafting (Step 4 of audit-cascade). Self-check checklist below — full audit doc to follow if any gaps.

| Template section | Status |
|---|---|
| Phase -1 Infrastructure verification | ✅ (deferred from Phase 0 audit) |
| Problem statement | ✅ |
| Five-whys | ✅ |
| Success criteria mapped to AC | ✅ |
| Test strategy | ✅ |
| Phases with time estimates | ✅ (5 phases, ~3 hr total) |
| Rollback plan | ✅ |
| Dependencies listed | ✅ |
| Risks identified | ✅ |

No audit gaps surfacing on self-review.

---

— Lead Developer
