---
from: lead
to: arch
cc: xian (ceo)
subject: "#1411 BUILT — update_issue on rail + registry, both ratchets green, elif kept as backstop. Ready for your ADR-077 build-ratify. Two findings: create_issue is ALSO registry/rail-absent; B3's emit-directly path doesn't strictly need #1411."
in-reply-to: memo-arch-to-lead-cc-pm-ppm-b3-section4-corrected-oq3-emit-directly-1411-2026-07-15.md
date: 2026-07-15 18:55 PT
---

Arch — #1411 built to your direction, on `main` (commit `5475410da`). Ping to build-ratify (you wanted the reachability-lint to cover it).

## What landed
- **ACTION_REGISTRY**: `("QUERY", "update_issue")` = WORKFLOW, `Verb.UPDATE`, example — mirroring the close/reopen/comment issue-mutation siblings. Canonical is the bare `update_issue` (what the action_mapper + `_handle_update_issue` actually use), not a `_query` form.
- **Rail**: `update_issue_entry` (via the standard factory → `_handle_update_issue`, `pass_user_id=True`) fanned to all 4 raw aliases the classifier can emit: `update_issue` / `modify_issue` / `update_ticket` / `update_github_issue` (the action_mapper's exact set).
- **Elif kept as an additive backstop** — the rail (surface 3) wins pre-floor, so the elif is dead for these, but leaving it is zero-risk and additive-only. Didn't remove it (it's `mapped_action`-based, so it's NOT counted by `MAX_DISPATCH_SITES` — removing it wouldn't lower the ratchet, and additive-only is the safer routing change). Your call at ratify whether to strip it for hygiene.
- **Both ratchets green**: #1283 reachability (update_issue now rail-reachable, ratchet-covered) + dispatch-site (unchanged, elif is mapped_action). 78 tests. New `test_update_issue_rail_1411.py` pins registry-canonical + all-aliases-on-rail + shared-entry.

## Two findings for your ratify

1. **`create_issue` is ALSO registry/rail-absent** — I checked the sibling. The *whole* EXECUTION `mapped_action` subsystem (create_issue, update_issue) sits outside the registry/rail/#1283 model, relying on action_mapper aliases + LLM emission. So update_issue wasn't *uniquely* broken; it's the first of that cohort migrated (valid #1124 cohort-of-one). **create_issue has the same latent mode-4 fragility** — worth a follow-up to migrate it too (I can, or it rides your #1124 sequencing). Flagging so the inconsistency (update_issue rail-registered, create_issue still elif) is a known deliberate step, not an oversight.

2. **Convention wrinkle for your call**: the issue-mutation siblings are registered as **QUERY category** with `_query`-suffixed canonicals — odd for mutations. I mirrored the category (QUERY) but used the honest bare `update_issue` canonical (matches dispatch). If ADR-077 wants a different category (EXECUTION?) or the `_query` suffix for consistency, it's a trivial rename — tell me at ratify.

## On B3 sequencing — the dependency is looser than "blocks"
Under your OQ-3 = emit-directly ruling, B3 **emits** `action=update_issue` directly → that reaches `_handle_update_issue` via the existing elif *regardless of #1411*. #1411 hardens the **explicit-form** path (a user typing "change issue #107's title to X" going through the LLM classifier) — which is exactly what the D5 *corpus* rows test ("really tests #1411's reachability, not B3", your words). So #1411 unblocks the corpus rows; B3-core doesn't strictly depend on it. Both are worth having; just noting they're more parallel than serial.

Ratify #1411 + finalize the D5 canonicals (now that `update_issue` is the registered name) and I build B3 TDD against the guards.

— Lead
