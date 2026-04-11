# Intent Classification Developer Guide

**Last Updated**: October 6, 2025
**Status**: ⚠️ OUTDATED — predates M1 floor inversion
**Epic**: GREAT-4E - Complete Validation

> ⚠️ **STALE ARCHITECTURE WARNING (Apr 11, 2026)**
> This guide describes a "fast path canonical (~1ms) vs workflow handler (2000-3000ms)" dichotomy that no longer exists. After M1's floor inversion (#911) and the Apr 8 IDENTITY full migration to floor (commit `33e6758a`), the conversational floor is the default routing destination. Canonical handlers now serve only mutation operations and a small set of fast-path exceptions (TEMPORAL, STATUS, PRIORITY, PORTFOLIO).
>
> See [ADR-060: Floor-First Routing](../internal/architecture/current/adrs/adr-060-floor-first-routing.md) for current routing rules. The current intent category count is 19 (not 13 as stated below).
>
> **Full rewrite pending in M2a doc cleanup.** Use this guide for historical context only.

---

## Overview

This guide explains when and how to use intent classification in Piper Morgan. As of GREAT-4E completion, intent classification is **mandatory** for all natural language user input, with 13/13 intent categories fully implemented and validated.

---

## Intent Categories (Complete List)

### Canonical Handler Categories (Fast Path ~1ms)
1. **IDENTITY**: "Who are you?" - Bot identity and capabilities
2. **TEMPORAL**: "What's on my calendar?" - Time and schedule queries
3. **STATUS**: "Show my standup" - Current state and progress
4. **PRIORITY**: "What's most important?" - Priority and focus
5. **GUIDANCE**: "How should I approach this?" - Recommendations and advice

### Workflow Handler Categories (Standard Path 2000-3000ms)
6. **EXECUTION**: "Create GitHub issue" - Action execution
7. **ANALYSIS**: "Analyze commits" - Data analysis
8. **SYNTHESIS**: "Generate summary" - Content generation
9. **STRATEGY**: "Plan next sprint" - Strategic planning
10. **LEARNING**: "What patterns exist?" - Pattern recognition
11. **UNKNOWN**: "Blarghhh" - Unclassifiable input (helpful fallback)
12. **QUERY**: "What's the weather?" - General queries
13. **CONVERSATION**: "Let's chat" - Conversational responses

---

## When Intent Classification is Required

### Required (Natural Language Input)

Intent classification **MUST** be used for:

✅ **User text messages** - Slack, chat, conversational UI
✅ **Free-text queries** - Unstructured user input
✅ **Ambiguous requests** - Need interpretation
✅ **Natural language commands** - "What's my schedule?", "Create an issue"

### Not Required (Exempt)

Intent classification is **NOT** needed for:

❌ **Structured CLI commands** - `piper documents search --query X`

- Structure already expresses intent
- Argparse/click parameters are explicit

❌ **Output processing** - Personality enhancement

- Processes Piper's responses, not user input
- Different pipeline direction

❌ **Direct ID lookups** - `/api/workflows/12345`

- No ambiguity, explicit resource access

❌ **Static resources** - Health checks, docs, config

- Infrastructure endpoints

---

## How to Add a New NL Endpoint

### Step 1: Register in Middleware

Edit `web/middleware/intent_enforcement.py`:

```python
NL_ENDPOINTS = [
    '/api/v1/intent',
    '/api/standup',
    '/api/chat',
    '/api/message',
    '/api/your-new-endpoint'  # Add here
]
```

### Step 2: Route Through Intent

Your endpoint should call the intent classifier:

```python
@app.post("/api/your-new-endpoint")
async def your_endpoint(request: Request):
    user_text = request.json().get("text")

    # Classify intent
    from services.intent_service import classifier
    intent = await classifier.classify(user_text)

    # Route to appropriate handler
    if intent.category == IntentCategory.TEMPORAL:
        return await handle_temporal_query(intent)
    elif intent.category == IntentCategory.STATUS:
        return await handle_status_query(intent)
    # ... etc
```

