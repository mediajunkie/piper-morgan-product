# Canonical Handlers Architecture

**Last Updated**: April 11, 2026
**Status**: Current (post-M1 floor inversion)
**See also**: [Architecture Decision Record (ADR) 060: Floor-First Routing](https://github.com/mediajunkie/piper-morgan-product/blob/main/docs/internal/architecture/adrs/adr-060-floor-first-routing.md)

---

## Overview

Canonical handlers are the **narrow exception** in Piper Morgan's routing
model, not the conversational core. After M1's floor-first inversion
(Issue #911) and the April 8, 2026 IDENTITY migration to the floor (commit
`33e6758a`), most user queries route through the conversational floor with
contextual assembly. Canonical handlers run only for a small set of
categories where a deterministic fast path or a database-mutating side
effect is required.

This guide describes the current canonical scope, the detection methods
that drive action-gate routing, and the places where "canonical" and
"dead code" now overlap.

**Prior version**: Dated October 6, 2025 (GREAT-4C), this doc described
five canonical handlers (Identity, Temporal, Status, Priority, Guidance)
as "the core of Piper Morgan's conversational interface" with a fast-path
framing of ~1ms responses. That framing is obsolete — see the Changelog
at the bottom.

---

## Current Canonical Scope

The authoritative list is `CanonicalHandlers.can_handle()` in
`services/intent_service/canonical_handlers.py` (around line 129). As of
M1:

```python
canonical_categories = {
    IntentCategoryEnum.TEMPORAL,      # fast-path date/time
    IntentCategoryEnum.STATUS,        # project status (not yet migrated)
    IntentCategoryEnum.PRIORITY,      # focus queries (not yet migrated)
    IntentCategoryEnum.GUIDANCE,      # setup requests only — action gate enforces
    IntentCategoryEnum.PORTFOLIO,     # project mutations (add/delete/archive/restore)
    IntentCategoryEnum.CONVERSATION,  # greeting only — action gate enforces
}
```

**Removed from this set** in M1: `IDENTITY`, `DISCOVERY`, `TRUST`,
`MEMORY`. Issue #963 removed them so any accidental routing falls through
to the floor instead of reaching dead code.

### Why each category is still canonical

- **TEMPORAL**: Pure time queries ("what day is it?") are deterministic
  and sub-millisecond. There's no benefit to sending them through the
  floor.
- **STATUS**: Triggers onboarding when no projects exist; otherwise still
  goes through canonical because it hasn't been migrated yet. Listed as
  future floor migration work.
- **PRIORITY**: Not yet migrated to floor (tracked for Phase 5 of the
  floor-routing work).
- **GUIDANCE (setup only)**: When `_detect_setup_request()` matches, the
  canonical path triggers the setup workflow. All other GUIDANCE queries
  route to the floor.
- **PORTFOLIO**: All operations are database mutations
  (add/delete/archive/restore projects). These must run as canonical
  actions, not floor conversation.
- **CONVERSATION (greeting only)**: Greeting has calendar side effects
  and onboarding integration. `_requires_canonical_handler` keeps it
  canonical "until floor has calendar context integration." Other
  CONVERSATION actions (chitchat, farewell, thanks) route to the floor.

Also canonical but governed by `_requires_canonical_handler` rather than
`can_handle()`:

- **EXECUTION**: All operations (create issue, manage todos, etc.) are
  side-effecting and always canonical.

---

## The Action Gate

The action gate is the decision layer that chooses between floor and
canonical routing. Its two key methods live in
`services/intent/intent_service.py` (around lines 9863 and 9933):

- **`_requires_canonical_handler(intent)`** — returns `True` only for
  intents that need side effects, database writes, or deterministic
  fast-path responses. This is the positive test for canonical routing.
- **`_should_route_to_floor(intent)`** — returns `True` for intents in
  categories that have been migrated to floor routing, unless the
  canonical gate above claims them first.

The gate runs **after** intent classification and **before** handler
dispatch. A simplified view:

```
Intent classified
      │
      ▼
_requires_canonical_handler? ──yes──▶ CanonicalHandlers.handle()
      │
     no
      │
      ▼
_should_route_to_floor?      ──yes──▶ _handle_floor_with_context()
      │
     no
      │
      ▼
Fall through to legacy dispatcher (workflow handlers, etc.)
```

See ADR-060 for the design rationale.

---

## Pattern Detection: Alive Even When the Handler is Dead

`CanonicalHandlers` still exposes pattern-detection methods that the
action gate relies on, even though the corresponding `_handle_*_query`
methods for IDENTITY/DISCOVERY/TRUST/MEMORY are now dead code in
production.

Active detection methods (in `canonical_handlers.py`):

- `_detect_setup_request(intent)` — line ~2455. Returns a setup topic
  string when the user is asking for setup/onboarding help. Used by
  `_requires_canonical_handler` to keep GUIDANCE-setup canonical.
- `_detect_health_check_request(intent)` — line ~439. Used by
  `_is_adjacent_identity` in the action gate to detect identity-adjacent
  "are you okay?" style queries.
- `_detect_differentiation_request(intent)` — line ~462. "How are you
  different from X?" Used by `_is_adjacent_identity`.
- `_detect_help_request(intent)` — line ~2497. "Can you help me get
  started?" Used by `_is_adjacent_identity`.

**Why these are still here**: The detection methods are useful feature
extractors. The action gate uses them to make routing decisions; it
doesn't care that the old identity/help/differentiation handlers they
were originally paired with no longer run in production. If you're
cleaning up canonical_handlers.py, **do not** remove these detection
methods without also updating the action gate.

---

## Dead Code You Can Ignore (but probably shouldn't delete yet)

The following `_handle_*_query` methods still exist on `CanonicalHandlers`
but are never reached in production because their categories fall out of
`can_handle()`:

- `_handle_identity_query`
- `_handle_discovery_query`
- `_handle_trust_query`
- `_handle_memory_query`

These are preserved for git archaeology and to make a roll-back possible
if the floor migration has to be reversed. Do not route new code at them.
If you're adding a feature for one of these categories, add it to the
floor context assembler (`services/intent_service/context_assembler.py`)
and the conversational floor response path
(`services/intent_service/conversational_floor.py`).

---

## Response Format (when canonical handlers run)

Canonical handlers still return the standard response dict:

```python
{
    "message": "User-facing response text",
    "is_generic_response": False,  # Issue #908: flag for generic templates
    "intent": {
        "category": "...",
        "action": "...",
        "confidence": 1.0,
        "context": {...},
    },
    "requires_clarification": False,
    # Handler-specific fields (error, action_required, etc.)
}
```

Issue #907/#908 added the `is_generic_response` flag so the action gate
can detect template-style canonical responses and optionally fall through
to the floor. If you write a new canonical handler that returns a
hand-rolled template message, set `is_generic_response=True` in the
return dict.

---

## Related Source of Truth

| Concern | File | Key symbol |
|---|---|---|
| Canonical category set | `services/intent_service/canonical_handlers.py` | `CanonicalHandlers.can_handle` |
| Canonical vs floor decision | `services/intent/intent_service.py` | `_requires_canonical_handler`, `_should_route_to_floor` |
| Floor context assembly | `services/intent_service/context_assembler.py` | `ContextAssembler.gather_context` |
| Floor response generation | `services/intent_service/conversational_floor.py` | `ConversationalFloor.respond` |
| Intent category enum (19 values) | `services/shared_types.py` | `IntentCategory` |
| Routing principle | `docs/internal/architecture/adrs/adr-060-floor-first-routing.md` | — |

---

## Changelog

- **2026-04-11**: Rewritten for post-M1 reality. Canonical handlers are
  now the narrow exception, not the conversational core. IDENTITY,
  DISCOVERY, TRUST, and MEMORY have been removed from `can_handle()` and
  route to the floor. Added Action Gate section and distinguished
  detection methods (alive) from dead `_handle_*_query` methods. Added
  cross-reference to ADR-060.
- **2025-10-06**: Original GREAT-4C document describing five canonical
  handlers (Identity, Temporal, Status, Priority, Guidance) as the core
  of the conversational interface, with fast-path ~1ms framing.
</content>
</invoke>
