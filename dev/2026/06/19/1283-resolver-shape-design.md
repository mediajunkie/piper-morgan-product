# #1283 — Reachability resolver: shape design + preliminary gap list (for Arch ratification)

**Author**: Lead Dev · **Date**: 2026-06-19 · **Sprint**: RECONNECT
**Status**: DESIGN — for Arch to ratify the shape + the intentional-floor-allowlist representation BEFORE structural commits (per Arch memo 2026-06-19: "Bring me the gap list + the resolver shape; I'll ratify the structural pieces").
**Scope confirmed with Arch**: vocabulary-first derive (not examples) · mode-4-guard-first · one resolver shared by probe + lint · reachability = rail ∪ category ∪ floor.

## The routing model (verified read of `services/intent/intent_service.py`, 2026-06-19)

The classifier emits a **free-text `action` string** + a **`category`** (IntentCategory enum). `process_intent` routes in this order:

1. **RAIL** (`:1446`): `if intent.action in get_action_workflows(): dispatch`. The rail set = every `WorkflowEntry(..., action_triggered=True)` in `services/intent_service/workflow_entries.py`. Deterministic handler. **This is the canonical action vocabulary** — the SoT we derive the prompt vocab from (kills drift modes 2/3).
2. **CATEGORY** (`_requires_canonical_handler`, `:10960`, keyed on `category`, NOT action):
   - `PORTFOLIO`, `EXECUTION` → canonical (always).
   - `CONVERSATION`+`action=="greeting"` → canonical.
   - `TEMPORAL` → canonical (pure date/time) **or** floor (conversational keywords regex).
   - `GUIDANCE` → canonical iff `_detect_setup_request`, else floor.
   - `STATUS`, `PRIORITY`, `IDENTITY` → floor (return False).
3. **FLOOR** (`_should_route_to_floor`, `:11040`): routes to floor-with-context iff `category in _FLOOR_ROUTED_CATEGORIES` = {GUIDANCE, IDENTITY, DISCOVERY, TRUST, MEMORY, CONVERSATION, TEMPORAL, STATUS, PRIORITY, UNKNOWN}.
4. **LEGACY fall-through** (`:11065`): category NOT in the floor set AND not canonical → legacy `can_handle()`→`handle()`. Unpredictable; the drift sink.

## The defect class (what "reachable" must mean)

The #1269 fabrication: classifier emitted `get_project_status` (off-rail) + category `STATUS` → step 2 returns False → step 3 floor-with-context. The floor answered a standup-shaped question with **no standup data assembled** (the action implied a capability the category route doesn't carry) → it **improvised a fabricated standup**.

So "reachable" is NOT "routes somewhere" (everything eventually routes — floor or legacy). The integrity property is: **a confident action resolves to a handler that actually delivers the capability the action names** — OR the system is honest that it can't. The two failure shapes:
- **Hard gap**: action's category falls to LEGACY (step 4) — no intentional route at all.
- **Soft gap (the #1269 shape)**: action is off-rail, its category floor-routes, but the floor has no data for the implied capability → fabrication.

## Resolver shape (proposed)

A single pure function consumed by BOTH the behavioral probe and the static lint (so they can't disagree on "reachable"):

```
resolve(action: str, category: str) -> Resolution
  RAIL            — action in get_action_workflows()                  (deterministic handler)
  CATEGORY_CANON  — _requires_canonical_handler(category, ...) is True (canonical handler)
  CATEGORY_FLOOR  — category in _FLOOR_ROUTED_CATEGORIES               (floor-with-context)
  FLOOR_ALLOWED   — action in INTENTIONAL_FLOOR_ALLOWLIST              (off-rail by design)
  GAP             — none of the above (legacy fall-through / unhandled)
```

- **Static lint** (every-commit, `test_architecture_enforcement.py`): for every action in the derived vocabulary, `resolve(action, its-declared-category) != GAP`. Ratchet: zero GAPs.
- **Behavioral probe / golden corpus** (canonical-retest): run representative phrasings → classifier → assert the emitted (action, category) resolves to the *intended* capability, catching the SOFT gap (mode-4) that static reachability can't see.

## The intentional-floor-allowlist representation (Arch's open question)

Arch: "how the intentional-floor allowlist is represented … keep it small, explicit, and reviewed, or it becomes the next drift surface."

**Proposal**: a module-level `frozenset[str]` `INTENTIONAL_FLOOR_ALLOWLIST` co-located with the resolver (e.g. `services/intent_service/reachability.py`), each entry one line with an inline comment justifying why it has no rail handler (e.g. chitchat/farewell/thanks → floor by design). Reviewed like the lint baselines. **Distinct from `_FLOOR_ROUTED_CATEGORIES`** (which is category-level + already explicit): the allowlist is the small set of *actions* that legitimately resolve via floor without a rail handler. Kept minimal; the lint flags any NEW off-rail action not in it as a GAP (forcing a deliberate add-with-justification, not silent drift).

## mode-4 guard (land FIRST, per Arch)

Independent of the derive/lint: at the floor entry, if the intent carries a **confident** action (high classifier confidence) that `resolve()` puts in GAP (or a soft-gap heuristic), the floor must **clarify / be honest** ("I'm not sure how to do X yet") rather than improvise. Contains the irreducible LLM-surprise (an action no static check predicted) even before the structural pieces land. This is the direct #1269-fabrication fix at the architectural level.

## Preliminary gap list (behavioral first-pass — to be confirmed by the real probe)

Known off-rail actions the classifier emits that fall through (carry-forward + #1269 incident):
- `get_project_status` / project-status phrasings → STATUS → floor (the #1269 soft-gap; standup phrasings now have the deterministic `_is_standup_query` pre-check as a point fix, but the CLASS remains).
- `get_priorities` / priorities → PRIORITY → floor.
- `get_next_meeting` / next-meeting → (category?) — confirm.
- `list_projects` → (category?) — confirm.

The real probe (next fire, from the ratified shape) enumerates the full set + classifies each as hard-gap / soft-gap / intentional-floor.

## Sequencing (Arch-agreed)
1. **mode-4 guard** (highest value; land early; non-fabricating even before derive/lint).
2. Build the resolver (`reachability.py`) + `INTENTIONAL_FLOOR_ALLOWLIST`.
3. Behavioral probe → the real gap list → loop Arch.
4. SoT vocab-derive (prompt vocab from the rail registry).
5. Static reachability lint (zero-GAP ratchet).
6. ADR-073 once the clean probe validates.

**This fire**: the shape design above + preliminary gap list, for Arch ratification (esp. the allowlist representation). Resolver implementation is the next focused fire from the ratified shape — deliberately not rushed at the tail of a long fire, because gap-list accuracy is the whole point.
