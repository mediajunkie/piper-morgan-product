# Intent Classification Developer Guide

**Last Updated**: April 11, 2026
**Status**: Current (post-M1 floor inversion)
**See also**: [Architecture Decision Record (ADR) 060: Floor-First Routing](../internal/architecture/current/adrs/adr-060-floor-first-routing.md), [Canonical Handlers Architecture](canonical-handlers-architecture.md)

> **REWRITE NOTE (April 11, 2026)**
> The previous version of this guide described a "fast path canonical (~1ms)
> vs workflow handler (2000-3000ms)" dichotomy and listed 13 intent categories.
> That model is obsolete. After M1's floor inversion (Issue #911) and the
> April 8 IDENTITY full migration to the floor (commit `33e6758a`), the
> conversational floor is the default routing destination. Canonical handlers
> now serve only mutation operations and a small set of fast-path exceptions.
> The actual intent category count is 19, not 13. This doc has been rewritten
> to reflect current reality; see the Changelog for history.

---

## Overview

Intent classification is **mandatory** for all natural-language user input
that hits Piper Morgan. The classifier decides which `IntentCategory` a
message belongs to; the action gate then decides whether that intent
routes to the conversational floor or to a canonical handler.

**Source of truth**:

- `services/shared_types.py` — `IntentCategory` enum (19 values)
- `services/intent_service/pre_classifier.py` — deterministic pattern
  matcher run before the LLM
- `services/intent_service/classifier.py` — LLM-backed classifier
- `services/intent/intent_service.py` — orchestration, including the
  action gate methods `_requires_canonical_handler` and
  `_should_route_to_floor`
- `services/intent_service/canonical_handlers.py` — `can_handle()` for
  canonical category scope
- `services/intent_service/conversational_floor.py` — floor response
  generation

---

## Intent Categories (Current List)

Per `services/shared_types.py`, there are **19** intent categories:

| Category | Typical example | Default destination |
|---|---|---|
| `EXECUTION` | "Create a GitHub issue for X" | canonical (mutations) |
| `ANALYSIS` | "Analyze our sprint velocity" | dispatcher |
| `SYNTHESIS` | "Generate a release summary" | dispatcher |
| `STRATEGY` | "Plan the next quarter" | dispatcher |
| `PLANNING` | "Draft a design doc outline" | dispatcher |
| `REVIEW` | "Review this PR description" | dispatcher |
| `LEARNING` | "What patterns do you see?" | dispatcher |
| `QUERY` | CQRS-lite read-only data retrieval | dispatcher |
| `CONVERSATION` | "Hi", "thanks", chitchat | floor (greeting → canonical) |
| `IDENTITY` | "Who are you?" | **floor** (as of Apr 8, 2026) |
| `DISCOVERY` | "What can you do?" | **floor** |
| `TEMPORAL` | "What day is it?" | canonical (fast path) |
| `STATUS` | "What am I working on?" | canonical (pending migration) |
| `PRIORITY` | "What's my top priority?" | canonical (pending migration) |
| `GUIDANCE` | "What should I focus on?" | floor — except setup requests, which stay canonical |
| `TRUST` | "Why can't you…?" / "How well do you know me?" | **floor** |
| `MEMORY` | "What do you remember about me?" | **floor** |
| `PORTFOLIO` | "Archive project X" | canonical (mutations) |
| `UNKNOWN` | unclassifiable input | floor |

"Dispatcher" means the request falls through to the legacy workflow/handler
dispatch path — neither the floor nor a canonical handler. Categories
currently labeled "dispatcher" are out of scope for the floor/canonical
split this guide describes.

---

## Classification Flow

When a natural-language message reaches the intent service, it passes
through four stages:

```
User message
     │
     ▼
1. Pre-classifier (deterministic patterns)
     │   services/intent_service/pre_classifier.py
     │   Fast pattern match for common shapes; also performs multi-intent
     │   detection and returns a MultiIntentResult. If the pre-classifier
     │   is confident, its output is used directly and the LLM is skipped.
     │
     ▼  (on miss)
2. LLM classifier
     │   services/intent_service/classifier.py
     │   Full LLM classification with PIPER.md context, cache lookup, and
     │   conversation-context-aware follow-up resolution.
     │
     ▼
3. Action Gate
     │   services/intent/intent_service.py
     │   _requires_canonical_handler(intent) → True means canonical
     │   _should_route_to_floor(intent)       → True means floor
     │
     ▼
4. Dispatch
         ├── CanonicalHandlers.handle()      (mutation / fast path)
         ├── _handle_floor_with_context()    (conversational floor)
         └── legacy workflow dispatcher      (unmigrated categories)
```

