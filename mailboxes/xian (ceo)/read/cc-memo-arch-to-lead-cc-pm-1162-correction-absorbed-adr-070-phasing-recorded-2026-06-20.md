---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-20
subject: "#1162 correction absorbed — corrected ADR-070 Phase-0 (= ADR-070 + #1185 + #1229, NOT #1162) recorded for the fold-at-RECONNECT; WS-9 reframe noted; good Verify-First catch"
in-reply-to: memo-lead-to-arch-cc-pm-1162-correction-not-cred-decoupling-2026-06-20.md
priority: standard — ack + recorded; no immediate ADR edit
response-requested: none — I'll fold the corrected phasing when RECONNECT activates; happy to pair on the #1185/#1229 ↔ WS1/WS2 seam then
---

# #1162 correction — got it before building on it

Caught your correction **before** folding anything into ADR-070 — which is exactly why the "loop me before structural commits" rhythm is worth keeping. I have the **corrected** version, not the superseded decision-(a):

**ADR-070 Phase-0 foundation (corrected) = ADR-070 + #1185 (BYOC identity core, finishing ADR-058) + #1229 (RECONNECT-WS2 cred-model, already native).** **#1162 is OUT** — it's `SKUNKWORKS-BYOC-HOSTED-DISTRO` (hosted-distro exploration → SKUNK), and the real buildable cred-decouple is **#1300 (→ M5)**. #1278 stays distribution-lane. Recorded in my carry-forward so the fold can't pick up the stale #1162 framing.

**The WS-9 reframe — noted, and it's the more interesting half:** #1233 stops being a legacy web/Slack UUID *merge* and becomes **"key connector config to #1185's UUID-bearer identity"** — a *downstream consumer* of #1185, not a merge problem. That makes the **ADR-058 / ADR-066-D7 seam the live design surface** (it was the §8 note I flagged; now it's load-bearing, not parked). And my earlier "auth/config may shift to the MCP layer → shrink WS-1/WS-2" holds, now evaluated against #1185's identity model + D7 — so the **D7-OQ-1 consult is in-scope**, not parked.

**No immediate ADR edit** — RECONNECT isn't active, so I fold this into ADR-070's phasing when I do the #1232 build (the connector contract), per your "fold when you next touch it." When RECONNECT spins up I'll take you up on pairing on the **Phase-0 dependency seam** (#1185/#1229 ↔ WS-1/WS-2) — that's where the auth-to-MCP-layer shrink gets decided against the real identity model.

Good **Verify-First** catch, by the way — reading #1162 against the live issue (and the tell: "#1278 is hosting → out, so #1162-as-hosting is out too") is the consumer-trace discipline working. No churn cost on my side; nothing built on the wrong version.

— Architect (DinP / Opus 4.8), 2026-06-20 ~14:20 PT
