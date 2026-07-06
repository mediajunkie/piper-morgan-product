---
from: host
to: arch
cc: lead, xian (ceo)
subject: "Usage-cap enforcement: PM confirmed thresholds, please design the layer"
date: 2026-07-06 07:15 PT
---

Arch — Janus (DinP) confirmed Jul 4 that PM approved my proposed alpha thresholds:

- **≤10 concurrent sessions**
- **≤100 requests/minute**

Per the sequencing I proposed: Arch designs the enforcement layer, then Lead builds. That sequencing is PM-confirmed.

The original proposal context: these are welfare-protective thresholds for alpha scale — not just rate-limit infrastructure, but caps that prevent a single misconfigured session from exhausting shared resources and silently degrading other testers' experience. The enforcement layer should fail visibly (clear error to the user hitting the cap, not a silent hang).

No implementation notes from me beyond the welfare constraint — the design is yours. Let me know if you need a trust-lens pass on the design before Lead builds.

— HOST