### Stage 1: Pre-classifier

`services/intent_service/pre_classifier.py` holds the deterministic
patterns that recognize common message shapes. A hit here is sub-millisecond
and skips the LLM entirely. The pre-classifier also handles multi-intent
detection (Issue #595) and returns a `MultiIntentResult` that downstream
code uses to pick a primary intent.

### Stage 2: LLM classifier

`services/intent_service/classifier.py` runs when the pre-classifier
misses or returns low confidence. It loads PIPER.md context for the user,
consults the intent cache, resolves follow-ups against conversation
context, and returns an `Intent` with category, action, confidence, and
extracted slots.

### Stage 3: Action Gate

The action gate is the routing decision layer introduced in Issue #911
Phase 2. It has two methods in `services/intent/intent_service.py`:

- **`_requires_canonical_handler(intent)`** (around line 9863). Returns
  `True` only for intents that need side effects, database writes, or
  deterministic fast-path responses. The positive test for canonical
  routing.
- **`_should_route_to_floor(intent)`** (around line 9933). Returns `True`
  for intents in floor-migrated categories, unless the canonical gate
  above claims them first.

The two methods are complementary, not strict inverses: a category can be
unmigrated (returns `False` from both) and fall through to the legacy
dispatcher.

See [ADR-060](../internal/architecture/current/adrs/adr-060-floor-first-routing.md)
for the rationale behind this gate structure.

### Stage 4: Dispatch

- **Canonical path**: `CanonicalHandlers.handle()` in
  `services/intent_service/canonical_handlers.py`. Runs for TEMPORAL,
  STATUS, PRIORITY, GUIDANCE (setup only), PORTFOLIO, CONVERSATION
  (greeting only), and EXECUTION.
- **Floor path**: `_handle_floor_with_context()` assembles category-specific
  context via `ContextAssembler`, builds a `FloorContext`, and calls
  `ConversationalFloor.respond()`. Runs for IDENTITY, DISCOVERY, TRUST,
  MEMORY, most GUIDANCE, most CONVERSATION, and UNKNOWN.
- **Legacy dispatcher**: Unmigrated categories (ANALYSIS, SYNTHESIS,
  STRATEGY, PLANNING, REVIEW, LEARNING, QUERY) fall through to the
  workflow handlers.

---

## When Intent Classification is Required

### Required (natural-language input)

- User text messages (Slack, chat, conversational UI)
- Free-text queries
- Ambiguous requests that need interpretation
- Natural-language commands

### Not required (exempt)

- Structured CLI commands where argparse/click parameters already express
  intent explicitly
- Output processing (personality enhancement operates on Piper's responses,
  not user input)
- Direct ID lookups (`/api/v1/workflows/12345`)
- Static resources — health checks, docs, config

Exempt paths are managed in `web/middleware/intent_enforcement.py`.

---

## Adding a New Natural-Language Endpoint

### 1. Register with the enforcement middleware

Edit `web/middleware/intent_enforcement.py` and add your path to the
appropriate list. Use the `/api/v1/` prefix per the project's API
conventions.

```python
NL_ENDPOINTS = [
    '/api/v1/intent',
    '/api/v1/standup',
    '/api/v1/chat',
    '/api/v1/your-new-endpoint',  # add here
]
```

### 2. Route through the intent service

The simplest option is to delegate to the universal intent endpoint, so
all natural-language traffic shares the same pre-classifier → classifier
→ action-gate pipeline:

```python
@app.post("/api/v1/your-new-endpoint")
async def your_endpoint(request: Request):
    return await process_intent(request)
```

If you need custom pre-processing, call the classifier directly and let
the action gate decide routing:

```python
from services.intent_service.classifier import classifier

intent = await classifier.classify(user_text)
# Don't branch on category yourself — let the action gate do it.
# Call the main intent service entry point that runs the gate.
```

Avoid branching on `intent.category` in your endpoint and dispatching to
handlers by hand. Every hand-rolled branch is a new place for
floor/canonical routing to drift out of sync with the action gate.

### 3. Add tests

Exercise the endpoint from `tests/intent/` so bypass prevention tests
cover it. The test suite verifies that new NL endpoints actually go
through the classifier.

### 4. Validate

```bash
python scripts/check_intent_bypasses.py
pytest tests/intent/ -v
curl http://localhost:8001/api/v1/admin/intent-monitoring
```

---

## Caching

Intent classification results are cached (see
`services/intent_service/cache.py`). Cache hits bypass the LLM and return
sub-millisecond. Disable per-call with `classify(text, use_cache=False)`
when you need fresh classification (e.g., in integration tests that
manipulate PIPER.md mid-run).

---

## Common Patterns

### Let the pipeline handle routing

```python
# Preferred: send to the universal intent endpoint.
response = await client.post("/api/v1/intent", json={"text": user_text})
```

### Classify for inspection only

```python
from services.intent_service.classifier import classifier

intent = await classifier.classify("What's my schedule?")
# intent.category → IntentCategory.TEMPORAL
# intent.confidence → 0.0–1.0
# intent.action → e.g., "get_current_time"
```

### Test category coverage

```python
@pytest.mark.parametrize("text,expected_category", [
    ("what day is it", IntentCategory.TEMPORAL),
    ("who are you", IntentCategory.IDENTITY),
    ("archive piper-morgan", IntentCategory.PORTFOLIO),
])
async def test_classification(text, expected_category):
    intent = await classifier.classify(text)
    assert intent.category == expected_category
```

Note that asserting on category is reasonable; asserting on "which
handler ran" is not, because that's an action-gate decision that may
change as categories migrate to the floor.

---

## Troubleshooting

### Intent classified correctly but wrong code path ran

This is almost always an action-gate question, not a classifier question.
Check `_requires_canonical_handler` and `_should_route_to_floor` in
`services/intent/intent_service.py`. If you think a category should
route differently, open an issue and reference ADR-060.

### Low confidence on queries that used to work

The LLM classifier is sensitive to PIPER.md context. If a user's PIPER.md
changed recently, clear the intent cache and reclassify. For persistent
drift, check `pre_classifier.py` patterns and consider adding a pattern
for the common shape.

### New NL endpoint not enforcing classification

Run `python scripts/check_intent_bypasses.py` and make sure the endpoint
is in `NL_ENDPOINTS`. The bypass scanner is your friend.

### Floor and canonical disagree about who handles a category

`_requires_canonical_handler` wins. `_should_route_to_floor` explicitly
defers to it (see the "If the Action Gate says canonical is required,
don't route to floor" check around line 9959 of `intent_service.py`).

---

## Monitoring

Admin endpoints (all under `/api/v1/admin/`):

- `intent-monitoring` — middleware enforcement status and NL endpoint list
- `intent-cache-metrics` — cache hit rate, size, memory usage
- `piper-config-cache-metrics` — PIPER.md loader cache (affects
  classifier context)

Key things to watch:

- Cache hit rate — low rates mean the LLM is being hit more than needed
- Classification confidence distribution — a lot of low-confidence
  results can indicate a missing pre-classifier pattern or a drifting
  LLM prompt
- Pre-classifier vs LLM usage split — most common shapes should be
  matched by the pre-classifier

---

## Related Documentation

- [ADR-060: Floor-First Routing](../internal/architecture/current/adrs/adr-060-floor-first-routing.md) —
  the routing principle this guide implements
- [Canonical Handlers Architecture](canonical-handlers-architecture.md) —
  current canonical scope and the action gate
- [Canonical Queries Architecture (historical)](../internal/architecture/canonical-queries-architecture.md) —
  the pre-M1 design, preserved as historical context

---

## Changelog

- **2026-04-11**: Body rewritten for post-M1 reality. Category count
  corrected from 13 to 19. Replaced fast-path/workflow dichotomy with
  pre-classifier → LLM → action gate → floor/canonical/dispatcher flow.
  Added cross-references to ADR-060 and the canonical handlers guide.
  Retained the stale-warning note at the top, repositioned as a rewrite
  note so readers know what changed.
- **2025-10-06**: Original GREAT-4E document describing 13 categories
  and a fast-path (~1ms) vs workflow-handler (2000–3000ms) split.
</content>
</invoke>
