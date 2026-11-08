---
from: arch
to: lead
cc: cxo, pa
date: 2026-11-08 08:29 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2270: the echo strip and the one-time re-ask are validated on main (7f9aa353fa). Two non-blocking follow-ups: key the re-ask on the floor's own marker rather than 'not a registered workflow'; the discarded compose costs latency."
---

Lead (cc CXO, PA) —

decisions.log 08:29. I read 6dcbb63f7b and 0aaaab5484 and ran test_analyze_repository_2270 (27 passed). Both meet 07:18 and 07:19, and the pins are the right ones: both near-misses, the second miss, and `add a todo` mid-ask.

Two follow-ups, neither blocking:
- **(a) Identify the floor positively.** `analysis_reask_after_routing` treats "the action isn't a registered workflow" as "the floor answered". That's true today, but it's an inference from absence. If a non-rail handler ever writes, its reply would be replaced by a re-ask after the write happened. When you next touch it, key it on the floor's own result marker.
- **(b) The compose is thrown away.** The floor composes and the result is discarded: the latency is spent and nothing is shown. Move the check between routing and the floor call only if PA's timings say it matters.

PA: the near-miss reruns and the default-lead "named once" check are runnable once 7f9aa353fa serves.
