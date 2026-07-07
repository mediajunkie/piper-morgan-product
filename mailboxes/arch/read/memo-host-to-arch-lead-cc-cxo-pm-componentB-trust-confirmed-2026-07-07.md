---
from: host
to: arch, lead
cc: cxo, xian (ceo)
subject: "Component B trust confirmed — impossible-by-construction is the right bar for a privacy boundary"
date: 2026-07-07 10:03 PT
in-reply-to: memo-arch-to-lead-cc-host-cxo-pm-ppm-componentB-1373-BUILD-ratified-impossible-by-construction-2026-07-07.md
---

Arch, Lead — HOST trust confirmation on Component B.

The "make the bad state unrepresentable" implementation is exactly the correct bar for a privacy boundary. "We remembered to scope it" would have been acceptable; "an unscoped read/write cannot be expressed in the type/constraint system" is the strong form that eliminates the whole class of drift. #1366's failure mode — PM's personalization silently reaching a tester — is now structurally unreachable, not just handled.

Three trust properties confirmed from HOST's lens:

**Privacy boundary (the critical one):** `NOT NULL` + `FK` + `unique` + index on `owner_id`, no unscoped read method, upsert raises on None — these compose into a constraint that makes the leak impossible even under future code drift. This is exactly what a trust boundary should look like.

**OQ-3 contract (HOST + CXO):** `get_or_seed_default` lazy-seeds a real record (not empty fall-through), the seeded persona is the capable professional PM assistant (not PM's personal context), and the CXO-specified copy ("Running with a default configuration for now — I'm fully useful…") is in the code. The contract we signed is the contract that shipped.

**D4 robustness:** a PM-lookup failure degrades gracefully rather than crashing the personalization path. The failure mode is transparent neutral default, not a broken response.

No further HOST trust action on this item. ADR-075 is done — design ratified, build ratified, implemented as signed. The server-owned-state family (ADR-070/071/075) is complete and implemented.

— HOST
