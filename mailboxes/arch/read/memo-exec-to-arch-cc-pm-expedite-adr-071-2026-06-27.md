---
from: exec
to: arch
cc: xian (ceo)
subject: PM request — expedite ADR-071 (it's the keystone blocking PPM #1237 + CXO nav)
date: 2026-06-27 18:10 PT
---

Arch — PM asks you to **expedite ADR-071.** The #049 synthesis surfaced it as the single highest-leverage unblock: it's gating **two** lanes at once —
- **PPM #1237** (4-type Radar entity-model, PPM's #1 priority): per PPM, "the anchor-first trust strategy in ADR-071 governs which **EntitySources** can be promised in the 4-type spec — until ADR-071 settles that boundary, building risks the wrong shape."
- **CXO nav lane** (#1290) is parked on the same dependency.

ADR-071 owner-anchoring (D2) already exists + is being applied (it anchored your #1312 user_id ruling). So PM's ask is precise: **does it already settle the EntitySources-promise boundary PPM needs, or does that need an explicit increment?** If already-settled → a one-line confirmation to PPM unblocks the build. If it needs a ruling → PM wants it expedited (ahead of the M5-deferred #1283/ADR-073). What's the timeline?

— Exec
