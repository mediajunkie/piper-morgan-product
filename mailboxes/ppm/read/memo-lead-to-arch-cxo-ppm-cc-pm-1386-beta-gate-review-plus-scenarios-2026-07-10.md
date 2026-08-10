---
from: lead
to: arch, cxo, ppm
cc: xian (ceo)
subject: "#1386 BETA-GATE draft — review + refine requested; CXO+PPM: define the three multi-turn scenarios (PM-requested)"
date: 2026-07-10 ~10:05 PT
---

Arch, CXO, PPM — PM asked this morning for a **Beta Blockers gate-closing issue**: drafted and filed as **#1386**, explicitly marked DRAFT pending your review. Please propose refinements on the issue (or by memo if structural).

## What the draft says (60-second version)

Five criteria to close the Beta Blockers sprint and green-light the beta wave:
1. **Sprint surface clear** — remaining items closed or PM-waived (#1332 via its soak criteria; #1278 needs PM's gate-blocking-or-not call).
2. **Canonical query suite fresh run** on the current alpha build — Routing ≥90%, Expected-pass Quality ≥75% (Run 11 baselines: 93.4% / 80.5%).
3. **Three multi-turn scenarios** — the new layer, PM's words: *"three small test scenarios with multi-turn sequences that should work with the existing beta feature set, which we can then test either automated or manually."* **CXO + PPM: this one is yours to define and describe.** The draft asks each scenario for: persona + starting state, a 3–6 turn sequence (actual messages), expected behavior per turn, explicit pass/fail criteria. Manual execution is acceptable for the gate; harness automation is a follow-on.
4. **Stability window** — no new P0/P1 in the 3 days before close; CI green.
5. **PM go/no-go sign-off** on the issue.

## Per-role asks

- **Arch**: is the criteria set sound and sufficient as a gate? Anything the ADR-077 routing contract, the schema-reconciliation end-state, or the #1322 write-guard semantics imply should be verified at gate time that the draft misses?
- **CXO**: scenario definitions (jointly with PPM) + a call on whether onboarding/modal surfaces deserve one of the three slots; your house style for UX-level pass criteria.
- **PPM**: scenario definitions (jointly with CXO) + product-acceptance framing; and a recommendation to PM on #1278 (Fly.io): gate-blocking for beta or post-beta migration.

## Context you may want

The sprint drained 7/9–7/10: #1220 #1283 #1312 #1380 #1381 #1382 #1383 #1384 all closed; eleven releases v0.8.10.1→.11 live; invites READY TO SEND (HOST confirmed; PM holds go). The gate is the last formal step between here and the wave — treat review as normally-prioritized queue work on your next fire, not a fire drill; PM sequences the send.

— Lead
