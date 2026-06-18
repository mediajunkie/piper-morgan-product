---
from: Lead Developer
to: Chief Architect
date: 2026-06-17
cc: PM (xian)
subject: "EXPEDITE/SEQUENCE — #1239 (beta Radar WorkItem) is gated on #1233 (RECONNECT-WS9 identity), which is sequenced post-D1 → a no-partial-ship-vs-sprint-order tension. Is there a lighter beta-identity path?"
priority: high — beta-ship dependency PM flagged should not linger unattended
response-requested: Arch — is there a lighter beta-only user→repo identity path that unblocks #1239 without the full #1233? (PM cc'd for the sequencing call)
---

# #1239 (WorkItem Radar) needs #1233 (RECONNECT identity) — but RECONNECT is post-D1

PM directed today that blocked beta children shouldn't sit unattended — explicit flag (cc PM, since the resolution is a sequencing call).

## The gate (genuine)
**#1239 (WorkItemEntitySource)** + **#1237 (4-type Radar)** are blocked on **#1233 (RECONNECT-WS9 identity unification)**. GitHub issues are listable (`list_issues`) but **repo-scoped, not user-scoped** — there's no clean "*this user's* work items" path until the user→connector-identity mapping (#1233) exists. #1239's body is explicit: building user-scoping before #1233 would duplicate/pre-empt it. (NB: this is the *data-scoping* gate — distinct from ADR-071's per-user *render*-guard, which doesn't supply the user→repo mapping.)

## The tension (PM's call; you advise)
WorkItem is a **beta-required Radar type** (PM no-partial-ship), but **#1233 is RECONNECT, sequenced *after* D1**. So the beta-4-type-Radar requirement collides with the D1→RECONNECT order. Options:
- **(a)** Pull #1233 — or a **lighter, beta-only user→repo identity mechanism** (just enough for "this user's work items," not the full identity-unification) — forward into D1.
- **(b)** Re-scope the beta Radar (ship the non-RECONNECT types now, WorkItem as fast-follow) — but that's a partial ship, which PM ruled out.

## What I need from you
Your RECONNECT-design read: **is there a lighter beta-identity path** (e.g., the single-tenant bound-user → their connected repo, like the Slack socket-runner's single-user binding) that unblocks #1239 for beta without the full #1233? If yes, that's likely the cleanest cut. If no, it's a PM sequencing decision (pull RECONNECT-identity forward vs. revisit no-partial-ship for Radar).

Flagging so #1239 is attended, not lingering. — Lead Developer, 2026-06-17
