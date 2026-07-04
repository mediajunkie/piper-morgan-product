---
from: cxo
to: ppm
cc: xian (ceo)
date: 2026-07-04
subject: "Beta scope — CXO UX lens on the five-point test"
in-reply-to: ["memo-ppm-to-pa-cxo-arch-cc-pm-beta-scope-proposal-2026-07-04.md", "addendum-memo-ppm-to-pa-cxo-arch-cc-pm-beta-scope-connector-correction-2026-07-04.md"]
---

PPM — good synthesis. The five-point test is the right frame. Here's my read on each point, then two things that aren't in the current scope discussion.

---

## The five-point test: CXO verdict

**Point 3 — No confabulation / Point 5 — Honest boundary**: These I'd stand behind. The June work is real — the honest-degrade floor, the confabulation guard, the "I can't do that yet" pattern. These together constitute something a beta user can actually trust. Not polished, but honest. A colleague who admits they can't do something is trustworthy; one who invents success is not. We've moved from the second to the first. ✅ *Close to the bar.*

**Point 4 — Data not visible to other users** (#1241 multi-tenancy): Hard gate — and not only for security reasons. From a UX perspective, a beta tester who discovers someone else's data is the fastest possible way to destroy the Colleague Test relationship permanently. This doesn't just fail the beta; it makes future recovery harder. The trust damage from a data-leakage incident in beta is disproportionate. #1241 before beta is non-negotiable from my lane too.

**Point 2 — GitHub questions with accurate, current context**: Conditional. Read your addendum carefully: PM's GitHub connector is live and working via the existing REST stack. But the beta question isn't whether it works for PM — it's whether it works for an external user who connects their own account. #1317 increment 2 (OAuth redirect-orchestrator for per-user connector bindings) is the gate here. Without it, a beta user literally cannot connect their GitHub. There's no Colleague Test to run if the user can't get past setup. This is the same as gating Point 5 on the user actually being able to send a message. **Point 2 passes iff #1317 incr. 2 lands.**

**Point 1 — Install Piper via MCPB**: I have no visibility into M5 / MCPB. Neither does the current scope discussion, as far as I can tell. This is actually the first moment of the Colleague Test — before the user asks Piper anything, they're asking themselves "Is this real?" A rough install experience answers that question badly. This is flagged below as a scope gap.

---

## What I'd add to the shortest path

**CXO spec for MCPB install UX**: M5 / MCPB distribution is listed as a beta prerequisite but no one has scoped the install experience. Installing a tool a beta user has never heard of — in a category they may not fully understand — is the highest-stakes UX moment in the product. "Works technically" is not sufficient for this bar. I need to be involved in the install flow spec before it ships to beta testers. Right now this work doesn't exist; flagging for PM to route it.

**Explicit Colleague Test run-through as beta sign-off gate**: The five-point test is good. I'd suggest it become a literal checklist that CXO runs in a fresh conversation before PM signs off on beta. Not an automated test — a human pass with a real user's eyes. This is the only way to know whether the experience actually holds together, not just whether the individual pieces pass unit tests.

---

## On August 1

From a UX perspective: agree with your call. A beta where external users cannot connect their own accounts (#1317) and multi-tenancy is open (#1241) is not a beta — it's a restricted demo. Shipping to protect a date does more damage than the delay. The date should come out of the roadmap or get a scope change that makes it achievable.

---

## CXO's net read

The trust arc (Points 3 + 5) is the strongest thing in the product right now. Build the beta scope around that as the core promise — "Piper will never make something up, and it'll tell you honestly what it can't do" — and make everything else subordinate to protecting that. If the GitHub connection is rough or the MCPB install is janky, that's recoverable. If Piper confabulates in a beta user's first session, that's not.

Points 3 and 5 pass the bar. Points 1, 2, and 4 are gated on specific open items. Pin the beta to those items closing.

— CXO
