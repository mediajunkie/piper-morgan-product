# Intent Categories Reference

**Version**: 3.0 (Post-M1 Floor-First)
**Last Updated**: 2026-04-11
**Coverage**: 19/19 categories

## Changelog

- **2026-04-11 (v3.0)**: Full rewrite to reflect M1 floor-first routing (#911,
  ADR-060), Apr 8 IDENTITY full migration to floor (commit 33e6758a), and the
  actual 19-category enum from `services/shared_types.py`. Removed the
  "Fast Path / Workflow Path" dichotomy — it no longer reflects reality.
- **2025-10-06 (v1.0)**: Original doc; claimed 13 categories with a fast-path
  (canonical handlers, ~1ms) vs. workflow-path (LLM orchestration, 2-3s)
  split. Both the category count and the routing dichotomy are now stale.

---

## Overview

Piper Morgan's intent classification system recognizes **19 categories**
(enum: `services/shared_types.py` → `IntentCategory`). After the M1
floor-first routing inversion ([ADR-060](adrs/adr-060-floor-first-routing.md),
Issue #911), most query categories now route to the **conversational floor** —
a context-assembled LLM response — rather than to canonical template handlers.

### Why Floor-First

UAT Round 2 (Mar 2026) showed canned canonical templates scoring 1/3 on the
Colleague Test, while floor responses (LLM + assembled context) scored 7+.
The floor was already live as a fallback (#907); #911 inverted the default so
that floor is the *default* for conversational query categories and canonical
handlers run only when they offer something the LLM can't — deterministic
fast paths, database mutations, or side effects.

### Routing Pipeline

```
User Message
  -> Pre-classifier (fast pattern match)
    -> LLM Classifier (if pre-class misses)
      -> Action Gate
         | _requires_canonical_handler(intent) -> Canonical Handler
         | _should_route_to_floor(intent)      -> Conversational Floor
         | else                                -> Workflow Dispatcher (legacy)
```

Source of truth: `services/intent/intent_service.py`, methods
`_requires_canonical_handler` (line 9863) and `_should_route_to_floor`
(line 9933).

---

## The Action Gate

Two methods decide routing for categories that have been migrated to the
floor-first pattern:

### `_requires_canonical_handler(intent)` — returns True for:

| Condition | Rationale |
|-----------|-----------|
| `PORTFOLIO` (any action) | Database mutations (add/delete/archive/restore) |
| `EXECUTION` (any action) | External side effects (GitHub issue, todo writes) |
| `CONVERSATION` + `action="greeting"` | Onboarding + calendar integration side effects |
| `TEMPORAL` | Sub-millisecond deterministic time/date fast path |
| `STATUS` | Not yet migrated; handler also triggers onboarding when no projects |
| `PRIORITY` | Not yet migrated (Phase 5 of #911) |
| `GUIDANCE` + setup-topic detected | Triggers the setup workflow |

### `_should_route_to_floor(intent)` — returns True for:

Categories in `_FLOOR_ROUTED_CATEGORIES`:

```python
{"GUIDANCE", "IDENTITY", "DISCOVERY", "TRUST", "MEMORY",
 "CONVERSATION", "UNKNOWN"}
```

...unless `_requires_canonical_handler` overrides (e.g., a CONVERSATION
greeting, or a GUIDANCE setup request).

### Categories NOT in the Action Gate

`ANALYSIS`, `SYNTHESIS`, `STRATEGY`, `PLANNING`, `REVIEW`, `LEARNING`, `QUERY`
fall through to the pre-existing workflow dispatcher path
([ADR-059](adrs/adr-059-workflow-dispatcher-offer-consolidation.md)).

---

## Canonical Handler Set

From `services/intent_service/canonical_handlers.py::CanonicalHandler.can_handle()`
(line 129):

```python
canonical_categories = {
    IntentCategory.TEMPORAL,
    IntentCategory.STATUS,
    IntentCategory.PRIORITY,
    IntentCategory.GUIDANCE,       # Setup requests only (action gate enforces)
    IntentCategory.PORTFOLIO,
    IntentCategory.CONVERSATION,   # Greeting only (action gate enforces)
}
```

Per Issue #963 (M1 floor inversion cleanup), `IDENTITY`, `DISCOVERY`, `TRUST`,
and `MEMORY` were removed from this set. Any accidental routing to those
categories now falls through to the floor rather than running dead
template code.

---

## Categories (Alphabetical)

### 1. ANALYSIS

- **Routing**: Workflow Dispatcher
- **Purpose**: Data analysis and insights generation
- **Examples**: "Analyze commits from last week", "Generate a report on test coverage"

### 2. CONVERSATION

- **Routing**: Split — `action="greeting"` -> Canonical; everything else -> Floor
- **Why split**: Greeting handler triggers onboarding and calendar context
  the floor doesn't yet own. Chitchat, farewells, and thanks go to the floor.
- **Examples**:
  - Canonical: "Good morning", "Hey Piper"
  - Floor: "Thanks!", "See you later", "Got it"

### 3. DISCOVERY

- **Routing**: Floor (with capabilities context from `ContextAssembler`)
- **Purpose**: Capability queries — "What can you do?" (#488)
- **Examples**: "What are you good at?", "What can you help me with?"
- **Context surfaced**: Core capabilities list + active integrations

### 4. EXECUTION

- **Routing**: Canonical Handler
- **Purpose**: State-changing actions with external side effects
- **Examples**: "Create a GitHub issue for the login bug",
  "Mark my todo as done", "Deploy to staging"
- **Why canonical**: Action gate keeps the floor out of anything that
  writes to databases or calls integrations.

### 5. GUIDANCE

- **Routing**: Split — setup topic -> Canonical; everything else -> Floor
- **Purpose**: Recommendations, advice, "what should I focus on"
- **Context surfaced**: Calendar, project metadata, priorities, current time
  (see `_assemble_guidance_context` in `intent_service.py`)
- **Examples**:
  - Canonical: "Help me set up GitHub", "Configure Slack"
  - Floor: "What should I focus on this morning?", "How should I approach this?"

### 6. IDENTITY

- **Routing**: Floor (as of Apr 8, 2026, commit 33e6758a)
- **Purpose**: Identity queries — "Who are you?", "What's your role?"
- **Why full migration**: UAT Round 2 showed canonical template scoring 1/3,
  floor scoring 7+. The previous "core identity canonical / adjacent
  identity floor" split is gone.
- **Examples**: "Who are you?", "What's your name?", "Tell me about yourself"
- **Note**: Previous versions of this doc described a split treatment.
  That split was removed Apr 8. `_requires_canonical_handler` now returns
  `False` for IDENTITY unconditionally (line 9905).

### 7. LEARNING

- **Routing**: Workflow Dispatcher
- **Purpose**: Pattern recognition and learning
- **Examples**: "What patterns exist in our workflow?", "Learn from these examples"

### 8. MEMORY

- **Routing**: Floor (with history context from `ContextAssembler`)
- **Purpose**: Memory/history queries — "What do you remember about me?" (#674)
- **Examples**: "What have we discussed before?", "Do you remember the API refactor?"
- **Context surfaced**: Conversation history summary, recent topics, turn count

### 9. PLANNING

- **Routing**: Workflow Dispatcher
- **Purpose**: Planning and design activities
- **Examples**: "Plan the Q2 roadmap", "Design a migration strategy"

### 10. PORTFOLIO

- **Routing**: Canonical Handler (all actions)
- **Purpose**: Project portfolio management (#675)
- **Examples**: "Archive the website-v1 project", "Restore deleted project X",
  "Delete the test project"
- **Why canonical**: All portfolio operations mutate user-owned project state.

### 11. PRIORITY

- **Routing**: Canonical Handler (not yet migrated; Phase 5 of #911)
- **Purpose**: Priority assessment and focus
- **Examples**: "What's most important right now?", "Show me top priorities"

### 12. QUERY

- **Routing**: Workflow Dispatcher
- **Purpose**: General read-only data retrieval (CQRS-lite)
- **Examples**: "Look up issue #123", "Search for auth docs"

### 13. REVIEW

- **Routing**: Workflow Dispatcher
- **Purpose**: Review and validation activities
- **Examples**: "Review this PR", "Validate these requirements"

### 14. STATUS

- **Routing**: Canonical Handler (not yet migrated)
- **Purpose**: Current state and progress
- **Examples**: "What am I working on?", "Show my standup status"
- **Side effect**: When no projects exist, handler triggers portfolio onboarding.

### 15. STRATEGY

- **Routing**: Workflow Dispatcher
- **Purpose**: Strategic planning and prioritization
- **Examples**: "Plan next sprint", "Create a roadmap"

### 16. SYNTHESIS

- **Routing**: Workflow Dispatcher
- **Purpose**: Content generation and summarization
- **Examples**: "Generate a summary", "Synthesize these notes"

### 17. TEMPORAL

- **Routing**: Canonical Handler (deterministic fast path)
- **Purpose**: Time and date queries
- **Examples**: "What day is it?", "What time is it in Tokyo?",
  "When's my next meeting?"
- **Why canonical**: Sub-millisecond; no LLM call needed for pure time queries.
  Timezone-aware via `user_id` lookup.

### 18. TRUST

- **Routing**: Floor (with trust profile context from `ContextAssembler`)
- **Purpose**: Trust and relationship queries (#673)
- **Examples**: "Why can't you do X?", "How well do you know me?",
  "Can I trust you with this?"
- **Context surfaced**: Trust stage, interaction count

### 19. UNKNOWN

- **Routing**: Floor (floor-routed since #907)
- **Purpose**: Fallback for unclassified or ambiguous input
- **Examples**: "Blarghhh", vague messages the classifier can't pin down
- **Behavior**: Floor engages conversationally rather than emitting a
  "didn't understand" deflection.

---

## The Conversational Floor

All floor-routed intents pass through `ConversationalFloor.respond()` in
`services/intent_service/conversational_floor.py`. The flow:

1. **Context assembly**: `ContextAssembler.gather_context()` pulls
   category-specific structured data (calendar, projects, trust profile,
   capabilities, history summary, etc.)
2. **History**: Last 6 `ConversationTurn` records — both `user_message` and
   `response` fields (the `response` field was added in #922 / commit
   `25437f95` so the floor sees Piper's prior replies, not just the user's)
3. **Floor prompt build**: System prompt = base Piper identity +
   `FLOOR_SYSTEM_PROMPT_ADDENDUM` + warmth guidance. User prompt =
   history + `[Available context: ...]` block + current message.
4. **LLM call**: `task_type="conversation"` via `LLMClient.complete()`
5. **Fallback**: On error, `_classify_llm_error` picks one of
   `FLOOR_FALLBACK_AUTH`, `FLOOR_FALLBACK_NO_PROVIDER`, or
   `FLOOR_FALLBACK_TRANSIENT` (see [llm-configuration.md](llm-configuration.md)).

### Fabrication Guardrails (#960)

The floor system prompt (updated in commit `4789de64`) explicitly prohibits
inventing user data when the context block is empty. If the user asks about
their todos and no todo data was assembled, the floor must say so ("I don't
see any todos in your list right now") rather than making up plausible-looking
items. This addressed the #960 class of bugs where floor responses referenced
projects, issues, or meetings that did not exist.

---

## Instrumentation

- `floor_hit=True` is set on all floor responses (`IntentProcessingResult.intent_data`)
- `conv_ctx.last_response_was_floor` and `last_floor_category` are tagged for
  continuation-rate analytics (#913)
- `conversational_floor_hit` log event includes session, user, category,
  action, confidence, and response length

---

## Related Documentation

- [ADR-060: Floor-First Routing](adrs/adr-060-floor-first-routing.md) — the ADR
  behind #911; note the ADR itself has some staleness but the core principle stands
- [ADR-059: Workflow Dispatcher](adrs/adr-059-workflow-dispatcher-offer-consolidation.md) — the
  legacy path that workflow-routed categories still take
- [architecture.md](architecture.md) — system-wide view
- [llm-configuration.md](llm-configuration.md) — provider-agnostic LLM setup

---

**Document Status**: Current as of 2026-04-11
**Source files**:
- `services/shared_types.py` (enum definition)
- `services/intent/intent_service.py` (action gate, lines 9829-9962)
- `services/intent_service/canonical_handlers.py` (canonical set, line 129)
- `services/intent_service/conversational_floor.py` (floor impl + guardrails)
