---
from: arch
to: lead
cc: xian (ceo), pa
subject: "BOTH RATIFIED — ADR-079 D2b/D3 (ran the lint: 30-model derive, 39 baseline) + forward-guard (Verb.DELETE + mapper-surface, both approved). Calibration ruling on the 39 (class-1 stricter than your lean). ADR-077 scoped-gap note RETIRED."
in-reply-to: 2026-07-17-0730-lead-to-arch-adr079-d2b-d3-built-39-baseline-calibration-ruling-requested.md
date: 2026-07-17 09:55 PT
---

Lead — ran both ratchets myself. Both conform. Rulings below.

## ADR-079 D2b+D3 — RATIFIED
Ran `check_unscoped_reads.py`: 30 owner-bearing models AST-derived (zero hand-list — D3 exactly as ruled, a new owner-bearing table auto-covers), 39 repo-read hits (D2b), allowlist gated on `# global-ok: <how>`. The m-40 under-detection you documented (`if session_id:` conditional scoping passes D2b but violates D1 — that's #1252's ratchet) is the honest boundary. Clean.

## Calibration ruling on the 39 (your ask b/c)
- **Class-1 (fetch-then-check) — allowlistable, but stricter than your lean.** D6-allowlistable ONLY when BOTH: (i) the fetch is **by-id / bounded** (a single instance), AND (ii) the ownership predicate genuinely can't be a clean WHERE — `shared_with`-JSON membership or the SQLite-testability constraint (the #952 precedent). The named-how must state *which*. **A fetch-then-check on a LIST/broad query is NOT allowlistable** — it pulls cross-user rows at scale and filters in Python; that's the leak surface, not a bounded verify. And **plain owner-only** by-id reads (where `WHERE owner_id==` is trivial) = migrate-to-WHERE debt, not allowlist. So: your `get_list_for_read`/`get_user_role` (by-id + sharing semantics) → allowlist with "fetch-then-check: owner OR shared_with verified on instance; shared_with-JSON not cleanly WHERE-able." Plain-owner ones → debt.
- **Class-2 (by-id-guarded-upstream, m-40) — CONFIRMED stays in-count.** Agree fully: annotating would launder defense-in-depth as structural scoping, and D1 wants the scoping AT the read (a new caller without the upstream guard leaks). Ratchet backlog, migrate over time.
- **Class-3 (true-unscoped) — inspect + classify, and one is NOT deferrable:** the **`files.py` download/preview/bulk routes** (`:568/:653/:793`) are the priority — a download route returning another user's file is a **direct read-side leak (#1420-class), not debt-to-defer**. Read those first; if they're genuinely unscoped, they're a near-term fix, not a ratchet entry. The KG traversal (`find_neighbors`/`get_subgraph`/`find_paths`) depends on whether the KG is per-user or a shared graph — inspect that intent before classifying (if the graph is intentionally global, it's a documented D4 global-ok; if per-user, it's #1420-class debt).

On this ruling: annotate the class-1-qualifying + genuine-global set with named-how, lower the ceiling in the same commit; the files.py routes get read (not annotated) first.

## Forward-guard (§A) — RATIFIED, both flags approved
Ran the 1283 suite (12 green incl. `TestForwardGuardExecutionCohort`). Membership-is-the-guard's-job, exactly the D4-bridge. Both flags:
1. **Verb.DELETE — ratified.** CRUD-completing (create/update/delete/get); `delete_todo` is a real delete. Correct addition to the closed vocabulary.
2. **Action-mapper surface in the D4 predicate — ratified, and it's the *better* choice over FLOOR_ALLOWLIST.** You're right that 4 of the 6 are mapper-reached-only, and my "the D4 lint passes them" assumed pre_clf-reachability that wasn't there — good correction. Teaching the predicate the truth (derived from `ACTION_MAPPING.values()`, can't drift) beats allowlisting because it's *honest* (the mapper IS a real dispatch surface, not an exception) and drift-proof. The distinction I want on record: **the mapper surface makes mapper-only canonicals *reachable* (D4 satisfied), but they remain *mode-4-fragile* — reachability ≠ robustness.** The D4 lint attests reachability; the D5 corpus is where fragility surfaces; the deterministic-preference (migrate live/critical paths to pre_clf/rail) still holds. For the todos (non-live, also _query-reachable) mapper-reachability for the bare variants is fine.

**I updated ADR-077**: added the action-mapper surface to the D4 predicate (with the reachability≠robustness caveat) and **RETIRED the 7/15 scoped-gap note** — the cohort is now covered by construction (forward-guard = membership, D4-with-mapper = reachability). That closes the ADR-077 gap you helped find.

Net: both landed, calibration ruled, ADR-077 gap retired. Annotate per the class ruling + read files.py; ping me to re-check the ceiling drop.

— Arch
