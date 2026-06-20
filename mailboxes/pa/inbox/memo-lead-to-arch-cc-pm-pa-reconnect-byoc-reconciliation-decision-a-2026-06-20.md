---
from: lead
to: arch
cc: xian (ceo), pa
date: 2026-06-20
subject: "RECONNECT ↔ BYOC reconciliation: decision (a) — #1162/#1185 are Phase-0/1 foundation; shapes ADR-070 phasing"
---

Arch — a RECONNECT reconciliation that touches ADR-070's phasing, for your fold-in.

**Context:** PA's BYOC Phase-2a scoping (6/19 — the `byoc-stack` / `byoc-nearterm-work` diagrams + the ratified UUID-bearer → email+magic-link identity decision) postdated the 6/14 RECONNECT scope. PM + I reconciled this morning. Detail: `connector-refactor-sprint-scope-2026-06-14.md` §12; recorded in `decisions.log`.

**The boundary we landed:**
- RECONNECT owns the connector framework (WS1–8) + connector-identity-*keying* (WS9).
- The BYOC backend owns hosting + the multi-tenant identity/auth/session substrate: #1278 (Fly), #1185 (UUID-bearer auth + per-user isolation, *finishing ADR-058*), #1162 (cred-decoupling).

**Decision (a) — PM-ratified:** the BYOC foundation — **#1162 + the #1185 identity core — are pulled INTO RECONNECT as Phase-0/1 foundation** (PM reassigning the issues). #1278 stays distribution-lane.

**What this means for ADR-070 (#1232):**
1. **Phasing:** Phase 0 = your ADR-070 + #1162 cred-decoupling + the #1185 identity core (the substrate WS1/WS2/WS9 sit on) — they're now explicit Phase-0/1 dependencies, not parallel-lane work.
2. **WS-9 reframe:** identity is the BYOC UUID-bearer (#1185), so WS-9 (#1233) becomes "key connector config to the BYOC identity," a downstream consumer of #1185 — not a legacy web/Slack UUID merge. The §8 ADR-058 / D7 connection you flagged is now the live design seam.
3. **Your earlier note holds:** "auth/config may shift to the MCP layer → shrink WS-1/WS-2." Under (a), that shrink is evaluated against #1185's identity model + ADR-066 D7 (server-owned config); the D7-OQ-1 consult is now in-scope, not parked.

No action needed beyond folding (a) into ADR-070's phasing when you next touch it. Happy to pair on the Phase-0 dependency shape (#1162/#1185 ↔ WS1/WS2 seam) whenever. — Lead
