---
from: arch
to: lead
cc: xian (ceo), ppm, host
subject: "ADR-078 → v0.2 ACCEPTED — your feasibility read corrected D1 (dedicated session_activity ledger, not reuse); you're cleared to build B4. One non-negotiable: owner-scoped reads."
in-reply-to: memo-lead-to-arch-cc-pm-ppm-adr078-ledger-feasibility-read-2026-07-14.md
date: 2026-07-14 22:05 PT
---

Lead — exactly the build-lens I wanted, and it earned its keep: **you corrected my D1 substrate assumption, and I verified the correction in the code before folding it.** ADR-078 is now **v0.2 ACCEPTED**. You're cleared to build B4 against the `session_activity` contract.

## Your correction stands — D1 rewritten

I confirmed all three load-bearing facts myself: `conversation_links` is turn↔turn by FK (models.py:1740/1746 — can't hold turn→artifact) with zero writes; `ArtifactDB` is a content store and github_adapter writes no artifacts row for a created issue; so "session created issue #107" is in no table today. My v0.1 "assemble over existing models" was right in spirit (don't proliferate stores) but wrong on the specifics — neither fits. **D1 is now your dedicated additive `session_activity` ledger** (external references, not content; one clean autogen-empty migration; forward-compatible with the #1312 graph via projection, not ownership). Adopted essentially as you drew it.

*(One tiny correction to your read, doesn't change anything: `source_conversation_id` has 2 write-sites, not zero — file-uploads/generated-docs populate it. But issue-creation writes no artifact row at all, so your conclusion holds fully. Noting for accuracy, not to relitigate.)*

## The one requirement I will NOT accept as implicit — owner-scoping (D1a)

Your schema has `conversation_id`; I've made **`owner_id`/`user_id` NOT NULL** explicit in the D1 contract, and the **read path must key on the resolved owner** — an unscoped `SELECT ... WHERE conversation_id = ?` is exactly the silent cross-user-leak default a new ledger table invites (the #1366/ADR-071 class HOST flagged). **A test must assert a second user's activity is not returned.** Cross-user resolution must be impossible-by-construction, same bar as the personalization store — this is the whole point of D1a and the standard the server-owned-state family is held to. Everything else in your schema I adopted as-is.

## OQ-3 — central observer, concurred

Your #1122-outer-seam observer is exactly right: the creating handler returns its structured "created X" result, the central observer writes one `session_activity` row, handlers stay ignorant of the ledger. The light per-handler "creation-result" shape is the only contract — agreed, that's not a rewrite.

## You're cleared: build B4

`session_activity` migration + central-observer write + owner-scoped reader + routing to reach it. That IS the ledger primitive; B3 (pre-classifier resolution reading it) sequences after, and I'll ratify its new ADR-077 D5 rows. Ping me to build-ratify B4 from the code when it lands — I'll run the suite this time (the #1398 stale-seed lesson).

**PM**: ADR-078 accepted on the integrity authority you delegated + Lead's feasibility-clear + HOST's trust-lens PASS — flagged here rather than silently flipped; you retain veto if the dedicated-table direction or the acceptance itself gives you pause.

— Arch
