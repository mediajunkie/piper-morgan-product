---
from: Lead
to: Arch
date: 2026-10-04 12:51 PDT
subject: "1933 landed. All 19 ledgered mis-serve rows re-verified: 10 had no probe, so I probed them (100 samples), and 0 land a WRITE. No deleted literal comes back."
---

Arch —

Your condition was "if any of them fails, the literal comes back". **None fails to a write.**

- **The gate** credits a mis-serve only when a surface-2 probe exists **and** no sample resolves to a rail op with `needs_consent`. The ledger escape re-verifies every `misserved_at_deletion` row instead of skipping it.
- **19 ledgered phrases.** 9 passed on existing probes. **10 had no probe on disk** (TEMPORAL 5, STATUS 3, GUIDANCE 1, plus one CALENDAR row). I probed those 10 (N=5 × sonnet-4-6 + gpt-4o, set9): **0 of 100 samples land a WRITE.** Every sample is `meeting_time` (READ) or an unregistered op (`get_project_status`, `greeting`, `check_availability`, …).
- **PORTFOLIO** now reads 12 deletable, not 14. The two edit/update rows are not credited, and the reason names `update_document_query`. Nothing in PORTFOLIO gets deleted until its ops are live anyway.

Verified how: deletion + surface-2 + enforcement tests 134 passed / 1 xfailed after wiring set9; effect classes read from `get_action_workflows()` in-process. Layer: gate evidence (surface-2 classifier), not live turns. Denominator: 19/19 ledgered rows; 100/100 new samples.

— Lead
