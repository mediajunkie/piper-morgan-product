# #714 MUX-LISTS-STALENESS-UI — Phase 0 Staleness Design v0

**Date**: 2026-05-03
**Author**: Lead Developer
**Status**: Design v0 (input to Phase 1 implementation)

---

## Decisions (per PM audit walkthrough May 3)

### 1. Definition (Q2 disposition: Option C — lazy effective timestamp)

A list is **stale** when:

```
effective_updated_at = max(
    List.updated_at,
    max(ListItem.added_at for ListItem in list_items, default=List.updated_at)
)
days_since_update = (now() - effective_updated_at).days
is_stale = days_since_update > THRESHOLD_DAYS
```

**Rationale**: A list with fresh contents shouldn't be marked stale just because the List record itself wasn't directly modified. Adding an item bumps `ListItem.added_at` but may not bump `List.updated_at` (depending on the upstream code path that creates list memberships). Taking the max captures both signals.

**Note on per-item activity**: `ListItemDB` schema (`services/database/models.py:1610`) has only `added_at`, NOT `updated_at`. So we capture "is anyone adding items to this list?" but NOT "is anyone modifying items already in the list?". For MVP this is acceptable; richer per-item-modification staleness would require the polymorphic join through Todo/Feature/Bug `updated_at` fields, which is out of scope.

### 2. Threshold (Q3 disposition)

**60 days** default, env-configurable via `PIPER_LIST_STALENESS_DAYS`. Single threshold for all list types (no per-`list_type` differentiation for MVP). Tunable later if observation data surfaces "this is too aggressive for sprint lists" or "too lax for personal lists."

### 3. Visual treatment (Q4 disposition: Option A — subtle muted card)

- Stale lists: muted background (use existing `--color-background-tertiary` token) + reduced opacity (~0.85) on the list card
- Inline hint text: `"Last updated N days ago"` (informational, NOT punitive)
- No "Stale!" badge (would feel accusatory; conflicts with conceptual-integrity principle)

### 4. Conceptual-integrity language (Q5 disposition)

OK vocabulary: `stale`, `old`, `untouched`, `last updated`, `haven't touched`
NOT OK: `archived`, `RATIFIED` / any lifecycle stage name as visible text, `deprecated`, `obsolete`

The `staleness` field on the API response should be named `staleness`, NOT `lifecycle_state` or anything implying it's a lifecycle stage.

---

## Data flow

```
GET /api/v1/lists
  ↓
list_repo.get_lists_by_owner(user.sub)  → List[domain.List]
  ↓
For each list:
  fetch ListItem.added_at values from DB (small query per list)
  compute effective_updated_at
  build StalenessSignal{is_stale, days_since_update, last_updated_human}
  ↓
Response: lists[].staleness = {...}
```

**Performance note**: At alpha scale (1 user, <10 lists, <100 items per list), per-list item-fetch is sub-second. Post-MVP optimization path: denormalize `last_item_activity_at` on `ListDB` and update on item-add; eliminates the join.

---

## API response shape

```json
{
  "lists": [
    {
      "id": "...",
      "name": "Books to Read",
      "description": "...",
      "owner_id": "...",
      "created_at": "...",
      "staleness": {
        "is_stale": true,
        "days_since_update": 73,
        "last_updated_human": "73 days ago"
      }
    }
  ],
  "count": 1
}
```

Backwards-compat: `staleness` is a NEW field; existing consumers ignore it. UI consumers read it and render the muted treatment + hint.

---

## Implementation phases

- **Phase 1**: `compute_staleness()` helper + `last_updated_human()` formatter; threshold from env. Pure functions, easy unit tests.
- **Phase 2**: API endpoint integration — `web/api/routes/lists.py:216` GET adds the per-list ListItem fetch + staleness computation.
- **Phase 3**: `templates/lists.html` UI — muted card + hint text (no JS dependency on lifecycle indicator; this is a different concept).
- **Phase Z**: handoff + #703 / M2d gate update.

---

## Out of scope (Post-MVP)

- Per-item-modification staleness (would require polymorphic join through Todo/Feature/Bug)
- Differentiated thresholds by `list_type` (sprint vs personal)
- Auto-archive stale lists (would conflate staleness with ARCHIVED transition — explicit Q5 / AC violation)
- Denormalized `last_item_activity_at` (Post-MVP optimization)
