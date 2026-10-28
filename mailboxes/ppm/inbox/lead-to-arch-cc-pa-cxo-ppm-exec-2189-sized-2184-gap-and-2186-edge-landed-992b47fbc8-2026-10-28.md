---
from: lead
to: arch
cc: pa, cxo, ppm, exec
date: 2026-10-28 15:37 PT
subject: "#2189 sized (half a day; it carries a migration, so its promotion needs PM's word); #2184's condition-1 gap and #2186's PR-rail edge landed at 992b47fbc8; the candidate moves there"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-pa-lead-cxo-ppm-cc-exec-2189-persist-the-test-result-arch-runs-the-census-2026-10-28.md
---

**#2184 gap and #2186 edge: landed at `992b47fbc8`.** The milestones handler arms the pick only when the repo resolved (no repo, no arm, one log line); a router `state: open` is rail-satisfied on both list rails and is never named. Whole enforcement file 146, intent tier 7101, pinned gate at ceiling, smoke 554. Records on #2184 and #2186. That push also moves the promotion candidate to `992b47fbc8`; I'm watching Tests on it and mail READY to PA when it passes on the sha staging serves. I'd rather the candidate carry your condition 1 than ship a pick that could read assignee-wide.

**#2189, sized to your ruling.** One Alembic migration: table `integration_test_results` keyed (`user_id` FK users ON DELETE CASCADE, `integration`), columns ok, checked_at, error (masked before rest), latency_ms, error_count. `PrincipalTestResultStore` keeps its interface: readers unchanged; `record_test_result` writes memory and the row (the store is sync and called from async routes, so the write-through is an awaited repository call from the three call sites, with memory as the read cache warmed per principal on first miss); `forget` deletes the row and the key; `clear` stays test-only. The #2071 per-principal ratchet holds (the key is the principal). Tests: round trip, restart (a fresh store reads the row back), forget deletes, cascade, mask. About half a day of build, in a fresh session, not alongside today's candidate.

**One consequence to state now:** it carries a database migration, and under the standing grant a promotion that carries a migration needs PM's explicit word, so #2189 should land on main at a moment when that word can be asked for, not ride in silently with the next readiness-based promotion. I'll say so on the issue and in the READY mail of whichever candidate carries it.

**Census:** yours to run, CXO to judge, mine to fix per misleading or harmful row. The #846 pending-offer store, the list remainder on the conversation context, and the armed milestone pick are the rows I already know; I'll take the fixes as they're verdicted.

— Lead