Or redirect to universal intent endpoint:

```python
@app.post("/api/your-new-endpoint")
async def your_endpoint(request: Request):
    # Redirect to universal handler
    return await process_intent(request)
```

### Step 3: Add Tests

Create test in `tests/intent/test_user_flows_complete.py`:

```python
def test_your_endpoint_flow(self):
    response = client.post("/api/your-new-endpoint", json={
        "text": "Sample query"
    })
    assert response.status_code in [200, 422]

    # Verify intent was classified
    if response.status_code == 200:
        data = response.json()
        assert "intent" in data or "category" in data
```

### Step 4: Validate

```bash
# Run bypass scanner
python scripts/check_intent_bypasses.py

# Run tests
pytest tests/intent/ -v

# Check middleware config
curl http://localhost:8001/api/admin/intent-monitoring
```

---

## Performance Considerations

### Performance Expectations

#### Response Time Targets
- **Canonical handlers**: <10ms (fast path, no LLM)
- **Pre-classifier hit**: ~1ms (pattern recognition)
- **LLM classification**: 2000-3000ms (full classification)
- **Cached responses**: <1ms (cache hit)

#### Cache Performance
- **Hit rate target**: >80%
- **Actual performance**: 84.6% (GREAT-4E validation)
- **Speedup**: 7.6x for cached requests

#### Load Capacity
- **Sustained throughput**: 600K+ requests/sec
- **Memory**: Stable, no leaks under sustained load
- **Concurrent requests**: Excellent parallel processing

### Caching

- **Common queries are cached** (1 hour TTL)
- **Cache provides 7.6x performance improvement**
- **Disable caching**: `classify(text, use_cache=False)`

### Monitoring

Check cache performance:

```bash
curl http://localhost:8001/api/admin/intent-cache-metrics
```

Monitor middleware:

```bash
curl http://localhost:8001/api/admin/intent-monitoring
```

---

## Classification Accuracy

As of October 7, 2025 (GREAT-4F), the intent classifier achieves the following accuracy:

### High-Confidence Categories (95%+ accuracy)
- **PRIORITY**: 100% accuracy - "what should I focus on", "my priorities"
- **TEMPORAL**: 96.7% accuracy - "show my calendar", "what's my schedule"
- **STATUS**: 96.7% accuracy - "show my standup", "what am I working on"

### Moderate-Confidence Categories (75-85% accuracy)
- **GUIDANCE**: 76.7% accuracy - advice and recommendation requests
- **IDENTITY**: 76.0% accuracy - bot identity and capability queries

### Classification Tips for Developers

**To maximize accuracy**:
1. **Use personal pronouns**: "my calendar" vs "the calendar"
2. **Be specific**: "show my standup" vs "show status"
3. **Use category keywords**: calendar, schedule, priorities, focus

**If classification seems wrong**:
1. Check if query uses personal pronouns (I, my, our)
2. Verify category keywords are present
3. Consider if query might legitimately fit multiple categories
4. Review disambiguation rules in classifier prompt

---

## Common Patterns

### Pattern 1: Simple Query

```python
intent = await classifier.classify("What's my schedule?")
category = intent.category  # TEMPORAL, STATUS, PRIORITY, etc.
confidence = intent.confidence  # 0.0-1.0
action = intent.action  # get_current_time, get_project_status, etc.
```

### Pattern 2: With Context

```python
intent = await classifier.classify(
    text="Create an issue",
    context={"project": "piper-morgan"}
)
```

### Pattern 3: Disable Cache

```python
intent = await classifier.classify(
    text="Real-time query",
    use_cache=False
)
```

### Pattern 4: Handle All Categories

```python
intent = await classifier.classify(user_input)

match intent.category:
    case IntentCategory.TEMPORAL:
        return await handle_temporal(intent)
    case IntentCategory.STATUS:
        return await handle_status(intent)
    case IntentCategory.PRIORITY:
        return await handle_priority(intent)
    case IntentCategory.EXECUTION:
        return await handle_execution(intent)
    case _:
        return await handle_unknown(intent)
```

