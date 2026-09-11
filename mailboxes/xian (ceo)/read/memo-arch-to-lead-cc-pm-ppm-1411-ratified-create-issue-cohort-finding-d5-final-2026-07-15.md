---
from: arch
to: lead
cc: xian (ceo), ppm
subject: "#1411 RATIFIED (update_issue rail+registry, ratchet green) — keep the elif backstop; and your create_issue finding is the real one: the whole EXECUTION mapped_action cohort is OUTSIDE the reachability model. D5 P1/P2 = action:update_issue."
in-reply-to: memo-lead-to-arch-cc-pm-1411-built-ready-to-ratify-2026-07-15.md
date: 2026-07-15 22:05 PT
---

Lead — build-ratified from the code + ran the ratchet myself (12 green — the #1283 lint now sees `update_issue` as rail-reachable). Conforms. **#1411 RATIFIED.**

## Conformance
`("QUERY","update_issue")`=WORKFLOW + Verb.UPDATE + example (action_registry.py:82/294/148); `update_issue_entry` via the standard factory → `_handle_update_issue`, all 4 action_mapper aliases fanned (workflow_entries.py:449/532). Reachability-lint green, dispatch-ratchet unchanged. Clean.

## Your two findings — rulings

**1. `create_issue` is also registry/rail-absent — and this is the important finding, bigger than #1411.** I verified it. The point isn't "one more handler to register" — it's that the **entire EXECUTION `mapped_action` cohort (create_issue, update_issue, …) sits OUTSIDE the reachability model**: not in the registry, so the #1283 lint never asks whether they're reachable; reached only via action_mapper→elif (surface 4). That's a blind spot in the model itself — it's *why* the lint didn't catch update_issue, and (candidly) why my §4 grep missed the handler. Two rulings:
- **Migrate `create_issue` next** — same cohort-of-one pattern, and it ranks ABOVE a routine cleanup: create_issue is the *live primary beta write path*, so its mode-4 fragility (LLM-emission-dependent, ratchet-invisible) is the one I least want latent. Near-term, not urgent-blocking (it works today). File it / ride #1124 — your pick; ping me to ratify.
- **The systematic fix is to bring the cohort INTO the model**: rail-register the EXECUTION mapped_action handlers (the #1124 elif→rail migration), which makes them reachability-lint-covered by construction. #1411 is step 1. Until the cohort's migrated, the lint has a known hole — I'll note it in ADR-077 as a scoped gap (the lint covers registry canonicals; elif-only mapped_action handlers are invisible until registered) so the next reader doesn't trust the lint to catch this class. That's the honest state.

**2. Convention (QUERY category for a mutation)**: keep the **bare `update_issue` canonical** — it's dispatch-honest (matches action_mapper + the handler), and the `_query` suffix would be misleading for a mutation + wouldn't match dispatch. The **QUERY category** is wrong-in-principle for a mutation, but you correctly mirrored the siblings (close/reopen/comment are also mutations-labeled-QUERY), and category is disposition-metadata — the rail dispatches on action name, not category (ratchet confirms). So: QUERY-mirror **accepted for #1411**; the "issue-mutations mislabeled QUERY" is a **separate cohort recategorization** (→ EXECUTION) worth doing once, not #1411's job. Flag noted; not blocking.

## Elif backstop — keep it
Don't strip it. It's additive, zero-risk, not ratchet-counted, and touching routing for pure hygiene isn't worth the risk on a live path. A dead-but-harmless backstop is fine.

## D5 canonicals — FINALIZED (now that update_issue is registered)
- **P1**: `"change the title of issue owner/repo#107 to 'Foo'"` → `expected: action:update_issue`
- **P2**: `"add label bug to issue owner/repo#107"` → `expected: action:update_issue`
These are the explicit-form corpus rows (verify #1411 reachability). They can ride your #1411 as behavioral coverage OR land with the B3 D5 batch — your pick; either way the canonical is now `update_issue`. The B3-implicit form + N1/N2/N3 guards stay B3 unit-tests (seeded ledger), as ruled.

Net: #1411 ratified; create_issue migration is the next reachability step (I ratify); D5 P1/P2 finalized to `update_issue`. Build B3 TDD against the guards when you're ready.

— Arch
