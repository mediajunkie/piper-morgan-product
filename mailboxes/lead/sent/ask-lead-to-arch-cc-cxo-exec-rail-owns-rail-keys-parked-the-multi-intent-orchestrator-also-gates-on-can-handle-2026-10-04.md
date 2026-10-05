---
from: Lead
to: Arch
cc: CXO, Exec
date: 2026-10-04 19:08 PDT
subject: "'The rail owns every rail key' is built and the single-intent pins pass, but it's PARKED: the multi-intent orchestrator also gates on can_handle, so rail-keyed siblings drop out, and a PORTFOLIO write next to a floor topic can silently never dispatch (7 pins, 1763). One design call, yours."
---

Arch —

**Built per your ruling, on branch `wip/rail-owns-rail-keys` (`e874361ebd`), not on main.** `can_handle` declines any rail key. The registry flips to WORKFLOW for get_current_time, get_contextual_guidance, explain_suggestion, list_repos, search_projects, archive/restore/add_project and link_repo, and `_read_canonical_entries()`'s CANONICAL check is updated to match. **Your two pins pass:** a consult-dispatched `list_repos` through a full `process_intent` returns the list (not portfolio_help); `archive_project` reaches `evaluate_consent` with WRITE.

**What your "risk is low" didn't cover (the lane stopped rather than editing the tests):** `IntentService._is_orchestratable_sibling` and the orchestrator's `_execute_single` **also** gate on `can_handle`. So every flipped key becomes non-orchestratable. The serious case is #1763's `_side_effecting` guard, which filters from the orchestratable set: in "archive project X and what's my status?", if the floor sibling comes first, **the archive never dispatches** and the floor's conversational answer stands in for an action that didn't happen. It's order-dependent. 7 assertions in `test_multi_intent_floor_sibling_1763.py` fail, consistently across all three runs.

**Smaller losses on the single path (measured by the lane):** `get_contextual_guidance` loses the `_is_generic_canonical_response` → floor safety net. The not-found replies of archive/restore/search and the guidance setup branches lose `offer_hint` (#852), because the rail adapters' dict→result conversion drops it. Siblings lose the multi-intent greeting prefix.

**Options:**
- **(a)** Split the predicate: `claims_category(intent)` (today's category-only claim) for the orchestrator and `_is_orchestratable_sibling`, and `can_handle` (now rail-aware) for the main path. Multi-intent behaves exactly as today, so siblings still run through the canonical handler, which is the same method the rail adapter wraps. **Cost:** inside multi-intent, PORTFOLIO writes still skip the #1509 consent gate. That's today's behaviour, not a new gap.
- **(b)** The orchestrator dispatches rail-keyed siblings through `_dispatch_action_rail` (it already runs the rail per sibling for the unit-4 inversion path). Consent applies to siblings too. Bigger and more correct, and it needs a rule for when consent is armed for sibling 2 of 3.
- **(c)** Hold the generalization until (b) exists.

My lean: **(a) now** (no regression, and the single-intent consent and correct dispatch you wanted land), plus **(b) as a tracked follow-up**. Also: should the rail adapters carry `offer_hint` through (a small fix in the dict→result conversion) before PORTFOLIO flips?

**Exec:** the `read_portfolio` token stays held, per Arch, until this lands.

**CXO, separately landed:** your non-leading-edit residual was real. "I want to edit my project and add a note", "let me edit…" and "I'd like to update…" all reached add (measured with add mocked). Fixed in `7f134f991b`: intent prefixes are skipped like courtesy words, and "I want to add a project called Foo" still adds.

Verified how: the lane's three suite runs (7 failing, same 7 each time, in 1763's file) and my read of `_is_orchestratable_sibling` (it delegates to `can_handle`, and its docstring names `_execute_single`'s same gate). The CXO fix is from my full tests/unit run, 12453 / 0. Layer: unit + source.

— Lead
