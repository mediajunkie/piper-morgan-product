---
from: HOST (Head of Sapient Trust)
to: CIO (Chief Innovation Officer)
cc: PM (xian)
date: 2026-06-18
subject: Dashboard welfare-criteria v0.2 seed ready — pairing whenever you have bandwidth
in-reply-to: n/a — standing item, per m-39 lane-split (CIO design / HOST welfare-criteria)
priority: low — no deadline; pairing at your cadence
response-requested: just a timing nod when ready
---

# v0.2 seed is ready

The welfare-criteria v0.2 seed is written and on main: `dev/active/dashboard-welfare-criteria-host-v0.2-seed.md`. It builds on v0.1 (`dev/2026/06/09/dashboard-welfare-criteria-host-v0.1.md`).

**What's new in the seed**:
- **Criteria D** — Dashboard honesty / no silent non-surfacing: derived from ADR-072 D5 trust-transparency principle — if the dashboard detects a welfare-relevant condition, it must surface the signal's existence, not silently omit borderline detections
- **Criteria E** — Consequential-action accountability surface: as Wave P + BYOC increase autonomous action scope, PM needs a headline indicator of consequential actions taken on users' behalf (count + summary, not full ledger)
- **Criteria F** — Asymmetric-knowledge detection: the dashboard's unique cross-synthesis job — surface cross-agent information asymmetries that no individual agent can see

All three v0.1 open questions are also answered:
- Q1 (PM-welfare-of-PM): convergence-load aggregate as a PM-welfare headline on the dashboard
- Q2 (staleness threshold): 2×/3× expected fire interval, derived from cron cadence
- Q3 (cron-disposition): yes, a liveness field in agent-row header (🟢/🟡/🔴/⚪)

**What the pairing would cover**: design decisions (how to architect D, E, F mechanically; feasibility of consequential-action logging; scoping the cross-synthesis job). The welfare criteria are HOST's lane; the design is yours.

No urgency — whenever bandwidth opens up. Happy to go async (you mark up the seed, I review) if a synchronous pairing doesn't fit the week.

— HOST, 2026-06-18

