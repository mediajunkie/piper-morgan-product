# Prompt for Code Agent: GREAT-4C Phase 3 - PIPER.md Caching

## Context

Phase 2 complete: Error handling implemented across all handlers.

**Next priority**: Implement caching for PIPER.md reads to reduce file I/O overhead.

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0725-prog-code-log.md`

## Mission

Add caching layer for PIPER.md configuration to improve performance under load and reduce repeated file system access.

---

## Phase 3: PIPER.md Caching Implementation

### Step 1: Analyze Current PIPER.md Access Patterns

Check how often PIPER.md is accessed:

```bash
# Find all PIPER.md access points
grep -r "load_config\|load_standup_config\|piper_config_loader" services/intent_service/ --include="*.py" -n

# Check user context service access
grep -r "load_config" services/user_context_service.py -A 3
```

Current pattern: Every handler call loads PIPER.md from disk.

### Step 2: Create PIPER Config Cache Service

Create: `services/configuration/piper_config_cache.py`

```python
"""Caching layer for PIPER.md configuration."""
import time
from typing import Dict, Optional, Any
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class PiperConfigCache:
    """
    Cache for PIPER.md configuration files.
    Reduces file I/O by caching parsed config with TTL.
    """

    def __init__(self, ttl: int = 300):
        """
        Initialize cache.

        Args:
            ttl: Time-to-live in seconds (default 5 minutes)
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
        self.hits = 0
        self.misses = 0
        logger.info(f"PiperConfigCache initialized with TTL={ttl}s")

    def get(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get cached config if exists and not expired.

        Args:
            user_id: User identifier (or session_id)

        Returns:
            Cached config dict or None if miss/expired
        """
        if user_id in self.cache:
            entry = self.cache[user_id]

            # Check expiration
            if time.time() < entry['expires_at']:
                self.hits += 1
                logger.debug(f"Config cache HIT for user: {user_id}")
                return entry['config']
            else:
                # Expired - remove
                del self.cache[user_id]
                logger.debug(f"Config cache EXPIRED for user: {user_id}")

        self.misses += 1
        logger.debug(f"Config cache MISS for user: {user_id}")
        return None

    def set(self, user_id: str, config: Dict[str, Any]) -> None:
        """
        Cache configuration.

        Args:
            user_id: User identifier
            config: Parsed PIPER.md configuration
        """
        self.cache[user_id] = {
            'config': config,
            'expires_at': time.time() + self.ttl,
            'cached_at': time.time()
        }
        logger.debug(f"Config cached for user: {user_id}")

    def invalidate(self, user_id: str) -> bool:
        """
        Remove specific user's config from cache.

        Args:
            user_id: User identifier

        Returns:
            True if entry was removed, False if not found
        """
        if user_id in self.cache:
            del self.cache[user_id]
            logger.info(f"Config cache invalidated for user: {user_id}")
            return True
        return False

    def clear(self) -> None:
        """Clear entire cache."""
        count = len(self.cache)
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info(f"Config cache cleared ({count} entries removed)")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Return cache performance metrics.

        Returns:
            Dict with hits, misses, hit_rate, size
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0

        return {
            'hits': self.hits,
            'misses': self.misses,
            'total_requests': total,
            'hit_rate_percent': round(hit_rate, 2),
            'cache_size': len(self.cache),
            'ttl_seconds': self.ttl
        }

# Singleton instance
piper_config_cache = PiperConfigCache(ttl=300)  # 5 minutes
```

### Step 3: Integrate Cache with User Context Service

Edit: `services/user_context_service.py`

Add cache integration:

```python
from services.configuration.piper_config_cache import piper_config_cache

class UserContextService:
    """Manages user-specific context with caching."""

    async def _load_context_from_config(self, session_id: str) -> UserContext:
        """Load user context from PIPER.md with caching."""
        from services.configuration.piper_config_loader import piper_config_loader

        # Check cache first
        cached_config = piper_config_cache.get(session_id)
        if cached_config:
            logger.debug(f"Using cached config for session: {session_id}")
            config = cached_config
        else:
            # Load from file
            try:
                config = piper_config_loader.load_config()
                # Cache it
                piper_config_cache.set(session_id, config)
                logger.debug(f"Loaded and cached config for session: {session_id}")
            except Exception as e:
                logger.warning(f"Could not load user context: {e}")
                return UserContext(user_id=session_id)

        # Extract user context from config
        context = UserContext(
            user_id=session_id,
            organization=self._extract_organization(config),
            projects=self._extract_projects(config),
            priorities=self._extract_priorities(config)
        )

        return context
```

### Step 4: Add Cache Monitoring Endpoint

Edit: `web/app.py`

Add cache metrics endpoint:

```python
@app.get("/api/admin/piper-config-cache-metrics")
async def piper_config_cache_metrics():
    """Get PIPER config cache performance metrics."""
    from services.configuration.piper_config_cache import piper_config_cache

    metrics = piper_config_cache.get_metrics()
    return {
        "cache_enabled": True,
        "metrics": metrics,
        "status": "operational"
    }

@app.post("/api/admin/piper-config-cache-clear")
async def clear_piper_config_cache():
    """Clear the PIPER config cache (admin only)."""
    from services.configuration.piper_config_cache import piper_config_cache

    piper_config_cache.clear()
    return {"status": "cache_cleared"}

@app.post("/api/admin/piper-config-cache-invalidate/{user_id}")
async def invalidate_user_config(user_id: str):
    """Invalidate specific user's cached config."""
    from services.configuration.piper_config_cache import piper_config_cache

    invalidated = piper_config_cache.invalidate(user_id)
    return {
        "status": "invalidated" if invalidated else "not_found",
        "user_id": user_id
    }
