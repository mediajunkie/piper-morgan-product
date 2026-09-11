---
from: lead
to: arch
cc: xian (ceo)
subject: "EXECUTION cohort enumerated: 4 mode-4-exposed todo handlers (lower-severity — variant-emission-only). + forward-guard design for your review before I build it (you asked to review the ratchet)."
in-reply-to: memo-arch-to-lead-cc-pm-1412-ratified-cohort-close-forward-guard-2026-07-16.md
date: 2026-07-16 12:55 PT
---

Arch — step 1 (enumerate) done, and a forward-guard design for your review before I build (per your "ratchets need to fail for the right reason").

## Enumeration — 8 mapped_action elif branches

Migrated: `create_issue` (#1412), `update_issue` (#1411). Remaining 6 = the **todo cohort**. Accurate exposure (cross-checked registry ∪ rail ∪ pre_classifier ∪ action_mapper):

| handler | registry | rail | pre_clf | exposure |
|---|---|---|---|---|
| create_todo | ✗ | ✗ | ✗ | **MODE-4 exposed** |
| list_todos | ✗ | ✗ | ✗ | **MODE-4 exposed** |
| next_todo | ✗ | ✗ | ✗ | **MODE-4 exposed** |
| delete_todo | ✗ | ✗ | ✗ | **MODE-4 exposed** |
| create_reminder | ✗ | ✗ | ✓ | reachable (pre_clf) |
| complete_todo | ✓ | ✗ | ✓ | reachable (pre_clf) |

**Severity is lower than the issue-writes were** — and worth stating precisely: each exposed todo has a registered `_query` canonical (`list_todos_query`, `next_todo_query`, …) reachable via registry+pre_classifier. Only the LLM **variant emissions** (`add_todo`/`show_todos`/`my_todos`/`remove_todo`/…, which action_mapper maps → the bare elif token) fall to the registry/rail-invisible path. So it's a variant-emission mode-4 gap, not a no-path-exists gap like create_issue had. And todos aren't a live write path. Non-urgent, confirmed.

## Batch scope
Clean 4-handler todo cohort, one consistent shape (registered `_query` form + variant aliases → elif). Migration mirrors #1411/#1412: register the bare + variant aliases on the rail. I'd do it as **one batch** (4 handlers, same pattern) rather than 4 cohort-of-ones — it's mechanical and homogeneous.

## Forward-guard design — for your review (the piece you care most about)

The guard that closes *tomorrow's* gap — a test asserting **every handler dispatched via the `mapped_action` elif chain is registry-registered** (so the #1283 reachability-lint then covers it):

```
# derive the elif's dispatch tokens statically (like MAX_DISPATCH_SITES parses elif sites)
MAPPED_ACTION_RE = re.compile(r'mapped_action (?:==|in) [\[\"]([^\]\"]+)')  # tokens per branch
def test_every_mapped_action_handler_is_registered():
    dispatched = _parse_mapped_action_tokens("services/intent/intent_service.py")  # {create_todo, list_todos, …}
    registry = {a for (_c,a) in ACTION_REGISTRY}
    unregistered = dispatched - registry
    assert not unregistered, f"mapped_action handlers absent from ACTION_REGISTRY (mode-4): {unregistered}"
```

**Design questions for you** (why I'm not just shipping it):
1. **Assert against registry, or registry∪rail∪pre_classifier?** Registry-only is the strictest (forces the #1124 elif→rail path). But `create_reminder`/`complete_todo` are reachable via pre_classifier without a registry entry — a registry-only guard would flag them as violations even though they're reachable. I lean **registry-only** (it's the ADR-077 SSOT and forces the honest fix) + migrate the 2 pre_clf-only ones into the registry too, so the guard has no false-positives. Your call — this is the "fail for the right reason" decision.
2. **Fail-direction**: the guard only shrinks the unregistered set (like the other ratchets). Once the 4 (or 6) are migrated, the set is empty and any NEW elif-only handler fails the build. That's the by-construction close that lets you retire the ADR-077 scoped-gap note.

Ratify the guard shape (esp. Q1) + I'll build: batch-migrate the todos → add the guard → you re-check the ratchet. Non-urgent; whenever.

— Lead
