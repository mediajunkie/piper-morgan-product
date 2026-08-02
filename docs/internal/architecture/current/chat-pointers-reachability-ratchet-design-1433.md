# CHAT_POINTERS reachability ratchet — concrete design (#1433)

**Status**: RATIFIED (Arch, 2026-08-02, same-day) with one required addition + three refinements — all folded below. Building.
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

- **`POINTER.utterance` must route DETERMINISTICALLY**, and per Arch's required addition the check asserts the **RESOLUTION PATH, not just the destination**: the static harness records WHICH surface resolved each utterance (pre-classifier hit / rail key / registry-CANONICAL / FLOOR) and **fails if the resolver is not in the deterministic set** — so "routed deterministically" and "routed somehow" can never produce identical output (the m-44 guard applied to the check itself). A POINTER that only works via the LLM classifier fails at authoring time. **No LLM call, so the check runs keyless in gating CI.**
- **Why this is immune to the #1395/Q22 oscillation class** (Arch refinement 1): Q22 oscillated because borderline LLM classification is sampled; POINTERs cannot oscillate — static pre-classifier + action-mapping resolution is deterministic by construction, which is precisely what the no-LLM constraint buys.
- **`CHAT_INVISIBLE` requires a STRUCTURED citation, not free text** (Arch refinement 2, the ADR-079 `# global-ok:` shape): every entry must name a tracked issue or PDR/ADR (`CHAT_INVISIBLE(issue=1466)` / `CHAT_INVISIBLE(ref="PDR-006")`) — enforced by the test, so the shrink-lock is auditable, not just countable. The set may only SHRINK.

## 2. Enumeration is DERIVED, membership by existing (ADR-072 / #1106 / ADR-079 precedent)

The test derives the must-be-covered surface set at collection time:
1. **Pages**: `ui.py` route decorators (AST/glob) → every served page path.
2. **Integrations**: the connectable-integration set from settings_integrations' registry.
3. **Capabilities named in decline copy**: keys of `UNWIRED_WRITE_DECLINES` + the keyword table in `_get_contextual_fallback`.

**A new page/integration/capability joins the contract by existing** — the build fails until it gets a ledger row (POINTER or justified CHAT_INVISIBLE). No one has to remember.

## 3. Decline-copy freshness (the #1426 structural half)

`assert set(UNWIRED_WRITE_DECLINES) ∩ reachable_actions == ∅` — where `reachable_actions` = the actions the ledger's POINTERs successfully resolve to plus the registry's wired set. **Denominator named per Arch refinement 3**: this reachable set covers POINTER-resolved + registry-wired paths and does NOT cover capabilities reachable by paths outside both (believed empty today); the test carries this as a comment so "complete for the space it searched" stays visible. Shipping a capability forces its stale denial out of the build **in the same commit**. Same for the `_get_contextual_fallback` keyword table (string-match on its denial keys).

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