```

### Step 5: Test Cache Performance

Create: `dev/2025/10/06/test_piper_cache_performance.py`

```python
"""Test PIPER config caching performance."""
import asyncio
import time
from services.user_context_service import user_context_service
from services.configuration.piper_config_cache import piper_config_cache

async def test_cache_performance():
    """Measure cache hit rate and performance improvement."""

    print("=== PIPER Config Cache Performance Test ===\n")

    # Clear cache to start fresh
    piper_config_cache.clear()

    test_session = "test_session_123"

    # First load (cache miss)
    print("1. First load (cache miss):")
    start = time.time()
    context1 = await user_context_service.get_user_context(test_session)
    duration1 = (time.time() - start) * 1000
    print(f"   Duration: {duration1:.2f}ms")
    print(f"   Organization: {context1.organization}")

    # Second load (cache hit)
    print("\n2. Second load (cache hit):")
    start = time.time()
    context2 = await user_context_service.get_user_context(test_session)
    duration2 = (time.time() - start) * 1000
    print(f"   Duration: {duration2:.2f}ms")
    print(f"   Organization: {context2.organization}")

    # Calculate improvement
    if duration1 > duration2:
        improvement = ((duration1 - duration2) / duration1) * 100
        print(f"\n✅ Cache improved performance by {improvement:.1f}%")
        print(f"   ({duration1:.2f}ms → {duration2:.2f}ms)")

    # Multiple loads to test hit rate
    print("\n3. Multiple loads (testing hit rate):")
    for i in range(3, 11):
        await user_context_service.get_user_context(test_session)
        print(f"   Load {i}: cached")

    # Check final metrics
    metrics = piper_config_cache.get_metrics()
    print(f"\n=== Cache Metrics ===")
    print(f"Total Requests: {metrics['total_requests']}")
    print(f"Cache Hits: {metrics['hits']}")
    print(f"Cache Misses: {metrics['misses']}")
    print(f"Hit Rate: {metrics['hit_rate_percent']}%")
    print(f"Cache Size: {metrics['cache_size']} entries")

    # Validate hit rate
    if metrics['hit_rate_percent'] >= 80:
        print(f"\n✅ Cache performing excellently (>80% hit rate)")
    elif metrics['hit_rate_percent'] >= 60:
        print(f"\n✅ Cache performing well (>60% hit rate)")
    else:
        print(f"\n⚠️  Cache hit rate below 60%")

if __name__ == "__main__":
    asyncio.run(test_cache_performance())
```

Run test:
```bash
python3 dev/2025/10/06/test_piper_cache_performance.py
```

### Step 6: Document Caching Implementation

Create: `dev/2025/10/06/piper-cache-implementation.md`

```markdown
# PIPER Config Caching Implementation

## Overview
PIPER.md configuration caching reduces file I/O overhead and improves performance under load.

## Cache Design

### Strategy
- **Type**: In-memory cache with TTL
- **TTL**: 5 minutes (300 seconds)
- **Key**: User/session ID
- **Eviction**: Lazy expiration on access

### Benefits
- Reduces file system reads
- Improves handler response time
- Scales better under concurrent load

## Configuration

### Adjust TTL
```python
from services.configuration.piper_config_cache import piper_config_cache

# Longer TTL for stable configs
piper_config_cache.ttl = 600  # 10 minutes

# Shorter TTL for frequently updated configs
piper_config_cache.ttl = 60  # 1 minute
```

### Invalidate Cache
When PIPER.md is updated:
```python
# Invalidate specific user
piper_config_cache.invalidate(user_id)

# Or clear entire cache
piper_config_cache.clear()
```

## Monitoring

### Metrics Endpoint
```bash
curl http://localhost:8001/api/admin/piper-config-cache-metrics
```

Returns:
```json
{
  "cache_enabled": true,
  "metrics": {
    "hits": 45,
    "misses": 5,
    "hit_rate_percent": 90.0,
    "cache_size": 3
  }
}
```

### Cache Management
```bash
# Clear cache
curl -X POST http://localhost:8001/api/admin/piper-config-cache-clear

# Invalidate specific user
curl -X POST http://localhost:8001/api/admin/piper-config-cache-invalidate/user123
```

## Performance Impact

**Before**: Every handler call → file read (~2-5ms)
**After**: First call → file read (~2-5ms), subsequent → cache (~0.1ms)

**Expected hit rate**: 80-90% for typical usage patterns
**Performance improvement**: ~50-90% reduction in config load time
```

---

## Success Criteria

- [ ] PiperConfigCache service created
- [ ] User context service integrated with cache
- [ ] Cache metrics endpoint operational
- [ ] Cache management endpoints working
- [ ] Performance test shows improvement
- [ ] Hit rate >60% in tests
- [ ] Documentation complete
- [ ] Session log updated

---

## Evidence Format

```bash
$ python3 dev/2025/10/06/test_piper_cache_performance.py
=== PIPER Config Cache Performance Test ===

1. First load (cache miss):
   Duration: 3.24ms
   Organization: Example Org

2. Second load (cache hit):
   Duration: 0.08ms
   Organization: Example Org

✅ Cache improved performance by 97.5%
   (3.24ms → 0.08ms)

3. Multiple loads (testing hit rate):
   Load 3: cached
   ...

=== Cache Metrics ===
Total Requests: 10
Cache Hits: 9
Cache Misses: 1
Hit Rate: 90.0%
Cache Size: 1 entries

✅ Cache performing excellently (>80% hit rate)
```

---

**Effort**: Medium
**Priority**: MEDIUM (performance optimization)
**Complexity**: Moderate (cache service + integration)
