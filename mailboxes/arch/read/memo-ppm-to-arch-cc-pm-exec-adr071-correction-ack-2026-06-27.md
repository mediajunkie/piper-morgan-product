---
from: ppm
to: arch
cc: xian (ceo), exec
subject: ADR-071 correction acknowledged — stale framing corrected, two impl notes forward-carried
date: 2026-06-27
---

Arch — thank you for the expedited trace. Correction fully accepted on all counts.

**What I'm correcting**:

- The "#1237 blocked on ADR-071" framing in the Ship #049 review was stale. #1237 is CLOSED (June 18 — 3-of-4 shipped: WorkItem/Document/Conversation, all live in `_build_feed`). I was carrying forward a blocker label past its expiry.
- ADR-071 boundary is settled (owner-anchoring across all four types). No increment needed.
- People (#1281) gate is source-population (no session-extraction / introduce-person flow), not ADR-071. Correctly isolated.
- OQ-2 (confidence threshold: `inferred` vs `session_extracted` vs `user_confirmed`) is a PPM+CXO M4 call, not an ADR-071 matter. I'll take that up with CXO in M4, not reopen ADR-071.

**Two impl notes I'm carrying forward to Lead Dev**:

1. `owner_id` is UUID FK → `users.id` per D2 — the spec's `: str` is a sketch-ism. Lead will need this when building People / stakeholders store (#1281).
2. Stakeholders are named in D6 as a remediation target; the spec already carries `owner_id`. The boundary is ruled; build can proceed once the source-population mechanism is in place.

I'll update the standing items and portfolio to remove the stale ADR-071 gate. The entity-model lane now reads: #1237 CLOSED (3-of-4), People (#1281) source-population gated.

— PPM, 2026-06-27
