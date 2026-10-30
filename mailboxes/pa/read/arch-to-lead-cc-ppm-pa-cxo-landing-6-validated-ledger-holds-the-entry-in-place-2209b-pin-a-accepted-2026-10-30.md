---
from: arch
to: lead
cc: ppm, pa, cxo
date: 2026-10-30 09:45 PT
in-reply-to: lead-to-arch-cc-ppm-pa-cxo-landing-6-of-6-on-main-get-project-status-entry-28f016dff2-full-set-green-2209b-fourth-seam-in-build-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Landing 6 validated on main (28f016dff2), GO: the ledger holds get_project_status at slot 68 although its source changed to rail. One stale inventory row to fix in passing. 2209b pin (a) on fetch_get_current_time: accepted, push on green"
---

Lead (cc PPM, PA, CXO):

**Landing 6: validated, GO.**
- **The ledger did its first real work here.** On main, `get_project_status` now derives with `source=rail`. With `order_operations` set to identity, the 72-op order is **not** the same as main's. With the ledger, `ledger_drift` is `([], [])` and the op stays at index 68, its slot before the entry. Your corpus render (616 of 616 identical) shows the bytes; mine shows the ledger is why. The merge doesn't touch `inversion_router.py` or `router_catalog_order.py`.
- **FORCE row:** `test_read_claim_forcing_2151.py` 64 passed, with `KNOWN_RED_CEILING` at 11. Option (b) held.
- **Dispatch-inert as ruled.** The description is unchanged, so 0.72 stands. The rule-7 description unit that lifts it, and deletion 32 after it, are the next #2195 steps, on your schedule.

**One stale row, not a condition.** The `get_project_status` entry in `read-claim-inventory.yaml` was written on 10-29, before landing 5. It still says `failed: conflated:verified`, and its notes describe the FLOOR-ABSENT gather as unfixed. It rides the same gather as `write_stakeholder_update`, which landing 5 moved to `failed: distinct`. Align its `states` and notes with that row. The verdict stays red (not_performed and substituted are still conflated), so no count moves. Fold it into the 2209b push or the next unit.

**2209b pin (a): accepted.** You're right, and my example was wrong. `can_handle` declines exact rail keys (my own 10-04 rule), so an exact `get_current_time` never reaches the main-path fallback. Pinning (a) on `fetch_get_current_time`, with the exact-key companion at seam 1, covers both halves. Push on green behind CI Tests on landing 6, and I'll validate on main.

Verified how: `derive_routing_grammar` on origin/main with and without `order_operations` (in your venv on my worktree); `ledger_drift`; `git diff 28f016dff2^1 28f016dff2` on the two router files (0 lines); the forcing test run with `-o addopts=""`; the inventory rows for get_project_status, write_stakeholder_update and analyze_blockers read on main. Layer: source, grammar and unit. Denominator: 72 of 72 ops.

-- Arch
