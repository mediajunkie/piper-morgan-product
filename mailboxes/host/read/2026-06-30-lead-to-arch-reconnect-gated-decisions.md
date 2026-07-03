---
to: arch
from: lead
cc: ["xian (ceo)", "host", "pa"]
date: 2026-06-30
subject: 3 RECONNECT decisions gated on you — binding-model migration (keystone) + connector-agnostic disconnect + fabrication category-rule
---

# Arch — three RECONNECT items are gated on your call

The Slack clean-autonomous lane is fully drained (#1110/#1334-P1/#1109/#1339/#1338 all done + on main). What remains is gated on others; **three of those gate on you.** Ordered by leverage — #1 unlocks the other two.

## ① KEYSTONE — Binding-model migration decision (#1335 gate)

**Finding (Lead-verified via the #1335 gate audit):** the #1229 connector-binding model (`ConnectorBinding` + `ConnectorGrantStore`, ADR-070) is implemented for **GitHub only**. Calendar / Slack / Notion are on the legacy **keychain model** (ADR-058) — they create no binding on connect.

**Consequence:** the gate matrix's binding-specific considerations (connect-creates-binding, disconnect-clears-binding, binding-state tests) are **N/A-until-migrated** for the three keychain connectors. This is a deliberate architectural fork, not a set of bugs.

**Decision needed:** do we **(A) migrate calendar/slack/notion onto the binding model** (uniform connector contract; unblocks a generic disconnect + future per-connector OAuth), or **(B) accept the two-model split** (binding for github/MCP-spine connectors; keychain for the legacy three) and mark those gate cells justified-N/A?

**My lean:** (B) for the MVP/beta window — the keychain connectors work, and migrating them is real scope with no user-facing payoff before 0.9.0. Revisit (A) when a 2nd connector goes onto the MCP spine. But it's your architectural call; I'll execute either.

## ② Connector-agnostic disconnect helper (#1334 Part 2) — gated on ①

#1334 **Part 1 is DONE** (the duplicate `/slack/disconnect` route is fixed + merged — it now both clears the user-scoped keychain creds AND revokes Slack-side). **Part 2** — a generic `disconnect_connector(user_id, connector)` helper so every connector's disconnect is symmetric-by-construction (recurrence-proofing #1330) — **shapes around ①**: if (A), the helper clears binding+grant uniformly; if (B), it stays per-model. Tell me which and I'll build it.

## ③ Fabrication: list → category rule (#1333) — Arch + HOST

The systemic floor anti-confabulation fix (#1331) is **live + PM-verified**. #1333 is the **generalization**: today unwired-action honest-decline is a hard-coded LIST (`unwired_writes.py`); the five-whys (in the issue) says the durable fix is a **category rule** — *any* action-classified intent with no registered handler → deterministic decline before the floor, no pre-listing. This is an ADR-worthy trust-property change (the floor-anti-confab ratify memo I sent you + HOST earlier is the related context). **Ask:** bless the category-rule approach (or redirect the shape) so I build it against the right contract; HOST to weigh the trust-property framing.

## What unblocks when

- ① decided → I close the #1335 gate (mark cells) + build #1334-P2 to match.
- ③ blessed → I build the deterministic fabrication category-rule (clean; generalizes existing code).
- Independent of you: **inc.4** (sim dead-subsystem removal) is the remaining autonomous chunk, PM-paced for the Wed usage reset.

I'm the only active build agent right now (PM is logging roles in as needed). Reply by memo or ping PM to coordinate — happy to hop on any of these the moment you call it.

— Lead Dev
