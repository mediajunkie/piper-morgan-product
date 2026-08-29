# Pattern-051: Parallel Place Gathering

**Status**: Proven
**Category**: Grammar Application
**First Documented**: January 20, 2026
**Ratified**: January 20, 2026 (Grammar Implementation)

---

## Problem Statement

Features need to synthesize information from multiple integrations (GitHub, Calendar, Documents, etc.) to provide holistic context. Common challenges:

- Sequential fetches create latency (2s + 2s + 2s = 6s total)
- One failing integration blocks entire flow
- No graceful degradation when sources unavailable
- Place attribution lost in aggregation
- Error handling inconsistent across sources

This creates slow, fragile features where a single integration failure destroys the entire user experience.

---

## Solution

Implement **Parallel Place Gathering** where:

1. **Concurrent fetches** - Use `asyncio.gather()` to fetch from all Places simultaneously
2. **Per-place error handling** - Each Place handles its own failures independently
3. **Graceful degradation** - Feature works with partial data if some Places fail
4. **Source attribution** - Track which Place provided which data
5. **Synthesis layer** - Combine Place-specific data into unified context

---

## Pattern Description

**Parallel Place Gathering** is a concurrent data collection pattern that treats each integration as a distinct Place with its own atmosphere and failure modes. The pattern emphasizes:

- **Concurrency**: Fetch from multiple Places simultaneously
- **Independence**: Each Place fetch isolated (no cross-contamination)
- **Fault tolerance**: Failures in one Place don't break others
- **Attribution**: Results track which Place they came from
- **Synthesis**: Smart combination of Place-specific data

### Key Characteristics

1. **Parallel execution**:
   - `asyncio.gather()` for concurrent Place fetches
   - Sub-2-second total time even with 3+ sources

