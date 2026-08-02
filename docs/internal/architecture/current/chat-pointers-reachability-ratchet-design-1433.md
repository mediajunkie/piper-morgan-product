# CHAT_POINTERS reachability ratchet — concrete design (#1433)

**Status**: DESIGN — awaiting Arch ratification (supersedes the un-answered 2026-07-16 census memo by carrying the full buildable design; Lead, 2026-08-02).
**Extends**: the #1283 routing-vocabulary ratchet (registry-outward) with the missing product-inward half.
**The defect class it kills**: a shipped user-facing surface no chat utterance can reach (integrations-connect ×4, file-upload, api-keys, lists, work-items — census 2026-07-16), and its dual: decline copy that denies a shipped capability (#1426's false denials, cured 7/16 but unguarded against recurrence).

## 1. The ledger (declarative, in `tests/test_architecture_enforcement.py`)

```python
CHAT_POINTERS = {
    # surface_id: POINTER(utterance=..., expects=DEST) | CHAT_INVISIBLE(reason=...)
    "page:/files":        POINTER("upload a file", expects=("execution", "upload_file")),
    "integration:github": POINTER("connect my github account", expects=("execution", "connect_integration")),
    "capability:create_reminder": POINTER("remind me tomorrow at 9 to check CI",
                                          expects=("execution", "create_reminder")),
    "page:/learning":     CHAT_INVISIBLE("dashboard-only by design; PDR-XXX"),
    ...
}
```

- **`POINTER.utterance` must route DETERMINISTICALLY**: resolved by pre-classifier pattern hit, rail key, or registry-CANONICAL/FLOOR — asserted by running the pre-classifier + action-mapping statically. **No LLM call, so the check runs keyless in gating CI** (this is what makes it a ratchet and not an llm-lane test).
- **`CHAT_INVISIBLE` requires a reason and the set may only SHRINK** (shrink-lock, MAX-count style): deliberate chat-invisibility is allowed but always visible and always a decision.

## 2. Enumeration is DERIVED, membership by existing (ADR-072 / #1106 / ADR-079 precedent)

The test derives the must-be-covered surface set at collection time:
1. **Pages**: `ui.py` route decorators (AST/glob) → every served page path.
2. **Integrations**: the connectable-integration set from settings_integrations' registry.
3. **Capabilities named in decline copy**: keys of `UNWIRED_WRITE_DECLINES` + the keyword table in `_get_contextual_fallback`.

**A new page/integration/capability joins the contract by existing** — the build fails until it gets a ledger row (POINTER or justified CHAT_INVISIBLE). No one has to remember.

## 3. Decline-copy freshness (the #1426 structural half)

`assert set(UNWIRED_WRITE_DECLINES) ∩ reachable_actions == ∅` — where `reachable_actions` = the actions the ledger's POINTERs successfully resolve to plus the registry's wired set. Shipping a capability forces its stale denial out of the build **in the same commit**. Same for the `_get_contextual_fallback` keyword table (string-match on its denial keys).

## 4. F24 folds (same commit as the ratchet lands)

- The 5 pre-classifier actions absent from ACTION_REGISTRY → register or ledger-justify.
- The circular validator noted in the census → replaced by this test's derived enumeration.
- `intent-routing-stack.md` stale rail count → corrected; doc gains a pointer to this ratchet as the enforcement surface.

## 5. What this deliberately does NOT do

- No LLM-quality claims (a POINTER passing ≠ good conversation — that's #1468's lane).
- No new runtime code: the ledger is test-side; product changes only where a POINTER exposes a genuinely unreachable surface (each becomes its own tracked fix, like the census issues).
- No blanket "everything must be chat-reachable" policy: CHAT_INVISIBLE is legitimate, justified, shrinking.

## 6. Sequencing

1. Arch ratifies this design (the 7/16 memo's ask, now with the concrete shape).
2. Ledger + ratchet land with **current-truth rows** (today's unreachable surfaces enter as CHAT_INVISIBLE with `reason="census F-finding #N, fix tracked in #XXXX"` — honest baseline, no big-bang fixes).
3. #1428 ("what can you do" understates) builds ON the ledger — the capability answer derives from POINTER rows instead of rail descriptions (wave 3, with #1466).
4. Census F-findings graduate rows from CHAT_INVISIBLE → POINTER as their fixes land; the shrink-lock records each.
