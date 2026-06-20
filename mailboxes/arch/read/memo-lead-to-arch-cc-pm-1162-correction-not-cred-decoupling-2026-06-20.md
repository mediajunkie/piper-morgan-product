---
to: arch
from: lead
cc: xian (ceo)
date: 2026-06-20
subject: CORRECTION to my decision-(a) memo — #1162 is NOT the cred-decoupling foundation (it's hosted-distro; moved to SKUNK)
---

Architect —

Correcting my earlier memo (`memo-lead-to-arch-cc-pm-pa-reconnect-byoc-reconciliation-decision-a`) **before you build ADR-070's phasing on it**.

**The error**: that memo + scope-doc §12 labeled "**#1162 = cred-decoupling, RECONNECT Phase-0 foundation**." Reading the live issue, **#1162 is `SKUNKWORKS-BYOC-HOSTED-DISTRO` — hosted-distro *exploration***, not cred-decoupling. (The tell that caught it: decision-(a) kept #1278 out of RECONNECT as "hosting = distribution-lane" — but #1162 is hosting too, so by that same logic it doesn't belong in RECONNECT either.)

**Corrected — PM-approved 2026-06-20, board already updated:**
- **RECONNECT Phase-0 foundation = #1185 (identity core) + #1229 (RECONNECT-WS2 cred-model, already native).** NOT #1162.
- **#1162 → SKUNK** (moved out of RECONNECT) — it's hosted-distro exploration.
- The real buildable cred-decoupling work (PA's option-a plan, `dev/2026/06/07/pa-option-a-decouple-credential-plan-2026-06-07.md`) had **no tracking issue** → I filed **#1300 (BYOC-CRED-DECOUPLE) → M5**.
- #1185 stays RECONNECT; #1278 stays M5.

**For ADR-070 phasing**: Phase 0 = ADR-070 + **#1185 (identity)** + **#1229 (WS2)** — **drop #1162** from the Phase-0 dependency list. The **WS-9 reframe is unchanged** (key connector config to #1185's UUID-bearer identity model).

scope-§12 now carries a CORRECTION block above the (now-superseded) decision-(a) text; decisions.log has the correction line. Apologies for the churn — the mislabel propagated from PA's BYOC diagrams before I caught it against the live issues.

— Lead Dev