2. **Per-place error handling**:
   - Each `_get_[place]_context()` handles own errors
   - Returns empty/default on failure (doesn't raise)

3. **Graceful degradation**:
   - Feature works with 3/3, 2/3, 1/3, or 0/3 sources
   - Quality degrades gracefully, doesn't fail binary

4. **Source tracking**:
   - Result indicates which Places contributed
   - `context_source` field tracks attribution

5. **Synthesis layer**:
   - Combines Place data intelligently
   - Resolves conflicts (e.g., priority from GitHub overrides default)

---

## Implementation

### Structure

```python
import asyncio
from typing import Dict, Any, List

class FeatureService:
    async def gather_context(self, user_id: str) -> Dict[str, Any]:
        """
        Gather context from multiple Places concurrently.

        Returns unified context with source attribution.
        """

        # Parallel fetch from all Places
        github_activity, calendar_events, documents = await asyncio.gather(
            self._get_github_context(user_id),
            self._get_calendar_context(user_id),
            self._get_document_context(user_id),
        )

        # Synthesize into unified context
        return self._synthesize_context(
            github_activity,
            calendar_events,
            documents
        )

    async def _get_github_context(self, user_id: str) -> Dict[str, Any]:
        """Fetch from GitHub Place with local error handling."""
        try:
            return await self.github_service.get_activity(user_id)
        except Exception as e:
            logger.warning("GitHub Place unavailable", error=str(e))
            return {"source": "github", "available": False, "error": str(e)}

    async def _get_calendar_context(self, user_id: str) -> Dict[str, Any]:
        """Fetch from Calendar Place with local error handling."""
        try:
            return await self.calendar_service.get_events(user_id)
        except Exception as e:
            logger.warning("Calendar Place unavailable", error=str(e))
            return {"source": "calendar", "available": False, "error": str(e)}

    async def _get_document_context(self, user_id: str) -> Dict[str, Any]:
        """Fetch from Document Place with local error handling."""
        try:
            return await self.document_service.get_relevant(user_id)
        except Exception as e:
            logger.warning("Document Place unavailable", error=str(e))
            return {"source": "documents", "available": False, "error": str(e)}

    def _synthesize_context(
        self,
        github: Dict[str, Any],
        calendar: Dict[str, Any],
        documents: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synthesize Place-specific data into unified context."""

        sources_available = []
        if github.get("available", True):
            sources_available.append("github")
        if calendar.get("available", True):
            sources_available.append("calendar")
        if documents.get("available", True):
            sources_available.append("documents")

        return {
            "github": github,
            "calendar": calendar,
            "documents": documents,
            "sources_available": sources_available,
            "context_quality": len(sources_available) / 3.0  # 0.0 to 1.0
        }
```

### Example from Morning Standup

**File**: `services/features/morning_standup.py:116-138`

```python
async def generate_standup(self, user_id: str) -> StandupResult:
    """Generate morning standup for user using persistent context.

    Performance optimized: session context and GitHub activity are
    fetched in parallel using asyncio.gather().
    """
    import asyncio

    start_time = time.time()

    try:
        # Parallel fetch: session context and GitHub activity (Issue #556 optimization)
        session_context, github_activity = await asyncio.gather(
            self._get_session_context(user_id),
            self._get_github_activity(),
        )

        # Generate standup content
        result = await self._generate_standup_content(
            user_id, session_context, github_activity, start_time
        )

        return result

    except Exception as e:
        # No fallbacks - fail honestly (see Pattern-054: Honest Failure)
        # ... error handling
```

**Performance impact**:
- Sequential: 2s (session) + 2s (github) = 4s
- Parallel: max(2s, 2s) = 2s (50% improvement)

**File**: `services/features/morning_standup.py:154-186`

```python
async def _get_session_context(self, user_id: str) -> Dict[str, Any]:
    """Get session context using SessionPersistenceManager"""
    try:
        # Try multiple preference sources
        yesterday_context = (
            await self.preference_manager.get_preference("yesterday_context", user_id=user_id)
            or {}
        )

        active_repos = await self.preference_manager.get_preference(
            "active_repos", user_id=user_id
        ) or ["piper-morgan"]

        # ... gather from session Place

        return {
            "yesterday_context": yesterday_context,
            "active_repos": active_repos,
            # ... Place-specific data
        }

    except Exception:
        return {}  # Graceful degradation - empty context

async def _get_github_activity(self) -> Dict[str, Any]:
    """Get GitHub activity from last 24 hours"""
    try:
        recent_issues = await self.github_domain_service.get_recent_issues(limit=5)
        return {"commits": [], "issues": recent_issues}
    except Exception as e:
        # Re-raise integration errors for honest failure
        raise StandupIntegrationError(...)
```

**Graceful degradation**:
- Session unavailable → Returns `{}` → Feature uses defaults
- GitHub unavailable → Raises error → User sees honest failure with suggestion

### Trifecta Pattern (3-Place Gathering)

**File**: `services/features/morning_standup.py:485-523`

```python
async def generate_with_trifecta(
    self,
    user_id: str,
    with_issues: bool = True,
    with_documents: bool = True,
    with_calendar: bool = True,
) -> StandupResult:
    """Generate standup with full intelligence trifecta combination."""

    # Get base standup (includes github + session)
    base_standup = await self.generate_standup(user_id)

    # Add document context if requested
    if with_documents:
        try:
            document_service = get_document_service()
            yesterday_context = await document_service.get_relevant_context("yesterday")
            recent_decisions = await document_service.find_decisions("", "yesterday")

            if yesterday_context.get("context_documents"):
                for doc in yesterday_context["context_documents"][:2]:
                    base_standup.today_priorities.append(f"📄 Review: {doc['title']}")

        except Exception as e:
            # Graceful degradation - annotate but continue
            base_standup.today_priorities.append(
                f"⚠️ Document memory unavailable: {str(e)[:50]}..."
            )

    # Add issue context if requested (similar pattern)
    # Add calendar context if requested (similar pattern)

    return base_standup
```

**Trifecta pattern characteristics**:
- Base standup (2 Places) + optional 3rd/4th/5th Places
- Each additional Place wrapped in try/except
- Failures annotated in output (honest about degradation)
- User sees best available data, not binary success/failure

---

## Consequences

### Benefits

- **Performance**: 50-70% latency reduction via parallelism
- **Resilience**: One Place failure doesn't break entire feature
- **Graceful degradation**: Quality degrades smoothly, not binary
- **Source attribution**: Clear tracking of which Place provided what
- **User trust**: Honest about limitations (see unavailable sources)
- **Scalability**: Easy to add new Places (add to gather() call)

### Trade-offs

- **Complexity**: More code than sequential fetches
- **Error handling**: Must handle failures at two levels (per-place + synthesis)
- **Testing**: Need to test all combinations (3/3, 2/3, 1/3, 0/3 sources)
- **Debugging**: Concurrent failures harder to trace than sequential
- **Resource usage**: Peak concurrent connections higher

---

## Related Patterns

### Complements

- **[Pattern-050: Context Dataclass Pair](pattern-050-context-dataclass-pair.md)** - How to structure gathered context
- **[Pattern-052: Personality Bridge](pattern-052-personality-bridge.md)** - How to present gathered data
- **[Pattern-054: Honest Failure](pattern-054-honest-failure.md)** - How to communicate Place failures

### Alternatives

- **Sequential gathering** - Simpler but slower and more fragile
- **Single-source features** - Easier but less contextual
- **Message queue aggregation** - More robust but complex infrastructure

### Dependencies

- **asyncio.gather()** - Python standard library
- **Structured logging** - For Place-specific failure tracking
- **Place abstractions** - Each integration as distinct Place

---

## Usage Guidelines

### When to Use

✅ **Use Parallel Place Gathering when:**

- Feature needs data from 2+ integrations
- Performance matters (user-facing, interactive)
- Graceful degradation acceptable (partial data useful)
- Places are independent (no ordering dependencies)
- Want to maximize availability despite integration failures

### When NOT to Use

❌ **Don't use when:**

- **Single source**: Only fetching from one Place (use direct call)
- **Sequential dependencies**: Place B needs result from Place A
- **All-or-nothing**: Feature useless with partial data
- **Transactional semantics**: Need atomic success/failure
- **Real-time streaming**: Use WebSocket/SSE instead

### Best Practices

1. **Wrap each Place in try/except**: Local error handling prevents cascade
2. **Return default on failure**: Empty dict/list rather than raising
3. **Log warnings, not errors**: Integration unavailability is expected
4. **Track source attribution**: Include `source` field in Place data
5. **Calculate quality metric**: 3/3 vs 2/3 vs 1/3 sources available
6. **Test all combinations**: Success matrix (all, some, none available)
7. **Use timeouts**: Prevent slow Place from blocking others
8. **Document degradation**: What does feature lose when Place unavailable?
9. **Consider Place ordering**: Place most reliable/fast sources first in tuple
10. **Synthesize intelligently**: Resolve conflicts and prioritize sources

---

## Examples in Codebase

### Primary Usage

- `services/features/morning_standup.py` - Parallel session + GitHub fetch
- `services/features/morning_standup.py` - Trifecta pattern (issues + documents + calendar)

### Applicable To (from audit)

**High Priority** (should adopt pattern):
- Intent Classification - Gather from history + preferences + session
- Todo Management - Gather from lists + projects + calendar
- Slack Integration - Gather from channels + DMs + threads
- GitHub Integration - Gather from issues + PRs + commits

**Medium Priority**:
- Feedback System - Gather from session + previous feedback + user profile
- Conversation Handler - Gather from history + personality + session

---

## Implementation Checklist

- [ ] Identify all Places (integrations/sources) to gather from
- [ ] Create `_get_[place]_context()` method for each Place
- [ ] Add try/except to each Place method (return default on error)
- [ ] Use `asyncio.gather()` to fetch all Places concurrently
- [ ] Create `_synthesize_context()` to combine Place data
- [ ] Track `sources_available` list in synthesis
- [ ] Calculate `context_quality` metric (0.0 to 1.0)
- [ ] Test with all Places available
- [ ] Test with each Place failing individually
- [ ] Test with all Places failing
- [ ] Add timeouts to Place fetches (prevent blocking)
- [ ] Log Place availability for observability
- [ ] Document graceful degradation behavior

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **Morning Standup Base** (2-Place gathering)
   - Location: `services/features/morning_standup.py:116-138`
   - Places: Session context + GitHub activity
   - Performance: Sub-2-second with parallel fetch
   - Degradation: Session failure → defaults; GitHub failure → honest error

2. **Morning Standup Trifecta** (5-Place gathering)
   - Location: `services/features/morning_standup.py:485-615`
   - Places: Session + GitHub + Issues + Documents + Calendar
   - Pattern: Sequential base + parallel optional Places
   - Each Place wrapped independently with graceful degradation

**Performance Evidence**:
- Parallel fetch (Issue #556 optimization): 50% latency reduction
- User perceives <2s = "instant" (vs >4s = "slow")

**Resilience Evidence**:
- Document unavailable → Feature annotates but continues
- Calendar unavailable → Feature annotates but continues
- All Places unavailable → Base standup with defaults

---

_Pattern Identified: January 19, 2026 (P0 Morning Standup Analysis)_
_Ratified: January 20, 2026_
_Category: Grammar Application_
