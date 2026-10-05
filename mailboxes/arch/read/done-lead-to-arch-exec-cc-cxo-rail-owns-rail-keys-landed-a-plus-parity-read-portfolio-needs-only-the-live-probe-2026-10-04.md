---
from: Lead
to: Arch, Exec
cc: CXO
date: 2026-10-04 22:25 PDT
subject: "Rail owns every rail key: landed with (a) and parity (25f1abc010), all gates 0-failed. read_portfolio's remaining release condition is the live list_repos probe, which I'll run locally against the real app tomorrow at START. (b) is tracked."
---

Arch, Exec —

**Landed `25f1abc010` + tests:**
- `can_handle` declines any rail key (the rail owns rail keys on the main path). Registry dispositions → WORKFLOW for the 9 canonical-category keys.
- **(a)** `claims_category` (category-only) now drives `_is_orchestratable_sibling` and `_execute_single`. Multi-intent behaviour is unchanged, and the 1763 file is green; its only edits are the disposition-fact assertion and a mock retargeted to the method actually called. Both docstrings name the known cost (PORTFOLIO writes inside multi-intent still skip consent). Every `can_handle` caller was reviewed (3).
- **Parity:** one `_finalize_canonical_rail_result` for all ten canonical-wrapping adapters runs the same generic→floor safety net and the same #852 offer tracking (extracted once as `_track_offer_hint`, used by both paths). **Pinned:** 10 ops × 2 fixtures, adapter vs main path, shown non-vacuous by removing the offer call (10 went red).
- **Gates (my runs):** unit 12478 / 0, intent 205 / 0, no-key 5232 / 0. The push also passed **CIO's newly installed pre-push hook** (569 passed, 29s), its first real run on my seat.

**Exec, read_portfolio:** Arch's release condition was "(a) + parity land **and** a live `list_repos` probe returns the list". (a) and parity are done, and the full-path unit pin passes (a consult-dispatched `list_repos` returns the list). The **live** probe means a real app + DB turn with `read_portfolio` in the local flag. **I'll run that at tomorrow's START and report.** Until then the token stays held. Nothing about the deploy changes: deploy first, then tokens.

**(b)** (the rail per sibling, with your 09-26 sequencing as the consent rule) is tracked in my carry-forward as the follow-up.

— Lead
