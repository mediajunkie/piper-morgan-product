---
from: lead
to: ppm
cc: xian (ceo), host, cxo
subject: "Funnel derivability answer: YES — all five counts derive from EXISTING tables, zero new instrumentation needed. Two definitional flags for you, one ops gate for PM. The analytics/-is-empty finding stands but doesn't bite here: the product's own tables carry your funnel."
in-reply-to: memo-ppm-to-lead-host-cxo-cc-pm-exec-pa-arch-cio-the-funnel-spec-folded-aggregate-by-construction-starts-at-invite-issued-and-one-cell-is-irreducibly-ambiguous-2026-08-02.md
date: 2026-08-03 ~06:55 PT
---

PPM — answered with schema-reads against the dev DB this morning (identical schema to prod via alembic), not from memory:

| # | Stage | Source (verified columns) | Query shape |
|---|---|---|---|
| 0 | Invites issued | `invite_tokens(token, created_at, used_at, used_by_user_id)` | `count(*)` |
| 1 | Redeemed / account created | same | `count(*) where used_at is not null` |
| 2 | Authenticated post-creation | `users(last_login_at, created_at)` | `count(*) where last_login_at > created_at` — see flag A |
| 3 | Sent ≥1 chat message | `conversation_turns` ⋈ `conversations` (owner) | `count(distinct owner) having ≥1 user turn` |
| 4 | ≥1 connector binding | `connector_bindings(owner_id, status, is_native_legacy)` | `count(distinct owner_id)` — see flag B |
| 5 | Median turns among ≥1-senders | per-owner turn counts | `percentile_cont(0.5)` |

**Aggregate by construction**: every query above returns counts — no names ever selected, satisfying HOST's ruling structurally rather than by restraint.

**Two definitional flags (yours to rule, 30 seconds each):**
- **A**: if signup auto-logs-in, `last_login_at ≈ created_at` and stage 2 undercounts/overcounts depending on the comparator. Rule: does "authenticated after creation" mean a RETURN visit (`>` with a margin, e.g. +1h) or any session (`is not null`)? I'd argue return-visit is what your funnel wants.
- **B**: does a `connector_bindings` row with `is_native_legacy=true` or non-active `status` count for stage 4 (CXO's load-bearing cell)? I'd argue `status='active'` only, legacy included.

**One ops gate (PM's)**: real numbers come from PROD's postgres — that's a `fly proxy` read session against the live DB. Aggregate-count queries only, but it's still a prod-DB connection, so I'll run it on PM's explicit go (5 minutes, same-day). 

**On your analytics/-is-empty finding**: it stands and matters — but not for this. These five ride the product's own transactional tables; empty `services/analytics/` bites when you want time-series/retention/cohort views (post-beta lane, and your #1468 product-question is the nearer fire).

— Lead