---

## Architecture Reference

### Input vs Output Flow

```
User INPUT → Intent Classification (enforced here)
     ↓
Handler → Response Generation
     ↓
Piper OUTPUT → Personality Enhancement (separate concern)
```

### What Requires Intent

- ✅ **Natural language user messages** (ambiguous input)
- ✅ **Unstructured text queries**
- ❌ **Structured CLI commands** (structure = intent)
- ❌ **Output processing** (different flow)
- ❌ **Static/health/config endpoints**

### Enforcement Infrastructure

1. **IntentEnforcementMiddleware**: Monitors all HTTP requests
2. **Bypass Prevention Tests**: Prevents regressions
3. **CI/CD Scanner**: Automated bypass detection
4. **Cache Layer**: Performance optimization

---

## Troubleshooting

### Cache Not Working

- Check cache metrics endpoint - should show hits/misses
- Verify `cache_enabled: true` in metrics response
- Check for cache integration in classifier

### Bypass Detection Failing

- Run scanner: `python scripts/check_intent_bypasses.py`
- Review NL_ENDPOINTS list in middleware
- Check if new endpoint matches NL patterns

### Performance Issues

- Check if caching is enabled
- Review cache hit rate (target >60%)
- Consider increasing TTL for stable queries
- Monitor with `/api/admin/intent-cache-metrics`

### Middleware Not Enforcing

- Verify middleware is registered in FastAPI app
- Check `/api/admin/intent-monitoring` endpoint
- Ensure NL endpoints are in middleware config

### Classification Errors

- Check confidence scores (low confidence may indicate edge cases)
- Review pre-classifier patterns for common queries
- Monitor LLM fallback usage and errors

---

## Testing Guidelines

### Unit Tests

```python
# Test intent classification directly
intent = await classifier.classify("What day is it?")
assert intent.category == IntentCategory.TEMPORAL
assert intent.confidence >= 0.8
```

### Integration Tests

```python
# Test full HTTP flow
response = client.post("/api/v1/intent", json={"text": "What day is it?"})
assert response.status_code == 200
```

### Performance Tests

```python
# Test caching behavior
start = time.time()
intent1 = await classifier.classify("What day is it?")
time1 = time.time() - start

start = time.time()
intent2 = await classifier.classify("What day is it?")  # Should hit cache
time2 = time.time() - start

assert time2 < time1  # Cache should be faster
```

---

## Configuration

### Cache Settings

```python
# In services/intent_service/cache.py
CACHE_TTL = 3600  # 1 hour
MAX_CACHE_SIZE = 1000  # entries
```

### Middleware Settings

```python
# In web/middleware/intent_enforcement.py
NL_ENDPOINTS = [...]  # Natural language endpoints
EXEMPT_PATHS = [...]  # Paths that don't need intent
```

---

## Monitoring and Metrics

### Key Metrics to Track

1. **Cache Performance**:

   - Hit rate (target >60%)
   - Average response time
   - Cache size and memory usage

2. **Classification Accuracy**:

   - Confidence scores distribution
   - Pre-classifier vs LLM usage
   - Error rates by category

3. **Middleware Enforcement**:
   - NL endpoint coverage
   - Bypass detection alerts
   - Request volume by endpoint

### Alerting Recommendations

- Cache hit rate < 40%
- Intent classification errors > 5%
- Response time > 1000ms (uncached)
- Bypass detection failures

---

## Related Documentation

- **ADR-032**: Intent Classification Universal Entry
- **Pattern-032**: Intent Pattern Catalog
- **GREAT-4E Epic**: Complete validation details (126 tests, 5 load benchmarks)
- **Test Strategy**: `dev/2025/10/05/bypass-prevention-strategy.md`

---

**Status**: ✅ Production ready - All 13 categories implemented and validated

**Last Validated**: October 6, 2025 (GREAT-4E completion)
