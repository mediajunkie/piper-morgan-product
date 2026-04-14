# Combined Audit: #960 + #961

## Status of #960 (floor guardrails)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Hard guardrail in system prompt | ✅ DONE | Commit 4789de64 (Apr 11) |
| Context contract | Open | This session |
| Audit existing routes | Open | Combined with #961 |

## Status of #961 (route audit)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Map all floor routes + context | Open | This session |
| Find data-query gaps | Open | This session |
| Define context contract | Open | Combined with #960 |
| Add tests | Open | known_pathological category per PA cross-pollination |

## Combined approach

1. Audit: map every floor-routed category → ContextAssembler output
2. Gap identification: where can users ask for data the context doesn't provide?
3. Contract: minimum required context per category
4. Enforcement: log violations + known_pathological test category

## Audit result: proceeding directly to research (no separate gameplan needed — scope is research + documentation + small code component)
